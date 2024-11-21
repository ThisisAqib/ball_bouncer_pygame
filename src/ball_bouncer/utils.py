"""
Utility functions for the Ball Bouncer Game.
"""

import random


def generate_non_black_color(brightness_threshold=100):
    """
    Generate a random RGB color that is not too dark (perceived brightness > threshold).

    Args:
        brightness_threshold (int): Minimum brightness for the color. Defaults to 100.

    Returns:
        tuple: A tuple representing an RGB color (r, g, b) with values between 0 and 255.
    """
    while True:
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        brightness = (
            0.299 * red + 0.587 * green + 0.114 * blue
        )  # Perceived brightness formula
        if brightness > brightness_threshold:
            return red, green, blue
