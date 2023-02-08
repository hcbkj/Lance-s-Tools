# 1. 拿到contId
# 2. 拿到videoStatus返回的json. -> srcURL
# 3. srcURL里面的内容进行修整
# 4. 下载视频

import requests

url = 'https://www.pearvideo.com/video_1756772'
contId = url.split('_')[-1]

video_status_url = 'https://www.pearvideo.com/videoStatus.jsp?contId=1756772&mrd=0.2239348727181376'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    # 防盗链:溯源, 当前本次请求的上一级是谁
    "Referer": url,
}

resp = requests.get(video_status_url, headers=headers)
dic = resp.json()
systemTime = dic['systemTime']
srcURL = dic['videoInfo']['videos']['srcUrl']
srcURL = srcURL.replace(systemTime, f"cont-{contId}")
# print(srcURL)

# 下载视频
with open("a.mp4", mode='wb') as f:
    f.write(requests.get(srcURL).content)

print("over!")
