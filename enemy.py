import pygame


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, name, health, damage):
        super().__init__()
        self.name = name
        self.health = health
        self.damage = damage

    def check_health(self):
        return self.health

    def get_damage(self, current_damage):
        self.health -= current_damage
        if self.check_health() <= 0:
            self.delete_enemy()
    
    def delete_enemy():
        pass


class Enemy1(BaseEnemy):
    def __init__(self):
        super().__init__("enemy1", 100, 20)

    def move(self):
        pass


class Enemy2(BaseEnemy):
    def __init__(self):
        super().__init__("enemy2", 500, 10)

    def move(self):
        pass
