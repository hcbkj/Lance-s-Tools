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
        print('eat123')

    def drink(self):
        print('drink123')

    def run(self):
        print('run123')

    def sleep(self):
        print('sleep123')


class Dog(Animal):
    # def eat(self):
    #     print('eat')
    #
    # def drink(self):
    #     print('drink')
    #
    # def run(self):
    #     print('run')
    #
    # def sleep(self):
    #     print('sleep')

    def bark(self):
        print('bark')


# 创建对象
wangcai = Dog()
wangcai.eat()
wangcai.drink()
wangcai.run()
wangcai.sleep()
wangcai.bark()

'''
专业术语
Dog类是Animal类的子类，Animal类是Dog类的父类，，Dog类从Animal类继承
Dog类是Animat类的派生类，Animal类是Dog类的基类，Dog类从Animal类派生
'''

