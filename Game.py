import pygame
import sys

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
        
    def start(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                #left mouse clicked
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "MENU":
                        #if click on start button, reset score and lives, and go to state "GAME"
                        if self.start_button.collidepoint(event.pos):
                            self.score = 0
                            self.lives = 3
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
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

    def increase_score(self):
        self.score += 1
    
    def decrease_lives(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = "GAME_OVER"
    
    def draw_menu_ui(self):
        self.screen.fill((240, 240, 240))
        
        title = self.font.render("FRUIT NINJA", True, (30, 30, 30))
        self.screen.blit(title, (400 - title.get_width() // 2, 100))
        
        pygame.draw.rect(self.screen, (0, 200, 100), self.start_button, border_radius=8)
        
        btn_label = self.font.render("PLAY", True, (255, 255, 255))
        self.screen.blit(btn_label, (400 - btn_label.get_width() // 2, 230))
        
    def draw_game_ui(self):
        pass

    def draw_game_over_ui(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.start()
