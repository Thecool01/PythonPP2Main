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
new_speed = 30
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)
pygame.display.set_caption("Racer")

background = pygame.image.load(r"C:\PP2Main\Python\lab8\racer\materials\AnimatedStreet.png")

#Images of coins
c1_path = r"C:\PP2Main\Python\lab9\racer\materials\monet1.png"
c2_path = r"C:\PP2Main\Python\lab9\racer\materials\monet3.png"
c3_path = r"C:\PP2Main\Python\lab9\racer\materials\monet5.png"

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
    def __init__(self, path, enemies, coins,  counting):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, width - 40), 50)
        self.enemies = enemies
        self.counting = counting
        self.coins = coins
        self.spawn_coin()
    
    def spawn_coin(self):
        max_attempts = 10 
        for _ in range(max_attempts):
            self.rect.center = (random.randint(40, width - 40), random.randint(50, 200))
            if (not pygame.sprite.spritecollideany(self, self.enemies) and 
                not pygame.sprite.spritecollideany(self, self.coins)):
                return
    
        # If there is no place, just spawn at the top
        self.rect.center = (random.randint(40, width - 40), 0)
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.spawn_coin()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Setting up player and enemy
P1 = Player()
E1 = Enemy()


#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins_sprite = pygame.sprite.Group()

C1 = Coin(c1_path, enemies, coins_sprite, 1)
C2 = Coin(c2_path, enemies, coins_sprite, 3)
C3 = Coin(c3_path, enemies, coins_sprite, 5)

coins_sprite.add(C1, C2, C3)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1, C2, C3)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

pygame.mixer_music.load(r"C:\PP2Main\Python\lab8\racer\materials\background.wav")
pygame.mixer_music.play(-1)

running = True
while running:
    # All actions
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.blit(background, (0, 0))

    # Information about game 
    screen.blit((font_small.render(str(f"Score: {SCORE}"), True, BLACK)), (10, 10))
    screen.blit((font_small.render(str(f"Money: {COINS}"), True, BLACK)), (10, 30))
    screen.blit((font_small.render(str(f"Speed: {round(SPEED, 1)}"), True, BLACK)), (10, 50))
    screen.blit((font_small.render(str(f"30 money = + 0.3 speed"), True, BLACK)), (10, 70))
    
    # Move all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    # Checking for collision with the enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer_music.stop()
        pygame.mixer.Sound(r"C:\PP2Main\Python\lab8\racer\materials\crash.wav").play()
        time.sleep(0.5)

        # Game Over
        screen.fill(RED)
        screen.blit(game_over, (30, 250))
        time.sleep(0.4)

        # Total Score
        screen.blit((font_medium.render(str(f"Total score: {SCORE}"), True, BLACK)), (30, 310))

        time.sleep(0.4)

        # Total Coins
        screen.blit((font_medium.render(str(f"Total money: {COINS}"), True, BLACK)), (30, 360))
        
        time.sleep(0.2)


        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()

    # Checking for collecting the coin
    collected_coin = pygame.sprite.spritecollideany(P1, coins_sprite)
    if collected_coin:
        pygame.mixer.Sound(r"C:\PP2Main\Python\lab8\racer\materials\coin.mp3").play()

        COINS += collected_coin.counting
        collected_coin.kill()

        # New coin spawning
        new_coin = Coin(c1_path if collected_coin.counting == 1 else 
                        c2_path if collected_coin.counting == 3 else 
                        c3_path, enemies, coins_sprite, collected_coin.counting)

        coins_sprite.add(new_coin)
        all_sprites.add(new_coin)


    if COINS > new_speed:
        SPEED += 0.3
        new_speed += 30
        screen.blit((font_small.render(str(f"NEW SPEED: + 0.3"), True, BLACK)), (100, 150))
        pygame.display.flip()
        time.sleep(0.5)

    pygame.display.update()
    fps.tick(60)
