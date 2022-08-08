# HappyCollision-pygame

#### 介绍
一个主要使用pygame库开发的简单2d小人对对碰游戏。
提供单/双人游戏，PVE和PVP模式。
![游戏示例](https://foruda.gitee.com/images/1659952320557156542/startgame.gif)

#### 软件架构
##### 开发和测试环境 
- Python 3.8(64-bit)
- Pygame 2.1.2
- PyInstaller 5.1

##### 模块介绍

1. main.py 程序入口，进行游戏内容的初始化及主循环。
2. game_event.py 处理输入事件，生成和更新物体状态的方法。
3. live.py 玩家操控人物的属性和行为。
4. enemy.py 游戏中的敌人的属性和行为。
5. gameui.py 游戏过程中的信息的显示。
6. startupui.py 游戏启动界面的按钮等组件的显示。
7. rigidbody.py 模拟物体碰撞产生的位移。
8. effect.py 包含人物和敌人产生的攻击物体的更新和显示。
9. setting.py 从外部加载图片，汇总游戏中各类属性的定义。

![程序模块组成](https://foruda.gitee.com/images/1659953945317055704/mod.jpeg)

1. 运行需要的外部资源包括Image文件夹下的图片，以及游戏控制介绍文本HowToPlay.txt。
2. 此外第一次运行会在目录下生成一个用于存储游戏记录的GameRecord.csv文件。


#### 安装教程
1.  克隆库到本地可从main.py运行，环境需要Python3以上和pygame库。
2.  发行版解压后可直接在windows上运行。
3.  pygame库可以通过pip install pygame命令安装。

#### 存在的问题

1. 初学者开发，代码命名存在不规范的情况，添加了中文注释。
2. 游戏的数值填的很糟糕，游戏开始界面可以选择关闭技能冷却。


#### 作者
- https://github.com/CNZHANGZHANG

