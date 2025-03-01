import pygame
import random
import time


# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танчики")

# Загрузка изображения цели
target_image = pygame.image.load('resource/target.jpg')  # Укажите путь к вашему изображению
target_image = pygame.transform.scale(target_image, (30, 30))  # Масштабирование изображения до нужного размера

# Цвета
DIFFIULTIES = {'легкий уровень': 1, 'средний уровень': 3, 'высокий уровень': 4}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс танка
class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 40
        self.height = 40
        self.color = RED

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Ограничение движения танка в нижней половине экрана
        if 0 <= new_x <= WIDTH - self.width:
            self.x = new_x
        if HEIGHT // 2 <= new_y <= HEIGHT - self.height:
            self.y = new_y

# Класс пули
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 5
        self.color = BLACK

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y -= self.speed

# Класс цели
class Target(pygame.sprite.Sprite):
    def __init__(self, speed):
        global DIFFIULTIES
        super().__init__()
        self.image = target_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(50, 150)
        self.speed = DIFFIULTIES[speed] # Скорость движения

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.speed

        if self.rect.x <= 0 or self.rect.x + self.rect.width >= WIDTH:
            self.speed = -self.speed  # Изменение направления

    def check_collision(self, other_target):
        return self.rect.colliderect(other_target.rect)


# Основной цикл игры
def main(diff='легкий уровень'):
    while True:
        tank = Tank(WIDTH // 2, HEIGHT - 60)
        bullets = []
        targets = [Target(diff) for _ in range(5)]
        shots_fired = 0
        targets_hit = 0
        start_time = pygame.time.get_ticks()  # Время начала игры

        clock = pygame.time.Clock()
        running = True

        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(tank.x + tank.width // 2, tank.y))
                        shots_fired += 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                tank.move(-1, 0)
            if keys[pygame.K_RIGHT]:
                tank.move(1, 0)
            if keys[pygame.K_UP]:
                tank.move(0, -1)
            if keys[pygame.K_DOWN]:
                tank.move(0, 1)

            # Движение пуль
            for bullet in bullets[:]:
                bullet.move()
                bullet.draw()

                if bullet.y < 0:
                    bullets.remove(bullet)

            # Движение и отрисовка целей
            for target in targets[:]:
                target.move()
                target.draw()

                # Проверка столкновений между целями
                for other_target in targets:
                    if target != other_target and target.check_collision(other_target):
                        target.speed = -target.speed
                        other_target.speed = -other_target.speed

            # Проверка попаданий
            for bullet in bullets[:]:
                for target in targets[:]:
                    if (target.rect.x < bullet.x < target.rect.x + target.rect.width and
                        target.rect.y < bullet.y < target.rect.y + target.rect.height):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if target in targets:
                            targets.remove(target)
                            targets.append(Target(diff))
                            targets_hit += 1

            # Отрисовка танка
            tank.draw()

            # Отображение счетчиков
            font = pygame.font.SysFont(None, 25)  # Уменьшил размер шрифта
            shots_text = font.render(f"Выстрелы: {shots_fired}", True, BLACK)
            hits_text = font.render(f"Сбито: {targets_hit}/15", True, BLACK)
            time_elapsed = (pygame.time.get_ticks() - start_time) // 1000
            time_text = font.render(f"Время: {time_elapsed} сек", True, BLACK)

            screen.blit(shots_text, (10, 5))
            screen.blit(hits_text, (10, 25))
            screen.blit(time_text, (10, 45))

            pygame.display.flip()
            clock.tick(30)

            # Проверка на победу
            if targets_hit >= 15:
                screen.fill(WHITE)
                win_text = pygame.font.SysFont(None, 50).render("Победа!", True, GREEN)
                screen.blit(win_text, (WIDTH // 2 - 50, HEIGHT // 2 - 25))
                pygame.display.flip()
                time.sleep(3)  # Пауза перед перезапуском
                break  # Перезапускаем игру