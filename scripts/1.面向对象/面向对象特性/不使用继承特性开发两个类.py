'''
开发两个类：
    动物类
    狗类

    动物类特性：
        吃   喝   跑   睡
    狗类特性：
        吃   喝   跑   睡   汪汪叫
'''


class Animal:
    def eat(self):
        print('eat')

    def drink(self):
        print('drink')

    def run(self):
        print('run')

    def sleep(self):
        print('sleep')


class Dog:
    def eat(self):
        print('eat')

    def drink(self):
        print('drink')

    def run(self):
        print('run')

    def sleep(self):
        print('sleep')

    def bark(self):
        print('bark')


# 创建对象
# wangcai = Animal()

# 让旺财汪汪叫
wangcai = Dog()

wangcai.eat()
wangcai.drink()
wangcai.run()
wangcai.sleep()

'''
    当前动物类和狗类的四个方法重复，有冗余
'''
