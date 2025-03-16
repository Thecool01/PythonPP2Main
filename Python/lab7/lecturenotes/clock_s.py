import pygame
import pygame.gfxdraw
from datetime import datetime
# Colors
DARK_GREY = (45, 45, 45)
WHITE = (255, 255, 255)
# Initialize Pygame
pygame.init()
SIZE = 400
CENTER = (SIZE // 2, SIZE // 2)
window = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()

# Function to draw the second hand
def draw_second_hand(surface, second):
    hand_length = SIZE * 0.4
    angle = -second * 6  # Rotate counterclockwise (each second moves by 6 degrees)
    end_x = CENTER[0] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).x
    end_y = CENTER[1] + hand_length * pygame.math.Vector2(0, -1).rotate(angle).y
    pygame.draw.line(surface, DARK_GREY, CENTER, (end_x, end_y), 5)

def main():
    running = True
    while running:
        window.fill(WHITE)
        now = datetime.now()
        draw_second_hand(window, now.second)  # Update based on seconds
        pygame.display.flip()
        clock.tick(1)  # Update every second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
if __name__ == "__main__":
    main()
