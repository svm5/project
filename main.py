import sys

import pygame


WIDTH = 1000
HEIGHT = 800
LIGTH_BLUE = (0, 0, 150)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
START_PAGE = 1


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
            self.color = LIGTH_BLUE
        else:
            self.color = BLUE

    def check_mouse_position(self, mouse_pos):
        return self.pos_x <= mouse_pos[0] < self.pos_x + self.width and \
                self.pos_y <= mouse_pos[1] < self.pos_y + self.heigth

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.width, self.heigth))
        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.pos_x + self.width // 2, self.pos_y + self.heigth // 2))
        screen.blit(text, text_rect)
        # screen.blit(text, (self.pos_x + self.width // 2, self.pos_y + self.heigth // 2))

def draw_start_page(screen, mouse_pos):
    all_sprites = pygame.sprite.Group()
    background = pygame.sprite.Sprite()
    background.image = pygame.image.load("res/backgrounds/volcanoes.jpg").convert()
    background.image = pygame.transform.scale(background.image, (WIDTH, HEIGHT))
    background.rect = background.image.get_rect()
    all_sprites.add(background)
    all_sprites.draw(screen)

    buttons = []
    button_width = WIDTH // 3
    button_height = HEIGHT // 12
    font_size = HEIGHT // 20
    step = HEIGHT // 30

    # кнопки
    # начало игры
    button_begin_game = Button(WIDTH // 3, HEIGHT // 2, button_width, button_height, BLUE, "НАЧАТЬ ИГРУ", font_size, WHITE)
    button_begin_game.set_color(button_begin_game.check_mouse_position(mouse_pos))
    buttons.append(button_begin_game)

    # магазины
    button_shops = Button(WIDTH // 3, HEIGHT // 2 + 1 * step + 1 * button_height, button_width, button_height, BLUE, "МАГАЗИНЫ", font_size, WHITE)
    button_shops.set_color(button_shops.check_mouse_position(mouse_pos))
    buttons.append(button_shops)

    # настройки
    button_settings = Button(WIDTH // 3, HEIGHT // 2 + 2 * step + 2 * button_height, button_width, button_height, BLUE, "НАСТРОЙКИ", font_size, WHITE)
    button_settings.set_color(button_settings.check_mouse_position(mouse_pos))
    buttons.append(button_settings)

    # правила игры
    button_rules = Button(WIDTH // 3, HEIGHT // 2 + 3 * step + 3 * button_height, button_width, button_height, BLUE, "ПРАВИЛА ИГРЫ", font_size, WHITE)
    button_rules.set_color(button_rules.check_mouse_position(mouse_pos))
    buttons.append(button_rules)

    for button in buttons:
        button.draw(screen)


def main():
    pygame.init()
    pygame.display.set_caption("Малелькая колдунья")
    cur_page = START_PAGE

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouse = pygame.mouse.get_pos()
        if cur_page == START_PAGE :
            draw_start_page(screen, mouse)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())