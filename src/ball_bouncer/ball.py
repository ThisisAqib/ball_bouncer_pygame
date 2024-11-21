"""
Ball module for the Ball Bouncer Game.

This module defines the Ball class, representing a ball that interacts with boundaries
and exhibits realistic bouncing behavior with configurable properties such as gravity,
elasticity, and speed.
"""

import random
import math
from dataclasses import dataclass


@dataclass
class BallConfig:
    """
    Configuration class for Ball properties.
    """

    initial_speed: tuple[float, float] = (0, 20)
    speed_adjustment: tuple[int, int] = ((10, 75),)  # minimum speed, maximum speed
    initial_position: tuple[float, float] = (0, 0)  # Initial position
    color: tuple[int, int, int] = (255, 0, 0)
    radius: int = 5
    elasticity: float = 1.0
    gravity: float = 2.0


class Ball:
    """Class representing the ball in the game."""

    def __init__(self, config=BallConfig()):
        """
        Initializes a new ball.

        Parameters:
        - config (BallConfig): Configuration object for ball properties.
        """
        # Use provided config or default values
        self.position_x, self.position_y = config.initial_position
        self.speed_x, self.speed_y = config.initial_speed
        self.config = config

    def update_position(self):
        """Update the ball's position based on its current speed."""
        self.position_x += self.speed_x
        self.position_y += self.speed_y

    def reflect_off_boundary(self, normal_x, normal_y):
        """Reflect the ball off a boundary defined by a normal vector."""
        dot_product = self.speed_x * normal_x + self.speed_y * normal_y
        self.speed_x -= 2 * dot_product * normal_x
        self.speed_y -= 2 * dot_product * normal_y

        # Apply elasticity: Reduce the speed after bouncing
        self.speed_x *= self.config.elasticity
        self.speed_y *= self.config.elasticity

        # Add randomness to the bounce to avoid repetitive patterns
        self.randomize_bounce()

    def randomize_bounce(self):
        """Introduce randomness in the ball's bounce direction and speed."""
        random_speed_factor = random.uniform(0.8, 1.2)  # Slight random speed variation
        random_angle_offset = random.uniform(
            -math.pi / 8, math.pi / 8
        )  # Angle variation

        # Apply randomization to speed and angle
        angle = math.atan2(self.speed_y, self.speed_x) + random_angle_offset
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2) * random_speed_factor

        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed

        # Ensure the speed stays within a reasonable range
        self.adjust_speed()

    def adjust_speed(self):
        """
        Ensure the ball's speed stays within a specified range.
        """
        if abs(self.speed_x) < self.config.speed_adjustment[0]:
            self.speed_x *= random.uniform(1.5, 3.0)
        elif abs(self.speed_x) > self.config.speed_adjustment[1]:
            self.speed_x *= random.uniform(0.5, 0.8)

        if abs(self.speed_y) < self.config.speed_adjustment[0]:
            self.speed_y *= random.uniform(1.5, 3.0)
        elif abs(self.speed_y) > self.config.speed_adjustment[0]:
            self.speed_y *= random.uniform(0.5, 0.8)

    def get_distance_from_center(self, center_x, center_y):
        """
        Calculate the distance from the ball's position to a specified center.

        Parameters:
        - center_x (float): x-coordinate of the center.
        - center_y (float): y-coordinate of the center.

        Returns:
        - float: The distance from the ball to the center.
        """
        return math.sqrt(
            (self.position_x - center_x) ** 2 + (self.position_y - center_y) ** 2
        )
