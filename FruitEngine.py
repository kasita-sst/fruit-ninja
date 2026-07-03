import pygame
import random
import math

class FruitEngine:
    def __init__(self, score_value, img_path, speed):
        self.x = random.randint(100, 700)
        self.y = 520

        try:
            self.fruit_image = pygame.image.load(img_path).convert_alpha()
        except pygame.error:
            self.fruit_image = pygame.Surface((40, 40), pygame.SRCALPHA)
            self.fruit_image.fill((255, 0, 0) if score_value > 0 else (0, 0, 0))
            
        self.rect = self.fruit_image.get_rect(center=(self.x, self.y))

        self.__score_value = score_value
        self.__is_alive = True
        
        self.gravity = 0.4
        
        angle_degrees = random.uniform(65, 115)
        angle_radians = math.radians(angle_degrees)
        
        self.speed_x = speed * math.cos(angle_radians)
        self.speed_y = -(speed * math.sin(angle_radians))

    def move(self):
        if self.__is_alive:
            self.speed_y += self.gravity
            
            self.x += self.speed_x
            self.y += self.speed_y
            
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def force_stop(self):
        self.__is_alive = False

    def get_score_value(self):
        return self.__score_value

    def draw(self, surface):
        if self.__is_alive:
            surface.blit(self.fruit_image, self.rect)
    
    def is_off_screen(self):
        if self.rect.top > 500:
            return True
        
        if self.rect.bottom < 0:
            return True

        if self.rect.right < 0 or self.rect.left > 800:
            return True
 
        return False


class Orange(FruitEngine):
    def __init__(self):
        super().__init__(score_value=1, img_path="assets/orange.png", speed=random.randint(50, 75))

class PineApple(FruitEngine):
    def __init__(self):
        super().__init__(score_value=2, img_path="assets/pineapple.png", speed=random.randint(20, 35))

class WaterMelon(FruitEngine):
    def __init__(self):
        super().__init__(score_value=1, img_path="assets/watermelon.png", speed=random.randint(15, 25))

class Bomb(FruitEngine):
    def __init__(self):
        super().__init__(score_value=-1, img_path="assets/bomb.png", speed=random.randint(15, 25))
