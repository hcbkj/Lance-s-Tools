class Dog:
    def __init__(self, name):
        self.name = name

    def game(self):
        print('%s 正在玩耍' % self.name)


class XiaoTianDog(Dog):
    # 子类继承父类的时候，继承其所以属性和方法
    def game(self):
        print('%s 在天上玩耍' % self.name)


class Person(object):
    def __init__(self, name):
        self.name = name

    def game_with_dog(self, dog):
        dog.game()
        print('%s 和 %s 在一起愉快的玩耍。' % (self.name, dog.name))


# d = Dog('汪汪')
d = XiaoTianDog('飞天汪汪')
p = Person('张三')
p.game_with_dog(d)

'''
多态的运行情况
    我们在调用子类中的同名方法时 输出的值不一样
    基于继承和重写
'''