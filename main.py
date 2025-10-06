# main.py

import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Create the game engine
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        # Event handling is now passed to the engine
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Let the engine handle game-specific input
            engine.process_input(event)

        # Check the engine's quit flag
        if engine.should_quit:
            running = False

        # Clear screen
        SCREEN.fill(BLACK)
        
        # Update and Render game state
        engine.update()
        engine.render(SCREEN)

        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()