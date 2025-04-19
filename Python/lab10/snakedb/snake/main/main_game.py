import pygame
import random
import time

from db_commands import *

pygame.init()
pygame.mixer.init()
player_nickname, best_score, best_level, initial_size_snake = init_player()

print(f"Loaded player data: {player_nickname},
      score: {best_score}, 
      level: {best_level}, 
      size: {initial_size_snake}")
time.sleep(0.2)

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (242, 94, 166)
ORANGE = (252, 144, 3)
YELLOW_BANANA = (243, 255, 5)
BLUE = (5, 255, 247)
GRAY = (100, 100, 100)

width, height = 1440, 960
cell_size = 30

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
game_started = False

# Game variables
level = best_level
max_level = 1
score = 0
max_score = best_score
size_of_snake = initial_size_snake
new_level_at = 6
fruits = []  # The list of all fruits
walls = []  # List to store wall positions

paused = False

time_fruit_spawn_time = time.time()  # Time when the time fruit was spawned
time_fruit_lifetime = 8  # Time before the time fruit spawns again

def draw_time_fruit(time_fruit):
    # Remaining time for fruit
    remaining_time = int(time_fruit_lifetime - (time.time() - time_fruit_spawn_time))

    # REMAINING TIME ON FRUIt
    if remaining_time >= 0:
        
        time_text = font.render(f"{remaining_time}", True, WHITE)
        screen.blit(time_text, (time_fruit[0] + cell_size // 5, time_fruit[1] + cell_size // 5))

# SPAWNING THE FRUITS
def spawn_apple():
    while True:
        new_apple = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                     random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_apple not in snake_body and new_apple not in fruits and new_apple not in walls:
            return new_apple

def spawn_orange():
    while True:
        new_orange = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                      random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_orange not in snake_body and new_orange not in fruits and new_orange not in walls:
            return new_orange
        
def spawn_banana():
    while True:
        new_banana = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                      random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_banana not in snake_body and new_banana not in fruits and new_banana not in walls :
            return new_banana

def spawn_time_fruit():
    while True:
        new_time_fruit = [random.randrange(1, game_width // cell_size - 1) * cell_size + game_offset_x,
                          random.randrange(1, game_height // cell_size - 1) * cell_size + game_offset_y]
        if new_time_fruit not in snake_body and new_time_fruit not in fruits and new_time_fruit not in walls:
            return new_time_fruit

def create_walls_for_level(level):
    walls.clear()
    global fps
    
    if level == 2:
        fps = 5.5
        # Maze-like pattern for higher levels
        for i in range(1, game_width // cell_size - 1, 4):
            for j in range(1, game_height // cell_size - 1, 4):
                if random.random() < 0.05:  # 5% chance to place a wall block
                    walls.append([i*cell_size + game_offset_x, j*cell_size + game_offset_y])

    if level == 3:
        fps = 6
        # Maze-like pattern for higher levels
        for i in range(1, game_width // cell_size - 1, 4):
            for j in range(1, game_height // cell_size - 1, 4):
                if random.random() < 0.10:  # 10% chance to place a wall block
                    walls.append([i*cell_size + game_offset_x, j*cell_size + game_offset_y])
    
    if level == 4:
        fps = 6.5
        # Maze-like pattern for higher levels
        for i in range(1, game_width // cell_size - 1, 4):
            for j in range(1, game_height // cell_size - 1, 4):
                if random.random() < 0.15:  # 15% chance to place a wall block
                    walls.append([i*cell_size + game_offset_x, j*cell_size + game_offset_y])

    if level == 5:
        fps = 7
        # Maze-like pattern for higher levels
        for i in range(1, game_width // cell_size - 1, 4):
            for j in range(1, game_height // cell_size - 1, 4):
                if random.random() < 0.20:  # 20% chance to place a wall block
                    walls.append([i*cell_size + game_offset_x, j*cell_size + game_offset_y])

    if level >= 6:
        fps = 7.5
        # Maze-like pattern for higher levels
        for i in range(1, game_width // cell_size - 1, 4):
            for j in range(1, game_height // cell_size - 1, 4):
                if random.random() < 0.25:  # 25% chance to place a wall block
                    walls.append([i*cell_size + game_offset_x, j*cell_size + game_offset_y])

        
apple = spawn_apple()
fruits.append(apple)

orange = spawn_orange()
fruits.append(orange)

banana = spawn_banana()
fruits.append(banana)

time_fruit = spawn_time_fruit()
fruits.append(time_fruit)

create_walls_for_level(level)

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
            if event.key == pygame.K_p and alive:
                paused = not paused
                if paused:
                    pygame.mixer_music.pause()
                else:
                    pygame.mixer_music.unpause()
            elif event.key == pygame.K_ESCAPE and paused:
                running = False
                # Saving the game
                save_records(player_nickname, score, level, size_of_snake)
                
            elif not paused:
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
                    new_level_at = 10
                    level = 1
                    size_of_snake = 1
                    walls = []

                    create_walls_for_level(level)

                    time_fruit_spawn_time = time.time()  # Reset time for the next fruit
                    time_fruit = spawn_time_fruit()
                    fruits.append(time_fruit)

                    pygame.mixer_music.unpause()

                
                
    direction = change_to
    if alive and not paused:
        # Move snake
        if direction == 'UP':
            snake_pos[1] -= cell_size
        elif direction == 'DOWN':
            snake_pos[1] += cell_size
        elif direction == 'RIGHT':
            snake_pos[0] += cell_size
        elif direction == 'LEFT':
            snake_pos[0] -= cell_size
        
        if (snake_pos[0] < game_offset_x):
            snake_pos[0] = (game_offset_x + game_height) - cell_size
        elif (snake_pos[0] >= game_width + game_offset_x):
            snake_pos[0] = game_offset_x
        elif (snake_pos[1] < game_offset_y):
            snake_pos[1] = (game_offset_y + game_height) - cell_size
        elif (snake_pos[1] >= game_height + game_offset_y):
            snake_pos[1] = game_offset_y + cell_size

        # Check for collision with snake body and walls
        if (snake_pos in snake_body or snake_pos in walls):
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

    if not alive:   
        # Game Over screen
        text_gameover = font.render(f"Game Over!", True, WHITE)
        screen.blit(text_gameover, (width // 2 - 80, 845))
        text_restart = font.render(f"Press SPACE to restart", True, WHITE)
        screen.blit(text_restart, (width // 2 - 160, 875))
        pygame.mixer_music.pause()
        
        save_records_gameover(player_nickname, score, level)
        
    elif paused:
        pause_text = font.render("PAUSED (Press P to continue, ESC to save & quit)", True, WHITE)
        screen.blit(pause_text, (width // 2 - 250, height // 2))
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, GRAY, (wall[0], wall[1], cell_size - 1, cell_size - 1))

    
    # Draw snake and fruits
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], cell_size - 1, cell_size - 1))
    
    pygame.draw.rect(screen, RED, (apple[0], apple[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, ORANGE, (orange[0], orange[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, YELLOW_BANANA, (banana[0], banana[1], cell_size - 1, cell_size - 1))
    pygame.draw.rect(screen, PINK, (time_fruit[0], time_fruit[1], cell_size - 1, cell_size - 1))
    
    #TIMEFRUIT
    screen.blit(font.render(f"TIME FRUIT: SCORE + 10, SIZE + 4", True, PINK), (450, 10))

    # Display score and level
    screen.blit(font.render(f"Score: {score}", True, WHITE), (5, 10))
    screen.blit(font.render(f"Level: {level}", True, YELLOW), (5, 35))
    screen.blit(font.render(f"Size: {size_of_snake}", True, GREEN), (5, 60))
    screen.blit(font.render(f"Speed: {fps}", True, BLUE), (5, 85))
    screen.blit(font.render(f"10 scores = New level", True, YELLOW), (130, 35))

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
        new_level_at += 10

        create_walls_for_level(level)

        text_new_level = font.render(f"New Level!", True, PINK)
        screen.blit(text_new_level, (width // 2 - 100, height // 2 - 80))
        
        if level <= 6:
            text_speed_up = font.render(f"Speed + 0.5!", True, PINK)
            screen.blit(text_speed_up, (width // 2 - 100, height // 2 - 50))

        pygame.mixer.Sound(r"C:\PP2Main\Python\lab9\snake\bonus-points.mp3").play()
        
        pygame.display.flip()
        time.sleep(0.5)

    pygame.display.flip()
