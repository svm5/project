import sys

import pygame
import pygame_gui


pygame.init()


WIDTH = 1000
HEIGHT = 800
CARD_WIDTH = 300
CARD_HEIGHT = 500
BUTTON_HEIGHT = 50
STEP_X = (WIDTH - 2 * CARD_WIDTH) // 3
STEP_Y = HEIGHT // 20

BACKGROUND_COLOR = (180, 0, 180)
CARD_COLOR = (0, 255, 0)
BUTTON_COLOR = (0, 0, 255)
BUTTON_COLOR_CHECKED = (0, 0, 150)

cards_sprites = pygame.sprite.Group()
buttons_sprites = pygame.sprite.Group()
buttons = []

magic = [[("Магия земли", 100), ("Магия воды", 300)],
        [("Магия воздуха", 800), ("Магия огня", 1500)]]

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
shop_clock = pygame.time.Clock()


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

        font = pygame.font.Font(None, 30)
        self.normal_text = text
        self.txt = font.render(text, True, "white")
        self.text_rect = self.txt.get_rect(center=(CARD_WIDTH // 2, BUTTON_HEIGHT // 2))
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
        font = pygame.font.Font(None, 30)
        self.txt = font.render(text, True, "white")
        self.text_rect = self.txt.get_rect(center=(CARD_WIDTH // 2, BUTTON_HEIGHT // 2))

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


class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, txt):
        super().__init__()
        self.x = x
        self.y = y
        self.txt = txt
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(pygame.Color(CARD_COLOR))
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        self.button = Button(x, y + CARD_HEIGHT - BUTTON_HEIGHT, CARD_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, "Купить", 30, "white")
        buttons.append((self, self.button))
        buttons_sprites.add(self.button)
        self.image.blit(self.button.image, (0, CARD_HEIGHT - BUTTON_HEIGHT))

        font = pygame.font.Font(None, 30)
        self.text = font.render(txt, True, "white")
        self.text_rect = self.text.get_rect(center=(CARD_WIDTH // 2, HEIGHT // 20))
        self.image.blit(self.text, self.text_rect)
    
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
    
    pygame.display.set_caption("Магазин")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    b = Button(50, 30, 100, 50, "black", "aaa", 30, "green")
    # buttons.append(b)
    buttons_sprites.add(b)

    pos_x = STEP_X
    pos_y = STEP_X
    for i in range(2):
        pos_x = STEP_X
        for j in range(2):
            card = Card(pos_x, pos_y, f"{magic[i][j][0]} - {magic[i][j][1]}")
            cards_sprites.add(card)
            pos_x += CARD_WIDTH + STEP_X
        pos_y += CARD_HEIGHT + STEP_Y

    running = True
    while running:
        time_delta = shop_clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for card, button in buttons:
                    if button.check_mouse_position(pos):
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
                for card, button in buttons:
                    if button.check_mouse_position(pos):
                        for card2, button2 in buttons:
                            if card2.button.get_text() != "Купить":
                                card2.button.set_text("Надеть")
                        card.button.set_text("Надето")
                        message = pygame_gui.windows.UIMessageWindow(
                            rect=pygame.Rect(250, 200, 300, 200),
                            manager=manager,
                            window_title="Сообщение",
                            html_message=f"Предмет '{card.txt}' приобретён успешно!"
                        )
                        break
            manager.process_events(event)
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        buttons_sprites.update()
        cards_sprites.update()
        cards_sprites.draw(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        # buttons_sprites.draw(screen)
        # buttons_sprites.update()
        # buttons_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())