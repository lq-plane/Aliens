import os
import sys
import pygame
from pygame.sprite import Group
from pygame.locals import *
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():
    #游戏初始化
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))

    # 加载背景音乐
    music_base_path = os.getcwd() + "/music/"
    pygame.mixer.music.load(music_base_path + "music.mp3")
    # 设置音量
    pygame.mixer.music.set_volume(0.1)
    # 循环播放
    pygame.mixer.music.play(-1, 0)

    pygame.display.set_caption("Alien Invasion")
    #创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)
    #创建ship对象，将屏幕对象作为参数传入
    #创建一座飞船、一个子弹编组和一个外星人编组
    ship=Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets=Group()
    # 创建一个外星人编组对象
    aliens=Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #创建一个外星人
    alien=Alien(ai_settings,screen)
    # 创建play按钮
    play_button = Button(ai_settings, screen, "Play")

    #游戏主循环
    while True:
        #事件驱动：监视键盘和鼠标事件
        #循环检查所获得的所有事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        #更新屏幕
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

r=run_game()
print(r)

