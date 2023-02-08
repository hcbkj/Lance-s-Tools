"""
推导式：
    简化语法
    语法：
        1. 列表推导式    [数据  for循环  if判断]
        2. 集合推导式    {数据  for循环  if判断}
        3. 字典推导式    {k:v  for循环  if判断}

    不要滥用推导式
    (数据  for循环  if判断)   --->    这个不是元组推导式,根本就没有元组推导式,这玩意叫做 *生成器表达式*

"""

# lst = []
# for i in range(10):
#     lst.append(i)
#
# print(lst)
# # 改写推导式
# lst = [i for i in range(10)]
# print(lst)

# *列表推导式*
# # 1. 请创建一个列表[1,3,5,7,9]
# lst = [i for i in range(1, 10, 2)]
# lst = [i for i in range(10) if i % 2 == 1]
# print(lst)

# # 2. 生成50件衣服
# lst = [f'衣服{i}' for i in range(50)]
# print(lst)

# # 3. 将如下列表中的字母全部换成大写
# lst1 = ['allen', 'tony', 'tom']
# lst2 = [item.upper() for item in lst1]
# print(lst2)

# # *集合推导式*
# s = {i for i in range(10)}
# print(s)

# *字典推导式*
# 请将下列的列表修改成字典,要求: 索引做为key, 数据作为value
lst = ['春', '夏', '秋', '冬']
dic = {i: lst[i] for i in range(len(lst))}
print(dic)


