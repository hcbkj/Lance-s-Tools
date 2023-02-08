import requests

url = 'https://pearvideo.com/'
proxies = {
    "https": "https://183.224.41.199:80"
}

resp = requests.get(url, proxies=proxies)
resp.encoding = 'utf-8'
print(resp.text)
