import pygame
import random
import time
#qwerr
# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танчики")

# Цвета
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
class Target:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = random.randint(50, 150)
        self.width = 30
        self.height = 30
        self.color = BLACK
        self.speed = random.choice([2, 3])  # Скорость движения

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.speed = -self.speed  # Изменение направления

# Основной цикл игры
def main():
    while True:
        tank = Tank(WIDTH // 2, HEIGHT - 60)
        bullets = []
        targets = [Target() for _ in range(5)]
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

            # Проверка попаданий
            for bullet in bullets[:]:
                for target in targets[:]:
                    if (target.x < bullet.x < target.x + target.width and
                        target.y < bullet.y < target.y + target.height):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if target in targets:
                            targets.remove(target)
                            targets.append(Target())
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

if __name__ == "__main__":
    main()
