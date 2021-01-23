import os
import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event,stats,aliens,ai_settings, screen, ship,bullets):
    # event.key被按下的键、pygame.K_RIGHT方向键右
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(stats, aliens, bullets, ai_settings, screen, ship)
    elif event.key==pygame.K_q:
        sys.exit()


def start_game(stats, aliens, bullets, ai_settings, screen, ship):
    #重置游戏设置
    ai_settings.initialize_dynamic_settings()
    #隐藏光标
    pygame.mouse.set_visible(False)
    #重置游戏统计信息
    stats.reset_stats()
    stats.game_active=True

    # # 重置记分牌图像
    # sb.prep_score()
    # sb.prep_high_score()
    # sb.prep_level()
    # sb.prep_ships()

    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    #创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
        # 如果没有达到限制，就发射一颗子弹
        # 创建一颗子弹，并将其加入到编组bullets中
        if len(bullets)<ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)




def check_keyup_events(event, ship):
    # event.key被抬起的键、pygame.K_RIGHT方向键右
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen,stats,sb,play_button, ship,aliens,bullets):#检查事件
    # 循环检查所获得的所有事件
    for event in pygame.event.get():
        # 如果事件的类型是退出
        if event.type == pygame.QUIT:
            # 中断进程
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,stats,aliens,ai_settings, screen, ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    #玩家单击play按钮开始新游戏
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
    # if play_button.rect.collidepoint(mouse_x,mouse_y):
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active=True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #绘制飞船
    ship.blitme()
    aliens.draw(screen)
    # alien.blitme()


    ##显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
        # introduce_button.drawintroduce_button()
    #让最近的绘制的屏幕可见
    #刷新屏幕
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #更新子弹的位置，并删除以消失得的子弹
    bullets.update()
    # 删除以消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


_sound_library = {}
# 播放音效(与背景音乐可同时播放，但默认只支持wav格式)
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        temp = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(temp)
        sound.set_volume(0.1)
        _sound_library[path] = sound
    sound.play()

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #检查是否有子弹击中了外星人
    #如果这样，就删除相应的子弹和外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
            #添加子弹音效
            # pygame.mixer.init()
            # pygame.mixer.music.load("music\传奇音效素材-选择框中闪光(SelectBoxFlash)_爱给网_aigei_com.mp3")
            # pygame.mixer.music.play()
            music_base_path = os.getcwd() + "/music/"
            play_sound(music_base_path + "hit.wav")
        check_high_score(stats, sb)

    if len(aliens)==0:
        #如果整群外星人都被消灭，就提高一个等级
        #删除所有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
    #计算每行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    #计算屏幕可容纳多少行外星人
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    #创建一个外星人并将其放在当前行,生成一个alien对象
    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    #调整外星人坐标
    alien.rect.x = alien.x
    #没往下一行，下一两倍的外星人高度
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    #将alien加入到编组
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    #创建外星人群
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)



def check_fleet_edges(ai_settings,aliens):
    #对每一个外星人逐一检查是否撞到墙
    for alien in aliens.sprites():
        if alien.check_edges():#如果外星人碰到了边缘
            change_fleet_direction(ai_settings, aliens)#改变移动方向
            break

#改变舰队方向
def change_fleet_direction(ai_settings, aliens):
    # 将整群外星人下移，并改变它们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed#x向下滑动
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):

    # 响应被外星人撞到的飞船
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen,stats, sb, ship, aliens, bullets):
    # 检查是否有外星人到达了屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
             # 像飞船被撞到一样进行处理
            ship_hit(ai_settings,  screen, stats,sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #检查是否有外星人到达屏幕边缘，然后更新所有外星人位置

    check_fleet_edges(ai_settings,aliens)
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
        # print("Ship hit!!!!!!!")
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen,stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    # 检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()




