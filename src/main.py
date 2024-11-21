"""
Entry point for the Ball Bouncer game.

This script initializes the game configuration and starts the main game loop.
"""

# Import necessary classes and configurations
from ball_bouncer.game import Game, GameConfig
from ball_bouncer.ball import BallConfig

# Main entry point of the program
if __name__ == "__main__":
    # Create the game configuration
    game_config = GameConfig(
        # Screen dimensions
        width=1280,  # The width of the game window in pixels
        height=720,  # The height of the game window in pixels
        fps=30,  # Frames per second for smooth rendering and game updates
        # Ball-specific configuration
        ball_config=BallConfig(
            initial_speed=(
                0,
                25,
            ),  # Initial speed of the ball in the x and y directions
            elasticity=1.3,  # How much the ball "bounces back" after hitting a boundary
            gravity=3.0,  # Downward acceleration applied to the ball (higher means stronger gravity)
            speed_adjustment=(
                20,
                75,
            ),  # Minimum and maximum speed adjustments for the ball after collisions
        ),
        # Number of boundaries in the game
        boundaries_range=(
            5,
            15,
        ),  # Range for the number of boundaries (minimum and maximum)
        # Rotation speed of boundaries
        rotation_speed=(0.05, 0.2),  # Range for boundary rotation speed (min and max)
        # Ball radius configuration
        ball_radius=(5, 15),  # Range for the ball's radius (smallest and largest size)
        # Boundary width configuration
        boundary_width=(2, 8),  # Range for the width of each boundary (thin to thick)
    )

    # Initialize the game with the defined configuration
    game = Game(game_config)

    # Start the game loop
    game.run()
