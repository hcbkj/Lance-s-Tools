# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 17:20

import pysftp

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  # 忽略主机密钥

username = "yuanhao"
password = "eO1bZ2pT4gZ8sI1yB1qE"

# 建立连接
with pysftp.Connection(host="116.62.26.205", port=22, username=username, password=password, cnopts=cnopts) as sftp:
    # 进入目录
    with sftp.cd('/异常情况处理测试文件夹/sftp'):
        # 上传文件
        sftp.put('/path/to/local/file')

