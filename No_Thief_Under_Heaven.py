import pygame
from midi_and_metronome import metronome
from midi_and_metronome import play_note
import time as ti
from pygame.sprite import Group
from screen import Settings
import game_function as gf
from Thief import Thief
from Police import Police
import pyaudio
from lino_settings import lino_settings


def run_game():

    # Initialize 
    pygame.init()
    ai_settings = Settings()
    p = pyaudio.PyAudio()
    lino = lino_settings()
    inputFile = input("Please input your file name:")
    # PATH_TO_MIDI = 'test_CSD/midi/en0{}a.mid'.format(inputFile)
    PATH_TO_MIDI = 'test_POP909/{}.mid'.format(inputFile)
    ai_settings.midi = PATH_TO_MIDI
    
    # Initialize the Game Interfave
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ai_settings.rect = screen.get_rect()
    pygame.display.set_caption('No Thief Under Heaven')
    ai_settings.background = pygame.transform.scale(ai_settings.background,(ai_settings.screen_width+1,ai_settings.screen_height)).convert()
    score_ratio=0.5
    lino_score_width, lino_score, lino_bar_rect =ai_settings.music_score()
    lino_score = pygame.transform.scale(
        lino_score, 
        (int(lino_score.get_width() * ai_settings.screen_height * score_ratio / lino_score.get_height()), int(ai_settings.screen_height) * score_ratio)).convert_alpha()
    
    # Open Game and Play a Standard Tone Followed by a Metro
    screen.blit(ai_settings.background, (0, 0))
    ti.sleep(1)
    end_time, bpm, firstPitch = ai_settings.process()
    play_note(firstPitch,1, octave = firstPitch//12)
    pygame.display.flip()
    ti.sleep(1)
    thief = Thief(ai_settings, screen)
    police=Police(ai_settings, screen, 1)
    step=0
    step_score=0.1034 * lino_score_width
    image_Win = pygame.image.load('you_win2.png')
    image_Win=pygame.transform.scale(
        image_Win,
        (int(image_Win.get_width()*73/670), 
        int(image_Win.get_height()*73/670))).convert_alpha()     
    win=False
    image_Lose=pygame.image.load('game_over.png')
    lose=False
    time=0
    step_time=0
    only_m=0

    midi_length = lino.get_midi_length(PATH_TO_MIDI)
    step_score_blank_left = 60/600 * lino_score.get_width()
    step_score_blank_right = 51/600 * lino_score.get_width()

    
    # Open Stream
    stream = p.open(format=lino.pyaudio_format,
                    channels=lino.n_channels,
                    rate=lino.samplerate,
                    input=True,
                    frames_per_buffer=lino.buffer_size)

    # Setup Pitch
    lino.pitch_o.set_unit("midi")
    lino.pitch_o.set_tolerance(lino.tolerance)
    gt_arr, tempo, total_step = lino.midi_arr(PATH_TO_MIDI)
    index = 0
    step_cur = 0
    pitch_list = []
    police_speed = 0
    thief_position = thief.rect.centerx
    
    # Update the Interface and Grade
    while True:
        if not only_m==0:
            gf.update_screen(ai_settings, screen, thief, police, step, step_score, win, image_Win, lose, image_Lose, police_speed, lino_score, lino_score_width, lino_bar_rect) 
        else:
            metronome(bpm, 4)
            only_m=1
            time_lino = ti.time()

        time_start=ti.time()
        time+=1
        gf.check_events(ai_settings, screen, thief, police)

        # Pitch Tracking
        audiobuffer = stream.read(lino.buffer_size)
        pitch = lino.get_pitch(audiobuffer)
        t_cur = ti.time() - time_lino
        gt_cur = lino.get_gt(t_cur, gt_arr[index,:])

        # Grading Strategy
        if lino.score_strategy(gt_cur, pitch, t_cur, gt_arr[0,0]) == True :
            score = 'null'
        else:
            pitch_list.append(pitch)
           
        if time%20==0:
            thief.update()
            police.update()
        
        time_end = ti.time()
        step_score = (lino_score.get_width() - step_score_blank_left - step_score_blank_right ) * ((time_end-time_lino)/midi_length) + step_score_blank_left
        
        # Switch to the next pitch and Update the Policeman Speed
        if t_cur > gt_arr[index, 1] and index != gt_arr.shape[0]-1:
            step_cur = lino.policeman_step(pitch_list, gt_arr[index, 3], step_cur)
            police.rect.centerx = lino.policeman_move(step_cur, total_step, thief_position)
            index += 1
            pitch_list=[]
            print("----------------------------------------To win, you need:", total_step - step_cur, " more steps!------------------------------------------")
            if total_step == step_cur:
                gf.update_screen(ai_settings, screen, thief, police, step, step_score, True, image_Win, lose, image_Lose, police_speed, lino_score, lino_score_width, lino_bar_rect) 
                print('----------------------------------------You Win!!!------------------------------------------')
                print('Total steps to win:{}, you spend:{} '.format(total_step, index))
                ti.sleep(5)
                break

        
        if index == gt_arr.shape[0]-1 and t_cur > gt_arr[index, 1]:
            step_cur = lino.policeman_step(pitch_list, gt_arr[index, 3], step_cur)
            police.rect.centerx = lino.policeman_move(step_cur, total_step, thief_position)
            if total_step == step_cur:
                gf.update_screen(ai_settings, screen, thief, police, step, step_score, True, image_Win, False, image_Lose, police_speed, lino_score, lino_score_width, lino_bar_rect) 
                print('----------------------------------------You Win!!!------------------------------------------')
                print('Total steps to win:{}, you spend:{} '.format(total_step, index))
                ti.sleep(5)
                break
            else:
                gf.update_screen(ai_settings, screen, thief, police, step, step_score, win, image_Win, True, image_Lose, police_speed, lino_score, lino_score_width, lino_bar_rect) 
                print('----------------------------------------You Lose!!!------------------------------------------')   
                ti.sleep(5)
                break
            

run_game()