# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 10month 10day
"""
import pygame

from midi_and_metronome import metronome
from midi_and_metronome import play_note

from score_function import generate_score

from midi_note import midi_note

from recording import recordingTool

import time as ti

import sys

from pygame.sprite import Group

from screen import Settings

import game_function as gf

from Thief import Thief

from Police import Police

from condition import policeman_step

from lino_settings import midi_arr


#import game_functions as gf

def run_game():


    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ai_settings.rect = screen.get_rect()
    pygame.display.set_caption('No Thief Under Heaven')
    ai_settings.background = pygame.transform.scale(ai_settings.background,(ai_settings.screen_width+1,ai_settings.screen_height)).convert()
    score_ratio=0.5
    ai_settings.score = pygame.transform.scale(ai_settings.score,(int(ai_settings.score.get_width()*ai_settings.screen_height * score_ratio/ai_settings.score.get_height()), int(ai_settings.screen_height * score_ratio))).convert_alpha()
    screen.blit(ai_settings.background, (0, 0))
    ti.sleep(1)
    play_note(ai_settings.firstPitch,1, octave = ai_settings.firstPitch//12)
    pygame.display.flip()
    ti.sleep(1)



    thief = Thief(ai_settings, screen)
    police=Police(ai_settings, screen, 1)
    step=0
    step_score=0.1034*ai_settings.score_width
    image_Win = pygame.image.load('you_win2.png')
    image_Win=pygame.transform.scale(image_Win,(int(image_Win.get_width()*73/670), int(image_Win.get_height()*73/670))).convert_alpha()
    win=False
    image_Lose=pygame.image.load('game_over.png')
    lose=False
    time=0
    tempo_para=1000
    timelimited=ai_settings.score.get_width()*tempo_para/ai_settings.tempo-500
    block_time=0
    step_time=0
    only_m=0

    #####
    gt_arr, tempo, total_step = midi_arr(ai_settings.midi)
    step_cur=0
    time_limit=1

    #####


    while True:
        time_start=ti.time()
        time+=1
        if time>=timelimited:
            lose=True
        if thief.rect.centerx-police.rect.centerx<=10 and not lose:
            win=True

        gf.check_events(ai_settings, screen, thief, police)
        police_speed=0
        if time%100==0:
            thief.update()
            police.update()
        if time%200==0:
            #######
            note_list = []
            while True:
                if block_time <= time_limit:
                    note_list.append(recordingTool())
                else:
                    time_limit += 1
                    break
            step_cur = policeman_step(note_list, midi_note(ai_settings.notesClass, block_time), step_cur)
            ########
            police_speed=step_cur/total_step#0.5*generate_score(midi_note(ai_settings.notesClass,block_time),recordingTool())
            print(midi_note(ai_settings.notesClass,block_time))
            print(recordingTool())
        if not only_m==0:
            gf.update_screen(ai_settings, screen, thief, police, step, step_score, win, image_Win, lose, image_Lose,police_speed)
        else:
            metronome(ai_settings.bpm, 4)
            only_m=1
        step += ai_settings.thief_speed_factor
        time_end = ti.time()
        step_score += 2.65*step_time/ai_settings.end_time*(1-0.1144)*ai_settings.score_width
        block_time+=time_end-time_start
        step_time=time_end-time_start

run_game()