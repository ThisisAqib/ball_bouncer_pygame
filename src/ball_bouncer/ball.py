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

    position_x: float = 0
    position_y: float = 0
    speed_x: float = 0
    speed_y: float = 15
    radius: int = 5
    elasticity: float = 1.0
    gravity: float = 2.0


@dataclass
class BallSettings:
    """
    Settings for the ball, including its size, speed, and physics properties.
    """

    radius: int
    initial_speed: int
    elasticity: float
    gravity: float


class Ball:
    """Class representing the ball in the game."""

    def __init__(self, config=BallConfig()):
        """
        Initializes a new ball.

        Parameters:
        - config (BallConfig): Configuration object for ball properties.
        """
        # Use provided config or default values
        self.position_x = config.position_x
        self.position_y = config.position_y
        self.speed_x = config.speed_x
        self.speed_y = config.speed_y
        self.radius = config.radius
        self.elasticity = config.elasticity
        self.gravity = config.gravity

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
        self.speed_x *= self.elasticity
        self.speed_y *= self.elasticity

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

    def adjust_speed(self, min_speed=10, max_speed=75):
        """
        Ensure the ball's speed stays within a specified range.

        Parameters:
        - min_speed (float): Minimum allowable speed.
        - max_speed (float): Maximum allowable speed.
        """
        if abs(self.speed_x) < min_speed:
            self.speed_x *= random.uniform(1.5, 3.0)
        elif abs(self.speed_x) > max_speed:
            self.speed_x *= random.uniform(0.5, 0.8)

        if abs(self.speed_y) < min_speed:
            self.speed_y *= random.uniform(1.5, 3.0)
        elif abs(self.speed_y) > max_speed:
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

    def get_angle_from_center(self, center_x, center_y):
        """
        Calculate the angle between the ball and a specified center.

        Parameters:
        - center_x (float): x-coordinate of the center.
        - center_y (float): y-coordinate of the center.

        Returns:
        - float: The angle in radians.
        """
        return math.atan2(self.position_y - center_y, self.position_x - center_x)
