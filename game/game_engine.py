import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
WINNING_SCORE = 5 

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # --- NEW ATTRIBUTES FOR GAME OVER ---
        self.game_over = False
        self.winner_text = ""
        self.game_over_font = pygame.font.SysFont("Arial", 60) 
        # --- END OF NEW ATTRIBUTES ---

    def handle_input(self):
        # Only handle input if the game is not over
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def check_for_winner(self):
        if self.player_score >= WINNING_SCORE:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= WINNING_SCORE:
            self.winner_text = "AI Wins!"
            self.game_over = True

    def update(self):
        # Only update game logic if the game is not over
        if not self.game_over:
            self.ball.move()

            # Check for collision with the player's paddle
            if self.ball.velocity_x < 0:
                if self.player.rect().colliderect(self.ball.rect()):
                    self.ball.velocity_x *= -1
                    self.ball.x = self.player.rect().right

            # Check for collision with the AI's paddle
            if self.ball.velocity_x > 0:
                if self.ai.rect().colliderect(self.ball.rect()):
                    self.ball.velocity_x *= -1
                    self.ball.x = self.ai.rect().left - self.ball.width

            # Check for scoring
            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
                self.check_for_winner() # Check for a winner after a score
            elif self.ball.x + self.ball.width >= self.width:
                self.player_score += 1
                self.ball.reset()
                self.check_for_winner() # Check for a winner after a score

            # Update the AI's position
            self.ai.auto_track(self.ball, self.height)


    def render(self, screen):
        # Always draw the game elements
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # --- NEW: RENDER GAME OVER TEXT ---
        if self.game_over:
            text_surface = self.game_over_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
            screen.blit(text_surface, text_rect)
        # --- END OF NEW RENDER LOGIC ---