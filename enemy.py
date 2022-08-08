import pygame
import random
import effect
from pygame.sprite import Sprite


class Enemy(Sprite):
    """敌人的基类"""
    def __init__(self,setting,screen,surface,generate_point,health,speed,action_interval,attack_interval,weight,score):
        super().__init__()
        #基本变量
        self.screen=screen
        self.setting=setting
        self.screen_rect=screen.get_rect()
        #移动速度
        self.speed=speed
        #重设移动方向间隔
        self.action_interval=action_interval
        #攻击间隔
        self.attack_interval=attack_interval
        #重量
        self.weight=weight
        #死亡后玩家获取的得分
        self.score=score
        #选择一名玩家人物作为目标
        if setting.player_1!=None and setting.player_2!=None:
            target=[setting.player_1,setting.player_2]
            self.player=random.choice(target)
        elif setting.player_1!=None: 
            self.player=setting.player_1
        else:
            self.player=setting.player_2
        #以一个随机时刻开始移动和攻击计时器
        self.action_timer=random.randint(0,int(action_interval))
        self.attack_timer=random.randint(0,int(attack_interval))
        #是否还存活
        self.isalive=True
        #是否是近战
        self.ismelee=False
        #近战攻击生成次数
        self.melee_count=1
        #朝向(-1朝左，1朝右)
        self.forward=-1
        #图像
        self.surface=surface
        self.surface_flip=pygame.transform.flip(self.surface,True,False)
        #布局
        self.rect=self.surface.get_rect()
        #出生位置
        self.rect.center=generate_point
        #生命属性
        self.max_health=health
        self.health=self.max_health
        #生命条布局
        self.health_rect_background=pygame.Rect(self.rect.centerx-10,self.rect.centery-30,50,20)
        self.health_rect=pygame.Rect(self.rect.centerx-10,self.rect.centery-30,self.health/self.max_health*50,20)
        #移动方向
        self.direction_x=0.0
        self.direction_y=0.0

    def update(self):
        """更新状态"""
        self.flip()
        self.auto_move()
        self.update_health_ui()

    def draw(self):
        """绘制图像"""
        if self.forward==-1:
            self.screen.blit(self.surface,self.rect)
        else:
            self.screen.blit(self.surface_flip,self.rect)
        #绘制生命条
        pygame.draw.rect(self.screen,(200,200,200),self.health_rect_background)
        pygame.draw.rect(self.screen,(30,30,30),self.health_rect)
  
    def flip(self):
        """更新当前朝向"""
        if (self.rect.centerx-self.player.rect.centerx)>=0:
            self.forward=-1
        else:
            self.forward=1

    def update_health_ui(self,x=-25,y=-40,width=50,height=10):
        """更新血量ui"""
        self.health_rect_background=pygame.Rect(self.rect.centerx+x,self.rect.centery+y,width,height)
        self.health_rect=pygame.Rect(self.rect.centerx+x,self.rect.centery+y,self.health/self.max_health*width,height)

    def auto_move(self):
        """自主更新位置"""
        pass

class Mage(Enemy):
    """小法师"""
    def __init__(self,setting,screen):
        super().__init__(setting,screen,setting.enemy_mage_surface,setting.enemy_genrate_point,
                         setting.enemy_mage_health,setting.enemy_mage_move_speed,setting.enemy_mage_action_interval,
                         setting.enemy_mage_attack_interval,setting.enemy_mage_weight,setting.enemy_mage_score)
        self.rect.centery+=random.randint(-150,150)
    
    def auto_move(self):
        """上下随机移动"""
        if(self.action_timer<=0):
            self.direction_x=0
            self.direction_y=random.uniform(-2,2)
            #重置计时器
            self.action_timer=self.action_interval
        elif(self.action_timer%2==0):
            #移动不能超出窗口
            if self.rect.left > 0 and self.direction_x<0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.right < self.screen_rect.right and self.direction_x>0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.bottom < self.screen_rect.bottom and self.direction_y>0:
                self.rect.centery+=self.direction_y*self.speed
            if self.rect.top > 0 and self.direction_y<0:
                self.rect.centery+=self.direction_y*self.speed
            self.action_timer-=1
        else:
            self.action_timer-=1

    def auto_attack(self):
        """返回攻击物"""
        return effect.EnemyFireBall(self.setting,self.screen,self.player,self)

class Warrior(Enemy):
    """小战士"""
    def __init__(self,setting,screen):
        super().__init__(setting,screen,setting.enemy_warrior_surface,setting.enemy_genrate_point,
                         setting.enemy_warrior_health,setting.enemy_warrior_move_speed,setting.enemy_warrior_action_interval,
                         setting.enemy_warrior_attack_interval,setting.enemy_warrior_weight,setting.enemy_warrior_score)
        self.ismelee=True
        self.rect.centerx+=random.randint(-100,0)
        self.rect.centery+=random.randint(-120,120)
       

    def auto_move(self):
        """朝向目标玩家移动"""
        if(self.action_timer<=0):
            if self.player.rect.centerx-self.rect.centerx<=0:
                self.direction_x=random.uniform(-2,-1)
            else:
                self.direction_x=random.uniform(1,2)

            if self.player.rect.centery-self.rect.centery<=0:
                self.direction_y=random.uniform(-2,-1)
            else:
                self.direction_y=random.uniform(1,2)
            #重置计时器
            self.action_timer=self.action_interval
        elif(self.action_timer%2==0):
            #移动不能超出窗口
            if self.rect.left > 0 and self.direction_x<0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.right < self.screen_rect.right and self.direction_x>0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.bottom < self.screen_rect.bottom and self.direction_y>0:
                self.rect.centery+=self.direction_y*self.speed
            if self.rect.top > 0 and self.direction_y<0:
                self.rect.centery+=self.direction_y*self.speed
            self.action_timer-=1
        else:
            self.action_timer-=1

    def auto_attack(self):
        return effect.EnemyCollide(self.setting,self.screen,self.player,self)


class Artillery(Enemy):
    """小炮兵"""
    def __init__(self,setting,screen):
        super().__init__(setting,screen,setting.enemy_artillery_surface,setting.enemy_genrate_point,
                         setting.enemy_artillery_health,setting.enemy_artillery_move_speed,setting.enemy_artillery_action_interval,
                         setting.enemy_artillery_attack_interval,setting.enemy_artillery_weight,setting.enemy_artillery_score)
        self.rect.centery+=random.randint(-200,200)
    
    def auto_move(self):
        """远离玩家移动"""
        if(self.action_timer<=0):
            if self.player.rect.centerx-self.rect.centerx<=0:
                self.direction_x=random.uniform(1,2)
            else:
                self.direction_x=random.uniform(-2,-1)
                
            if self.player.rect.centery-self.rect.centery<=0:
                self.direction_y=random.uniform(1,2)             
            else:
                self.direction_y=random.uniform(-2,-1)
            #重置计时器
            self.action_timer=self.action_interval
        elif(self.action_timer%2==0):
            #移动不能超出窗口
            if self.rect.left > 0 and self.direction_x<0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.right < self.screen_rect.right and self.direction_x>0:
                self.rect.centerx+=self.direction_x*self.speed
            if self.rect.bottom < self.screen_rect.bottom and self.direction_y>0:
                self.rect.centery+=self.direction_y*self.speed
            if self.rect.top > 0 and self.direction_y<0:
                self.rect.centery+=self.direction_y*self.speed
            self.action_timer-=1
        else:
            self.action_timer-=1

    def auto_attack(self):
        return effect.EnemyTargetBall(self.setting,self.screen,self.player,self)

class Overlord(Enemy):
    """大宿主"""
    def __init__(self,setting,screen):
        super().__init__(setting,screen,setting.enemy_overlord_surface,setting.enemy_genrate_point,
                         setting.enemy_overlord_health,setting.enemy_overlord_move_speed,setting.enemy_overlord_action_interval,
                         setting.enemy_overlord_attack_interval,setting.enemy_overlord_weight,setting.enemy_overlord_score)
        self.rect.centerx-=random.randint(0,300)
        #眼睛的图像
        self.eye_surface=setting.enemy_eye_surface        
        self.eye_rect=self.eye_surface.get_rect()
        self.eye_rect.center=self.rect.center
        #半径的平方
        self.radius=12**2

    def eye_move(self):
        """眼睛移动向玩家"""
        move_x=0
        move_y=0
        if self.player.rect.centerx-self.rect.centerx>=0:
            move_x+=1
        else:
            move_x-=1               
        if self.player.rect.centery-self.rect.centery>=0:
            move_y+=1
        else:
            move_y-=1
        #计算和圆心的距离
        delta_x=((self.eye_rect.centerx+move_x)-self.rect.centerx)
        delta_y=((self.eye_rect.centery+move_y)-self.rect.centery)
        #如果超出半径，则往回移动，否则朝目标移动
        if (delta_x**2+delta_y**2)<self.radius:
            self.eye_rect.centerx+=move_x
            self.eye_rect.centery+=move_y
        else:
            if delta_x<=0:
                self.eye_rect.centerx+=1
            else:
                self.eye_rect.centerx-=1
            if delta_y<=0:
                self.eye_rect.centery+=1
            else:
                self.eye_rect.centery-=1


    def update(self):
        """更新状态"""
        self.flip()
        self.eye_move()
        self.update_health_ui(y=-100,x=-50,width=100,height=15)
   

    def auto_attack(self):
        """随机选择一种攻击返回"""
        i=random.randint(0,1)
        if i==0:          
            return effect.EnemyRingAttack(self.setting,self.screen,self.player,self)
        else:
            return effect.EnemyShoot(self.setting,self.screen,self.player,self)


    def draw(self):
        """绘制自身和眼睛"""
        super().draw()
        self.screen.blit(self.eye_surface,self.eye_rect)


        
       