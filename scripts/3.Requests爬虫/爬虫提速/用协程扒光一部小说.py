# http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"}  => 所有章节的内容(名称, cid)
# 章节内部的内容
# http://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|11348571","need_bookinfo":1}

import requests
import asyncio
import aiohttp
import aiofiles
import json

"""
1. 同步操作: 访问getCatalog 拿到所有章节的cid和名称
2. 异步操作: 访问getChapterContent 下载所有的文章内容
"""


async def getCatalog(url):
    # 此时还没有其他任务会和该任务⼀起并⾏执⾏. 所以完全没必要⽤异步
    resp = requests.get(url)
    # print(resp.text)
    dic = resp.json()
    tasks = []
    for item in dic['data']['novel']['items']:
        # item就是对应的每一个章节的名称和cid
        title = item['title']
        cid = item['cid']       # 每一个cid都是一个url, 异步任务
        # 准备异步任务
        tasks.append(aiodownload(cid, b_id, title))
        print(cid, title)

    await asyncio.wait(tasks)


async def aiodownload(cid, b_id, name):
    data = {
        "book_id": b_id,
        "cid": f"{b_id}|{cid}",
        "need_bookinfo": 1,
    }
    # 因为是json,需要变成json字符串
    data = json.dumps(data)
    url = f"http://dushu.baidu.com/api/pc/getCatalog?data={data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.json()
            # 异步的文件读写
            async with aiofiles.open('novel/'+name, mode='w', encoding='utf-8') as f:
                await f.write(dic['data']['novel']['content'])        # 把小说内容写入
    print(name, "下载完成")


if __name__ == '__main__':
    b_id = "4306063500"
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + b_id + '"}'
    asyncio.run(getCatalog(url))
    # print(url)
