# -*- coding: utf-8 -*-
import http.cookiejar
import json
import re
import urllib
from urllib import request

import scrapy


from yuntucwpjt.items import YuntucwpjtItem


def getUrllist(url, folderName, type):
    cjar = http.cookiejar.CookieJar()
    request.HTTPCookieProcessor(cjar)
    opener = request.build_opener(request.HTTPCookieProcessor(cjar))
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'),
                         ('Content-Type', 'application/x-www-form-urlencoded')
                         ]
    request.install_opener(opener)
    html = request.urlopen("http://www.tz121.com/index.php/Observation/Satellite", timeout=3).read().decode("utf-8")
    htmlpat = 'name="_token" value="(.*?)"'
    token = re.compile(htmlpat, re.S).findall(html)
    formdata = {"folderName": folderName, "type": type}
    formdata = urllib.parse.urlencode(formdata).encode('utf-8')
    req = urllib.request.Request(url, formdata)
    req.add_header('X-CSRF-Token', token[0])
    data = request.urlopen(req).read().decode('utf-8')
    jsondata = json.loads(data)
    urllist = []
    urlpre = "http://www.tz121.com/radarsatellite/"
    for i in jsondata["data"]:
        urllist.append(urlpre + i)
    return urllist

ulnamelist = ["2GHW", "2GKJ", "2GSQ", "2G"]
class AutospdSpider(scrapy.Spider):
    name = 'autospd'
    allowed_domains = ['tz121.com']
    start_urls = ['http://www.tz121.com/index.php/Observation/Satellite?tdsourcetag=s_pctim_aiomsg']

    def parse(self, response):
        item = YuntucwpjtItem()
        item["_2GHWUrl"]=getUrllist("http://www.tz121.com/index.php/Observation/PostRadarSatellite", "satellite/2GHW","0-sate")
        item["_2GKJUrl"]=getUrllist("http://www.tz121.com/index.php/Observation/PostRadarSatellite", "satellite/2GKJ","0-sate")
        item["_2GSQUrl"]=getUrllist("http://www.tz121.com/index.php/Observation/PostRadarSatellite", "satellite/2GSQ","0-sate")
        item["_2GUrl"]=getUrllist("http://www.tz121.com/index.php/Observation/PostRadarSatellite", "satellite/2G","0-sate")
        item["radarUrl"] = getUrllist("http://www.tz121.com/index.php/Observation/PostRadarSatellite", "RadarPro","0-radar")
        return item



