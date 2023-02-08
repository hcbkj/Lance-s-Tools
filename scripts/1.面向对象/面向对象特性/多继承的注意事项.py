class A:
    def test(self):
        print('A test')

    def demo(self):
        print('A demo')


class B:
    def test(self):
        print('B test')

    def demo(self):
        print('B demo')


class C(A, B):
    pass

class D(B, A):
    pass


# 创建C类对象
c = C()
# 继承顺序与同名函数的调用顺序有关
c.test()
c.demo()

d = D()
d.test()
d.demo()
# 若发现父类方法有重名，则尽量避免多继承

print(C.__mro__)
'''
C.__mro__
    查询mro搜索顺序
    class C     先在本类中查询有没有调用的方法
        class A
            class B     根据继承顺序在父类中查询
                class object    在基类中查询
                    报错
    从左至右
'''