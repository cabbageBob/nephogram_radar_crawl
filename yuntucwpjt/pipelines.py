# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import logging
import os
from urllib import request

from logging.handlers import TimedRotatingFileHandler
from dateutil import parser
import datetime

class YuntucwpjtPipeline(object):
    def mymkdir(self,path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(path + ' 目录已存在')
            return False

    def get_logger(self,loggerName):
        LOG_FILE = r'C:\Users\Administrator\Desktop\yuntulog\nephogram.log'
        handler = TimedRotatingFileHandler(LOG_FILE, when='D', backupCount=5, encoding='utf-8')
        fmt = '%(asctime)s- %(name)s  - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger = logging.getLogger(loggerName)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger
    def process_item(self, item, spider):
        self.nephogramJob(item,"_2GHWUrl")
        self.nephogramJob(item, "_2GKJUrl")
        self.nephogramJob(item, "_2GSQUrl")
        self.nephogramJob(item, "_2GUrl")
        self.radarJob(item)

        return item

    def nephogramJob(self,item,itemname):
        for j in item[itemname]:
            dirname = j.split("/")
            filename = dirname[7]
            strlist = filename.split("_")
            datestr = strlist[1] + strlist[2] + strlist[3] + " " + strlist[4] + strlist[5]
            datetime_struct = parser.parse(datestr)
            eighthourdate = datetime_struct + datetime.timedelta(hours=8)
            eighthourdatestr = eighthourdate.strftime('%Y%m%d')
            eighthourdate_str = eighthourdate.strftime('%Y_%m_%d_%H_%M')
            newfilename = "FY2G_" + eighthourdate_str + "_M_PJ2_3D.JPG"
            if itemname == "_2GHWUrl":
                nephogramname = "hongwai"
            elif itemname == "_2GKJUrl":
                nephogramname = "kejianguang"
            elif itemname == "_2GSQUrl":
                nephogramname = "shuiqi"
            else:
                nephogramname = "liti"
            print("开始获取" + nephogramname + "的图片")
            path = "D:\\Java\\apache-tomcat-6.0.32\\webapps\ROOT\\NBSL\\nb_nephogram\\"+nephogramname+"\\"+eighthourdatestr
            # path = "F:\pythonLearning\myspider\images\yuntu\\" + nephogramname + "\\" + eighthourdatestr
            self.mymkdir(path)
            imagename = "D:\\Java\\apache-tomcat-6.0.32\\webapps\ROOT\\NBSL\\nb_nephogram\\"+nephogramname+"\\"+eighthourdatestr+"\\"+newfilename
            # imagename = "F:\pythonLearning\myspider\images\yuntu\\" + nephogramname + "\\" + eighthourdatestr + "\\" + newfilename
            if os.path.exists(imagename):
                continue
            try:
                request.urlretrieve(j, filename=imagename)
            except BaseException as e:
                self.get_logger('nephogram').error(e)
                print(imagename + "获取失败")

    def radarJob(self,item):
        print("开始获取RadarPro的照片")
        for j in item["radarUrl"]:
            dirList = j.split("/")
            dirname = dirList[5]
            time = dirList[6].split(".")[2][0:4]
            datetime_struct = parser.parse(dirname + time)
            eighthourdate = datetime_struct + datetime.timedelta(hours=8)
            path = "D:\\Java\\apache-tomcat-6.0.32\\webapps\ROOT\\NBSL\\zjradar_new\\" + dirname
            # path = "F:\pythonLearning\myspider\images\yuntu\\zjradar_new\\"+dirname
            self.mymkdir(path)
            imagename = eighthourdate.strftime('%Y%m%d%H%M')
            imagepath = "D:\\Java\\apache-tomcat-6.0.32\\webapps\ROOT\\NBSL\\zjradar_new\\" + dirname + "\\" + imagename + ".png"
            # imagepath = "F:\pythonLearning\myspider\images\yuntu\\zjradar_new\\"+dirname+"\\"+imagename+".png"
            if os.path.exists(imagename):
                continue
            try:
                request.urlretrieve(j, filename=imagepath)
            except BaseException as e:
                self.get_logger('radar').error(e)
                print(e)
                print(imagename + "获取失败")
