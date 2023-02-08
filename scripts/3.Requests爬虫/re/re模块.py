import re

# lst = re.findall(r"\d+", "我的电话号是：10086， 我同学的电话是：10010")
# print(lst)

# it = re.finditer(r"\d+", "我的电话号是：10086， 我同学的电话是：10010")
# for i in it:
#     print(i.group())

# # search返回的结果是match对象, 拿数据需要.group(), search找到一个结果就返回, 全文匹配
# s = re.search(r"\d+", "我的电话号是：10086， 我同学的电话是：10010")
# print(s.group())

# # match是从头开始匹配 相当于r"^\d+"了
# s = re.match(r"\d+", "我的电话号是：10086， 我同学的电话是：10010")
# print(s.group())

# # 预加载正则表达式, 优点是可以反复使用
# obj = re.compile(r"\d+")

# ret = obj.finditer("我的电话号是：10086， 我同学的电话是：10010")
# for i in ret:
#     print(i.group())

s = """
 <div class='⻄游记'><span id='1'>猴</span></div>
 <div class='三国'><span id='2'>谋略</span></div>
 <div class='金瓶梅'><span id='3'>风俗</span></div>
 <div class='西厢记'><span id='4'>悲情</span></div>
 <div class='红楼梦'><span id='5'>爱情</span></div>
"""

# (?P<分组名字>正则) 可以单独从正则匹配的内容中进一步获取内容
obj = re.compile(r"<div class='.*?'><span id='(?P<id>\d+)'>(?P<wahaha>.*?)</span></div>", re.S)      # re.S: 通配符，让.能匹配换行符

result = obj.finditer(s)
for it in result:
    print(f"{it.group('id')}:{it.group('wahaha')}")


