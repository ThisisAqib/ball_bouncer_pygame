"""
Game module for the Ball Bouncer Game.

This module handles the game logic, rendering, and interaction between
the ball and the boundary arc.
"""
import math
import sys
from dataclasses import dataclass

import pygame

from .config import SOUND_FILE, RED, BLACK
from .ball import Ball, BallConfig, BallSettings
from .boundary import BoundaryArc, BoundaryConfig


@dataclass
class GameConfig:
    """
    Configuration for the game, including screen size, ball settings, and other parameters.
    """

    width: int
    height: int
    ball_settings: BallSettings
    speed_adjustment_min: int
    speed_adjustment_max: int
    angle_speed: float


class Game:
    """Class to manage the game logic and rendering."""

    def __init__(self, config: GameConfig):
        """
        Initialize the game.

        Args:
            config: GameConfig object containing all settings.
        """
        pygame.init()  # pylint: disable=no-member
        pygame.mixer.init()

        self.config = config
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("Ball Bouncer Game")
        self.clock = pygame.time.Clock()

        self.ball = Ball(
            config=BallConfig(
                position_x=config.width // 2,
                position_y=config.height // 2,
                speed_x=0,
                speed_y=config.ball_settings.initial_speed,
                radius=config.ball_settings.radius,
                elasticity=config.ball_settings.elasticity,
                gravity=config.ball_settings.gravity,
            )
        )

        self.test_sound = pygame.mixer.Sound(SOUND_FILE)

        self.boundary = BoundaryArc(
            config=BoundaryConfig(
                center_x=config.width // 2,
                center_y=config.height // 2,
                radius=min(config.width, config.height) // 2 - 10,
                start_angle=math.radians(95),
                end_angle=math.radians(390),
                rotation_speed=config.angle_speed,
                color=RED,
                width=2,
            )
        )

        self.running = True

    def handle_events(self):
        """Handle the events such as quitting the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.running = False

    def check_collisions(self):
        """Check for collisions between the ball and the boundary."""
        if self.boundary.is_point_outside_boundary(
            self.ball.position_x, self.ball.position_y, self.config.ball_settings.radius
        ):
            distance = math.sqrt(
                (self.ball.position_x - self.boundary.config.center_x) ** 2
                + (self.ball.position_y - self.boundary.config.center_y) ** 2
            )
            normal_x = (self.ball.position_x - self.boundary.config.center_x) / distance
            normal_y = (self.ball.position_y - self.boundary.config.center_y) / distance

            self.ball.reflect_off_boundary(normal_x, normal_y)

            # Check if the ball is in the empty arc
            if self.boundary.is_point_in_empty_arc(
                self.ball.position_x, self.ball.position_y
            ):
                self.test_sound.play()

    def keep_ball_within_boundary(self):
        """Ensure the ball stays within the boundary."""
        distance = math.sqrt(
            (self.ball.position_x - self.boundary.config.center_x) ** 2
            + (self.ball.position_y - self.boundary.config.center_y) ** 2
        )
        if distance + self.config.ball_settings.radius > self.boundary.config.radius:
            excess = (
                distance
                + self.config.ball_settings.radius
                - self.boundary.config.radius
            )
            angle = math.atan2(
                self.ball.position_y - self.boundary.config.center_y,
                self.ball.position_x - self.boundary.config.center_x,
            )
            self.ball.position_x -= math.cos(angle) * excess
            self.ball.position_y -= math.sin(angle) * excess

    def draw(self):
        """Draw the game objects on the screen."""
        self.screen.fill(BLACK)
        self.boundary.draw(self.screen)
        pygame.draw.circle(
            self.screen,
            RED,
            (int(self.ball.position_x), int(self.ball.position_y)),
            self.config.ball_settings.radius,
        )

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()

            self.ball.update_position()
            self.check_collisions()
            self.boundary.update_angles()
            self.keep_ball_within_boundary()

            # Apply gravity to the ball
            self.ball.speed_y += self.config.ball_settings.gravity

            self.draw()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()  # pylint: disable=no-member
        sys.exit()
