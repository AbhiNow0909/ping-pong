import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        # --- NEW: HANDLE GAME OVER EXIT ---
        if engine.game_over:
            pygame.display.flip() # Update the screen one last time to show the message
            pygame.time.delay(3000) # Wait for 3 seconds (3000 milliseconds)
            running = False # End the game loop
        else:
            pygame.display.flip() # Normal screen update
        # --- END OF NEW EXIT LOGIC ---

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()