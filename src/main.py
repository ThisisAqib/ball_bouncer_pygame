"""
Entry point for the Ball Bouncer game.

This script initializes the game configuration and starts the main game loop.
"""
import math
from ball_bouncer.game import Game, GameConfig, BallSettings


if __name__ == "__main__":
    game_config = GameConfig(
        width=800,
        height=600,
        ball_settings=BallSettings(
            radius=5,
            initial_speed=25,
            elasticity=1.0,
            gravity=2.0,
        ),
        speed_adjustment_min=5,
        speed_adjustment_max=50,
        angle_speed=math.radians(5),
    )
    game = Game(game_config)
    game.run()
