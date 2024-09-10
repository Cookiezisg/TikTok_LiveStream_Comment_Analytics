import json
import os
import csv
import datetime
from aliyunsdkalinlp.request.v20200629 import GetWsCustomizedChGeneralRequest
from aliyunsdkcore.client import AcsClient


access_key_id = 'xxxxxxxxxxxxxxxx'
access_key_secret = 'xxxxxxxxxxxxxxx'

client = AcsClient(
    access_key_id,
    access_key_secret,
    "cn-hangzhou"
)

def Sentiment_analysis(content):
    try:
        request = GetWsCustomizedChGeneralRequest.GetWsCustomizedChGeneralRequest()
        request.set_action_name('GetSaChGeneral')
        request.set_Text(content)
        request.set_ServiceCode("alinlp")
        response = client.do_action_with_exception(request)
        resp_obj = json.loads(response)
        resp_data = json.loads(resp_obj['Data'])
        if resp_data['success'] == True:
            print(resp_data)
            print(datetime.datetime.now(), '评论:\'', content, '\'解析状态:','success','结果如下:')
            print(datetime.datetime.now(),'情感极性:',resp_data['result']['sentiment'],';',\
                  'Positive概率:',resp_data['result']['positive_prob'],';',\
                  'Neutral概率:', resp_data['result']['neutral_prob'], ';',\
                  'Negative概率:',resp_data['result']['negative_prob'],';')
            with open('../Collected_Data/all_comments.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([content, resp_data['result']['sentiment'],\
                                 resp_data['result']['positive_prob'],\
                                 resp_data['result']['neutral_prob'],\
                                 resp_data['result']['negative_prob']])
            if resp_data['result']['sentiment'] == '负面':
                with open('../Collected_Data/neg_comments.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([content, resp_data['result']['sentiment'],\
                                     resp_data['result']['positive_prob'],\
                                     resp_data['result']['neutral_prob'],\
                                     resp_data['result']['negative_prob']])

        else:
            print(datetime.datetime.now(), '评论:\'', content, '\'解析状态:', 'failed')
        return resp_obj
    except:
        pass