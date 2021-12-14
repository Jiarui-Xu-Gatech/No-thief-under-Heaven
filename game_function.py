# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 10month 10day
"""
import sys

import pygame

from recording import recordingTool

step=0

def check_keydown_events(event,ai_settings,screen,thief,police):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        police.speed=3
        police.rect.centerx=police.rect.centerx+1
    elif event.key==pygame.K_q:
        sys.exit()

def check_keyup_events(event,police):
    if event.key == pygame.K_RIGHT:
        police.speed = 1

def check_events(ai_settings,screen,thief,police):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,thief,police)

        elif event.type==pygame.KEYUP:
            check_keyup_events(event,police)

def update_screen(ai_settings,screen,thief,police,step,step_score, win, image_Win,lose, image_Lose,police_speed):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    if step<=ai_settings.rect.width:
        screen.blit(ai_settings.background, (0-step,0))
        screen.blit(ai_settings.background, (ai_settings.rect.width - step, 0))
    else:
        step=step%ai_settings.rect.width
        screen.blit(ai_settings.background, (0 - step, 0))
        screen.blit(ai_settings.background, (ai_settings.rect.width - step, 0))
    if step_score<=ai_settings.score.get_width():
        screen.blit(ai_settings.score, (-step_score,-50))
    #在飞船和外星人后面重绘所有子弹
    thief.blitme()
    police.blitme(police_speed)
    #draw the bar
    pygame.draw.rect(screen, ai_settings.bar_color, ai_settings.bar_rect)
    if win:
        screen.blit(image_Win, (ai_settings.rect.width * 0.5-200, ai_settings.rect.height * 0.5-200))
    elif lose:
        screen.blit(image_Lose, (ai_settings.rect.width * 0.5 - 200, ai_settings.rect.height * 0.5 - 200))
    # 让最近绘制的屏幕可见
    pygame.display.flip()