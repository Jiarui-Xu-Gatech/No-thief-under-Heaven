import sys
from time import sleep

import pygame


step=0

def check_keydown_events(event,ai_settings,screen,thief,police):
    if event.key == pygame.K_RIGHT:
        police.speed=3
        police.rect.centerx=police.rect.centerx+1
    elif event.key==pygame.K_q:
        sys.exit()

def check_keyup_events(event,police):
    if event.key == pygame.K_RIGHT:
        police.speed = 1

def check_events(ai_settings,screen,thief,police):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,thief,police)

        elif event.type==pygame.KEYUP:
            check_keyup_events(event,police)

def update_screen(ai_settings,screen,thief,police,step,step_score, win, image_Win,lose, image_Lose,police_speed, score, score_width, bar_rect ):
    if step<=ai_settings.rect.width:
        screen.blit(ai_settings.background, (0-step,0))
        screen.blit(ai_settings.background, (ai_settings.rect.width - step, 0))
    else:
        step=step%ai_settings.rect.width
        screen.blit(ai_settings.background, (0 - step, 0))
        screen.blit(ai_settings.background, (ai_settings.rect.width - step, 0))
    if step_score<=score.get_width():
        screen.blit(score, (-step_score,0))
    
    thief.blitme()
    police.blitme(police_speed)
    pygame.draw.rect(screen, ai_settings.bar_color, bar_rect)
    if win:
        
        screen.blit(image_Win, (ai_settings.rect.width * 0.5-200, ai_settings.rect.height * 0.5-200))           
        
    elif lose:
        screen.blit(image_Lose, (ai_settings.rect.width * 0.5 - 200, ai_settings.rect.height * 0.5 - 200))
    pygame.display.flip()