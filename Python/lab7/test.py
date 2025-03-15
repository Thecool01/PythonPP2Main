import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Клик по кнопке")

# Создаем кнопку (прямоугольник)
button_rect = pygame.Rect(200, 200, 100, 50)  # (x, y, ширина, высота)

running = True
while running:
    screen.fill((255, 255, 255))  # Очистка экрана

    pygame.draw.rect(screen, (0, 128, 255), button_rect)  # Рисуем кнопку

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие мыши
            if button_rect.collidepoint(event.pos):  # Проверяем клик в кнопку
                print("Кнопка нажата!")

    pygame.display.flip()

pygame.quit()
