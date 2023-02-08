'''
方法的重写
子类拥有父类的所有方法和属性
子类继承自父类，可以直接享受父类中已经封装好的方法，不需要再次开发

应用场景
当父类的方法实现不能满足子类需求时，可以对方法进行重写（override）
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

    # 需要修改哮天犬的bark方法，方法重写
    def bark(self):
        print('bark like god')


xtq = XiaoTianQuan()
xtq.fly()
xtq.bark()
