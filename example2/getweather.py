#!/usr/bin/env python
# -*- coding: utf-8 -*-


#http://wthrcdn.etouch.cn/weather_mini?city=北京

import requests
import sys
import json

ENCODING = 'utf-8'



def queryRealTimeWeatherInfo(city):
    #url = "http://m.weather.com.cn/data/%s.html" % code
    url = "http://wthrcdn.etouch.cn/weather_mini?city="+city
    print url
    resp = requests.get(url)
    print(resp.text)
    data = json.loads(resp.text)
    if not data:
        print(u"天气预报还没出来".encode(ENCODING))
    return data['data']['forecast'][0]

def showRealTimeWeatherInfo(city,info):
    template = u"{date} {type} 天气实况: 气温:{low}-{high}"
    print(template.format(**info).encode(ENCODING))


def main():
    # assert len(sys.argv) >= 3
    # function = sys.argv[1]
    city = ''.join(sys.argv[1])
    showRealTimeWeatherInfo(city,queryRealTimeWeatherInfo(city))

if __name__ == '__main__':
    main()
