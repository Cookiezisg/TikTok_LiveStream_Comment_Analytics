
import requests


def wechat_user_login():
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://dy.huitun.com',
        'Pragma': 'no-cache',
        'Referer': 'https://dy.huitun.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'mobile': 'xxxxxxxxxxxxx',
        'password': 'xxxxxxxxxxxx',
    }

    response = requests.post('https://login.huitun.com/weChat/userLogin', headers=headers, json=json_data)
    return response.json()


def user_login():
    cookies = {
        '_ga': 'GA1.1.1557684942.1682144720',
        '__root_domain_v': '.huitun.com',
        '_qddaz': 'QD.176582144720017',
        '_clck': 'p57yqs|1|faz|0',
        '_ga_JBKBWWH0KV': 'GS1.1.1682144719.1.1.1682146910.0.0.0',
        '_clsk': 'v2q3o4|1682146910835|8|1|y.clarity.ms/collect',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.1557684942.1682144720; __root_domain_v=.huitun.com; _qddaz=QD.176582144720017; _clck=p57yqs|1|faz|0; _ga_JBKBWWH0KV=GS1.1.1682144719.1.1.1682146910.0.0.0; _clsk=v2q3o4|1682146910835|8|1|y.clarity.ms/collect',
        'Origin': 'https://dy.huitun.com',
        'Pragma': 'no-cache',
        'Referer': 'https://dy.huitun.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'htspm': '',
        'shareid': '',
    }

    json_data = {
        'mobile': 'xxxxxxxxxxx',
        'password': 'xxxxxxxxxxxx',
    }

    response = requests.post('https://dyapi.huitun.com/userLogin', params=params, cookies=cookies, headers=headers, json=json_data)
    return response.cookies.items()


if __name__ == "__main__":
    print(wechat_user_login())
    print(user_login())