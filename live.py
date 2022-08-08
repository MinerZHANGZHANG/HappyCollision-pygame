'''
live模块定义了玩家操控的人物
基类Hero,继承pygame中的精灵类，通过setting实例初始化了人物的生命值等属性
基类Hero实例方法 update()更新人物位置  attack()按照技能冷却决定是否返回攻击物体  draw()绘制人物到屏幕
继承Hero类的MonkeyKing\Yi\Fox\Bin类，添加了三个返回攻击物体的实例方法
common_attack() skill_attack() break_attack() 对应人物不同类型的攻击

'''

import pygame
import effect

class Hero(pygame.sprite.Sprite):
    """人物基类"""
    def __init__(self,surface,size,cooling,screen,max_health,speed,skill_icon):
        #初始化精灵(Sprite)类
        super().__init__()
        #屏幕的图像
        self.screen=screen
        #屏幕的布局rect
        self.screen_rect=self.screen.get_rect()
        #人物的正反图像
        self.surface=surface
        self.surface=pygame.transform.scale(self.surface,size)
        self.flip_surface=pygame.transform.flip(self.surface,True,False)
        #人物的布局
        self.rect=self.surface.get_rect()
        #人物的属性
        self.max_health=max_health
        self.speed=speed
        self.weight=5
        self.skill_cooling=cooling
        self.rehealth=self.setting.rehealth_rate*self.max_health
        #人物的状态
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.skill_timer=[0,0,0]
        self.skill_icon=skill_icon
        #人物朝向 -1朝左，1朝右
        self.forward=1

    def update(self):
        """更新人物位置和冷却"""
        #根据状态标志更新位置
        if self.move_left and self.rect.left > 0:
            self.rect.centerx -= self.speed
            self.forward=-1            
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed
            self.forward=1
        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += self.speed
        if self.move_up and self.rect.top > 0:
            self.rect.centery -= self.speed
        #更新冷却时间
        for i in range(3):
            if self.skill_timer[i]>0:
                self.skill_timer[i]-=1
    
    def attack(self,number,skill):
        """根据冷却状态返回攻击物体"""
        if self.setting.iscooling:
             if self.skill_timer[number]<=0:              
                 self.skill_timer[number]=self.skill_cooling[number]
                 return skill
             else:
                 return None
        else:
             return skill

    def draw(self):
        """根据朝向和布局绘制人物图像"""
        if self.forward==1:
            self.screen.blit(self.surface,self.rect)
        elif self.forward==-1:
            self.screen.blit(self.flip_surface,self.rect)


class MonkeyKing(Hero):
    """战士类"""
    def __init__(self,setting,screen):
        self.setting=setting
        super().__init__(setting.hero_monkey_surface,setting.hero_size,setting.monkey_cooling,
                     screen,setting.hero_monekey_maxhealth,setting.hero_monekey_speed,setting.monkey_attack_icon)
           
    def common_attack(self):
         """返回一个普通攻击(技能1)物体"""
         return super().attack(0,effect.MonkeyHit(self.setting,self.screen,self))

    def skill_attack(self):
         """返回一个技能攻击(技能2)物体"""
         return super().attack(1,effect.MonkeyRush(self.setting,self.screen,self))

    def break_attack(self):
         """返回一个大招攻击(技能3)物体"""
         return super().attack(2,effect.MonkeyBreak(self.setting,self.screen,self))

class Yi(Hero):
    """射手类"""
    def __init__(self,setting,screen):
        self.setting=setting
        super().__init__(setting.hero_yi_surface,setting.hero_size,setting.yi_cooling,
                     screen,setting.hero_yi_maxhealth,setting.hero_yi_speed,setting.yi_attack_icon)
        
    def common_attack(self):
         return super().attack(0,effect.YiShoot(self.setting,self.screen,self))

    def skill_attack(self):
         return super().attack(1,effect.YiSuperShoot(self.setting,self.screen,self))

    def break_attack(self):
         return super().attack(2,effect.YiBreakShoot(self.setting,self.screen,self))

class Fox(Hero):
    """法师类"""
    def __init__(self,setting,screen):
        self.setting=setting
        super().__init__(setting.hero_fox_surface,setting.hero_size,setting.fox_cooling,
                     screen,setting.hero_fox_maxhealth,setting.hero_fox_speed,setting.fox_attack_icon)
        

    def common_attack(self):
        return super().attack(0,effect.FoxHeart(self.setting,self.screen,self))       

    def skill_attack(self):
        return super().attack(1,effect.FoxBeam(self.setting,self.screen,self))    
   
    def break_attack(self):
         return super().attack(2,effect.FoxBreak(self.setting,self.screen,self))    

class Bin(Hero):
    """辅助类"""
    def __init__(self,setting,screen):
        self.setting=setting
        super().__init__(setting.hero_bin_surface,setting.hero_size,setting.bin_cooling,
                     screen,setting.hero_bin_maxhealth,setting.hero_bin_speed,setting.bin_attack_icon)       

    def common_attack(self):
         return super().attack(0,effect.BinBall(self.setting,self.screen,self))

    def skill_attack(self):
         return super().attack(1,effect.BinBuff(self.setting,self.screen,self))

    def break_attack(self):
         return super().attack(2,effect.BinBreak(self.setting,self.screen,self))
