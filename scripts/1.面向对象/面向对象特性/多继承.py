class A:
    def test(self):
        print('test方法')


class B:
    def demo(self):
        print('demo方法')


class C(A, B):
    pass


c = C()
c.test()
c.demo()

'''
在python中面向对象是支持多个类进行继承的
    子类同时具有父类中的所有方法和所有属性
A B
'''
