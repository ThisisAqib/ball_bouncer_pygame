"""
Game module for the Ball Bouncer Game.

This module defines the `Game` class, which encapsulates the gameplay logic, 
rendering, and interactions between the ball and the boundaries.

Classes:
    GameConfig: Configuration data for the game, including screen settings, 
                ball properties, and boundary properties.
    Game: Core class that manages the game lifecycle, rendering, and interactions.
"""

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
    """
    Holds configuration settings for the Ball Bouncer Game.

    Attributes:
        width (int): Width of the game window (pixels).
        height (int): Height of the game window (pixels).
        fps (int): Target frames per second for game rendering and updates.
        ball_config (BallConfig): Configuration for the ball's properties.
        rotation_speed (tuple[int, int]): Range of rotation speeds for boundaries.
        ball_radius (tuple[int, int]): Minimum and maximum ball radius.
        boundary_width (tuple[int, int]): Minimum and maximum width of boundaries.
        boundaries_range (tuple[int, int]): Minimum and maximum number of boundaries.
    """

    width: int
    height: int
    fps: int
    ball_config: BallConfig
    rotation_speed: tuple[int, int]
    ball_radius: tuple[int, int]
    boundary_width: tuple[int, int]
    boundaries_range: tuple[int, int]


class Game:
    """
    Manages the Ball Bouncer Game, including game logic, rendering,
    and interactions.

    The Game class orchestrates the movement of the ball, interactions
    with boundaries, and game state transitions. It handles collision
    detection, boundary management, and graphical updates.
    """

    def __init__(self, config: GameConfig):
        """
        Initializes the game with the provided configuration.

        Args:
            config (GameConfig): The configuration object containing all game settings.
        """
        # Initialize Pygame and mixer
        pygame.init()  # pylint: disable=no-member
        pygame.mixer.init()

        # Store game configuration
        self.config = config
        self.running = True

        # Set up the game display
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("Ball Bouncer Game")
        self.clock = pygame.time.Clock()

        # Initialize game objects
        self.ball = self._create_ball()
        self._initialize_ball_properties()

        # Load sound effects
        self.test_sound = pygame.mixer.Sound(SOUND_FILE)

        # Initialize boundaries
        self.boundaries = self._create_boundaries()

    def _initialize_ball_properties(self):
        """Randomly initializes the ball's properties such as radius and color."""
        self.ball.speed_y = self.config.ball_config.initial_speed[1]
        self.config.ball_config.radius = random.randint(
            self.config.ball_radius[0], self.config.ball_radius[1]
        )
        self.ball.color = utils.generate_non_black_color(brightness_threshold=150)

    def _create_ball(self) -> Ball:
        """Creates and returns a Ball instance."""
        return Ball(config=self.config.ball_config)

    def _create_boundaries(self) -> list[BoundaryArc]:
        """
        Creates and returns a list of boundary arcs with random properties.

        Returns:
            list[BoundaryArc]: A list of boundary arcs initialized with random angles,
                               rotation speeds, and colors.
        """
        base_radius = min(self.config.width, self.config.height) // 2 - 10
        num_boundaries = random.randint(
            self.config.boundaries_range[0], self.config.boundaries_range[1]
        )
        radius_step = base_radius // (num_boundaries + 1)

        boundaries = []
        for i in range(num_boundaries):
            radius = base_radius - (i * radius_step)
            if radius <= 0:
                break  # Avoid non-positive radii

            start_angle = math.radians(random.randint(0, 180))
            end_angle = start_angle + math.radians(random.randint(270, 300))
            rotation_speed = random.uniform(
                self.config.rotation_speed[0], self.config.rotation_speed[1]
            )
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
                        width=random.randint(
                            self.config.boundary_width[0], self.config.boundary_width[1]
                        ),
                    )
                )
            )

        return boundaries

    def handle_events(self):
        """Processes user input and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.running = False

    def check_collisions(self):
        """Checks for and processes collisions between the ball and the boundaries."""
        if self.boundaries:
            boundary = self.boundaries[-1]
            if boundary.is_point_outside_boundary(
                self.ball.position_x,
                self.ball.position_y,
                self.config.ball_config.radius,
            ):
                self._handle_ball_boundary_collision(boundary)

    def _handle_ball_boundary_collision(self, boundary: BoundaryArc):
        """
        Processes a collision between the ball and a boundary.

        If the ball collides with an empty arc, a sound is played, and the boundary is removed.
        Otherwise, the ball is reflected off the boundary.
        """
        if boundary.is_point_in_empty_arc(self.ball.position_x, self.ball.position_y):
            self.test_sound.play()
            self.boundaries.remove(boundary)
        else:
            distance = math.hypot(
                self.ball.position_x - boundary.config.center_x,
                self.ball.position_y - boundary.config.center_y,
            )
            normal_x = (self.ball.position_x - boundary.config.center_x) / distance
            normal_y = (self.ball.position_y - boundary.config.center_y) / distance
            self.ball.reflect_off_boundary(normal_x, normal_y)

    def keep_ball_within_boundary(self):
        """Ensures the ball remains within the active boundary."""
        if self.boundaries:
            boundary = self.boundaries[-1]
            distance = math.hypot(
                self.ball.position_x - boundary.config.center_x,
                self.ball.position_y - boundary.config.center_y,
            )
            if distance + self.config.ball_config.radius > boundary.config.radius:
                excess = (
                    distance + self.config.ball_config.radius - boundary.config.radius
                )
                angle = math.atan2(
                    self.ball.position_y - boundary.config.center_y,
                    self.ball.position_x - boundary.config.center_x,
                )
                self.ball.position_x -= math.cos(angle) * excess
                self.ball.position_y -= math.sin(angle) * excess

    def draw(self):
        """Renders the game objects onto the screen."""
        self.screen.fill((0, 0, 0))  # Clear the screen
        for boundary in self.boundaries:
            boundary.draw(self.screen)

        pygame.draw.circle(
            self.screen,
            self.ball.color,
            (int(self.ball.position_x), int(self.ball.position_y)),
            self.config.ball_config.radius,
        )

    def restart_game(self):
        """Resets the game state to start a new session."""
        self.ball.position_x = self.config.width // 2
        self.ball.position_y = self.config.height // 2
        self.ball.speed_x = 0
        self._initialize_ball_properties()
        self.boundaries = self._create_boundaries()

    def _update_boundaries(self):
        """Updates the angles of the rotating boundaries."""
        for boundary in self.boundaries:
            boundary.update_angles()

    def run(self):
        """
        Main game loop.

        This loop handles events, updates the game state, and redraws the screen.
        """
        while self.running:
            self.handle_events()
            if self.ball.get_distance_from_center(
                self.config.width // 2, self.config.height // 2
            ) > min(self.config.width, self.config.height):
                self.restart_game()

            self.ball.update_position()
            self.check_collisions()
            self._update_boundaries()
            self.keep_ball_within_boundary()

            self.ball.speed_y += self.config.ball_config.gravity  # Apply gravity

            self.draw()
            pygame.display.flip()
            self.clock.tick(self.config.fps)

        pygame.quit()  # pylint: disable=no-member
        sys.exit()
