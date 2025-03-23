import pygame
import random

pygame.init()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)

width = 720
height = 480
screen = pygame.display.set_mode((width, height))

# Size of the snake
TSIDE = 30
# Grid size
MSIZE = width // TSIDE, height // TSIDE

# Start position
start_pos: tuple[int, int] = MSIZE[0] // 2, MSIZE[1] // 2
snake: list[tuple[int, int]] = [start_pos]
alive: bool = True

direction: int = 0
directions: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Apple
apple: tuple[int, int] = random.randint(0, MSIZE[0] - 1), random.randint(0, MSIZE[1] - 1)

clock = pygame.time.Clock()

running: bool = True

while running:
    clock.tick(5)
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_DOWN:
                direction = 1
            if event.key == pygame.K_LEFT:
                direction = 2
            if event.key == pygame.K_UP:
                direction = 3

    pygame.draw.rect(screen, GREEN, (snake[0][0] * TSIDE, snake[0][1] * TSIDE, TSIDE - 1, TSIDE - 1))   
    pygame.draw.rect(screen, RED, (apple[0] * TSIDE, apple[1] * TSIDE, TSIDE - 1, TSIDE - 1))
    
    if alive:
        # Move snake
        new_pos: tuple[int, int] = (snake[0][0] + directions[direction][0], snake[0][1] + directions[direction][1])
        
        # Check borders and self-collision
        if not (0 <= new_pos[0] < MSIZE[0] and 0 <= new_pos[1] < MSIZE[1]) or new_pos in snake:
            alive = False
        else:
            snake.insert(0, new_pos)
            if new_pos == apple:
                apple = random.randint(0, MSIZE[0] - 1), random.randint(0, MSIZE[1] - 1)
            else:
                snake.pop(-1)

    pygame.display.flip()
