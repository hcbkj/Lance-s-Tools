'''
Python是一门动态语言，即“在运行中可以改变其结构的语言，例如新的函数、对象、甚至代码都可以被引进，已有的函数也可以被删除后是其他结构上的变化。
动态语言非常灵活，目前流行的Python和Javascript都是动态语言，除此之外如PHP、Ruby等也都属于动态语言，而C、C++等语言则不属于动态语言”

在Python中，我们可以动态为对象添加属性，这是Python作为动态类型语言的一项特权，代码如下所示。需要提醒大家的是，对象的方
法其实本质上也是对象的属性，如果给对象发送一个无法接收的消息，引发的异常仍然是AttributeError

'''


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 如果当前的类不允许开发者进行动态属性的添加,可以使用Python的魔术方法__slots__确定类中属性
    __slots__ = ('name', 'age')


stu = Student('zhangshan', 20)

# 想要在不修改当前类代码的情况下，去添加一个属性
stu.sex = "男"
print(stu.name, stu.age, stu.sex)
