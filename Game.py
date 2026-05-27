import pygame
import sys
import random

from HandTracker import HandTracker
from FruitEngine import Orange, PineApple, WaterMelon, Bomb

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 500))
        self.clock = pygame.time.Clock()
        self.running = False

        self.score = 0
        self.lives = 3
        self.state = "MENU" 
        
        self.font = pygame.font.SysFont("Arial", 40)
        self.start_button = pygame.Rect(300, 220, 200, 60)

        self.hand_tracker = HandTracker()

        self.active_fruits = []
        self.spawn_timer = 0
        
    def start(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.state == "GAME":
                        self.hand_tracker.release_camera()
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "MENU":
                        if self.start_button.collidepoint(event.pos):
                            self.score = 0
                            self.lives = 3
                            
                            self.hand_tracker.start_camera()
                            self.state = "GAME"
                            
                    elif self.state == "GAME_OVER":
                        self.state = "MENU"

            if self.state == "MENU":
                self.draw_menu_ui()
            elif self.state == "GAME":
                self.draw_game_ui()
            elif self.state == "GAME_OVER":
                self.draw_game_over_ui()

            pygame.display.flip()
            self.clock.tick(30)
            
        pygame.quit()
        sys.exit()

    def increase_score(self, score_value):
        self.score += score_value

    def decrease_lives(self):
        self.lives -= 1
        if self.lives <= 0:
            self.hand_tracker.release_camera()
            self.state = "GAME_OVER"
    
    def draw_menu_ui(self):
        self.screen.fill((240, 240, 240))
        
        title = self.font.render("FRUIT NINJA", True, (30, 30, 30))
        self.screen.blit(title, (400 - title.get_width() // 2, 100))
        
        pygame.draw.rect(self.screen, (0, 200, 100), self.start_button, border_radius=8)
        btn_label = self.font.render("PLAY", True, (255, 255, 255))
        self.screen.blit(btn_label, (400 - btn_label.get_width() // 2, 230))
        
    def draw_game_ui(self):
        frame, results, pos_x, pos_y = self.hand_tracker.process_frame()
        frame = pygame.transform.flip(frame, True, False) 

        print(f"Index Finger Position - X: {pos_x}, Y: {pos_y}")

        if frame is not None:
            self.screen.blit(frame, (0, 0))
        else:
            self.screen.fill((50, 50, 50))     

        self.spawn_timer += 1

        #if 1.5 second have passed, add more fruit or bomb!
        if self.spawn_timer >= 45:
            fruit_types = [Orange, PineApple, WaterMelon, Bomb]
            chosen_class = random.choice(fruit_types)
            new_spawn = chosen_class()
            self.active_fruits.append(new_spawn)
            self.spawn_timer = 0

        for fruit in self.active_fruits[::-1]:
            fruit.move()
            fruit.draw(self.screen)   

            if pos_x is not None and pos_y is not None:
                flexible_hitbox = fruit.rect.inflate(15, 15)
                if flexible_hitbox.collidepoint(pos_x, pos_y):
                    if isinstance(fruit, Bomb):
                        self.decrease_lives()
                    else:
                        self.increase_score(fruit.get_score_value())

                    fruit.force_stop()
                    self.active_fruits.remove(fruit)
                    continue

                if fruit.is_off_screen():
                    self.active_fruits.remove(fruit)
            
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 0, 0))
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (650, 20))
        

    def draw_game_over_ui(self):
        self.screen.fill((0, 0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        
        self.screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 150))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 220))

if __name__ == "__main__":
    game = Game()
    game.start()
