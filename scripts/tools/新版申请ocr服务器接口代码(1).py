import time
import os
import requests

url = r"http://172.29.9.116:9292/ocr/prediction"
img_path = r"C:\Users\9000\Desktop\emblem.jpg"
dir_path = r"C:\Users\9000\Desktop"
# for i in os.listdir(dir_path):
#     file_path = os.path.join(dir_path, i)
#     files = {"file": open(file_path, "rb")}
#     print(files)
#     print('--------')
#     start_time = time.time()
#     res = requests.post(url=url, files=files)
#     # print(res)
#     print(res.json())
#     end_time = time.time()
#     print((end_time - start_time)*1000)


files = {"file": open(img_path, "rb")}
print(files)
print('--------')
res = requests.post(url=url, files=files)
# print(res)
print(res.json())

