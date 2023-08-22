# import cv2
# import numpy as np
#
#
# def get_distance(background_img_path, slider_img_path):
#     # 读取背景图和滑块图
#     background_img = cv2.imread(background_img_path)
#     slider_img = cv2.imread(slider_img_path)
#
#     # 将滑块图片转换为灰度图
#     slider_gray = cv2.cvtColor(slider_img, cv2.COLOR_BGR2GRAY)
#     background_gray = cv2.cvtColor(background_img, cv2.COLOR_BGR2GRAY)
#
#     # 获取滑块图的宽度和高度
#     slider_height, slider_width = slider_gray.shape[:2]
#
#     # 使用模板匹配方法获取滑块位置
#     result = cv2.matchTemplate(background_gray, slider_gray, cv2.TM_CCORR_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     loc = max_loc
#
#     # 计算滑块中心点的坐标
#     slider_center_x = loc[0] + slider_width / 2
#     slider_center_y = loc[1] + slider_height / 2
#
#     # 找到滑块图中的缺口位置
#     contours, _ = cv2.findContours(slider_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contour = max(contours, key=cv2.contourArea)
#     x, y, w, h = cv2.boundingRect(contour)
#     gap_position = x
#
#     # 计算滑块中心点到缺口位置的距离
#     distance = gap_position - slider_center_x
#
#     return -distance
#
bg = r"C:\Users\9000\Desktop\yzm\bg.jpg"
hk = r"C:\Users\9000\Desktop\yzm\hk.png"
# print(get_distance(bg, hk))

import ddddocr

det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

with open(hk, 'rb') as f:
    target_bytes = f.read()

with open(bg, 'rb') as f:
    background_bytes = f.read()

res = det.slide_match(target_bytes, background_bytes, simple_target=True)
print(res)
distance = (res['target'][2] - res['target'][0])/2 + res['target'][0]
print(distance)