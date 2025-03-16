import pygame
import math
from datetime import datetime

pygame.init()

# Window setup
WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load and scale the second-hand image
second_hand_img = pygame.image.load("second_hand.png")  # Ensure it's a vertical PNG
hand_length = 120  # Length from center to tip
second_hand_img = pygame.transform.scale(second_hand_img, (10, hand_length))

def rotate_hand(image, angle, center, length):
    """Rotate the image around the pivot at the bottom and reposition it."""
    rotated_image = pygame.transform.rotate(image, -angle)  # Rotate counterclockwise

    # Compute new position (trigonometry: place pivot at the center)
    offset_x = math.sin(math.radians(angle)) * length
    offset_y = math.cos(math.radians(angle)) * length

    rotated_rect = rotated_image.get_rect(center=(center[0] + offset_x, center[1] - offset_y))
    
    return rotated_image, rotated_rect

running = True
while running:
    screen.fill((255, 255, 255))  # White background

    # Get current second
    now = datetime.now()
    second = now.second
    angle = second * 6  # 360 degrees / 60 seconds = 6 degrees per second

    # Rotate and reposition the second-hand image
    rotated_image, rotated_rect = rotate_hand(second_hand_img, angle, CENTER, hand_length)

    # Draw the clock center point
    pygame.draw.circle(screen, (0, 0, 0), CENTER, 5)  # Small dot at center

    # Blit the rotated second-hand
    screen.blit(rotated_image, rotated_rect)

    pygame.display.flip()
    clock.tick(1)  # Update every second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
