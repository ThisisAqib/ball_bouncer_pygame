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


class BoundaryArc:
    """Class representing a rotating arc in the game."""

    def __init__(self, config: BoundaryConfig):
        """
        Initialize the BoundaryArc.

        Args:
            config (BoundaryConfig): Configuration dataclass for the boundary arc.
        """
        config.validate()  # Validate the configuration at initialization
        self.config = config

    def update_angles(self):
        """
        Update the start and end angles of the arc for rotation.

        This method updates the angles by adding the current rotation speed
        to both the start and end angles. The configuration is immutable,
        so a new configuration object is created with the updated angles.
        """
        # Create a new configuration with updated angles
        self.config = self.config.__class__(  # Re-create config to ensure immutability
            **{
                **self.config.__dict__,  # Unpack current configuration
                "start_angle": self.config.start_angle + self.config.rotation_speed,
                "end_angle": self.config.end_angle + self.config.rotation_speed,
            }
        )

    def draw(self, screen):
        """
        Draw the boundary arc on the screen.

        This function uses Pygame's draw.arc() to draw the arc of the boundary
        on the screen. The color of the arc is determined by the color attribute
        of the BoundaryConfig object.

        Args:
            screen (pygame.Surface): The surface to draw the arc on.
        """
        pygame.draw.arc(
            screen,
            self.config.color,
            (
                # Calculate the top-left corner of the arc's bounding box
                self.config.center_x - self.config.radius,
                self.config.center_y - self.config.radius,
                # Calculate the width and height of the arc's bounding box
                self.config.radius * 2,
                self.config.radius * 2,
            ),
            # Calculate the start and end angles for the arc
            self.config.start_angle,
            self.config.end_angle,
            # Set the width of the arc
            self.config.width,
        )

    def is_point_outside_boundary(self, pos_x, pos_y, ball_radius):
        """
        Check if a point is outside the boundary.

        This function calculates the distance from the point to the center of
        the boundary and checks if it is greater than the radius plus the
        radius of the ball. If it is, the point is considered to be outside
        the boundary.

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
        # Check if the distance from the point to the center of the boundary
        # plus the radius of the ball is greater than the radius of the
        # boundary
        return distance + ball_radius > self.config.radius

    def is_point_in_empty_arc(self, pos_x, pos_y):
        """
        Check if a point is in the empty arc region.

        This function is used to detect if the ball is in the empty arc region
        of the boundary. The empty arc region is the part of the boundary
        that is not filled with the arc.

        Args:
            pos_x (float): X-coordinate of the point.
            pos_y (float): Y-coordinate of the point.

        Returns:
            bool: True if the point is in the empty arc region, False otherwise.
        """
        # Calculate the angle of the point relative to the center of the boundary
        angle = math.atan2(pos_y - self.config.center_y, pos_x - self.config.center_x)

        # Normalize the angle to [0, 360)
        angle_degrees = (math.degrees(angle) + 360) % 360

        # Reverse the angle to match the direction of the arc
        angle_degrees = (360 - angle_degrees) % 360

        # Calculate the start and end angles of the arc
        start_deg = (math.degrees(self.config.start_angle) + 360) % 360
        end_deg = (math.degrees(self.config.end_angle) + 360) % 360

        # Check if the point is in the empty arc region
        if start_deg < end_deg:
            return not start_deg <= angle_degrees <= end_deg
        return not (angle_degrees >= start_deg or angle_degrees <= end_deg)
