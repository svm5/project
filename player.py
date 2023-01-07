import pygame


MAX_HEALTH = 100
MAX_NUMBER_OF_LIVES = 3

BASE_DRESS = 1


clothes = {
    BASE_DRESS: "girl_w.png"
}


class Player(pygame.sprite.Sprite):
    def __init__(self, amount_of_money, weapon, current_clothes, shop_weapon, shop_clothes):
        super().__init__()
        self.name = "player"
        self.health = MAX_HEALTH
        self.number_of_lives = MAX_NUMBER_OF_LIVES
        self.weapon = weapon
        self.amount_of_money = amount_of_money
        self.current_clothes = clothes[current_clothes]
        self.shop_weapon = shop_weapon.copy()
        self.shop_clothes = shop_clothes.copy()

    def move(self):
        pass

    def attack(self):
        pass

    def set_weapon(self, new_weapon):
        self.weapon = new_weapon

    def set_weapon_state(self, number, state):
        self.shop_weapon[number] = state
    
    def set_clothes(self, new_clothes):
        self.current_clothes = clothes[new_clothes]
    
    def change_amount_of_money(self, amount):
        self.amount_of_money += amount
    
    def get_amount_of_money(self):
        return self.amount_of_money

    def get_weapon_state(self, number):
        if self.shop_weapon[number] == 0:
            return "Купить"
        elif self.shop_weapon[number] == 1:
            return "Надеть"
        else:
            return "Надето"