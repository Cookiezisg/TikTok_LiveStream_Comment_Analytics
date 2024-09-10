from Spiders.LiveConetnts import DouyinLiveWebFetcher
from Spiders.Login import wechat_user_login
from Spiders.Login import user_login
from Spiders.GetLiveID import get_live_id
from Spiders.OutputMgt import CaptureMgt
from Cores.CommentFilter import truncate_message
from Cores.CommentFilter import filter_comments_by_threshold
from bs4 import BeautifulSoup
from aliyunsdkcore.client import AcsClient
from Cores.SentimentAnalysis import Sentiment_analysis
import requests
import threading
import random
import ctypes
import time
import json
import datetime


def core_func(single_capture_seconds,brush_threshold):

    #阿里云API密钥
    access_key_id = 'xxxxxx'
    access_key_secret = 'xxxxxxx'

    # 创建AcsClient实例
    client = AcsClient(
        access_key_id,
        access_key_secret,
        "cn-hangzhou"
    )

    # 定义一个函数用于强制终止线程
    def terminate_thread(thread):
        if not thread.is_alive():
            return

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, 0)
            print(datetime.datetime.now(),'[Error] 无法终止线程')
        else:
            print(f'{datetime.datetime.now()} 线程{thread.ident}已被终止')

    #灰豚数据网二层登录cookies获取

    timestamp = str(time.time())
    wechat_user_login()
    cookies = {
        'SESSION': str(user_login()[0][1])
    }

    #灰豚数据网主播实施榜单读取
    headers = {}
    params = {
        '_t': timestamp,
        'cat0': '',
        'from': '1',
        'sort': 'gmv'
    }
    response = requests.get('https://dyapi.huitun.com/rank/live/currentTakeGoodsUser', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    json_str = soup.prettify()
    data = json.loads(json_str)
    data = data['data']
    search_content = []

    #基于bing检索特性定位指定直播间重定向网址并解析直播间网址获取live_id
    for i in data:
        print(datetime.datetime.now(), '主播房间名称:',i['nickName'],'主播排名:',i['rank'],'类目:',i['superCategory'])
        search_content.append(i['nickName'] + '抖音直播')



    live_id_list_index=0
    live_id_list=['']*5
    for i in search_content:
        current_live_id = get_live_id(i)
        random_sleep = int(random.randint(0, 2))
        print(datetime.datetime.now(), '为防止bing站点封禁，随机停机，本次停机', random_sleep, '秒')
        time.sleep(random_sleep)
        if current_live_id is not None:
            live_id_list[live_id_list_index] = current_live_id
            print(datetime.datetime.now(), '重定向链接解析直播间', live_id_list_index + 1, '成功;Live_id为', current_live_id)
            live_id_list_index += 1




    # 定义多线程并发抓包func
    def target_function_0():
        DouyinLiveWebFetcher(live_id_list[0]).start()

    def target_function_1():
        DouyinLiveWebFetcher(live_id_list[1]).start()

    def target_function_2():
        DouyinLiveWebFetcher(live_id_list[2]).start()

    def target_function_3():
        DouyinLiveWebFetcher(live_id_list[3]).start()

    def target_function_4():
        DouyinLiveWebFetcher(live_id_list[4]).start()


    # 创建并启动目标函数的线程
    thread0 = threading.Thread(target=target_function_0)
    thread1 = threading.Thread(target=target_function_1)
    thread2 = threading.Thread(target=target_function_2)
    thread3 = threading.Thread(target=target_function_3)
    thread4 = threading.Thread(target=target_function_4)


    with CaptureMgt() as output:
        thread0.start()
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        # 传入单次抓包时长（秒）
        time.sleep(single_capture_seconds)
        # 尝试终止这些线程
        terminate_thread(thread0)
        terminate_thread(thread1)
        terminate_thread(thread2)
        terminate_thread(thread3)
        terminate_thread(thread4)
        print(datetime.datetime.now(), '抓包数据解析中...')
        # 等待线程完全终止
        thread0.join()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()

    #输出预处理
    output = truncate_message(output,40,live_id_list_index)
    # 输出被捕获且同时打印
    print(datetime.datetime.now(), '抓包数据解析成功')
    #清理重复刷屏内容
    output = output[:-1]
    output = filter_comments_by_threshold(output,brush_threshold)
    #情感评分与录入
    for i in output:
        Sentiment_analysis(i)
