"""
部分内置函数
    zip():  可以把多个可迭代内容合并
    locals(): 函数会以字典的类型返回当前位置的全部局部变量
    globals(): 函数以字典形式返回全局变量
    sorted(): 排序, sorted(__iterable, key, reverse) 可迭代对象排序, key是自定义排序规则, reverse=True 是倒序
    filter(): 筛选, filter(function, __iterable) 根据自定义筛选函数, 对可迭代对象进行筛选, 通过函数func结果确定元素是否保留
    map():  映射, map(function, __iterable), 函数func的结果就作为最终答案进行保留
"""

# # zip函数
# # 把每个列表里面对应的数据放在一起
# lst1 = ['赵本山', '范伟', '苏有朋']
# lst2 = [60, 55, 48]
# lst3 = ["卖拐", "耳朵大有福", "情深深雨蒙蒙"]

# result = []
# for i in range(len(lst1)):
#     first = lst1[i]
#     second = lst2[i]
#     third = lst3[i]
#     result.append((first, second, third))
#
# print(result)

# # zip函数
# result = zip(lst1, lst2, lst3)
# # print(result)       # <zip object at 0x0000015A94B89440>

# print(dir(result))
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
# '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__',
# '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
# 可迭代

# for item in result:
#     print(item)

# lst = list(result)
# print(lst)

# # locals()和globals()
# a = 188
# print(locals())     # 此时locals()被写在了全局作用域范围内, 此时看到的就是全局作用域中的内容

# def func():
#     a = 188
#     print(locals())   # 此时locals()被写在局部作用域中, 看到的就是局部作用域的内容
#
# func()  # {'a': 188}


# b = 188
# print(globals())

# def func():
#     b = 188
#     print(globals())       # 不论globals()写在哪个作用域中,返回的都是全局变量的内容
#
# func()

# # 排序函数
# lst = [1, 15, 2, 345, 34, 32, 3]
#
# s = sorted(lst, reverse=True)
# print(s)

# lst = ['秋', '嘎子', '刀锋战士陈二狗', '泽瑞拉']
#
# # def func(item):     # item对应的就是列表中的每一项数据
# #     return len(item)
# # func = lambda x: len(x)
#
# s = sorted(lst, key=lambda x: len(x))       # key部分输入排序函数, 注意func不加括号()
# print(s)

# lst = [
#     {'id': 1, 'name': '周润发', 'age': 68, 'salary': 50000},
#     {'id': 2, 'name': '周形成', 'age': 21, 'salary': 12400},
#     {'id': 3, 'name': '周大福', 'age': 24, 'salary': 3444},
#     {'id': 4, 'name': '周生死', 'age': 34, 'salary': 5020},
#     {'id': 5, 'name': '周伯通', 'age': 45, 'salary': 8300},
# ]

# # 1. 根据每个人的年龄排序
# s = sorted(lst, key=lambda dict: dict['age'])
# print(s)

# # 2. 根据每个人的工资排序, 要求从大到小
# s = sorted(lst, key=lambda dict: dict['salary'], reverse=True)
# print(s)


# # filter()筛选
# lst = ["张三", "李四", "张无忌", "王五", "张天师"]
# f = filter(lambda x: not x.startswith("张"), lst)
# print(list(f))


# map()
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# # 列表推导式实现列表各元素求平方
# result = [item * item for item in lst]
# print(result)

# map()函数
r = map(lambda x: x * x, lst)
print(list(r))

