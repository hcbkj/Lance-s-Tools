# -*- coding: utf-8 -*-
# @Time    : 2023/4/10 13:44
import base64

file = r"C:\Users\9000\Desktop\51651996-BC83-4767-962B-C91A8F2BDBD1.txt"
x = open("xx.jpg", "wb")
with open(file) as f:
    secret = f.read()
    x.write(base64.b64decode(secret))
x.close()
