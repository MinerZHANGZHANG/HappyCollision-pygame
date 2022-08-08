'''
effect模块定义了攻击物体的外观和攻击产生的效果
Attack类为模块中其余类的父类，定义了攻击物体的属性
Attack类中 update()方法负责更新攻击物体的移动等状态 draw()方法负责绘制自身
'''

import pygame
import random
import copy
import math

class Attack(pygame.sprite.Sprite):
     """攻击物的基类"""
     def __init__(self,setting,screen,player):
        super().__init__()
        #基本属性
        self.screen=screen
        self.setting=setting
        #发出该攻击的玩家人物
        self.player=player
        #攻击是否结束的标志
        self.isover=False
        #攻击是否命中后消除自身的标志
        self.isbreak=True
        #和攻击发生碰撞的物体列表
        self.collide_list=[]
        #计时器
        self.timer=0
        #物体攻击力
        self.damage=1
        #物体冲击力
        self.power=10
        #攻击的正反图片
        self.surface=setting.hero_monkey_surface
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        #攻击的布局位置
        self.rect=pygame.Rect(0,0,1,1)     
        #攻击的朝向
        self.forward=player.forward
     
     def update(self):
        """更新状态"""
        pass


     def draw(self):
        """根据朝向绘制图像"""
        if(self.forward==1):
            self.screen.blit(self.surface,self.rect)
        else:
            self.screen.blit(self.flip_surface,self.rect)

class YiShoot(Attack):
    """射击,生成一支向右的箭，碰撞销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.yi_weapon_0
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        self.rect=self.surface.get_rect()
        self.rect.centerx=player.rect.centerx
        self.rect.centery=player.rect.centery
        #移动和攻击属性
        self.speed=self.setting.yi_common_speed*player.forward             
        self.damage=self.setting.yi_common_damage
        self.power=self.setting.yi_common_power
        #初始位置
        self.x=float(self.rect.x)  

    def update(self):
        #更新位置，向右移动
        self.x+=self.speed
        self.rect.x=self.x

    def draw(self):
        #绘制到屏幕
        super().draw()

class YiSuperShoot(Attack):
    """生成箭雨向下,碰撞不销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.yi_weapon_1    
        if player.forward==1:
            self.rect=pygame.Rect(player.rect.centerx+160*player.forward,player.rect.centery-100,200,150)
        else:
            self.rect=pygame.Rect(player.rect.centerx+310*player.forward,player.rect.centery-100,200,150)
        #标记碰撞不销毁
        self.isbreak=False
        #伤害属性
        self.damage=self.setting.yi_skill_damage
        self.power=self.setting.yi_skill_power
        #生成三波箭雨队列
        self.arrows_rect_first=[]
        self.arrows_rect_second=[]
        self.arrows_rect_thrid=[]
        for i in range(-5,6):
            self.arrows_rect_first.append(pygame.Rect(player.rect.centerx+250*player.forward+20*i*player.forward,player.rect.centery-150-random.randint(0,150),40,40))
        self.arrows_rect_second=copy.deepcopy(self.arrows_rect_first)
        self.arrows_rect_thrid=copy.deepcopy(self.arrows_rect_first)

    def update(self):
        #根据时间调整箭雨位置
        self.timer+=1   
        if(self.timer<=20):
            for rect in self.arrows_rect_first:
                rect.centery+=10
        elif(self.timer<=40):
            for rect in self.arrows_rect_second:
                rect.centery+=10
        elif(self.timer<=60):
            for rect in self.arrows_rect_thrid:
                rect.centery+=10
        else:
            self.isover=True

    def draw(self):
        #渲染箭雨
        #pygame.draw.rect(self.screen,(200,200,200),self.rect)
        for rect in self.arrows_rect_first:
            self.screen.blit(self.surface,rect)
        for rect in self.arrows_rect_second:
            self.screen.blit(self.surface,rect)
        for rect in self.arrows_rect_thrid:
            self.screen.blit(self.surface,rect)

class YiBreakShoot(Attack):
    """射击一支大型箭矢，碰撞销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.yi_weapon_2
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        self.rect=self.surface.get_rect()
        self.rect.center=player.rect.center
        #移动和攻击属性
        self.speed=self.setting.yi_break_speed*player.forward             
        self.damage=self.setting.yi_break_damage
        self.power=self.setting.yi_break_power
        #初始位置
        self.x=float(self.rect.x) 
        
    def update(self):
        #更新位置，向右移动
        self.x+=self.speed
        self.rect.x=self.x

    def draw(self):
        #绘制到屏幕
        super().draw()

class MonkeyHit(Attack):
    """旋转棍子攻击，碰撞不销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        self.surface=setting.monkey_weapon_0
        self.surface=pygame.transform.scale(self.surface,setting.weapon_size)
        self.rect=self.surface.get_rect()
        self.rect.center=player.rect.center
        self.isbreak=False
        self.damage=setting.monkey_common_damage
        self.power=setting.monkey_common_power

    def update(self):
        #根据时间更换图片形成旋转动画效果
        self.timer+=1   
        if(self.timer<=59):
            self.surface=self.setting.monkey_hit_list[self.timer]
            self.rect.center=(self.player.rect.centerx+30*self.player.forward,self.player.rect.centery)
        else:
            self.isover=True

    def draw(self):
        self.screen.blit(self.surface,self.rect)

class MonkeyRush(Attack):
    """向前跳跃"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #窗口背景图布局
        self.screen_rect=screen.get_rect()
        #属性
        self.isbreak=False
        self.speed=setting.monkey_skill_speed*player.forward
        self.damage=0

    def update(self):
        #根据实现替换英雄图片，并替换玩家位置，形成旋转跳跃的动画效果
        self.timer+=1   
        if(self.timer<=10):
            self.player.surface=self.setting.monkey_jump_list[self.timer]
            self.player.flip_surface=self.setting.monkey_jump_list[self.timer]
            if(self.player.rect.right<self.screen_rect.right) and (self.player.rect.left>self.screen_rect.left):
                self.player.rect.centerx+=self.speed;
                self.player.rect.centery-=(self.speed if self.speed>0 else -self.speed)/2;
        elif(self.timer<=20):
            self.player.surface=self.setting.monkey_jump_list[self.timer]
            self.player.flip_surface=self.setting.monkey_jump_list[self.timer]
            if(self.player.rect.right<self.screen_rect.right) and (self.player.rect.left>self.screen_rect.left):
                self.player.rect.centerx+=self.speed;
                self.player.rect.centery+=(self.speed if self.speed>0 else -self.speed)/2;
        else:
            self.player.surface=self.setting.hero_monkey_surface
            self.player.flip_surface=pygame.transform.flip(self.player.surface,True,False)
            self.isover=True

    def draw(self):
        pass

class MonkeyBreak(Attack):
    """棍子戳地，碰撞不销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.monkey_weapon_1      
        self.rect=self.surface.get_rect()
        self.rect.center=(self.player.rect.x+50,self.player.rect.y-300)
        #标记碰撞不销毁
        self.isbreak=False
        #伤害属性
        self.damage=self.setting.monkey_break_damage
        self.power=self.setting.monkey_break_power

    def update(self):
        #根据时间调整位置
        self.timer+=1   
        if(self.timer<=20):
            self.rect.centery+=15
        elif(self.timer>=60):
            self.isover=True

    def draw(self):
        self.screen.blit(self.surface,self.rect)
        
class FoxHeart(Attack):
    """上下波动的爱心攻击，碰撞销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像
        self.surface=setting.fox_weapon_0
        #布局
        self.rect=self.surface.get_rect()
        self.rect.center=player.rect.center
        #属性
        self.damage=setting.fox_common_damage
        self.speed=setting.fox_common_speed*player.forward

    def update(self):
        self.timer+=1   
        if(self.timer<=20):
            self.rect.centerx+=self.speed
            self.rect.centery+=self.speed/2
        elif(self.timer<=40):
            self.rect.centerx+=self.speed
            self.rect.centery-=self.speed/2
        elif(self.timer<=60):
            self.rect.centerx+=self.speed
            self.rect.centery+=self.speed/2
        elif(self.timer<=80):
            self.rect.centerx+=self.speed
            self.rect.centery-=self.speed/2
        else:
            self.isover=True

    def draw(self):
       self.screen.blit(self.surface,self.rect)

class FoxBeam(Attack):
    """平移的冲击波攻击，碰撞不销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像
        self.surface=setting.fox_weapon_1
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        #布局
        self.rect=self.surface.get_rect()
        self.rect.center=player.rect.center
        #属性
        self.isbreak=False
        self.damage=setting.fox_skill_damage
        self.speed=setting.fox_skill_speed*player.forward

    def update(self):
        self.timer+=1   
        self.rect.centerx+=self.speed

    def draw(self):
        super().draw()

class FoxBreak(Attack):
    """平移的爱心群攻击，碰撞不销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.fox_weapon_2       
        self.rect=pygame.Rect(0,0,120,120)
        self.isbreak=False
        #伤害属性
        self.damage=self.setting.fox_break_damage
        self.speed=self.setting.fox_break_speed*player.forward
        self.power=self.setting.fox_break_power
        #爱心列表
        self.hearts_rect=[]
        for i in range(-5,5):
            self.hearts_rect.append(pygame.Rect((player.rect.centerx+i*random.randint(-20,20),player.rect.centery+i*10),(self.rect.size)))

    def update(self):
        avg_center=[0,0]
        #根据时间调整位置
        for rect in self.hearts_rect:
            rect.centerx+=self.speed
            rect.centery+=random.randint(-5,5)
            avg_center[0]+=rect.centerx
            avg_center[1]+=rect.centery         
        self.rect.center=(avg_center[0]/10-60,avg_center[1]/10-60)


    def draw(self):
        #pygame.draw.rect(self.screen,(200,200,200),self.rect)
        for rect in self.hearts_rect:
            self.screen.blit(self.surface,rect)

class BinBall(Attack):
    """射出一个东西，碰撞销毁"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.bin_weapon_0
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        self.rect=self.surface.get_rect()
        self.rect.center=player.rect.center
        #移动和攻击属性
        self.speed=self.setting.bin_common_speed*player.forward             
        self.damage=self.setting.bin_common_damage
        self.power=self.setting.bin_common_power
 
    def update(self):
        #更新位置，向右移动
        self.rect.centerx+=self.speed

    def draw(self):
        #绘制到屏幕
        super().draw()

class BinBuff(Attack):
    """为自己和队友提供加速效果"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #图像和布局
        self.surface=setting.bin_weapon_1
        self.rect=self.surface.get_rect()
        self.rect.size=(0,0)
        self.rect_=self.surface.get_rect()
        self.rect_.centerx=player.rect.centerx
        self.rect_.centery=player.rect.centery-60
        self.isbreak=False
        #移动和攻击属性
        self.add_speed=self.setting.bin_skill_speed           
        self.damage=0
        self.power=0

    def update(self):        
        self.timer+=1
        #开始时加速
        if self.timer==1:
            if self.setting.game_mode!=1:
                if self.setting.player_1!=None:
                    self.setting.player_1.speed+=self.add_speed
                if self.setting.player_2!=None:
                    self.setting.player_2.speed+=self.add_speed
            else:
                self.player.speed+=self.add_speed
        #更新位置和人物一同移动
        if self.timer<self.setting.bin_skill_during:
            self.rect_.centerx=self.player.rect.centerx
            self.rect_.centery=self.player.rect.centery-60
        #结束时减速
        if self.timer==self.setting.bin_skill_during:
            self.isover=True
            if self.setting.game_mode!=1:
                if self.setting.player_1!=None:
                    self.setting.player_1.speed-=self.add_speed
                if self.setting.player_2!=None:
                    self.setting.player_2.speed-=self.add_speed 
            else:
                self.player.speed-=self.add_speed             

    def draw(self):
        #绘制到屏幕
        self.screen.blit(self.surface,self.rect_)

class BinBreak(Attack):
    """范围逐渐增大的攻击"""
    def __init__(self,setting,screen,player):
        super().__init__(setting,screen,player)
        #逐渐变大的图像列表
        self.surface=setting.bin_break_list[0]
        #布局
        self.rect=self.surface.get_rect()
        #初始位置
        self.rect.center=player.rect.center
        self.local_center_x=self.rect.centerx
        self.local_center_y=self.rect.centery
        #属性
        self.isbreak=False
        self.damage=setting.bin_break_damage
        self.speed=setting.bin_break_speed*player.forward
        self.power=setting.bin_break_power

    def update(self):
        self.timer+=1
        #随时间替换更大的图像，形成动画
        if(self.timer<70):
            self.surface=self.setting.bin_break_list[self.timer]
            self.rect=self.surface.get_rect()
            self.rect.centery=self.local_center_y
            self.rect.centerx=self.local_center_x+self.timer*self.speed
        elif(self.timer>160):
            self.isover=True

    def draw(self):
        self.screen.blit(self.surface,self.rect)


class EnemyFireBall(Attack):
    """敌人的远程攻击"""
    def __init__(self,setting,screen,player,enemy):
        super().__init__(setting,screen,player)
        #发出该攻击的敌人物体
        self.enemy=enemy
        #图像
        self.surface=setting.enemy_weapon_0
        #布局
        self.rect=self.surface.get_rect()
        self.rect.center=enemy.rect.center
        #属性
        self.speed=setting.enemy_mage_attack_speed*(-enemy.forward)
        self.damage=setting.enemy_mage_attack_damage
    
    def update(self):
        self.rect.centerx-=self.speed

    def draw(self):
        self.screen.blit(self.surface,self.rect)

class EnemyTargetBall(Attack):
    """敌人的远程攻击(追踪版本)"""
    def __init__(self,setting,screen,player,enemy):
        super().__init__(setting,screen,player)
        #发出该攻击的敌人物体
        self.enemy=enemy
        #图像
        self.surface=setting.enemy_weapon_2
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        #布局
        self.rect=self.surface.get_rect()
        self.rect.center=enemy.rect.center
        #属性
        self.speed=setting.enemy_artillery_attack_speed
        self.damage=setting.enemy_artillery_attack_damage
        #目标玩家
        self.player=self.enemy.player
        #移动朝向
        self.direction_x=0
        self.direction_y=0
        #修改朝向的间隔
        self.change_interval=1.5*setting.fps
        #最大修改次数
        self.count=8

    def update(self):
        #根据玩家位置计算朝向
        if(self.timer<=0):
            if self.player.rect.centerx-self.rect.centerx<=0:
                self.direction_x=-1             
            else:
                self.direction_x=1
            self.forward=(-self.direction_x)
            if self.player.rect.centery-self.rect.centery<=0:
                self.direction_y=-1
            else:
                self.direction_y=1
            #重置计时器
            self.timer=self.change_interval
            self.count-=1
        #根据朝向移动
        else:
            if self.rect.left > 0 and self.direction_x<0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.right < self.setting.screen_width and self.direction_x>0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.bottom < self.setting.screen_height and self.direction_y>0:
                self.rect.centery+=self.direction_y*self.speed
            if self.rect.top > 0 and self.direction_y<0:
                self.rect.centery+=self.direction_y*self.speed
            self.timer-=1
        #当改变朝向的次数用完时销毁自身
        if self.count==0:
            self.isover=True

    def draw(self):
        super().draw()

class EnemyCollide(Attack):
    """敌人的近战攻击"""
    def __init__(self,setting,screen,player,enemy):
        super().__init__(setting,screen,player)
        #发出该攻击的敌人物体
        self.enemy=enemy
        #布局
        self.rect=self.enemy.rect
        #属性
        self.damage=setting.enemy_warrior_attack_damage
        self.isbreak=False

    def update(self):
        #当敌人死亡后终止该攻击(把碰撞范围设为0)
        if(self.enemy.isalive):
            self.rect.center=self.enemy.rect.center
        else:
            self.rect.size=(0,0)

    def draw(self):
        pass


class EnemyRingAttack(Attack):
    """逐渐变大的范围攻击"""
    def __init__(self,setting,screen,player,enemy):
        super().__init__(setting,screen,player)
        #图像
        self.enemy=enemy
        self.surface=setting.enemy_weapon_1_list[0]
        #布局
        self.rect=self.surface.get_rect()
        self.rect.center=enemy.rect.center
        #属性
        self.isbreak=False
        self.damage=setting.enemy_overlord_attack_damage_0

    def update(self):
        #更新位置跟随人物，并调整大小
        self.timer+=1   
        if(self.timer<100):            
            self.surface=self.setting.enemy_weapon_1_list[self.timer]
            self.rect=self.surface.get_rect()
            self.rect.center=self.enemy.rect.center
        elif(self.timer>160):
            self.isover=True

    def draw(self):
        self.screen.blit(self.surface,self.rect)


class EnemyShoot(Attack):
    """敌人的较大范围远程攻击"""
    def __init__(self,setting,screen,player,enemy):
        super().__init__(setting,screen,player)
        #发出该攻击的敌人物体
        self.enemy=enemy
        self.isbreak=False
        #图像
        self.surface=setting.enemy_weapon_2
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        #布局
        self.rect=pygame.Rect(0,0,250,80)
        self.rect.center=enemy.rect.center
        self.rect_list=[]
        #属性
        self.forward=-enemy.forward
        self.speed=setting.enemy_overlord_attack_speed*(-self.forward)
        self.damage=setting.enemy_overlord_attack_damage_1
        #生成位置布局列表
        for i in range (20):
            self.rect_list.append(pygame.Rect(self.rect.centerx+random.randint(-200,100),self.rect.centery+random.randint(-50,50),30,30))
        
    def update(self):
        #更新位置
        self.rect.centerx+=self.speed
        for rect in self.rect_list:
            rect.centerx+=self.speed

    def draw(self):
        #根据布局列表绘制各个物体
        for rect in self.rect_list:
            if self.speed<0:
                self.screen.blit(self.surface,rect)
            else:
                self.screen.blit(self.flip_surface,rect)