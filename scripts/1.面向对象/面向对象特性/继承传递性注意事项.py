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


class Cat(Animal):
    def catch(self):
        print('抓老鼠')


# 定义了一个猫类这个猫类继承自动物类
# 自身实现了一个方法抓老鼠
# 我现在通过xtq对象可不可以调用猫类的方法
xtq = XiaoTianQuan()
xtq.fly()
xtq.bark()
xtq.eat()

# 当前的哮天犬对象并没有和猫类进行绑定继承
# 一定要分清当前类的继承关系
# xtq.catch()
