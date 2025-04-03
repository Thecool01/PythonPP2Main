import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (242, 94, 166)
ORANGE = (252, 144, 3)
YELLOW_BANANA = (243, 255, 5)
BLUE = (5, 255, 247)

width, height = 1440, 960
cell_size = 40
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Font
font = pygame.font.SysFont("Bahnschrift", 30)
font_small = pygame.font.SysFont("Bahnschrift", 15)

# Snake setup
snake_pos = [width // 2, height // 2]
snake_body = [[width // 2, height // 2]]
direction = 'RIGHT'
change_to = direction


clock = pygame.time.Clock()
fps = 5
running = True
alive = True

# Game variables
level = 1
score = 0
size_of_snake = 1
new_level_at = 6
fruits = []  # The list of all fruits


"""SPAWNING THE FRUITS"""
def spawn_apple():
    while True:
        new_apple = [random.randrange(1, width // cell_size - 1) * cell_size,
                     random.randrange(1, height // cell_size - 1) * cell_size]
        if new_apple not in snake_body and new_apple not in fruits:
            return new_apple

def spawn_orange():
    while True:
        new_orange = [random.randrange(1, width // cell_size - 1) * cell_size,
                      random.randrange(1, height // cell_size - 1) * cell_size]
        if new_orange not in snake_body and new_orange not in fruits:  
            return new_orange
        
        
def spawn_banana():
    while True:
        new_banana = [random.randrange(1, width // cell_size - 1) * cell_size,
                      random.randrange(1, height // cell_size - 1) * cell_size]
        if new_banana not in snake_body and new_banana not in fruits:  
            return new_banana





apple = spawn_apple()
fruits.append(apple)

orange = spawn_orange()
fruits.append(orange)

banana = spawn_banana()
fruits.append(banana)


# MUSIC
pygame.mixer_music.load(r"C:\PP2Main\Python\lab9\snake\snake_soundtrack.mp3")
pygame.mixer_music.play(-1)
pygame.mixer_music.set_volume(0.5)

while running:
    
    clock.tick(fps)
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            # Changing the direction when typing the key
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif not alive and event.key == pygame.K_SPACE:
                # Restart game
                alive = True
                snake_pos = [width // 2, height // 2]
                snake_body = [[width // 2, height // 2]]
                direction = 'RIGHT'
                change_to = direction
                apple = [random.randrange(0, width // cell_size) * cell_size,
                         random.randrange(0, height // cell_size) * cell_size]
                fps = 5
                score = 0
                new_level_at = 6
                level = 1
                size_of_snake = 1
    
    direction = change_to
    if alive:
        # Move snake
        if direction == 'UP':
            snake_pos[1] -= cell_size
        elif direction == 'DOWN':
            snake_pos[1] += cell_size
        elif direction == 'RIGHT':
            snake_pos[0] += cell_size
        elif direction == 'LEFT':
            snake_pos[0] -= cell_size
        
        # Check collisions with boreders of the screen
        if (snake_pos[0] < 0 or snake_pos[0] >= width or
                snake_pos[1] < 0 or snake_pos[1] >= height or
                snake_pos in snake_body):
            alive = False
        else:
            snake_body.insert(0, list(snake_pos))
            
            if snake_pos == apple:
                score += 1
                size_of_snake += 1
                apple = spawn_apple()
            elif snake_pos == orange:
                score += 3
                size_of_snake += 2
                orange = spawn_orange()
            elif snake_pos == banana:
                score += 5
                size_of_snake += 3
                banana = spawn_banana()
            else:
                snake_body.pop()
            
            # Increasing the size of the snake after eating
            for _ in range(size_of_snake - len(snake_body)):
                snake_body.append(snake_body[-1])

    else:   
        # Game Over screen
        text_gameover = font.render(f"Game Over!", True, WHITE)
        screen.blit(text_gameover, (width // 2 - 80, height // 2))
        text_restart = font.render(f"Press SPACE to restart", True, WHITE)
        screen.blit(text_restart, (width // 2 - 160, height // 2 + 30))
    
    # Draw snake and apple
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, RED, (apple[0], apple[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, ORANGE, (orange[0], orange[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, YELLOW_BANANA, (banana[0], banana[1], cell_size - 1, cell_size - 1))
    
    # Display score and level
    screen.blit(font.render(f"Score: {score}", True, WHITE), (5, 10))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (5, 35))
    screen.blit(font.render(f"Size: {size_of_snake}", True, GREEN), (5, 60))
    screen.blit(font.render(f"Speed: {fps}", True, BLUE), (5, 85))

    # RULES
    screen.blit(font.render(f"Rules", True, WHITE), (5, 400))
    screen.blit(font.render(f"                Size    Score", True, WHITE), (5, 425))
    screen.blit(font.render(f"Apple:          +1       +1", True, WHITE), (5, 450))
    screen.blit(font.render(f"Orange:       +2       +3", True, WHITE), (5, 475))
    screen.blit(font.render(f"Banana:      +3       +5", True, WHITE), (5, 500))
    

    # Level up logic
    if score >= new_level_at:
        level += 1
        new_level_at += 6
        fps += 0.5

        text_new_level = font.render(f"New Level!", True, PINK)
        screen.blit(text_new_level, (width // 2 - 100, 30))
                    
        text_speed_up = font.render(f"Speed + 0.5!", True, PINK)
        screen.blit(text_speed_up, (width // 2 - 100, 60))

        pygame.mixer.Sound(r"C:\PP2Main\Python\lab9\snake\bonus-points.mp3").play()
        
        pygame.display.flip()
        time.sleep(0.5)
    pygame.display.flip()