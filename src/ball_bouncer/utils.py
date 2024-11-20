import random

def generate_non_black_color(brightness_threshold=100):
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        brightness = 0.299 * r + 0.587 * g + 0.114 * b  # Perceived brightness formula
        if brightness > brightness_threshold:  # Adjust threshold as needed
            return (r, g, b)
