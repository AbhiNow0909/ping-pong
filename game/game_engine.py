import pygame
from .paddle import Paddle
from .ball import Ball

# Initialize the mixer before creating the GameEngine class
pygame.mixer.init()

# --- Constants ---
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # --- Game Objects ---
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # --- State Management ---
        self.game_state = "playing"  # Can be "playing" or "replay"
        self.winning_score = 5       # Default winning score
        self.winner = None           # To store who won ("Player" or "AI")
        self.should_quit = False     # Flag to signal the main loop to exit

        # --- Scoring & Text ---
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 24)

        # --- Sound Initialization ---
        try:
            self.paddle_hit_sound = pygame.mixer.Sound('sounds/paddle_hit.wav')
            self.wall_bounce_sound = pygame.mixer.Sound('sounds/wall_bounce.wav')
            self.score_sound = pygame.mixer.Sound('sounds/score.wav')
        except pygame.error as e:
            print(f"Error loading sound file: {e}")
            # Create silent sound objects so the game doesn't crash if files are missing
            self.paddle_hit_sound = pygame.mixer.Sound(buffer=b'')
            self.wall_bounce_sound = pygame.mixer.Sound(buffer=b'')
            self.score_sound = pygame.mixer.Sound(buffer=b'')

    def reset_game(self, new_winning_score):
        """Resets the game to a fresh start with a new score target."""
        self.winning_score = new_winning_score
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50
        self.game_state = "playing"

    def process_input(self, event):
        """Handles single-press inputs based on the current game state."""
        if self.game_state == "replay":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.reset_game(3)
                elif event.key == pygame.K_5:
                    self.reset_game(5)
                elif event.key == pygame.K_7:
                    self.reset_game(7)
                elif event.key == pygame.K_ESCAPE:
                    self.should_quit = True

    def update(self):
        """Updates game objects only if the game is in the 'playing' state."""
        if self.game_state != "playing":
            return  # Do nothing if the game is not active

        self.ball.move()

        # Wall collision (top/bottom)
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height:
            self.ball.velocity_y *= -1
            self.wall_bounce_sound.play()

        # Paddle Collisions
        if self.ball.velocity_x < 0 and self.player.rect().colliderect(self.ball.rect()):
            self.ball.velocity_x *= -1
            self.ball.x = self.player.rect().right
            self.paddle_hit_sound.play()
        if self.ball.velocity_x > 0 and self.ai.rect().colliderect(self.ball.rect()):
            self.ball.velocity_x *= -1
            self.ball.x = self.ai.rect().left - self.ball.width
            self.paddle_hit_sound.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.score_sound.play()
            self.ball.reset()

        # AI Movement
        self.ai.auto_track(self.ball, self.height)

        # Player Movement (continuous check)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

        # Check for winner
        if self.player_score >= self.winning_score:
            self.winner = "Player"
            self.game_state = "replay"
        elif self.ai_score >= self.winning_score:
            self.winner = "AI"
            self.game_state = "replay"

    def render(self, screen):
        """Draws everything to the screen based on the game state."""
        # Common elements drawn in all states
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # State-specific rendering
        if self.game_state == "playing":
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 20))
            screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width()//2, 20))

        elif self.game_state == "replay":
            # Display winner text
            winner_text_surf = self.game_over_font.render(f"{self.winner} Wins!", True, WHITE)
            winner_rect = winner_text_surf.get_rect(center=(self.width/2, self.height/2 - 100))
            screen.blit(winner_text_surf, winner_rect)

            # Display menu options
            options = [
                "Play again:",
                "[3] - Best of 3",
                "[5] - Best of 5",
                "[7] - Best of 7",
                "[ESC] - Exit"
            ]
            for i, option in enumerate(options):
                text_surf = self.menu_font.render(option, True, WHITE)
                text_rect = text_surf.get_rect(center=(self.width/2, self.height/2 + i*40))
                screen.blit(text_surf, text_rect)