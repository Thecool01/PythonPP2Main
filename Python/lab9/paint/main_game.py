import pygame
import math
import os

pygame.init()
pygame.mixer.init()

# Screen and canvas sizes
width = 1000
height = 480
sidebar_width = 150

screen = pygame.display.set_mode((width, height))
canva = pygame.Surface((width - sidebar_width, height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)
light_grey = (180, 180, 180)

# Constants
running = True
mouse_click = False
last_mouse_pos = None
painting_mode = 'line'
scale = 2  # Brush size
current_color = black  # Default brush color
start_pos = None

# Font
font = pygame.font.SysFont("Leelawadee", 20)
font_small = pygame.font.SysFont("Leelawadee", 15)
font_smaller = pygame.font.SysFont("Leelawadee", 10)

# Tool buttons
buttons = {
    "Line":                     pygame.Rect(10, 20, 135, 20),
    "Rectangle":                pygame.Rect(10, 45, 135, 20),
    "Circle":                   pygame.Rect(10, 70, 135, 20),
    "Square":                   pygame.Rect(10, 95, 135, 20),
    "Right triangle":           pygame.Rect(10, 120, 135, 20),
    "Equilateral triangle":     pygame.Rect(10, 145, 135, 20),
    "Rhombus":                  pygame.Rect(10, 170, 135, 20),
    "Eraser":                   pygame.Rect(10, 195, 135, 20),
    "+":                        pygame.Rect(50, 260, 20, 20),
    "-":                        pygame.Rect(10, 260, 20, 20),
    "<":                        pygame.Rect(10, 355, 20, 20),
    "||":                       pygame.Rect(35, 355, 20, 20),
    ">":                        pygame.Rect(60, 355, 20, 20),
    "Clear":                    pygame.Rect(90, 450, 50, 20),

    
}

button_states = {mode: False for mode in buttons} # The status of button(click or not)
# Color selection buttons
color_buttons = {
    black: pygame.Rect(10, 390, 30, 30),
    blue: pygame.Rect(50, 390, 30, 30),
    red: pygame.Rect(10, 440, 30, 30),
    yellow: pygame.Rect(50, 440, 30, 30),
}

# Music 
music_folder = r"C:\PP2Main\Python\lab9\music"
music_mp3 = [os.path.join(music_folder, track) for track in os.listdir(music_folder) if track.endswith(".mp3")]

current_music = 0
music_play = True

pygame.mixer_music.load(music_mp3[current_music])
pygame.mixer_music.play(-1)
pygame.mixer_music.set_volume(0.5)

message = f"{os.path.basename(music_mp3[current_music])}"

screen.fill(black)
canva.fill(white)

# All left buttons
def draw_buttons():
    
    for mode, rect in buttons.items():
        color = (233, 233, 233) if button_states[mode] else (light_grey if painting_mode == mode else grey)
        # color = light_grey if painting_mode == mode else grey
        pygame.draw.rect(screen, color, rect)
        text = font_small.render(mode.capitalize(), True, white)
        screen.blit(text, (rect.x + 8, rect.y))
        pygame.draw.rect(screen, white, rect, 1)

    # Display current brush size
    scale_text = font.render(f"Size: {scale}", True, white)
    screen.blit(scale_text, (10, 230))

    # Draw color selection buttons
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, white, rect, 3)  # Highlight active color

# All events with keyboard, mouse, etc.
def handle_events():

    global running, mouse_click, last_mouse_pos, painting_mode, scale, current_color, current_music, music_play, message

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            mx, my = pygame.mouse.get_pos()

            # Check if a tool button was clicked
            for mode, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    if mode == "+" and scale < 30:
                        scale += 1
                    elif mode == "-" and scale > 1:
                        scale -= 1
                    elif mode == "Clear":
                        canva.fill(white)
                    else:
                        painting_mode = mode
                if rect.collidepoint(event.pos):
                    button_states[mode] = True  # Button is clicked
                
                if rect.collidepoint(mx, my):
                    if mode == "<":
                        current_music = (current_music - 1) % len(music_mp3)
                        pygame.mixer_music.load(music_mp3[current_music])
                        message = f"{os.path.basename(music_mp3[current_music])}"
                        pygame.mixer_music.play(-1)
                    
                    elif mode == ">":
                        current_music = (current_music + 1) % len(music_mp3)
                        pygame.mixer_music.load(music_mp3[current_music])
                        message = f"{os.path.basename(music_mp3[current_music])}"
                        pygame.mixer_music.play(-1)

                    elif mode == "||":
                        if music_play:
                            pygame.mixer_music.pause()
                            music_play = False
                        elif not music_play:
                            pygame.mixer_music.unpause()
                            music_play = True
                    
            # Check if a color button was clicked
            for color, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    current_color = color

            if mx >= sidebar_width:
                global start_pos
                start_pos = (mx - sidebar_width, my) # Handle the start position
            
        """PROCESS OF DRAWING ALL FIGURES"""    
        if event.type == pygame.MOUSEBUTTONUP:
            for mode, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    button_states[mode] = False  # Button is released
                
            mouse_click = False
            last_mouse_pos = None
            # Preview before drawing a shape (rectangle and circle)

            
            if start_pos is not None:
                # Coordinates of the mouse
                mx, my = pygame.mouse.get_pos()
                mx -= sidebar_width

                width = abs(mx - start_pos[0])
                height = abs(my - start_pos[1])

                #RECTANGLE
                if painting_mode == "Rectangle":
                    pygame.draw.rect(canva, current_color, 
                                     (min(start_pos[0], mx), min(start_pos[1], my), 
                                      width, height), scale) # To draw a rectangle correctly in either direction.

                #CIRCLE
                elif painting_mode == "Circle":
                    # The radius(Radius is half of the diameter)
                    radius = max(width, height) // 2
                    center = (min(start_pos[0], mx) + width // 2, min(start_pos[1], my) + height // 2) # To draw a circle correctly in either direction.
                    pygame.draw.circle(canva, current_color, center, radius, scale)
                
                #SQUARE
                elif painting_mode == "Square":
                    # Size of the Square
                    side = max(abs(mx - start_pos[0]), abs(my - start_pos[1]))

                    x = min(start_pos[0], mx)
                    y = min(start_pos[1], my)

                    pygame.draw.rect(canva, current_color, 
                                     (min(start_pos[0], mx), min(start_pos[1], my), 
                                      side, side), scale)
                
                #RIGHT TRIANGLE
                elif painting_mode == "Right triangle":

                    side = max(abs(mx - start_pos[0]), abs(my - start_pos[1]))

                    # 1) We must find the height of the trianle. h = sqrt(3) / 2 * 3
                    # 2) Find top point 3) Left point 4) Right point
                    top = (start_pos[0], start_pos[1])
                    left = (start_pos[0] - side // 2, start_pos[1] + int(math.sqrt(3) / 2 * side))
                    right = (start_pos[0] + side // 2, start_pos[1] + int(math.sqrt(3) / 2 * side))

                    # Poligon is drawing with 3 points
                    pygame.draw.polygon(canva, current_color, [top, left, right], scale)

                #EQUILATERAL TRIANGLE
                elif painting_mode == "Equilateral triangle":

                    side = max(abs(mx - start_pos[0]), abs(my - start_pos[1]))

                    base_center_x = (start_pos[0] + mx) // 2

                    # The points of the rectangle
                    top = (base_center_x, start_pos[1])
                    bottom_left = (start_pos[0], my)
                    bottom_right = (mx, my)
                
                    pygame.draw.polygon(canva, current_color, [top, bottom_left, bottom_right], scale)
                
                #RHOMBUS
                elif painting_mode == "Rhombus":
                    
                    # Center points
                    center_x = (start_pos[0] + mx) // 2
                    center_y = (start_pos[1] + my) // 2

                    # Points of the Rhombus
                    top = (center_x, start_pos[1]) # Top point 
                    bottom = (center_x, my) # Bottom point 
                    left = (start_pos[0], center_y) # Left point
                    right = (mx, center_y) # Right point

                    pygame.draw.polygon(canva, current_color, [top, left, bottom, right], scale)

            start_pos = None

"""PROCCESS OF PRINTING AND ERASING"""
def update():

    global last_mouse_pos

    mx, my = pygame.mouse.get_pos()
    mx -= sidebar_width  # Adjust mouse position for the canvas

    if mouse_click and last_mouse_pos is not None and mx >= 0:
        if painting_mode == 'Line':
            pygame.draw.line(canva, current_color, last_mouse_pos, (mx, my), scale)
        elif painting_mode == 'Eraser':
            pygame.draw.line(canva, white, last_mouse_pos, (mx, my), scale)

    if mouse_click and mx >= 0:
        last_mouse_pos = (mx, my)

# Rendering all parts of the program
def render():

    screen.fill(black)  # Clear the screen
    pygame.draw.rect(screen, grey, (0, 0, sidebar_width, height))  # Draw sidebar
    screen.blit(canva, (sidebar_width, 0))  # Display the canvas
    draw_buttons()  # Draw buttons

    """MUSIC"""
    #PLAYER TEXT
    text_player = font.render("Player", True, white)
    screen.blit(text_player, (10, 325))

    #NOW PLAYING TEXT
    pygame.draw.rect(screen, black, (750, 0, 250, 50))
    text_music = font_small.render("Now playing:", True, white)
    screen.blit(text_music, (755, 5))

    #MUSIC NAME
    text_now_music = font_small.render(message, True, (0, 200, 0))
    screen.blit(text_now_music, (755, 25))

    """RENDERING THE FIGURES BEFORE DRAWING"""
    if mouse_click and start_pos:
        mx, my = pygame.mouse.get_pos()
        mx -= sidebar_width

        width_l = abs(mx - start_pos[0]) # Local width for figures
        height_l = abs(my - start_pos[1]) # local height for figures

        #RENDERING RECTANGLE
        if painting_mode == "Rectangle":
            # Drawing the rectangle on the position where mouse were clicked
             pygame.draw.rect(screen, current_color, 
                             (sidebar_width + min(start_pos[0], mx), 
                              min(start_pos[1], my), width_l, height_l), scale)

        #RENDERING CIRCLE
        elif painting_mode == "Circle":
            radius = max(width_l, height_l) // 2 # Radius is a half of diameter
            
            # Drawing the circle on the position where mouse were clicked
            center = (sidebar_width + min(start_pos[0], mx) + width_l // 2, 
                      min(start_pos[1], my) + height_l // 2)
            pygame.draw.circle(screen, current_color, center, radius, scale)
        
        #RENDERING SQUARE
        elif painting_mode == "Square":
                    side = max(abs(mx - start_pos[0]), abs(my - start_pos[1]))

                    x = min(start_pos[0], mx)
                    y = min(start_pos[1], my)

                    pygame.draw.rect(screen, current_color, 
                                     (sidebar_width + min(start_pos[0], mx), min(start_pos[1], my), 
                                      side, side), scale)
        
        #RENDERING RIGHT TRIANGLE
        elif painting_mode == "Right triangle":

                side = max(abs(mx - start_pos[0]), abs(my - start_pos[1]))

                top = (start_pos[0] + sidebar_width, start_pos[1])
                left = (start_pos[0] - side // 2 + sidebar_width, start_pos[1] + int(math.sqrt(3) / 2 * side))
                right = (start_pos[0] + side // 2 + sidebar_width, start_pos[1] + int(math.sqrt(3) / 2 * side))

                pygame.draw.polygon(screen, current_color, [top, left, right], scale)
        
        #RENDERING EQUILATERAL TRIANGLE
        elif painting_mode == "Equilateral triangle":

            side = max(abs(mx - start_pos[0]), abs(my - start_pos[1]))
            base_center_x = (start_pos[0] + mx) // 2

            # The points of the rectangle
            top = (base_center_x + sidebar_width, start_pos[1])
            bottom_left = (start_pos[0] + sidebar_width, my)
            bottom_right = (mx + sidebar_width, my)
            
            
            pygame.draw.polygon(screen, current_color, [top, bottom_left, bottom_right], scale)

        #RENDERING RHOMBUS
        elif painting_mode == "Rhombus":
                    
            # Center points
            center_x = (start_pos[0] + mx) // 2
            center_y = (start_pos[1] + my) // 2

            # Points of the Rhombus
            top = (center_x + sidebar_width, start_pos[1]) # Top point 
            bottom = (center_x + sidebar_width, my) # Bottom point 
            left = (start_pos[0] + sidebar_width, center_y) # Left point
            right = (mx + sidebar_width, center_y) # Right poin

            pygame.draw.polygon(screen, current_color, [top, left, bottom, right], scale)

"""THE BASE PROGRAMM"""   
while running:
    handle_events()
    update()
    render()
    pygame.display.flip()

pygame.quit()
