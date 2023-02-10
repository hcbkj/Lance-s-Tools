# import time
#
# config = {}
# dict1 = {"rpa-path1": r';D:\工作相关\Project\aliyun-mns-python\文书批处理', "rpa-path2": r'文书批处理\已审核;D:\工作相关\Project\aliyun-mns-python\xxx'}
#
# for k, v in dict1.items():
#     if 'RPA' in k.upper():
#         if not len(v.split(";")[0]):
#             continue
#         else:
#             keys = k + ';' + v.split(";")[0].lstrip('\\').lstrip('/')
#             values = v.split(";")[1]
#             config[keys] = values
# print(config)
# print("**********")
# # for i in config:
# #     print(i)
# #     print(config[i])
#
#
# file_name = r'文书批处理\已审核\工作相关\Project\aliyun-mns-python\xxx\abc.docx'
#
# while 2:
#     time.sleep(1)
#     rep = []
#     for i in config:
#         print(i)
#         print(file_name)
#         if file_name.startswith(i.split(";")[-1]):
#             rep.append(i.split(";")[-1])
#
#     # rep = [i.split(";")[-1] for i in config if file_name.startswith(i.split(";")[-1])]
#     print(rep)
#     if not rep:
#         print(f"规则不匹配！{file_name}")
#         break
#
#     rep = rep[0]
#     print(rep)
#     file_name = file_name.replace(rep, config[rep])
#     print(file_name)
#     break

# message = {'bucket': {'arn': 'acs:oss:cn-hangzhou:1786291783352655:moon-files', 'name': 'moon-files',
#                       'ownerIdentity': '1786291783352655', 'virtualBucket': ''},
#            'object': {'deltaSize': 15537, 'eTag': '968FDC93D7FB48CEC589347EF8FF6E1A',
#                       'key': '文书批处理/已审核/曹帅琛/20230210/DP808648117985325147/王丹-220381198605242240-调解协议-95+5.docx',
#                       'objectMeta': {'mimeType': 'application / octet - stream',
#                                      'userMeta': {'x - oss - meta - ctime': '1675996738', 'x - oss - meta - gid': '0',
#                                                   'x - oss - meta - mode': '33188',
#                                                   'x - oss - meta - mtime': '1675996738', 'x - oss - meta - uid': '0'}},
#                       'size': 15537}, 'ossSchemaVersion': '1.0', 'ruleId': 'moon - file- CM'}
#
# print(message['object']['size'] / 1024 / 1024)

import os
os.environ['ISPRODUCTION'] = 'a'
print(os.environ.get("ISPRODUCTION"))
if os.environ.get("ISPRODUCTION"):
    print(11)

# if 'a':
#     print(1)
