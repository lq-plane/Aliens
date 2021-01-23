import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        #初始化飞船，并设置其属性
        super(Ship, self).__init__()
        #是飞船对象拥有属性
        self.screen=screen
        #将游戏设置参数作为ship对象属性
        self.ai_settings=ai_settings
        #加载飞船图像
        self.image=pygame.image.load('images/ship.bmp')
        #飞船的外接矩形
        self.rect=self.image.get_rect()
        #屏幕screen的外接矩形
        self.screen_rect=screen.get_rect()

        #飞船初始位置，纵向底部对齐
        #飞船矩形中心点
        self.rect.centerx=self.screen_rect.centerx
        #飞船矩形纵部坐标
        self.rect.bottom=self.screen_rect.bottom
        #在飞船属性center中存储小数值
        self.center=float(self.rect.centerx)
        self.center1 = float(self.rect.centery)

        #移动标致
        self.moving_right=False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left>0:
            self.center-=self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.center1 -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center1 += self.ai_settings.ship_speed_factor

        self.rect.centerx=self.center#
        self.rect.centery = self.center1
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        #让飞船在屏幕上居中
        self.center=self.screen_rect.centerx