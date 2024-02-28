import pygame

import settings as s


class UI:

    def __init__(self):

        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load("../graphics/logos/ensōurobo.png")
        self.font = pygame.font.Font("../graphics/now_regular.otf", 36)
        self.company_text = "Dark Forest Presents"
        self.by_text = "A GAME BY ALEKSANDR HEMINGWAY"
        self.title_text = s.TITLE

        self.image_x = (self.surface.get_width() // 2) - 110
        self.image_y = (self.surface.get_height() // 2) - 110

    def draw_text(self):

        company_surface = self.font.render(self.company_text, True, "blue")
        company_rect = company_surface.get_rect(
            topright=(
                self.surface.get_width() - 80,
                self.surface.get_height() - 80
            )
        )

        by_surface = self.font.render(self.by_text, True, "blue")
        by_rect = by_surface.get_rect(
            center=(
                self.surface.get_width() // 2,
                self.surface.get_height() * 0.75
            )
        )

        self.surface.blit(company_surface, company_rect)
        self.surface.blit(by_surface, by_rect)
    
    def fade_in(self):

        clock = pygame.time.Clock()
        alpha = 0
    
        while alpha < 255:

            self.surface.fill((0 + alpha, 0 + alpha, 0 + alpha))
            self.surface.set_alpha(alpha)
            self.surface.blit(self.image, (self.image_x, self.image_y))
            self.draw_text()
            pygame.display.flip()
            alpha += 2.5
            clock.tick(30)
    
        pygame.time.wait(1250)

    def fade_out(self):

        clock = pygame.time.Clock()
        alpha = 255

        while alpha > 0:

            self.surface.fill((255, 255, 255))
            self.surface.set_alpha(alpha)
            self.surface.blit(self.image, (self.image_x, self.image_y))
            self.draw_text()
            pygame.display.flip()
            alpha -= 2.5
            clock.tick(30)
    
        pygame.time.wait(1250)

    def reveal_game(self):
    
        clock = pygame.time.Clock()
        alpha = 0
    
        while alpha < 255:
    
            self.surface.fill((255 - alpha, 255 - alpha, 255 - alpha))
            self.surface.blit(self.image, (self.image_x, self.image_y))
            self.draw_text()
            pygame.display.flip()
            alpha += 2.5
            clock.tick(30)
    
    def run_splash(self):
        
        self.fade_in()
        self.fade_out()
        self.reveal_game()
