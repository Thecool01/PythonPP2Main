import pygame

pygame.init()

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
light_grey = (150, 150, 150)

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
# Tool buttons
buttons = {
    "Line":                     pygame.Rect(10, 20, 130, 20),
    "Rectangle":                pygame.Rect(10, 45, 130, 20),
    "Circle":                   pygame.Rect(10, 70, 130, 20),
    "Square":                   pygame.Rect(10, 95, 130, 20),
    "Right triangle":           pygame.Rect(10, 95, 130, 20),
    "Equilateral triangle":     pygame.Rect(10, 95, 130, 20),
    "Eraser":                   pygame.Rect(10, 95, 130, 20),
    "+":                        pygame.Rect(50, 115, 30, 20),
    "-":                        pygame.Rect(10, 115, 30, 20),
    "Clear":                    pygame.Rect(10, 165, 130, 20),
}

button_states = {mode: False for mode in buttons} # The status of button(click or not)
# Color selection buttons
color_buttons = {
    black: pygame.Rect(10, 390, 30, 30),
    blue: pygame.Rect(50, 390, 30, 30),
    red: pygame.Rect(10, 440, 30, 30),
    yellow: pygame.Rect(50, 440, 30, 30),
}

screen.fill(black)
canva.fill(white)

# All left buttons
def draw_buttons():
    
    for mode, rect in buttons.items():
        color = (233, 233, 233) if button_states[mode] else (light_grey if painting_mode == mode else grey)
        # color = light_grey if painting_mode == mode else grey
        pygame.draw.rect(screen, color, rect)
        text = font_small.render(mode.capitalize(), True, white)
        screen.blit(text, (rect.x + 20, rect.y))

    # Display current brush size
    scale_text = font.render(f"Size: {scale}", True, white)
    screen.blit(scale_text, (10, 250))

    # Draw color selection buttons
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, white, rect, 3)  # Highlight active color

# All events with keyboard, mouse, etc.
def handle_events():

    global running, mouse_click, last_mouse_pos, painting_mode, scale, current_color

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
                    
            # Check if a color button was clicked
            for color, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    current_color = color

            if mx >= sidebar_width:
                global start_pos
                start_pos = (mx - sidebar_width, my) # Handle the start position
            
        if event.type == pygame.MOUSEBUTTONUP:
            for mode, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    button_states[mode] = False  # Button is released
                
            mouse_click = False
            last_mouse_pos = None
            # Preview before drawing a shape (rectangle and circle)
            if start_pos is not None:
                mx, my = pygame.mouse.get_pos()
                mx -= sidebar_width

                width = abs(mx - start_pos[0])
                height = abs(my - start_pos[1])

                if painting_mode == "Rectangle":
                    pygame.draw.rect(canva, current_color, (min(start_pos[0], mx), min(start_pos[1], my), width, height), scale) # To draw a rectangle correctly in either direction.

                elif painting_mode == "Circle":
                    radius = max(width, height) // 2
                    center = (min(start_pos[0], mx) + width // 2, min(start_pos[1], my) + height // 2) # To draw a circle correctly in either direction.
                    pygame.draw.circle(canva, current_color, center, radius, scale)
                
            start_pos = None

# Process of painting
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

    # Drawing the circle and square
    if mouse_click and start_pos:
        mx, my = pygame.mouse.get_pos()
        mx -= sidebar_width

        width_l = abs(mx - start_pos[0]) # Local width for figures
        height_l = abs(my - start_pos[1]) # local height for figures

        if painting_mode == "rectangle":
            # Drawing the rectangle on the position where mouse were clicked
             pygame.draw.rect(screen, current_color, 
                             (sidebar_width + min(start_pos[0], mx), 
                              min(start_pos[1], my), width_l, height_l), scale)

        elif painting_mode == "circle":
            radius = max(width_l, height_l) // 2 # Radius is a half of diameter
            
            # Drawing the circle on the position where mouse were clicked
            center = (sidebar_width + min(start_pos[0], mx) + width_l // 2, 
                      min(start_pos[1], my) + height_l // 2)
            pygame.draw.circle(screen, current_color, center, radius, scale)
            
while running:
    handle_events()
    update()
    render()
    pygame.display.flip()

pygame.quit()
