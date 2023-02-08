# Requests库爬虫

## Web请求的全链路分析

![关键字！](C:\Users\9000\AppData\Roaming\Typora\typora-user-images\image-20220726095707825.png)

<center>带有关键字的html内容</center>



### 1.服务器渲染：

在服务器那边直接把数据和html整合在一起，统一返回给浏览器

​    在页面源代码中能看到数据



### 2.客户端渲染：

第一次请求只要一个html骨架，第二次请求拿到数据，进行数据展示
    在页面源代码中看不到数据,requests请求

熟练使用浏览器抓包数据:    network,预览页面

<img src="C:\Users\9000\AppData\Roaming\Typora\typora-user-images\image-20220726100200575.png" alt="image-20220726100200575" style="zoom:67%;" />

<center>客户端渲染，数据在客户端组合</center>



## HTTP协议

协议：就是两个计算机之间为了能够流畅的进行沟通而设置的一个君子协定.常见的协议有TCP/IPSOAP协议，HTTP协议，SMTP协议等等！..

HTTP协议，HyperTextTransferProtocol（超文本传输协议）的缩写，是用于从万维网（WWW：WorldWideWeb）服务器传输超文本到本地浏览器的传送协议.直白点儿，就是浏览器和服务器之间的数据交互遵守的就是HTTP协议。

HTTP协议把一条消息分为三大块内容，无论是请求还是响应都是三块内容。



### 请求：

```python
请求行->请求方式（get/post）请求url地址协议
请求头->放一些服务器要使用的附加信息

请求体->一般放一些请求参数
```



### 响应：

```python
状态行->协议 状态码
响应头->放一些客户端要使用的一些附加信息

响应体->服务器返回的真正客户端要用的内容（HTML，json）等
```



### 请求头中最常见的一些重要内容（爬虫需要）

1.User-Agent：请求载体的身份标识（用啥发送的请求）Referer:防盗链（这次请求是从哪个页面来的？反爬会用到）
2.cookie:本地字符串数据信息（用户登录信息，反爬的token）



### 响应头中一些重要的内容

1.cookie:本地字符串数据信息（用户登录信息，反爬的token）
2.各种神奇的莫名其妙的字符串（这个需要经验了，一般都是token字样，防止各种攻击和反爬）



### 请求方式:

GET:显式提交

POST:隐式提交

![image-20220726102309876](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220726102309876.png)



## 	==豆瓣案例==

### [requests爬虫01]("D:\工作相关\Test\First\Study\爬虫\requests爬虫01.py")

```python
# 安装 pip install requests

import requests

# # 01 get
# query = input('输入你喜欢的明星:')
# url = f'https://www.sogou.com/web?query={query}'  # 地址栏中复制的url都是get方式,get可以直接拼接url
# headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
# }
#
# resp = requests.get(url, headers=headers)   # 处理一个小小的反爬
#
# print(resp)  # <Response [200]> 200成功
# print(resp.text)  # 拿到页面源代码
# resp.close()    # 关闭resp,避免请求过多

# 02 Post
url = "https://fanyi.baidu.com/sug"

s = input("请输入你要翻译的英文单词:")
data = {
    "kw": s
}
resp = requests.post(url, data=data)
print(resp.json())      # 将服务器返回直接处理成json() =>dict
resp.close()    # 关闭resp,避免请求过多


```



### [Requests爬虫案例豆瓣]("D:\工作相关\Test\First\Study\爬虫\Requests爬虫案例豆瓣.py")

```python
# 爬虫
import requests

url = "https://movie.douban.com/j/chart/top_list?"

# url参数过长,重新封装参数
param = {
    'type': '24',
    'interval_id': '100:90',
    'action': '',
    'start': 40,
    'limit': 20,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

resp = requests.get(url=url, params=param, headers=headers)

# 什么也没用,反爬虫:第一时间考虑user-agent
print(resp.json())
resp.close()    # 关闭resp,避免请求过多

```



## 数据解析概述

在上一章中，我们基本上掌据了抓取整个网页的基本技能，但是呢，大多数情况下，我们并不需要整个网页的内容，只是需要那么一小部分.怎么办呢？这就涉及到了数据提取的问题。

本课程中，提供三种解析方式：

**1.re解析**		*# 正则表达式解析，最快*

**2.bs4解析**		*# beautifulsoup4 最简单，效率一般*

**3.xpath解析**		*# 方便*

这三种方式可以混合进行使用，完全以结果做导向，只要能拿到你想要的数据，用什么方案并不重要，当你掌握了这些之后，再考虑性能的问题.



### re解析

#### 正则表达式：

Regular Expression正则表达式，一种使用表达式的方式对字符串进行匹配的语法规则

我们抓取到的网页源代码本质上就是一个超长的字符串，想从里面提取内容.用正则再合适不过了

-   <u>正则的优点：速度快，效率高，准确性高</u>
-   <u>正则的缺点：新手上手难度有点儿高</u>

不过只要掌握了正则编写的逻辑关系，写出一个提取页面内容的正则其实并不复杂

正则的语法：使用元字符进行排列组合用来匹配字符串。

>   在线测试正则表达式https://tool.oschina.net/regex/



#### **元字符：具有固定含义的特殊符号**

**常用元字符：**

-   . 匹配除换行符以外的任意字符

-   \w 延配字母或数字或下划线

-   \s 匹配任意的空白符

-   \d 匹配数字

-   \n 匹配一个换行符

-   \t 匹配一个制表符

    

-   ^ 匹配字符串的开始

-   $ 匹配字符串的结尾

    *上述两个爬虫中用到的不多，但是多用于校验*



*大写就是上述小写的反义词*

-   \W 匹配非字母或数字或下划线 (大写，下同)
-   \D 匹配非数字
-   \S 匹配非空白符
-   a|b 匹配字符a或字符b
-   () 匹配括号内的表达式，也表示一个组  *略复杂*
-   [...] 匹配字符组中的字符
-   [^...]匹配除了字符组中字符的所有字符  *非*



#### **量词：控制前面的元字符出现的次数**

-   \* 重复零次或更多次
-   \+ 重复⼀次或更多次
-   ? 重复零次或⼀次
    -   出现一次或者更多次
-   {n} 重复n次 
-   {n,} 重复n次或更多次
-   {n,m} 重复n到m次



#### **贪婪匹配和惰性匹配**

-    .* 贪婪匹配
-   .*? 惰性匹配
    -   尽可能少，回溯算法

**<span style="color:red">这两个要着重的看⼀下. 因为我们写爬⾍⽤的最多的就是这个惰性匹配.</span>**



#### 分组group

(?P\<name>.*?)



#### **案例**

-   str: 玩⼉吃鸡游戏, 晚上⼀起上游戏, ⼲嘛呢? 打游戏啊

-   reg: 玩⼉.*?游戏

-   此时匹配的是: 玩⼉吃鸡游戏

-   reg: 玩⼉.*游戏 

-   此时匹配的是: 玩⼉吃鸡游戏, 晚上⼀起上游戏, ⼲嘛呢? 打游戏 



-   str: \<div>胡辣汤\</div>

-   reg: <.*>

-   结果: \<div>胡辣汤\</div>



-   str: \<div>胡辣汤\</div>

-   reg: <.*?>

-   结果：

-   \<div>\</div>



-   str: \<div>胡辣汤\</div><span>饭团</span>

-   reg: \<div>.*?\</div>

-   结果:

-   \<div>胡辣汤\</div>

所以我们能发现这样⼀个规律: .\*? 表示尽可能少的匹配, .\*表示尽可能多的匹配, 先记住这个规律. 后⾯写爬⾍会⽤到的



#### 实战案例

1.  [⼿刃⾖瓣TOP250电影信息](re\手刃豆瓣TOP250电影信息.py)

2.  [屠戮盗版天堂](re\屠戮盗版天堂.py)

    

### bs4解析

#### HTMl语法

bs4解析⽐较简单, 但是呢, ⾸先你需要了解⼀丢丢的html知识. 然后再去使⽤bs4去提取, 逻辑和编写难度就会⾮常简单和清晰。

<u>HTML(Hyper Text Markup Language)</u>超⽂本标记语⾔, 是我们编写⽹⻚的最基本也是最核⼼的⼀种语⾔. 其语法规则就是⽤不同的标签对⽹⻚上的内容进⾏标记, 从⽽使⽹⻚显示出不同的展示效果balabala...

**<span style="color:blue">bs4实际上逻辑就是通过标签名称及属性来拿到数据</span>**

还有些就是零零碎碎的小使用技巧：

-   先创建BeautifulSoup对象，例如：

    -   ```python
        page = BeautifulSoup(resp.text, "html.parser")      # 指定为HTML的解释器
        ```

-   <span style="color:blue">**bs主要方法：find() and findall()**</span>

    -   ```python
        # find(标签, 属性=值)
        # find_all(标签, 属性=值)
        # 具体：
        table = page.find("table", class_="hq_table")  # class是python的关键字
        table = page.find("table", attrs={"class": "hq_table"})  # 和上一行是一个意思. 此时可以避免class
        ```

-   <span style="color:blue">**如何在bs中拿到标签的属性？**</span>

    -   ```python
        BeautifulSoup().get('属性名')
        ```

#### 案例

[电影天堂爬取2022新片精品](bs4\bs4Test.py)

==[抓取优美图库](bs4\抓取优美图库.py)==



### xpath解析

#### 简述

XPath是⼀⻔在 XML ⽂档中查找信息的语⾔. XPath可⽤来在 XML⽂档中对元素和属性进⾏遍历. ⽽我们熟知的HTML恰巧属于XML的⼀个⼦集. 所以完全可以⽤xpath去查找html中的内容。

```xml
<book>
	<id>1</id>
	<name>野花遍地⾹</name>
	<price>1.23</price>
	<author>
	<nick>周⼤强</nick>
	<nick>周芷若</nick>
	</author>
</book>
```

在上述html中,

1.  book, id, name, price....都被称为节点.

2.  Id, name, price, author被称为book的⼦节点

3.  book被称为id, name, price, author的⽗节点

4.  id, name, price,author被称为同胞节点

    OK~ 有了这些基础知识后, 我们就可以开始了解xpath的基本语法了,在python中想要使⽤xpath, 需要安装lxml模块



#### 语法

直接上代码界面：

**part1：**

```python
# xpath 是在XML文档中搜索内容的一门语言
# html是xml的一个子集
"""
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <author>
        <nick>周大强</nick>
        <nick>周芷若</nick>
    </author>
</book>
"""
# 安装lxml模块
# xpath解析
from lxml import etree
# etree.XML().xpath()

xml = """
<book>
    <id>1</id>
    <name>野花遍地香</name>
    <price>1.23</price>
    <nick>臭豆腐</nick>
    <author>
        <nick id="10086">周大强</nick>
        <nick id="10010">周芷若</nick>
        <nick class="joy">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
        <div>
            <nick>热热热热热1</nick>
        </div>
        <span>
            <nick>热热热热热2</nick>
        </span>
    </author>

    <partner>
        <nick id="ppc">胖胖陈</nick>
        <nick id="ppbc">胖胖不陈</nick>
    </partner>
</book>
"""

tree = etree.XML(xml)
# result = tree.xpath("/book")  # /表示层级关系. 第一个/是根节点
# result = tree.xpath("/book/name")
# result = tree.xpath("/book/name/text()")  # text() 拿文本
# result = tree.xpath("/book/author//nick/text()")  # // 后代
# result = tree.xpath("/book/author/*/nick/text()")  # * 任意的节点. 通配符(会儿)
result = tree.xpath("/book//nick/text()")
print(result)
```

**part2:**

```python
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
```



#### 案例：

[xpath案例-猪八戒网](xpath\xpath案例-猪八戒网.py)



## requests进阶概述

我们在之前的爬⾍中其实已经使⽤过**headers**了. header为HTTP议中的请求头. ⼀般存放⼀些和请求内容⽆关的数据. 有时也会存放⼀些安全验证信息.⽐如常⻅的User-Agent, token, cookie等.

通过requests发送的请求, 我们可以把请求头信息放在headers中. 也可以单独进⾏存放, 最终由requests⾃动帮我们拼接成完整的http请求头.

1.  模拟浏览器登录->处理cookie
2.  防盗链处理-> 抓取梨视频数据
3.  代理 -> 防⽌被封IP    <u>*灰色，少用*</u>



### 处理cookie

这cookie网站多少沾点问题，先这样，这一部分显然学的浅。

*插个眼,之后来练习*

>flag!



### 防盗链处理

\<video>标签在页面检查中可以看到，但是在页面源代码中却无法看到\<video>标签，基本可以断定，这个video是通过后期二次加载，通过js脚本的方式添加的，因此无法在页面中直接找到video的相关链接src。

**防盗链：**

Referer： 溯源, 当前本次请求的上一级是谁

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    # 防盗链:溯源, 当前本次请求的上一级是谁
    "Referer": "https://www.pearvideo.com/video_1756772",
}
```

[防盗链的处理](requests进阶_headers\防盗链的处理.py)



### 代理

<u>高并发，大批量</u>

当我们反复抓取⼀个⽹站时, 由于请求过于频繁, 服务器很可能会将你的IP进⾏封锁来反爬. 应对⽅案就是通过⽹络代理的形式进⾏伪装。

**代理的原理：**

![image-20220728160816721](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220728160816721.png)

<center>从图上可以得知. 对于⽬标⽹站来说. 是通过代理服务器发送的请求. 也就可以避免你的IP被封锁了.</center>

爬⾍如何使⽤代理:

[代理](requests进阶_headers\代理.py)

*代理IP⼀般属于⼀个灰⾊产业. 在本课程中不做深⼊讨论.* 



### 案例

[抓取网易云评论]()

![image-20220728160628216](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220728160628216.png)



**寻找加密位置的过程**

```javascript
# 处理加密过程
	'''
    function a(a) {         # a = 16
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)      # 循环16次
            e = Math.random() * b.length,       # random 随机数 例:1.2345
            e = Math.floor(e),          # 取整 例:1
            c += b.charAt(e);           # 取字符串中的xxx位置 例:b
        return c        # 16个随机的字符串
    }
    function b(a, b) {      # a: 要加密的内容, 
        var c = CryptoJS.enc.Utf8.parse(b)      # b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)      # e是数据
          , f = CryptoJS.AES.encrypt(e, c, {    # c: 加密的密钥
            iv: d,          # AES加密中的iv是偏移量
            mode: CryptoJS.mode.CBC     # 加密模式,CBC
        });
        return f.toString()         # 加密后把f变成了字符串
    }
    function c(a, b, c) {       # 算法,里面并不产生随机值
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    
    # d: 数据data, e: buV4Z(["流泪", "强"]) => Console => 010001, 
    f: buV4Z(Rg0x.md) => Console => "很长一串"    g: buV4Z(["爱心", "女孩", "惊恐", "大笑"]) => 0CoJUm6Qyw8W8jud
    
    function d(d, e, f, g) {        
            var h = {}      # 空对象
          , i = a(16);      # function a() => i是16位的随机值
        return h.encText = b(d, g),         # g就是密钥
        h.encText = b(h.encText, i),        # 返回的就是params, i也是密钥
        h.encSecKey = c(i, e, f),           # 返回的就是encSecKey  e和f是固定值, 在i身上做文章, 当此时的i固定, 则key一定能够固定
        h       # return h
    }
    
    # 两次加密
    # 数据 + g => b => 第一次加密 + i => params
'''
```

[综合训练_抓取网易云音乐热评](requests进阶_headers\综合训练_抓取网易云音乐热评.py)



## 爬虫提速

到⽬前为⽌, 我们可以解决爬⾍的基本抓取流程了. 但是抓取效率还是不够⾼. 如何提⾼抓取效率呢? 我们可以选择<u>多线程</u>, <u>多进程</u>, <u>协程</u>等操作完成**<u>异步爬⾍</u>**.

何为异步? 这⾥我们不讨论蹩脚的概念性问题. 直接说效果.

打个⽐⽅, 我们⽬前写的爬⾍可以理解为单线程, ⽐喻为单⻋道公路.如何提⾼效率呢? 很简单, 搞成多⻋道就OK了啊. 异步爬⾍你就可以理解为多⻋道同时进⾏爬取.

![image-20220729142833702](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220729142833702.png)



在这⾥要特殊说明⼀下. 多线程异步爬⾍中每⼀步都可以设⽴成多线程的. 具体操作得实际去分析. 当然, 也可以像我画图这样, 每⼀个url⼀个单独线程. 还是那句话. 技术是死的. ⼈是活的. 怎么⼲还得看你⾃⼰~



**本章节重点内容：**

1.  快速学会多线程
2.  快速学会多进程
3.  线程池和进程池
4.  扒光新发地
5.  协程
6.  多任务异步协程实现
7.  aiohttp模块详解
8.  扒光⼀本⼩说
9.  综合训练-抓取⼀部电影



### 多线程

<center><span style="color:blue">进程 -> 资源单位，线程 -> 执行单位</span></center>

![image-20220729144427415](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220729144427415.png)

*进程好比公司，线程就是员工*



python中实现多线程⾮常简单. 我们要借助Thread类来完成.

```python
# 线程, 进程
# 进程是资源单位, 每一个进程至少要有一个线程
# 线程是执行单位

# 启动每一个程序默认都会有一个主线程

# def func():
#     for i in range(100):
#         print("func", i)
#
#
# if __name__ == '__main__':
#     func()
#     for i in range(100):
#         print("main", i)


# 多线程
from threading import Thread        # 线程类

# 实现多线程的第一种方法
def func(name):
    for i in range(100):
        print(name, i)

if __name__ == '__main__':
    # t = Thread(target=func)     # 创建线程并给线程安排任务
    # t.start()       # 开始执行该线程，实际上，只是给线路赋予了一个状态，表示可以开始了，具体的执行时间由cpu决定

    t1 = Thread(target=func, args=("周杰伦",))     # 传参 args(,)必须是元组,因此,当args()里面只有一个参数的时候,要加上逗号,
    t1.start()
    t2 = Thread(target=func, args=("王力宏",))  # 传参 args(,)必须是元组,因此,当args()里面只有一个参数的时候,要加上逗号,
    t2.start()

    for i in range(100):
        print("main", i)

# # 实现多线程的第二种方法
# class MyThread(Thread):
#     def run(self):
#         # 固定的, --> 当线程可以被执行的时候,被执行的就是run()
#         for i in range(100):
#             print("子线程", i)
#
# if __name__ == '__main__':
#     t = MyThread()
#     # t.run()       # 方法的调用 -> 单线程??
#     t.start()       # 开启线程
#
#     for i in range(100):
#         print("主线程", i)
# 线程, 进程
# 进程是资源单位, 每一个进程至少要有一个线程
# 线程是执行单位

# 启动每一个程序默认都会有一个主线程

# def func():
#     for i in range(100):
#         print("func", i)
#
#
# if __name__ == '__main__':
#     func()
#     for i in range(100):
#         print("main", i)


# 多线程
from threading import Thread        # 线程类

# 实现多线程的第一种方法
# def func():
#     for i in range(100):
#         print("func:", i)
#
# if __name__ == '__main__':
#     t = Thread(target=func)     # 创建线程并给线程安排任务
#     t.start()       # 开始执行该线程，实际上，只是给线路赋予了一个状态，表示可以开始了，具体的执行时间由cpu决定
#     # t2 = Thread(target=xxx)
#     # t2.start()
#
#     for i in range(100):
#         print("main", i)

# 实现多线程的第二种方法
class MyThread(Thread):
    def run(self):
        # 固定的, --> 当线程可以被执行的时候,被执行的就是run()
        for i in range(100):
            print("子线程", i)

if __name__ == '__main__':
    t = MyThread()
    # t.run()       # 方法的调用 -> 单线程??
    t.start()       # 开启线程

    for i in range(100):
        print("主线程", i)
```



### 多进程

用的不多

因为开辟一个进程所消耗的资源要比开辟线程多得多。

```python
from multiprocessing import Process


def func():
    for i in range(100):
        print("子进程", i)


if __name__ == '__main__':
    p = Process(target=func)
    p.start()

    for i in range(100):
        print("主进程", i)
```

写法与多线程基本相似（包括自己创建一个类，继承自Process的操作也是基本相似），但是背后的工作原理相差很多。



### 线程池和进程池

线程池: 一次性开辟一些线程. 我们用户直接给线程池子提交任务. <u>**线程任务的<span style="color:red">调度</span>交给线程池来完成**</u>

```python
# 线程池: 一次性开辟一些线程. 我们用户直接给线程池子提交任务. 线程任务的调度交给线程池来完成
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor      # 线程池和进程池

def fn(name):
    for i in range(100):
        print(name, i)


if __name__ == '__main__':
    # 创建线程池
    with ThreadPoolExecutor(50) as t:
        for i in range(100):
            t.submit(fn, name=f'线程{i}')

    # 等待线程池中的任务全部执行完毕, 才继续执行(守护线程)
    print("123")
```



#### 实战案例

网页问题待定，之后补齐，教学代码如下(可参考逻辑)：

```python
# 1. 如何提取单个页面的数据
# 2. 上线程池,多个页面同时抓取
import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor

f = open("data.csv", mode="w", encoding="utf-8")
csvwriter = csv.writer(f)


def download_one_page(url):
    # 拿到页面源代码
    resp = requests.get(url)
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/div[2]/div[4]/div[1]/table")[0]
    # trs = table.xpath("./tr")[1:]
    trs = table.xpath("./tr[position()>1]")
    # 拿到每个tr
    for tr in trs:
        txt = tr.xpath("./td/text()")
        # 对数据做简单的处理: \\  / 去掉
        txt = (item.replace("\\", "").replace("/", "") for item in txt)
        # 把数据存放在文件中
        csvwriter.writerow(txt)
    print(url, "提取完毕!")


if __name__ == '__main__':
    # for i in range(1, 14870):  # 效率及其低下
    #     download_one_page(f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml")

    # 创建线程池
    with ThreadPoolExecutor(50) as t:
        for i in range(1, 200):  # 199 * 20 = 3980
            # 把下载任务提交给线程池
            t.submit(download_one_page, f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml")

    print("全部下载完毕!")

```



### 协程

协程是我要重点去讲解的⼀个知识点. 它能够更加⾼效的利⽤CPU.

其实, 我们能够⾼效的利⽤多线程来完成爬⾍其实已经很6了. 但是,从某种⻆度讲, 线程的执⾏效率真的就⽆敌了么? 我们真的充分的利⽤CPU资源了么? ⾮也~ 

我们要知道CPU⼀般抛开执⾏周期不谈, 如果⼀个线程遇到了IO操作, CPU就会⾃动的切换到其他线程进⾏执⾏. 那么, 如果我想办法让我的线程遇到了IO操作就挂起, 留下的都是运算操作. 那CPU是不是就会⻓时间的来照顾我。

以此为⽬的, 伟⼤的程序员就发明了⼀个新的执⾏过程. 当线程中遇到了IO操作的时候, 将线程中的任务进⾏切换, 切换成⾮IO操作. 等原来的IO执⾏完了. 再恢复回原来的任务中。

![image-20220729174209202](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220729174209202.png)

**就形成了这样⼀种模型, 在程序遇到了IO操作(费时不费⼒的操作)时,自动切换到其他任务. 该模型被称为协程.**（***多任务异步操作***）



协程: 当程序遇见了IO操作的时候. 可以选择性的切换到其他任务上.

-   在微观上是一个任务一个任务的进行切换. 切换条件一般就是IO操作
-   在宏观上,我们能看到的其实是多个任务一起在执行

*上方所讲的一切. 都是在单线程的条件下，*

*尽可能充分的利用单线程的资源，且协程的操作模型是**<span style="color:blue"><u>由程序来实现的</u></span>**,而不是系统*



#### 案例

[协程](爬虫提速\协程.py)



**内部很多细节！！**

```python
import time

# def func():
#     print("123")
#     time.sleep(1)       # 让当前的线程处于阻塞状态,cpu是是不为我工作的
#     print("12345")
#
# if __name__ == '__main__':
#     func()

# input() 时程序也是处于阻塞状态, requests.get(),在网络请求返回数据之前,程序也是处于阻塞状态的
# 一般情况下,当程序处于IO操作的是时候,线程都会处于阻塞状态

"""
协程: 当程序遇见了IO操作的时候,可以选择性的切换到其他任务上.
在微观上是,一个任务一个任务的进行切换,切换条件一般是IO
在宏观上, 我们能看到的其实是多个任务在一起执行
多任务异步操作

上方所将的一切,都是在单线程的情况下
尽可能充分的利用单线程的资源
且协程的操作模型是由程序来实现的,而不是系统
"""

# python编写协程的程序
import asyncio

async def func1():
    # 异步协程函数
    print('你好,我是张三')
    # time.sleep(3)   # 当程序出现了同步操作的时候, 异步就中断了
    await asyncio.sleep(3)    # 异步操作的代码
    print('张三搞定')

async def func2():
    print('你好,我是潘周丹')
    # time.sleep(2)
    await asyncio.sleep(2)
    print('潘周丹搞定')

async def func3():
    print('你好,我是赵构')
    # time.sleep(4)
    await asyncio.sleep(4)
    print('赵构搞定')

# if __name__ == '__main__':
#     # g = func1()       # 异步协程函数,此时函数执行得到的是一个协程对象
#     # # print(g)
#     # asyncio.run(g)      # 协程程序运行需要asyncio模块的支持
#
#     f1 = func1()
#     f2 = func2()
#     f3 = func3()
#
#     tasks = [
#         f1, f2, f3
#     ]
#
#     t1 = time.time()
#     # 一次性启动多个任务(协程)
#     asyncio.run(asyncio.wait(tasks))
#     t2 = time.time()
#
#     print(t2 - t1)


# # 推荐的写法,可以有效避免主线程过长
# # 协程函数
# async def main():
#     # # 第一种写法
#     # f1 = func1()        # 协程对象
#     # # 一般await挂起操作都放在协程对象前面
#     # await f1
#
#     # 第二种写法(推荐), 便于套在爬虫上
#     # 统一执行
#     # tasks = [
#     #     func1(),
#     #     func2(),
#     #     func3(),
#     # ]
#
#     # 为避免报错,可以手动的把协程对象包装成task对象
#     tasks = [
#         asyncio.create_task(func1()),     # 执行
#         asyncio.create_task(func2()),     # 执行
#         asyncio.create_task(func3()),     # 执行
#     ]
#
#     await asyncio.wait(tasks)
#
#
# if __name__ == '__main__':
#     t1 = time.time()
#     # 一次性启动多个任务(协程)
#     asyncio.run(main())
#     t2 = time.time()
#     print(t2 - t1)


# 在爬虫领域的应用
async def download(url):
    print("准备开始下载")
    await asyncio.sleep(2)      # 模拟网络请求, 在此处requests.get()不好使,因为requests.get()是同步操作,换成异步方式
    print("下载完成")


async def main():
    urls = [
        'http://www.baidu,com',
        'http://www.bilibili.com',
        'http://www.163.com',
    ]

    tasks = []
    for url in urls:
        d = asyncio.create_task(download(url))       # 不是函数执行,是得到了一个协程对象
        tasks.append(d)

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())

```



### 异步http请求 aiohttp模块

[代码部分](爬虫提速\异步http请求aiohttp模块.py)

代码：

```python
# requests.get() 同步的代码 -> 异步操作aiohttp
# pip install aiohttp

import asyncio
import aiohttp

urls = [
    "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg"
]


async def aioDownload(url):
    # 发送请求，得到图片内容，保存到图片
    # s = aiohttp.ClientSession()  <==> requests
    # s.get()   s.post()    <==>    requests.get()  requests.post()
    name = url.rsplit("/", 1)[1]
    async with aiohttp.ClientSession() as session:      # requests
        async with session.get(url) as resp:        # resp = requests.get()
            # 请求回来了,写入文件
            # 可以学一下aiofiles
            with open(name, mode="wb") as f:         # 创建文件
                f.write(await resp.content.read())      # 需要加上一个await来挂起


async def main():
    tasks = []
    for url in urls:
        tasks.append(aioDownload(url))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())

```



#### 案例

##### 用协程扒光一部小说

思路:

先同步请求到需要大量请求的部分,再进行异步操作去获取网络请求.

[异步http请求aiohttp模块](爬虫提速\异步http请求aiohttp模块.py)

**代码:**

```python
# requests.get() 同步的代码 -> 异步操作aiohttp
# pip install aiohttp

import asyncio
import aiohttp

urls = [
    "http://kr.shanghai-jiuxin.com/file/2020/1031/191468637cab2f0206f7d1d9b175ac81.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/563337d07af599a9ea64e620729f367e.jpg",
    "http://kr.shanghai-jiuxin.com/file/2020/1031/774218be86d832f359637ab120eba52d.jpg"
]


async def aioDownload(url):
    # 发送请求，得到图片内容，保存到图片
    # s = aiohttp.ClientSession()  <==> requests
    # s.get()   s.post()    <==>    requests.get()  requests.post()
    name = url.rsplit("/", 1)[1]
    async with aiohttp.ClientSession() as session:      # requests
        async with session.get(url) as resp:        # resp = requests.get()
            # 请求回来了,写入文件
            # 可以学一下aiofiles
            with open(name, mode="wb") as f:         # 创建文件
                f.write(await resp.content.read())      # 需要加上一个await来挂起


async def main():
    tasks = []
    for url in urls:
        tasks.append(aioDownload(url))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())

```

*小说内容为空主要是网站问题*



##### ==如何抓取视频==

###### 思路:

常规方式(最基础):\<video src="不能播的视频.mp4">\</video>	*不实用*



**一般的视频网站是怎么做的?**

-   用户上传 -> 转码(把视频做处理, 2K, 1080, 标清)  -> 切片处理(把单个的文件进行拆分)  60

-   用户在进行拉动进度条的时候

-   需要一个文件记录: 1.视频播放顺序, 2.视频存放的路径, 3. 其他....

-   M3U8  txt  json   => 文本

    既然要把视频切成⾮常多个小碎⽚. 那就需要有个⽂件来记录这些⼩碎⽚的路径. 该⽂件⼀般为M3U⽂件. M3U⽂件中的内容经过UTF-8的编码后, 就是M3U8⽂件. 今天, 我们看到的各⼤视频⽹站平台使⽤的⼏乎都是M3U8⽂件:

    ![image-20220801151643107](D:\工作相关\Test\First\Study\Requests爬虫\Requests库爬虫.assets\image-20220801151643107.png)

**想要抓取一个视频:**

1.  <u>找到m3u8 **(各种手段)</u>**	  *有些网站需要二次操作*

2.  通过m3u8下载到ts文件

3.  可以通过各种手段(不仅是编程手段) 把ts文件合并为一个mp4文件



###### 简单案例:91看剧

页面视频一定是通过\<video>标签展示的,但是若是没有在页面源代码中搜索到\<video>标签,说明该页面中用于展示视频的\<video>标签一定是通过js脚本动态生成的 -->因而需要找到生成标签的页面源代码.

例: 

\<script type=...>

video...



**一种比较少见的反爬方式:**

url中的的动态字符串

当用户直接请求m3u8文件的时候,对其进行一次校验(通过url中的动态字符串进行校验)

这种方式要求用户必须按照步骤依次访问页面,并带着上一个页面的返回值进行下一次请求,当用户跳过其中的某些步骤直接访问后续页面时(即获取url直接爬取等..),访问请求就不会带有上一个页面的返回值,从而被拒绝请求.

且请求返回值的字符串具有时效性,需要刷新一下页面(即生成了新的字符串).



**视频网站抓取流程：**

流程:

1.  拿到548121-1-1.html的页面源代码
2.  从源代码中提取到m3u8的url
3.  下载m3u8
4.  读取m3u8文件, 下载视频
5.  合并视频



<u>有的可能需要二次或多次下载m3u8,还有的网站需要解密处理之后才可以得到,下载的ts切片可以用其他工具来进行合并</u>

**案例：**[91视频网](爬虫提速\简单案例-91看剧.py)

代码：

```python
"""
流程:
    1. 拿到548121-1-1.html的页面源代码
    2. 从源代码中提取到m3u8的url
    3. 下载m3u8
    4. 读取m3u8文件, 下载视频
    5. 合并视频(上述下载部分为切片)
"""
import requests
import re

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
# }
#
# obj = re.compile(r'"url":"(?P<url>.*?)",', re.S)        # 用来提取m3u8的url地址
# url = "https://91kju.com/vod-play-id-62944-sid-1-pid-1.html"
#
# resp = requests.get(url, headers=headers)
# m3u8_url = obj.search(resp.text).group('url').replace('\\', '')
# # print(m3u8_url)
# resp.close()
#
# """
# <script>var cms_player = {"yun":true,"url":"https:\/\/m3api.awenhao.com\/index.php?note=kkRsgytw4hnar2b5kjcd9&raw=1&n.m3u8",
# "copyright":0,"name":"pdplayer","jiexi":"https:\/\/www.1717yun.com\/jx\/ty.php?url=","time":3,
# "buffer":"\/\/91kju.com\/Public\/loading\/buffer.html","pause":"\/\/91kju.com\/Public\/loading\/pause.html",
# "next_path":null,"next_url":null,"url_path":"kk_91kju_com_bianyuanxingzhe_62944_8_1_1"};</script>
# """
#
# # 下载m3u8文件
# resp2 = requests.get(m3u8_url, headers=headers)
#
# with open('测试视频.m3u8', mode='wb') as f:
#     f.write(resp2.content)
#
# print(resp2.status_code)
# resp2.close()
# print("下载完成！")

# 解析m3u8文件
n = 1

with open("测试视频.m3u8", mode='r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            # 如果以#开头,我不需要
            continue

        # print(line)
        # 下载ts片段
        resp3 = requests.get(line)
        f = open(f"video/{n}.ts", mode="wb")
        f.write(resp3.content)
        f.close()
        resp3.close()
        n += 1
        print("完成了1个")


```





### 复杂案例-综合训练

**91看剧:**

思路:

1.  拿到主页面的页面源代码, 找到iframe
2.  从iframe的页面源代码中拿到m3u8文件的地址
3.  下载第一层m3u8文件 -> 下载第二层m3u8文件(视频存放路径)
4.  下载视频
5.  下载秘钥, 进行解密操作
6.  合并所有ts文件为一个mp4文件



[综合训练-抓取视频](爬虫提速\综合训练_抓取91看剧完整视频.py)

*时过境迁,该网站网页格式已经发生改变,代码仅作为参考,之后可以找其他网站来练练手*

>flag!



代码:

```python
"""
思路:
    1. 拿到主页面的页面源代码, 找到iframe
    2. 从iframe的页面源代码中拿到m3u8文件的地址
    3. 下载第一层m3u8文件 -> 下载第二层m3u8文件(视频存放路径)
    4. 下载视频
    5. 下载秘钥, 进行解密操作
    6. 合并所有ts文件为一个mp4文件
"""
import requests
from bs4 import BeautifulSoup as bs  # 在这种页面源代码中只有一个iframe，且该iframe正好是需要的iframe的时候，使用bs比较简单
import re
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES
import os


def get_iframe_url(resp):
    main_page = bs(resp.text, 'html.parser')
    src = main_page.find('iframe').get('src')
    return src


def get_m3u8_from_iframe(url):
    resp = requests.get(url)
    m3u8_url = re.search(r'var main = "(?P<m3u8_url>.*?)"', resp.text, re.S).group('m3u8_url')
    return m3u8_url


def download_m3u8_file(url, name):
    resp = requests.get(url)
    with open(name, mode='wb') as f:
        f.write(resp.content)


async def aio_download_task(url, name, session):
    # async with aiohttp.ClientSession() as session
    # 本来在异步任务的第一步是创建会话来进行异步aiohttp请求,但是在异步任务的内部写会导致每次异步(ts下载)都创建一个新的Session,所有在上一层的异步函数内创建Session
    async with session.get(url) as resp:
        # 下载ts切片文件
        async with aiofiles.open(f'video{name}', mode='wb') as f:
            await f.write(await resp.content.read())  # 把下载到的内容写入到文件中
    print(f"{name}下载完毕")


async def aio_download_video(up_url):
    # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/
    tasks = []  # 创建任务列表
    async with aiohttp.ClientSession() as session:  # 提前准备好session
        async with aiofiles.open('second_m3u8.txt', mode='r', encoding='utf-8') as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                # line --> xxxxx.ts
                line = line.strip()  # 格式化
                # 拼接真正的ts文件路径
                ts_url = up_url + line
                # 有了url就开始创建异步任务
                task = asyncio.create_task(aio_download_task(ts_url, line, session))  # 创建任务
                tasks.append(task)  # 把任务加入任务列表
            await asyncio.wait(tasks)  # 当第一个ts进入io操作(下载)时,await,进入下一个ts


def get_key(url):
    resp = requests.get(url)
    return resp.text


async def dec_ts(name, key):
    aes = AES.new(key=key, IV=b'0000000000000000', mode=AES.MODE_CBC)  # 偏移量IV是字节流16位(密钥是几位就是几位)  解码模式默认CBC
    async with aiofiles.open(f'video/{name}', mode='rb') as f1, aiofiles.open(f'video/temp_{name}', mode='wb') as f2:
        # 一个切片打开两个对象,一个读一个写,写的生成temp_新文件
        bs = await f1.read()  # 从源文件读取内容
        await f2.write(aes.decrypt(bs))  # 把解密好的内容写入文件
    print(f"{name}处理完毕")


async def aio_dec(key):
    tasks = []  # 同样是先创建任务列表
    async with aiofiles.open('second_m3u8.txt', mode='r', encoding='utf-8') as f:
        async for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            # 开始创建异步任务
            task = asyncio.create_task(dec_ts(line, key))
            tasks.append(task)
        await asyncio.wait(tasks)


def merge_ts():
    # 不同电脑写法格式不同
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    lst = []
    with open('second_m3u8.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip()
            lst.append(f'video/temp_{line}')

    s = '+'.join(lst)
    os.system(f'copy /b {s} movie.mp4')
    print('搞定!')


def main():
    url = 'https://www.91kanju.com/vod-play/541-2-1.html'
    resp = requests.get(url)
    # 1. 拿到主页面的页面源代码, 找到iframe
    src = get_iframe_url(resp)
    # 拿到iframe的域名
    # "https://boba.52kuyun.com/share/xfPs9NPHvYGhNzFp"
    iframe_url = src.split('/share')[0]

    # 2. 从iframe的页面源代码中拿到m3u8文件的地址
    m3u8_url = get_m3u8_from_iframe(src)
    # 拼接出完整的的m3u8文件下载地址
    first_m3u8_url = iframe_url + m3u8_url
    # https://boba.52kuyun.com/20170906/Moh2l9zV/index.m3u8?sign=548ae366a075f0f9e7c76af215aa18e1

    # 3. 下载第一层m3u8文件 -> 下载第二层m3u8文件(视频存放路径)
    # 先下载第一层m3u8
    download_m3u8_file(first_m3u8_url, 'first_m3u8.txt')
    # 读取m3u8文件,获得第二层m3u8
    with open('first_m3u8.txt', mode='r', encoding='utf-8') as first_m3u8_file:
        for line in first_m3u8_file:
            if line.startswith('#'):
                # m3u8文件中#开头的部分并不是我所需要的
                continue
            else:
                line = line.strip()  # 格式化处理     hls/index.m3u8
                # 拼接出第二层m3u8的路径
                # https://boba.52kuyun.com/20170906/Moh2l9zV/ + hls/index.m3u8
                # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/index.m3u8
                # https://boba.52kuyun.com/20170906/Moh2l9zV/hls/cFN8o3436000.ts
                second_m3u8_url = iframe_url + line
                # 再下载第二层m3u8的内容
                download_m3u8_file(second_m3u8_url, 'second_m3u8.txt')
                print("second_m3u8.txt文件下载完毕")

    # 4. 下载视频
    # 这地方显然是需要异步操作了
    # second_m3u8.txt的解析不能在外面做,需要放在异步函数里面去执行,因为读取.txt文件的操作已经需要异步的处理了
    second_m3u8_url_up = second_m3u8_url.replace("index.m3u8", "")  # 用于拼接
    asyncio.run(aio_download_video(second_m3u8_url_up))

    # 5. 下载秘钥, 进行解密操作
    # 解密的数据很多,且也是多为io操作,显然是异步
    # 首先是要下载密钥
    with open('second_m3u8.txt', mode='r', encoding='utf-8') as second_m3u8_file:
        m3u8_text = ''
        for line in second_m3u8_file:
            m3u8_text += line
        key_url_part = re.search(r'URI="(?P<key_url>.*?)"', m3u8_text, re.S).group('key_url')

    key_url = second_m3u8_url_up + key_url_part
    # 获取密钥的内容
    key_text = get_key(key_url)

    # 解密
    # 需要使用密钥给每一个ts切片文件解密,因此需要异步操作
    asyncio.run(aio_dec(key_text))

    # 6. 合并所有ts文件为一个mp4文件,直接同步操作就行
    # 合并切片的操作,可以由软件来完成,或者是通过程序os.system()来完成合并
    merge_ts()


if __name__ == '__main__':
    main()

```









