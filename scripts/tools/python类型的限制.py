# -*- coding: utf-8 -*-
# @Time    : 2022/9/1 14:36

# name: str 是输入参数的类型被预期为str     -> str 是返回值的预期类型为str
def gets(name: str) -> str:
    return 'Hello' + name


# a = gets("1")
# print(a)

def appends(lst=[]):
    lst.append(1)
    print(lst)
    # return lst


appends()
appends()
appends()
