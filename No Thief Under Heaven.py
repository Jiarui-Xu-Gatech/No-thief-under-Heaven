# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 10month 10day
"""
import pygame

from midi_and_metronome import metronome

import sys

from pygame.sprite import Group

from screen import Settings

import game_function as gf

from Thief import Thief

from Police import Police


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

    thief = Thief(ai_settings, screen)
    police=Police(ai_settings, screen, 1)
    step=0
    step_score=0
    image_Win = pygame.image.load('you_win2.png')
    image_Win=pygame.transform.scale(image_Win,(int(image_Win.get_width()*73/670), int(image_Win.get_height()*73/670))).convert_alpha()
    win=False
    image_Lose=pygame.image.load('game_over.png')
    lose=False
    time=0
    tempo_para=1200
    timelimited=ai_settings.score.get_width()*tempo_para/ai_settings.tempo-500
    while True:
        time+=1
        if time>=timelimited:
            lose=True
        if thief.rect.centerx-police.rect.centerx<=10 and not lose:
            win=True

        gf.check_events(ai_settings, screen, thief, police)

        if time%100==0:
            thief.update()
            police.update()

        gf.update_screen(ai_settings, screen, thief, police, step, step_score, win, image_Win, lose, image_Lose)
        step += ai_settings.thief_speed_factor
        step_score += ai_settings.tempo/tempo_para
run_game()