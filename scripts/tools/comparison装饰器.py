# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 11:35

import functools

def comparison(func):
    @functools.wraps(func)
    def inner(**kwargs):
        # 开始进行比对
        blocks = kwargs.get('blocks')
        cls = kwargs.get('cls')

        idcard_ocr_result = func(**kwargs)
        # print(idcard_ocr_result)

        aliyun_idcard_ocr_result = AliyunIdCardOcr().extract(blocks, cls)
        # print(aliyun_idcard_ocr_result)

        if idcard_ocr_result == aliyun_idcard_ocr_result:
            return idcard_ocr_result
        else:
            # print("结果不同")
            if type(aliyun_idcard_ocr_result) == RuntimeError:
                idcard_ocr_result['err'] = aliyun_idcard_ocr_result
                return idcard_ocr_result

            # # 当双方接口均正常返回且结果不同时，选择阿里云接口调用结果。
            # if not os.path.exists("img_comparison"):
            #     os.makedirs("img_comparison")
            # filename = f'img_comparison/img_diff_{time.time()}.jpg'
            #
            # with open(filename, 'wb') as f:
            #     # 应该为完整图片
            #     f.write(blocks[1])
            #
            # # 将双方结果写入数据库
            # ApiComparison.objects.create(image=filename,
            #                              IdCardOcr_result=idcard_ocr_result,
            #                              Aliyun_IdCardOcr_result=aliyun_idcard_ocr_result,
            #                              created_time=time.time()
            #                              )
            return aliyun_idcard_ocr_result

    return inner
