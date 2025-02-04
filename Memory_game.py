import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_SPACING = 20
START_X = 150
START_Y = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BG = (26, 76, 59)
CARD_BACK = (51, 102, 204)
MONSTER_COLORS = {
    1: (255, 0, 0),      # Red
    2: (0, 255, 0),      # Green
    3: (255, 0, 255),    # Pink
    4: (255, 153, 0),    # Orange
    5: (153, 0, 255),    # Purple
    6: (0, 255, 255)     # Cyan
}

# Setup display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Card Matching Game')

class Card:
    def __init__(self, x, y, card_type):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.type = card_type
        self.is_flipped = False
        self.is_matched = False

    def draw(self, screen):
        if self.is_flipped:
            # Draw card front
            pygame.draw.rect(screen, WHITE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)
            
            # Draw monster shape based on type
            center_x = self.rect.x + CARD_WIDTH // 2
            center_y = self.rect.y + CARD_HEIGHT // 2
            color = MONSTER_COLORS[self.type]
            
            if self.type == 1:  # Circle
                pygame.draw.circle(screen, color, (center_x, center_y), 30)
            elif self.type == 2:  # Triangle
                points = [(center_x, center_y - 30),
                         (center_x + 30, center_y + 30),
                         (center_x - 30, center_y + 30)]
                pygame.draw.polygon(screen, color, points)
            elif self.type == 3:  # Star (simplified as circle)
                pygame.draw.circle(screen, color, (center_x, center_y), 30)
            elif self.type == 4:  # Rectangle
                pygame.draw.rect(screen, color, (center_x - 25, center_y - 25, 50, 50))
            elif self.type == 5:  # Diamond
                points = [(center_x, center_y - 30),
                         (center_x + 30, center_y),
                         (center_x, center_y + 30),
                         (center_x - 30, center_y)]
                pygame.draw.polygon(screen, color, points)
            else:  # type 6 - Circle with border
                pygame.draw.circle(screen, color, (center_x, center_y), 30)
                pygame.draw.circle(screen, BLACK, (center_x, center_y), 30, 4)
        else:
            # Draw card back
            pygame.draw.rect(screen, CARD_BACK, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)

class Game:
    def __init__(self):
        self.cards = []
        self.selected_card = None
        self.matches_found = 0
        self.can_click = True
        self.game_won = False
        self.setup_cards()
        
        # Setup font for score
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)

    def setup_cards(self):
        card_types = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        random.shuffle(card_types)
        
        card_index = 0
        for row in range(3):
            for col in range(4):
                x = START_X + col * (CARD_WIDTH + CARD_SPACING)
                y = START_Y + row * (CARD_HEIGHT + CARD_SPACING)
                self.cards.append(Card(x, y, card_types[card_index]))
                card_index += 1

    def handle_click(self, pos):
        if not self.can_click or self.game_won:
            return

        for card in self.cards:
            if card.rect.collidepoint(pos) and not card.is_flipped:
                self.flip_card(card)
                break

    def flip_card(self, card):
        card.is_flipped = True

        if not self.selected_card:
            self.selected_card = card
        else:
            self.can_click = False
            if self.selected_card.type == card.type:
                # Match found
                self.matches_found += 1
                self.selected_card = None
                self.can_click = True

                if self.matches_found == 6:
                    self.game_won = True
            else:
                # No match
                current_card = card
                selected_card = self.selected_card
                pygame.display.flip()
                time.sleep(1)  # Show cards for 1 second
                
                current_card.is_flipped = False
                selected_card.is_flipped = False
                self.selected_card = None
                self.can_click = True

    def draw(self, screen):
        screen.fill(GREEN_BG)
        
        # Draw score
        score_text = self.font.render(f'Matches: {self.matches_found}', True, WHITE)
        screen.blit(score_text, (16, 16))
        
        # Draw cards
        for card in self.cards:
            card.draw(screen)
            
        # Draw win message
        if self.game_won:
            win_text = self.big_font.render('You Win!', True, WHITE)
            text_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(win_text, text_rect)

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
