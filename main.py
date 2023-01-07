import sys
import csv

import pygame

from player import Player
from globals import WIDTH, HEIGHT
from globals import WHITE, BUTTON_COLOR, BUTTON_COLOR_CHECKED
from globals import save_progress
from globals import Button
import test_room
import settings
import shop


# DARK_BLUE = "#5F2580"
# BLUE = "#48036F"
# START_PAGE = 1


# cur_page = START_PAGE


def load_player():
    with open('data.csv', encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for el in reader:
            res = el
    res['amount_of_money'] = int(res['amount_of_money'])
    shop_weapon = res['shop_weapon']
    arr = []
    for el in shop_weapon:
        arr.append(int(el))
    res['shop_weapon'] = arr.copy()

    shop_clothes = res['shop_clothes']
    arr = []
    for el in shop_clothes:
        arr.append(int(el))
    res['shop_clothes'] = arr.copy()

    if res['weapon'] == 'None':
        res['weapon'] = None

    if res['current_clothes'] == 'BASE_DRESS':
        res['current_clothes'] = 1

    return res


player_properties = load_player()
player = Player(player_properties['amount_of_money'],
                player_properties['weapon'],
                player_properties['current_clothes'],
                player_properties['shop_weapon'],
                player_properties['shop_clothes'])

static_elements = pygame.sprite.Group()
buttons = pygame.sprite.Group()


def prepare_buttons():
    button_width = WIDTH // 3
    button_height = HEIGHT // 12
    font_size = HEIGHT // 20
    step = HEIGHT // 30

    button_start_game = Button(WIDTH // 3, HEIGHT // 2, button_width, button_height, BUTTON_COLOR, "НАЧАТЬ ИГРУ", font_size, WHITE)
    button_start_game.set_func(test_room.main)
    buttons.add(button_start_game)

    button_shop = Button(WIDTH // 3, HEIGHT // 2 + 1 * step + 1 * button_height,
                        button_width, button_height, BUTTON_COLOR, "МАГАЗИН", font_size, WHITE)
    button_shop.set_func(shop.main)
    buttons.add(button_shop)

    button_settings = Button(WIDTH // 3, HEIGHT // 2 + 2 * step + 2 * button_height,
                            button_width, button_height, BUTTON_COLOR, "НАСТРОЙКИ", font_size, WHITE)
    button_settings.set_func(settings.main)
    buttons.add(button_settings)

    button_rules = Button(WIDTH // 3, HEIGHT // 2 + 3 * step + 3 * button_height,
                            button_width, button_height, BUTTON_COLOR, "ПРАВИЛА ИГРЫ", font_size, WHITE)
    buttons.add(button_rules)


def prepare_static_elements():
    background = pygame.sprite.Sprite()
    background.image = pygame.image.load("res/backgrounds/background_start_page.jpg")
    background.rect = background.image.get_rect()
    static_elements.add(background)
    

    money = pygame.sprite.Sprite()
    money.image = pygame.image.load("res/icons/money.svg")
    money.rect = money.image.get_rect()
    money.rect.x = WIDTH - 150
    money.rect.y = 30
    static_elements.add(money)


def draw_amount_of_money(screen):
    amount_of_money = pygame.sprite.Sprite()
    amount_of_money.image = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
    amount_of_money.rect = (WIDTH - 210, 30, 50, 50)
    font = pygame.font.Font(None, 30)
    text = font.render(str(player.get_amount_of_money()), True, WHITE)
    text_rect = text.get_rect(center=amount_of_money.image.get_rect().center)
    text_rect.x = WIDTH - 210
    text_rect.y = 45
    # amount_of_money.image.blit(text, text_rect)
    screen.blit(text, text_rect)


# class Button:
#     def __init__(self, pos_x, pos_y, width, heigth, color, text, text_size, text_color):
#         self.pos_x = pos_x
#         self.pos_y = pos_y
#         self.width = width
#         self.heigth = heigth
#         self.color = color
#         self.text = text
#         self.text_size = text_size
#         self.text_color = text_color

#     def set_color(self, state):
#         if state:
#             self.color = DARK_BLUE
#         else:
#             self.color = BLUE

#     def set_func(self, func):
#         self.func = func

#     def check_mouse_position(self, mouse_pos):
#         return self.pos_x <= mouse_pos[0] < self.pos_x + self.width and \
#                 self.pos_y <= mouse_pos[1] < self.pos_y + self.heigth
    
#     def action(self):
#         # self.func()
#         try:
#             self.func()
#         except:
#             print("Пока у кнопки нет функции нет")

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.width, self.heigth))
#         font = pygame.font.Font(None, self.text_size)
#         text = font.render(self.text, True, self.text_color)
#         text_rect = text.get_rect(center=(self.pos_x + self.width // 2, self.pos_y + self.heigth // 2))
#         screen.blit(text, text_rect)
#         # screen.blit(text, (self.pos_x + self.width // 2, self.pos_y + self.heigth // 2))


# class StartPage:
#     def __init__(self):
#         self.all_sprites = pygame.sprite.Group()
#         self.prepare_sprites()
        
#         self.buttons = []
#         self.prepare_buttons()

#     def prepare_sprites(self):
#         self.background = pygame.sprite.Sprite()
#         self.background.image = pygame.image.load("res/backgrounds/background_start_page.jpg").convert()
#         self.background.image = pygame.transform.scale(self.background.image, (WIDTH, HEIGHT))
#         self.background.rect = self.background.image.get_rect()
#         self.all_sprites.add(self.background)
#         self.money = pygame.sprite.Sprite()
#         self.money.image = pygame.image.load("res/icons/money.svg")
#         # self.money.image = pygame.transform.scale(self.money.image, (50, 50))
#         self.money.rect = self.money.image.get_rect()
#         self.money.rect.x = 5 * WIDTH // 6
#         self.money.rect.y = 30
#         self.all_sprites.add(self.money)

#         font = pygame.font.Font(None, 30)
#         text = font.render(str(player.get_amount_of_money()), True, WHITE)
#         text_rect = text.get_rect(center=(5 * WIDTH // 6 - len(str(player.get_amount_of_money())) * 10, 55))
#         self.background.image.blit(text, text_rect)

#     def prepare_buttons(self):
#         button_width = WIDTH // 3
#         button_height = HEIGHT // 12
#         font_size = HEIGHT // 20
#         step = HEIGHT // 30

#         # начало игры
#         self.button_begin_game = Button(WIDTH // 3, HEIGHT // 2, button_width, button_height, BLUE, "НАЧАТЬ ИГРУ", font_size, WHITE)
#         self.button_begin_game.set_func(test_room.main)
#         self.buttons.append(self.button_begin_game)

#         # магазины
#         self.button_shops = Button(WIDTH // 3, HEIGHT // 2 + 1 * step + 1 * button_height, button_width, button_height, BLUE, "МАГАЗИНЫ", font_size, WHITE)
#         self.button_shops.set_func(shop.main)
#         self.buttons.append(self.button_shops)

#         # настройки
#         self.button_settings = Button(WIDTH // 3, HEIGHT // 2 + 2 * step + 2 * button_height, button_width, button_height, BLUE, "НАСТРОЙКИ", font_size, WHITE)
#         self.button_settings.set_func(settings.main)
#         self.buttons.append(self.button_settings)

#         # правила игры
#         self.button_rules = Button(WIDTH // 3, HEIGHT // 2 + 3 * step + 3 * button_height, button_width, button_height, BLUE, "ПРАВИЛА ИГРЫ", font_size, WHITE)
#         self.buttons.append(self.button_rules)

#     def check_transition(self, mouse_pos):
#         for button in self.buttons:
#             if button.check_mouse_position(mouse_pos) is True:
#                 button.action()
    
#     def draw_start_page(self, screen, mouse_pos):
#         self.all_sprites.draw(screen)

#         self.button_begin_game.set_color(self.button_begin_game.check_mouse_position(mouse_pos))
#         self.button_shops.set_color(self.button_shops.check_mouse_position(mouse_pos))
#         self.button_settings.set_color(self.button_settings.check_mouse_position(mouse_pos))
#         self.button_rules.set_color(self.button_rules.check_mouse_position(mouse_pos))

#         for button in self.buttons:
#             button.draw(screen)


def main():
    pygame.init()
    pygame.display.set_caption("Малелькая колдунья")

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    # page = StartPage()
    prepare_buttons()
    prepare_static_elements()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(player.amount_of_money)
                save_progress(player)
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.check_mouse_position((pos[0], pos[1])):
                        button.set_color(True)
                        break
                    else:
                        button.set_color(False)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.check_mouse_position((pos[0], pos[1])):
                        button.action()
                        if button.get_text() == "МАГАЗИН":
                            player_properties = load_player()
                            player.amount_of_money = player_properties["amount_of_money"]
                            print(player.get_amount_of_money())
                        break
                # page.check_transition(event.pos)
        mouse = pygame.mouse.get_pos()
        # if cur_page == START_PAGE:
        #     page.draw_start_page(screen, mouse)
        static_elements.update()
        static_elements.draw(screen)
        buttons.update()
        buttons.draw(screen)
        draw_amount_of_money(screen)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())