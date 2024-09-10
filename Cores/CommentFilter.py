from collections import Counter
import datetime

#清理刷屏
def filter_comments_by_threshold(comments,threshold):
    print(datetime.datetime.now(),'本轮共收集评论数:',len(comments),'待刷屏解析')
    # 统计每个评论出现的次数
    comment_counts = Counter(comments)
    # 确定超过阈值的评论
    over_threshold_comments = {comment for comment, count in comment_counts.items() if count > threshold}
    # 创建一个新的列表来存放最终的评论，只包括未超过阈值的评论
    final_comments = [comment for comment in comments if comment not in over_threshold_comments]
    # 打印最终的评论列表
    print(datetime.datetime.now(),'清理刷屏内容后的评论数为:', len(final_comments))
    return final_comments

#LIVE_ID裁剪
def truncate_strings_in_list(input_list, max_length=12):
    return [string[:max_length] for string in input_list]

#message裁剪
def truncate_message(input_list, head_length,live_id_list_index):
    return [string[head_length-1:] for string in input_list[:-live_id_list_index]]

if __name__ == '__main__':
    # 示例评论列表
    comments = [
        "欢迎来到直播间！",
        "今天的主题是什么？",
        "今天的主题是什么？",
        "大家好！",
        "重复的评论，刷屏用。",
        "重复的评论，刷屏用。",
        "重复的评论，刷屏用。",
        "不要刷屏哦。",
        "再见！",
        "再见！",
    ]
    print(filter_comments_by_threshold(comments,2))