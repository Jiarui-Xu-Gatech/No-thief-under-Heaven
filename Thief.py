# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 10month 10day
"""
import pygame

class Thief():

    def __init__(self,ai_settings,screen):
        """初始化小偷并设置其初始位置"""
        self.screen=screen
        self.ai_settings=ai_settings
        self.small_scale=0.2
        self.image1 = pygame.image.load('Interface_pics\\Interface_pics\\thief1.png')
        #self.image1 = ai_settings.image_convert(self.image1)
        self.image1 = pygame.transform.scale(self.image1, (int(self.image1.get_width() * self.small_scale), int(self.image1.get_height() * self.small_scale))).convert_alpha()
        self.rect1 = self.image1.get_rect()
        self.image2 = pygame.image.load('Interface_pics\\Interface_pics\\thief2.png')
        #self.image2 = ai_settings.image_convert(self.image2)
        self.image2 = pygame.transform.scale(self.image2, (int(self.image2.get_width() * self.small_scale), int(self.image2.get_height() * self.small_scale))).convert_alpha()
        self.rect2 = self.image2.get_rect()
        self.image = pygame.image.load('Interface_pics\\Interface_pics\\thief1.png')
        #self.image = ai_settings.image_convert(self.image)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.small_scale), int(self.image.get_height() * self.small_scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx-75
        self.rect.bottom = self.screen_rect.bottom-5

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect1.centerx)

        # 移动标志
        self.moving = True

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值，而不是rect
        if self.image == self.image1:
            self.image = self.image2
        else:
            self.image = self.image1

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)