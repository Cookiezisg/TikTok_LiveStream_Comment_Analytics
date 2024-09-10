import datetime
import time
from Cores.CoreFunc import core_func
def contral_func(sustain_days=0, sustain_hours=0, sustain_minutes=0, sustain_seconds=0,\
              single_capture_days=0, single_capture_hours=0, single_capture_minutes=0, single_capture_seconds=0,\
                 brush_threshold=10):
    sustain_time = datetime.timedelta(days=sustain_days, hours=sustain_hours, \
                                      minutes=sustain_minutes, seconds=sustain_seconds)
    single_capture_times = datetime.timedelta(days=single_capture_days, hours=single_capture_hours,\
                                              minutes=single_capture_minutes, seconds=single_capture_seconds)
    end_time = datetime.datetime.now() + sustain_time
    program_start_time = datetime.datetime.now()
    print(datetime.datetime.now(),'项目开始运行')
    print(datetime.datetime.now(),'项目设定总运行时长为:',sustain_time)
    print(datetime.datetime.now(), '项目设定终止时间:', end_time)
    print(datetime.datetime.now(),'项目设定单次并行抓包运行时长为:',single_capture_times)
    single_capture_seconds = int(single_capture_times.total_seconds())
    func_run_times = 1
    while True:
        if datetime.datetime.now() < end_time:
            subroutine_start_time = datetime.datetime.now()
            print(datetime.datetime.now(),'项目子程序循环运行第',func_run_times,'次')
            time.sleep(5)#到时候替换成core
            try:
                core_func(single_capture_seconds,brush_threshold)
            except:
                pass
            if datetime.datetime.now() < subroutine_start_time + single_capture_times:
                print(datetime.datetime.now(),'项目子程序出现错误，请及时排查，为防止api额度浪费，休息预定单次抓包时长:',single_capture_times)
                time.sleep(single_capture_seconds)
            else:
                print(datetime.datetime.now(),'项目子程序第',func_run_times,'次运行成功，本次运行时长:',datetime.datetime.now()-subroutine_start_time)
            func_run_times += 1
        else:
            print(datetime.datetime.now(),'预设运行时间已达成，共运行子程序',func_run_times,'次')
            print(datetime.datetime.now(), '预设结束时间:', end_time, '总程序运行时间:',datetime.datetime.now()-program_start_time)
            print(datetime.datetime.now(), '请回收数据进行分析')
            break


if __name__ == '__main__':
    contral_func(sustain_seconds=10,single_capture_seconds=5)