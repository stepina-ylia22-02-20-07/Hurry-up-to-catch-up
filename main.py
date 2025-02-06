import random
import pygame
import pytmx
import os
import sys
from message import *
from labirint import *

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
FPS = 15
MAP = "data"
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 32
KOL_WIN = 0
KOL_LOSE = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Hero:

    def __init__(self, position):
        self.image = pygame.image.load(f"data/play_2.png")
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, image):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Enemy:

    def __init__(self, position):
        self.image = pygame.image.load(f"data/fox_1.png")
        self.x, self.y = position
        self.delay = 100

        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Game:

    def __init__(self, labirint, hero, enemy):
        self.labirint = labirint
        self.hero = hero
        self.enemy = enemy

    def render(self, screen):
        self.labirint.render(screen)
        self.hero.render(screen)
        self.enemy.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1

        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1

        if self.labirint.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_enemy(self):
        next_position = self.labirint.find_path_step(self.enemy.get_position(),
                                                     self.hero.get_position())

        self.enemy.set_position(next_position)

    def check_lose(self):
        return self.hero.get_position() == self.enemy.get_position()

    def check_win(self):
        return self.labirint.get_tile_id(self.hero.get_position()) == self.labirint.finish


def start_screen():
    channel_music = pygame.mixer.Channel(0)
    music = pygame.mixer.Sound('data/81cebf7e45fdef7.mp3')

    channel_music.play(music, -1)

    intro_text = ["Hurry up",
                  "     to",
                  "catch up"]

    fon = pygame.transform.scale(load_image('fon.webp'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/Gantauluauope.ttf', 100)
    text_coord = 50

    for line in intro_text:
        string_rendered = font.render(line, 2, pygame.Color('paleturquoise'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    show_message_start(screen, "Начать игру")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate_2()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    width = 672
    height = 608
    screen = pygame.display.set_mode((width, height))

    screen_rect = (0, 0, width, height)

    class Particle(pygame.sprite.Sprite):
        fire = [load_image("star.png")]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))

        def __init__(self, pos, dx, dy):
            super().__init__(all_sprites)
            self.image = random.choice(self.fire)
            self.rect = self.image.get_rect()

            self.velocity = [dx, dy]
            self.rect.x, self.rect.y = pos

            self.gravity = 1

        def update(self):
            self.velocity[1] += self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            if not self.rect.colliderect(screen_rect):
                self.kill()

    def create_particles(position):
        particle_count = 20
        numbers = range(-5, 6)

        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate_2()
            else:
                create_particles(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()

        all_sprites.update()
        screen.fill(pygame.Color("aquamarine"))

        show_message(screen, "YOU WIN!")

        show_message_result_win(screen, f"Number of wins: {str(KOL_WIN)}")
        show_message_result_lose(screen, f"Number of defeats: {str(KOL_LOSE)}")

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(40)


def lose_screen():
    FPS = 5
    WIDTH = 672
    HEIDHT = 608
    screen = pygame.display.set_mode((WIDTH, HEIDHT))

    all_sprites = pygame.sprite.Group()

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(30, 300, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
            self.frames = self.frames[8:-4]

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    fox = AnimatedSprite(load_image("foxs.jpg"), 4, 4, 100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main()

        screen.fill(pygame.Color("black"))
        all_sprites.draw(screen)
        all_sprites.update()

        show_message(screen, "YOU LOSE!")

        show_message_result_win(screen, f"Number of wins: {str(KOL_WIN)}")
        show_message_result_lose(screen, f"Number of loses: {str(KOL_LOSE)}")

        pygame.display.flip()
        clock = pygame.time.Clock()
        clock.tick(FPS)

    pygame.quit()


def terminate_2():
    pygame.quit()
    sys.exit()


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    global KOL_WIN
    global KOL_LOSE

    pygame.display.set_caption("Hurry up to catch up")
    img = pygame.image.load("data/fon.webp")

    pygame.display.set_icon(img)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    start_screen()
    levels = ["Play.tmx", "Play_2.tmx"]

    labirint = Labirint(random.choice(levels), [2110, 2], 2110)

    hero = Hero((1, 9))
    enemy = Enemy((19, 11))

    game = Game(labirint, hero, enemy)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()

        if not game_over:
            game.update_hero()

        screen.fill((0, 0, 0))
        game.render(screen)

        if game.check_win():
            KOL_WIN += 1
            win_screen()
            try:
                file = open('data/result.txt', 'w')
                file.write('WIN!\n')
                file.close()

                game_over = True

            except:
                game_over = True

        if game.check_lose():
            KOL_LOSE += 1
            lose_screen()
            try:
                file = open('data/result.txt', 'w')
                file.write('LOSE!\n')
                file.close()

                game_over = True

            except:
                game_over = True

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption("Hurry up to catch up")
    img = pygame.image.load("data/fon.webp")

    pygame.display.set_icon(img)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    start_screen()
    levels = ["Play.tmx", "Play_2.tmx"]

    labirint = Labirint(random.choice(levels), [2110, 2], 2110)

    hero = Hero((1, 9))
    enemy = Enemy((19, 11))

    game = Game(labirint, hero, enemy)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()

        if not game_over:
            game.update_hero()

        screen.fill((0, 0, 0))
        game.render(screen)

        if game.check_win():
            KOL_WIN += 1
            win_screen()

            game_over = True

        if game.check_lose():
            KOL_LOSE += 1
            lose_screen()

            game_over = True

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
