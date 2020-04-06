#-*- coding: utf-8 -*-
import threading
import requests
import time
import re
from time import sleep


method = "get"
url ="https://zx.tengzhikk.com/api/orders/query"
#url ="https://zx.tengzhikk.com/api/payments/config"
data={'type':'order_id', 'order_id':'QLPD158209387500800140'}
#data={'order_id':'QLPD158209522800800100'}
thread_num =1#线程数
circle_num =2#每个线程循环的次数
loop_sleep =0#每次请求的时间间隔
response_time=[]#平均响应时间列表
error=[]#错误信息列表

class CreateThresd:
    def __init__(self):
        pass
    @classmethod
    def thread_api(cls):
        #请求接口的函数
        global results
        try:
            if method =="post":
                results =requests.post(url,data)
            if method =="get":
                results =requests.get(url,data)
            return results
        except requests.ConnectionError:
            return results

    @classmethod
    def thread_response(cls):
        #响应时间，单位：毫秒
        responsetime =float(CreateThresd.thread_api().elapsed.microseconds)/1000#毫秒
        return  responsetime

    @classmethod
    def thread_response_avg(cls):
        #平均响应时间，单位：毫秒
        avg = 0.000
        l =len(response_time)
        for num in response_time:
            avg +=1.000*num/l
        return avg

    @classmethod
    def thread_time(cls):
        #获取当前时间
        return time.asctime(time.localtime(time.time()))

    @classmethod
    def thread_error(cls):
        try:
            pa =u"情侣姓名配对"
            pattern =re.compile(pa)#创建匹配规则为pa
            match =pattern.search(CreateThresd.thread_api().text)#匹配接口返回的信息是否有相对应的信息
            if CreateThresd.thread_api().status_code == 200:
                #接口返回状态码为200
                pass
                if match.group()==pa:
                #匹配找到的所有信息和规则一样
                   pass
            else:
                error.append(CreateThresd.thread_api().text)#写入错误信息
                print "请求失败,失败信息：",error
                error.pop()
        except AttributeError:
            #尝试访问未知对象属性
            error.append("失败")

    @classmethod
    def thread_work(cls):
        #线程循环
         threadname =threading.currentThread().getName()#返回当前线程的方法
         print "[",threadname,"]Sub Thread Begin"
         for i in range(circle_num):
             CreateThresd.thread_api()
             print "接口请求时间：",CreateThresd.thread_time()
             response_time.append(CreateThresd.thread_response())
             CreateThresd.thread_error()
             sleep(loop_sleep)
         print "[",threadname,"]Sub Thread End"

    @classmethod
    def thread_main(cls):
        start =time.time()#当前时间的时间戳
        threads=[]
        for i in range(thread_num):
            t =threading.Thread(target=CreateThresd.thread_work())#创建线程，执行方法
            t.setDaemon(True)#将子线程标记为守护线程或者用户线程，主线程执行完成后，子线程不管有没有在执行，都会退出，在start前设置
            threads.append(t)
        for t in threads:
            t.start()#启动所有线程
        for t in threads:
            t.join()#主线程中等待所有子进程操作后可继续执行、退出
        end = time.time()
        print"==============================================="
        print"接口性能测试开始时间：",time.asctime(time.localtime(start))
        print"接口性能测试结束时间：",time.asctime(time.localtime(end))
        print"接口地址：",url
        print"接口类型：",method
        print"线程数：",thread_num
        print"每个线程循环次数：",circle_num
        print"每次请求时间间隔：",loop_sleep
        print"总请求数：",thread_num*circle_num
        print"错误请求数：",len(error)
        print"总耗时（秒）：",end-start
        print"每次请求耗时（秒）：",(end-start)/(thread_num*circle_num)
        print"每秒承载请求数（TPS）",(thread_num*circle_num)/(end-start)
        print"平均响应时间（毫秒）",CreateThresd.thread_response_avg()


if __name__ =='__main__':
    CreateThresd.thread_main()