import csv
import pygame


# размеры окна
WIDTH = 1000
HEIGHT = 800
# размеры карточек
CARD_WIDTH = 300
CARD_HEIGHT = 500
# высота кнопки
BUTTON_HEIGHT = 50

# цвета
WHITE = (255, 255, 255)
BUTTON_COLOR = "#48036F"
BUTTON_COLOR_CHECKED = "#5F2580"


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, color, text, text_size, text_color):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

        font = pygame.font.Font(None, text_size)
        self.normal_text = text
        self.txt = font.render(text, True, text_color)
        self.text_rect = self.txt.get_rect(center=(width // 2, height // 2))
        self.image.blit(self.txt, self.text_rect)

    def update(self):
        # self.image = pygame.Surface((self.width, self.height))
        # self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        # self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.image.blit(self.txt, self.text_rect)
        # self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def set_color(self, state):
        if state:
            self.color = BUTTON_COLOR_CHECKED
        else:
            self.color = BUTTON_COLOR
        
    def set_text(self, text):
        self.normal_text = text
        font = pygame.font.Font(None, self.text_size)
        self.txt = font.render(text, True, self.text_color)
        self.text_rect = self.txt.get_rect(center=(self.width // 2, self.height // 2))

    def get_text(self):
        return self.normal_text

    def set_func(self, func):
        self.func = func

    def check_mouse_position(self, mouse_pos):
        return self.pos_x <= mouse_pos[0] < self.pos_x + self.width and \
                self.pos_y <= mouse_pos[1] < self.pos_y + self.height
    
    def action(self):
        try:
            self.func()
        except:
            print("Пока у кнопки нет функции нет")


def save_progress(player):
    with open('data.csv', 'w', newline='', encoding="utf8") as f:
        d = {
            "amount_of_money": player.amount_of_money,
            "weapon": '',
            "current_clothes": "BASE_DRESS",
            "shop_weapon": player.shop_weapon,
            "shop_clothes": player.shop_clothes
        }
        if player.weapon is None:
            d["weapon"] = "None"
        res_shop_weapon = ""
        for el in player.shop_weapon:
            res_shop_weapon += str(el)
        d["shop_weapon"] = res_shop_weapon
        res_shop_clothes = ""
        for el in player.shop_clothes:
            res_shop_clothes += str(el)
        d["shop_clothes"] = res_shop_clothes
        writer = csv.DictWriter(f, fieldnames=list(d.keys()), delimiter=';')
        writer.writeheader()
        writer.writerow(d)
    # pygame.quit()