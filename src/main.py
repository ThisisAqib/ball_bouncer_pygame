"""
Entry point for the Ball Bouncer game.

This script initializes the game configuration and starts the main game loop.
"""
import math
from ball_bouncer.game import Game, GameConfig, BallSettings


if __name__ == "__main__":
    game_config = GameConfig(
        width=1920,
        height=1080,
        ball_settings=BallSettings(
            radius=5,
            initial_speed=50,
            elasticity=1.1,
            gravity=2.0,
        ),
        speed_adjustment_min=20,
        speed_adjustment_max=100,
        angle_speed=math.radians(5),
    )
    game = Game(game_config)
    game.run()
