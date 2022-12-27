import sys

import pygame

import test_room
import settings
import shop


WIDTH = 1000
HEIGHT = 800
DARK_BLUE = (0, 0, 150)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
START_PAGE = 1

cur_page = START_PAGE


class Button:
    def __init__(self, pos_x, pos_y, width, heigth, color, text, text_size, text_color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.heigth = heigth
        self.color = color
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

    def set_color(self, state):
        if state:
            self.color = DARK_BLUE
        else:
            self.color = BLUE

    def set_func(self, func):
        self.func = func

    def check_mouse_position(self, mouse_pos):
        return self.pos_x <= mouse_pos[0] < self.pos_x + self.width and \
                self.pos_y <= mouse_pos[1] < self.pos_y + self.heigth
    
    def action(self):
        try:
            self.func()
        except:
            print("Пока у кнопки нет функции нет")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.width, self.heigth))
        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.pos_x + self.width // 2, self.pos_y + self.heigth // 2))
        screen.blit(text, text_rect)
        # screen.blit(text, (self.pos_x + self.width // 2, self.pos_y + self.heigth // 2))

class StartPage:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.prepare_sprites()
        
        self.buttons = []
        self.prepare_buttons()

    def prepare_sprites(self):
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.image.load("res/backgrounds/volcanoes.jpg").convert()
        self.background.image = pygame.transform.scale(self.background.image, (WIDTH, HEIGHT))
        self.background.rect = self.background.image.get_rect()
        self.all_sprites.add(self.background)

    def prepare_buttons(self):
        button_width = WIDTH // 3
        button_height = HEIGHT // 12
        font_size = HEIGHT // 20
        step = HEIGHT // 30

        # начало игры
        self.button_begin_game = Button(WIDTH // 3, HEIGHT // 2, button_width, button_height, BLUE, "НАЧАТЬ ИГРУ", font_size, WHITE)
        self.button_begin_game.set_func(test_room.main)
        self.buttons.append(self.button_begin_game)

        # магазины
        self.button_shops = Button(WIDTH // 3, HEIGHT // 2 + 1 * step + 1 * button_height, button_width, button_height, BLUE, "МАГАЗИНЫ", font_size, WHITE)
        self.button_shops.set_func(shop.main)
        self.buttons.append(self.button_shops)

        # настройки
        self.button_settings = Button(WIDTH // 3, HEIGHT // 2 + 2 * step + 2 * button_height, button_width, button_height, BLUE, "НАСТРОЙКИ", font_size, WHITE)
        self.button_settings.set_func(settings.main)
        self.buttons.append(self.button_settings)

        # правила игры
        self.button_rules = Button(WIDTH // 3, HEIGHT // 2 + 3 * step + 3 * button_height, button_width, button_height, BLUE, "ПРАВИЛА ИГРЫ", font_size, WHITE)
        self.buttons.append(self.button_rules)

    def check_transition(self, mouse_pos):
        for button in self.buttons:
            if button.check_mouse_position(mouse_pos) is True:
                button.action()
    
    def draw_start_page(self, screen, mouse_pos):
        self.all_sprites.draw(screen)

        self.button_begin_game.set_color(self.button_begin_game.check_mouse_position(mouse_pos))
        self.button_shops.set_color(self.button_shops.check_mouse_position(mouse_pos))
        self.button_settings.set_color(self.button_settings.check_mouse_position(mouse_pos))
        self.button_rules.set_color(self.button_rules.check_mouse_position(mouse_pos))

        for button in self.buttons:
            button.draw(screen)


def main():
    pygame.init()
    pygame.display.set_caption("Малелькая колдунья")

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    page = StartPage()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                page.check_transition(event.pos)
        mouse = pygame.mouse.get_pos()
        if cur_page == START_PAGE:
            page.draw_start_page(screen, mouse)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())