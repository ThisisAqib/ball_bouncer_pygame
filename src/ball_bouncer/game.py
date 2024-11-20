import math
import sys
import random
from dataclasses import dataclass

import pygame

from . import utils
from .config import SOUND_FILE
from .ball import Ball, BallConfig
from .boundary import BoundaryArc, BoundaryConfig



@dataclass
class GameConfig:
    """Configuration for the game, including screen size, ball settings, and other parameters."""
    width: int
    height: int
    fps: int
    ball_config: BallConfig
    rotation_speed: tuple[int, int]
    ball_radius: tuple[int, int]
    boundary_width: tuple[int, int]
    boundaries_range: tuple[int, int]


class Game:
    """Class to manage the game logic, rendering, and interaction between the ball and boundaries."""

    def __init__(self, config: GameConfig):
        """
        Initialize the game.

        Args:
            config: GameConfig object containing all settings.
        """
        pygame.init()
        pygame.mixer.init()

        self.config = config
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("Ball Bouncer Game")
        self.clock = pygame.time.Clock()

        # Initialize ball
        self.ball = self._create_ball()
        self._ball_initializations()

        self.test_sound = pygame.mixer.Sound(SOUND_FILE)

        # Initialize boundaries
        self.boundaries = self._create_boundaries()

        self.running = True

    def _ball_initializations(self):
        self.ball.speed_y = self.config.ball_config.initial_speed[1]
        self.config.ball_config.radius = random.randint(self.config.ball_radius[0], self.config.ball_radius[1])
        self.ball.color=utils.generate_non_black_color(brightness_threshold=150)     

    def _create_ball(self) -> Ball:
        """Creates and returns a Ball instance."""
        return Ball(
            config=self.config.ball_config
        )

    def _create_boundaries(self) -> list:
        """Creates and returns a list of boundary arcs with random angles, rotation speeds, and colors."""
        base_radius = min(self.config.width, self.config.height) // 2 - 10
        # Select a random number of boundaries (e.g., between 5 and 10)
        num_boundaries = random.randint(self.config.boundaries_range[0], self.config.boundaries_range[1])

        # Calculate radius step based on the number of boundaries
        radius_step = base_radius // (num_boundaries + 1)

        boundaries = []
        for i in range(num_boundaries):
            radius = base_radius - (i * radius_step)
            if radius <= 0:
                break  # Stop if radius becomes non-positive

            # Calculate start and end angles with some randomness
            start_angle = math.radians(random.randint(0, 180))
            end_angle = start_angle + math.radians(random.randint(270, 300))

            # Randomize rotation speed
            rotation_speed = random.uniform(self.config.rotation_speed[0], self.config.rotation_speed[1])

            # Generate a non-black color for the boundary
            boundary_color = utils.generate_non_black_color()

            boundaries.append(
                BoundaryArc(
                    config=BoundaryConfig(
                        center_x=self.config.width // 2,
                        center_y=self.config.height // 2,
                        radius=radius,
                        start_angle=start_angle,
                        end_angle=end_angle,
                        rotation_speed=rotation_speed,
                        color=boundary_color,
                        width=random.randint(self.config.boundary_width[0], self.config.boundary_width[1]),
                    )
                )
            )

        return boundaries


    def handle_events(self):
        """Handles events such as quitting the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_collisions(self):
        """Checks for collisions between the ball and boundaries."""
        if self.boundaries:
            boundary = self.boundaries[-1]
            if boundary.is_point_outside_boundary(self.ball.position_x, self.ball.position_y, self.config.ball_config.radius):
                self._handle_ball_boundary_collision(boundary)

    def _handle_ball_boundary_collision(self, boundary: BoundaryArc):
        """Handles the ball's collision with a boundary."""
        if boundary.is_point_in_empty_arc(self.ball.position_x, self.ball.position_y):
            self.test_sound.play()

            # Remove the boundary after collision
            self.boundaries.remove(boundary)
        else:
            distance = math.sqrt(
                (self.ball.position_x - boundary.config.center_x) ** 2
                + (self.ball.position_y - boundary.config.center_y) ** 2
            )
            normal_x = (self.ball.position_x - boundary.config.center_x) / distance
            normal_y = (self.ball.position_y - boundary.config.center_y) / distance

            self.ball.reflect_off_boundary(normal_x, normal_y)

    def keep_ball_within_boundary(self):
        """Ensures the ball stays within the active boundary."""
        if self.boundaries:
            boundary = self.boundaries[-1]
            distance = math.sqrt(
                (self.ball.position_x - boundary.config.center_x) ** 2
                + (self.ball.position_y - boundary.config.center_y) ** 2
            )
            if distance + self.config.ball_config.radius > boundary.config.radius:
                excess = distance + self.config.ball_config.radius - boundary.config.radius
                angle = math.atan2(self.ball.position_y - boundary.config.center_y,
                                    self.ball.position_x - boundary.config.center_x)
                self.ball.position_x -= math.cos(angle) * excess
                self.ball.position_y -= math.sin(angle) * excess

    def draw(self):
        """Draws the game objects on the screen."""
        self.screen.fill((0, 0, 0))
        for boundary in self.boundaries:
            boundary.draw(self.screen)

        pygame.draw.circle(self.screen, self.ball.color, (int(self.ball.position_x), int(self.ball.position_y)), self.config.ball_config.radius)

    def restart_game(self):
        """Reset the game state and start over."""
        self.ball.position_x = self.config.width // 2
        self.ball.position_y = self.config.height // 2
        self.ball.speed_x = 0

        self._ball_initializations()

        # Reinitialize boundaries
        self.boundaries = self._create_boundaries()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()

            # Check if all boundaries have been removed and restart the game
            # if not self.boundaries:
            if self.ball.get_distance_from_center(self.config.width // 2, self.config.height // 2) > min(self.config.width, self.config.height):
                self.restart_game()

            self.ball.update_position()
            self.check_collisions()
            self._update_boundaries()
            self.keep_ball_within_boundary()

            self.ball.speed_y += self.config.ball_config.gravity  # Apply gravity

            self.draw()

            pygame.display.flip()
            self.clock.tick(self.config.fps)

        pygame.quit()
        sys.exit()

    def _update_boundaries(self):
        """Updates the angles of all active boundaries."""
        for boundary in self.boundaries:
            boundary.update_angles()
