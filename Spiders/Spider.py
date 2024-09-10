from bs4 import BeautifulSoup
import requests

cookies = {
    'SESSION': 'OWM5ZDI4NWQtNTJhNi00ZDZiLWI5YzItODY2ZTVhYmU2YmM1'
}

headers = {}

params = {
    '_t': '1709884916549',
    'cat0': '',
    'from': '1',
    'sort': 'gmv'
}

response = requests.get('https://dyapi.huitun.com/rank/live/currentTakeGoodsUser', params=params, cookies=cookies, headers=headers)

# 使用 Beautiful Soup 解析 HTML

soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

# 打印出整个 HTML 内容，您可以替换这部分来提取您需要的具体信息
print(soup.prettify())
