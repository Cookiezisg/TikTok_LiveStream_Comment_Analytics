import pandas as pd
import re
import jieba
import datetime

def cut_word_jieba(content):
    try:
        content_cut = jieba.cut_for_search(content)
        content_cut = str(",".join(content_cut))
        print(datetime.datetime.now(),'内容为：',content,'解析结果为：',content_cut)
        return content_cut
    except:
        pass


#读取文件
all_comments = pd.read_csv('/Collected_Data/all_comments.csv', names=['comments_content', 'sentiment', 'positive_prob', 'neutral_prob', 'negative_prob'])
neg_comments = pd.read_csv('/Collected_Data/neg_comments.csv', names=['comments_content', 'sentiment', 'positive_prob', 'neutral_prob', 'negative_prob'])

# 定义一个函数，用于删除被中括号包围的内容
def remove_bracketed_content(comment):
    return re.sub(r'\[.*?\]', '', comment)
# 定义一个函数，用于删除@用户
def remove_at_to_space(text):
    # This regex finds all occurrences of "@" followed by any characters that are not spaces, and then the nearest space
    return re.sub(r'@[^ ]* ', '', text)

#全部评论数据处理
all_comments['comments_content'] = all_comments['comments_content'].str.split(':').str[-1]#删掉冒号前面无用内容
all_comments['comments_content'] = all_comments['comments_content'].apply(remove_bracketed_content)#删掉表情包内容
all_comments['comments_content'] = all_comments['comments_content'].apply(remove_at_to_space)#删掉表情包内容
all_comments['comments_content'] = all_comments['comments_content'].str.replace(' ', '', regex=False)#去掉空格
all_comments['comments_content'] = all_comments['comments_content'].str.replace(',', '。', regex=False)#去掉英文逗号，防止误判
print(datetime.datetime.now(),'预处理结束，开始分词处理')
all_comments['cutword']=all_comments['comments_content'].astype('str').apply(cut_word_jieba)#分词
all_comments['cutword'] = all_comments['cutword'].str.replace(' ', '', regex=False)#去掉空格
all_comments = all_comments[['comments_content','sentiment','positive_prob','neutral_prob','negative_prob','cutword']]
all_comments.to_csv('all_comments_preprocessed.csv',index=False)
all_comments_preprocessed=all_comments
print(all_comments.head())

#负面评论数据处理
neg_comments['comments_content'] = neg_comments['comments_content'].str.split(':').str[-1]#删掉冒号前面无用内容
neg_comments['comments_content'] = neg_comments['comments_content'].apply(remove_bracketed_content)#删掉表情包内容
neg_comments['comments_content'] = neg_comments['comments_content'].apply(remove_at_to_space)#删掉表情包内容
neg_comments['comments_content'] = neg_comments['comments_content'].str.replace(' ', '', regex=False)#去掉空格
neg_comments['comments_content'] = neg_comments['comments_content'].str.replace(',', '。', regex=False)#去掉英文逗号，防止误判
print(datetime.datetime.now(),'预处理结束，开始分词处理')
neg_comments['cutword']=neg_comments['comments_content'].astype('str').apply(cut_word_jieba)#分词
neg_comments['cutword'] = neg_comments['cutword'].str.replace(' ', '', regex=False)#去掉空格
neg_comments = neg_comments[['comments_content','sentiment','positive_prob','neutral_prob','negative_prob','cutword']]
neg_comments.to_csv('neg_comments_preprocessed.csv',index=False)
neg_comments_preprocessed=neg_comments
print(neg_comments.head())



# 去除停用词
def remove_stopwords(sentence, stopwords):
    if pd.isna(sentence):# 直接返回NaN
        return sentence
    words = sentence.split(',')
    filtered_words = [word for word in words if word not in stopwords]
    return ','.join(filtered_words)


 # 停用词文件列表
stop_words1 = pd.read_csv('../Stopwords-Master/baidu_stopwords.txt', header=None, names=['stopword'], encoding='utf-8')
stop_words2 = pd.read_csv('../Stopwords-Master/cn_stopwords.txt', header=None, names=['stopword'], encoding='utf-8')
#stop_words3 = pd.read_csv('C:/Users/12748/Desktop/TikStreamSentiGather/Stopwords-Master/hit_stopwords.txt', header=None, names=['stopword'], encoding='utf-8')
stop_words4 = pd.read_csv('../Stopwords-Master/scu_stopwords.txt', header=None, names=['stopword'], encoding='utf-8')
stop_words5 = pd.read_csv('../Stopwords-Master/emoji_list.txt', header=None, names=['stopword'], encoding='utf-8')
# 合并所有DataFrame
combined_df = pd.concat([stop_words1,stop_words2,stop_words4,stop_words5])
# 去除重复值
stop_list = combined_df.drop_duplicates()
stop_list.head(200)

# 应用到每个评论
stopwords_list = stop_list['stopword'].tolist()
all_comments_preprocessed['filtered_sentences'] = all_comments_preprocessed['cutword'].apply(lambda x: remove_stopwords(x, stopwords_list))
all_comments_preprocessed = all_comments_preprocessed[['comments_content','sentiment','positive_prob','neutral_prob','negative_prob','cutword','filtered_sentences']]
# 应用到负面评论
neg_comments_preprocessed['filtered_sentences'] = neg_comments_preprocessed['cutword'].apply(lambda x: remove_stopwords(x, stopwords_list))
neg_comments_preprocessed = neg_comments_preprocessed[['comments_content','sentiment','positive_prob','neutral_prob','negative_prob','cutword','filtered_sentences']]

#表情处理
non_chinese_english_pattern = r'[^\u4e00-\u9fffA-Za-z]'
def clean_words_keep_correct_format(sentence):
    if pd.isna(sentence):# 直接返回NaN
        return sentence
    words = sentence.split(',')
    # 对每个词进行清理，然后检查清理后的词是否为空
    cleaned_words = [re.sub(non_chinese_english_pattern, '', word) for word in words if re.sub(non_chinese_english_pattern, '', word)]
    return ','.join(cleaned_words)
# 应用调整后的清理函数到每个句子
all_comments_preprocessed['filtered_sentences'] = all_comments_preprocessed['filtered_sentences'].apply(clean_words_keep_correct_format)
neg_comments_preprocessed['filtered_sentences'] = neg_comments_preprocessed['filtered_sentences'].apply(clean_words_keep_correct_format)
all_comments_preprocessed.to_csv('all_comments_preprocessed.csv',index=False)
neg_comments_preprocessed.to_csv('neg_comments_preprocessed.csv',index=False)
