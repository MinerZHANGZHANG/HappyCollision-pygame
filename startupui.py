'''
startupui模块定义了在游戏启动界面的各类ui组件外观
Button类为模块中其它类的父类，虽然叫button但不包括事件处理，只定义了图像和布局（点击事件的处理在game_event模块中）
Button类提供一个draw()实例方法绘制自身
子类 SelectButton WinButton DeadButton 作为界面背景（选人、胜利、失败）
子类 MonkeyKingButton YiButton FoxButton BinButton 作为选人按钮
其它子类为启动界面的各类功能按钮，包括开始特定模式的游戏，开关冷却等
'''

import pygame.font
import pygame.draw

class Button():
    """按钮基类"""
    def __init__(self,screen,setting):
        #窗口和设置属性
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.setting=setting
        #按钮的长宽
        self.width = 120
        self.height = 50
        #按钮背景和字体颜色
        self.button_color = (40, 200, 0)
        self.text_color = (255, 255, 255)
        #默认字体
        self.font = pygame.font.SysFont(None, 50)
        #布局
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
    
    def draw(self):
        """渲染方法"""
        self.screen.blit(self.surface, self.rect)


class MonkeyKingButton(Button):
     """战士按钮"""
     def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=self.setting.surface_none
        self.rect =  pygame.Rect((0,0),(200,380))

class FoxButton(Button):
     """法师按钮"""
     def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=self.setting.surface_none
        self.rect =  pygame.Rect((200,0),(200,380))

class BinButton(Button):
     """辅助按钮"""
     def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=self.setting.surface_none
        self.rect =  pygame.Rect((400,0),(200,380))

class YiButton(Button):
     """射手按钮"""
     def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=self.setting.surface_none
        self.rect =  pygame.Rect((600,0),(200,380))

class SelectButton(Button):
    """人物选择界面"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=self.setting.screen_surface_select
        self.rect = self.surface.get_rect()        

class WinButton(Button):
     """胜利界面"""
     def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=self.setting.screen_surface_win
        self.rect =  self.surface.get_rect()

class DeadButton(Button):
     """失败界面"""
     def __init__(self,screen,setting):
         super().__init__(screen,setting)
         self.surface=setting.screen_surface_dead
         self.rect =  self.surface.get_rect()

class PVEButton(Button):
    """普通模式按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.button_pve_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(400,100)

class PVPButton(Button):
    """玩家对抗按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.button_pvp_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(400,200)

class EndlessButton(Button):
    """无尽模式按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.button_endless_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(400,300)


class PlayerButton1(Button):
    """玩家1人物选择标记"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.player_1_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(1000,1000)

class PlayerButton2(Button):
    """玩家2人物选择标记"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.player_2_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(1000,1000)

class NoneButton(Button):
    """空白按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.surface_none
        self.rect=self.surface.get_rect()
        self.rect.center=(1000,1000)
        self.rect.size=(1,1)

class CoolingButton(Button):
    """技能冷却按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.button_cooling_surface_0
        self.surface_=setting.button_cooling_surface_1
        self.rect=self.surface.get_rect()
        self.rect.center=(70,360)
    
    def draw(self):
        """根据技能状态绘制按钮"""
        if self.setting.iscooling:
            self.screen.blit(self.surface, self.rect)
        else:
            self.screen.blit(self.surface_, self.rect)


class ControlButton(Button):
    """控制按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.button_control_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(740,390)

class RecordButton(Button):
    """记录按钮"""
    def __init__(self,screen,setting):
        super().__init__(screen,setting)
        self.surface=setting.button_memory_surface
        self.rect=self.surface.get_rect()
        self.rect.center=(70,420)
