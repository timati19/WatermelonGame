import random
import sys

import pygame


def terminate():
    pygame.quit()
    sys.exit()

# класс шара
class Ball:
    def __init__(self, x, radius):
        self.fall = False
        self.motion = True
        self.x = x
        self.y = radius
        self.radius = radius
        self.deathline = 101
        self.speed = 5

    # функция движения шара
    def update(self):
        if (self.y + self.radius) >= height:
            pass
        else:
            self.y += self.speed

    # функция отрисовки шара
    def draw(self):
        pygame.draw.circle(screen, 'green', (self.x, self.y), self.radius)
        pygame.draw.line(screen, 'red', (0, self.deathline), (width, self.deathline), 5)

    # функция получения радиуса
    def print_radius(self):
        return self.radius


if __name__ == '__main__':
    # Инициализация
    pygame.init()
    size = width, height = 600, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Падающие шары")
    clock = pygame.time.Clock()
    # Список шаров
    balls = []
    running = True
    # Создание начального шара
    ball = Ball(pygame.mouse.get_pos()[0], random.randint(30, 50))
    balls.append(ball)
    while running:

        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if ball.motion:
                    ball.x = event.pos[0]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ball.fall = True
                ball.motion = False

        # Отрисовка экрана
        screen.fill('white')
        for ball in balls:
            ball.draw()

        # Обновление состояния шаров
        for ball in balls:
            if ball.fall:
                ball.update()

        # Проверка коллизий
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                dx = balls[i].x - balls[j].x
                dy = balls[i].y - balls[j].y
                distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                if distance < balls[i].radius + balls[j].radius:
                    balls[i].speed *= 0
                    balls[j].speed *= 0

        pygame.display.flip()
        # тут проверка выхода за границы и создание нового шара
        try:
            if (ball.y - ball.radius) // ball.speed == ball.deathline // ball.speed:
                ball = Ball(pygame.mouse.get_pos()[0], random.randint(30, 50))
                balls.append(ball)
        except Exception as e:
            print('Game over')
            terminate()

        clock.tick(60)

    # Завершение Pygame
    terminate()
