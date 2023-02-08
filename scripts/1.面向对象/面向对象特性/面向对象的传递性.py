'''
继承的传递性
C类从B类继承，B类又从A类继承
那么C类就具有B类和A类的所有属性和方法
C-->B-->A
子类拥有父类以及父类的父类中封装的所有属性和方法
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


class Dog(Animal):
    def bark(self):
        print('bark')


class XiaoTianQuan(Dog):
    def fly(self):
        print('I can fly')


xtq = XiaoTianQuan()
xtq.fly()
xtq.bark()
xtq.eat()

'''
哮天犬类继承自狗类
狗类继承自动物类
哮天犬类是狗类的子类，狗类是动物类的子类
'''
