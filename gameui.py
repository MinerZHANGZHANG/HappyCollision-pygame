'''
gameui模块定义了游戏过程中的ui显示，例如玩家的血条经验条等(敌人的血条在enemy模块中定义),以及当鼠标移入按钮区域时的提示内容
Info类定义了游戏过程中，玩家的血条、经验条、血量数值、经验数值、技能冷却、玩家得分、敌人数量的显示
Info类中 update()方法负责更新上述图像的内容 draw()方法负责绘制这些图像
ExInfo类定义了按钮移入时显示的图像,以及按钮本身的放大效果
ExInfo类中 draw()方法负责绘制自身和替换按钮的图像 recover()方法负责恢复按钮原图像
'''

import pygame
from pygame.sprite import Group
from live import Hero
from startupui import CoolingButton

class Info():
    """显示游戏内各类信息"""
    def __init__(self,setting,screen):
        #屏幕图像和布局
        self.screen=screen
        self.screen_rect=screen.get_rect()
        #设置
        self.setting=setting  
        #设置字体为30号的系统默认字体
        self.font=pygame.font.SysFont(None,30)
        #生命条背景
        self.health_rect_background_1=pygame.Rect(50,400,200,15)
        self.health_rect_background_2=pygame.Rect(550,400,200,15)
        #经验条背景
        self.exp_rect_background_1=pygame.Rect(50,430,200,15)
        self.exp_rect_background_2=pygame.Rect(550,430,200,15)
        #技能冷却条
        self.skill_background_1=self.setting.monkey_attack_icon
        self.skill_rect_background_1=[pygame.Rect(50,340,40,40),pygame.Rect(110,340,40,40),pygame.Rect(170,340,40,40)]
        self.skill_rect_1=[pygame.Rect(50,340,40,40),pygame.Rect(110,340,40,40),pygame.Rect(170,340,40,40)]

        self.skill_background_2=self.setting.monkey_attack_icon
        self.skill_rect_background_2=[pygame.Rect(550,340,40,40),pygame.Rect(610,340,40,40),pygame.Rect(670,340,40,40)]
        self.skill_rect_2=[pygame.Rect(550,340,40,40),pygame.Rect(610,340,40,40),pygame.Rect(670,340,40,40)]
        #更新初始化各种图像
        self.update()

    def update(self):
        """更新各类信息"""

        #更新经验条
        self.exp_rect_1=pygame.Rect(50,430,self.setting.score_1/(self.setting.level_exp*self.setting.level_1)*200,15)
        self.exp_rect_2=pygame.Rect(550,430,self.setting.score_2/(self.setting.level_exp*self.setting.level_2)*200,15)
        
        #更新生命条
        if(self.setting.game_mode==1):
            self.health_rect_1=pygame.Rect(50,400,self.setting.health_1/self.setting.max_health_1*200/self.setting.pvp_health_rate,15)
            self.health_rect_2=pygame.Rect(550,400,self.setting.health_2/self.setting.max_health_2*200/self.setting.pvp_health_rate,15)
        else:
            self.health_rect_1=pygame.Rect(50,400,self.setting.health_1/self.setting.max_health_1*200,15)
            self.health_rect_2=pygame.Rect(550,400,self.setting.health_2/self.setting.max_health_2*200,15)

        #更新人物技能图标冷却状态
        if self.setting.player_1!=None:
            for i in range(3):
                self.skill_background_1=self.setting.player_1.skill_icon
                if i<self.setting.level_1:
                    self.skill_rect_1[i].size=(40,(self.setting.player_1.skill_timer[i]/self.setting.player_1.skill_cooling[i])*40)
                else:
                    self.skill_rect_1[i].size=(40,40)
        if self.setting.player_2!=None:
            for i in range(3):
                self.skill_background_2=self.setting.player_2.skill_icon
                if i<self.setting.level_2:
                    self.skill_rect_2[i].size=(40,(self.setting.player_2.skill_timer[i]/self.setting.player_2.skill_cooling[i])*40)
                else:
                    self.skill_rect_2[i].size=(40,40)  
                    
        #更新得分文字图像
        self.score_surface=self.font.render("score:{0}:{1}".format(str(self.setting.score_1),str(self.setting.score_2)),True,self.setting.text_color)
        self.score_rect=self.score_surface.get_rect()
        self.score_rect.center=(400,50)

        #更新等级文字图像
        self.level_surface_1=self.font.render(str(self.setting.level_1),True,self.setting.text_color)
        self.level_rect_1=self.score_surface.get_rect()
        self.level_rect_1.center=(65,438)

        self.level_surface_2=self.font.render(str(self.setting.level_2),True,self.setting.text_color)
        self.level_rect_2=self.score_surface.get_rect()
        self.level_rect_2.center=(565,438)
        
        #更新血量文字图像
        self.health_number_surface_1=self.font.render(format(self.setting.health_1,".1f"),True,self.setting.text_color)
        self.health_number_rect_1=self.score_surface.get_rect()
        self.health_number_rect_1.center=(55,408)

        self.health_number_surface_2=self.font.render(format(self.setting.health_2,".1f"),True,self.setting.text_color)
        self.health_number_rect_2=self.score_surface.get_rect()
        self.health_number_rect_2.center=(555,408)
        
        #更新敌人数量文字图像
        self.enemy_surface=self.font.render("enemy:"+str(self.setting.enemy_number),True,self.setting.text_color)
        self.enemy_rect=self.enemy_surface.get_rect()
        self.enemy_rect.left=self.screen_rect.left+40
        self.enemy_rect.top=10

    def draw(self):
        """绘制各类信息"""

        if self.setting.player_1!=None:
            #绘制生命条和其背景
            pygame.draw.rect(self.screen,(200,200,200),self.health_rect_background_1)
            pygame.draw.rect(self.screen,(30,30,30),self.health_rect_1)

            #绘制经验条和其背景
            pygame.draw.rect(self.screen,(200,200,200),self.exp_rect_background_1)
            pygame.draw.rect(self.screen,(30,30,30),self.exp_rect_1)

            #绘制技能图标和冷却状态
            for i in range(3):
                self.screen.blit(self.skill_background_1[i],self.skill_rect_background_1[i])
                if self.setting.iscooling or i>=self.setting.level_1:
                    pygame.draw.rect(self.screen,(200,200,200),self.skill_rect_1[i])
            
            #绘制等级和生命值文字
            self.screen.blit(self.level_surface_1,self.level_rect_1)
            self.screen.blit(self.health_number_surface_1,self.health_number_rect_1)
        
        #同上
        if self.setting.player_2!=None:
            pygame.draw.rect(self.screen,(200,200,200),self.health_rect_background_2)
            pygame.draw.rect(self.screen,(30,30,30),self.health_rect_2)

            pygame.draw.rect(self.screen,(200,200,200),self.exp_rect_background_2)
            pygame.draw.rect(self.screen,(30,30,30),self.exp_rect_2)

            for i in range(3):
                self.screen.blit(self.skill_background_2[i],self.skill_rect_background_2[i])
                if self.setting.iscooling or i>=self.setting.level_2:
                    pygame.draw.rect(self.screen,(200,200,200),self.skill_rect_2[i])

            self.screen.blit(self.level_surface_2,self.level_rect_2)
            self.screen.blit(self.health_number_surface_2,self.health_number_rect_2)


        #绘制分数和敌人量文字
        self.screen.blit(self.score_surface,self.score_rect)
        self.screen.blit(self.enemy_surface,self.enemy_rect)

class ExInfo():
    """为物体显示其补充信息"""
    def __init__(self,screen,base,info_surface):
        #屏幕、图片和布局
        self.screen=screen       
        self.surface=info_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(400,400)     
        #补充信息的物体，大概也可以叫父物体？
        self.base=base
        self.base_surface=self.base.surface
        #该物体图像的放大版本，用于在鼠标移入时替换，产生缩放效果
        self.base_bigger_surface=pygame.transform.scale(self.base.surface,(self.base.rect.width*1.1,self.base.rect.height*1.1))        
        #对于自身有多种图片的按钮，特殊处理
        if isinstance(self.base,CoolingButton):
            self.base_surface_=self.base.surface_
            self.base_bigger_surface_=pygame.transform.scale(self.base.surface_,(self.base.rect.width*1.1,self.base.rect.height*1.1))

    def draw(self): 
        """渲染自身并替换父物体图像"""
        self.base.surface=self.base_bigger_surface
        if isinstance(self.base,CoolingButton):
            self.base.surface_=self.base_bigger_surface_
        self.screen.blit(self.surface,self.rect)

    
    def recover(self):
        """恢复父物体图像的原有大小"""
        self.base.surface=self.base_surface
        if isinstance(self.base,CoolingButton):
            self.base.surface_=self.base_surface_

