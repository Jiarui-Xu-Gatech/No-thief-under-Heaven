# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 10month 10day
"""
# 屏幕创建和初始化参数
import pygame
from CreateMIDIScore import create_score
from PIL import Image
import pretty_midi
from midi_and_metronome import metronome
#from pygame.locals import *
pygame.init()

class Settings():
    def __init__(self):
        # 屏幕设置
        self.midi='en002a.mid'
        create_score(self.midi)
        midi_data = pretty_midi.PrettyMIDI(self.midi)
        self.end_time=midi_data.get_end_time()
        self.bpm=midi_data.get_tempo_changes()[1][0]
        self.notesClass=midi_data.instruments[0].notes
        self.firstPitch=midi_data.instruments[0].notes[0].pitch
        im = Image.open("midiscore.png")
        self.score_width =im.size[0]
        img_size = im.size
        region = im.crop((20, img_size[1]//2-40,img_size[0]-20 , img_size[1]//2+40))
        region.save("midiscore.png")
        self.screen_width = 1306
        self.screen_height = 483
        self.bg_color = (230, 230, 230)
        self.background = pygame.image.load('Interface_pics\\Interface_pics\\BG2.png')
        self.score=pygame.image.load('midiscore.png')
        self.tempo=60
        self.back_rect = self.background.get_rect()
        self.thief_speed_factor = 1.5
        self.bar_color=250,0,0
        self.bar_width=5
        self.bar_height=150
        self.bar_rect = pygame.Rect(0.12925*self.score_width, 0, self.bar_width, self.bar_height)

        #self.background = pygame.transform.scale(self.background,(int(self.back_rect.width * 1),int(self.back_rect.height * 1))).convert()

    def image_convert(self,image):
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                if image.get_at((x, y)) == (0, 0, 0, 0):
                    image.set_at((x, y), (255, 255, 255, 255))
        return image