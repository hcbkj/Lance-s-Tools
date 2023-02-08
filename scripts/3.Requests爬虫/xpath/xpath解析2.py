from lxml import etree

etree = etree.parse("b.html")
# result = etree.xpath('/html')
# result = etree.xpath('/html/body/ul/li/a/text()')
# result = etree.xpath('/html/body/ul/li[1]/a/text()')    # 从1开始, []表示索引
# result = etree.xpath("/html/body/ol/li/a[@href='dapao']/text()")    # [@xxx='xxx'] 属性的筛选
ol_li_list = etree.xpath("/html/body/ol/li")    # 列表里面放着三个标签
for i in ol_li_list:
    # print(i)
    # 从每个li中提取到文字信息
    result = i.xpath("./a/text()")       # 相对查找 ./当前节点
    # print(result)
    # a标签中href的值
    result2 = i.xpath("./a/@href")      # 拿到属性值：@属性
    # print(result2)

print(etree.xpath("/html/body/ul/li/a/@href"))

print(etree.xpath("/html/body/div[1]"))     # f12 页面右键 copy xpath
