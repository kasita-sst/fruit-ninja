import pygame
import random

class FruitEngine:
    def __init__(self, score_value, img_path, speed):
        self.randomize = random.randint(0, 800)

        self.fruit_image = pygame.image.load(img_path)
        self.score_value = score_value

        self.speed = speed
    
    def move(self):
        pass

    def get_score_value(self):
        return self.score_value
    
    def get_image(self):
        return self.fruit_image
    
    def get_speed(self):
        return self.speed

class Orange(FruitEngine):
    def __init__(self):
        super().__init__(score_value=1, img_path="assets/orange.png", speed=5)
    
    def move(self):
        pass

class PineApple(FruitEngine):
    def __init__(self):
        super().__init__(score_value=2, img_path="assets/pineapple.png", speed=10)
    
    def move(self):
        pass

class WaterMelon(FruitEngine):
    def __init__(self):
        super().__init__(score_value=1, img_path="assets/watermelon.png", speed=5)
    
    def move(self):
        pass

class Bomb(FruitEngine):
    def __init__(self):
        super().__init__(score_value=-1, img_path="assets/bomb.png", speed=5)
    
    def move(self):
        pass