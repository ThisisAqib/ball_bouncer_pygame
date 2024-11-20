"""
Entry point for the Ball Bouncer game.

This script initializes the game configuration and starts the main game loop.
"""
from ball_bouncer.game import Game, GameConfig
from ball_bouncer.ball import BallConfig


if __name__ == "__main__":
    game_config = GameConfig(
        width=1920,
        height=1080,
        fps=30,
        ball_config=BallConfig(
            initial_speed=(0, 25),  # speed_x, speed_y
            elasticity=1.3,
            gravity=3.0,
            speed_adjustment=(20, 75),  # minimum speed, maximum speed
        ),
        rotation_speed=(0.05, 0.2),  # minimum rotation speed, maximum rotation speed
        ball_radius=(5, 15),  # minimum ball radius, maximum ball radius
        boundary_width=(2, 8),  # minimum boundary width, maximum boundary width
        boundaries_range=(5, 15),  # minimum number of boundaries, maximum number of boundaries

    )
    game = Game(game_config)
    game.run()
