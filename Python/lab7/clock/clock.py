import pygame
import pygame.gfxdraw
from datetime import datetime

pygame.init()
clock_path = r"C:\PP2Main\Python\lab7\clock\clock.png"
size = 600
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("Clock")

clock_tick = pygame.time.Clock()
font = pygame.font.Font(None, 50)

# Function for drawing the second hand
def draw_second_hand(surface, second):
    hand_length = size * 0.45
    angle = second * 6
    end_x = 300 + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = 300 + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, (255, 45, 45), (300, 300), (end_x, end_y), 3)

# Function for drawing the minute hand
def draw_minute_hand(surface, minute):
    hand_length = size * 0.35
    angle = minute * 6
    end_x = 300 + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = 300 + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, (70, 70, 70), (300, 300), (end_x, end_y), 7)

# Function for drawin the hour hand
def draw_hour_hand(surface, hour):
    hand_length = size * 0.30
    angle = hour * 6
    end_x = 300 + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = 300 + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, (70, 70, 70), (300, 300), (end_x, end_y), 7)

# Function for digital time
def draw_digital_time(surface, hour, minute, second):
    time_str = f"{hour:02}:{minute:02}:{second:02}"
    text_surface = font.render(time_str, True, (45, 45, 45))
    surface.blit(text_surface, (300, 350))

def run():
    clock = pygame.image.load(clock_path)
    clock = pygame.transform.scale(clock, (600, 600))
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(clock, (0, 0))
        now = datetime.now()
        draw_second_hand(screen, now.second)
        draw_minute_hand(screen, now.minute)
        draw_hour_hand(screen, now.hour)
        draw_digital_time(screen, now.hour, now.minute, now.second)
        
        pygame.display.flip()
        clock_tick.tick(30)

run()