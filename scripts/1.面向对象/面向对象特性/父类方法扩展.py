'''
对父类方法进行扩展
如果在开发中，子类的方法实现中包含父类的方法实现
父类原本封装的方法实现是子类方法的一部分 ,就可以使用扩展的方式
1.在子类中重写父类的方法
2.在需要的位置使用super（）.父类方法来调用父类方法的执行
3.代码其他的位置针对子类的需求，编写子类特有的代码实现

关于super
在Python中super是一个特殊的类
super（）就是使用super类创建出来的对象
最常使用的场景就是在重写父类方法时，调用在父类中封装的方法实现

在python2中，调用父类方法的方式为：
父类名.方法(self)
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

    def bark(self):
        print('bark like god')

        # 如果需要在当前方法中调用父类方法
        # 使用super()方法
        # super()也是一个对象
        super().bark()

        # # 在python2中，调用父类方法的方式为：(不推荐使用)
        # Dog.bark(self)
        # # 在当前代码中通过子类.方法的方式去调用，会出现递归循环 死循环
        # XiaoTianQuan.bark(self)

        # 当前子类方法进行拓展
        print('test')


xtq = XiaoTianQuan()
xtq.bark()

