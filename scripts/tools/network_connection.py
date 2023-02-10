import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import win32con
import win32api


# 数据防泄漏自动登录
def automatic_login(username, password):
    driver = webdriver.Chrome(executable_path=r"D:\Driver\chromedriver.exe")
    driver.get("http://172.29.8.100:8099/portal/redirect/nacc/")
    driver.find_element(By.XPATH, '//input[@id="usr"]').send_keys(username)
    time.sleep(2)
    driver.find_element(By.XPATH, '//input[@id="pwd"]').send_keys(password)
    time.sleep(1)
    driver.execute_script("login.userLoginPreCheck(this);")
    time.sleep(5)
    driver.find_element(By.XPATH, "//p[text()='您好，您已成功接入网络！']")
    success = (0, "登录成功", "提醒", win32con.MB_OK)
    driver.quit()
    win32api.MessageBox(*success)


if __name__ == '__main__':
    username = 'shenyuanhao'
    password = '442480745s'
    automatic_login(username, password)
