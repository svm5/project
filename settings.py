import sys

import pygame


WIDTH = 1000
HEIGHT = 800


class SettingsPage:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.prepare_sprites()
        
        # self.buttons = []
        # self.prepare_buttons()

    def prepare_sprites(self):
        self.arrow_back = pygame.sprite.Sprite()
        self.arrow_back.image = pygame.image.load("res/icons/arrow_back.png").convert()
        self.arrow_back.image = pygame.transform.scale(self.arrow_back.image, (WIDTH // 10, WIDTH // 10))
        self.arrow_back.rect = self.arrow_back.image.get_rect()
        self.arrow_back.rect.x = WIDTH // 20
        self.arrow_back.rect.y = WIDTH // 20
        self.all_sprites.add(self.arrow_back)

    def draw_settings_page(self, screen, mouse_pos=None):
        self.all_sprites.draw(screen)

        # self.button_begin_game.set_color(self.button_begin_game.check_mouse_position(mouse_pos))
        # self.button_shops.set_color(self.button_shops.check_mouse_position(mouse_pos))
        # self.button_settings.set_color(self.button_settings.check_mouse_position(mouse_pos))
        # self.button_rules.set_color(self.button_rules.check_mouse_position(mouse_pos))

        # for button in self.buttons:
        #     button.draw(screen)


def main():
    pygame.init()
    pygame.display.set_caption("Настройки")

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    page = SettingsPage()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if page.arrow_back.rect.x <= event.pos[0] < page.arrow_back.rect.x + WIDTH // 10 and \
                        page.arrow_back.rect.y <= event.pos[1] < page.arrow_back.rect.y + WIDTH // 10:
                    return
        page.draw_settings_page(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())