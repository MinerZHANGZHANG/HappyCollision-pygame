'''
程序主函数，汇总其它模块输出游戏窗口
'''

import pygame
import os.path
import setting as set
import live
import game_event
import gameui as gi
import startupui as si

#程序主函数
def run_game():
    #初始化pygame库
    pygame.init()
    #创建时钟对象(控制帧率)
    clock=pygame.time.Clock()
    #实例化设置类,用于导入游戏设置
    setting=set.Setting()
    #设置游戏窗口
    screen=pygame.display.set_mode((setting.screen_width,setting.screen_height))
    pygame.display.set_caption(setting.screen_caption)

    #设置不同的组，用于分别处理各种物品间的关系
    #玩家组
    group_player=pygame.sprite.Group()
    #玩家的攻击组
    group_attack=pygame.sprite.Group()
    #敌人组
    group_enemy=pygame.sprite.Group()
    #敌人的攻击组
    group_enemy_attack=pygame.sprite.Group()

    #实例化ui对象
    #showinfo用于在游戏内显示人物血条等信息
    showinfo=gi.Info(setting,screen)
    #人物选择按钮
    yi_button=si.MonkeyKingButton(screen,setting)
    monkey_button=si.YiButton(screen,setting)
    fox_button=si.FoxButton(screen,setting)
    bin_button=si.BinButton(screen,setting)
    #游戏开始界面的按钮
    pve_button=si.PVEButton(screen,setting)
    pvp_button=si.PVPButton(screen,setting)
    endless_button=si.EndlessButton(screen,setting)
    control_button=si.ControlButton(screen,setting)
    memory_button=si.RecordButton(screen,setting)
    cooling_button=si.CoolingButton(screen,setting)
    #游戏背景
    select_button=si.SelectButton(screen,setting)
    win_button=si.WinButton(screen,setting)
    dead_button=si.DeadButton(screen,setting)
    #玩家当前选择的人物标记
    player_button_1=si.PlayerButton1(screen,setting)
    player_button_2=si.PlayerButton2(screen,setting)
    #空白按钮
    none_button=si.NoneButton(screen,setting)
    #空白图像
    none_info=gi.ExInfo(screen,none_button,setting.introduce_none)
    #介绍按钮作用的图像
    pve_info=gi.ExInfo(screen,pve_button,setting.introduce_pve)
    pvp_info=gi.ExInfo(screen,pvp_button,setting.introduce_pvp)
    endless_info=gi.ExInfo(screen,endless_button,setting.introduce_endless)
    control_info=gi.ExInfo(screen,control_button,setting.introduce_control)
    record_info=gi.ExInfo(screen,memory_button,setting.introduce_record)
    cooling_info=gi.ExInfo(screen,cooling_button,setting.introduce_cooling)
    #按钮组(绘制时，在前的按钮会被在后的按钮覆盖)
    buttons=[select_button,yi_button,monkey_button,fox_button,bin_button,
             pve_button,pvp_button,endless_button,
             cooling_button,control_button,memory_button,
             dead_button,win_button]
    #标签按钮组
    choose_buttons=[player_button_1,player_button_2]
    #介绍按钮作用的图像组
    button_info_dict={none_button:none_info,pve_button:pve_info,pvp_button:pvp_info,
                      endless_button:endless_info,control_button:control_info,
                      memory_button:record_info,cooling_button:cooling_info}
    #当前显示的图像列表
    info_label=[]
    #存储模拟刚体运动的列表
    rigidbody_list=[]
    #玩家实例,初始化为战士
    player_1=live.MonkeyKing(setting,screen)
    player_2=live.MonkeyKing(setting,screen)

    if not os.path.exists(setting.record_path):
        #如果游戏记录文件不存在就新创建一个
        with open(setting.record_path,'w',newline="") as f:
            writer=csv.writer(f)
            header=["Time","Mode","Winner","1st Score","2st Score","Duration(s)","1st Player","2nd Player","isCooling"]
            writer.writerow(header)  

    #游戏主循环
    while True: 
        #绘制背景
        screen.blit(setting.screen_surface_background,(0,0))
        #设置游戏帧率
        clock.tick(setting.fps)
        #检测键盘鼠标事件   
        game_event.check_event(setting,screen,group_player,group_attack,group_enemy,
                               group_enemy_attack,buttons,showinfo,button_info_dict,info_label)
        #更新当前选择人物的标签
        game_event.update_choose(setting,buttons,choose_buttons)
        #游戏运行，非玩家对抗模式
        if (setting.game_active and (setting.game_mode==0 or setting.game_mode==2)):
            #人物初始化
            if(not setting.isinit):
                if setting.player_1!=None:
                    player_1=setting.player_1
                    group_player.add(player_1)
                if setting.player_2!=None:
                    player_2=setting.player_2
                    group_player.add(player_2)                
                setting.isinit=True
            #游戏计时器
            setting.timer+=1
            #更新玩家
            group_player.update()
            #生成敌人
            game_event.generate_enemies(setting,group_enemy,screen) 
            #更新敌人，玩家的攻击，敌人的攻击，玩家状态等
            game_event.update_enemies(setting,showinfo,screen,group_player,group_enemy,group_attack,group_enemy_attack)
            game_event.update_attacks(setting,screen,group_attack,group_enemy,rigidbody_list)
            game_event.update_enemy_attacks(setting,screen,group_player,group_enemy_attack,rigidbody_list)
            game_event.update_state(setting,showinfo)
            game_event.update_rigidbody(setting,rigidbody_list)
            #胜利条件
            if setting.timer>=60*setting.fps and not group_enemy.spritedict and setting.game_mode==0:
                game_event.game_win(setting,showinfo,group_enemy,group_attack,group_enemy_attack)
            #失败条件
            if setting.isinit and (setting.health_1<=0 or setting.health_2<=0):
                game_event.game_dead(setting,showinfo,group_enemy,group_attack,group_enemy_attack)
        #玩家对抗模式
        elif setting.game_active and setting.game_mode==1:
            #人物初始化
            if(not setting.isinit):
                if setting.player_1!=None and setting.player_2!=None:
                    player_1=setting.player_1
                    group_player.add(player_1)
                    player_2=setting.player_2
                    group_player.add(player_2)                        
                    setting.isinit=True

            #游戏计时器
            setting.timer+=1
            #更新玩家
            player_1.update()
            player_2.update()
            #更新玩家的攻击,信息显示和物理模拟
            game_event.update_attacks_pvp(setting,screen,group_attack,rigidbody_list)
            game_event.update_state(setting,showinfo)
            game_event.update_rigidbody(setting,rigidbody_list)

            #玩家1胜利条件
            if setting.isinit and setting.health_2<=0:
                setting.score_1+=1
                game_event.game_win(setting,showinfo,group_enemy,group_attack,group_enemy_attack)
            #玩家2胜利条件
            if setting.isinit and setting.health_1<=0:
                setting.score_2+=1
                game_event.game_win(setting,showinfo,group_enemy,group_attack,group_enemy_attack)
        
        #根据上述更新的结果绘制整个游戏窗口
        game_event.update_screen(setting,screen,group_player,group_attack,group_enemy,group_enemy_attack,
                                 showinfo,buttons,info_label,choose_buttons)                 

#运行游戏
run_game()
            