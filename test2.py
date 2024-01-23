import math
import random

import pygame
import pymunk
import pymunk.pygame_util


# Загрузка изображения
def load_image(radius, image='imgs/smile.jpg'):
    ball_image = pygame.image.load(image)
    ball_image = pygame.transform.scale(ball_image, (radius * 2, radius * 2))
    return ball_image


# Переменная для отслеживания количества шаров
ball_count = 0
sp_coord = (0, 0)


# Функция для создания шарика
def create_ball(space, pos, radius):
    global ball_count, sp_coord
    mass = 0.1
    sp_coord = (pos[0], pos[1])
    inertia = pymunk.moment_for_circle(mass, 10, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = pos
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.4
    shape.friction = 0.5
    space.add(body, shape)
    ball_count += 1
    return shape


def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)


# Функция для удаления шаров и создания нового
def remove_ball(arbiter, space, data):
    global ball_count
    if isinstance(arbiter.shapes[0], pymunk.Circle) and isinstance(arbiter.shapes[1], pymunk.Circle):
        shape = arbiter.shapes[0]
        shape2 = arbiter.shapes[1]
        if shape.radius == shape2.radius and shape.radius != max(radius):
            ball_count -= 2
            create_ball(space, (shape2.body.position.x, shape2.body.position.y), shape.radius + 10)
            ball_count += 1
            space.remove(shape, shape.body)
            space.remove(shape2, shape2.body)
    return True
    pass


def main():
    global radius, ball_count
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 500)
    radius = [45, 55, 65]
    dic = {45: 'imgs/smile.png', 55: 'imgs/skull.png', 65: 'imgs/ball1.png'}

    # Создание краев окна
    static_lines = [
        pymunk.Segment(space.static_body, (0, height - 1), (width, height - 1), 5.0),
        pymunk.Segment(space.static_body, (1, 1), (1, height), 0.0),
        pymunk.Segment(space.static_body, (width - 1, 1), (width - 1, height), 0.0), ]

    # Добовление краев окна
    for l in static_lines:
        l.friction = 0.5
    space.add(*static_lines)
    random_rad = min(radius)
    running = True
    while running:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Создание шарика при нажатии кнопки мыши
                create_ball(space, (event.pos[0], 0 + random_rad), random_rad)
                random_rad = random.choice(radius[:2])

        # Отрисовка шара сверху
        if ball_count == 0 or ball.body.position.y > 200:
            x = pygame.mouse.get_pos()[0] - random_rad
            pygame.draw.line(screen, 'black', (pygame.mouse.get_pos()[0], 10), (pygame.mouse.get_pos()[0], height), 2)
            screen.blit(load_image(random_rad, dic[random_rad]), (x, 0))

        # Обновление физики
        space.step(1 / 50.0)

        # Отрисовка краев окна
        pygame.draw.line(screen, 'black', (0, height - 1), (width, height - 1), 5)
        pygame.draw.line(screen, 'black', (1, 1), (1, height), 5)
        pygame.draw.line(screen, 'black', (width - 1, 1), (width - 1, height), 5)

        # Отрисовка изображения на шарике

        for ball in space.shapes:
            if isinstance(ball, pymunk.shapes.Circle):
                w = h = ball.radius * 2
                image = load_image(ball.radius, dic[ball.radius])
                blitRotate(screen, image, ball.body.position, (w / 2, h / 2), -ball.body.angle * 180 / math.pi)

        # Обработка столкновения шаров
        space.collision_handler = space.add_collision_handler(0, 0)
        space.collision_handler.begin = remove_ball

        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()
