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
cell_size = 45

# Game area reduced by half and centered on the screen
game_width, game_height = 1080, 720
game_offset_x, game_offset_y = (width - game_width) // 2, (height - game_height) // 2  # Center of the game

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Font
font = pygame.font.SysFont("Bahnschrift", 30)
font_small = pygame.font.SysFont("Bahnschrift", 15)

# Snake setup
snake_pos = [game_width // 2 + game_offset_x, game_height // 2 + game_offset_y]
snake_body = [[game_width // 2 + game_offset_x, game_height // 2 + game_offset_y]]
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

time_fruit_spawn_time = time.time()  # Time when the time fruit was spawned
time_fruit_lifetime = 8  # Time before the time fruit spawns again

def draw_time_fruit(time_fruit):
    # Remaining time for fruit
    remaining_time = int(time_fruit_lifetime - (time.time() - time_fruit_spawn_time))

    # REMAINING TIME ON FRUIt
    if remaining_time >= 0:
        
        time_text = font.render(f"{remaining_time}", True, WHITE)
        screen.blit(time_text, (time_fruit[0] + cell_size // 3, time_fruit[1] + cell_size // 3))

# SPAWNING THE FRUITS
def spawn_apple():
    while True:
        new_apple = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                     random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_apple not in snake_body and new_apple not in fruits:
            return new_apple

def spawn_orange():
    while True:
        new_orange = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                      random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_orange not in snake_body and new_orange not in fruits:
            return new_orange
        
def spawn_banana():
    while True:
        new_banana = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                      random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_banana not in snake_body and new_banana not in fruits:
            return new_banana

def spawn_time_fruit():
    while True:
        new_time_fruit = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                          random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_time_fruit not in snake_body and new_time_fruit not in fruits:
            return new_time_fruit

apple = spawn_apple()
fruits.append(apple)

orange = spawn_orange()
fruits.append(orange)

banana = spawn_banana()
fruits.append(banana)

time_fruit = spawn_time_fruit()
fruits.append(time_fruit)

# MUSIC
pygame.mixer_music.load(r"C:\PP2Main\Python\lab9\snake\snake_soundtrack.mp3")
pygame.mixer_music.play(-1)
pygame.mixer_music.set_volume(0.7)

while running:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, GREEN, (game_offset_x, game_offset_y, game_width, game_height), 5)

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
                snake_pos = [game_width // 2 + game_offset_x, game_height // 2 + game_offset_y]
                snake_body = [[game_width // 2 + game_offset_x, game_height // 2 + game_offset_y]]
                direction = 'RIGHT'
                change_to = direction
                apple = spawn_apple()
                fps = 5
                score = 0
                new_level_at = 6
                level = 1
                size_of_snake = 1

                time_fruit_spawn_time = time.time()  # Reset time for the next fruit
                time_fruit = spawn_time_fruit()
                fruits.append(time_fruit)
    
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
        
        # Check collisions with borders of the screen (within the game area)
        if (snake_pos[0] < game_offset_x or snake_pos[0] >= game_width + game_offset_x or
                snake_pos[1] < game_offset_y or snake_pos[1] >= game_height + game_offset_y or
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
            
            if snake_pos == time_fruit:
                score += 10
                size_of_snake += 4
                time_fruit_spawn_time = time.time()  # Reset time for the next fruit
                time_fruit = spawn_time_fruit()
                fruits.append(time_fruit)

            # Increase snake size when eating fruits
            for _ in range(size_of_snake - len(snake_body)):
                snake_body.append(snake_body[-1])

    else:   
        # Game Over screen
        text_gameover = font.render(f"Game Over!", True, WHITE)
        screen.blit(text_gameover, (width // 2 - 80, 845))
        text_restart = font.render(f"Press SPACE to restart", True, WHITE)
        screen.blit(text_restart, (width // 2 - 160, 875))
    
    # Draw snake and fruits
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, RED, (apple[0], apple[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, ORANGE, (orange[0], orange[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, YELLOW_BANANA, (banana[0], banana[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, PINK, (time_fruit[0], time_fruit[1], cell_size - 1, cell_size - 1))
    
    #TIMEFRUIT
    screen.blit(font.render(f"TIME FRUIT: SCORE + 10, SIZE + 4", True, PINK), (300, 10))

    # Display score and level
    screen.blit(font.render(f"Score: {score}", True, WHITE), (5, 10))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (5, 35))
    screen.blit(font.render(f"Size: {size_of_snake}", True, GREEN), (5, 60))
    screen.blit(font.render(f"Speed: {fps}", True, BLUE), (5, 85))

    # RULES
    screen.blit(font.render(f"Rules:       Size    Score", True, WHITE), (1100, 5))
    screen.blit(font.render(f"Apple:          +1       +1", True, RED), (1100, 30))
    screen.blit(font.render(f"Orange:       +2       +3", True, ORANGE), (1100, 55))
    screen.blit(font.render(f"Banana:      +3       +5", True, YELLOW_BANANA), (1100, 80))

    # Time fruit spawning logic
    if time.time() - time_fruit_spawn_time >= time_fruit_lifetime and alive:
        time_fruit = spawn_time_fruit()
        fruits.append(time_fruit)
        time_fruit_spawn_time = time.time()  # Update spawn time for the time fruit

    if time.time() - time_fruit_spawn_time <= time_fruit_lifetime and alive:
        draw_time_fruit(time_fruit)

    # Level up logic
    if score >= new_level_at:
        level += 1
        new_level_at += 6
        fps += 0.5

        text_new_level = font.render(f"New Level!", True, PINK)
        screen.blit(text_new_level, (width // 2 - 100, height // 2 - 80))
                    
        text_speed_up = font.render(f"Speed + 0.5!", True, PINK)
        screen.blit(text_speed_up, (width // 2 - 100, height // 2 - 50))

        pygame.mixer.Sound(r"C:\PP2Main\Python\lab9\snake\bonus-points.mp3").play()
        
        pygame.display.flip()
        time.sleep(0.5)

    pygame.display.flip()
