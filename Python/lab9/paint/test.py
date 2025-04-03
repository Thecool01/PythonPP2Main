import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

def draw_rhombus(surface, center, width, height, color):
    x, y = center
    p1 = (x, y - height // 2)
    p2 = (x - width // 2, y) 
    p3 = (x, y + height // 2)
    p4 = (x + width // 2, y) 

    pygame.draw.polygon(surface, color, [p1, p2, p3, p4])

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_rhombus(screen, (300, 200), 150, 100, GREEN)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
