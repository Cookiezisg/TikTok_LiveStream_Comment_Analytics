from Cores.CoreContral import contral_func

'''
sustain_days:项目总持续天数    默认值=0
sustain_hours:项目总持续小时数    默认值=0
sustain_minutes:项目总持续分钟数    默认值=0
sustain_seconds:项目总持续秒数    默认值=0
single_capture_days:单次抓包持续天数    默认值=0
single_capture_hours:单次抓包持续小时数    默认值=0
single_capture_minutes:单次抓包持续分钟数    默认值=0
single_capture_seconds:单次抓包持续秒数    默认值=0
brush_threshold:判定刷屏阈值    默认值=10
'''
contral_func(sustain_seconds=30,single_capture_seconds=10,brush_threshold=10)