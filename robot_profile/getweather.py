#!/usr/bin/env python
# -*- coding: utf-8 -*-


#http://wthrcdn.etouch.cn/weather_mini?city=北京

import requests
import sys
import json

ENCODING = 'utf-8'



def queryRealTimeWeatherInfo(city):
    #url = "http://m.weather.com.cn/data/%s.html" % code
    url = u"http://wthrcdn.etouch.cn/weather_mini?city="+city
    resp = requests.get(url)
    data = json.loads(resp.text)
    # print(data)
    ret = None
    try:
        ret = data['data']['forecast'][0]
    except:
        # print(u"天气预报还没出来")
        return None
    return ret

def showRealTimeWeatherInfo(city,info):
    if info==None:
        print("不知道",city,"是哪里")
        return
    print(city+":")
    template = u"{date} {type} 天气实况: 气温:{low}-{high}"
    print(template.format(**info))


def main():
    # assert len(sys.argv) >= 3
    # function = sys.argv[1]
    city = "".join(sys.argv[1:])
    # print(city)
    # city ="上海"
    showRealTimeWeatherInfo(city,queryRealTimeWeatherInfo(city))

if __name__ == '__main__':
    main()
