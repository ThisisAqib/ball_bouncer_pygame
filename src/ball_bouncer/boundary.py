"""
Boundary module for the Ball Bouncer Game.

This module defines the BoundaryArc class, representing a rotating arc
with collision detection for the ball.
"""

import math
from dataclasses import dataclass
import pygame


@dataclass(frozen=True)
class BoundaryConfig:
    """Immutable configuration for a BoundaryArc."""

    center_x: float
    center_y: float
    radius: float
    start_angle: float
    end_angle: float
    rotation_speed: float
    color: tuple[int, int, int]
    width: int

    def validate(self):
        """Ensure the configuration is valid."""
        if self.radius <= 0:
            raise ValueError("Radius must be positive.")
        if self.width <= 0:
            raise ValueError("Width must be positive.")
        if not (
            0 <= self.color[0] <= 255
            and 0 <= self.color[1] <= 255
            and 0 <= self.color[2] <= 255
        ):
            raise ValueError("Color values must be between 0 and 255.")


def default_boundary_config() -> BoundaryConfig:
    """Factory function to create a default BoundaryConfig."""
    return BoundaryConfig(
        center_x=400,
        center_y=300,
        radius=200,
        start_angle=0,
        end_angle=2 * math.pi,
        rotation_speed=0.01,
        color=(255, 0, 0),
        width=2,
    )


class BoundaryArc:
    """Class representing a rotating arc in the game."""

    def __init__(self, config: BoundaryConfig = default_boundary_config()):
        """
        Initialize the BoundaryArc.

        Args:
            config (BoundaryConfig): Configuration dataclass for the boundary arc.
        """
        config.validate()  # Validate the configuration at initialization
        self.config = config

    def update_angles(self):
        """Update the arc angles for rotation."""
        self.config = self.config.__class__(
            **{
                **self.config.__dict__,
                "start_angle": self.config.start_angle + self.config.rotation_speed,
                "end_angle": self.config.end_angle + self.config.rotation_speed,
            }
        )

    def draw(self, screen):
        """Draw the boundary arc on the screen."""
        pygame.draw.arc(
            screen,
            self.config.color,
            (
                self.config.center_x - self.config.radius,
                self.config.center_y - self.config.radius,
                self.config.radius * 2,
                self.config.radius * 2,
            ),
            self.config.start_angle,
            self.config.end_angle,
            self.config.width,
        )

    def is_point_outside_boundary(self, pos_x, pos_y, ball_radius):
        """
        Check if a point is outside the boundary.

        Args:
            pos_x (float): X-coordinate of the point.
            pos_y (float): Y-coordinate of the point.
            ball_radius (float): Radius of the ball.

        Returns:
            bool: True if the point is outside the boundary, False otherwise.
        """
        distance = math.sqrt(
            (pos_x - self.config.center_x) ** 2 + (pos_y - self.config.center_y) ** 2
        )
        return distance + ball_radius > self.config.radius

    def is_point_in_empty_arc(self, pos_x, pos_y):
        """
        Check if a point is in the empty arc region.

        Args:
            pos_x (float): X-coordinate of the point.
            pos_y (float): Y-coordinate of the point.

        Returns:
            bool: True if the point is in the empty arc region, False otherwise.
        """
        angle = math.atan2(pos_y - self.config.center_y, pos_x - self.config.center_x)
        angle_degrees = (math.degrees(angle) + 360) % 360
        angle_degrees = (360 - angle_degrees) % 360
        start_deg = (math.degrees(self.config.start_angle) + 360) % 360
        end_deg = (math.degrees(self.config.end_angle) + 360) % 360

        if start_deg < end_deg:
            return not start_deg <= angle_degrees <= end_deg
        return not (angle_degrees >= start_deg or angle_degrees <= end_deg)
