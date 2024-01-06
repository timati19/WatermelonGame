import pygame
import random

all_sprites = pygame.sprite.Group()

class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__(all_sprites)
        self.motion = False
        self.radius = random.randint(30, 70)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(x, 20, 2 * self.radius, 2 * self.radius)

    def update(self, mouse_ball):
        if self.motion:
            self.rect.y += 3
        if pygame.sprite.spritecollide(self, all_sprites, False):
            lst = pygame.sprite.spritecollide(self, all_sprites, False)
            if len(lst) > 1:
                for i in lst:
                    if pygame.sprite.collide_circle(self, i) and self.rect.y > 300:
                        self.motion = False
        # if pygame.sprite.spritecollideany(self, horizontal_borders):
        #     self.motion = False
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if self.rect.x < 300:
                self.rect.x = 5
            else:
                self.rect.x = 595 - self.radius * 2

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def main():
    pygame.init()
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255 ,255))
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10)
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    mouse_ball = Ball(pygame.mouse.get_pos()[0])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_ball.rect.x = event.pos[0] - mouse_ball.radius
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_ball.motion = True
                mouse_ball = Ball(pygame.mouse.get_pos()[0])
            if event.type == MYEVENTTYPE:
                screen.fill((255, 255 ,255))
                all_sprites.update(mouse_ball)
                all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
