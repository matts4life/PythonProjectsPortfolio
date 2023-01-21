import time
import random

import pygame

import sys
import os

WHITE = (100, 100, 100)
RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        asset_url = resource_path('res/paddle.png')
        self.image = pygame.image.load(asset_url).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 395
        self.rect.y = 450

        self.going_left = False
        self.going_right = False

        self.move = 2.75

    def update(self):
        pos = pygame.mouse.get_pos()

        time.sleep(0.005)

        if self.rect.x - 5 > pos[0]:
            self.going_left = True
            self.going_right = False
            self.rect.x += -self.move
            asset_url1 = resource_path('res/paddlerotleft.png')
            self.image = pygame.image.load(asset_url1).convert_alpha()
        if self.rect.x < pos[0]:
            self.going_left = False
            self.going_right = True
            self.rect.x += self.move + 0.25
            asset_url2 = resource_path('res/paddlerotright.png')
            self.image = pygame.image.load(asset_url2).convert_alpha()
        elif self.rect.x == pos[0]:
            self.going_left = False
            self.going_right = False
            asset_url = resource_path('res/paddle.png')
            self.image = pygame.image.load(asset_url).convert_alpha()

        if self.rect.x >= 745:
            self.rect.x = 745


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        asset_url = resource_path('res/ball.png')
        self.image = pygame.image.load(asset_url).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(375, 475) - 32
        self.rect.y = 100

        self.freefall = True

        self.y_vel = 0
        self.x_vel = 0

    def gravity(self):
        if self.freefall:
            self.y_vel += 0.065
        else:
            self.y_vel = 0
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel

    def update(self):
        self.gravity()


class Game:
    def __init__(self):
        self.all_sprites_list = pygame.sprite.Group()
        self.player = Player()
        self.ball = Ball()
        self.all_sprites_list.add(self.player, self.ball)

        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 122)
        self.font_small = pygame.font.Font('freesansbold.ttf', 76)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.score == 0:
                        self.ball.rect.y = 100
                        self.ball.rect.x = 425 - 16
                        self.ball.x_vel = 0
                        self.ball.y_vel = 0

        return False

    def run(self, screen):
        self.all_sprites_list.update()
        self.player.update()
        self.ball.update()

        if self.ball.rect.colliderect(self.player.rect):
            music_url = resource_path('res/Hit_hurt 55 (mp3cut.net).wav')
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_url))
            self.score += 1
            if self.player.going_right:
                self.ball.y_vel = random.uniform(-6, -7.5)
                self.ball.x_vel = 0
                self.ball.x_vel -= random.uniform(-1, -4.5)
                self.ball.freefall = False
                self.ball.freefall = True
            if self.player.going_left:
                self.ball.y_vel = random.uniform(-6, -7.5)
                self.ball.x_vel = 0
                self.ball.x_vel -= random.uniform(.5, 4)
                self.ball.freefall = False
                self.ball.freefall = True
            elif not self.player.going_right and not self.player.going_left:
                self.ball.y_vel = random.uniform(-6, -7.5)
                self.ball.x_vel = 0
                self.ball.freefall = False
                self.ball.freefall = True

        window_rect = screen.get_rect()
        window_rect = window_rect.inflate(-0.1, -0.1)
        window_rect.x = window_rect.x + 10
        if not window_rect.colliderect(self.ball.rect):
            self.ball.x_vel = -self.ball.x_vel

        if self.ball.rect.y >= 580:
            self.score = 0

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        self.all_sprites_list.draw(screen)

        score_text = self.font.render(str(self.score), True, (166, 166, 166))

        if self.score == 0:
            score_text = self.font_small.render("press 'space' to play", True, (166, 166, 166))

        score_text_rect = score_text.get_rect()

        score_text_rect.center = (850 // 2, 600 // 2)
        screen.blit(score_text, score_text_rect)

        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.init()

    size = [850, 600]

    screen = pygame.display.set_mode((size[0], size[1]))

    asset_url = resource_path('res/paddle.png')
    pygame_icon = pygame.image.load(asset_url)
    pygame.display.set_icon(pygame_icon)
    pygame.display.set_caption("Pro Paddle")

    clock = pygame.time.Clock()

    game = Game()

    music_url = resource_path('res/music (mp3cut.net).wav')
    pygame.mixer.music.load(music_url)
    pygame.mixer.music.play(-1)

    done = False

    while not done:
        game.process_events()
        game.run(screen)
        game.display_frame(screen)

        clock.tick()
    pygame.quit()


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    main()
