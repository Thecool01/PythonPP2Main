import pygame

def run():
    pygame.init()

    width = 500
    height = 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Red Ball Game")
    
    x_cord, y_cord = width // 2, height // 2
    radius = 25
    speed = 20
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_cord - speed > 0 + radius: # The border for ball
                    x_cord -= speed
                elif event.key == pygame.K_RIGHT and x_cord + speed < height - radius:
                    x_cord += speed
                elif event.key == pygame.K_UP and y_cord - speed > 0 + radius:
                    y_cord -= speed
                elif event.key == pygame.K_DOWN and y_cord + speed < width - radius:
                    y_cord += speed
        
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (x_cord, y_cord), radius)  # Drawing circle
        pygame.display.flip()

    pygame.quit()

run()
