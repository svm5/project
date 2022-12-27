import pygame


MAX_HEALTH = 100
MAX_NUMBER_OF_LIVES = 3

BASE_DRESS = 1


clothes = {
    BASE_DRESS: "girl_w.png"
}


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "player"
        self.health = MAX_HEALTH
        self.number_of_lives = MAX_NUMBER_OF_LIVES
        self.weapon = None
        self.amount_of_money = 0
        self.current_clothes = clothes[BASE_DRESS]

    def move(self):
        pass

    def attack(self):
        pass

    def set_weapon(self, new_weapon):
        self.weapon = new_weapon
    
    def set_clothes(self, new_clothes):
        self.current_clothes = clothes[new_clothes]
    
    def change_amount_of_money(self, amount):
        self.amount_of_money -= amount
    
    def get_amount_of_money(self):
        return self.amount_of_money