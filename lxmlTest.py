from lxml import etree
from io import StringIO


test_html = '''
<html>
    <h4>学号</h4>
    <ul>
       <li>2112001</li>
       <li>2112002</li>
       <li class='blank'>2112003</li>
       <li>2112004</li>
    </ul>
    <h4>姓名</h4>
    <ul class="ul" style="color:red">
        <li>张三</li>
        <li>李四</li>
        <li>王五</li>
        <li>老六</li>
    </ul>
</html>
'''

# 将html网页源码加入带etree中
html = etree.parse(StringIO(test_html))
# print(html)

# # 获取所有li标签下的数据，并提取其内容
# lists = html.xpath('//li')
# for i in lists:
#     print("数据：" + i.text)

# 获取class为blank的所有li标签，并提取其内容
blank_li_list = html.xpath('//li[@class="blank"]')
for l in blank_li_list:
    print("数据：" + l.text)
