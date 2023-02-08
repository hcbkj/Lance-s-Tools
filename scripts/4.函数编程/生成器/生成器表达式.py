"""
生成器表达式: -->一次性的
    (数据  for循环  if判断)
    代码调优的时候比较好用


"""
gen = (i**2 for i in range(10))
# print(gen)      # 生成器

# print(gen.__next__())
# print(gen.__next__())
# print(gen.__next__())
# print(gen.__next__())

for item in gen:
    print(item)

lst = list(gen)     # 生成器表达式也是一次性的！ 当for循环拿空迭代器中的数据时，再次输出列表lst为空列表
print(lst)

# # list()、dict()等，实质是一个循环迭代
# # 例如：
# s = list("你好啊！")    # list() => for =>next()
# print(s)

