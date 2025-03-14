import pygame

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 51)
green = (0, 255, 0)
red = (255, 0, 0)
sky_blue = (51, 255, 255)
dark_green = (0, 102, 0)


class Button():

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = sky_blue
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, dark_green)
        text_rect = text_surf.get_rect(center = self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
