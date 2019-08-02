#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
获取指定简历的截图
'''

import oss2
import requests
import shutil
import json
import os
import re
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import platform
from func_58 import Module_58
from func_hzrc import Module_hzrc
import getpass
from PIL import Image
from selenium import webdriver
from win32api import GetSystemMetrics
import traceback
import logging
from win32com import client as wc
import shutil
import zipfile
import xml.etree.cElementTree as ET
import pythoncom
from func_lp import Module_lp
import fitz   # pip install pyMupdf
import glob
import datetime
import threading
import sys
from settings import *
import configparser
# 外网
# wu_cjbc_url = 'http://********/resume/cleanoutResumes'
#     # 内网：http://********
# wu_cjxw_url = 'http://********/resume/searchResumeStatusForPlugin'
# cra_login_url = 'http://********/pluginlogin/login'


# cra_login_url = 'http://********/pluginlogin/login'
# code_url = 'http://********/crawler/resume/codes'
# plugin_url = 'http://********/crawler/resume/plugin'  # 插件有关，更新cjType--update/save/ask,
py_ini_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'Py_Config.ini'
conf_ini = configparser.ConfigParser(strict=False, allow_no_value=True)
conf_ini.read(py_ini_path, encoding='utf-8')
try:
    API_URL = conf_ini.get("INIT_START", "API_URL")
    PLUGIN_LOGIN_URL = conf_ini.get("INIT_START", "PLUGIN_LOGIN_URL")
    RESUME_DOWNLOAD_URL = conf_ini.get("INIT_START", "RESUME_DOWNLOAD_URL")
    RESUME_CODES_URL = conf_ini.get("INIT_START", "RESUME_CODES_URL")
    RESUME_PLUGIN_URL = conf_ini.get("INIT_START", "RESUME_PLUGIN_URL")
    RESUME_SAVE_URL = conf_ini.get("INIT_START", "RESUME_SAVE_URL")
    POP_OUT_URL = conf_ini.get("INIT_START", "POP_OUT_URL")
    AccessKeyId = conf_ini.get("INIT_START", "AccessKeyId")
    AccessKeySecret = conf_ini.get("INIT_START", "AccessKeySecret")
    BucketName = conf_ini.get("INIT_START", "BucketName")
    BucketUrl = conf_ini.get("INIT_START", "BucketUrl")
    MYSQL_HOST = conf_ini.get("INIT_START", "MYSQL_HOST")
    MYSQL_USER = conf_ini.get("INIT_START", "MYSQL_USER")
    MYSQL_PASSWD = conf_ini.get("INIT_START", "MYSQL_PASSWD")
    MYSQL_DB = conf_ini.get("INIT_START", "MYSQL_DB")
    CLEAN_RESUME_URL = conf_ini.get("INIT_START", "CLEAN_RESUME_URL")
    TIME_RANGE_URL = conf_ini.get("INIT_START", "TIME_RANGE_URL")
    SEARCH_STATUS_URL = conf_ini.get("INIT_START", "SEARCH_STATUS_URL")
    CLEAN_JOB_URL = conf_ini.get("INIT_START", "CLEAN_JOB_URL")
except:
    pass
# 测试
cra_login_url = PLUGIN_LOGIN_URL
code_url = RESUME_CODES_URL
plugin_url = RESUME_PLUGIN_URL  # 插件有关，更新cjType--update/save/ask,
wu_yxbc_url = RESUME_SAVE_URL  # 邮箱简历保存
# driver_jt = webdriver.Chrome()
resp_code_page = requests.get(url=code_url)
resp_code_page.encoding = 'utf-8'
resp_code_dic = json.loads(resp_code_page.text, strict=False)
print(resp_code_dic)

class KThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)
    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class Timeouter(Exception):
    """function run timeout"""


def timeouter(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):
        """真正的装饰器"""
        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))
        def _(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                raise Timeouter(u'function run too long, timeout %d seconds.' % seconds)
            else:
                return result[0]

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _
    return timeout_decorator

def convert_code(jl_data,code_dic,channelid):
    channelid = str(channelid)
    channel_dic = {'1':'zlzpName','2':'qcwyName','3':'tcName','4':'gjwName','5':'hzrcwName','6':'zhycwName',
                   '7':'djwName','8':'bossName','9':'ntName','10':'lpwName','11':'lyName','12':'zgrcrxName',
                   '13':'lgwName','14':'yjsNmae','15':'zgqcrcwName','16':'sxsName','17':'mmName'}
    channel_key = channel_dic[channelid]
    # key_list = ['dutystatus', 'foreignsuffer', 'scale', 'sex', 'education', 'resumestage', 'workproperty', 'comedate', 'memberstatus', 'jobstatus', 'maritalstatus', 'interviewstage', 'remindschedule', 'workyears', 'industry', 'adversevent', 'readstatus', 'political', 'companyproperty', 'resume', 'degree', 'templateuse', 'refusetype', 'callstate', 'channel', 'candidatestatus']
    sub_li = ['objective---work_status', 'objective---job_nature', 'objective---duty_time', 'objective---trade', 'info---marital_status',
              'info---politics_status', 'info---degree', 'info---sex', 'info---oversea_experience', 'jobs---company_nature',
              'jobs---trade', 'jobs---company_scale', 'languages---skill---level', 'educations---degree',
              'languages---language---writing', 'languages---language---speaking']
    # print(len(sub_li))
    for sub_1 in sub_li:
        sub_list = sub_1.split('---')
        if len(sub_list) == 2:
            first_w = sub_list[0]
            second_w = sub_list[1]
            # xxx = jl_data[first_w][second_w]
            # print(second_w)
            if second_w == 'work_status':
                for code_1 in code_dic['jobstatus']:
                    # time.sleep(3)
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        # traceback.print_exc()
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    # traceback.print_exc()
                    pass
            elif second_w == 'job_nature':
                try:
                    for job_na_1_index, job_na_1 in enumerate(jl_data[first_w][second_w]):
                        # print(job_na_1_index)
                        # print(job_na_1)
                        for code_1 in code_dic['workproperty']:
                            try:
                                if job_na_1:
                                    if job_na_1 in code_1[channel_key].split(';'):
                                        jl_data[first_w][second_w][job_na_1_index] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    try:
                        jl_data[first_w][second_w] = [obj_tra_1 for obj_tra_1 in jl_data[first_w][second_w] if isinstance(obj_tra_1, int)]
                        if not jl_data[first_w][second_w]:
                            del jl_data[first_w][second_w]
                    except:
                        pass
                except:
                    pass
            elif second_w == 'duty_time':
                for code_1 in code_dic['comedate']:
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    pass
            elif second_w == 'marital_status':
                for code_1 in code_dic['maritalstatus']:
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    pass
            elif second_w == 'politics_status':
                for code_1 in code_dic['political']:
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    pass
            elif second_w == 'degree' and first_w == 'info':
                for code_1 in code_dic['education']:
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    pass
            elif second_w == 'degree' and first_w == 'educations':
                try:
                    for comp_edu_1_index, comp_edu_1 in enumerate(jl_data[first_w]):
                        for code_1 in code_dic['education']:
                            try:
                                if comp_edu_1[second_w]:
                                    if comp_edu_1[second_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_edu_1_index][second_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    for comp_edu_1_index, comp_edu_1 in enumerate(jl_data[first_w]):
                        try:
                            if not isinstance(comp_edu_1[second_w], int):
                                del comp_edu_1[second_w]
                        except:
                            pass
                except:
                    pass
            elif second_w == 'oversea_experience':
                for code_1 in code_dic['foreignsuffer']:
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    pass
            elif second_w == 'company_nature':
                try:
                    for comp_na_1_index, comp_na_1 in enumerate(jl_data[first_w]):
                        for code_1 in code_dic['companyproperty']:
                            try:
                                if comp_na_1[second_w]:
                                    if comp_na_1[second_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_na_1_index][second_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    for comp_na_2_index, comp_na_2 in enumerate(jl_data[first_w]):
                        try:
                            if not isinstance(comp_na_2[second_w], int):
                                del comp_na_2[second_w]
                        except:
                            pass
                except:
                    pass
            elif second_w == 'trade' and first_w == 'jobs':
                try:
                    for comp_tra_1_index, comp_tra_1 in enumerate(jl_data[first_w]):
                        for code_1 in code_dic['industry']:
                            try:
                                if comp_tra_1[second_w]:
                                    if comp_tra_1[second_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_tra_1_index][second_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    for comp_tra_1_index, comp_tra_1 in enumerate(jl_data[first_w]):
                        try:
                            if not isinstance(comp_tra_1[second_w], int):
                                del comp_tra_1[second_w]
                        except:
                            pass
                except:
                    pass
            elif second_w == 'trade' and first_w == 'objective':
                try:
                    for obj_tra_1_index, obj_tra_1 in enumerate(jl_data[first_w][second_w]):
                        # print(job_na_1_index)
                        # print(job_na_1)
                        for code_1 in code_dic['industry']:
                            try:
                                if obj_tra_1:
                                    if obj_tra_1 in code_1[channel_key].split(';'):
                                        jl_data[first_w][second_w][obj_tra_1_index] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    try:
                        jl_data[first_w][second_w] = [obj_tra_1 for obj_tra_1 in jl_data[first_w][second_w] if isinstance(obj_tra_1, int)]
                        if not jl_data[first_w][second_w]:
                            del jl_data[first_w][second_w]
                    except:
                        pass
                except:
                    pass
            elif second_w == 'company_scale':
                try:
                    for comp_scale_1_index, comp_scale_1 in enumerate(jl_data[first_w]):
                        for code_1 in code_dic['scale']:
                            try:
                                if comp_scale_1[second_w]:
                                    if comp_scale_1[second_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_scale_1_index][second_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    for comp_scale_1_index, comp_scale_1 in enumerate(jl_data[first_w]):
                        try:
                            if not isinstance(comp_scale_1[second_w], int):
                                del comp_scale_1[second_w]
                        except:
                            pass
                except:
                    pass
            elif second_w == 'sex':
                for code_1 in code_dic['sex']:
                    try:
                        if jl_data[first_w][second_w]:
                            if jl_data[first_w][second_w] in code_1[channel_key].split(';'):
                                jl_data[first_w][second_w] = int(code_1['keyValue'])
                            else:
                                continue
                    except:
                        pass
                try:
                    if not isinstance(jl_data[first_w][second_w], int):
                        del jl_data[first_w][second_w]
                except:
                    pass
        elif len(sub_list) == 3:
            first_w = sub_list[0]
            second_w = sub_list[1]
            third_w = sub_list[2]
            try:
                for comp_lang_1_index, comp_lang_1 in enumerate(jl_data[first_w]):
                    if third_w == 'level':
                        for code_1 in code_dic['degree']:
                            try:
                                if comp_lang_1[third_w]:
                                    if comp_lang_1[third_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_lang_1_index][third_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    elif third_w == 'writing':
                        for code_1 in code_dic['degree']:
                            try:
                                if comp_lang_1[third_w]:
                                    if comp_lang_1[third_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_lang_1_index][third_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                    elif third_w == 'speaking':
                        for code_1 in code_dic['degree']:
                            try:
                                if comp_lang_1[third_w]:
                                    if comp_lang_1[third_w] in code_1[channel_key].split(';'):
                                        jl_data[first_w][comp_lang_1_index][third_w] = int(code_1['keyValue'])
                                    else:
                                        continue
                            except:
                                pass
                for comp_lang_1_index, comp_lang_1 in enumerate(jl_data[first_w]):
                    try:
                        if not isinstance(comp_lang_1[third_w], int):
                            del comp_lang_1[third_w]
                    except:
                        pass
            except:
                pass
    return jl_data

now_cwd = os.getcwd()
file_cj_photo = now_cwd + os.sep + 'Mod_Pyth' + os.sep +'Mod_Cj_photo'
if not os.path.exists(file_cj_photo):
    # print('文件夹', new_tj, '不存在，重新建立')
    # os.mkdir(file_path)
    os.makedirs(file_cj_photo)
else:
    shutil.rmtree(file_cj_photo)
    os.makedirs(file_cj_photo)
if 'Mod_Ymjx' in now_cwd:
    now_cwd = now_cwd.replace('\Mod_Ymjx', '')
exe_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'phantomjs.exe'
filedir = now_cwd + os.sep + 'Mod_Pyth' + os.sep + 'Mod_Cj'
filelog = now_cwd + os.sep + 'logging' + os.sep + 'logging.log'
# print(new_tj)
if not os.path.exists(filedir):
    os.makedirs(filedir)
logging.basicConfig(
    level=logging.ERROR,  # 定义输出到文件的log级别，
    format='%(asctime)s : %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    filename=filelog,  # log文件名
    filemode='a')  # 写入模式“w”或“a”
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。
# 强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
yourAccessKeyId = AccessKeyId
yourAccessKeySecret = AccessKeySecret
yourBucketName = BucketName
auth = oss2.Auth(yourAccessKeyId, yourAccessKeySecret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, BucketUrl, yourBucketName)
# 设置存储空间为私有读写权限。
# bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
# 公共读权限
bucket.create_bucket(oss2.OBJECT_ACL_PUBLIC_READ)
oss2.ObjectIterator(bucket, delimiter='/')
# picture_path = r'C:\Users\Administrator\Desktop\123.jpg'
# with open(picture_path, 'rb') as f_58:
#     filename = 'channel_resume/default/default_photo.png'
#     resp_save = bucket.put_object(filename, f_58)
#     save_url = resp_save.resp.response.url
#     print(save_url)
# exit()
def word2pdf(source_path, target_path):
    try:
        pythoncom.CoInitialize()
        word = wc.DispatchEx('Word.Application')
    except:
        pythoncom.CoInitialize()
        word = wc.DispatchEx('kwps.Application')
    try:
        word.Documents.Close()
        word.Documents.Close(word.wdDoNotSaveChanges)
        word.Quit()
    except:
        pass
    word.Visible = 0
    word.DisplayAlerts = 0
    doc = word.Documents.Open(source_path)
    doc.SaveAs(target_path, 17, False, "", True, "", False, False, False, False)
    doc.Close()
    word.Quit()
def pdf2img(source_path, target_path):
    pdffile = glob.glob(source_path)[0]
    doc = fitz.open(pdffile)
    totaling = doc.pageCount

    for pg in range(totaling):
        page = doc[pg]
        zoom = int(100)
        rotate = int(0)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(os.path.join(target_path, '%s.jpg' % str(pg + 1)))
    return totaling
#inputFile为图片的地址，outputFile为输出的地址，saveq为将图片分辨率等比例压缩savep倍
def image2webp(inputFile, outputFile,saveq):
    try:
        image = Image.open(inputFile)
        if image.mode != 'RGBA' and image.mode != 'RGB':
            image = image.convert('RGBA')
        ori_w, ori_h = image.size
        print(int(ori_w*saveq),int(ori_h*saveq))
        newimage=image.resize((int(ori_w*saveq),int(ori_h*saveq)))
        newimage.save(outputFile, 'WEBP')
        print(inputFile + ' has converted to ' + outputFile)
    except Exception as e:
        traceback.print_exc()
        print('Error: ' + inputFile + ' converte failed to ' + outputFile)
headers_jt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
cap = DesiredCapabilities.PHANTOMJS.copy()  # 使用copy()防止修改原代码定义dict
for key, value in headers_jt.items():
    cap['phantomjs.page.customHeaders.{}'.format(key)] = value
driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
# driver_jt.set_page_load_timeout(10)
# driver_jt.set_script_timeout(10)
cookies_basis_58 = '58home=hz; id58=c5/njVrkAq4CHw7fCy2pAg==; city=hz; 58tj_uuid=1f516501-df3b-4ebd-9c53-ecc7b1d9b885; als=0; commontopbar_myfeet_tooltip=end; xxzl_deviceid=Hb6BJKfGNnpCtcAZW5scSlpeq0arRmILCxjIJuH%2Bv2dVGVZgAb3wEV4Ca0Ot5vXV; xxzl_smartid=5df4462181a0e9a59ad660693e06180b; showOrder=1; showPTTip=1; ljrzfc=1; wmda_uuid=3bbb65d735f4aca3baf11990491e042a; wmda_new_uuid=1; wmda_visited_projects=%3B1731916484865; getKey=1; new_uv=18; utm_source=; spm=; init_refer=; new_session=0; ppStore_fingerprint=1E29E49F92B622558C0F49B1EEC5C6D071A46AB80C1100D2%EF%BC%BF1526605436746; PPU="UID=34650726585862&UN=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&TT=5a6401ac9086214f9d16ca3b1086d9e7&PBODY=Z8JmnhEeK5SxeIcyEEsZuf89rEIg-vcNBo40_0H-zkIWAdUIHCbzrQ5Q4XFC48aQrJWcGAMR7B-SUAL7zPYcbl4lIn9oaKBoEvC0g6rIRITDcj5qOOuP3efm-Koeua7KdCyiddcL-DbXX0teXQaq0ynbEV-OeY4OeQK-4vz5MIw&VER=1"; 58cooper="userid=34650726585862&username=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&cooperkey=e27167b5b83925fb7d570f5ce95666ab"; www58com="AutoLogin=true&UserID=34650726585862&UserName=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=887EB60F8846773DB0F871F4A103A2056CDD83AE89F6452A0&Phone=&WltUrl=&UserLoginVer=08CDD29DF3C97588732B3336A726CC43F&LT=1526605454806"; vip=vipusertype%3D0%26vipuserpline%3D0%26v%3D1%26vipkey%3D782bcfd78f29e63156ec0afa9efbfc25%26masteruserid%3D34650726585862; wmda_session_id_1731916484865=1526605965138-4d558735-cb44-1cac'
cookies_basis_hzrc = 'UM_distinctid=163de889caed3-028b380ab63eff-44410a2e-100200-163de889caf41c; _ubm_id.d2cc513d10e26176994c26da25947ea2=1096e84c977a2486; longinUser=wb; Hm_lvt_46b0265c3ac55b35a0fc9e4683094a94=1528508654,1528685759; JSESSIONID=fFwgwAdo1QFX1mrVudLvHNpTntWrDysZgTlsfgj8A1c9cFn9Q-Cw!-196033929; CNZZDATA2145298=cnzz_eid%3D868844613-1528441555-null%26ntime%3D1529560309; _ubm_ses.d2cc513d10e26176994c26da25947ea2=*; Hm_lpvt_46b0265c3ac55b35a0fc9e4683094a94=1529563918'
cookies_basis_zl = "JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976"
cookies_basis_gj = 'ganji_xuuid=c7dc72ef-60db-4264-aced-0a6a701c2cd3.1528708751959; ganji_uuid=7150266604199787963746; xxzl_deviceid=hNmWYgYm3yVBw3yuNYA%2BLPpzVYJGhHRfC9VGkavtS3QxEfmxbyvsUW%2F%2FIgzp8FIi; lg=1; NTKF_T2D_CLIENTID=guestA8ABE4E8-9FE5-DEC9-A48B-EE251D637B74; cityDomain=bj; citydomain=bj; 58tj_uuid=def2acb6-3e85-430a-8c40-c72caf90a077; als=0; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A31561918616%7D; use_https=1; new_uv=3; __utmc=32156897; __utmz=32156897.1529023568.3.3.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; nTalk_CACHE_DATA={uid:kf_10111_ISME9754_557709909}; username_login_n=15669087700; GanjiLoginType=0; __utma=32156897.1024205804.1528708769.1529023568.1529029837.4; GANJISESSID=shdb8t2vgn99tnkn0ofdcgrihf; sscode=9HsRkf041lVH%2BQf39HWsQh54; GanjiUserName=szfl666; GanjiUserInfo=%7B%22user_id%22%3A557709909%2C%22email%22%3A%22%22%2C%22username%22%3A%22szfl666%22%2C%22user_name%22%3A%22szfl666%22%2C%22nickname%22%3A%22%5Cu5e73%5Cu5b89%5Cu6768%5Cu9752%5Cu9752%22%7D; bizs=%5B3%5D; supercookie=AGH3AmN5BGN5WQtlMTMuAmRkMwNlLmOvLGp0ZTMzLzMyMJWvAJZ0BGH0LmpjMwSuMGR%3D; xxzl_smartid=46229e619fb608c62d39dc189295baf9; last_name=szfl666; ganji_login_act=1529044045164'
cookies_basis_lp = 'abtest=0; _fecdn_=1; __uuid=1530527233544.45; __tlog=1530527233545.26%7C00000000%7C00000000%7Cs_00_pz0%7Cs_00_pz0; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1530527234; _mscid=s_00_pz0; _uuid=5A88398AFFA848187736D9B9BF2D2CD8; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1530527255; user_name=%E9%83%AD%E5%AD%90%E6%A1%A2; lt_auth=6L5bbCcFxl76tnGKiGpet69N3dOtU27O9H9Y0RFV1oe%2BD%2F3i4PrlQwOErLIDxBIhlkt3JsULNLP%2B%0D%0AMOr5y3VD6UMTwGmnlYCxuuW70XweTedcdvmi0a72kMzZQslxnXEHyHBg8H9Okx31sUAhN9TvnF7I%0D%0Ap6HH7ral8vvE%0D%0A; UniqueKey=d4d47f8153c841621a667e00ad0d9493; user_kind=1; _l_o_L_=e3c9b446218c5b2bd4d47f8153c841621a667e00ad0d9493; login_temp=islogin; _e_ld_auth_=ac23e04875d8628e; b-beta2-config=%7B%22d%22%3A365%2C%22e%22%3A9612079%2C%22ejm%22%3A%221%22%2C%22n%22%3A%22%25E9%2583%25AD%25E5%25AD%2590%25E6%25A1%25A2%22%2C%22audit%22%3A%221%22%2C%22ecomp_id%22%3A9612079%2C%22photo%22%3A%22%2F%2Fimage0.lietou-static.com%2Fimg%2F5afa5b868e50d906233368cf04a.png%22%2C%22version%22%3A%222%22%2C%22hasPhoneNum%22%3A%221%22%2C%22v%22%3A%222%22%2C%22ecreate_time%22%3A%2220180702%22%2C%22p%22%3A%222%22%2C%22entry%22%3A%221%22%2C%22jz%22%3A%220%22%7D; imClientId=3a3ef6be625ffffc4462f629076d8d2a; imId=3a3ef6be625ffffc5da7d3574f2ad402; fe_lpt_jipinByOneGiveTwo=true; fe_lpt_resumeLib=true; fe_lpt_sevenAnniversaryBegin=true; fe_lpt_realname=true; JSESSIONID=24835A675443F7EA7CF7131A3639013B; __session_seq=34; __uv_seq=34'
cookies_basis_boss = 't=iGi5GHct1hJtEcXs; wt=iGi5GHct1hJtEcXs; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1531788978,1531874497; __c=1531874497; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCwtxAKnPLdPYamZHCAx0xu2z7FldlGtRqlEqZHkU2JxwW_10IbmDQVPG88TAoDGb%26wd%3D%26eqid%3D84749153000331aa000000045b4e8cbb; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1531874825; __a=6342634.1531788976.1531789284.1531874497.18.3.7.18'
cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
cookies_basis_sxs = '__jsluid=b479516d6fb68b555bdf3b04d4d95aee; sxs_usr="2|1:0|10:1531880807|7:sxs_usr|24:dXNyX3lnbG92OGlhdnh5cg==|2a088019793e0f5181ca05d9c09de6b6511c9b0c35e8f00e1375e684b3f84a67"; userflag=company; SXS_XSESSION_ID="2|1:0|10:1531880807|15:SXS_XSESSION_ID|48:ZjAyNzI0NTYtYTJhYi00YjRlLWFkMGYtZTU1OGU4NzE2OThh|87ab5a1f8555f7dbbbacae30c510c055e7bfc75842456a8f43c4c5befad00ac7"; affefdgx=usr_yglov8iavxyr; SXS_XSESSION_ID_EXP="2|1:0|10:1531880807|19:SXS_XSESSION_ID_EXP|16:MTUzNDQ3MjgwNw==|5f37d54f26f71115fadb8462a3f777c2ea7e600f266699a0f4859f703d2abf75"; MEIQIA_EXTRA_TRACK_ID=17JF0z0rxLHrzun3hmKojCV9fxz; gr_cs1_57cc3437-e85d-4913-9e20-797e6c09a06e=user_id%3Anull; gr_session_id_96145fbb44e87b47_57cc3437-e85d-4913-9e20-797e6c09a06e=true; gr_session_id_96145fbb44e87b47=5d9cca33-8fd2-44e3-808e-792a4ab834e2; Hm_lvt_59802bedd38a5af834100b04592579e2=1531880789,1531905358; Hm_lpvt_59802bedd38a5af834100b04592579e2=1531905358; gr_session_id_96145fbb44e87b47_5d9cca33-8fd2-44e3-808e-792a4ab834e2=true; MEIQIA_VISIT_ID=17YDuEFXd92jqzS7Jak0VQMi5T8; SXS_VISIT_XSESSION_ID_V3.0="2|1:0|10:1531905511|26:SXS_VISIT_XSESSION_ID_V3.0|48:ZjAyNzI0NTYtYTJhYi00YjRlLWFkMGYtZTU1OGU4NzE2OThh|0d4f552f74fe5296028dc0e38f05db60fc3dee6640440954f2a4455ebcc15612"; SXS_VISIT_XSESSION_ID_V3.0_EXP="2|1:0|10:1531905511|30:SXS_VISIT_XSESSION_ID_V3.0_EXP|16:MTUzNDQ5NzUxMQ==|e158607ee0e678f5c72eaf35f30ed79d66771f180643b9133604feab50ca0054"'
cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532135172; login_email=3001261262%40qq.com; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
cookies_basis_51 = 'guid=15126185243667940069; EhireGuid=57343d4ab9144eeaaac53570c55c6bd5; RememberLoginInfo=member_name=790EDF22D15A367144E78236FFD81B69&user_name=3F6D7EB2B10CC033; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0VmkU00uiAs0aQA-p00000aaJBdb00000X8ZxsW.THLZ_Q5n1VeHksK85ydEUhkGUhNxndqbusK15y7-uj-BP1fdnj0snvnzrjn0IHY4fW0knHI7wWRsrj-KwD7KwRDYnbfdn1n3rDwaP1Naw0K95gTqFhdWpyfqn10LP1T4PWbLPiusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqPHnzPWb%2526tpl%253Dtpl_10085_16624_12226%2526l%253D1502325280%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m4b66f41d%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D233%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dmonline_3_dg%2526inputT%253D4274%26%7C%26adsnum%3D789233; LangType=Lang=&Flag=1; 51job=cuid%3D52237061%26%7C%26cusername%3D13598213097%26%7C%26cpassword%3D%26%7C%26cname%3D%25D1%25EE%25D2%25F8%25B2%25A8%26%7C%26cemail%3D455471846%2540qq.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0g4r6HYlhTBg%26%7C%26cconfirmkey%3D4555sQmuzH7DE%26%7C%26cresumeids%3D.0Sy8EEE7wagc%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D45usYTv%252FFNEs.%26%7C%26to%3DXmMBaANjCz5cOlo2UTJRYwxzBjYANVU1AT5dNwE5BTQNNlA7D2QLOlF8XTALa1ViBT9UZQM0AWRdYlQ%252BATI%253D%26%7C%26; ps=us%3DXGUCawBgVn4CYVg2B2dXegIzBjVWYwZ9VWIBag0zBXkLMgBuUzALOgJnXzRRMAA7Vm0BOQA2UDJdY1Z4D0QANFxhAjEAFw%253D%253D%26%7C%26needv%3D0; _ujz=NTIyMzcwNjEw; AccessKey=d45a0618ef944d1; partner=baidupz; slife=lastlogindate%3D20180209%26%7C%26; ASP.NET_SessionId=tnj5cjfsmtf5h2nf3avtcvrc; HRUSERINFO=CtmID=2424128&DBID=2&MType=02&HRUID=2788355&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=hzjl340&IsStandard=0&LoginTime=02%2f09%2f2018+09%3a01%3a32&ExpireTime=02%2f09%2f2018+09%3a11%3a32&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=bf9abebe61bef674; KWD=SEARCH='

ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
if r'\\' in ini_p:
    ini_p = ini_p.replace(r'\\', '/')
conf = configparser.ConfigParser(strict=False, allow_no_value=True)
conf.read(ini_p, encoding='utf-8')  # 文件路径
cookfile = conf.get('config', 'pro1')

def time_sec(str_1):
    return str(str_1[0:4]) + '-' + str(str_1[4:6]) + '-' + str(str_1[6:8]) + ' ' + str(str_1[8:10]) + ':' + str(str_1[10:12]) + ':' + str(str_1[12:14])
class Cookie_str2dict(object):
    def __init__(self, cookie):
        self.keys = [i.strip().split('=', 1)[0] for i in cookie.split(';') if '=' in i]
        self.value = [i.strip().split('=', 1)[1] for i in cookie.split(';') if '=' in i]

    def merge(self):
        return dict(zip(self.keys, self.value))
def get_cook_str(cookfile, hostKey, cook_yb):
    cookieFile = cookfile

    LocalFree = windll.kernel32.LocalFree
    memcpy = cdll.msvcrt.memcpy
    CryptProtectData = windll.crypt32.CryptProtectData
    CryptUnprotectData = windll.crypt32.CryptUnprotectData
    CRYPTPROTECT_UI_FORBIDDEN = 0x01

    class DATA_BLOB(Structure):
        _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

    def getData(blobOut):
        cbData = int(blobOut.cbData)
        pbData = blobOut.pbData
        buffer = c_buffer(cbData)
        memcpy(buffer, pbData, cbData)
        LocalFree(pbData)
        return buffer.raw

    def encrypt(plainText):
        bufferIn = c_buffer(plainText, len(plainText))
        blobIn = DATA_BLOB(len(plainText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptProtectData(byref(blobIn), u"python_data", None,
                            None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to encrypt data")

    def decrypt(cipherText):
        bufferIn = c_buffer(cipherText, len(cipherText))
        blobIn = DATA_BLOB(len(cipherText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to decrypt data")

    # 获取cookies，此处cookies需要保存在本地
    conn = sqlite3.connect(cookieFile)
    c = conn.cursor()
    sql = "select host_key, name, value, path,encrypted_value from cookies where host_key like \'%" + hostKey + "%\'"
    c.execute(sql)
    cookies = c.fetchall()
    # print(cookies)
    # print(len(cookies))
    c.close()
    # 加工cookies成字符串
    cookies_list = []
    cookies_all_list = []
    cookies_name_list = []
    cookies_str_zl = cook_yb
    cookies_list0 = cookies_str_zl.split(';')

    for cookie in cookies_list0:
        cookies_name = cookie.split('=')[0].strip()
        cookies_name_list.append(cookies_name)

    cookies_str_list = []
    for row in cookies:
        dc = decrypt(row[4])
        cookie_one2 = str(row[1]) + '=' + str(dc, encoding='utf-8')
        cookies_all_list.append(cookie_one2)
        if str(row[1]) in cookies_name_list:
            cookies_dict = {}
            cookies_dict['domain'] = str(row[0])
            cookies_dict['name'] = str(row[1])
            cookies_dict['value'] = str(dc, encoding='utf-8')
            cookies_dict['path'] = '/'
            cookies_dict['httpOnly'] = False
            cookies_dict['HostOnly'] = False
            cookies_dict['Secure'] = False
            str_cook = str(row[1]) + '=' + str(dc, encoding='utf-8')
            cookies_str_list.append(str_cook)
    cookies_str = ';'.join(cookies_str_list)
    return cookies_str
def change_cookie(driver, hostKey, cookies_str):
    ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
    if r'\\' in ini_p:
        ini_p = ini_p.replace(r'\\', '/')
    conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    conf.read(ini_p, encoding='utf-8')  # 文件路径
    cookfile = conf.get('config', 'pro1')

    LocalFree = windll.kernel32.LocalFree
    memcpy = cdll.msvcrt.memcpy
    CryptProtectData = windll.crypt32.CryptProtectData
    CryptUnprotectData = windll.crypt32.CryptUnprotectData
    CRYPTPROTECT_UI_FORBIDDEN = 0x01

    class DATA_BLOB(Structure):
        _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

    def getData(blobOut):
        cbData = int(blobOut.cbData)
        pbData = blobOut.pbData
        buffer = c_buffer(cbData)
        memcpy(buffer, pbData, cbData)
        LocalFree(pbData)
        return buffer.raw

    def encrypt(plainText):
        bufferIn = c_buffer(plainText, len(plainText))
        blobIn = DATA_BLOB(len(plainText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptProtectData(byref(blobIn), u"python_data", None,
                            None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to encrypt data")

    def decrypt(cipherText):
        bufferIn = c_buffer(cipherText, len(cipherText))
        blobIn = DATA_BLOB(len(cipherText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to decrypt data")

    # 获取cookies，此处cookies需要保存在本地
    conn = sqlite3.connect(cookfile)
    c = conn.cursor()
    sql = "select host_key, name, value, path,encrypted_value from cookies where host_key like \'%" + hostKey + "%\'"
    c.execute(sql)
    cookies = c.fetchall()
    # print(cookies)
    # print(len(cookies))
    c.close()
    # 加工cookies成字符串
    cookies_list = []
    cookies_all_list = []
    cookies_name_list = []
    cookies_list0 = cookies_str.split(';')
    # print(cookies_list0)
    # print(len(cookies_list0))
    for cookie in cookies_list0:
        cookies_name = cookie.split('=')[0].strip()
        cookies_name_list.append(cookies_name)
    # print(cookies_name_list)
    # print(len(cookies_name_list))
    # 数量不一样，找原因
    try:
        driver.maximize_window()
    except:
        pass
    # print(xx)
    # driver.get(url)
    driver.delete_all_cookies()
    for row in cookies:
        # print(row)
        dc = decrypt(row[4])
        cookie_one2 = str(row[1]) + '=' + str(dc, encoding='utf-8')
        cookies_all_list.append(cookie_one2)
        if str(row[1]) in cookies_name_list:
            cookies_dict = {}
            cookies_dict['domain'] = str(row[0])
            cookies_dict['name'] = str(row[1])
            cookies_dict['value'] = str(dc, encoding='utf-8')
            cookies_dict['path'] = '/'
            cookies_dict['httpOnly'] = False
            cookies_dict['HostOnly'] = False
            cookies_dict['Secure'] = False
            try:
                driver.add_cookie(cookies_dict)
            except:
                continue
    return driver
def change_cookie_lg(driver, hostKey, url):
    ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
    if r'\\' in ini_p:
        ini_p = ini_p.replace(r'\\', '/')
    conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    conf.read(ini_p, encoding='utf-8')  # 文件路径
    cookfile = conf.get('config', 'pro1')

    LocalFree = windll.kernel32.LocalFree
    memcpy = cdll.msvcrt.memcpy
    CryptProtectData = windll.crypt32.CryptProtectData
    CryptUnprotectData = windll.crypt32.CryptUnprotectData
    CRYPTPROTECT_UI_FORBIDDEN = 0x01

    class DATA_BLOB(Structure):
        _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

    def getData(blobOut):
        cbData = int(blobOut.cbData)
        pbData = blobOut.pbData
        buffer = c_buffer(cbData)
        memcpy(buffer, pbData, cbData)
        LocalFree(pbData)
        return buffer.raw

    def encrypt(plainText):
        bufferIn = c_buffer(plainText, len(plainText))
        blobIn = DATA_BLOB(len(plainText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptProtectData(byref(blobIn), u"python_data", None,
                            None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to encrypt data")

    def decrypt(cipherText):
        bufferIn = c_buffer(cipherText, len(cipherText))
        blobIn = DATA_BLOB(len(cipherText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to decrypt data")

    # 获取cookies，此处cookies需要保存在本地
    conn = sqlite3.connect(cookfile)
    c = conn.cursor()
    sql = "select host_key, name, value, path,encrypted_value from cookies where host_key like \'%" + hostKey + "%\'"
    c.execute(sql)
    cookies = c.fetchall()
    # print(cookies)
    # print(len(cookies))
    c.close()
    # 加工cookies成字符串
    cookies_list = []
    cookies_all_list = []
    cookies_name_list = []
    try:
        driver.maximize_window()
    except:
        pass
    # print(xx)
    if 'resumeDetailSign' in url:
        driver.get('https://easy.lagou.com')
    driver.delete_all_cookies()
    for row in cookies:
        dc = decrypt(row[4])
        # cookie_one2 = str(row[1]) + '=' + str(dc, encoding='utf-8')
        # cookies_all_list.append(cookie_one2)
        # if str(row[1]) in cookies_name_list:
        cookies_dict = {}
        domain = str(row[0])
        if not domain.startswith('.') and not domain.startswith('www'):
            domain = '.' + domain
        cookies_dict['domain'] = domain
        cookies_dict['name'] = str(row[1])
        cookies_dict['value'] = str(dc, encoding='utf-8')
        cookies_dict['path'] = '/'
        cookies_dict['httpOnly'] = False
        cookies_dict['HostOnly'] = False
        cookies_dict['Secure'] = False
        try:
            driver.add_cookie(cookies_dict)
        except:
            print('出错', domain, str(row[1]), str(dc, encoding='utf-8'))
            continue
    return driver
def jl_jx_email_lg(dict_jl_lg, org_id='', dt=''):
        # 开始解析
        lg_data = {}
        now_year = datetime.datetime.now().year
        # 简历主表
        # print(dict_jl_lg)
        lg_data['info'] = {}
        lg_data['info']['channel'] = 13
        lg_data['info']['channel_resume_id'] = dict_jl_lg["resumeVo"]['id'].strip()
        lg_data['info']['name'] = dict_jl_lg['resumeVo']["name"].strip()
        try:
            if 'www.lgstatic.com' not in dict_jl_lg['resumeVo']["headPic"]:
                photo_url_lg_email = 'https://www.lgstatic.com/thumbnail_160x160/yun/' + dict_jl_lg['resumeVo']["headPic"].strip()
                lg_data['info']['photo_url'] = photo_url_lg_email
        except:
            pass
        try:
            lg_data['info']['mobilephone'] = dict_jl_lg['resumeVo']["phone"].strip()
        except:
            pass
        try:
            lg_data['info']['email'] = dict_jl_lg['resumeVo']["email"].strip()
        except:
            pass
        try:
            lg_data['info']['birth_year'] = int(dict_jl_lg['resumeVo']["birthday"].split(".")[0].strip())
            lg_data['info']['start_working_year'] = int(now_year) - int(
                dict_jl_lg['resumeVo']["workYear"].split("年")[0].strip())
        except:
            pass
        lg_data['info']['degree'] = dict_jl_lg['resumeVo']["highestEducation"].strip()
        lg_data['info']['sex'] = dict_jl_lg['resumeVo']["sex"].strip()
        try:
            lg_data['info']['current_address'] = dict_jl_lg['resumeVo']["liveCity"].strip()
        except:
            pass


        # 求职意向
        try:
            lg_data['objective'] = {}
            lg_data['objective']['self_evaluation'] = dict_jl_lg['resumeVo']["myRemark"].replace("\r", "").replace("\n",
                                                                                                                   "").replace(
                "\t", "").replace(" ", "").replace("<p>", "").replace("</p>", "")
        except:
            pass

        try:
            salary = dict_jl_lg['resumeVo']["expectJob"]["salarys"]  # 薪资要求
            if '保密' in salary or '面议' in salary:
                lg_data['objective']['expected_salary_lower'] = int(0)
                lg_data['objective']['expected_salary_upper'] = int(0)
            elif '-' in salary:
                lg_data['objective']['expected_salary_lower'] = int(
                    salary.replace("k", "").split('-')[0].strip()) * 1000
                lg_data['objective']['expected_salary_upper'] = int(
                    salary.replace("k", "").split('-')[1].strip()) * 1000
            elif "以" in salary:
                lg_data['objective']['expected_salary_lower'] = int(
                    salary.replace("k", "").split('以')[0].strip()) * 1000
                lg_data['objective']['expected_salary_upper'] = int(
                    salary.replace("k", "").split('以')[0].strip()) * 1000
        except:
            pass
        try:
            lg_data['objective']['expected_address'] = []  # 期望工作地点
            expected_address = dict_jl_lg['resumeVo']['expectJob']['city']
            lg_data['objective']['expected_address'].append(expected_address)

            lg_data['objective']['expected_job_title'] = []  # 期望职业
            expected_job_title = dict_jl_lg['resumeVo']['expectJob']['positionName'].replace("<em>", "").replace(
                "</em>", "")
            lg_data['objective']['expected_job_title'].append(expected_job_title)
        except:
            pass
        try:
            lg_data['objective']['job_nature'] = []  # 工作性质
            job_nature = dict_jl_lg['resumeVo']['expectJob']['positionType']
            lg_data['objective']['job_nature'].append(job_nature)
        except:
            pass

        # 求职状态
        try:
            lg_data['objective']['work_status'] = dict_jl_lg['resumeVo']['expectJob']['status']
        except:
            pass

        # 工作经历
        try:
            WorkExperience = dict_jl_lg['resumeVo']["workExperiences"]
            if str(WorkExperience) != "[]":
                lg_data['jobs'] = []
                for job_xinxi in WorkExperience:
                    train_dic = {}
                    try:
                        train_dic['company'] = job_xinxi["companyName"]  # 公司名称
                        train_dic['job_title'] = job_xinxi["positionName"].replace("<em>", "").replace("</em>",
                                                                                                       "")  # 职位名称
                        train_dic['during_start'] = job_xinxi["startDate"].replace(".", "-").split(" ")[
                                                        0] + "-01"  # 开始时间
                    except:
                        traceback.print_exc()
                        pass
                    try:
                        enddate = job_xinxi["endDate"].split(" ")[0]  # 结束时间
                        if enddate == "" or "至今" in enddate:
                            train_dic['during_end'] = "9999-01-01"
                        else:
                            train_dic['during_end'] = enddate.replace(".", "-").split(" ")[0] + "-01"
                    except:
                        traceback.print_exc()
                        pass
                    try:
                        train_dic['job_content'] = job_xinxi["workContent"].replace("\r", "").replace("\n",
                                                                                                      "").replace(
                            "\t", "").replace("<p>", "").replace("</p>", "").replace("<br />", "").replace("<em>",
                                                                                                           "").replace(
                            "</em>", "").strip()  # 工作内容
                    except:
                        traceback.print_exc()
                        pass
                    lg_data['jobs'].append(train_dic)

        except:
            pass

        # 项目经历
        try:
            xm_exp = dict_jl_lg['resumeVo']['projectExperiences']
            if str(xm_exp) != "[]":
                lg_data['projects'] = []
                for pro_in in xm_exp:
                    pro_dic = {}
                    pro_dic['title'] = pro_in['projectName'].strip()  # 项目名称
                    pro_dic['duty'] = pro_in['positionName'].strip()  # 项目名称
                    pro_dic['description'] = pro_in['projectRemark'].replace("\r", "").replace("\n",
                                                                                               "").replace(
                        "\t", "").replace("<p>", "").replace("</p>", "").replace("<br />", "").replace("<em>",
                                                                                                       "").replace(
                        "</em>", "").strip()
                    pro_dic['during_start'] = pro_in['startDate'].strip().replace(".", "-").replace(" ",
                                                                                                    "") + "-01"  # 开始时间
                    try:
                        enddate = pro_in["endDate"].split(" ")[0]  # 结束时间
                        if enddate == "" or "至今" in enddate:
                            pro_dic['during_end'] = "9999-01-01"
                        else:
                            pro_dic['during_end'] = enddate.replace(".", "-").split(" ")[0] + "-01"
                    except:
                        traceback.print_exc()
                        pass
                    lg_data['projects'].append(pro_dic)
        except:
            pass

        # 教育经历
        try:
            EducationExperience = dict_jl_lg['resumeVo']["educationExperiences"]
            if str(EducationExperience) != "[]":
                lg_data['educations'] = []
                try:
                    for edu_dict_jl in EducationExperience[0:]:
                        try:
                            edu_dic = {}
                            edu_dic['school'] = edu_dict_jl["schoolName"]  # 学校名称
                            edu_dic['major'] = edu_dict_jl["professional"]  # 专业名称
                            edu_dic['degree'] = edu_dict_jl["education"]  # 学历
                            try:
                                edu_dic['during_start'] = edu_dict_jl["startDate"].replace(" ", "") + "-09-01"  # 开始时间
                                DateEnd = edu_dict_jl["endDate"].replace(" ", "") + "-06-01"  # 结束时间
                                if DateEnd == "06-01" or "至今" in DateEnd:
                                    edu_dic['during_end'] = "9999-01-01"
                                else:
                                    edu_dic['during_end'] = DateEnd
                            except:
                                pass

                            lg_data['educations'].append(edu_dic)
                        except:
                            pass
                except:
                    traceback.print_exc()
                    pass
        except:
            pass

        # 语言及技能
        try:
            skills_lg = dict_jl_lg['resumeVo']["skillEvaluates"]
            if str(skills_lg) != "[]":
                lg_data['languages'] = []
                for langu_in in skills_lg:
                    try:
                        langu_dic = {}
                        langu_dic['skill'] = langu_in["skillName"].strip()  # 技能名称
                        langu_dic['level'] = langu_in["masterLevel"].strip()  # 掌握程度
                        lg_data['languages'].append(langu_dic)
                    except:
                        pass
        except:
            pass

        # org
        lg_data['org'] = {}
        lg_data['org']['resume_type'] = 1
        lg_data['org']['org_id'] = org_id
        lg_data['org']['job_title'] = dict_jl_lg['positionName']
        lg_data['org']['job_id'] = dict_jl_lg['positionId']
        try:
            if lg_data['info']['mobilephone']:
                lg_data['org']['download_status'] = 1
        except:
            lg_data['org']['download_status'] = 0
        lg_data['org']['receive_time'] = dt
        return lg_data
@timeouter(20)
def get_email_lg(driver, eamil_jl_url, org_id='', dt='', Email=''):
    if 'http://' in eamil_jl_url:
        eamil_jl_url = eamil_jl_url.replace('http://', 'https://')
        print(eamil_jl_url, '6666666')
        # time.sleep(100000)
    # driver = change_cookie_lg(driver, 'lagou.com')
    driver.get(eamil_jl_url)
    lg_email_time = 0
    json_url_id = ''
    while lg_email_time < 6:
        time.sleep(3)
        lg_source_text = driver.page_source
        if 'directRid=' not in lg_source_text and lg_email_time < 6:
            lg_email_time = lg_email_time + 1
            continue
        else:
            lg_email_time = 6
            try:
                json_url_id = lg_source_text.split('directRid=')[1]
                if '&' in json_url_id:
                    json_url_id = json_url_id.split('&')[0]
                print(json_url_id)
            except:
                # traceback.print_exc()
                pass
            print('有了')
    if not json_url_id:
        logging.error('get email {} fail'.format(eamil_jl_url))
        print('get email {} fail'.format(eamil_jl_url))
        return None
    # print(lg_source_text)
    # time.sleep(1000)
    cookies_basis_lg3 = 'user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; JSESSIONID=ABAAABAABCBABEH74BEE5676F9A466A1A56B697BC20DAA7; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; _ga=GA1.3.1173048019.1535530109; _gat=1; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644; Hm_lvt_b53988385ecf648a7a8254b14163814d=1535522015,1535527088,1535527152,1535530126; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1535530126; gate_login_token=698b8e2141e952828d32f2882b133246c5c747cabedc94dc26e6e9780e5022f4'
    cookies_str_lg3 = get_cook_str(cookfile, "easy.lagou.com", cookies_basis_lg3)
    cookie_dic3 = Cookie_str2dict(cookies_str_lg3).merge() if bool(cookies_str_lg3) else dict()
    cookie_jar3 = requests.utils.cookiejar_from_dict(cookie_dic3, cookiejar=None, overwrite=True)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    session3 = requests.Session()
    session3.headers = headers
    session3.cookies = cookie_jar3
    try:
        json_url = 'https://easy.lagou.com/resume/order/' + json_url_id + '.json'
        print(json_url)
        final_url = 'https://easy.lagou.com/can/index.htm?from=gray&directRid=' + json_url_id
        pattern_data_0 = re.compile(r"window.X_Anti_Forge_Code = '(.*?)';")
        # print(login_html_0)
        text_code = pattern_data_0.search(lg_source_text).groups()
        code_str = text_code[0].replace("'", '')
        pattern_data_1 = re.compile(r"window.X_Anti_Forge_Token = '(.*?)';")
        text_token = pattern_data_1.search(lg_source_text).groups()
        token_str = text_token[0].replace("'", '')
        new_headers = session3.headers
        new_headers['X-Anit-Forge-Code'] = code_str
        new_headers['X-Anit-Forge-Token'] = token_str
        new_headers['Referer'] = final_url

        # exit()
        login_html_lg_email = session3.post(url=json_url, headers=new_headers)
        # print(66666666666, new_headers)
        # print(login_html_1.text)
        logging.error('lg email return:' + str(login_html_lg_email.text))
        logging.error(str(new_headers))
        dict_jl_lg = json.loads(login_html_lg_email.text, strict=False)
        print(9999, dict_jl_lg)
        if int(dict_jl_lg['state']) == 1:
            # print(666)
            dict_jl_lg = dict_jl_lg['content']['data']
            lg_jl_data = jl_jx_email_lg(dict_jl_lg, org_id='', dt='')
            # try:
            #     conf = configparser.ConfigParser(strict=False, allow_no_value=True)
            #     conf.read(ini_file, encoding='utf-8')  # 文件路径
            #     org_id = conf.get("config", "orgid")
            # except:
            #     logging.exception("Exception Logged")
            try:
                lg_jl_data['org']['org_id'] = org_id
                lg_jl_data['info']['plugin_url'] = eamil_jl_url
                lg_jl_data['org']['original_email'] = Email
                deliver_dt = time_sec(str(dt))
                lg_jl_data['org']['delivery_time'] = deliver_dt
                # print(final_url)
                save_channel = lg_jl_data['info']['channel']
                jl_data_1 = convert_code(lg_jl_data, resp_code_dic, channelid=save_channel)
                print('准备获取原始简历')
            except:
                traceback.print_exc()
                logging.exception("Exception Logged")
            return lg_jl_data
    except:
        traceback.print_exc()
        # time.sleep(1000)
        logging.exception("Exception Logged")
# driver = change_cookie_lg(driver_jt, 'lagou.com')
# # get_email_lg(driver, 'https://www.lagou.com/nearBy/preview.html?deliverId=1041518597179596800', org_id='', dt='', Email='')
# driver.get('https://www.lagou.com/nearBy/preview.html?deliverId=1041518597179596800')
# time.sleep(10)
# print(driver.page_source)
# exit()
@timeouter(20)
def get_url_intime(driver, url):
    driver.get(url)
    return driver
# 所有渠道共有截图
def save_jl_picture(url, driver, org_id, bucket, channel_png, html=''):
    time_str = str(int(time.time() * 1000))
    filedir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str
    picture_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str + os.sep + channel_png
    print(picture_path)
    picture_path_1 = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str + os.sep + 'bosscj_1.png'
    file_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str + os.sep + 'temp.html'
    # 显示器高GetSystemMetrics(1)
    # 显示器宽GetSystemMetrics(0)
    width = GetSystemMetrics(0)
    if not os.path.exists(filedir):
        # print('文件夹', new_tj, '不存在，重新建立')
        # os.mkdir(file_path)
        os.makedirs(filedir)
    else:
        shutil.rmtree(filedir)
        os.makedirs(filedir)
    # driver.get(url)
    get_time = 0
    if 'zhipin.com' not in url:
        while get_time < 3:
            try:
                driver = get_url_intime(driver, url)
                break
            except:
                time.sleep(10)
                get_time = get_time + 1
                if get_time == 3:
                    shutil.rmtree(filedir)
                    logging.error('something wrong happened-------------timeout')
                    raise Exception('something wrong happened')
    # print(time.time())
    # print(browser.page_source)
    time.sleep(1)
    special_v = 0
    if ".lagou.com" in url and not html:
        try:
            time.sleep(3)
            ele_path = '//div[@id="resumePreviewContainer"]'
            base_salary = driver.find_element_by_xpath(ele_path)
            location = base_salary.location
            # print(location)
            size = base_salary.size
            # print(size)
            # new_height = size['height']
            new_height = location['y'] + size['height'] + 30
            driver.set_window_size(height=new_height, width=width)
            time.sleep(3)
        except:
            pass
    elif ".lagou.com" in url and html:
        with open(file_path, 'w+', encoding='utf-8', errors='ignore') as f_temp:
            lg_head = """
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
            <link href="https://www.lgstatic.com/mds-pipline-fed/searchTalent/page/talent/main_f9343597.css" rel="stylesheet" crossorigin="anonymous">
        </head>
        \n
        <body style="background-color: white">\n
                    """
            f_temp.write(lg_head)
            f_temp.write(html+'</body>\n')
        print('file:///' + file_path)
        driver.get('file:///' + file_path)
        # time.sleep(10)
        driver.execute_script('window.stop()')

    elif 'dajie.com' in url:
        try:
            time.sleep(3)
            try:
                driver.switch_to.frame(driver.find_element_by_id('apply-resume-in'))
                special_v = 1
            except:
                pass
            ele_path = '//html[@class="ua-win ua-wk"]/descendant::div[@class="dj-content-inner"]'
            base_salary = driver.find_element_by_xpath(ele_path)
            location = base_salary.location
            # print(location)
            size = base_salary.size
            # print(size)
            # # new_height = size['height']
            # # 显示器高GetSystemMetrics(1)
            # # 显示器宽GetSystemMetrics(0)
            new_height = location['y'] + size['height']
            if special_v:
                driver.switch_to.default_content()
            driver.set_window_size(height=new_height, width=width)
            time.sleep(3)

        except:
            traceback.print_exc()
            pass
    elif 'zhipin.com' in url:
        with open(file_path, 'w') as f_temp:
            boss_head = """
            <head>
    <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>BOSS直聘</title>
    <link href="https://static.zhipin.com/zhipin/v87/web/boss/css/main.css" type="text/css" rel="stylesheet">
    <script charset="utf-8" src="https://tag.baidu.com/vcard/v.js?siteid=10433020&amp;url=https%3A%2F%2Fwww.zhipin.com%2Fchat%2Fim%3Fmu%3Drecommend&amp;source=&amp;rnd=1460671222&amp;hm=1"></script><script src="https://hm.baidu.com/hm.js?194df3105ad7148dcf2b98a91b5e727a"></script>
</head>
\n
            """
            f_temp.write(boss_head)
            f_temp.write(html)
        driver.get('file:///' + file_path)
        # time.sleep(10)
        driver.execute_script('window.stop()')
        try:
            ele_path_boss = '//div[@class="dialog-container"]'
            base_salary = driver.find_element_by_xpath(ele_path_boss)
            location_boss = base_salary.location
            size_boss = base_salary.size
            # print(location_boss)
            # print(size_boss)
            new_height_boss = location_boss['y'] + size_boss['height'] + 300
            driver.set_window_size(height=new_height_boss, width=width)
            time.sleep(1)
        except:
            ele_path_boss = '//body/div[1]'
            base_salary = driver.find_element_by_xpath(ele_path_boss)
            location_boss = base_salary.location
            size_boss = base_salary.size
            # print(location_boss)
            # print(size_boss)
            new_height_boss = location_boss['y'] + size_boss['height']
            driver.set_window_size(height=new_height_boss, width=width)
            time.sleep(1)
            driver.save_screenshot(picture_path)
    driver.save_screenshot(picture_path)
    if 'zhipin.com' in url:
        # print('boss')
        try:
            ele_path_boss = '//div[@class="dialog-container"]'
            base_salary = driver.find_element_by_xpath(ele_path_boss)
            location_boss = base_salary.location
            size_boss = base_salary.size
            # print(location_boss)
            # print(size_boss)
            rangle_boss = (
            int(location_boss['x']), int(location_boss['y']), int(location_boss['x'] + size_boss['width']),
            int(location_boss['y'] + size_boss['height']))
            img_58 = Image.open(picture_path)
            rangle_img = img_58.crop(rangle_boss)
            rangle_img.save(picture_path)
        except:
            pass
        # print('boss666')
    elif ".lagou.com" in url and html:
        try:
            ele_path_lg = '//body/div[1]'
            base_salary = driver.find_element_by_xpath(ele_path_lg)
            location_lg = base_salary.location
            size_lg = base_salary.size
            # print(location_boss)
            # print(size_boss)
            rangle_boss = (
                int(location_lg['x']), int(location_lg['y']), int(location_lg['x'] + size_lg['width']),
                int(location_lg['y'] + size_lg['height']))
            img_lg = Image.open(picture_path)
            rangle_img = img_lg.crop(rangle_boss)
            rangle_img.save(picture_path)
        except:
            pass
    elif "resumeDetailSign" in url and ".lagou.com" in url:
        try:
            # 对专场简历截图
            ele_path_lg_zc = '//div[@class="resume-content"]'
            base_salary_zc = driver.find_element_by_xpath(ele_path_lg_zc)
            location_lg_zc = base_salary_zc.location
            size_lg_zc = base_salary_zc.size
            # print(location_boss)
            # print(size_boss)
            rangle_boss = (
                int(location_lg_zc['x']), int(location_lg_zc['y']), int(location_lg_zc['x'] + size_lg_zc['width']),
                int(location_lg_zc['y'] + size_lg_zc['height']))
            img_lg = Image.open(picture_path)
            rangle_img = img_lg.crop(rangle_boss)
            rangle_img.save(picture_path)
        except:
            traceback.print_exc()
            pass
    try:
        source_58_xpa_li = ['//div[@class="resDetailRight"]']
        source_zl_xpa_li = ['//div[@id="resume-detail-wrapper"]']
        source_qc_xpa_li = ['//*[@id="divResume"]']
        source_hzrc_xpa_li = ['//div[@class="match-vita"]']   # 在func_hzrc里面处理原始简历
        source_lg_xpa_li = ['//div[@class="resume-content"]', '//div[@class="scrollarea left-content"]']
        source_djw_xpa_li = ['//div[@class="profile-in"]']
        source_zhycw_xpa_li = ['//div[@class="rm-body"]']
        source_sxs_xpa_li = []
        source_boss_xpa_li = []
        source_lp_xpa_li = ['//aside[@class="board"]']
        source_gjw_xpa_li = ['//div[@class="new-resume-wrapper"]']
        if '.ganji.com' in url:
            source_comman_xpa_li = source_gjw_xpa_li
        elif 'zhipin.com' in url:
            source_comman_xpa_li = source_boss_xpa_li
        elif 'zhaopin.com' in url:
            source_comman_xpa_li = source_zl_xpa_li
        elif '51job.com' in url:
            source_comman_xpa_li = source_qc_xpa_li
        elif 'hzrc.com' in url:
            source_comman_xpa_li = source_hzrc_xpa_li
        elif '.58.com' in url:
            source_comman_xpa_li = source_58_xpa_li
        elif '.lagou.com' in url:
            source_comman_xpa_li = source_lg_xpa_li
        elif '.liepin.com' in url:
            source_comman_xpa_li = source_lp_xpa_li
        elif '.dajie.com' in url:
            source_comman_xpa_li = source_djw_xpa_li
        elif '.shixiseng.com' in url:
            source_comman_xpa_li = source_sxs_xpa_li
        elif 'chinahr' in url:
            source_comman_xpa_li = source_zhycw_xpa_li
        for source_xpa_comman in source_comman_xpa_li:
            try:
                # ele_path_boss = '//div[@class="dialog-container"]'
                base_salary = driver.find_element_by_xpath(source_xpa_comman)
                location_boss = base_salary.location
                size_boss = base_salary.size
                # print(location_boss)
                # print(size_boss)
                rangle_boss = (
                int(location_boss['x']), int(location_boss['y']), int(location_boss['x'] + size_boss['width']),
                int(location_boss['y'] + size_boss['height']))
                img_58 = Image.open(picture_path)
                rangle_img = img_58.crop(rangle_boss)
                rangle_img.save(picture_path)
            except:
                pass
    except:
        pass
    with open(picture_path, 'rb') as f_58:
        shotname = time_str + '_' + picture_path.split(os.sep)[-1]
        filename = 'channel_resume/' + org_id + '/' + str(shotname)
        resp_save = bucket.put_object(filename, f_58)
        save_url = resp_save.resp.response.url
    shutil.rmtree(filedir)
    return save_url
# save_jl_picture_lg-----拉钩邮箱专用截图
def save_jl_picture_lg(url, driver, org_id, bucket, channel_png, html=''):
    time_str = str(int(time.time() * 1000))
    filedir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str
    picture_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str + os.sep + channel_png
    picture_path_1 = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str + os.sep + 'bosscj_1.png'
    file_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + time_str + os.sep + 'temp.html'
    # 显示器高GetSystemMetrics(1)
    # 显示器宽GetSystemMetrics(0)
    width = GetSystemMetrics(0)
    if not os.path.exists(filedir):
        # print('文件夹', new_tj, '不存在，重新建立')
        # os.mkdir(file_path)
        os.makedirs(filedir)
    else:
        shutil.rmtree(filedir)
        os.makedirs(filedir)
    # print(time.time())
    # print(browser.page_source)
    time.sleep(1)
    special_v = 0
    # print(url)
    if ".lagou.com" in url:
        try:
            time.sleep(3)
            ele_path = '//div[@id="resumePreviewContainer"]'
            base_salary = driver.find_element_by_xpath(ele_path)
            location = base_salary.location
            # print(location)
            size = base_salary.size
            # print(size)
            # new_height = size['height']
            new_height = location['y'] + size['height'] + 30
            driver.set_window_size(height=new_height, width=width)
            time.sleep(3)
        except:
            pass
    driver.save_screenshot(picture_path)
    with open(picture_path, 'rb') as f_58:
        shotname = time_str + '_' + picture_path.split(os.sep)[-1]
        filename = 'channel_resume/' + org_id + '/' + str(shotname)
        resp_save = bucket.put_object(filename, f_58)
        save_url = resp_save.resp.response.url
    shutil.rmtree(filedir)
    return save_url



def handle_source_jl(driver, filedir):
    while True:
        time.sleep(1)
        try:
            global driver_jt
        except:
            driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
        for parent, dirnames, filenames in os.walk(filedir):
            for filename in filenames:
                full_path = os.path.join(parent, filename)
                try:
                    # print("parent folder is:" + parent)
                    # print(filename)
                    print("filename with full path:\n" + full_path)
                    logging.error("filename with full path:\n" + full_path)

                    with open(full_path, 'r+') as f_1:
                        file_cont = f_1.read()
                        print(file_cont)
                        if not file_cont.startswith('lg--------'):
                            html_lg_1 = ''
                            if 'zhipin.com' in file_cont:
                                try:
                                    html_boss = re.findall("'html': '(.*)</div>'", file_cont, re.S)
                                    file_cont = file_cont.replace(html_boss[0], '')
                                    html_boss_1 = html_boss[0] + "</div>"
                                    html_boss_1 = html_boss_1.replace("'", '"').replace(r"\xa0", '').replace(r"\n", '')
                                except:
                                    traceback.print_exc()
                                    logging.error(file_cont)
                            elif 'lagou.com' in file_cont and "'html': '" in file_cont:
                                try:
                                    html_lg = re.findall("'html': '(.*)</div>'", file_cont, re.S)
                                    file_cont = file_cont.replace(html_lg[0], '')
                                    html_lg_1 = html_lg[0] + "</div>"
                                    html_lg_1 = html_lg_1.replace("'", '"').replace(r"\xa0", '').replace(r"\n", '')
                                except:
                                    traceback.print_exc()
                                    logging.error(file_cont)
                            file_cont = file_cont.replace("'", '"').replace(r"\xa0", '')
                            # print(file_cont)
                            file_cont_dic = json.loads(file_cont, strict=False)
                            plugin_channel_url = file_cont_dic['info']['plugin_url']
                            try:
                                org_id = file_cont_dic['orgId']
                            except:
                                org_id = file_cont_dic['org']['org_id']
                            try:
                                if file_cont_dic['org']['resume_type'] == 3:
                                    file_cont_dic['cjType'] = 'update'
                            except:
                                pass
                            # file_cont_dic['cjType'] = 'save'
                            # print(plugin_channel_url)
                            if '.zhaopin.com' in plugin_channel_url:
                                print(plugin_channel_url)
                                cookie_zl = get_cook_str(cookfile, '.zhaopin.com', cookies_basis_zl)
                                headers_jt['Cookie'] = cookie_zl
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.zhaopin.com', cookies_basis_zl)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'zlcj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    # driver_jt.set_page_load_timeout(10)
                                    # driver_jt.set_script_timeout(10)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.zhaopin.com', cookies_basis_zl)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'zlcj.png')
                                print(oss_url)
                            elif '.51job.com' in plugin_channel_url:
                                cookie_51 = get_cook_str(cookfile, 'ehire.51job.com', cookies_basis_51)
                                headers_jt['Cookie'] = cookie_51
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, 'ehire.51job.com', cookies_basis_51)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'qcwycj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, 'ehire.51job.com', cookies_basis_51)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'qcwycj.png')
                            elif '.ganji.com' in plugin_channel_url:
                                cookie_gj = get_cook_str(cookfile, '.ganji.com', cookies_basis_gj)
                                headers_jt['Cookie'] = cookie_gj
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.ganji.com', cookies_basis_gj)
                                    time.sleep(3.6)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'gjcj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.ganji.com', cookies_basis_gj)
                                    time.sleep(3.6)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'gjcj.png')
                            elif '.hzrc.com' in plugin_channel_url:
                                cookie_hzrc = get_cook_str(cookfile, '.hzrc.com', cookies_basis_hzrc)
                                module_hzrc_0 = Module_hzrc(cookie_hzrc)
                                headers_jt['Cookie'] = cookie_hzrc
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.hzrc.com', cookies_basis_hzrc)
                                    oss_url = module_hzrc_0.save_jl_picture(plugin_channel_url, driver, org_id, bucket)
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.hzrc.com', cookies_basis_hzrc)
                                    oss_url = module_hzrc_0.save_jl_picture(plugin_channel_url, driver, org_id, bucket)
                            elif '.58.com' in plugin_channel_url:
                                # print('开始58')
                                cookie_58 = get_cook_str(cookfile, '.58.com', cookies_basis_58)
                                module_58_0 = Module_58(cookie_58)
                                try:
                                    oss_url = module_58_0.save_jl_picture(plugin_channel_url, driver, org_id, bucket)
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    oss_url = module_58_0.save_jl_picture(plugin_channel_url, driver_jt, org_id, bucket)
                                # print(66666, oss_url)
                            elif '.lagou.com' in plugin_channel_url:
                                if 'resumeDetailSign' in plugin_channel_url:
                                    lg_host = 'easy.lagou.com'
                                else:
                                    lg_host = '.lagou.com'
                                cookie_lg = get_cook_str(cookfile, lg_host, cookies_basis_lg)
                                headers_jt['Cookie'] = cookie_lg
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie_lg(driver, lg_host, plugin_channel_url)
                                    print('拉钩新的Cookies----1', driver.get_cookies())
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'lgcj.png', html_lg_1)
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver = change_cookie_lg(driver_jt, lg_host, plugin_channel_url)
                                    print('拉钩新的Cookies----2', driver.get_cookies())
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'lgcj.png', html_lg_1)
                            elif '.liepin.com' in plugin_channel_url:
                                cookie_lp = get_cook_str(cookfile, '.liepin.com', cookies_basis_lp)
                                headers_jt['Cookie'] = cookie_lp
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.liepin.com', cookies_basis_lp)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'lpcj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.liepin.com', cookies_basis_lp)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'lpcj.png')
                            elif '.chinahr.com' in plugin_channel_url:
                                cookie_zhyc = get_cook_str(cookfile, '.chinahr.com', cookies_basis_zhyc)
                                headers_jt['Cookie'] = cookie_zhyc
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.chinahr.com', cookies_basis_zhyc)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'zhyccj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.chinahr.com', cookies_basis_zhyc)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'zhyccj.png')
                            elif '.dajie.com' in plugin_channel_url:
                                cookie_djw = get_cook_str(cookfile, '.dajie.com', cookies_basis_djw)
                                headers_jt['Cookie'] = cookie_djw
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.dajie.com', cookies_basis_djw)
                                    time.sleep(3.6)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'djwcj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.dajie.com', cookies_basis_djw)
                                    time.sleep(3.6)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'djwcj.png')
                                print(oss_url)
                            elif '.shixiseng.com' in plugin_channel_url:
                                cookie_sxs = get_cook_str(cookfile, '.shixiseng.com', cookies_basis_sxs)
                                headers_jt['Cookie'] = cookie_sxs
                                try:
                                    driver.get(plugin_channel_url)
                                    driver = change_cookie(driver, '.shixiseng.com', cookies_basis_sxs)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket,  'sxscj.png')
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    driver_jt.get(plugin_channel_url)
                                    driver = change_cookie(driver_jt, '.shixiseng.com', cookies_basis_sxs)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'sxscj.png')
                            elif '.zhipin.com' in plugin_channel_url:
                                # print(html_boss_1)
                                try:
                                    # driver.set_page_load_timeout(5)
                                    # driver.set_script_timeout(5)
                                    driver = change_cookie(driver, '.zhipin.com', cookies_basis_boss)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket,  'bosscj.png', html=html_boss_1)
                                except:
                                    driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                    # driver.set_page_load_timeout(5)
                                    # driver.set_script_timeout(5)
                                    driver = change_cookie(driver_jt, '.zhipin.com', cookies_basis_boss)
                                    oss_url = save_jl_picture(plugin_channel_url, driver, org_id, bucket, 'bosscj.png', html=html_boss_1)
                        else:
                            time.sleep(12)
                            cookie_lg = get_cook_str(cookfile, 'lagou.com', cookies_basis_lg)
                            headers_jt['Cookie'] = cookie_lg

                            lg_email_li = file_cont.split('--------')
                            print(lg_email_li)
                            eamil_jl_url = lg_email_li[1]
                            org_id = lg_email_li[4]
                            dt = lg_email_li[3]
                            Email = lg_email_li[2]
                            try:
                                driver = change_cookie_lg(driver, 'lagou.com', eamil_jl_url)
                            except:
                                driver_jt = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                                driver = change_cookie_lg(driver_jt, 'lagou.com', eamil_jl_url)

                            file_cont_dic = get_email_lg(driver, eamil_jl_url, org_id=org_id, dt=dt, Email=Email)
                            lg_get_time = 0
                            while lg_get_time < 3 and not file_cont_dic:
                                time.sleep(30)
                                lg_get_time = lg_get_time + 1
                                file_cont_dic = get_email_lg(driver, eamil_jl_url, org_id=org_id, dt=dt, Email=Email)
                            print(file_cont_dic)
                            oss_url = save_jl_picture_lg(eamil_jl_url, driver, org_id, bucket, 'lgcj.png')
                        logging.error('oss_url---' + oss_url)
                        file_cont_dic['info']['source_url'] = oss_url
                        del_html_label_pat = re.compile('<[^>]+>', re.S)  # 删除html标签
                        # 处理自我介绍中的html标签
                        try:
                            need_del_evaluation = file_cont_dic['objective']['self_evaluation']
                            deled_evaluation = del_html_label_pat.sub('', need_del_evaluation)
                            file_cont_dic['objective']['self_evaluation'] = deled_evaluation.replace('&nbsp;', '')
                        except:
                            pass
                        # 处理工作内容的html标签
                        try:
                            for jobs_index, job_1 in enumerate(file_cont_dic['jobs']):
                                try:
                                    need_del_job_cont = job_1['job_content']
                                    deled_job_cont = del_html_label_pat.sub('', need_del_job_cont)
                                    file_cont_dic['jobs'][jobs_index]['job_content'] = deled_job_cont.replace('&nbsp;', '')
                                except:
                                    pass
                                try:
                                    need_del_job_achi = job_1['achievements']
                                    deled_job_achi = del_html_label_pat.sub('', need_del_job_achi)
                                    file_cont_dic['jobs'][jobs_index]['achievements'] = deled_job_achi.replace('&nbsp;', '')
                                except:
                                    pass
                        except:
                            pass
                        # 处理项目相关内容的html标签
                        try:
                            for pros_index, pro_1 in enumerate(file_cont_dic['projects']):
                                try:
                                    need_del_pro_desp = pro_1['description']
                                    deled_pro_desp = del_html_label_pat.sub('', need_del_pro_desp)
                                    file_cont_dic['projects'][pros_index]['description'] = deled_pro_desp.replace('&nbsp;', '')
                                except:
                                    pass
                                try:
                                    need_del_pro_duty = pro_1['duty']
                                    deled_pro_duty = del_html_label_pat.sub('', need_del_pro_duty)
                                    file_cont_dic['projects'][pros_index]['duty'] = deled_pro_duty.replace('&nbsp;', '')
                                except:
                                    pass
                        except:
                            pass
                        # 处理培训相关内容的html标签
                        try:
                            for trains_index, train_1 in enumerate(file_cont_dic['trainings']):
                                try:
                                    need_del_train_desp = train_1['description']
                                    deled_train_desp = del_html_label_pat.sub('', need_del_train_desp)
                                    file_cont_dic['trainings'][trains_index]['description'] = deled_train_desp.replace(
                                        '&nbsp;', '')
                                except:
                                    pass
                        except:
                            pass
                        print(oss_url)
                        # 处理头像
                        try:
                            if file_cont_dic['info']['channel'] == 3:
                                hostKey_photo_url = '.58.com'
                                cook_yb_photo_url = cookies_basis_58
                            elif file_cont_dic['info']['channel'] == 1:
                                hostKey_photo_url = '.zhaopin.com'
                                cook_yb_photo_url = cookies_basis_zl
                            elif file_cont_dic['info']['channel'] == 7:
                                hostKey_photo_url = '.dajie.com'
                                cook_yb_photo_url = cookies_basis_djw
                            elif file_cont_dic['info']['channel'] == 2:
                                hostKey_photo_url = '.51job.com'
                                cook_yb_photo_url = cookies_basis_51
                            elif file_cont_dic['info']['channel'] == 4:
                                hostKey_photo_url = '.ganji.com'
                                cook_yb_photo_url = cookies_basis_gj
                            elif file_cont_dic['info']['channel'] == 6:
                                hostKey_photo_url = '.chinahr.com'
                                cook_yb_photo_url = cookies_basis_zhyc
                            elif file_cont_dic['info']['channel'] == 8:
                                hostKey_photo_url = '.zhipin.com'
                                cook_yb_photo_url = cookies_basis_boss
                            elif file_cont_dic['info']['channel'] == 5:
                                hostKey_photo_url = '.hzrc.com'
                                cook_yb_photo_url = cookies_basis_hzrc
                            elif file_cont_dic['info']['channel'] == 10:
                                hostKey_photo_url = '.liepin.com'
                                cook_yb_photo_url = cookies_basis_lp
                            elif file_cont_dic['info']['channel'] == 13:
                                hostKey_photo_url = '.lagou.com'
                                cook_yb_photo_url = cookies_basis_lg
                            elif file_cont_dic['info']['channel'] == 16:
                                hostKey_photo_url = '.shixiseng.com'
                                cook_yb_photo_url = cookies_basis_sxs
                            cookies_photo_url = get_cook_str(cookfile, hostKey=hostKey_photo_url,
                                                             cook_yb=cook_yb_photo_url)
                            headers = {
                                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                                'cookie': cookies_photo_url
                            }
                            # 设置请求头信息
                            to_get_photo_url = file_cont_dic['info']['photo_url']
                            response = requests.get(to_get_photo_url, headers=headers)
                            # print(response.content)
                            # 下载二进制数据到本地
                            photo_time_str = str(int(time.time() * 100000)) + '_photo.'
                            photo_ext = file_cont_dic['info']['photo_url'].split('.')[-1]
                            if '?' in photo_ext:
                                photo_ext = photo_ext.split('?')[0]
                            photo_ext_li = ['bmp','jpg','png','webp', 'jpeg','gif']
                            if photo_ext not in photo_ext_li:
                                photo_ext = 'png'
                            photo_url_path = file_cj_photo + os.sep + photo_time_str + photo_ext
                            print(photo_url_path)
                            with open(photo_url_path, 'wb') as f:
                                f.write(response.content)
                            with open(photo_url_path, 'rb') as f_58:
                                shotname = photo_url_path.split(os.sep)[-1]
                                filename = 'channel_resume/' + org_id + '/' + str(shotname)
                                resp_save = bucket.put_object(filename, f_58)
                                save_url = resp_save.resp.response.url
                                file_cont_dic['info']['photo_url'] = save_url
                                print(save_url)
                            try:
                                os.remove(photo_url_path)
                            except:
                                pass
                        except:
                            logging.error('get photo_url fail')
                            logging.exception("Exception Logged")
                            traceback.print_exc()
                            pass
                        try:
                            if file_cont_dic['info']['photo_url']:
                                # pass
                                print('have photo_url')
                        except:
                            file_cont_dic['info'][
                                'photo_url'] = 'http://rsmfiletest.oss-cn-hangzhou.aliyuncs.com/channel_resume%2Fdefault%2Fdefault_photo.png'
                            print('add default photo_url')
                        logging.error('原始简历保存/更新发送---：' + str(file_cont_dic))
                        cj_send = []
                        cj_send.append(file_cont_dic)
                        data = json.dumps(cj_send)
                        data = data.encode('utf-8')
                        if file_cont_dic['org']['resume_type'] == 1:
                            resp_cjxw = requests.post(url=wu_yxbc_url, data=data)
                        elif file_cont_dic['org']['resume_type'] == 3:
                            resp_cjxw = requests.post(url=plugin_url, data=data)
                        logging.error(resp_cjxw)
                        resp_cjxw = resp_cjxw.text
                        # print(resp_cjxw)
                        resp_cjxw_dic = json.loads(resp_cjxw, strict=False)
                        logging.error('原始简历保存/更新返回---：' + resp_cjxw)
                    os.remove(full_path)
                except:
                    traceback.print_exc()
                    # os.remove(full_path)
                    os.remove(full_path)
                    logging.exception("Exception Logged")
                    pass
handle_source_jl(driver_jt,filedir)

