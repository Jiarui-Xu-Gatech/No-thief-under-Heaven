import pygame
from CreateMIDIScore import create_score
from PIL import Image
import pretty_midi
from midi_and_metronome import metronome
pygame.init()

class Settings():
    def __init__(self):
        self.midi=''
        self.screen_width = 1306
        self.screen_height = 483
        self.bg_color = (230, 230, 230)
        self.background = pygame.image.load('Interface_pics/Interface_pics/BG2.png')
        self.tempo=60
        self.back_rect = self.background.get_rect()
        self.thief_speed_factor = 1.5
        self.bar_color=250,0,0
        self.bar_width=5
        self.bar_height=150

    def image_convert(self,image):
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                if image.get_at((x, y)) == (0, 0, 0, 0):
                    image.set_at((x, y), (255, 255, 255, 255))
        return image
    
    def music_score(self):
        create_score(self.midi)
        fig_name = self.midi[:-3] + 'png'
        im = Image.open(fig_name)
        score_width =im.size[0]
        img_size = im.size
        region = im.crop((20, img_size[1]//2-40,img_size[0]-20 , img_size[1]//2+40))
        region.save(fig_name)
        score=pygame.image.load(fig_name)
        bar_rect  = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        return score_width, score, bar_rect

    def process(self):
            midi_data = pretty_midi.PrettyMIDI(self.midi)
            end_time=midi_data.get_end_time()
            bpm=midi_data.get_tempo_changes()[1][0]
            firstPitch=midi_data.instruments[0].notes[0].pitch
            return end_time, bpm, firstPitch