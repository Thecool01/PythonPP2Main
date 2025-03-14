import pygame
import sys
from Python.lecture9.music.button import Button
from image_game import Pic

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
    pygame.display.set_caption("Test game")

    pygame.mixer.music.load(r"C:\PP2Main\Python\lecture9\Megalo Strike Back.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    running = True
    music_paused = True
    button = Button(x = screen_width // 2 - 75, y = 20, width=150, height=50, text='PAUSE')


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
        screen.fill(yellow)
        button.draw(screen)
        Pic.output()
        #pygame.mixer.music.unpause()
        #pygame.mixer.music.pause()
        #pygame.mixer.music.stop()
        pygame.display.flip()
run()