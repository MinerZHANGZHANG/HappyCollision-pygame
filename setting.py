'''
setting模块负责汇总游戏中的数据
Setting类定义了游戏中各类属性，导入的图像，游戏状态等信息
'''

import pygame
import live

class Setting(object):
    """全局设置，导入各类文件和属性"""
    def __init__(self):
        
        #游戏窗口大小
        self.screen_width=800
        self.screen_height=450
        #窗口标题(中文可能会导致pyinstaller打包失败)
        self.screen_caption="HappyKings"
        #游戏记录文件路径       
        self.record_path="GameRecord.csv"
        #游戏操作文件路径
        self.control_path="HowToPlay.txt"
        #游戏默认最大帧率
        self.fps=60

        #不同界面的背景
        self.screen_surface_background=pygame.image.load(r"Image\Background\Background.png")
        self.screen_surface_select=pygame.image.load(r"Image\Background\Select.png")
        self.screen_surface_win=pygame.image.load(r"Image\Background\Win.png")
        self.screen_surface_dead=pygame.image.load(r"Image\Background\Dead.png")
        #透明图片
        self.surface_none=pygame.image.load(r"Image\Background\None.png")
        #按钮图片
        self.button_pve_surface=pygame.image.load(r"Image\Button\PVE.png")
        self.button_pvp_surface=pygame.image.load(r"Image\Button\PVP.png")
        self.button_endless_surface=pygame.image.load(r"Image\Button\Endless.png")
        self.button_control_surface=pygame.image.load(r"Image\Button\Control.png")
        self.button_memory_surface=pygame.image.load(r"Image\Button\Record.png")
        self.button_cooling_surface_0=pygame.image.load(r"Image\Button\CoolingYes.png")
        self.button_cooling_surface_1=pygame.image.load(r"Image\Button\CoolingNo.png")
        #玩家选择标签
        self.player_1_surface=pygame.image.load(r"Image\Button\Player1.png")
        self.player_2_surface=pygame.image.load(r"Image\Button\Player2.png")
        #按钮功能介绍图片
        self.introduce_none=pygame.image.load(r"Image\Info\Introduce.png")
        self.introduce_control=pygame.image.load(r"Image\Info\Control.png")
        self.introduce_cooling=pygame.image.load(r"Image\Info\Cooling.png")
        self.introduce_pvp=pygame.image.load(r"Image\Info\PVP.png")
        self.introduce_pve=pygame.image.load(r"Image\Info\PVE.png")
        self.introduce_endless=pygame.image.load(r"Image\Info\Endless.png")
        self.introduce_record=pygame.image.load(r"Image\Info\Record.png")

        #游戏状态标志
        #是否在游戏中
        self.game_active=False
        #游戏结束后是否在等待输入
        self.iswait=True
        #游戏是否初始化
        self.isinit=False
        #游戏是否胜利
        self.iswin=False
        #游戏是否失败
        self.isdead=False
        #游戏模式(0:五波敌人的PVE模式 1:玩家对抗的PVP模式 2:无限刷出怪物的无尽模式)
        self.game_mode=0
        #游戏持续时间计数
        self.timer=0        
        #敌人计数
        self.enemy_number=0

        #游戏是否启动技能冷却
        self.iscooling=True

        #玩家人物状态
        #玩家的选择的人物1
        self.player_1=None
        #该人物最大生命值
        self.max_health_1=1
        #该人物当前生命值
        self.health_1=0
        #该人物等级
        self.level_1=1
        #得分计数
        self.score_1=0
        
        #玩家的选择的人物2，属性作用同上
        self.player_2=None
        self.max_health_2=1
        self.health_2=0
        self.level_2=1
        self.score_2=0

        #物理模拟
        #摩擦系数
        self.friction=0.05
        #反弹系数
        self.rebound=0.8

        #默认人物大小
        self.hero_size=(80,80)  
        #默认武器大小
        self.weapon_size=(100,100)
        #玩家的生命回复速度
        self.rehealth_rate=0.001
        #玩家对抗模式下的血量倍率
        self.pvp_health_rate=10
        #每次升级需要的经验
        self.level_exp=5

        #战士属性    
        #最大生命值    
        self.hero_monekey_maxhealth=200
        #移动速度
        self.hero_monekey_speed=5
        
        #战士攻击属性
        #技能冷却，先后对应三个技能
        self.monkey_cooling=[1*self.fps,2*self.fps,5*self.fps]
        #技能1伤害
        self.monkey_common_damage=3
        #技能1冲击力
        self.monkey_common_power=20
        #技能2速度
        self.monkey_skill_speed=8
        #技能3伤害
        self.monkey_break_damage=6
        #技能3冲击力
        self.monkey_break_power=50

        #技能相关图片 
        #人物图片
        self.hero_monkey_surface=pygame.image.load(r"Image\Hero\MonkeyKing.png") 
        #技能1
        self.monkey_weapon_0=pygame.image.load(r"Image\Skill\MonkeyKing\0.png")
        self.monkey_weapon_0=pygame.transform.scale(self.monkey_weapon_0,(100,100))
        #生成技能1武器旋转攻击的帧动画
        self.monkey_hit_list=[]
        for i in range(0,60):           
            self.monkey_hit_list.append(pygame.transform.rotate(self.monkey_weapon_0,-i*10))
        #技能2
        self.monkey_jump_list=[]
        #生成技能2旋转跳跃的帧动画
        self.hero_monkey_surface=pygame.transform.scale(self.hero_monkey_surface,self.hero_size)
        for i in range(0,21):           
            self.monkey_jump_list.append(pygame.transform.rotate(self.hero_monkey_surface,-i*18))
        #技能3
        self.monkey_weapon_1=pygame.image.load(r"Image\Skill\MonkeyKing\1.png")
        self.monkey_weapon_1=pygame.transform.scale(self.monkey_weapon_1,(180,180))
        #技能的图标
        self.monkey_attack_icon=[]
        for i in range(3):
            self.monkey_attack_icon.append(pygame.transform.scale(pygame.image.load(r"Image\Icon\MonkeyKing\{0}.png".format(i)),(40,40)))


        #射手属性       
        self.hero_yi_maxhealth=140
        self.hero_yi_speed=4
        #射手攻击属性
        self.yi_cooling=[0.5*self.fps,3*self.fps,7*self.fps]

        self.yi_common_damage=40
        self.yi_common_speed=6
        self.yi_common_power=20

        self.yi_skill_damage=2
        self.yi_skill_power=10

        self.yi_break_damage=120
        self.yi_break_speed=4
        self.yi_break_power=100
        #射手图片
        self.hero_yi_surface=pygame.image.load(r"Image\Hero\Yi.png")
        self.yi_weapon_0=pygame.image.load(r"Image\Skill\Yi\0.png")
        self.yi_weapon_0=pygame.transform.scale(self.yi_weapon_0,(40,40))
        self.yi_weapon_1=pygame.transform.rotate(self.yi_weapon_0,-90)
        self.yi_weapon_2=pygame.image.load(r"Image\Skill\Yi\1.png")
        self.yi_weapon_2=pygame.transform.scale(self.yi_weapon_2,(120,120))
        self.yi_attack_icon=[]
        for i in range(3):
            self.yi_attack_icon.append(pygame.transform.scale(pygame.image.load(r"Image\Icon\Yi\{0}.png".format(i)),(40,40)))


        #法师属性    
        self.hero_fox_maxhealth=120
        self.hero_fox_speed=3
        #法师攻击属性
        self.fox_cooling=[1.5*self.fps,2*self.fps,8*self.fps]
        self.fox_common_damage=90
        self.fox_common_speed=10
        self.fox_common_power=30

        self.fox_skill_damage=1.5
        self.fox_skill_speed=6
        self.fox_skill_power=15

        self.fox_break_damage=4
        self.fox_break_speed=4
        self.fox_break_power=10
        #法师图片
        self.hero_fox_surface=pygame.image.load(r"Image\Hero\Fox.png")
        self.fox_weapon_0=pygame.image.load(r"Image\Skill\Fox\0.png")
        self.fox_weapon_0=pygame.transform.scale(self.fox_weapon_0,(60,60))
        self.fox_weapon_1=pygame.image.load(r"Image\Skill\Fox\1.png")
        self.fox_weapon_1=pygame.transform.scale(self.fox_weapon_1,(100,100))
        self.fox_weapon_2=pygame.transform.scale(self.fox_weapon_0,(40,40))
        self.fox_attack_icon=[]
        for i in range(3):
            self.fox_attack_icon.append(pygame.transform.scale(pygame.image.load(r"Image\Icon\Fox\{0}.png".format(i)),(40,40)))

        

        #辅助属性      
        self.hero_bin_maxhealth=150
        self.hero_bin_speed=4
        #辅助攻击属性
        self.bin_cooling=[1*self.fps,5*self.fps,8*self.fps]

        self.bin_common_damage=80
        self.bin_common_speed=5
        self.bin_common_power=20

        self.bin_skill_during=2*self.fps
        self.bin_skill_speed=4

        self.bin_break_damage=2
        self.bin_break_speed=5
        self.bin_break_power=1

        #辅助图片
        self.bin_weapon_0=pygame.image.load(r"Image\Skill\Bin\0.png")
        self.bin_weapon_0=pygame.transform.scale(self.bin_weapon_0,(60,60))
        self.bin_weapon_1=pygame.image.load(r"Image\Skill\Bin\1.png")
        self.bin_weapon_1=pygame.transform.scale(self.bin_weapon_1,(60,60))
        self.bin_weapon_2=pygame.image.load(r"Image\Skill\Bin\2.png")
        self.bin_attack_icon=[]
        for i in range(3):
            self.bin_attack_icon.append(pygame.transform.scale(pygame.image.load(r"Image\Icon\Bin\{0}.png".format(i)),(40,40)))

        self.hero_bin_surface=pygame.image.load(r"Image\Hero\Bin.png")
        #生成逐渐变大的攻击帧动画
        self.bin_break_list=[]
        for i in range(20):
            self.bin_break_list.append(pygame.transform.scale(self.bin_weapon_2,(60,60)))
        for i in range(50):
            self.bin_break_list.append(pygame.transform.scale(self.bin_weapon_2,(60+i*4,60+i*4)))

        #默认字体颜色(白)
        self.text_color=(255,255,255)
       
        #敌人基础生成位置
        self.enemy_genrate_point=(650,200)
        #无尽模式中，敌人同一时间内最大数量
        self.enemy_max=30

        #敌人图片
        #小法师=v=
        self.enemy_mage_surface=pygame.image.load(r"Image\Enemy\SmallMage.png")
        self.enemy_mage_surface=pygame.transform.scale(self.enemy_mage_surface,(60,60))
        #小战士0_0
        self.enemy_warrior_surface=pygame.image.load(r"Image\Enemy\SmallWarrior.png")
        self.enemy_warrior_surface=pygame.transform.scale(self.enemy_warrior_surface,(60,60))
        #小炮兵ovo
        self.enemy_artillery_surface=pygame.image.load(r"Image\Enemy\Artillery.png")
        self.enemy_artillery_surface=pygame.transform.scale(self.enemy_artillery_surface,(80,80))
        #大宿主 _
        self.enemy_overlord_surface=pygame.image.load(r"Image\Enemy\Overlord.png")
        self.enemy_overlord_surface=pygame.transform.scale(self.enemy_overlord_surface,(160,160))
        #宿主眼睛* *
        self.enemy_eye_surface=pygame.image.load(r"Image\Enemy\Eye.png")
        self.enemy_eye_surface=pygame.transform.scale(self.enemy_eye_surface,(160,160))

        #敌人攻击图片
        #火球
        self.enemy_weapon_0=pygame.image.load(r"Image\Skill\Enemy\0.png")
        self.enemy_weapon_0=pygame.transform.scale(self.enemy_weapon_0,(20,20))
        #和上面造型有一定区别的火球
        self.enemy_weapon_2=pygame.image.load(r"Image\Skill\Enemy\2.png")
        self.enemy_weapon_2=pygame.transform.scale(self.enemy_weapon_2,(30,30)) 
        #空心圆o
        self.enemy_weapon_1=pygame.image.load(r"Image\Skill\Enemy\1.png")
        self.enemy_weapon_1_list=[]
        #生成逐渐变大的圆o→O
        for i in range(100):
            self.enemy_weapon_1_list.append(pygame.transform.scale(self.enemy_weapon_1,(30+i*4,30+i*4)))

        #敌人属性

        #小战士
        #生命值
        self.enemy_warrior_health=120
        #攻击力
        self.enemy_warrior_attack_damage=0.2
        #移动速度
        self.enemy_warrior_move_speed=1
        #动作切换的间隔
        self.enemy_warrior_action_interval=0.2*self.fps
        #攻击的间隔
        self.enemy_warrior_attack_interval=1*self.fps
        #重量
        self.enemy_warrior_weight=8
        #击败后的得分
        self.enemy_warrior_score=1

        #小法师
        self.enemy_mage_health=80    
        self.enemy_mage_move_speed=1
        self.enemy_mage_attack_damage=5
        #攻击物的飞行速度
        self.enemy_mage_attack_speed=2
        self.enemy_mage_action_interval=2*self.fps
        self.enemy_mage_attack_interval=5*self.fps
        self.enemy_mage_weight=5
        self.enemy_mage_score=1

        #小炮兵
        self.enemy_artillery_health=300
        self.enemy_artillery_move_speed=1
        self.enemy_artillery_attack_damage=10
        #攻击物的飞行速度
        self.enemy_artillery_attack_speed=1        
        self.enemy_artillery_action_interval=3*self.fps
        self.enemy_artillery_attack_interval=6*self.fps
        self.enemy_artillery_weight=10
        self.enemy_artillery_score=2

        #大宿主
        self.enemy_overlord_health=2000
        self.enemy_overlord_move_speed=0
        #发射子弹攻击的伤害
        self.enemy_overlord_attack_damage_0=0.4
        #圆圈攻击的伤害
        self.enemy_overlord_attack_damage_1=0.4
        #发射子弹的飞行速度
        self.enemy_overlord_attack_speed=2
        self.enemy_overlord_action_interval=2*self.fps
        self.enemy_overlord_attack_interval=6*self.fps
        self.enemy_overlord_weight=1000
        self.enemy_overlord_score=5





