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

width, height = 720, 480
cell_size = 30
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

# Apple
apple = [random.randrange(0, width // cell_size) * cell_size,
         random.randrange(0, height // cell_size) * cell_size]

clock = pygame.time.Clock()
fps = 5
running = True
alive = True

# Game variables
level = 1
score = 0
new_level_at = 3

while running:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
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
                new_level_at = 3
                level = 1
    
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
        
        # Check collisions
        if (snake_pos[0] < 0 or snake_pos[0] >= width or
                snake_pos[1] < 0 or snake_pos[1] >= height or
                snake_pos in snake_body):
            alive = False
        else:
            snake_body.insert(0, list(snake_pos))
            
            if snake_pos == apple:
                score += 1
                apple = [random.randrange(0, width // cell_size) * cell_size,
                         random.randrange(0, height // cell_size) * cell_size]
            else:
                snake_body.pop()
    else:
        # Game Over screen
        text_gameover = font.render(f"Game Over!", True, WHITE)
        screen.blit(text_gameover, (width // 2 - 40, height // 2))
        text_restart = font.render(f"Press SPACE to restart", True, WHITE)
        screen.blit(text_restart, (width // 2 - 100, height // 2 + 30))
    
    # Draw snake and apple
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, RED, (apple[0], apple[1], cell_size - 1, cell_size - 1))
    
    # Display score and level
    screen.blit(font.render(f"Score: {score}", True, WHITE), (5, 5))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (5, 30))
    
    # Level up logic
    if score == new_level_at:
        level += 1
        new_level_at += 3
        fps += 1
        text_new_level = font_small.render(f"New Level!", True, PINK)
        screen.blit(text_new_level, (width // 2 - 40, height // 2 + 30))
        text_speed_up = font_small.render(f"Speed + 1!", True, PINK)
        screen.blit(text_speed_up, (width // 2 - 40, height // 2 + 50))
        pygame.display.flip()
        time.sleep(1)
    
    pygame.display.flip()
