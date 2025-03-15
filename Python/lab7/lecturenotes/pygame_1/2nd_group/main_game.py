import pygame
import sys
from button import Button
from image import Pic

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 51)
green = (0, 255, 0)
red = (255, 0, 0)

def run():

    pygame.init()

    screen_width = 500
    screen_height = 500

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Test gaming")

    pygame.mixer.music.load('mecano.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    music_paused = True
    running = True
    button = Button(x = screen_width // 2 - 75, y = 20, width = 150, heigth = 50, text = 'PAUSE')
    pic = Pic(screen)

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    
    while running:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                sys.exit()
                
            if button.is_clicked(event):
                if music_paused:
                    pygame.mixer.music.unpause()
                    button.text = 'PAUSE'
                else:
                    pygame.mixer.music.pause()
                    button.text = 'UNPAUSE'
                music_paused = not music_paused
            
            if event.type == pygame.KEYUP:
                print(f'Pressed the keyword: {pygame.key.name(event.key)}')
                if event.key == pygame.K_UP:
                    pygame.mixer.music.unpause()
                    button.text = 'PAUSE'
                if event.key == pygame.K_DOWN:
                    pygame.mixer.music.pause()
                    button.text = 'UNPAUSE'


        screen.fill(yellow)
        
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        font = pygame.font.Font(None, 36)
        time_next = font.render(f"Time: {elapsed_time} sec", True, red)
        screen.blit(time_next, (10, 10))
        
        
        
        pic.output()
        button.draw(screen)
        #pygame.draw.rect(screen, green, (5,5, 150, 150))

        #pygame.mixer.music.unpause()
        #pygame.mixer.music.pause()
        #pygame.mixer.music.stop()
        pygame.display.flip()

run()
                