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

width = 720
height = 480
screen = pygame.display.set_mode((width, height))

# Size of the snake
TSIDE = 30

# Center
MSIZE = width // TSIDE, height // TSIDE

# Font
font = pygame.font.SysFont("Bahnschrift", 30)
font_small = pygame.font.SysFont("Bahnschrift", 15)

# Start position
start_pos = MSIZE[0] // 2, MSIZE[1] // 2
snake = [start_pos]
alive = True

direction = 0
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Apple
apple = random.randint(0, MSIZE[0] - 1), random.randint(0, MSIZE[1] - 1)

clock = pygame.time.Clock()
fps = 5
running = True

# Const
level = 1
score = 0
new_level_at = 3

pygame.mixer_music.load(r"C:\PP2Main\Python\lab8\snake\snake_soundtrack.mp3")
pygame.mixer_music.play(-1)

while running:
    

    clock.tick(fps)
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        # Checking for key and changing the direction
        if event.type == pygame.KEYDOWN:
            if alive:
                if event.key == pygame.K_RIGHT and direction != 2:
                    direction = 0
                if event.key == pygame.K_DOWN and direction != 3:
                    direction = 1
                if event.key == pygame.K_LEFT and direction != 0:
                    direction = 2
                if event.key == pygame.K_UP and direction != 1:
                    direction = 3
            else:
                # If dead, press the space to revive
                if event.key == pygame.K_SPACE:
                    pygame.mixer_music.unpause()
                    alive = True
                    snake = [start_pos]
                    apple = random.randint(0, MSIZE[0] - 1), random.randint(0, MSIZE[1] - 1)
                    fps = 5
                    score = 0
                    new_level_at = 3
                    level = 1
                    
    [pygame.draw.rect(screen, "green", (x * TSIDE, y * TSIDE, TSIDE - 1, TSIDE - 1)) for x, y in snake]
    pygame.draw.rect(screen, RED, (apple[0] * TSIDE, apple[1] * TSIDE, TSIDE - 1, TSIDE - 1))
    
    if alive:
        # Position of the snake
        new_pos = snake[0][0] + directions[direction][0], snake[0][1] + directions[direction][1]
        
        # The borders
        if not (0 <= new_pos[0] < MSIZE[0] and 0 <= new_pos[1] < MSIZE[1]) or new_pos in snake:
            alive = False
        
        else:
            snake.insert(0, new_pos)
            if new_pos == apple:
                score += 1
                apple = random.randint(0, MSIZE[0] - 1), random.randint(0, MSIZE[1] - 1)
            else:
                snake.pop(-1)
    else:
        # Text in the end of the game
        pygame.mixer_music.pause()
        text_gameover = font.render(f"Game Over!", True, WHITE)
        screen.blit(text_gameover, (width // 2 - 40, height // 2))
        text_restart = font.render(f"Press SPACE to restart", True, WHITE)
        screen.blit(text_restart, (width // 2 - 40, height // 2 + 30))


    # The Score
    screen.blit((font.render(f"Score: {score}", True, WHITE)), (5, 5))
    screen.blit((font.render(f"Level: {level}", True, YELLOW)), (5, 30))
    # Level
    if score == new_level_at:
        pygame.mixer_music.pause()
        level += 1
        new_level_at += 3
        fps += 1
        pygame.mixer.Sound(r"C:\PP2Main\Python\lab8\snake\bonus-points.mp3").play()
        text_new_level = font_small.render(f"New Level!", True, PINK)
        screen.blit(text_new_level, (width // 2 - 40, height // 2 + 30))

        text_speed_up = font_small.render(f"Speed + 1!", True, PINK)
        screen.blit(text_speed_up, (width // 2 - 40, height // 2 + + 50))
        pygame.display.flip()
        time.sleep(1)
        pygame.mixer_music.unpause()

    pygame.display.flip()
