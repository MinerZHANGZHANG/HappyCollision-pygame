'''
game_event模块提供了一系列方法，主要是处理输入事件、更新敌我物体碰撞、生成物体等内容，并根据结果绘制到屏幕
'''

import pygame
import os
import csv
from datetime import datetime

import effect
import live
import startupui
import rigidbody
import enemy as ey

def check_event(setting,screen,player_group,attack_group,enemy_group,enemy_attack_group,buttons,showinfo,info_dict,info_label):
    """处理游戏事件"""

    #遍历事件队列处理事件
    for event in pygame.event.get():
        #print(event)
        #窗口关闭
        if event.type == pygame.QUIT:
            exit()
        #按键按下     
        elif event.type==pygame.KEYDOWN:
            check_event_key_down(event,setting,screen,player_group,attack_group,enemy_group,enemy_attack_group)
        #按键抬起 
        elif event.type==pygame.KEYUP:
            check_event_key_up(event,setting,screen,player_group)
        #鼠标按下
        elif event.type==pygame.MOUSEBUTTONDOWN:
            #获取鼠标位置          
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_mouse_button(setting,screen,buttons,showinfo,mouse_x,mouse_y,event)
        #鼠标移动  
        elif event.type==pygame.MOUSEMOTION:          
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_mouse_enter(setting,screen,buttons,info_dict,info_label,mouse_x,mouse_y,event)

def check_event_key_down(event,setting,screen,player_group,attack_group,enemy_group,enemy_attack_group):
    """处理键盘按键按下事件"""
    #与玩家移动、技能释放、返回初始界面有关

    #判断是否选择了人物作为玩家1
    if setting.player_1!=None:
        #wasd设置玩家1的移动标志为True
        if event.key== pygame.K_s:
            setting.player_1.move_down=True
        elif event.key== pygame.K_w:
            setting.player_1.move_up=True
        elif event.key== pygame.K_a:
            setting.player_1.move_left=True
        elif event.key== pygame.K_d:
            setting.player_1.move_right=True
        #c生成攻击1
        elif event.key==pygame.K_c:
            generate_attack_common(setting,screen,setting.player_1,attack_group)
        #k生成攻击2(需要玩家等级超过2级)
        elif event.key==pygame.K_v and setting.level_1>=2:
            generate_attack_skill(setting,screen,setting.player_1,attack_group)
        #b生成攻击3
        elif event.key==pygame.K_b and setting.level_1>=3:
            generate_attack_break(setting,screen,setting.player_1,attack_group)
    
    #同上
    if setting.player_2!=None:
        if event.key== pygame.K_k:
            setting.player_2.move_down=True
        elif event.key== pygame.K_i:
            setting.player_2.move_up=True
        elif event.key== pygame.K_j:
            setting.player_2.move_left=True
        elif event.key== pygame.K_l:
            setting.player_2.move_right=True
        elif event.key==pygame.K_p:
            generate_attack_common(setting,screen,setting.player_2,attack_group)
        #91对应键盘 [ 
        elif event.key==91 and setting.level_2>=2:
            generate_attack_skill(setting,screen,setting.player_2,attack_group)
        #93对应 ]
        elif event.key==93 and setting.level_2>=3:
            generate_attack_break(setting,screen,setting.player_2,attack_group)

    #esc退出游戏到初始界面
    if event.key==pygame.K_ESCAPE:
        setting.iswait=True
        game_over(setting,enemy_group,attack_group,enemy_attack_group)

def check_event_key_up(event,setting,screen,player):
    """处理键盘按键抬起事件"""
    #与玩家移动有关

    #wasd抬起设置移动标志为False
    if setting.player_1!=None:
        if event.key== pygame.K_s:
           setting.player_1.move_down=False
        elif event.key== pygame.K_w:
           setting.player_1.move_up=False
        elif event.key== pygame.K_a:
           setting.player_1.move_left=False
        elif event.key== pygame.K_d:
           setting.player_1.move_right=False

    if setting.player_2!=None:
        if event.key== pygame.K_k:
           setting.player_2.move_down=False
        elif event.key== pygame.K_i:
           setting.player_2.move_up=False
        elif event.key== pygame.K_j:
           setting.player_2.move_left=False
        elif event.key== pygame.K_l:
           setting.player_2.move_right=False

def check_mouse_button(setting,screen,buttons,showinfo,mouse_x,mouse_y,event):
    """处理鼠标按下事件"""

    #复制一个按钮组并反转，目的是使原队列中靠后的(绘制时覆盖在上方)按钮先被遍历到
    temp=buttons.copy()
    temp.reverse()
    #遍历按钮
    for button in temp:
        #通过碰撞检测法，判断遍历到的按钮是否被点击
        isclick=button.rect.collidepoint(mouse_x,mouse_y)      
        #按钮只在启动界面生效，game_active为False时
        if isclick and  not setting.game_active :  
            #当游戏结束后将标志位设为True，忘了为什么要放在这里，但既然没问题就这样吧
            if setting.isdead:
                iswait=True
            elif setting.iswin:
                iswait=True
            #当条件符合时，根据按钮类型进行处理
            elif setting.iswait:
                #设置游戏模式并启动的三类按钮
                if isinstance(button,startupui.PVEButton):
                    if setting.player_1==None and setting.player_2==None:
                        print("Please choose one or two hero")
                    else:
                        setting.game_mode=0
                        game_start(setting,showinfo,0) 
                    break
                elif isinstance(button,startupui.PVPButton):
                    if setting.player_1==None or setting.player_2==None:
                         print("Please choose two hero")
                    else:
                        setting.game_mode=1
                        game_start(setting,showinfo,1) 
                    break
                elif isinstance(button,startupui.EndlessButton):
                    if setting.player_1==None and setting.player_2==None:
                        print("Please choose one or two hero")
                    else:
                        setting.game_mode=2
                        game_start(setting,showinfo,2) 
                    break
                #设置游戏冷却的按钮
                elif isinstance(button,startupui.CoolingButton):
                    if setting.iscooling:
                        setting.iscooling=False
                    else:
                        setting.iscooling=True
                    break
                #打开游戏记录的按钮
                elif isinstance(button,startupui.RecordButton):
                    if os.path.exists(setting.record_path):
                        os.system("start {0}".format(setting.record_path))
                    else:
                        with open(setting.record_path,'w',newline="") as f:
                            writer=csv.writer(f)
                            header=["Time","Mode","Winner","1st Score","2st Score","Duration","1st Player","2nd Player","isCooling"]
                            writer.writerow(header)              
                        os.system("start {0}".format(setting.record_path))
                    break
                #打开游戏操作介绍的按钮
                elif isinstance(button,startupui.ControlButton):
                    if os.path.exists(setting.control_path):                     
                        os.system("start {0}".format(setting.control_path))
                    else:
                        print("no file be found..")
                    break
                #四个选择英雄的按钮
                elif isinstance(button,startupui.MonkeyKingButton):
                    choose_hero(setting,event,live.MonkeyKing(setting,screen))                   
                elif isinstance(button,startupui.YiButton):
                    choose_hero(setting,event,live.Yi(setting,screen))
                elif isinstance(button,startupui.FoxButton):
                    choose_hero(setting,event,live.Fox(setting,screen))                    
                elif isinstance(button,startupui.BinButton):
                    choose_hero(setting,event,live.Bin(setting,screen))

def choose_hero(setting,event,hero):
    """选择英雄，设置相关属性到setting中"""

    #event.button值为1对应鼠标左键，3对应鼠标右键
    if event.button==1:
        setting.player_1=hero
        setting.max_health_1=setting.player_1.max_health
        setting.health_1=setting.max_health_1
        print("you choose {0} as 1st player".format(type(setting.player_1).__name__))  
    elif event.button==3:
        setting.player_2=hero
        setting.max_health_2=setting.player_2.max_health
        setting.health_2=setting.max_health_2              
        print("you choose {0} as 2nd player".format(type(setting.player_2).__name__))

def check_mouse_enter(setting,screen,buttons,info_dict,info_label,mouse_x,mouse_y,event):
    """处理鼠标移动事件"""

    #当鼠标移动到按钮上时，产生动画效果并显示相应的介绍
    if (not setting.game_active):
        #遍历在字典中，有对应信息的按钮
        for button in info_dict:
            isenter=button.rect.collidepoint(mouse_x,mouse_y)
            if isenter:
                info_label.clear()
                info_label.append(info_dict[button])
                break
            else:
                info_label.clear()
                info_dict[button].recover()
                           
def game_start(setting,showinfo,game_mode):
    """启动游戏"""
    print("game start")
    #标记游戏状态
    setting.game_active=True
    setting.iswait=False
    setting.iswin=False
    setting.isdead=False
    #重置计时器
    setting.timer=0
    #清空玩家得分
    setting.score_1=0
    setting.score_2=0


    #普通模式或无尽模式
    if game_mode==0 or game_mode==2:       
        #重置玩家状态               
        if setting.player_1!=None:
            setting.health_1=setting.max_health_1
            setting.level_1=1
            setting.player_1.rect.centery=150
            setting.player_1.skill_timer=[0,0,0]
        if setting.player_2!=None:
            setting.health_2=setting.max_health_2
            setting.level_2=1
            setting.player_2.rect.centery=300
            setting.player_2.skill_timer=[0,0,0]
    
    #玩家对抗模式
    if game_mode==1:
        #重置玩家状态
        setting.health_1=setting.max_health_1*setting.pvp_health_rate
        setting.level_1=3
        setting.player_1.skill_timer=[0,0,0]
        setting.player_1.rect.center=(100,225)

        setting.health_2=setting.max_health_2*setting.pvp_health_rate
        setting.level_2=3
        setting.player_2.skill_timer=[0,0,0]      
        setting.player_2.rect.center=(700,225)
        #调整玩家2的朝向
        setting.player_2.forward=-1    

def game_over(setting,enemy_group,attack_group,enemy_attack_group):
    """终止游戏"""
    print("game over")
    #如果在游戏中，添加记录
    if setting.game_active:
        add_record(setting)
    #标记游戏状态
    setting.iswin=False
    setting.isdead=False
    setting.game_active=False
    setting.isinit=False
    #清空计数
    setting.player_1=None
    setting.player_2=None
    setting.score_1=0
    setting.score_2=0
    setting.enemy_number=0

def game_win(setting,showinfo,enemy_group,attack_group,enemy_attack_group):
    """游戏胜利"""
    #添加本次游戏记录到文件
    add_record(setting)
    #标记游戏状态
    setting.iswin=True
    setting.game_active=False
    setting.isinit=False
    
def game_dead(setting,showinfo,enemy_group,attack_group,enemy_attack_group):
    """游戏失败"""
    #怎么和上面那个方法一样啊
    #添加本次游戏记录到文件
    add_record(setting)
    #标记游戏状态
    setting.isdead=True
    setting.game_active=False
    setting.isinit=False

def add_record(setting):
    """添加游戏记录"""
    if os.path.exists(setting.record_path):
        #根据游戏状态添加记录
        try: 
            with open(setting.record_path,'a',newline="") as f:               
                #游戏的模式
                mode="PVE"
                if setting.game_mode==1:
                    mode="PVP"
                elif setting.game_mode==2:
                    mode="Endless"
                #游戏的胜利者
                winner="Peace"
                if setting.score_1>setting.score_2:
                    winner="1st Player"
                if setting.score_1<setting.score_2:
                    winner="2st Player"
                #游戏时长
                time=setting.timer/setting.fps
                #玩家选择的人物
                player_1="None"
                player_2="None"
                player_1="None" if setting.player_1==None else type(setting.player_1).__name__
                player_2="None" if setting.player_2==None else type(setting.player_2).__name__
                #是否启用冷却
                iscooling="No"
                if setting.iscooling:
                    iscooling="Yes"
                #将结果写入进csv文件
                writer=csv.writer(f)
                line=[datetime.now().strftime("%Y-%m-%d %H:%M:%S"),mode,winner,
                        setting.score_1,setting.score_2,time,player_1, player_2,iscooling]
                writer.writerow(line)
        except IOError:
            print("Add game record failed..")
    else:
        #如果文件不存在就新创建一个
        with open(setting.record_path,'w',newline="") as f:
            writer=csv.writer(f)
            header=["Time","Mode","Winner","1st Score","2st Score","Duration(s)","1st Player","2nd Player","isCooling"]
            writer.writerow(header)  

def generate_enemies(setting,enemy_group,screen):
    """按照时间生成敌人"""
    if(setting.game_mode==0):
        #根据游戏时间生成5波敌人
        if(setting.timer==(setting.fps*2)):
            print("First wave enemy: warrior*4 mage*2")
            for i in range(2):
                new_enemy=ey.Mage(setting,screen)
                enemy_group.add(new_enemy)
            for i in range(4):
                new_enemy=ey.Warrior(setting,screen)
                enemy_group.add(new_enemy)
        if(setting.timer==(setting.fps*14)):
            print("Second wave enemy: warrior*6 mage*4")
            for i in range(6):
                new_enemy=ey.Warrior(setting,screen)
                enemy_group.add(new_enemy)
            for i in range(4):
                new_enemy=ey.Mage(setting,screen)
                enemy_group.add(new_enemy)
        if(setting.timer==(setting.fps*28)):
            print("Third wave enemy: warrior*10 mage*6 artillery*4")
            for i in range(10):
                new_enemy=ey.Warrior(setting,screen)
                enemy_group.add(new_enemy)
            for i in range(6):
                new_enemy=ey.Mage(setting,screen)
                enemy_group.add(new_enemy)
            for i in range(4):
                new_enemy=ey.Artillery(setting,screen)
                enemy_group.add(new_enemy)
        if(setting.timer==(setting.fps*45)):
            print("4st wave enemy: warrior*20")
            for i in range(20):
                new_enemy=ey.Warrior(setting,screen)
                enemy_group.add(new_enemy)
        if(setting.timer==(setting.fps*55)):
            print("5st wave enemy:overlord*1 warrior*10 artillery*5 mage*5")
            new_enemy=ey.Overlord(setting,screen)
            enemy_group.add(new_enemy)
            for i in range(5):
                new_enemy_list=[ey.Warrior(setting,screen),ey.Warrior(setting,screen),
                           ey.Mage(setting,screen),ey.Artillery(setting,screen)]
                enemy_group.add(new_enemy_list)


    elif(setting.game_mode==2):
        #每隔5秒生成敌人，数量持续提升
        if(setting.timer%(5*setting.fps)==0) and setting.enemy_number<=setting.enemy_max:
            for i in range(0,(int(setting.timer/(5*setting.fps)))+1):
                new_enemy=ey.Warrior(setting,screen)
                enemy_group.add(new_enemy)
            for i in range(0,(int(setting.timer/(5*setting.fps)))+1):
                new_enemy=ey.Mage(setting,screen)
                enemy_group.add(new_enemy)            
            if setting.timer>=(20*setting.fps):
                for i in range(0,(int(setting.timer/(10*setting.fps)))+1):
                    new_enemy=ey.Artillery(setting,screen)
                    enemy_group.add(new_enemy)            
            if setting.timer>=(30*setting.fps):
                new_enemy=ey.Overlord(setting,screen)
                enemy_group.add(new_enemy)            
    
def generate_attack_common(setting,screen,player,attack_group):
    """生成玩家的普通攻击(技能1)"""
    new_attack=player.common_attack()
    if new_attack!=None:
        attack_group.add(new_attack)

def generate_attack_skill(setting,screen,player,attack_group):
    """生成玩家的技能攻击(技能2)"""
    new_attack=player.skill_attack()
    if new_attack!=None:
        attack_group.add(new_attack)

def generate_attack_break(setting,screen,player,attack_group):
    """生成玩家的大招攻击(技能3)"""
    new_attack=player.break_attack()
    if new_attack!=None:
        attack_group.add(new_attack)

def generate_enemy_attack(setting,screen,player_group,enemy,enemy_attack_group):
    """生成敌人的攻击"""
    #近战敌人的攻击，仅生成有限次
    if(enemy.ismelee):
        if(enemy.melee_count>0):
            new_attack=enemy.auto_attack()
            enemy_attack_group.add(new_attack)
            enemy.melee_count-=1
    #远程敌人的攻击
    else:
        new_attack=enemy.auto_attack()
        enemy_attack_group.add(new_attack)

def update_enemies(setting,showinfo,screen,player_group,enemy_group,attack_group,enemy_attack_group):
    """更新敌人"""
    enemy_group.update()
    #更新数量
    setting.enemy_number=len(enemy_group)
    #更新敌人的攻击，遍历敌人组，根据计时器生成攻击
    for enemy in enemy_group:
        if(enemy.attack_timer==0):
            generate_enemy_attack(setting,screen,player_group,enemy,enemy_attack_group)
            enemy.attack_timer=enemy.attack_interval
        else:
            enemy.attack_timer-=1

def update_attacks(setting,screen,attack_group,enemy_group,rigidbody_list):
    """更新玩家的攻击"""
    attack_group.update()
    #如果攻击超过屏幕一定距离，或被标记为结束，则销毁它
    for attack in attack_group.copy():
        if attack.rect.right>1000 or attack.isover or attack.rect.left<-200:
            attack_group.remove(attack)
            del attack
    #计算碰撞字典(键为发生碰撞的敌人物体,值为与它发生碰撞的物体列表)
    enemy_behit_dict=pygame.sprite.groupcollide(enemy_group,attack_group,False,False)
    #遍历字典的键(所有被碰撞的敌人)
    for enemy in enemy_behit_dict:
        #遍历字典键对应的列表(与该敌人碰撞的攻击)
        for attack in enemy_behit_dict[enemy]:    
            #根据攻击扣除血量
            enemy.health-=attack.damage
            #如果这个敌人未被该攻击碰撞过，生成一个冲击对象给它
            if not (enemy in attack.collide_list):
                rigidbody.Repel(setting,enemy,attack,rigidbody_list)
                attack.collide_list.append(enemy)
            #若血量不为正，给玩家加分，删除敌人
            if(enemy.health<=0):
                if setting.player_1!=None:
                    if attack.player==setting.player_1:
                        setting.score_1+=enemy.score  
                if setting.player_2!=None:
                    if attack.player==setting.player_2:
                        setting.score_2+=enemy.score  
                #如果这个攻击被标记为一次性的，销毁攻击物体               
                if(attack.isbreak):
                    attack_group.remove(attack)
                    del attack
                #移除敌人
                enemy_group.remove(enemy)
                enemy.isalive=False
                del enemy
                break
            else:
                #(为了避免销毁敌人和攻击的次序问题)
                #如果这个攻击被标记为一次性的，销毁攻击物体               
                if(attack.isbreak):
                    attack_group.remove(attack)
                    del attack

def update_attacks_pvp(setting,screen,attack_group,rigidbody_list):
    """更新玩家对抗时的攻击"""
    #更新攻击物体
    attack_group.update()
    #遍历攻击物体，超出屏幕一定距离则删除
    for attack in attack_group:
        if attack.rect.right>1000 or attack.isover or attack.rect.left<-200:
            attack_group.remove(attack)
            del attack

    #计算出攻击物体和玩家1的碰撞列表
    player_behit_list_1=pygame.sprite.spritecollide(setting.player_1,attack_group,False)
    for attack in player_behit_list_1:
        #如果发生碰撞的物体不由玩家1发出，则进行伤害、碰撞和消除攻击物体的步骤
        if attack.player != setting.player_1:
            setting.health_1-=attack.damage
            if not (setting.player_1 in attack.collide_list):
                rigidbody.Repel(setting,setting.player_1,attack,rigidbody_list)
                attack.collide_list.append(setting.player_1)
            if attack.isbreak:
                attack_group.remove(attack)
                del attack
    #同上，处理玩家2的碰撞
    player_behit_list_2=pygame.sprite.spritecollide(setting.player_2,attack_group,False)
    for attack in player_behit_list_2:
        if attack.player != setting.player_2:
            setting.health_2-=attack.damage
            if not (setting.player_2 in attack.collide_list):
                rigidbody.Repel(setting,setting.player_2,attack,rigidbody_list)
                attack.collide_list.append(setting.player_2)
            if attack.isbreak:
                attack_group.remove(attack)
                del attack    

def update_enemy_attacks(setting,screen,player_group,enemy_attack_group,rigidbody_list):
    """更新敌人的攻击"""
    #处理和玩家的碰撞
    player_behit_dict=pygame.sprite.groupcollide(player_group,enemy_attack_group,False,False)
    for player in player_behit_dict:
        for enemy_attack in player_behit_dict[player]:
            if(player==setting.player_1):
                setting.health_1-=enemy_attack.damage
                if(enemy_attack.isbreak):
                    enemy_attack_group.remove(enemy_attack)
                    del enemy_attack
            if(player==setting.player_2):
                setting.health_2-=enemy_attack.damage
                if(enemy_attack.isbreak):
                    enemy_attack_group.remove(enemy_attack)
                    del enemy_attack

    #更新和按条件销毁敌人的攻击
    enemy_attack_group.update()
    for attack in enemy_attack_group.copy():
        if attack.rect.centerx>setting.screen_width+200 or attack.rect.centerx<-200 or attack.isover:
            enemy_attack_group.remove(attack)
            del attack
    
def update_state(setting,showinfo):
    """更新玩家的状态"""
    #更新下ui信息
    showinfo.update()
    #当模式不为玩家对抗时，回复人物血量
    if setting.game_mode!=1:
        if setting.player_1!=None: 
            if setting.health_1+setting.player_1.rehealth<=setting.max_health_1:
                setting.health_1+=setting.player_1.rehealth
            else:
                setting.health_1=setting.max_health_1
        if setting.player_2!=None:
            if setting.health_2+setting.player_2.rehealth<=setting.max_health_2:
                setting.health_2+=setting.player_2.rehealth
            else:
                setting.health_2=setting.max_health_2
    #根据玩家得分，提升其等级和最大血量
    if(setting.score_1>=setting.level_exp*setting.level_1):
        setting.level_1+=1
        setting.max_health_1+=5
        setting.health_1+=5
    if(setting.score_2>=setting.level_exp*setting.level_2):
        setting.level_2+=1
        setting.max_health_2+=5
        setting.health_2+=5       

def update_choose(setting,buttons,choose_buttons):
    """更新当前选择人物的显示"""
    #遍历按钮，根据当前选择的人物，设置显示图片的位置
    for button in buttons:
        if isinstance(setting.player_1,live.MonkeyKing) and isinstance(button,startupui.MonkeyKingButton):
            choose_buttons[0].rect.center=button.rect.center      
        elif isinstance(setting.player_1,live.Fox) and isinstance(button,startupui.FoxButton):
            choose_buttons[0].rect.center=button.rect.center   
        elif isinstance(setting.player_1,live.Yi) and isinstance(button,startupui.YiButton):
            choose_buttons[0].rect.center=button.rect.center   
        elif isinstance(setting.player_1,live.Bin) and isinstance(button,startupui.BinButton):
            choose_buttons[0].rect.center=button.rect.center   

        if isinstance(setting.player_2,live.MonkeyKing) and isinstance(button,startupui.MonkeyKingButton):
            choose_buttons[1].rect.center=button.rect.center      
        elif isinstance(setting.player_2,live.Fox) and isinstance(button,startupui.FoxButton):
            choose_buttons[1].rect.center=button.rect.center   
        elif isinstance(setting.player_2,live.Yi) and isinstance(button,startupui.YiButton):
            choose_buttons[1].rect.center=button.rect.center   
        elif isinstance(setting.player_2,live.Bin) and isinstance(button,startupui.BinButton):
            choose_buttons[1].rect.center=button.rect.center   
    #如果没选的话，把ui设置到窗口外
    if setting.player_1==None:
        choose_buttons[0].rect.center=(1000,1000) 
    if setting.player_2==None:
        choose_buttons[1].rect.center=(1000,1000) 

def update_rigidbody(setting,rigidbody_list):
    """更新物理碰撞"""
    for body in rigidbody_list:
        body.update()

def update_screen(setting,screen,group_player,attack_group,enemy_group,enemy_attack_group,showinfo,buttons,info_label,choose_buttons):
    """更新屏幕"""
    #将各类物体绘制到屏幕上(后渲染的覆盖先渲染的)
    #开始和结束界面
    if(not setting.game_active):
        #清空各类物品
        enemy_group.empty()
        attack_group.empty()    
        enemy_attack_group.empty()
        #绘制按钮
        for button in buttons:
            if isinstance(button,startupui.WinButton):
                if setting.iswin:
                    button.draw()
            elif isinstance(button,startupui.DeadButton):
                if setting.isdead:
                    button.draw()
            else:
                button.draw()
        #如果不是游戏结束的情况，绘制人物选择和介绍图片
        if not (setting.isdead or setting.iswin):
            for button in choose_buttons:
                button.draw()
            if info_label:
                info_label[0].draw()
    #游戏界面
    else:
        #绘制敌人
        for enemy in enemy_group.sprites():
            enemy.draw()
        #绘制玩家
        if setting.player_1!=None:
            setting.player_1.draw()
        if setting.player_2!=None:
            setting.player_2.draw()
        #绘制游戏内的ui
        showinfo.draw()
        #绘制攻击物体
        for attack in attack_group.sprites():
            attack.draw()
        for enemy_attack in enemy_attack_group:
            enemy_attack.draw()

    #更新游戏窗口        
    pygame.display.flip();

