## при повторном вхоже - не работает
import sys
import csv

import pygame
import pygame_gui

from main import player
from globals import WIDTH, HEIGHT, CARD_WIDTH, CARD_HEIGHT
from globals import WHITE, BUTTON_COLOR
from globals import save_progress
from globals import Button


pygame.init()

cards_sprites = pygame.sprite.Group()
buttons_sprites = pygame.sprite.Group()
buttons = []

BUTTON_HEIGHT = 50
STEP_X = (WIDTH - 2 * CARD_WIDTH) // 3
STEP_Y = HEIGHT // 20

BACKGROUND_COLOR = (180, 0, 180)
CARD_COLOR = (0, 255, 0)


magic = [[("Магия земли", 100), ("Магия воды", 300)],
        [("Магия воздуха", 800), ("Магия огня", 1500)]]

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
shop_clock = pygame.time.Clock()


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    # print(t)
    _, _, w, h = camera
    # l, t = -l + WIDTH // 2, -t + HEIGHT // 2
    t = -t

    l = min(0, l)
    l = max(-(camera.width - WIDTH), l)
    # t = max(HEIGHT + 100, t)
    # print(t)
    t = min(0, t)
    t = max(-500, t)
    # print(t)
    return pygame.Rect(l, t, w, h)


def draw_amount_of_money(screen):
    font = pygame.font.Font(None, 30)
    text = font.render(str(player.get_amount_of_money()), True, WHITE)
    text_rect = text.get_rect(center=(5 * WIDTH // 6 - (len(str(player.get_amount_of_money())) + 2) * 10, 55))
    screen.blit(text, text_rect)


class Camera:
    def __init__(self, camera_func, width, height):
        self.func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        # print(self.state)
        self.state = self.func(self.state, target.rect)
        # print(self.state)


class Point:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    
    def move(self, delta_y):
        self.rect.y += delta_y
        # print(self.rect.y)


# class Button(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y, width, height, color, text, text_size, text_color):
#         super().__init__()
#         self.pos_x = pos_x
#         self.pos_y = pos_y
#         self.width = width
#         self.height = height
#         self.color = color
#         self.text = text
#         self.text_size = text_size
#         self.text_color = text_color

#         self.image = pygame.Surface((width, height))
#         self.image.fill(color)
#         self.rect = pygame.Rect(pos_x, pos_y, width, height)

#         font = pygame.font.Font(None, 30)
#         self.normal_text = text
#         self.txt = font.render(text, True, "white")
#         self.text_rect = self.txt.get_rect(center=(CARD_WIDTH // 2, BUTTON_HEIGHT // 2))
#         self.image.blit(self.txt, self.text_rect)

#     def update(self):
#         # self.image = pygame.Surface((self.width, self.height))
#         # self.image = pygame.Surface((self.width, self.height))
#         self.image.fill(self.color)
#         # self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
#         self.image.blit(self.txt, self.text_rect)
#         # self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

#     def set_color(self, state):
#         if state:
#             self.color = BUTTON_COLOR_CHECKED
#         else:
#             self.color = BUTTON_COLOR
        
#     def set_text(self, text):
#         self.normal_text = text
#         font = pygame.font.Font(None, 30)
#         self.txt = font.render(text, True, "white")
#         self.text_rect = self.txt.get_rect(center=(CARD_WIDTH // 2, BUTTON_HEIGHT // 2))

#     def get_text(self):
#         return self.normal_text

#     def set_func(self, func):
#         self.func = func

#     def check_mouse_position(self, mouse_pos):
#         return self.pos_x <= mouse_pos[0] < self.pos_x + self.width and \
#                 self.pos_y <= mouse_pos[1] < self.pos_y + self.height
    
#     def action(self):
#         try:
#             self.func()
#         except:
#             print("Пока у кнопки нет функции нет")


class Card(pygame.sprite.Sprite):
    def __init__(self, number, x, y, name, price, button_txt):
        super().__init__()
        self.number = number
        self.x = x
        self.y = y
        self.name = name
        self.price = price
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(pygame.Color(CARD_COLOR))
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        self.button = Button(x, y + CARD_HEIGHT - BUTTON_HEIGHT, CARD_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, button_txt, 30, "white")
        buttons.append((self, self.button))
        buttons_sprites.add(self.button)
        self.image.blit(self.button.image, (0, CARD_HEIGHT - BUTTON_HEIGHT))

        font = pygame.font.Font(None, 30)
        self.text = font.render(name + ' - ' + str(price), True, "white")
        self.text_rect = self.text.get_rect(center=(CARD_WIDTH // 2, HEIGHT // 20))
        self.image.blit(self.text, self.text_rect)

    def get_price(self):
        return self.price
    
    def update(self):
        # self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        # self.image.fill(pygame.Color(CARD_COLOR))
        # self.rect = pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT)
        # self.image.blit(self.text, self.text_rect)
        # self.image.fill(pygame.Color(CARD_COLOR))
        # self.image.blit(self.button.image, (0, CARD_HEIGHT - BUTTON_HEIGHT))
        # self.image.blit(self.text, self.text_rect)
        self.image.blit(self.button.image, (0, CARD_HEIGHT - BUTTON_HEIGHT))


def main():
    print("Here")
    global cards_sprites, buttons_sprites, buttons
    print(len(cards_sprites), buttons)

    pygame.display.set_caption("Магазин")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # b = Button(50, 30, 100, 50, "black", "aaa", 30, "green")
    # # buttons.append(b)
    # buttons_sprites.add(b)

    total_width = WIDTH
    total_height = STEP_X + 2 * CARD_HEIGHT + 2 * STEP_Y
    camera = Camera(camera_configure, total_width, total_height)
    p = Point()

    arrow_back = pygame.sprite.Sprite()
    arrow_back.image = pygame.image.load("res/icons/arrow_back.SVG")
    # arrow_back.image = pygame.transform.scale(arrow_back.image, (WIDTH // 20, WIDTH // 20))
    arrow_back.rect = arrow_back.image.get_rect()
    arrow_back.rect.x = (STEP_X - arrow_back.rect.width) // 2
    arrow_back.rect.y = (STEP_X - arrow_back.rect.width) // 2

    money = pygame.sprite.Sprite()
    money.image = pygame.image.load("res/icons/money.svg")
    money.rect = money.image.get_rect()
    money.rect.x = WIDTH - STEP_X - 50
    money.rect.y = 30

    static_elements = pygame.sprite.Group()
    static_elements.add(arrow_back)
    static_elements.add(money)

    pos_x = STEP_X
    pos_y = STEP_X
    number = 0
    for i in range(2):
        pos_x = STEP_X
        for j in range(2):
            button_text = player.get_weapon_state(number)
            card = Card(number, pos_x, pos_y, magic[i][j][0], magic[i][j][1], button_text)
            cards_sprites.add(card)
            pos_x += CARD_WIDTH + STEP_X
            number += 1
        pos_y += CARD_HEIGHT + STEP_Y

    running = True
    while running:
        time_delta = shop_clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(player)
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for card, button in buttons:
                    if button.check_mouse_position((pos[0], pos[1] + p.rect.y)):
                        # print(button)
                        # b.set_color(True)
                        # button.set_color(True)
                        # print(card.button.get_text())
                        card.button.set_color(True)
                        break
                    else:
                        # button.set_color(False)
                        # b.set_color(False)
                        card.button.set_color(False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    for card, button in buttons:
                        if button.check_mouse_position((pos[0], pos[1] + p.rect.y)):
                            if card.button.get_text() == "Надеть":
                                for card2, button2 in buttons:
                                    if card2.button.get_text() != "Купить":
                                        card2.button.set_text("Надеть")
                                        player.set_weapon_state(card2.number, 1)
                                card.button.set_text("Надето")
                                player.set_weapon_state(card.number, 2)
                                break
                            if card.button.get_text() == "Купить":
                                if player.get_amount_of_money() >= card.get_price():
                                    message_text = f"Предмет '{card.name}' приобретён успешно!"
                                    player.change_amount_of_money(-card.get_price())
                                    for card2, button2 in buttons:
                                        if card2.button.get_text() != "Купить":
                                            card2.button.set_text("Надеть")
                                            player.set_weapon_state(card2.number, 1)
                                    card.button.set_text("Надето")
                                    player.set_weapon_state(card.number, 2)
                                else:
                                    message_text = "Недостаточно средств. Проходите уровни, получайте награды!"
                                message = pygame_gui.windows.UIMessageWindow(
                                    rect=pygame.Rect(250, 200, 300, 200),
                                    manager=manager,
                                    window_title="Сообщение",
                                    html_message=message_text
                                )
                                # break
                    if arrow_back.rect.x <= event.pos[0] < arrow_back.rect.x + arrow_back.rect.width and \
                            arrow_back.rect.y <= event.pos[1] < arrow_back.rect.y + arrow_back.rect.height:
                        print("!")
                        
                        cards_sprites = pygame.sprite.Group()
                        buttons_sprites = pygame.sprite.Group()
                        buttons = []
                        save_progress(player)
                        print(player.amount_of_money)
                        return
                if event.button == 4:  # крутим вперёд
                    p.move(-10)
                if event.button == 5:  # крутим назад
                    p.move(10)
            manager.process_events(event)
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        buttons_sprites.update()
        cards_sprites.update()
        # cards_sprites.draw(screen)
        camera.update(p)
        for card in cards_sprites:
            camera.apply(card.button)
            # print(card.button.rect)
            screen.blit(card.image, camera.apply(card))
            # print(card.rect)
        manager.update(time_delta)
        manager.draw_ui(screen)
        # buttons_sprites.draw(screen)
        # buttons_sprites.update()
        # buttons_sprites.draw(screen)
        draw_amount_of_money(screen)
        static_elements.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())