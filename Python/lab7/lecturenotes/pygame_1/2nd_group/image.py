import pygame

class Pic():
    '''
    This class allows to draw a pic on the screen
    '''
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('chilly_dog.jpeg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.right = self.screen_rect.right
        

    def output(self):
        self.screen.blit(self.image, self.rect)


