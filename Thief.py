import pygame

class Thief():

    def __init__(self,ai_settings,screen):
        self.screen=screen
        self.ai_settings=ai_settings
        self.small_scale=0.2
        self.image1 = pygame.image.load('Interface_pics/Interface_pics/thief1.png')
        self.image1 = pygame.transform.scale(self.image1, (int(self.image1.get_width() * self.small_scale), int(self.image1.get_height() * self.small_scale))).convert_alpha()
        self.rect1 = self.image1.get_rect()
        self.image2 = pygame.image.load('Interface_pics/Interface_pics/thief2.png')
        self.image2 = pygame.transform.scale(self.image2, (int(self.image2.get_width() * self.small_scale), int(self.image2.get_height() * self.small_scale))).convert_alpha()
        self.rect2 = self.image2.get_rect()
        self.image = pygame.image.load('Interface_pics/Interface_pics/thief1.png')
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.small_scale), int(self.image.get_height() * self.small_scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx-75
        self.rect.bottom = self.screen_rect.bottom-5

        self.center = float(self.rect1.centerx)

        self.moving = True

    def update(self):
        if self.image == self.image1:
            self.image = self.image2
        else:
            self.image = self.image1

    def blitme(self):
        self.screen.blit(self.image, self.rect)