# 子类对象可以通过父类的公有方法间接访问到私有属性或私有方法

class A:
    def __init__(self):
        self.num_1 = 100
        self.__num_2 = 200

    # 私有方法
    def __test(self):
        print(f'公有属性和私有属性的值：{self.num_1}, {self.__num_2}')

    # 公有方法
    def test(self):
        print(f'父类中的公有方法输出私有属性:{self.__num_2}')

        # 在公有方法中调用私有方法
        self.__test()


# 创建的新类要继承自类A
class B(A):
    # 公有方法
    def demo(self):
        # 1.在子类方法中访问父类的公有属性
        print(f'子类方法输出父类的公有属性：{self.num_1}')
        # 2.在子类中调用父类的公有方法来输出私有属性
        self.test()


b = B()
b.demo()
