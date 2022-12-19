import pygame
import sys
import os


sprite_image = {
    "1": "grass.png",
    "2": "grass_2.png"
}


""" Загруска картинки """


def load_image(name="testblock.png", colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        if not os.path.isfile("testblock.png"):
            sys.exit()
        else:
            image = pygame.image.load("testblock.png")
    else:
        image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def set_map(l):
    fl = open(l)
    fl2 = fl.read()
    fl.close()
    return [[j for j in i] for i in fl2.split("\n")]


""" Игрок - Спрайт """


class Sprite(pygame.sprite.Sprite):
    def __init__(self, size=None, *groups):
        super().__init__(*groups)
        self.image = load_image()
        self.rect = self.image.get_rect()
        if size is not None:
            self.set_size(size[0], size[1])

    def set_image(self, way, k=None):
        x, y = self.rect.x, self.rect.y
        self.image = load_image(way, k)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_size(self, w, h):
        x, y = self.rect.x, self.rect.y
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        #self.rect = self.rect_move(x, y)

    def rect_move(self, x, y):
        rect = self.rect.copy()
        rect.x += x
        rect.y += y
        return rect


class Block(Sprite):
    def __init__(self, indexs_coords, size=None, *groups):
        self.coords = indexs_coords
        super().__init__(size, *groups)
        self.do_rect_coords()

    def do_rect_coords(self):
        x = self.coords[1] * self.rect.width
        y = self.coords[0] * self.rect.height
        self.rect.x = x
        self.rect.y = y

    def set_image(self, way, k=None):
        x, y = self.rect.x, self.rect.y
        self.image = load_image(way, k)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.do_rect_coords()

    def set_size(self, w, h):
        x, y = self.rect.x, self.rect.y
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.do_rect_coords()

    def set_coords(self, y, x):
        self.coords = (y, x)
        self.do_rect_coords()
        

class Player(Sprite):
    def __init__(self, size=None, *groups):
        super().__init__(size, *groups)
        self.flip = False
        self.down = True
    
    def update(self):
        if self.down:
            self.move(0, 2)


running = True
step = 3
pygame.init()
pygame.display.set_caption("Всё ещё тест :/")
screen = pygame.display.set_mode((600, 600))
scr_width, scr_height = screen.get_size()
players = pygame.sprite.Group()
k_player = 1
for i in range(k_player):
    player = Player()
    player.set_image("", (255, 255, 255))
    player.set_size(40, 40)
    players.add(player)

moving = [False, False, False, False]
map_blocks = pygame.sprite.Group()
map_list = set_map("map.txt")
for y in range(len(map_list)):
    for x in range(len(map_list[0])):
        if map_list[y][x] not in sprite_image:
            continue
        block = Block((y, x))
        block.set_image(sprite_image[map_list[y][x]])
        block.set_size(70, 70)
        map_blocks.add(block)
m = 40
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    # m -= 0.1
    # if m < 10:
    #     m = 10
    user = players.sprites()[0]
    user.set_size(m, m)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if not(user.flip):
                    user.image = pygame.transform.flip(user.image, True, False)
                user.flip = True
                moving[0] = True
            if event.key == pygame.K_LEFT:
                if user.flip:
                    user.image = pygame.transform.flip(user.image, True, False)
                user.flip = False
                moving[1] = True
            if event.key == pygame.K_DOWN:
                moving[2] = True
            if event.key == pygame.K_UP:
                #if not(user.down):
                moving[3] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving[0] = False
            if event.key == pygame.K_LEFT:
                moving[1] = False
            if event.key == pygame.K_DOWN:
                moving[2] = False
            if event.key == pygame.K_UP:
                moving[3] = False
    screen.fill((128, 218, 235))
    for b in map_blocks.sprites():
        b.set_size(m, m)
    for player in players.sprites():
        if moving[0]:
            player.move(step, 0)
            kol = player.rect.collidelist([b.rect for b in map_blocks.sprites()])
            if kol != -1:
                user.rect.x = map_blocks.sprites()[kol].rect.left - user.rect.width
        if moving[1]:
            player.move(-step, 0)
            kol = player.rect.collidelist([b.rect for b in map_blocks.sprites()])
            if kol != -1:
                user.rect.x = map_blocks.sprites()[kol].rect.right
        if moving[2]:
            player.move(0, step)
            kol = player.rect.collidelist([b.rect for b in map_blocks.sprites()])
            if kol != -1:
                user.rect.y = map_blocks.sprites()[kol].rect.top - user.rect.height
        if moving[3]:
            player.move(0, -step)
            kol = player.rect.collidelist([b.rect for b in map_blocks.sprites()])
            #print(kol)
            if kol != -1:
                user.rect.y = map_blocks.sprites()[kol].rect.bottom
    
    """ Защита от застреваний в блоке"""
    players.update()
    for player in players.sprites():
        kol = player.rect.collidelist([b.rect for b in map_blocks.sprites()])
        if kol != -1:
            rect = map_blocks.sprites()[kol].rect
            if rect.top < user.rect.bottom < rect.bottom + user.rect.height - step:
                user.rect.y = rect.top - user.rect.height

            

    map_blocks.draw(screen)
    players.draw(screen)
    
    pygame.display.flip()


        