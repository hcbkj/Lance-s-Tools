# -*- coding: utf-8 -*-
# @Time    : 2022/10/8 10:13
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


# 163 邮箱发件
def send_email(recipient, context, subject):
    # 构建邮件内容
    msg = MIMEText(context, "html", "utf-8")  # 内容
    msg["From"] = formataddr(["申元昊", "sender@163.com"])  # 发件人及邮箱
    msg["to"] = recipient  # 目标邮箱
    msg["Subject"] = subject  # 主题

    # 发送邮件
    server = smtplib.SMTP_SSL("smtp.163.com")
    server.login("s442480745@163.com", "KTUNELHQUTFZQNKC")  # 账号/授权码
    server.sendmail("s442480745@163.com", recipient, msg.as_string())  # 自己邮箱/目标邮箱/内容
    server.quit()


send_email("442480745@qq.com", "早安午安晚安", "这里是主题!")
