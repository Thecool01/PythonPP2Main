import pygame

class Pic():
    def __init__(self, screen):

        self.screen = screen
        self.image = pygame.image.load('dog.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.center = self.screen_rect.center
    
    def output(self):
        self.screen.blit(self.image, self.rect)