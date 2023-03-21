# -*- coding: utf-8 -*-
# @Time    : 2023/3/16 8:38
import re
text = 'a.b.c.d.e.f.g'

nums = ['1', '2', '3', '4', '5', '6'].__iter__()  # nums = '123456'.__iter__()
print(re.sub(r"\.", string=text, repl=lambda x: next(nums)))

#
# nums = {'a': "alpha", 'b': "beta", 'c': "gamma", 'd': "delta"}
# print(re.sub(r"[a-z]", string=text, repl=lambda x: nums[x.group()]))
