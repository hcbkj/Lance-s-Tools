import io
import os
import cv2
import json
import time
import base64
import requests
import numpy as np
import matplotlib.pyplot as plt

from paddle_serving_app.reader import *
from paddle_serving_client import HttpClient
from django.core.files.uploadedfile import UploadedFile

from core.config import API_AUTH_TOKEN
from rpa.settings import API_URL
from api.models import ApiComparison
from api.enum.IdCardImage import IdCardImageClass

from PIL import Image
from io import BytesIO
from typing import Tuple


def get_img(data: bytes) -> str:
    """
    base64读图片
    :param data: 字节流图片
    :return: encodestr的图片
    """
    try:
        encodestr = str(base64.b64encode(data), 'utf-8')
    except TypeError:
        encodestr = base64.b64encode(data)
    return encodestr


def bytes2cv2(img_bytes: str or bytes):
    """
    字节流图片转换为cv2格式
    :param img_bytes: 字节流图片
    :return: cv2格式的图片img_data
    """
    img_buffer_numpy = np.frombuffer(img_bytes, dtype=np.uint8)  # 将图片字节码bytes  转换成一维的numpy数组到缓存中
    img_data = cv2.imdecode(img_buffer_numpy, 1)  # 从指定的内存缓存中读取一维numpy数据，并把数据转换(解码)成图像矩阵格式

    return img_data


def image_point(x: int, y: int) -> Tuple[int, int]:
    """
    处理图片分辨率，要求resize时是32的倍数
    :param x: 分辨率的横坐标
    :param y: 分辨率的纵坐标
    :return: 处理后的分辨率
    """

    # if not (z := x % 32) == 0:
    #     x = (x // 32 + 1) * 32 if z >= 16 else x // 32 * 32
    # if not (z := y % 32) == 0:
    #     y = (y // 32 + 1) * 32 if z >= 16 else y // 32 * 32
    # tuples = (x, y)
    #
    # if max(x, y) > 640:
    #     proportion = y / x
    #     tuples = (int(640 // proportion), 640) if proportion > 0 else (640, int(640 * proportion))

    # 新模型的输入限制暂为强制输入640*640的精度
    tuples = (640, 640)
    return tuples


def image_result_duplication(data: dict):
    """
    对于身份证识别的新模型,部分图片会存在识别出相同类别出现多条识别结果的情况,当前方法即是对结果进行去重,保留识别相似度最高的数据.
    :param data: 模型返回结果中的result['value']部分,为一个列表,列表内每一条数据由6个部分构成,分别是类别、相似度、识别区域的四个点坐标
    :return: 去重后的结果
    """
    sets = {}
    values = []
    for i in data:
        if not sets.get(i[0], None):
            sets[i[0]] = i
        else:
            if sets[i[0]][1] < i[1]:
                sets[i[0]] = i

    for i in sets.values():
        values.append(i)
    return values


def image_rotate(box_list: list, flag_list: list, img, cls: IdCardImageClass):
    """
    根据box和image坐标信息，判断并旋转图片至正立
    :param box_list:存放有box坐标的列表，坐标在列表的第3-6项
    :param flag_list:存放有image坐标的列表，坐标在列表的第3-6项
    :return:旋转后的图片（cv2格式）
    """
    box_xmin, box_ymin, box_xmax, box_ymax = box_list[2], box_list[3], box_list[4], box_list[5]
    flag_xmin, flag_ymin = flag_list[2], flag_list[3]

    # 坐标原点
    x_mid = (box_xmax - box_xmin) / 2 + box_xmin
    y_mid = (box_ymax - box_ymin) / 2 + box_ymin

    # location是人像/国徽相对于图片中点的坐标系处于第几象限
    location = 1
    if flag_xmin > x_mid and flag_ymin < y_mid:
        location = 1
    elif flag_xmin < x_mid and flag_ymin < y_mid:
        location = 2
    elif flag_xmin < x_mid and flag_ymin > y_mid:
        location = 3
    elif flag_xmin > x_mid and flag_ymin > y_mid:
        location = 4

    if cls == IdCardImageClass.FACE:
        # 人像面
        if location:
            # 如果n>=4, 就取余数来确定旋转的度数
            # 正数代表逆时针旋转，负数代表顺时针旋转
            data = np.rot90(img, -(location - 1))
            return data
    else:
        # 国徽面
        if location:
            data = np.rot90(img, -(location - 2))
            return data


def PIL_to_bytes(im):
    """
    PIL转二进制
    :param im: PIL图像，PIL.Image
    :return: bytes图像
    """
    bytesIO = BytesIO()
    try:
        im.save(bytesIO, format='JPEG')
    except:
        im.save(bytesIO, format='PNG')
    # 转二进制
    return bytesIO.getvalue()


def format_idcard_ocr_result(ocr: dict, cls: IdCardImageClass) -> dict:
    for item in ocr:
        ocr[item] = ocr[item].replace(' ', '').replace('\n', '')
    if cls == IdCardImageClass.FACE:
        for item in ocr:
            if item == 'name':
                ocr[item] = ocr[item].strip('姓').strip('名')
            elif item == 'sex':
                ocr[item] = ocr[item].strip('性').strip('别')
            elif item == 'nationality':
                ocr[item] = ocr[item].strip('民').strip('族')
            elif item == 'birth':
                ocr[item] = ocr[item].strip('出').strip('生').replace('年', '').replace('月', '').strip('日')
            elif item == 'address':
                ocr[item] = ocr[item].strip('住').strip('址')
            elif item == 'num':
                ocr[item] = ocr[item].strip('公').strip('民').strip('身').strip('份').strip('号').strip('码')
    else:
        for item in ocr:
            if item == 'issue':
                ocr[item] = ocr[item].strip('签').strip('发').strip('机').strip('关')
            elif item == 'date':
                ocr[item] = ocr[item].strip('有').strip('效').strip('期').strip('限').replace('.', '')
    return ocr


class IdCardOcr(object):

    def classify(self, image: UploadedFile) -> IdCardImageClass:
        """
        分类
        :param image:图片
        :return:分类结果,是枚举类型的分类结果
        """
        url = API_URL['classify']
        resp = requests.post(url=url, files={'file': image})
        result = resp.json()['result']

        # 人像面、国徽面相似度
        face_like = result[0]
        emblem_like = result[1]
        # print(face_like, emblem_like)
        if face_like > emblem_like:
            return IdCardImageClass.FACE
        else:
            return IdCardImageClass.EMBLEM

    def dispose_idcard_img(self, box_list, image_list, im, img, cls, client):
        """
        对于身份证图片的处理部分,旋转、分割
        :param box_list:
        :param image_list:
        :param im:
        :param img:原图
        :param cls:
        :return: result
        """
        result = {cls: {}}

        # im是旋转后的图片
        im = image_rotate(box_list, image_list, im, cls)

        # 调整shape来进行旋转后的格式处理
        # 对旋转后的图片进行格式处理
        # shape_1st, shape_2nd, shape_3th = im.shape
        print(im.shape)
        re_tran = Sequential([
            # Transpose((im.shape.index(shape_1st), im.shape.index(shape_2nd), im.shape.index(shape_3th)))
            Transpose((1, 2, 0)),
        ])
        im = re_tran(im)
        print(im.shape)

        resize_img = Sequential([
            # resize中输入参数为第一项图片横坐标，第二项图片纵坐标
            Resize((640, 640), interpolation=cv2.INTER_LINEAR)
        ])
        im = resize_img(im)
        print(im.shape)

        fetch_map = client.predict(
            feed={
                "image": im,
                # "im_shape": np.array(list(im.shape[1:])).reshape(-1),
                "scale_factor": np.array([1.0, 1.0]).reshape(-1),
            },
            fetch=["multiclass_nms3_0.tmp_0"],
            batch=False
        )
        try:
            value_mid_2nd = fetch_map.outputs[0].tensor[0]
        except:
            raise RuntimeError('crop:旋转后图片无返回结果')
        value_shape_2nd = value_mid_2nd.shape
        value = np.array(list(value_mid_2nd.float_data), dtype="float32").reshape(value_shape_2nd)
        value = value[(value[:, 1] > 0.4) & (value[:, 0] > -1), :]

        # 通过PIL的方法进行图片的裁剪，并将其传给extract来进行处理
        # cv2转PIL
        pil_img = Image.fromarray(img)
        image_part = []
        for part in value:
            # print(part)
            cropped = pil_img.crop((part[2], part[3], part[4], part[5]))  # (left, upper, right, lower)
            part_img = PIL_to_bytes(cropped)
            image_part.append((part[0], part_img))

        result[cls]['value'] = value.tolist()
        result[cls]['image'] = image_part[0][1]
        result[cls]['image_part'] = image_part
        return result

    def crop(self, image: bytes):
        """
        检测,处理图片
        :param image: 图片
        :return: result: 接口处理结果包含身份证图像处理后的value列表(包含身份证图片标注各部分的类别、相似度、标注区域的四点坐标)
        """
        # 根据分类结果处理数据

        # 客户端请求方式
        img = bytes2cv2(image)
        # 图片分辨率，要求resize时是32的倍数，通过im.shape取出的元组中第一项是图片纵坐标，第二项是图片横坐标
        y, x = img.shape[0], img.shape[1]
        x, y = image_point(x, y)

        resize_img = Sequential([
            # resize中输入参数为第一项图片横坐标，第二项图片纵坐标
            Resize((x, y), interpolation=cv2.INTER_LINEAR)
        ])
        img = resize_img(img)

        preprocess = Sequential([
            # 按照顺序对图片进行预处理
            BGR2RGB(),
            Div(255.0),
            Transpose((2, 0, 1))
        ])
        client = HttpClient()
        client.load_client_config("./ocr/serving_client_conf.prototxt")

        # 模型不再分类,通过请求的返回结果来判断身份证分类情况
        url = API_URL['crop']
        client.connect(url)

        im = preprocess(img)
        print(im.shape)

        fetch_map = client.predict(
            feed={
                "image": im,
                "scale_factor": np.array([1.0, 1.0]).reshape(-1),
            },
            fetch=["multiclass_nms3_0.tmp_0"],
            batch=False
        )

        try:
            # 要处理的数据都在里面了，只需要进行写转化就行了
            value_mid = fetch_map.outputs[0].tensor[0]
        except:
            return RuntimeError("crop: 当前图片无返回结果")

        value_shape = value_mid.shape
        value = np.array(list(value_mid.float_data), dtype="float32").reshape(value_shape)  # 转成ndarray，并进行reshape

        # 剔除掉相似度在40%以下的
        # 标注结果: 返回6个参数：类别、相似度、xmin、ymin、xmax、ymax
        value = value[(value[:, 1] > 0.4) & (value[:, 0] > -1), :]
        # result = {'value': value.tolist(), 'change_point': (x, y)}

        # 判断识别结果中有没有被重复识别的类别,若有则去重,只保留相同类别的识别结果中相似度较高的那一条
        value = image_result_duplication(value.tolist())

        # 根据value判断当前图片分类，并根据box和image标签进行旋转,box为身份证框,image为人像/国徽框
        # 若图片中同时含有身份证正反面，进行裁剪并分别旋转
        cls = None
        box_list, image_list = {}, {}
        both_flag = False
        for i in value:
            if i[0] == 0.0:
                cls = IdCardImageClass.EMBLEM
                box_list[cls] = i
            if i[0] == 1.0: image_list[cls] = i
            if i[0] == 4.0:
                if cls == IdCardImageClass.EMBLEM:
                    both_flag = True
                    cls = None
                else:
                    cls = IdCardImageClass.FACE
                box_list[cls] = i
            if i[0] == 9.0: image_list[cls] = i
        if len(box_list) == 0 or len(image_list) == 0:
            return RuntimeError('crop: 未识别到全部坐标显示')
        else:
            result = {}

            # im是旋转后的图片
            im = image_rotate(box_list[cls], image_list[cls], im, cls)
            # 调整shape来进行旋转后的格式处理
            print(im.shape)

            fetch_map = client.predict(
                feed={
                    "image": im,
                    # "im_shape": np.array(list(im.shape[1:])).reshape(-1),
                    "scale_factor": np.array([1.0, 1.0]).reshape(-1),
                },
                fetch=["multiclass_nms3_0.tmp_0"],
                batch=False
            )
            try:
                value_mid_2nd = fetch_map.outputs[0].tensor[0]
            except:
                raise RuntimeError('crop:旋转后图片无返回结果')
            value_shape_2nd = value_mid_2nd.shape
            value = np.array(list(value_mid_2nd.float_data), dtype="float32").reshape(value_shape_2nd)
            value = value[(value[:, 1] > 0.4) & (value[:, 0] > -1), :]

            # 通过PIL的方法进行图片的裁剪，并将其传给extract来进行处理
            pil_img = Image.fromarray(img)      # cv2转PIL
            image_part = []
            for part in value:
                # print(part)
                cropped = pil_img.crop((part[2], part[3], part[4], part[5]))  # (left, upper, right, lower)
                part_img = PIL_to_bytes(cropped)
                image_part.append((part[0], part_img))

            result['value'] = value
            # 结果保存的图片单独处理
            # result['image'] = image_part[0][1]
            result['image_part'] = image_part

            # if not both_flag:
            #     # 同一张图片中只有身份证的一面存在的情况, 直接裁剪以用来识别
            #     result = self.dispose_idcard_img(box_list[cls], image_list[cls], im, img, cls, client)
            #     result[cls]['change_point'] = (x, y)
            # else:
            #     # 需要裁剪的部分，这部分的图片一般为身份证正反面的图片放在了同一张图片上，将身份证正反面照片进行裁剪
            #     # 通过PIL的方法进行图片的裁剪，并将其传给extract来进行处理, cv2转PIL
            #     pil_img = Image.fromarray(img)
            #     image_both_crop = {}
            #     for part in box_list.values():
            #         # print(part)
            #         cropped = pil_img.crop((part[2], part[3], part[4], part[5]))  # (left, upper, right, lower)
            #         part_img = PIL_to_bytes(cropped)
            #         if part[0] == 0.0:
            #             cls = IdCardImageClass.EMBLEM
            #         elif part[0] == 4.0:
            #             cls = IdCardImageClass.FACE
            #         image_both_crop[cls] = part_img
            #     for key in image_both_crop.keys():
            #         result = self.dispose_idcard_img(box_list[key], image_list[cls], im, img, cls, client)
            #         result[key]['change_point'] = (x, y)

        return result

    def extract(self, blocks, cls: IdCardImageClass):
        """
        识别
        :param blocks: crop中裁剪后的各部分图片
        :param cls:传入人像面或国徽面的分类结果
        :return: OCR结果
        """
        url = API_URL['text_ocr']
        result = {'value': {}}
        info = {2.0: "issue", 3.0: "date", 5.0: "name", 6.0: "sex", 7.0: "birth", 8.0: "address", 10.0: "num"}

        try:
            # 从block中依次取出各部分
            for i, block in enumerate(blocks):
                with open(f'{i}.jpg', 'wb') as f:
                    # 应该为完整图片
                    f.write(block[1])
                # 无需ocr的部分直接跳过
                if block[0] not in info.keys():
                    continue

                # textocr需传入io流
                img_io = io.BufferedReader(io.BytesIO(block[1]))
                files = {"file": img_io}
                # data = {"key": ["image"], "value": [get_img(block[1])]}
                r = requests.post(url=url, files=files)
                ocr_message = r.json()

                if len(ocr_message['err_msg']) == 0:
                    ocr_text = ''
                    for item in ocr_message["value"]:
                        ocr_text += item[0]
                    result['value'][info[block[0]]] = ocr_text

                    if block[0] == 6.0:
                        # 性别列同时包含了性别信息和民族信息，需要另外进行nlp
                        data = {'schema': ['性别', '民族'], 'text': ocr_message["value"][0][0]}
                        nlp = requests.post(url=API_URL['nlp'], json=data)
                        result['value']['sex'] = nlp.json()['性别'][0]['text']
                        result['value']['nationality'] = nlp.json()['民族'][0]['text']

                else:
                    return RuntimeError(f"服务器返回结果有报错，报错信息为{ocr_message['err_msg']}")
        except:
            return RuntimeError("extract: 没有获取到结果")

        return result

    def process(self, image: UploadedFile):
        """
        流水线，调用classify、crop、extract
        :param image: 图片
        :return: 身份证OCR结果
        """
        error = ''
        start_time = time.time()
        cls = self.classify(image)
        cls_time = time.time()
        # print(f"分类:{cls_time - start_time}")

        # 重置io流指针位置使得后续img对象使用read()方法读取
        image.seek(0)
        start_time = time.time()
        croped = self.crop(image.read())
        crop_time = time.time()
        # print(f"裁剪:{crop_time - start_time}")

        # 重置io流指针位置使得后续img对象使用read()方法读取
        image.seek(0)
        # start_time = time.time()
        # aliyun_idcard_ocr_result = AliyunIdCardOcr().extract(image.read(), cls=cls)
        # aliyun_time = time.time()
        # print(f"阿里云ocr识别:{aliyun_time - start_time}")
        # print(aliyun_idcard_ocr_result)
        #
        # if type(croped) == RuntimeError:
        #     error += str(croped)
        #     # AliyunIdCardOcr结果异常
        #     if type(aliyun_idcard_ocr_result) == RuntimeError:
        #         error += str(aliyun_idcard_ocr_result)
        #         return RuntimeError("图片清晰度问题,未识别全部结果")
        #     aliyun_idcard_ocr_result['err'] = error
        #     return aliyun_idcard_ocr_result

        start_time = time.time()
        idcard_ocr_result = self.extract(blocks=croped['image_part'], cls=cls)
        # print(idcard_ocr_result)
        idocr_time = time.time()
        # print(f'Idocr识别:{idocr_time - start_time}')
        return idcard_ocr_result

        # # IdCardOcr结果异常
        # if type(idcard_ocr_result) == RuntimeError:
        #     error += str(idcard_ocr_result)
        #     aliyun_idcard_ocr_result['err'] = error
        #     return aliyun_idcard_ocr_result
        # else:
        #     # IdCardOcr结果的格式化处理
        #     idcard_ocr_result = format_idcard_ocr_result(idcard_ocr_result, cls)
        #     if type(aliyun_idcard_ocr_result) == RuntimeError:
        #         error += str(aliyun_idcard_ocr_result)
        #         idcard_ocr_result['err'] = error
        #         return idcard_ocr_result
        #
        # # print(idcard_ocr_result)
        # # print(aliyun_idcard_ocr_result)
        #
        # # IdCardOcr 和 AliyunIdCardOcr 识别结果相同时返回IdCardOcr
        # if idcard_ocr_result == aliyun_idcard_ocr_result:
        #     return idcard_ocr_result
        # else:
        #     # print("结果不同")
        #     # 当双方接口均正常返回且结果不同时，选择阿里云接口调用结果。
        #     if not os.path.exists("img_comparison"):
        #         os.makedirs("img_comparison")
        #     filename = f'img_comparison/img_diff_{time.time()}.jpg'

        # with open(filename, 'wb') as f:
        #     # 应该为完整图片
        #     f.write(croped['image'])

        # # 将双方结果写入数据库
        # ApiComparison.objects.create(image=filename,
        #                              IdCardOcr_result=idcard_ocr_result,
        #                              Aliyun_IdCardOcr_result=aliyun_idcard_ocr_result,
        #                              created_time=time.time()
        #                              )
        # return aliyun_idcard_ocr_result


class PaddleIdCardOcr(IdCardOcr):
    def classify(self, image: str) -> IdCardImageClass:
        pass

    def crop(self, image: str):
        pass

    def extract(self, blocks: list, cls: IdCardImageClass):
        pass


class AliyunIdCardOcr(IdCardOcr):
    def classify(self, image: str) -> IdCardImageClass:
        pass

    def crop(self, image: str):
        pass

    def extract(self, blocks, cls: IdCardImageClass):
        """
        aliyun识别
        :param blocks: crop中完整身份证图片
        :param cls:传入人像面或国徽面的分类结果
        :return: OCR结果
        """
        url = 'https://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json'
        result = {}
        headers = {
            'Authorization': API_AUTH_TOKEN,
            # 'Authorization': 'APPCODE %s' % 'c529065b0e41400bb6cc12e427b646c3',
        }
        info = {
            IdCardImageClass.FACE: {1.0: "name", 2.0: "sex", 3.0: "nationality", 4.0: "birth", 5.0: "address",
                                    7.0: "num"},
            IdCardImageClass.EMBLEM: {2.0: "issue", 3.0: "date"}}
        # face身份证正面，back身份证反面
        if cls == IdCardImageClass.FACE:
            methods = 'face'
        else:
            methods = 'back'

        img = get_img(blocks)
        r = requests.post(url=url, json={
            "configure": {"side": methods}, "image": img
        }, headers=headers)

        if str(r.status_code) != "200":
            if str(r.status_code) == "403":
                return RuntimeError("阿里云剩余次数不足!")
            if str(r.status_code) == "463":
                return RuntimeError("阿里云用户受限，请稍后重试")
            return RuntimeError("阿里云接口调用失败，" + "当前请求状态码为：" + str(r.status_code))

        for i in info[cls]:
            if info[cls][i] == "date":
                result[info[cls][i]] = f'{r.json()["start_date"]}-{r.json()["end_date"]}'
            else:
                result[info[cls][i]] = r.json()[info[cls][i]]

        return result


default_idOcr = IdCardOcr()
ocr_idcard = {
    "default": default_idOcr,
    "idcardOcr": IdCardOcr(),
    "paddle": PaddleIdCardOcr(),
    "aliyun": AliyunIdCardOcr()
}
