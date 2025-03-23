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

# Font
font = pygame.font.SysFont("Leelawadee", 20)

# Tool buttons
buttons = {
    "line": pygame.Rect(10, 20, 130, 40),
    "rectangle": pygame.Rect(10, 70, 130, 40),
    "circle": pygame.Rect(10, 120, 130, 40),
    "eraser": pygame.Rect(10, 170, 130, 40),
    "+": pygame.Rect(50, 280, 30, 30),
    "-": pygame.Rect(10, 280, 30, 30),
    "clear": pygame.Rect(10, 330, 130, 40),
}

# Color selection buttons
color_buttons = {
    black: pygame.Rect(10, 390, 30, 30),
    blue: pygame.Rect(50, 390, 30, 30),
    red: pygame.Rect(10, 440, 30, 30),
    yellow: pygame.Rect(50, 440, 30, 30),
}

screen.fill(black)
canva.fill(white)

def draw_buttons():
    
    for mode, rect in buttons.items():
        color = light_grey if painting_mode == mode else grey
        pygame.draw.rect(screen, color, rect)
        text = font.render(mode.capitalize(), True, white)
        screen.blit(text, (rect.x + 10, rect.y + 10))

    # Display current brush size
    scale_text = font.render(f"Size: {scale}", True, white)
    screen.blit(scale_text, (10, 250))

    # Draw color selection buttons
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, white, rect, 3)  # Highlight active color

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
                    elif mode == "clear":
                        canva.fill(white)
                    else:
                        painting_mode = mode
            
            # Check if a color button was clicked
            for color, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    current_color = color

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = False
            last_mouse_pos = None

def update():

    global last_mouse_pos

    mx, my = pygame.mouse.get_pos()
    mx -= sidebar_width  # Adjust mouse position for the canvas

    if mouse_click and last_mouse_pos is not None and mx >= 0:
        if painting_mode == 'line':
            pygame.draw.line(canva, current_color, last_mouse_pos, (mx, my), scale)
        elif painting_mode == 'rectangle':
            pygame.draw.rect(canva, current_color, (mx - 25, my - 25, scale + 30, scale + 30))
        elif painting_mode == 'circle':
            pygame.draw.circle(canva, current_color, (mx, my), scale)
        elif painting_mode == 'eraser':
            pygame.draw.line(canva, white, last_mouse_pos, (mx, my), scale)

    if mouse_click and mx >= 0:
        last_mouse_pos = (mx, my)

def render():

    screen.fill(black)  # Clear the screen
    pygame.draw.rect(screen, grey, (0, 0, sidebar_width, height))  # Draw sidebar
    screen.blit(canva, (sidebar_width, 0))  # Display the canvas
    draw_buttons()  # Draw buttons

while running:
    handle_events()
    update()
    render()
    pygame.display.flip()

pygame.quit()
