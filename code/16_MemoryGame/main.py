import random
import sys
import pygame

pygame.init()

PADDING = 20
GAP = 5
CARD_SIZE = 100
ROWS = COLS = 4
FPS = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
WIDTH = HEIGHT = 455
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 40)


class Card:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.width = CARD_SIZE
        self.height = CARD_SIZE
        self.value = value
        self.color = RED
        self.flipped = False
        self.matched = False

    def draw(self, win):
        if self.flipped:
            self.color = GREEN if self.matched else WHITE
            pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

            text = FONT.render(str(self.value), 1, RED)
            win.blit(text, (self.x + self.width//2 - text.get_width() //
                            2, self.y + self.height//2 - text.get_height()//2))
        else:
            pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))

    def is_clicked(self, pos):
        x, y = pos
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)


def start_game():
    nums = list(range(1, ROWS * 2 + 1)) * 2
    random.shuffle(nums)

    cards = []

    for row in range(ROWS):
        y = row * (CARD_SIZE + GAP) + PADDING

        for col in range(COLS):
            x = PADDING + col * (CARD_SIZE + GAP)
            cards.append(Card(x, y, nums.pop()))
    
    return cards


def check_flipped(flipped):
    if len(flipped) == 2:
        if flipped[0].value == flipped[1].value:
            flipped[0].matched = True
            flipped[1].matched = True
            flipped.clear()
        else:
            pygame.time.delay(1000)
            flipped[0].flipped = False
            flipped[1].flipped = False
            flipped.clear()


def main():
    clock = pygame.time.Clock()
    cards = start_game()
    flipped = []
    
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for card in cards:
                    if card.is_clicked(pos) and (not card.flipped):
                        if len(flipped) < 2:
                            card.flipped = True
                            flipped.append(card)

        WIN.fill(BLACK)

        for card in cards:
            card.draw(WIN)
        
        pygame.display.update()
        check_flipped(flipped)
        
        if all(card.matched for card in cards):
            pygame.time.delay(2000)
            cards = start_game()
            flipped.clear()


if __name__ == '__main__':
    main()
