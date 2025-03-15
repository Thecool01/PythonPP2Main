import pygame
import datetime
main_clock = r"C:\Users\n_ishutin\Desktop\pp2\PythonPP2Main\Python\lab7\mickeyclock.jpeg"
minute = r"C:\Users\n_ishutin\Desktop\pp2\PythonPP2Main\Python\lab7\minutepng.png"
second = r"C:\Users\n_ishutin\Desktop\pp2\PythonPP2Main\Python\lab7\secondpng.png"


def run():
    
    pygame.init()
    
    screen = pygame.display.set_mode((700, 525))
    pygame.display.set_caption("Mickey Clock")
    
    # Main clock
    clock = pygame.image.load(main_clock)
    clock = pygame.transform.scale(clock, (700, 525))
    
    
    # # Main clock
    # minute_hand = Image(screen, minute, scale=(400, 400))
    
    # # Main clock
    # second_hand = Image(screen, second, scale=(400, 400))
    
    clock_tick = pygame.time.Clock()

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Текущая секунда
        current_time = datetime.datetime.now()
        second_value = current_time.second
        
        angle = (60 - second_value) * 6 # 360° / 60 сек = 6° за сек
        
        screen.fill((255, 255, 255))
    
        # minute_hand.output()
        # second_hand.output()
        
        
        # Тест вращения clock
        rotated_clock = pygame.transform.rotate(clock, angle)
        new_rect = rotated_clock.get_rect(center=(350, 260))
        
        screen.blit(rotated_clock, new_rect.topleft)
        pygame.display.flip()
        clock_tick.tick(60)
    
    
    
    
run()