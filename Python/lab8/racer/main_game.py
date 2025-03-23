import pygame
from pygame.locals import *
import random
import time

pygame.init()
pygame.mixer.init()

fps = pygame.time.Clock()
fps.tick(60)


# Colors

BLUE = (0, 0, 255)
YELLOW = (242, 242, 10)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)

# Variables for program
width = 400
height = 600
SPEED = 5
SCORE = 0
COINS = 0
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
pygame.display.set_caption("Racer")

background = pygame.image.load(r"C:\PP2Main\Python\lab8\racer\materials\AnimatedStreet.png")


# Actions for Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\PP2Main\Python\lab8\racer\materials\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            SCORE += 100
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Actions for Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\PP2Main\Python\lab8\racer\materials\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < width:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Class for Coins
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\PP2Main\Python\lab8\racer\materials\coin.gif")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 50)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Setting up player and enemy
P1 = Player()
E1 = Enemy()
C1 = Coin()
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins_sprite = pygame.sprite.Group()
coins_sprite.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

pygame.mixer_music.load(r"C:\PP2Main\Python\lab8\racer\materials\background.wav")
pygame.mixer_music.play(-1)

running = True
while running:
    
    # All events
        # After 1 sec speed becomes + 0,5
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.blit(background, (0, 0))

    screen.blit((font_small.render(str("Score:"), True, BLACK)), (10, 10))
    scores = font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (80, 10))

    screen.blit((font_small.render(str("Coins:"), True, BLACK)), (10, 30))
    coins = font_small.render(str(COINS), True, YELLOW)
    screen.blit(coins, (80, 30))
    
    # Move all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    # If collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer_music.stop()
        pygame.mixer.Sound(r"C:\PP2Main\Python\lab8\racer\materials\crash.wav").play()
        time.sleep(0.5)

        # Game Over
        screen.fill(RED)
        screen.blit(game_over, (30, 250))
        time.sleep(0.4)

        # Total Score
        screen.blit((font_medium.render(str("Total score:"), True, BLACK)), (30, 310))
        scores = font_medium.render(str(SCORE), True, BLACK)
        screen.blit(scores, (280, 310))
        time.sleep(0.4)

        # Total Coins
        screen.blit((font_medium.render(str("Total coins:"), True, BLACK)), (30, 360))
        scores = font_medium.render(str(COINS), True, YELLOW)
        screen.blit(scores, (280, 360))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()

    if pygame.sprite.spritecollideany(P1, coins_sprite):
        pygame.mixer.Sound(r"C:\PP2Main\Python\lab8\racer\materials\coin.mp3").play()
        COINS += 1
        C1.kill()

        C1 = Coin()
        coins_sprite.add(C1)
        all_sprites.add(C1)
    
    pygame.display.update()
    fps.tick(60)