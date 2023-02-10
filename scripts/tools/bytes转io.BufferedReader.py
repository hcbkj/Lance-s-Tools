# -*- coding: utf-8 -*-
# @Time    : 2022/12/28 16:42

import io

# io.BufferedReader(z)
# z.read()

x = open(r"C:\Users\9000\Desktop\emblem.jpg", "rb")
y = x.read()
print(type(y))
z = io.BytesIO(y)
b_br = io.BufferedReader(z)
print(type(b_br))
