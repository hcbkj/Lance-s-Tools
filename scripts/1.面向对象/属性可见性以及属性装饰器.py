class Student:
    def __init__(self, name, age):
        # 创建私有属性
        self.__name = name
        self.__age = age

    # 获取私有属性
    @property
    def name(self):
        return self.__name

    # 修改私有属性
    @name.setter
    def name(self, name):
        self.__name = name or ' 无名氏'

    # 获取私有属性
    def age(self):
        return self.__age

    def study(self, course_name):
        print(f'{self.__name}正在学习{course_name}')


stu = Student("zhangshan", 18)
# stu.study('python')
print(stu.age, stu.name)
stu.name = ''
print(stu.name)
# stu.age = 30
# print(stu.age)
