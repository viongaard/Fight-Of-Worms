import pygame
import random

# Инициализация библиотеки Pygame +
pygame.init()

# Настройки экрана +
WIDTH = 1000  # Ширина в пикселях
HEIGHT = 800  # Высота в пикселях
CELL_SIZE = 20  # Размер ячейки сетки

# Цветовая палитра +
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (125, 100, 0)


# Класс игрока +
# Добавить 3 вида картинок вместо цвета (надо поебаться)
class player_worm:
    # Конструктор
    def __init__(self):
        self.color = YELLOW
        self.direction = 'RIGHT'
        self.worm = self.generate_worm()

    # Генерирование червя
    def generate_worm(self):
        x = WIDTH // 2 // CELL_SIZE * CELL_SIZE + 300
        y = HEIGHT // 2 // CELL_SIZE * CELL_SIZE
        return [(x, y)]

    # Передвижение червя
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

    # Проверка на столкновение с едой
    def check_food(self, food):
        if self.worm[0] == food.coords:
            self.worm.append(self.worm[-1])
            food.coords = food.generate_food()
            self.body_worm = self.worm[1:]

    def check_walls(self):
        # Координаты головы червя
        head_x, head_y = self.worm[0]
        # Проверка на нахождение головы в пределах игрового поля
        if not (0 <= head_x < WIDTH and 0 <= head_y < HEIGHT):
            # Если голова выходит за границы, завершить игру
            pygame.quit()
            exit()

    def check_collision(self, other_worm):
        # Проверяем столкновение головы игрока с телом
        for segment in self.get_worm_body():
            if self.worm[0] == segment:
                # Если произошло столкновение с собственным телом, завершаем игру
                pygame.quit()
                exit()
        # Проверяем столкновение головы игрока с телом другого червя
        for segment in other_worm.worm:
            if self.worm[0] == segment:
                # Если произошло столкновение с телом другого червя, завершаем игру
                pygame.quit()
                exit()

    def get_worm_body(self):
        return self.worm[1:]


# Класс бота
# Добавить 3 вида картинок вместо цвета (надо поебаться)
class bot_worm:
    # Конструктор +
    def __init__(self):
        self.color = BROWN
        self.direction = 'LEFT'
        self.worm = self.generate_worm()
        self.target = None

    # Генерирование червя +
    def generate_worm(self):
        x = WIDTH // 2 // CELL_SIZE * CELL_SIZE - 300
        y = HEIGHT // 2 // CELL_SIZE * CELL_SIZE
        return [(x, y)]

    # Установить цель для бота (например, еду)
    def set_target(self, target):
        self.target = target

    # Передвижение червя +
    def move_worm(self):
        if self.target is None:
            return

        # Определяем направление движения к цели (еде)
        target_x, target_y = self.target
        head_x, head_y = self.worm[0]
        if head_x < target_x and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        elif head_x > target_x and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif head_y < target_y and self.direction != 'UP':
            self.direction = 'DOWN'
        elif head_y > target_y and self.direction != 'DOWN':
            self.direction = 'UP'
        #else:
        #    self.random_movement()

        # Двигаем червя в заданном направлении
        self.move_in_direction(self.direction)

    # Движение в заданном направлении
    def move_in_direction(self, direction):
        x, y = self.worm[0]
        if direction == 'UP':
            y -= CELL_SIZE
        elif direction == 'DOWN':
            y += CELL_SIZE
        elif direction == 'LEFT':
            x -= CELL_SIZE
        elif direction == 'RIGHT':
            x += CELL_SIZE
        self.worm = [(x, y)] + self.worm[:-1]

    # Проверка на столкновение с едой +
    def check_food(self, food):
        if self.worm[0] == food.coords:
            self.worm.append(self.worm[-1])
            food.coords = food.generate_food()
            self.body_worm = self.worm[1:]

    def check_walls(self):
        # Координаты головы червя
        head_x, head_y = self.worm[0]
        # Проверяем, находится ли голова в пределах игрового поля
        if not (0 <= head_x < WIDTH and 0 <= head_y < HEIGHT):
            # Если голова выходит за границы, пересоздаем бота
            self.worm = self.generate_worm()

    def check_collision(self, other_worm):
        other_worm_body = other_worm.get_worm_body()  # Получаем тело другого червя без головы
        # Проверяем столкновение головы бота с его собственным телом или телом игрока
        for segment in self.get_worm_body():
            if self.worm[0] == segment:
                # Если произошло столкновение, пересоздаем бота
                self.worm = self.generate_worm()
        for segment in other_worm_body:
            if self.worm[0] == segment:
                # Если произошло столкновение, пересоздаем бота
                self.worm = self.generate_worm()

    def get_worm_body(self):
        return self.worm[1:]

# Класс еды +
# Дополнительно: добавить несколько типов (надо поебаться)
class food:
    # Конструктор
    def __init__(self):
        self.coords = self.generate_food()
        self.color = RED

    # Генерирование еды
    def generate_food(self):
        x = random.randint(1, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(1, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        return (x, y)


# Обработка событий при нажатии клавиш +
def handle_events(player):
    for event in pygame.event.get():
        # Выход из игры +
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

        # Управление червём +
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player.direction != 'DOWN':
                player.direction = 'UP'
            elif event.key == pygame.K_DOWN and player.direction != 'UP':
                player.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and player.direction != 'RIGHT':
                player.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and player.direction != 'LEFT':
                player.direction = 'RIGHT'
    return True


# Отображение объектов +
def draw_objects(player, bot, food, screen):
    # Отображение червя игрока
    for segment in player.worm:
        pygame.draw.rect(screen, player.color,
                         pygame.Rect(segment[0], segment[1], CELL_SIZE,
                                     CELL_SIZE))
    # Отображение червя бота
    for segment in bot.worm:
        pygame.draw.rect(screen, bot.color,
                         pygame.Rect(segment[0], segment[1], CELL_SIZE,
                                     CELL_SIZE))
    # Отображение еды
    pygame.draw.rect(screen, food.color,
                     pygame.Rect(food.coords[0], food.coords[1], CELL_SIZE,
                                 CELL_SIZE))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Бой червей')

    clock = pygame.time.Clock()

    player = player_worm()
    bot = bot_worm()
    apple = food()

    speed = 20

    while True:
        # Обработка событий при нажатии клавиш
        if not handle_events(player):
            return

        # Установка цели для бота (еды)
        bot.set_target(apple.coords)

        # Передвижение червей
        player.move_worm()
        bot.move_worm()

        # Проверка на столкновение со своим телом или телом другого червя
        player.check_collision(bot)
        bot.check_collision(player)
        # Проверка на столкновение с едой
        player.check_food(apple)
        bot.check_food(apple)
        # Проверка на столкновение со стенами
        player.check_walls()
        bot.check_walls()

        # Отрисовка кадра
        screen.fill(BLACK)
        draw_objects(player, bot, apple, screen)
        pygame.display.flip()

        clock.tick(speed)


if __name__ == '__main__':
    main()
