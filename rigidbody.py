'''
rigidbody模块负责物理模拟，不过这里只有一个模拟冲击的效果
Repel类根据传入的值移动受力物体
Repel类中update()方法负责更新受力物体的位置，以及力的衰减 
'''
class Repel():
    """冲击类，通过输入的推力等值移动物体"""
    def __init__(self,setting,victim,attack,rigidbody_list):
        #设置信息
        self.setting=setting
        #受力者
        self.victim=victim
        #施力物体
        self.attack=attack
        #受力者重量
        self.weight=victim.weight
        #摩擦系数
        self.friction=setting.friction
        #弹性系数
        self.rebound=self.setting.rebound
        #添加自身到刚体列表
        self.rigidbody_list=rigidbody_list      
        rigidbody_list.append(self)
        #被击退的朝向
        self.forward=-1 if attack.rect.centerx-victim.rect.centerx>=0 else 1
        #推力
        self.power=attack.power
        #布局
        self.rect=victim.rect

    def update(self):
        """更新力的大小和受力者的位置"""
        if self.power<=1:
            #力过小时删除自身
            self.rigidbody_list.remove(self)
            del self
        else:
            #计算力对受力者的影响
            posx=self.rect.centerx+(self.power/self.weight)*self.forward
            #如果到窗口边界则反弹，根据反弹系数减小力
            if(posx<0 or posx>self.setting.screen_width):
                self.power*=self.rebound
                self.forward*=-1
            #没有则施加移动效果，根据摩擦系数减小力
            else:
                self.rect.centerx=posx
                self.power-=self.friction*self.weight