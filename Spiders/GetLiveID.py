import re
import requests
from lxml.html import etree

def get_live_id(search_content):
    def get_bing_url(keywords):
        keywords = keywords.strip('\n')
        bing_url = re.sub(r'^', 'https://cn.bing.com/search?q=', keywords)
        bing_url = re.sub(r'\s', '+', bing_url)
        return bing_url


    bing_url = get_bing_url(search_content)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'cookie':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' }
    for i in range(1, 2):  # 通过for in来翻页
        if i == 1:
            url = bing_url
        else:
            url = bing_url + '&qs=ds&first=' + str((i * 10) - 1) + '&FORM=PERE'
        content = requests.get(url=url, timeout=5, headers=headers)
        # 获取content中网页的url
        tree = etree.HTML(content.text)
        li = tree.xpath('//ol[@id="b_results"]//li[@class="b_algo"]')[0] # [0] query the first result

    try:
        h3 = li.xpath('//h2/a')
        for h in h3:
            result_url = h.attrib['href']  # 获取网页的url
            text = str(h.text)  # 获取网页的标题
            match = re.search(r"https://live\.douyin\.com/(\d+)", str(result_url))
            if match:
                return match.group(1)
            else:
                pass
    except Exception:
        return None

