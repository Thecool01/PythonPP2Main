import pygame
import os
import time

pygame.init()
pygame.mixer.init()

music_folder = r"C:\PP2Main\Python\lab7\music"
music_mp3 = [os.path.join(music_folder, track) for track in os.listdir(music_folder) if track.endswith(".mp3")]


screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("MP3 Player")
font = pygame.font.Font(None, 25)

current_track = 0
message = ""


def play_music():
    global message
    pygame.mixer.music.load(music_mp3[current_track])
    pygame.mixer.music.play()
    message = f"Now playing: {os.path.basename(music_mp3[current_track])}"
    print(message)
    updating_screen()

def stop_music():
    global message
    pygame.mixer.music.pause()
    message = "Music stopped"
    print(message)
    updating_screen()

def pause_music():
    # Pause or resume
    global message
    if pygame.mixer.music.get_busy(): 
        pygame.mixer.music.pause()
        message = "Paused"
    else:  
        pygame.mixer.music.unpause()
        message = "Resumed"
    print(message)
    updating_screen()

def next_music():
    global current_track, message
    current_track = (current_track + 1) % len(music_mp3)
    message = "Skipping..."
    print(f"➡ Next treck: {os.path.basename(music_mp3[current_track])}")
    updating_screen()
    pygame.time.delay(500)
    play_music()

def previous_music():
    global current_track, message
    current_track = (current_track - 1) % len(music_mp3)
    message = "Skipping..."
    print(f"➡ Previous treck: {os.path.basename(music_mp3[current_track])}")
    updating_screen()
    pygame.time.delay(500)
    play_music()

def updating_screen():
    screen.fill((134, 10, 148))

    global message
    
    # Title
    controls = font.render(f"Controls: Play - P, Pause - X, Stop - S, Next - E, Previous - Q", True, (255, 255, 0))
    music_text = font.render(f"Music: {os.path.basename(music_mp3[current_track])}", True, (255, 255, 255))
    screen.blit(music_text, (10, 50))
    screen.blit(controls, (10, 20))

    # Time of the music
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() // 1000
        time_text = font.render(f"Time: {current_time // 60}:{current_time % 60:02d}", True, (0, 0, 0), (255, 255, 255))
        screen.blit(time_text, (10, 70))
    
    # Text when skiping
    if message:
        message_text = font.render(message, True, (255, 255, 0))
        screen.blit(message_text, (10, 100))
        message = ""
    pygame.display.flip()



def run():
    running = True
    print("Controls: Play - P, Stop - S, Next - E, Previous - Q")

    while running:
        updating_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play_music()
                elif event.key == pygame.K_s:
                    stop_music()
                elif event.key == pygame.K_x:
                    pause_music()
                elif event.key == pygame.K_e:
                    next_music()
                elif event.key == pygame.K_q:
                    previous_music()

run()
pygame.quit()