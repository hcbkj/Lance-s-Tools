# -*- coding: utf-8 -*-
# @Time    : 2023/3/22 10:50

import docx

# 打开文档，并读取其中的所有段落内容
doc = docx.Document('test.docx')
text = '\n'.join([para.text for para in doc.paragraphs])

# 尝试自动检测编码方式
encoding_list = ['utf-8', 'gbk', 'big5', 'gb18030']
for encoding in encoding_list:
    try:
        decoded_text = text.encode(encoding).decode(encoding)
        print(f"Detected encoding: {encoding}")
        break
    except UnicodeDecodeError:
        pass
else:
    print("Unknown encoding.")

