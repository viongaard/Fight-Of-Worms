import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (125, 100, 0)


class Worm:
    def __init__(self, tag):
        self.tag = tag
        self.color = GREEN if tag == 'PLAYER' else YELLOW
        self.start_position = [(WIDTH // 2 // CELL_SIZE * CELL_SIZE,
                                HEIGHT // 2 // CELL_SIZE * CELL_SIZE)]
        self.direction = 'RIGHT' if tag == 'PLAYER' else 'LEFT'
        self.worm = self.generate_worm()
        self.food = self.generate_food()

    def generate_worm(self):
        x, y = self.start_position[0]
        offset = 100 if self.tag == 'PLAYER' else -100
        return [(x + offset, y)]

    def generate_food(self):
        x = random.randint(0, WIDTH // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, HEIGHT // CELL_SIZE) * CELL_SIZE
        return (x, y)

    def move_worm(self):
        x, y = self.worm[0]
        if self.direction == 'UP':
            y -= CELL_SIZE
        elif self.direction == 'DOWN':
            y += CELL_SIZE
        elif self.direction == 'LEFT':
            x -= CELL_SIZE
        elif self.direction == 'RIGHT':
            x += CELL_SIZE
        self.worm = [(x, y)] + self.worm[:-1]

    def draw_elements(self, screen):
        for segment in self.worm:
            pygame.draw.rect(screen, self.color,
                             pygame.Rect(segment[0], segment[1], CELL_SIZE,
                                         CELL_SIZE))
        pygame.draw.rect(screen, BLUE if self.tag == 'PLAYER' else RED,
                         pygame.Rect(self.food[0], self.food[1], CELL_SIZE,
                                     CELL_SIZE))

    def check_food(self):
        if self.worm[0] == self.food:
            self.worm.append(self.worm[-1])
            self.food = self.generate_food()

    def check_walls(self):
        if any(coord < CELL_SIZE or coord >= size - CELL_SIZE for coord, size
               in zip(self.worm[0], (WIDTH, HEIGHT))):
            return True
        return False


def handle_events(player_worm):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN and player_worm.tag == 'PLAYER':
            if event.key == pygame.K_UP and player_worm.direction != 'DOWN':
                player_worm.direction = 'UP'
            elif event.key == pygame.K_DOWN and player_worm.direction != 'UP':
                player_worm.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and player_worm.direction != 'RIGHT':
                player_worm.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and player_worm.direction != 'LEFT':
                player_worm.direction = 'RIGHT'
    return True


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Бой червей')

    clock = pygame.time.Clock()

    player_worm = Worm('PLAYER')
    bot_worm = Worm('BOT')

    while True:
        if not handle_events(player_worm):
            return

        player_worm.move_worm()
        bot_worm.move_worm()

        player_worm.check_food()
        bot_worm.check_food()

        if player_worm.check_walls():
            pygame.quit()
            return
        if bot_worm.check_walls():
            bot_worm.generate_worm()

        screen.fill(BLACK)
        player_worm.draw_elements(screen)
        bot_worm.draw_elements(screen)
        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
