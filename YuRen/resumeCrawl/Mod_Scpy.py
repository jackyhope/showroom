#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
获取邮箱中的简历并清洗
'''


from PIL import Image, ImageEnhance, ImageOps
import shutil
import execjs
import logging
import oss2
import requests
import psutil
import ctypes
import traceback
import datetime
from PIL import Image, ImageEnhance
import random
import numpy as np
import zipfile
import skimage
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3
import configparser
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import pymysql
import re
import time
from cache_clear import run_clear
import os
import codecs
import urllib.request
import win32com.client
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse, splitquery
import base64
import scrapy
from time import sleep
import chardet
import binascii
from pyDes import des, ECB, PAD_PKCS5
import threading
import multiprocessing
import urllib
import sys
import subprocess
import winreg
import wx
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import al_qf,zl_xghs,func_lg
from func_51 import Module_51
from func_hzrc import Module_hzrc
from func_lg import Module_lg
# from func_gj import Module_gj
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.utils import parsedate
import uuid
from win32com import client as wc
import shutil
import zipfile
import xml.etree.cElementTree as ET
import pythoncom
from func_lp import Module_lp
import fitz   # pip install pyMupdf
import glob
import platform
import getpass
from settings import *
import random
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3
import configparser
import os
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
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
wu_jl_url = RESUME_SAVE_URL  # 邮箱简历保存
code_url = RESUME_CODES_URL
resp_code_page = requests.get(url=code_url)
resp_code_page.encoding = 'utf-8'
resp_code_dic = json.loads(resp_code_page.text)
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
def get_oss_url(rootdir):
    imagefile = []
    new_height = 0
    new_width = 0
    page_height = 0
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            temp_1_name, temp_1_ext = os.path.splitext(f)
            if temp_1_ext in ['.jpg', '.png', '.jpeg']:
                if 'image' not in temp_1_name and 'result' not in temp_1_name:
                    try:
                        print('处理', f)
                        img_temp_1 = Image.open(rootdir + '/' + f)
                        new_height = new_height + img_temp_1.size[1]
                        new_width = img_temp_1.size[0]
                        page_height = img_temp_1.size[1]
                        imagefile.append(img_temp_1)
                    except:
                        pass
    target = Image.new('RGB', (new_width, new_height))  # 最终拼接的图像的大小为(229*3) * (229*6)
    left = 0
    right = page_height
    for image in imagefile:
        target.paste(image, (0, left, new_width, right))
        left += page_height  # 从上往下拼接，左上角的纵坐标递增
        right += page_height  # 左下角的纵坐标也递增　
        quality_value = 100
        target.save(rootdir + '/result.jpg', quality=quality_value)
    webp_from = rootdir + '/result.jpg'
    # webp_to = rootdir + '/result.webp'
    # image2webp(webp_from, webp_to, 1)
    with open(webp_from, 'rb') as f1:
        shotname = str(int(time.time() * 1000)) + '_' + webp_from.split(os.sep)[-1]
        file_oss = 'channel_resume/' + org_id + '/' + str(shotname)
        # print(file_oss)
        resp_save = bucket.put_object(file_oss, f1)
        save_url = resp_save.resp.response.url
        return save_url
def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.makedirs(unziptodir)
    else:
        shutil.rmtree(unziptodir)
        os.makedirs(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        print('******', len(parts))
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
# 文件转化
def doc_xml(source_doc):
    (filepath_1, tempfilename_1) = os.path.split(source_doc)
    (shotname_1, extension_1) = os.path.splitext(tempfilename_1)
    target_docx = filepath_1 + os.sep + shotname_1 + '.docx'
    # print(target_docx)
    target_path = filepath_1 + os.sep + shotname_1
    target_rar = filepath_1 + os.sep + shotname_1 + '.rar'
    pythoncom.CoInitialize()
    word = wc.DispatchEx('Word.Application')
    try:
        word.Documents.Close()
        word.Documents.Close(word.wdDoNotSaveChanges)
        word.Quit()
    except:
        pass
    word.Visible = 0
    word.DisplayAlerts = 0
    print(source_doc)
    doc = word.Documents.Open(source_doc)  # 目标路径下的文件
    doc.SaveAs(target_docx, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
    doc.Close()
    word.Quit()
    os.rename(src=target_docx, dst=target_rar)
    file = zipfile.ZipFile(target_rar)  # 这里写入的是需要解压的文件，别忘了加路径
    file.extractall(target_path)  # 这里写入的是你想要解压到的文件夹
    return_file = target_path + os.sep + 'word' + os.sep + 'document.xml'
    return return_file

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
def get_date(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset, errors='ignore')
    return value
def time_sec(str_1):
    return str(str_1[0:4]) + '-' + str(str_1[4:6]) + '-' + str(str_1[6:8]) + ' ' + str(str_1[8:10]) + ':' + str(str_1[10:12]) + ':' + str(str_1[12:14])

def get_useragent():
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
        "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent
def head_reqst():
    useragent = get_useragent()
    headers = {
        'User-Agent': useragent,
    }
    return headers
def sjxg(str_1):
    str_list = str_1.split('-')
    if int(str_list[1]) > 12:
        str_list[1] = '12'
    elif int(str_list[1]) < 1:
        str_list[1] = '1'
    else:
        pass
    new_str = '-'.join(str_list)
    return new_str
def first_show(s, list_1):
    list2 = []
    for ss1 in list_1:
        if ss1 in s:
            ss1_inx = s.index(ss1)
            list2.append(ss1_inx)
        else:
            pass
    return min(list2)
def riqizhaunhuan(xx):
    xx_li = xx.split('-')
    for index,value in enumerate(xx_li):
        if int(value) <= 9 and len(str(value)) == 1:
            xx_li_temp = '0' + str(value)
            xx_li[index] = xx_li_temp
    return '-'.join(xx_li)
def hzrc_email(module_hzrc_01, xz_url, dt_2):
    xz_url_stat = True
    while xz_url_stat:
        # print(6666666)
        dt_sec = time_sec(str(dt_2))
        hzrc_jl_li = []
        try:
            xz_return = module_hzrc_01.email_dl(xz_url)
            if xz_return == 'zip':
                rootdir_jl = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc' + os.sep + 'download' + os.sep + 'jl'
                logging.error("scpy email hzrc zip begin")
                unzip_file('Mod_Pyth/hzrc/download/hzrc.zip', 'Mod_Pyth/hzrc/download/jl')
                for parent, dirnames, filenames in os.walk(rootdir_jl):
                    for filename in filenames:
                        time.sleep(2)
                        try:
                            (name_1, extension_1) = os.path.splitext(filename)
                            filename_doc = rootdir_jl + os.sep + filename
                            filename_pdf = rootdir_jl + os.sep + name_1 + '.pdf'
                            xml_file = doc_xml(filename_doc)
                            word2pdf(filename_doc, filename_pdf)
                            pdf2img(filename_pdf,rootdir_jl)
                            save_url = get_oss_url(rootdir_jl)
                            hzrc_jl = jx_hzrc_email(xml_file, job_id='', org_id=org_id, dt=dt_sec)
                            hzrc_jl['info']['source_url'] = save_url
                            hzrc_jl_li.append(hzrc_jl)
                            print(hzrc_jl)
                        except:
                            # xz_url_stat = False
                            logging.error("scpy email hzrc zip fail")
                            traceback.print_exc()
            elif xz_return == 'doc':
                rootdir_jl = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc' + os.sep + 'download'
                logging.error("scpy email hzrc doc begin")
                try:
                    filename_doc = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc' + os.sep + 'download' + os.sep + 'hzrc.doc'
                    filename_pdf = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc' + os.sep + 'download' + os.sep + 'hzrc.pdf'
                    xml_file = doc_xml(filename_doc)
                    word2pdf(filename_doc, filename_pdf)
                    pdf2img(filename_pdf, rootdir_jl)
                    save_url = get_oss_url(rootdir_jl)
                    hzrc_jl = jx_hzrc_email(xml_file, job_id='', org_id=org_id, dt=dt_sec)
                    hzrc_jl['info']['source_url'] = save_url
                    hzrc_jl_li.append(hzrc_jl)
                    print(hzrc_jl)
                except:
                    xz_url_stat = False
                    logging.error("scpy email hzrc doc fail")
                    traceback.print_exc()
            xz_url_stat = False
            # print(8888888888)
            logging.error("scpy email hzrc return data")
            return hzrc_jl_li
        # time.sleep(1000)
        except:
            logging.exception("Exception Logged")
            logging.error("scpy email def hzrc_email()  fail")
            xz_url_stat = False
            traceback.print_exc()

def jx_hzrc_email(xml_file, job_id='', org_id='111', dt=''):
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    hzrcl_data = {}
    hzrcl_data['info'] = {}
    hzrcl_data['info']['channel'] = 5
    # namespace = str(int(time.time() * 1000)) + 'qftx'
    hzrcl_data['info']['channel_resume_id'] = str(uuid.uuid1())
    # hzrcl_data['info']['channel_update_time'] = dt
    hzrcl_data['objective'] = {}
    hzrcl_data['objective']['expected_job_title'] = []
    hzrcl_data['objective']['expected_address'] = []
    hzrcl_data['objective']['trade'] = []
    hzrcl_data['objective']['job_nature'] = []
    hzrcl_data['objective']['individual_label'] = []
    hzrcl_data['jobs'] = []
    hzrcl_data['languages'] = []
    hzrcl_data['educations'] = []
    hzrcl_data['credentials'] = []
    hzrcl_data['trainings'] = []
    hzrcl_data['at_schools'] = []
    # 无项目经历
    # hzrcl_data['projects'] = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for child in root.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl'):
        # print('child-tag是：', child.tag, ',child.attrib：', child.attrib, ',child.text：', child.text)
        text_li = []
        for sub_1 in child:
            temp_li = []
            for sub_2 in sub_1.iter():
                if sub_2.text and 'mailto:example@exampleabc.com' not in sub_2.text:
                    sub_2_text = sub_2.text.strip().replace("\n", "").replace("\r\n", "").replace("\r", "")
                    temp_li.append(sub_2_text)
                    text_li.append(sub_2_text)
                    # if sub_2_text:
                        # print(sub_2_text)
            # print(''.join(temp_li))
        bk_str = ''.join(text_li)
        bk_str = bk_str.replace(' ', '')
        # print(bk_str)
        if '简历名称' == bk_str[0:4]:
            hzrcl_data['info']['name'] = bk_str.split('个人信息姓名')[1].split('性别')[0]
            hzrcl_data['info']['sex'] = bk_str.split('性别')[1].split('民族')[0]
            hzrcl_data['info']['email'] = bk_str.split('邮箱')[1].split('邮政编码')[0]
            hzrcl_data['info']['channel_update_time'] = bk_str.split('最后修改时间：')[1].split('个人信息姓名')[0]
            hzrcl_data['info']['mobilephone'] = bk_str.split('手机号码')[1].split('固定电话')[0]
            hzrcl_data['info']['birth_year'] = int(bk_str.split('出生日期')[1].split('参加工作时间')[0].split('-')[0])
            hzrcl_data['info']['marital_status'] = bk_str.split('婚姻状况')[1].split('身份证号码')[0]
            hzrcl_data['info']['politics_status'] = bk_str.split('政治面貌')[1].split('手机号码')[0]
            wy_str = bk_str.split('工作年限')[1].split('婚姻状况')[0].replace('年', '')
            if '-' in wy_str and '年' in wy_str:
                hzrcl_data['info']['start_working_year'] = int(now_year) - int(bk_str.split('工作年限')[1].split('婚姻状况')[0].replace('年', '').split('-')[1].strip())
            elif '-' not in wy_str and '年' in wy_str:
                hzrcl_data['info']['start_working_year'] = int(now_year) - int(bk_str.split('工作年限')[1].split('婚姻状况')[0].replace('年', '').strip())
            else:
                hzrcl_data['info']['start_working_year'] = int(now_year)
            hzrcl_data['info']['degree'] = bk_str.split('文化程度')[1].split('政治面貌')[0]
            hzrcl_data['info']['current_address'] = bk_str.split('现住址')[1].split('爱好特长')[0]
            hzrcl_data['info']['residence_address'] = bk_str.split('户口所在地')[1].split('户口性质')[0]
            hzrcl_data['objective']['self_evaluation'] = bk_str.split('自我介绍')[1].strip()
        elif '求职意向' == bk_str[0:4]:
            exp_add_str = bk_str.split('求职意向求职区域')[1].split('期望行业')[0]
            exp_trade_str = bk_str.split('期望行业')[1].split('求职岗位')[0]
            exp_job_str = bk_str.split('求职岗位')[1].split('工作性质')[0]
            exp_salary_str = bk_str.split('期望月薪')[1].split('工作性质')[0]
            exp_nature_str = bk_str.split('工作性质')[1].split('期望月薪')[0]
            hzrcl_data['objective']['expected_address'].append(exp_add_str)
            hzrcl_data['objective']['trade'].append(exp_trade_str)
            if '请选择岗位类别,' in exp_job_str:
                exp_job_str = exp_job_str.replace('请选择岗位类别,', '')
            hzrcl_data['objective']['expected_job_title'] = exp_job_str.split(',')
            hzrcl_data['objective']['job_nature'].append(exp_nature_str)
            if '以' in exp_salary_str:
                hzrcl_data['objective']['expected_salary_lower'] = int(exp_salary_str.split('以')[0].strip())
                hzrcl_data['objective']['expected_salary_upper'] = int(exp_salary_str.split('以')[0].strip())
            elif '-' in exp_salary_str:
                exp_salary_str = exp_salary_str.split('元')[0].strip()
                hzrcl_data['objective']['expected_salary_lower'] = int(exp_salary_str.split('-')[0].strip())
                hzrcl_data['objective']['expected_salary_upper'] = int(exp_salary_str.split('-')[1].strip())
            else:
                hzrcl_data['objective']['expected_salary_lower'] = 0
                hzrcl_data['objective']['expected_salary_upper'] = 0
        elif '语言能力' == bk_str[0:4]:
            try:
                lang = {}
                lang['language'] = bk_str.split('语言能力外语语种')[1].split('外语水平')[0]
                lang['writing'] = bk_str.split('外语水平')[1].strip()
                lang['speaking'] = bk_str.split('外语水平')[1].strip()
                hzrcl_data['languages'].append(lang)
            except:
                pass
        elif '工作经历' == bk_str[0:4]:
            bk_str = bk_str[4:]
            patn_job = re.compile(r'((\d{4}-\d{2}-\d{2})?—(\d{4}-\d{2}-\d{2})?单位名称：)')
            job_li = patn_job.findall(bk_str)
            for job_index, job_1 in enumerate(job_li):
                try:
                    job_exp = {}
                    if job_1[1]:
                        job_exp['during_start'] = job_1[1]
                    else:
                        job_exp['during_start'] = '9999-01-01'
                    if job_1[2]:
                        job_exp['during_end'] = job_1[2]
                    # print(bk_str.split())
                    if job_index+1 != len(job_li):
                        job_exp_str = bk_str.split(job_li[int(job_index)][0])[1].split(job_li[int(job_index)+1][0])[0]
                    else:
                        job_exp_str = bk_str.split(job_li[int(job_index)][0])[1]
                    job_exp['company'] = job_exp_str.split('所在职位：')[0]
                    job_exp['job_title'] = job_exp_str.split('所在职位：')[1].split('所属行业：')[0]
                    job_exp['trade'] = job_exp_str.split('所属行业：')[1].split('|单位类型：')[0]
                    scale_str = job_exp_str.split('|人员规模：')[1].split('主要内容：')[0]
                    if '--' in scale_str:
                        scale_str = scale_str.replace('--', '-')
                    job_exp['company_scale'] = scale_str
                    job_exp['job_content'] = job_exp_str.split('主要内容：')[1].strip()
                    hzrcl_data['jobs'].append(job_exp)
                except:
                    pass
        elif '教育经历' == bk_str[0:4]:
            bk_str = bk_str[4:]
            patn_edu = re.compile(r'((\d{4}-\d{2}-\d{2})?—(\d{4}-\d{2}-\d{2})?学校名称：)')
            edu_li = patn_edu.findall(bk_str)
            for edu_index, edu_1 in enumerate(edu_li):
                try:
                    edu_exp = {}
                    if edu_1[1]:
                        edu_exp['during_start'] = edu_1[1]
                    else:
                        edu_exp['during_start'] = '9999-01-01'
                    if edu_1[2]:
                        edu_exp['during_end'] = edu_1[2]
                    # print(bk_str.split())
                    if edu_index+1 != len(edu_li):
                        edu_exp_str = bk_str.split(edu_li[int(edu_index)][0])[1].split(edu_li[int(edu_index)+1][0])[0]
                    else:
                        edu_exp_str = bk_str.split(edu_li[int(edu_index)][0])[1]
                    edu_exp['school'] = edu_exp_str.split('所学专业：')[0]
                    edu_exp['major'] = edu_exp_str.split('所学专业：')[1].split('学历：')[0]
                    edu_exp['degree'] = edu_exp_str.split('学历：')[1].split('|')[0]
                    hzrcl_data['educations'].append(edu_exp)
                except:
                    pass
        elif '培训经历' == bk_str[0:4]:
            bk_str = bk_str[4:]
            patn_train = re.compile(r'((\d{4}-\d{2}-\d{2})?—(\d{4}-\d{2}-\d{2})?培训机构：)')
            train_li = patn_train.findall(bk_str)
            for train_index, train_1 in enumerate(train_li):
                try:
                    train_exp = {}
                    if train_1[1]:
                        train_exp['during_start'] = train_1[1]
                    else:
                        train_exp['during_start'] = '9999-01-01'
                    if train_1[2]:
                        train_exp['during_end'] = train_1[2]
                    # print(bk_str.split())
                    if train_index+1 != len(train_li):
                        train_exp_str = bk_str.split(train_li[int(train_index)][0])[1].split(train_li[int(train_index)+1][0])[0]
                    else:
                        train_exp_str = bk_str.split(train_li[int(train_index)][0])[1]
                    train_exp['training_agency'] = train_exp_str.split('培训课程：')[0]
                    train_exp['training_course'] = train_exp_str.split('培训课程：')[1].split('培训内容：')[0]
                    train_exp['description'] = train_exp_str.split('培训内容：')[1].split('资格证书号码：')[0]
                    hzrcl_data['trainings'].append(train_exp)
                except:
                    pass
        # 技能当作证书处理
        elif '专业技能' == bk_str[0:4]:
            bk_str = bk_str[4:]
            patn_skill = re.compile(r'((\d{4}-\d{2}-\d{2})?技能特长：)')
            skill_li = patn_skill.findall(bk_str)
            # print(skill_li)
            for skill_index, skill_1 in enumerate(skill_li):
                try:
                    skill_exp = {}
                    if skill_1[1]:
                        skill_exp['get_date'] = skill_1[1]
                    # print(bk_str.split())
                    if skill_index+1 != len(skill_li):
                        skill_exp_str = bk_str.split(skill_li[int(skill_index)][0])[1].split(skill_li[int(skill_index)+1][0])[0]
                    else:
                        skill_exp_str = bk_str.split(skill_li[int(skill_index)][0])[1]
                    skill_exp['title'] = skill_exp_str.split('国家资格等级：')[1].split('|')[0]
                    hzrcl_data['credentials'].append(skill_exp)
                except:
                    pass
        elif '证书情况' == bk_str[0:4]:
            bk_str = bk_str[4:]
            patn_zs = re.compile(r'((\d{4}-\d{2}-\d{2})?证书名称：)')
            zs_li = patn_zs.findall(bk_str)
            # print(zs_li)
            for zs_index, zs_1 in enumerate(zs_li):
                try:
                    zs_exp = {}
                    if zs_1[1]:
                        zs_exp['get_date'] = zs_1[1]
                    # print(bk_str.split())
                    if zs_index+1 != len(zs_li):
                        zs_exp_str = bk_str.split(zs_li[int(zs_index)][0])[1].split(zs_li[int(zs_index)+1][0])[0]
                    else:
                        zs_exp_str = bk_str.split(zs_li[int(zs_index)][0])[1]
                    zs_exp['title'] = zs_exp_str.split('证书编号：')[0]
                    hzrcl_data['credentials'].append(zs_exp)
                except:
                    pass
        elif '获奖情况' == bk_str[0:4]:
            bk_str = bk_str[4:]
            patn_hj = re.compile(r'((\d{4}-\d{2}-\d{2})?证书名称：)')
            hj_li = patn_hj.findall(bk_str)
            # print(hj_li)
            for hj_index, hj_1 in enumerate(hj_li):
                try:
                    hj_exp = {}
                    if hj_1[1]:
                        hj_exp['get_date'] = hj_1[1]
                    # print(bk_str.split())
                    if hj_index+1 != len(hj_li):
                        hj_exp_str = bk_str.split(hj_li[int(hj_index)][0])[1].split(hj_li[int(hj_index)+1][0])[0]
                    else:
                        hj_exp_str = bk_str.split(hj_li[int(hj_index)][0])[1]
                    hj_exp['title'] = hj_exp_str.split('奖励成果名称：')[0]
                    hzrcl_data['credentials'].append(hj_exp)
                except:
                    pass
    hzrcl_data['org'] = {}
    hzrcl_data['org']['org_id'] = org_id
    try:
        if hzrcl_data['info']['mobilephone']:
            hzrcl_data['org']['download_status'] = 1
    except:
        hzrcl_data['org']['download_status'] = 0
    # 插件
    hzrcl_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 收件箱--------------渠道职位ID
    hzrcl_data['org']['resume_type'] = 1
    if job_id:
        hzrcl_data['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    if dt:
        hzrcl_data['org']['delivery_time'] = dt
    try:
        if hzrcl_data['info']['photo_url']:
            pass
            # print('have photo_url')
    except:
        hzrcl_data['info'][
            'photo_url'] = 'http://rsmfiletest.oss-cn-hangzhou.aliyuncs.com/channel_resume%2Fdefault%2Fdefault_photo.png'
        # print('add default photo_url')
    return hzrcl_data
def lg_email(xz_url, dt_2):
    xz_url_stat = True
    while xz_url_stat:
        time.sleep(60)
        dt_sec = time_sec(str(dt_2))
        try:
            conf = configparser.ConfigParser(strict=False, allow_no_value=True)
            ini_p = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '/pyth/conf.ini'
            if r'\\' in ini_p:
                ini_p = ini_p.replace(r'\\', '/')
            conf.read(ini_p, encoding='utf-8')  # 文件路径
            login_lg_r = conf.get("config", "login_lg")
            if login_lg_r == 'True':
                try:
                    cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
                    cookies_str_lg = func_lg.get_cook_str(".lagou.com", cookies_basis_lg)
                    login_judge_res = func_lg.login_judge_lg(cookies_str_lg)  # 判断是否登陆
                    login_lg = True
                except:
                    login_lg = False
                    logging.error("废弃函数")
                if login_lg:
                    try:
                        module_lg_0.email_dl(xz_url)
                        unzip_file('Mod_Pyth/hzrc.zip', 'Mod_Pyth/hzrc')
                        rootdir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc'
                        lg_jl_li = []
                        for parent, dirnames, filenames in os.walk(rootdir):
                            for filename in filenames:
                                try:
                                    (name_1, extension_1) = os.path.splitext(filename)
                                    filename_doc = rootdir + os.sep + filename
                                    xml_file = doc_xml(filename_doc)
                                    lg_jl = jx_lg_email(xml_file, job_id='', org_id=org_id, dt=dt_sec)
                                    lg_jl_li.append(lg_jl)
                                    print(lg_jl)
                                except:
                                    logging.error("scpy email hzrc one fail")
                                    traceback.print_exc()
                                    pass
                        xz_url_stat = False
                        return lg_jl_li
                    # time.sleep(1000)
                    except:
                        logging.exception("Exception Logged")
                        logging.error("scpy email lg jx fail")
                        xz_url_stat = False
                        traceback.print_exc()
        except:
            xz_url_stat = False
            logging.error("scpy email lg out all fail")
def jljx_lg(text, ds=0, job_id='', org_id='111',lx=0,dt='', jlid=''):
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    lg_data = {}
    lg_data['info'] = {}
    lg_data['info']['channel'] = 13
    lg_data['objective'] = {}
    lg_data['objective']['expected_job_title'] = []
    lg_data['objective']['expected_address'] = []
    lg_data['objective']['trade'] = []
    lg_data['objective']['job_nature'] = []
    lg_data['objective']['individual_label'] = []
    lg_data['jobs'] = []
    lg_data['languages'] = []
    lg_data['educations'] = []
    lg_data['credentials'] = []
    lg_data['trainings'] = []
    lg_data['at_schools'] = []
    lg_data['projects'] = []

    sel = Selector(text=text)

    if not jlid:
        xpa_name = '//div[@class="information-body"]/div/div[not(@class)]/span/text()'
        xpa_sex = '//div[@class="information-body"]/div/div[not(@class)]/i/@title'
        xpa_jbxx = '//span[@class="base-info-workyear-education"]/span'
        xpa_resumeid = '//a[contains(@class,"is_can_chat")]/@href'
        resumeid_str = sel.xpath(xpa_resumeid).extract()[0].strip()
        lg_data['info']['channel_resume_id'] = resumeid_str.split('resumeId=')[1]
        lg_data['info']['name'] = sel.xpath(xpa_name).extract()[0].strip()
        if '*' in lg_data['info']['name']:
            lg_data['info']['name'] = lg_data['info']['name'].replace('*', 'X')
        try:
            lg_data['info']['sex'] = sel.xpath(xpa_sex).extract()[0].strip()
        except:
            pass
        for jbxx_ele in sel.xpath(xpa_jbxx):
            try:
                jbxx_str = jbxx_ele.xpath('string(.)').extract()[0].strip()
                deg_li = ['大专', '硕士', '本科', '博士', '其他']
                if jbxx_str:
                    if jbxx_ele.xpath('@title'):
                        lg_data['info']['birth_year'] = int(jbxx_ele.xpath('@title').extract()[0].split('年')[0])
                    elif '应届' in jbxx_str:
                        lg_data['info']['start_working_year'] = int(now_year)
                    elif '工作经验' in jbxx_str:
                        lg_data['info']['start_working_year'] = int(now_year) - int(jbxx_str.split('年')[0])
                    elif jbxx_str in deg_li:
                        lg_data['info']['degree'] = jbxx_str
                    else:
                        lg_data['info']['current_address'] = jbxx_str
            except:
                pass

        xpa_phone = 'string(//div[@class="information-link"])'
        phone_str = sel.xpath(xpa_phone).extract()[0]
        if '手机号：' in phone_str:
            lg_data['info']['mobilephone'] = phone_str.split('手机号：')[1].split('(')[0].replace('-', '').strip()
        if '邮箱：' in phone_str:
            lg_data['info']['email'] = phone_str.split('邮箱：')[1].strip()
        xpa_bk = '//div[@id="resumePreviewContainer"]/div[@class="online-preview"]/div[@class="mr_content"]/div[@class="mr_w604"]/div'
    else:
        xpa_name = '//div[@class="mr_p_name mr_w604 clearfixs"]/span/text()'
        xpa_sex = '//div[@class="mr_p_info mr_infoed mr_w604 clearfixs"]/div/span[@class="base_info"]/em[@class="s"]/text()'
        xpa_age = '//div[@class="mr_p_info mr_infoed mr_w604 clearfixs"]/div/span[@class="base_info"]/em[@class="a"]/span/@title'
        xpa_degree = '//div[@class="mr_p_info mr_infoed mr_w604 clearfixs"]/div/span[@class="base_info"]/em[@class="x"]/text()'
        xpa_addr = '//div[@class="mr_p_info mr_infoed mr_w604 clearfixs"]/div/span[@class="base_info"]/em[@class="mr0 d"]/text()'
        xpa_wy = '//div[@class="mr_p_info mr_infoed mr_w604 clearfixs"]/div/span[@class="base_info"]/em[@class="j"]/span/text()'
        lg_data['info']['channel_resume_id'] = jlid
        lg_data['info']['name'] = sel.xpath(xpa_name).extract()[0].strip()
        try:
            lg_data['info']['sex'] = sel.xpath(xpa_sex).extract()[0].strip()
        except:
            pass
        try:
            lg_data['info']['degree'] = sel.xpath(xpa_degree).extract()[0].strip()
        except:
            pass
        try:
            lg_data['info']['current_address'] = sel.xpath(xpa_addr).extract()[0].strip()
        except:
            pass
        try:
            lg_data['info']['birth_year'] = int(sel.xpath(xpa_age).extract()[0].strip().split('年')[0])
        except:
            pass
        wy_str = sel.xpath(xpa_wy).extract()[0].strip()
        if '应届' in wy_str:
            lg_data['info']['start_working_year'] = int(now_year)
        elif '工作经验' in wy_str:
            lg_data['info']['start_working_year'] = int(now_year) - int(wy_str.split('年')[0])
        xpa_bk = '//div[@class="mr_w604"]/div'
    # print(sel.xpath(xpa_bk))
    for bk_ele in sel.xpath(xpa_bk):
        if 'expectJob' in bk_ele.xpath('@id').extract()[0]:
            for obj_ele in bk_ele.xpath('descendant::ul[@class="clearfixs"]/li'):
                try:
                    exp_str = obj_ele.xpath('string(.)').extract()[0].strip()
                    if exp_str:
                        if 'mr_name_li' in obj_ele.xpath('@class').extract()[0]:
                            lg_data['objective']['expected_job_title'].append(exp_str)
                        elif 'mr_jobtype_li' in obj_ele.xpath('@class').extract()[0]:
                            lg_data['objective']['job_nature'].append(exp_str)
                        elif 'mr_city_li' in obj_ele.xpath('@class').extract()[0]:
                            lg_data['objective']['expected_address'].append(exp_str)
                        elif 'mr_expect_job_li' in obj_ele.xpath('@class').extract()[0]:
                            lg_data['objective']['work_status'] = exp_str.split(' ')[0]
                        elif 'mr_jobrange_li' in obj_ele.xpath('@class').extract()[0]:
                            if '-' in exp_str:
                                lg_data['objective']['expected_salary_lower'] = int(exp_str.split('-')[0].replace('k', '').strip())*1000
                                lg_data['objective']['expected_salary_upper'] = int(exp_str.split('-')[1].replace('k', '').strip())*1000
                            else:
                                lg_data['objective']['expected_salary_lower'] = int(exp_str.split('k')[0].strip()) * 1000
                                lg_data['objective']['expected_salary_upper'] = int(exp_str.split('k')[0].strip()) * 1000
                except:
                    pass
        elif 'selfDescription' in bk_ele.xpath('@id').extract()[0]:
            self_str = bk_ele.xpath('string(.)').extract()[0].replace("\n", "").replace("\r\n", "").replace("\r", "").replace(' ', '')
            lg_data['objective']['self_evaluation'] = self_str
        elif 'workExperience' in bk_ele.xpath('@id').extract()[0]:
            for job_ele in bk_ele.xpath('descendant::div[@class="mr_jobe_list"]'):
                try:
                    xpa_comp = 'div[@class="clearfixs"]/div[@class="mr_content_l"]/div/h4/text()'
                    xpa_exp_job = 'div[@class="clearfixs"]/div[@class="mr_content_l"]/div/span/text()'
                    xpa_exp_time = 'string(div[@class="clearfixs"]/div[@class="mr_content_r"])'
                    xpa_exp_desc = 'string(div[@class="mr_content_m"])'
                    lg_job = {}
                    lg_job['company'] = job_ele.xpath(xpa_comp).extract()[0].strip()
                    lg_job['job_title'] = job_ele.xpath(xpa_exp_job).extract()[0].strip()
                    lg_job['job_content'] = job_ele.xpath(xpa_exp_desc).extract()[0].replace("\n", "").replace("\r\n", "").replace("\r", "").strip()
                    job_time_str = job_ele.xpath(xpa_exp_time).extract()[0].strip()
                    if '至今' in job_time_str:
                        lg_job['during_start'] = job_time_str.split('—')[0].replace('.', '-').strip() + '-01'
                        lg_job['during_end'] = '9999-01-01'
                    else:
                        lg_job['during_start'] = job_time_str.split('—')[0].replace('.', '-').strip() + '-01'
                        lg_job['during_end'] = job_time_str.split('—')[1].replace('.', '-').strip() + '-01'
                    lg_data['jobs'].append(lg_job)
                except:
                    pass
        elif 'educationalBackground' in bk_ele.xpath('@id').extract()[0]:
            for edu_ele in bk_ele.xpath('descendant::div[@class="clearfixs mb46 mr_jobe_list"]'):
                try:
                    xpa_school = 'div[@class="mr_content_l clearfix"]/div[@class="l2"]/h4/text()'
                    xpa_major_deg = 'string(div[@class="mr_content_l clearfix"]/div[@class="l2"]/span)'
                    xpa_edu_time = 'string(div[@class="mr_content_r"])'
                    lg_edu = {}
                    lg_edu['school'] = edu_ele.xpath(xpa_school).extract()[0].strip()
                    major_deg_str = edu_ele.xpath(xpa_major_deg).extract()[0].strip()
                    if '·' in major_deg_str:
                        lg_edu['degree'] = major_deg_str.split('·')[0].strip()
                        lg_edu['major'] = major_deg_str.split('·')[1].strip()

                    edu_time_str = edu_ele.xpath(xpa_edu_time).extract()[0].strip()
                    if '至今' in edu_time_str:
                        lg_edu['during_start'] = edu_time_str.split('-')[0].replace('年', '-').strip() + '09-01'
                        lg_edu['during_end'] = '9999-01-01'
                    else:
                        lg_edu['during_start'] = edu_time_str.split('-')[0].replace('年', '-').strip() + '09-01'
                        lg_edu['during_end'] = edu_time_str.split('-')[1].replace('年', '-').strip() + '06-30'
                    lg_data['educations'].append(lg_edu)
                except:
                    pass
        elif 'projectExperience' in bk_ele.xpath('@id').extract()[0]:
            for pro_ele in bk_ele.xpath('descendant::div[@class="mr_jobe_list"]'):
                try:
                    xpa_pro_name = 'div[@class="clearfixs"]/div[@class="mr_content_l"]/div[@class="l2"]/a/text()'
                    xpa_pro_job = 'string(div[@class="clearfixs"]/div[@class="mr_content_l"]/div[@class="l2"]/p)'
                    xpa_pro_time = 'string(div[@class="clearfixs"]/div[@class="mr_content_r"])'
                    xpa_pro_desc = 'string(div[@class="mr_content_m ueditor_unparse"])'
                    lg_pro = {}
                    lg_pro['title'] = pro_ele.xpath(xpa_pro_name).extract()[0].strip()
                    lg_pro['duty'] = pro_ele.xpath(xpa_pro_job).extract()[0].strip()
                    lg_pro['description'] = pro_ele.xpath(xpa_pro_desc).extract()[0].strip()
                    pro_time_str = pro_ele.xpath(xpa_pro_time).extract()[0].strip()
                    if '至今' in pro_time_str:
                        lg_pro['during_start'] = pro_time_str.split('-')[0].replace('.', '-').strip() + '-01'
                        lg_pro['during_end'] = '9999-01-01'
                    else:
                        lg_pro['during_start'] = pro_time_str.split('-')[0].replace('.', '-').strip() + '-01'
                        lg_pro['during_end'] = pro_time_str.split('-')[1].replace('.', '-').strip() + '-01'
                    lg_data['projects'].append(lg_pro)
                except:
                    pass
        elif 'skillsAssess' in bk_ele.xpath('@id').extract()[0]:
            for ski_ele in bk_ele.xpath('descendant::div[@class="mr_skill_con"]'):
                try:
                    lg_ski = {}
                    lg_ski['skill'] = ski_ele.xpath('span[@class="mr_skill_name"]/text()').extract()[0].strip()
                    lg_ski['level'] = ski_ele.xpath('span[@class="mr_skill_level"]/text()').extract()[0].strip()
                    lg_data['languages'].append(lg_ski)
                except:
                    pass
    lg_data['org'] = {}
    lg_data['org']['resume_type'] = 3
    lg_data['org']['org_id'] = org_id
    try:
        if lg_data['info']['mobilephone']:
            lg_data['org']['download_status'] = 1
    except:
        lg_data['org']['download_status'] = 0
    # 插件
    lg_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    if dt:
        lg_data['org']['delivery_time'] = dt
    return lg_data

filelog = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'logging' + os.sep + 'logging.log'
# print(new_tj)
logging.basicConfig(
    level=logging.ERROR,  # 定义输出到文件的log级别，
    format='%(asctime)s : %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    filename=filelog,  # log文件名
    filemode='a')  # 写入模式“w”或“a”
logging.error('into Scpy...')
new_tj = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'pyth' + os.sep + 'new_tj'
# print(new_tj)
# time.sleep(1000)
if not os.path.exists(new_tj):
    # print('文件夹', new_tj, '不存在，重新建立')
    # os.mkdir(file_path)
    os.makedirs(new_tj)
else:
    shutil.rmtree(new_tj)
    os.makedirs(new_tj)

logging.error('Scpy first init zhaopin sucess ...')


cookies_str_zl = "JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976"
cookie_zl_0 = zl_xghs.get_cook_str('.zhaopin.com', cookies_str_zl)
logging.error('run zl sucess, to run 51-----1')


cookies_basis_51 = 'guid=15126185243667940069; EhireGuid=57343d4ab9144eeaaac53570c55c6bd5; RememberLoginInfo=member_name=790EDF22D15A367144E78236FFD81B69&user_name=3F6D7EB2B10CC033; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0VmkU00uiAs0aQA-p00000aaJBdb00000X8ZxsW.THLZ_Q5n1VeHksK85ydEUhkGUhNxndqbusK15y7-uj-BP1fdnj0snvnzrjn0IHY4fW0knHI7wWRsrj-KwD7KwRDYnbfdn1n3rDwaP1Naw0K95gTqFhdWpyfqn10LP1T4PWbLPiusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqPHnzPWb%2526tpl%253Dtpl_10085_16624_12226%2526l%253D1502325280%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m4b66f41d%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D233%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dmonline_3_dg%2526inputT%253D4274%26%7C%26adsnum%3D789233; LangType=Lang=&Flag=1; 51job=cuid%3D52237061%26%7C%26cusername%3D13598213097%26%7C%26cpassword%3D%26%7C%26cname%3D%25D1%25EE%25D2%25F8%25B2%25A8%26%7C%26cemail%3D455471846%2540qq.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0g4r6HYlhTBg%26%7C%26cconfirmkey%3D4555sQmuzH7DE%26%7C%26cresumeids%3D.0Sy8EEE7wagc%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D45usYTv%252FFNEs.%26%7C%26to%3DXmMBaANjCz5cOlo2UTJRYwxzBjYANVU1AT5dNwE5BTQNNlA7D2QLOlF8XTALa1ViBT9UZQM0AWRdYlQ%252BATI%253D%26%7C%26; ps=us%3DXGUCawBgVn4CYVg2B2dXegIzBjVWYwZ9VWIBag0zBXkLMgBuUzALOgJnXzRRMAA7Vm0BOQA2UDJdY1Z4D0QANFxhAjEAFw%253D%253D%26%7C%26needv%3D0; _ujz=NTIyMzcwNjEw; AccessKey=d45a0618ef944d1; partner=baidupz; slife=lastlogindate%3D20180209%26%7C%26; ASP.NET_SessionId=tnj5cjfsmtf5h2nf3avtcvrc; HRUSERINFO=CtmID=2424128&DBID=2&MType=02&HRUID=2788355&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=hzjl340&IsStandard=0&LoginTime=02%2f09%2f2018+09%3a01%3a32&ExpireTime=02%2f09%2f2018+09%3a11%3a32&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=bf9abebe61bef674; KWD=SEARCH='
cookies_str_51 = al_qf.get_cook_str('ehire.51job.com', cookies_basis_51)
module_51_1 = Module_51(cookies_str_51)
logging.error('Scpy first init 51 sucess ...')


cookies_basis_hzrc = 'UM_distinctid=163de889caed3-028b380ab63eff-44410a2e-100200-163de889caf41c; _ubm_id.d2cc513d10e26176994c26da25947ea2=1096e84c977a2486; longinUser=wb; Hm_lvt_46b0265c3ac55b35a0fc9e4683094a94=1528508654,1528685759; JSESSIONID=fFwgwAdo1QFX1mrVudLvHNpTntWrDysZgTlsfgj8A1c9cFn9Q-Cw!-196033929; CNZZDATA2145298=cnzz_eid%3D868844613-1528441555-null%26ntime%3D1529560309; _ubm_ses.d2cc513d10e26176994c26da25947ea2=*; Hm_lpvt_46b0265c3ac55b35a0fc9e4683094a94=1529563918'
cookies_str_hzrc = al_qf.get_cook_str('.hzrc.com', cookies_basis_hzrc)
module_hzrc_0 = Module_hzrc(cookies_str_hzrc)
logging.error('Scpy first init hzrc sucess ...')

# cookies_basis_gj = 'ganji_xuuid=c7dc72ef-60db-4264-aced-0a6a701c2cd3.1528708751959; ganji_uuid=7150266604199787963746; xxzl_deviceid=hNmWYgYm3yVBw3yuNYA%2BLPpzVYJGhHRfC9VGkavtS3QxEfmxbyvsUW%2F%2FIgzp8FIi; lg=1; NTKF_T2D_CLIENTID=guestA8ABE4E8-9FE5-DEC9-A48B-EE251D637B74; cityDomain=bj; citydomain=bj; 58tj_uuid=def2acb6-3e85-430a-8c40-c72caf90a077; als=0; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A31561918616%7D; use_https=1; new_uv=3; __utmc=32156897; __utmz=32156897.1529023568.3.3.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; nTalk_CACHE_DATA={uid:kf_10111_ISME9754_557709909}; username_login_n=15669087700; GanjiLoginType=0; __utma=32156897.1024205804.1528708769.1529023568.1529029837.4; GANJISESSID=shdb8t2vgn99tnkn0ofdcgrihf; sscode=9HsRkf041lVH%2BQf39HWsQh54; GanjiUserName=szfl666; GanjiUserInfo=%7B%22user_id%22%3A557709909%2C%22email%22%3A%22%22%2C%22username%22%3A%22szfl666%22%2C%22user_name%22%3A%22szfl666%22%2C%22nickname%22%3A%22%5Cu5e73%5Cu5b89%5Cu6768%5Cu9752%5Cu9752%22%7D; bizs=%5B3%5D; supercookie=AGH3AmN5BGN5WQtlMTMuAmRkMwNlLmOvLGp0ZTMzLzMyMJWvAJZ0BGH0LmpjMwSuMGR%3D; xxzl_smartid=46229e619fb608c62d39dc189295baf9; last_name=szfl666; ganji_login_act=1529044045164'
# cookies_str_gj = al_qf.get_cook_str('.ganji.com', cookies_basis_gj)
# module_gj_1 = Module_gj(cookies_str_gj)
# logging.error('Scpy first init ganji sucess ...')

# cookies_basis_lp = 'abtest=0; _fecdn_=1; __uuid=1530527233544.45; __tlog=1530527233545.26%7C00000000%7C00000000%7Cs_00_pz0%7Cs_00_pz0; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1530527234; _mscid=s_00_pz0; _uuid=5A88398AFFA848187736D9B9BF2D2CD8; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1530527255; user_name=%E9%83%AD%E5%AD%90%E6%A1%A2; lt_auth=6L5bbCcFxl76tnGKiGpet69N3dOtU27O9H9Y0RFV1oe%2BD%2F3i4PrlQwOErLIDxBIhlkt3JsULNLP%2B%0D%0AMOr5y3VD6UMTwGmnlYCxuuW70XweTedcdvmi0a72kMzZQslxnXEHyHBg8H9Okx31sUAhN9TvnF7I%0D%0Ap6HH7ral8vvE%0D%0A; UniqueKey=d4d47f8153c841621a667e00ad0d9493; user_kind=1; _l_o_L_=e3c9b446218c5b2bd4d47f8153c841621a667e00ad0d9493; login_temp=islogin; _e_ld_auth_=ac23e04875d8628e; b-beta2-config=%7B%22d%22%3A365%2C%22e%22%3A9612079%2C%22ejm%22%3A%221%22%2C%22n%22%3A%22%25E9%2583%25AD%25E5%25AD%2590%25E6%25A1%25A2%22%2C%22audit%22%3A%221%22%2C%22ecomp_id%22%3A9612079%2C%22photo%22%3A%22%2F%2Fimage0.lietou-static.com%2Fimg%2F5afa5b868e50d906233368cf04a.png%22%2C%22version%22%3A%222%22%2C%22hasPhoneNum%22%3A%221%22%2C%22v%22%3A%222%22%2C%22ecreate_time%22%3A%2220180702%22%2C%22p%22%3A%222%22%2C%22entry%22%3A%221%22%2C%22jz%22%3A%220%22%7D; imClientId=3a3ef6be625ffffc4462f629076d8d2a; imId=3a3ef6be625ffffc5da7d3574f2ad402; fe_lpt_jipinByOneGiveTwo=true; fe_lpt_resumeLib=true; fe_lpt_sevenAnniversaryBegin=true; fe_lpt_realname=true; JSESSIONID=24835A675443F7EA7CF7131A3639013B; __session_seq=34; __uv_seq=34'
# cookies_str_lp = al_qf.get_cook_str('.liepin.com', cookies_basis_lp)
# module_lp_1 = Module_lp(cookies_str_lp)
# logging.error('Scpy first init lp sucess ...')

login_zl = False
login_51 = False
login_lp = False
login_lg = False



for i in range(1, 20):
    # 1智联2前程3同城
    if i == 1:
        try:
            zl_xghs.login_judge_zl(cookie_zl_0)
            # print('登录成功')
            login_zl = True
        except:
            login_zl = False
    elif i == 2:
        try:
            module_51_1.login_judge_51()
            login_51 = True
        except:
            pass
    elif i == 5:
        try:
            module_hzrc_0.login_judge_hzrc()
            login_hzrc = True
        except:
            pass
    elif i == 13:
        try:
            cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
            cookies_str_lg = func_lg.get_cook_str("easy.lagou.com", cookies_basis_lg)
            login_judge_res = func_lg.login_judge_lg(cookies_str_lg)  # 判断是否登陆
            login_lg = True
        except:
            login_lg = False
            logging.error("lg login fail-----scpy begin init")
    # elif i == 4:
    #     gj_log = {}
    #     try:
    #         module_gj_1.login_judge_gj()
    #         login_gj = True
    #     except:
    #         pass
    # elif i == 10:
    #     lp_log = {}
    #     try:
    #         module_lp_1.login_judge_lp()
    #         login_lp = True
    #     except:
    #         pass

logging.error('Scpy success ...')
# print(data)
try:
    conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    ini_p = os.getcwd() + os.sep + 'Config.ini'
    conf.read(ini_p, encoding='utf-8')  # 文件路径
    port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
    port = int(port)
    Account = conf.get("PUB_CONF", "PY_ACC")
    org_id = conf.get("PUB_CONF", "PY_COM")
except:
    Account = ''
    org_id = ''
tjgx_51 = ''
tjgx_zl = ''
tjgx_gj = ''
tjgx_lp = ''
tjgx_lg = ''

org_id = '131231321'

def get_tj(n,filename=''):
    if not filename:
        filename = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'pyth/ini_tj.txt'
    else:
        filename = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'pyth/new_tj/' + filename
        # print(filename)
    with open(filename, 'r+') as f_ini:
        tj_str = f_ini.read()
        # print(tj_str)
        # print(type(tj_str))
        # try:
        if tj_str[:3] == codecs.BOM_UTF8:
            tj_str = tj_str[3:]
        if tj_str[0] == "b":
            tj_str = str(tj_str)[1:]
            # print(str(tj_str))
            # print(type(tj_str))
        tj_str = tj_str.replace("'", '"')
        # if 'null' in tj_str:
        #     tj_str = tj_str.replace("null", 'None')
        # print(tj_str)
        try:
            newdata = json.loads(tj_str)
            # print(newdata)
            newdata = json.loads(newdata)
            # print(n, newdata)
        except:
            newdata = json.loads(tj_str)
            # print(n, newdata)
        # print(newdata)
        # print(type(newdata))
        tj_li = []
        if type(newdata) == list:
            for da in newdata:
                if str(da['channelType']) == str(n):
                    tj_li.append(da)
            if len(tj_li):
                return tj_li
            else:
                return None
            # print(newdata)
            # print('类型：', type(newdata))
        else:
            # print(newdata)
            return newdata

def run_M():
    # 定义线程池
    # time.sleep(360)
    threads = []
    # 条件，jobid, orgid
    # args是关键字参数，需要加上名字，写成args=(self,)
    # th1 = threading.Thread(target=scra_zl, args=())
    # threads.append(th1)
    # th2 = threading.Thread(target=scra_51, args=(module_51_1,))
    # threads.append(th2)
    # th3 = threading.Thread(target=scra_58, args=(dri_58_1,))
    # threads.append(th3)
    # th4 = threading.Thread(target=scra_gj, args=(module_gj_1,))
    # threads.append(th4)
    th5 = threading.Thread(target=run_clear, args=())
    threads.append(th5)
    th6 = threading.Thread(target=login_sx, args=())
    threads.append(th6)
    th7 = threading.Thread(target=kill_self, args=())
    threads.append(th7)
    th8 = threading.Thread(target=get_email, args=())
    threads.append(th8)
    # th9 = threading.Thread(target=scra_lp, args=(module_lp_1,))
    # threads.append(th9)
    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()
# tj_zl_li列表：[tj_dict,jobid,orgid]
def scra_zl():
    global tjgx_zl
    global login_zl
    sum_num = 0
    go_on = True
    sjx = 1
    rcj_gg = 1
    rcj_cb = 1
    dgt = 1
    newdata_zl = get_tj(1)
    if newdata_zl:
        all_tj = newdata_zl
    else:
        all_tj = []
    while not login_zl:
        time.sleep(60*15)
        try:
            conf = configparser.ConfigParser(strict=False, allow_no_value=True)
            ini_p = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '/pyth/conf.ini'
            if r'\\' in ini_p:
                ini_p = ini_p.replace(r'\\', '/')
            conf.read(ini_p, encoding='utf-8')  # 文件路径
            login_zl_r = conf.get("config", "login_zl")
            if login_zl_r == 'True':
                try:
                    zl_xghs.login_judge_zl(cookie_zl_0)
                    # print('验证登录成功')
                    login_zl = True
                except:
                    login_zl = False


        except:
            pass
    while login_zl:
        time.sleep(60)
        if go_on:
            ini_path = os.getcwd() + os.sep + 'Config.ini'
            try:
                conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                conf.read(ini_path, encoding='utf-8')  # 文件路径
                port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
                port = int(port)
                Account = conf.get("PUB_CONF", "PY_ACC")
                org_id = conf.get("PUB_CONF", "PY_COM")
            except:
                Account = ''
                org_id = ''
            try:
                js_to_py = {}
                js_to_py['JsToPython'] = {}
                js_to_py['JsToPython']['type'] = 'ChannelTj'
                js_to_py['JsToPython']['channel'] = 1
                data = json.dumps(js_to_py)
                data = data.encode('utf-8')
                url_to_js = 'http://127.0.0.1:' + str(port) + '/JsPython?account=' + str(Account)
                tj_text = requests.post(url=url_to_js, data=data)
                tj_str = tj_text.text
                tj_str = tj_str.replace("'", '"')
                tj_str_li_0 = tj_str.split(', "{"JsToPython": ')
                tj_str_li = []
                for index2, tj in enumerate(tj_str_li_0):
                    if 0 < index2 < len(tj_str_li_0) - 1:
                        tj = '{"JsToPython": ' + tj[:-1]
                        # tj = "'" + tj + "'"
                        # tj.insert(0, tj)
                        tj_str_li.append(tj)
                    elif index2 == 0:
                        tj = tj[2:-1]
                        if tj[-1] == '"':
                            tj = tj[:-1]
                        # tj = "'" + tj + "'"
                        # tj.insert(0, tj)
                        tj_str_li.append(tj)
                    elif index2 == len(tj_str_li_0) - 1:
                        tj = '{"JsToPython": ' + tj[:-2]
                        # tj = "'" + tj + "'"
                        # tj.insert(0, tj)
                        tj_str_li.append(tj)
                for newtj in tj_str_li:
                    try:
                        tempdata = json.loads(newtj)
                        # print(newdata)
                        tempdata = json.loads(tempdata)
                        # print(n, newdata)
                    except:
                        tempdata = json.loads(newtj)
                        # print(n, newdata)
                    all_tj.insert(0, tempdata)
            except:
                pass
            if len(all_tj) >= 1:
                still_tj = 'zl still_tj----------' + str(len(all_tj))
                logging.error(still_tj)
                newdata = all_tj.pop(0)
            else:
                newdata = ''
            # print(all_tj)
            # print('智联')
            logging.error('Scrapy tj zl:' + str(newdata))
            try:
                try:
                    if newdata['channelType'] == 1:
                        if tjgx_zl != str(newdata['jsonData']):
                            tjgx_zl = str(newdata['jsonData'])
                            tj_data = newdata['jsonData']
                            # print(11111111111, tj_data)
                            # print(type(tj_data))
                            tj_data = json.loads(tj_data)
                            # print(tj_data)
                            try:
                                jobid = tj_data['jobId']
                                zl_meta = zl_xghs.login_judge_zl(cookie_zl_0)[0]
                                ss_num=zl_xghs.jl_sou_suo(cookie_zl_0,zl_meta,tj_data,jobid, org_id)
                                sum_num = ss_num + sum_num
                                logging.error("the history_tj_zl got jl number:" + str(ss_num))
                                # print(sum_num)
                            except:
                                # traceback.print_exc()
                                logging.exception("Exception Logged")
                                pass
                except:
                    traceback.print_exc()
                    logging.error("no history tj zl ...")
                    pass
                try:
                    if newdata['JsToPython']['channel'] == 1:
                        if tjgx_zl != str(newdata['JsToPython']['json']):
                            tjgx_zl = str(newdata['JsToPython']['json'])
                            tj_data = newdata['JsToPython']['json']
                            # print(2222, tj_data)
                            try:
                                jobid = tj_data['jobId']
                                zl_meta = zl_xghs.login_judge_zl(cookie_zl_0)[0]
                                ss_num = zl_xghs.jl_sou_suo(cookie_zl_0, zl_meta, tj_data,jobid, org_id)
                                sum_num = ss_num + sum_num
                                # print(sum_num)
                                logging.error("the current_tj_zl got jl number:" + str(ss_num))

                            except:
                                logging.exception("Exception Logged")
                                traceback.print_exc()
                                pass
                except:
                    traceback.print_exc()
                    logging.error("no current tj zl ...")
                    pass
            except:
                pass
            if sum_num >= 1000:
                go_on = False
def scra_51(module_51_1):
    global tjgx_51
    global login_51
    sum_num = 0
    go_on = True
    sjx = 1
    yxz = 1
    newdata_51 = get_tj(2)
    if newdata_51:
        all_tj = newdata_51
    else:
        all_tj = []
    while not login_51:
        time.sleep(60*15)
        try:
            conf = configparser.ConfigParser(strict=False, allow_no_value=True)
            ini_p = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '/pyth/conf.ini'
            if r'\\' in ini_p:
                ini_p = ini_p.replace(r'\\', '/')
            conf.read(ini_p, encoding='utf-8')  # 文件路径
            login_51_r = conf.get("config", "login_51")
            if login_51_r == 'True':
                cookies_str_51 = al_qf.get_cook_str('ehire.51job.com', cookies_basis_51)
                module_51_1 = Module_51(cookies_str_51)
                try:
                    module_51_1.login_judge_51()
                    login_51 = True
                except:
                    login_51 = False
        except:
            pass
    while login_51:
        time.sleep(60)
        if go_on:
            ini_path = os.getcwd() + os.sep + 'Config.ini'
            try:
                conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                conf.read(ini_path, encoding='utf-8')  # 文件路径
                port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
                port = int(port)
                Account = conf.get("PUB_CONF", "PY_ACC")
                org_id = conf.get("PUB_CONF", "PY_COM")
            except:
                Account = ''
                org_id = ''
            # try:
            js_to_py = {}
            js_to_py['JsToPython'] = {}
            js_to_py['JsToPython']['type'] = 'ChannelTj'
            js_to_py['JsToPython']['channel'] = 2
            data = json.dumps(js_to_py)
            data = data.encode('utf-8')
            url_to_js = 'http://127.0.0.1:' + str(port) + '/JsPython?account=' + str(Account)
            tj_text = requests.post(url=url_to_js, data=data)
            tj_str = tj_text.text
            # print(tj_str)
            if tj_str != str([]):
                tj_str = tj_str.replace("'", '"')
                tj_str_li_0 = tj_str.split(', "{"JsToPython": ')
                tj_str_li = []
                for index2, tj in enumerate(tj_str_li_0):
                    if 0 < index2 < len(tj_str_li_0) - 1:
                        tj = '{"JsToPython": ' + tj[:-1]
                        # tj = "'" + tj + "'"
                        # tj.insert(0, tj)
                        tj_str_li.append(tj)
                    elif index2 == 0:
                        tj = tj[2:-1]
                        if tj[-1] == '"':
                            tj = tj[:-1]
                        # tj = "'" + tj + "'"
                        # tj.insert(0, tj)
                        tj_str_li.append(tj)
                    elif index2 == len(tj_str_li_0) - 1:
                        tj = '{"JsToPython": ' + tj[:-2]
                        # tj = "'" + tj + "'"
                        # tj.insert(0, tj)
                        tj_str_li.append(tj)

                for newtj in tj_str_li:
                    # print(newtj)
                    try:
                        tempdata = json.loads(newtj)
                        # print(newdata)
                        tempdata = json.loads(tempdata)
                        # print(n, newdata)
                    except:
                        tempdata = json.loads(newtj)
                        # print(n, newdata)
                    # print(88888, tempdata)
                    all_tj.insert(0, tempdata)
            # except:
            #     pass
            if len(all_tj) != 0:
                still_tj = '51 still_tj---------------' + str(len(all_tj))
                logging.error(still_tj)
                newdata = all_tj.pop(0)
            else:
                newdata = ''
            # print(9999999, newdata)
            logging.error('Scrapy tj qc:' + str(newdata))
            try:
                try:
                    if newdata['channelType'] == 2:   # 历史搜索条件
                        if tjgx_51 != str(newdata['jsonData']):
                            tjgx_51 = str(newdata['jsonData'])
                            tj_data = newdata['jsonData']
                            tj_data = json.loads(tj_data)
                            try:
                                jobid = tj_data['jobId']

                                search_value = module_51_1.search_resume_51(tj_data)
                                ss_num = module_51_1.read_resume_51(searchValueHid=search_value, orgid=org_id, jobid=jobid, max_num=50)
                                sum_num = ss_num + sum_num
                                logging.error("the history_tj_51 got jl number:" + str(ss_num))
                            except:
                                logging.exception("Exception Logged")
                                pass
                                
                except:
                    logging.error('no history tj 51 ...')
                    pass
                try:
                    if newdata['JsToPython']['channel'] == 2:   # 新增条件
                        if tjgx_51 != str(newdata['JsToPython']['json']):
                            tjgx_51 = str(newdata['JsToPython']['json'])
                            tj_data = newdata['JsToPython']['json']
                            try:
                                jobid = newdata['JsToPython']['json']['jobId']

                                search_value = module_51_1.search_resume_51(tj_data)
                                ss_num = module_51_1.read_resume_51(searchValueHid=search_value, orgid=org_id, jobid=jobid, max_num=50)
                                sum_num = ss_num + sum_num
                                logging.error("the current_tj_51 got jl number:" + str(ss_num))
                            except:
                                logging.exception("Exception Logged")
                                pass
                except:
                    logging.error('no current tj 51 ...')
                    pass
            except:
                pass
            if sum_num >= 1000:
                go_on = False

        time.sleep(8*60)
def change_cookie_lg(driver, hostKey):
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
    # driver.get(url)
    driver.delete_all_cookies()
    for row in cookies:
        # print(row)
        dc = decrypt(row[4])
        # cookie_one2 = str(row[1]) + '=' + str(dc, encoding='utf-8')
        # cookies_all_list.append(cookie_one2)
        # if str(row[1]) in cookies_name_list:
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
def get_email():
    email_conn_mysql = True
    lg_yzzt_times = 0
    hzrc_yzzt_times = 0
    while email_conn_mysql:
        lg_yzzt = False
        try:
            js_to_py = {}
            js_to_py['org_id'] = org_id
            # print('单位ID：', org_id)
            if not org_id:
                time.sleep(2)
                continue
            data = json.dumps(js_to_py)
            data = data.encode('utf-8')
            resp_page = requests.get(url=API_URL, data=data)
            # 查看最终发出去的url
            # print('11111', resp_page.url)
            # 修改返回值的编码
            resp_page.encoding = 'utf-8'
            # print(22222, resp_page.text)
            email_cont_data = json.loads(resp_page.text)
            # print('查询返回数据：', email_cont_data)
            if email_cont_data['data'] == 'no':
                time.sleep(30)
                continue
            for email_cont in email_cont_data['data']:
                logging.error('email---begin' + str(email_cont))
                logging.error(str(email_cont))
                # print(email_cont)
                Email, resume_cont_v, orgid_v, email_d_v = email_cont
                if 'hzrc--------http' in resume_cont_v:
                    try:
                        try:
                            cookies_hzrc_1 = 'UM_distinctid=163de889caed3-028b380ab63eff-44410a2e-100200-163de889caf41c; _ubm_id.d2cc513d10e26176994c26da25947ea2=1096e84c977a2486; longinUser=wb; Hm_lvt_46b0265c3ac55b35a0fc9e4683094a94=1528508654,1528685759; JSESSIONID=fFwgwAdo1QFX1mrVudLvHNpTntWrDysZgTlsfgj8A1c9cFn9Q-Cw!-196033929; CNZZDATA2145298=cnzz_eid%3D868844613-1528441555-null%26ntime%3D1529560309; _ubm_ses.d2cc513d10e26176994c26da25947ea2=*; Hm_lpvt_46b0265c3ac55b35a0fc9e4683094a94=1529563918'
                            cookies_hzrc_1 = al_qf.get_cook_str('.hzrc.com', cookies_hzrc_1)
                            module_hzrc_01 = Module_hzrc(cookies_hzrc_1)
                            module_hzrc_01.login_judge_hzrc()
                            login_hzrc = True
                        except:
                            login_hzrc = False
                            logging.error('email hzrc have  not login stat')
                        # print(26262)

                        if login_hzrc:
                            hzrc_xz_url = resume_cont_v.split('hzrc--------', 1)[1]
                            hzrc_jlcont_li = hzrc_email(module_hzrc_01, hzrc_xz_url, dt_2=email_d_v)
                            # print(666, hzrc_jlcont_li)
                            logging.error('email hzrc have returned data')
                            if hzrc_jlcont_li == None:
                                logging.error('returned data is None')
                                continue
                            for hzrc_jlcont in hzrc_jlcont_li:
                                try:
                                    jl_name = hzrc_jlcont['info']['name']
                                    jl_sex = hzrc_jlcont['info']['sex']
                                    jl_phone = hzrc_jlcont['info']['mobilephone']
                                    jl_age = hzrc_jlcont['info']['birth_year']
                                    select_sql = {}
                                    select_sql['select'] = [orgid_v, Email, jl_name, jl_sex, jl_phone, jl_age]
                                    data = json.dumps(select_sql)
                                    data = data.encode('utf-8')
                                    email_cont_num = requests.get(url=API_URL, data=data)
                                    print('数量：', email_cont_num.text)
                                    resp_page.encoding = 'utf-8'
                                    # print(22222, resp_page.text)
                                    email_cont_num = json.loads(email_cont_num.text)
                                    if not email_cont_num['num']:
                                        data_wu_hzrc = []
                                        hzrc_jlcont['org']['original_email'] = Email
                                        hzrc_jlcont = convert_code(hzrc_jlcont, resp_code_dic, 5)
                                        data_wu_hzrc.append(hzrc_jlcont)
                                        data = json.dumps(data_wu_hzrc)
                                        data = data.encode('utf-8')
                                        resp_page = requests.post(url=wu_jl_url, data=data)
                                        logging.error(jl_name + jl_phone + '-----已发送...')
                                        insert_sql = {}
                                        insert_sql['insert'] = [Email, hzrc_jlcont, email_d_v, orgid_v]
                                        data = json.dumps(insert_sql)
                                        data = data.encode('utf-8')
                                        email_cont_num = requests.get(url=API_URL, data=data)
                                        print('hzrc:', hzrc_jlcont)
                                    else:
                                        logging.error(jl_name + jl_phone + '-----已经存在，不再发送...')
                                except:
                                    logging.exception("Exception Logged")
                            select_del = {}
                            select_del['del'] = [orgid_v, resume_cont_v]
                            data = json.dumps(select_del)
                            data = data.encode('utf-8')
                            email_cont_num = requests.get(url=API_URL, data=data)
                        else:
                            if hzrc_yzzt_times == 0:
                                hzrc_yzzt_times = 1
                                try:
                                    send_lg = {}
                                    send_lg['messageContent'] = "系统检测到您的邮箱有来自杭州人才网的简历，请您登录杭州人才网以便系统正常获取简历。"
                                    send_lg['orgId'] = orgid_v
                                    send_lg['account'] = Account
                                    data = json.dumps(send_lg)
                                    data = data.encode('utf-8')
                                    resp_page = requests.post(url=POP_OUT_URL, data=data)
                                    logging.error('弹出窗口返回---hzrc' + str(resp_page.text))
                                    print('弹出窗口返回---hzrc' + str(resp_page.text))
                                except:
                                    logging.error('弹出窗口失败---hzrc')
                    except:
                        logging.exception("Exception Logged")
                    # sql_del = "delete from resume_data where resume_cont='" + resume_cont_v + "' and orgid_v='" + orgid_v + "'"
                    # # print(sql_del)
                    # cursor.execute(sql_del)
                    # conn.commit()
                elif 'lg--------http' in resume_cont_v:
                    try:
                        eamil_jl_url_lg = resume_cont_v.split('lg--------', 1)[1]
                        if not lg_yzzt:
                            headers_jt = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                            }
                            cap = DesiredCapabilities.PHANTOMJS.copy()  # 使用copy()防止修改原代码定义dict
                            for key, value in headers_jt.items():
                                cap['phantomjs.page.customHeaders.{}'.format(key)] = value
                            exe_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'phantomjs.exe'
                            driver_email_lg = webdriver.PhantomJS(desired_capabilities=cap, executable_path=exe_path)
                            if 'http://' in eamil_jl_url_lg:
                                eamil_jl_url_lg = eamil_jl_url_lg.replace('http://', 'https://')
                                # print(eamil_jl_url_lg, '6666666')
                                # time.sleep(100000)
                            driver_email_lg = change_cookie_lg(driver_email_lg, 'lagou.com')
                            driver_email_lg.get(eamil_jl_url_lg)
                            time.sleep(6)
                            lg_email_pagesource = driver_email_lg.page_source
                            if '密码登录' in lg_email_pagesource and '验证码登录' in lg_email_pagesource:
                                if lg_yzzt_times == 0:
                                    try:
                                        send_lg = {}
                                        send_lg['messageContent'] = "系统检测到您的邮箱有来自拉勾网的简历，请您登录拉勾网以便系统正常获取简历。"
                                        send_lg['orgId'] = orgid_v
                                        send_lg['account'] = Account
                                        data = json.dumps(send_lg)
                                        data = data.encode('utf-8')
                                        resp_page = requests.post(url=POP_OUT_URL, data=data)
                                        logging.error('弹出窗口返回---lg' + str(resp_page.text))
                                        # print('弹出窗口发送---lg' + str(send_lg))
                                        # print('弹出窗口返回---lg' + str(resp_page.text))
                                    except:
                                        logging.error('弹出窗口失败---lg')
                                    lg_yzzt_times = 1
                                driver_email_lg.quit()
                                time.sleep(60*2)
                                continue
                            else:
                                driver_email_lg.quit()
                                lg_yzzt = True
                                logging.error("lg email 通过验证")
                        cookies_basis_lg = '_ga=GA1.2.1276485683.1530750746; user_trace_token=20180705083229-e6220212-7fea-11e8-be58-525400f775ce; LGUID=20180705083229-e62207ee-7fea-11e8-be58-525400f775ce; index_location_city=%E6%9D%AD%E5%B7%9E; gray=resume; _ga=GA1.3.1276485683.1530750746; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%221646d1bdc7c2c-000f4cb5128556-44410a2e-1049088-1646d1bdc7d56d%22%2C%22first_id%22%3A%221646d1bdc7c2c-000f4cb5128556-44410a2e-1049088-1646d1bdc7d56d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LG_LOGIN_USER_ID=e0d153e5d03542fca441c66baf383d30114fe010da089d88b816b2cb49a8187e; JSESSIONID=ABAAABAAADAAAEE13E1782DCA911A8A3975BA2D52D2A6B4; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="ApNWmADVL3ADevZdlCvJLXtaBhWGKJ6M3PzMGPai2v9OUE8PlG7kgJiVQj/c7XPksYVMjL5F1MaDqjjrl3DFhd3tQouZ+uHHVyDOtigA5eYhKmOgGL4exWQRRNppYjI3Y3BQQf6n/ALHdZZdHz3OhTmVB3BHxsRjcoBZnBzIcKt4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; X_HTTP_TOKEN=1493260579a754a8617dcd7a7eb0c233; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530750745,1530837338,1530838887,1531096198; _gid=GA1.2.1123753758.1531096198; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530838940,1531111192; LGSID=20180709154105-6fa816c9-834b-11e8-993c-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531123601; gate_login_token=b04cccf5d0b61ece2b71be1daec9d225cd046675b1708a20455394ac4d9786cd; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530868055,1531096192,1531123603,1531123617; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531125149; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531127477; LGRID=20180709171116-0931dd7e-8358-11e8-821f-525400f775ce; _gat=1'
                        cookies_str_lg = al_qf.get_cook_str(".lagou.com", cookies_basis_lg)
                        Lg = Module_lg(cookies_str_lg)
                        dt_sec = time_sec(str(email_d_v))
                        try:
                            cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
                            cookies_str_lg = al_qf.get_cook_str("easy.lagou.com", cookies_basis_lg)
                            login_judge_res = Lg.login_judge_lg(cookies_str_lg)  # 判断是否登陆
                            login_lg = True
                            # print('已经得了')
                        except:
                            traceback.print_exc()
                            login_lg = False
                            # print("scpy email lg login fail---渠道未登录")
                            logging.error("scpy email lg login fail---渠道未登录")
                        if login_lg:
                            logging.error("开始获取拉钩邮件：" + resume_cont_v)
                            # print("开始获取拉钩邮件：" + resume_cont_v)
                            try:
                                # lg_jl_data = Lg.get_email_jl(lg_url, org_id=orgid_v, dt=dt_sec, Email=Email)
                                # print(lg_jl_data)
                                file_cj_dir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'Mod_Cj'
                                cj_file = file_cj_dir + os.sep + str(int(time.time() * 10000)) + '.txt'
                                lg_email_text = str(resume_cont_v) + '--------' + str(Email) + '--------' + str(email_d_v) + '--------' + str(orgid_v)
                                with open(cj_file, 'w+', errors='ignore') as f_Cj:
                                    f_Cj.write(lg_email_text)
                                print('获取成功')
                            except:
                                traceback.print_exc()
                                # time.sleep(1000)
                            # print(lg_jl_data)
                            # logging.error('lg return data is:' + str(lg_jl_data))
                            # if lg_jl_data != None:
                            #     data_wu_hzrc = []
                            #     lg_jl_data['org']['original_email'] = Email
                            #     data_wu_hzrc.append(lg_jl_data)
                            #     data = json.dumps(data_wu_hzrc)
                            #     data = data.encode('utf-8')
                            #     resp_page = requests.post(url=wu_jl_url, data=data)
                            #     # print('lg:', lg_jl_data)
                            #     sql_insert = "insert into resume_data(email_v, resume_cont, email_d,orgid_v) values(%s,%s,%s,%s)"
                            #     insert_info = (str(Email), str(lg_jl_data), str(email_d_v), str(org_id))
                            #     cursor.execute(sql_insert, insert_info)
                            #     conn.commit()
                            # else:
                            #     logging.error('lg return data is:None')
                            select_del = {}
                            select_del['del'] = [orgid_v, resume_cont_v]
                            data = json.dumps(select_del)
                            data = data.encode('utf-8')
                            email_cont_num = requests.get(url=API_URL, data=data)
                            logging.error('删除数据库' + resume_cont_v)
                    except:
                        logging.exception("Exception Logged")
        except:
            traceback.print_exc()
            logging.exception("Exception Logged")
            pass
        time.sleep(60)
# def scra_gj(module_gj_1):
#     global tjgx_gj
#     global login_gj
#     sum_num = 0
#     go_on = True
#     sjx = 1
#     yxz = 1
#     newdata_gj = get_tj(4)
#     if newdata_gj:
#         all_tj = newdata_gj
#     else:
#         all_tj = []
#     while not login_gj:
#         time.sleep(60*30)
#         try:
#             conf = configparser.ConfigParser(strict=False, allow_no_value=True)
#             ini_p = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '/pyth/conf.ini'
#             if r'\\' in ini_p:
#                 ini_p = ini_p.replace(r'\\', '/')
#             conf.read(ini_p, encoding='utf-8')  # 文件路径
#             login_gj_r = conf.get("config", "login_gj")
#             if login_gj_r == 'True':
#                 cookies_str_gj = al_qf.get_cook_str('.ganji.com', cookies_basis_gj)
#                 module_gj_1 = Module_gj(cookies_str_gj)
#                 try:
#                     module_gj_1.login_judge_gj()
#                     login_gj = True
#                 except:
#                     login_gj = False
#         except:
#             pass
#     while login_gj:
#         time.sleep(60)
#         if go_on:
#             ini_path = os.getcwd() + os.sep + 'Config.ini'
#             try:
#                 conf = configparser.ConfigParser(strict=False, allow_no_value=True)
#                 conf.read(ini_path, encoding='utf-8')  # 文件路径
#                 port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
#                 port = int(port)
#                 Account = conf.get("PUB_CONF", "PY_ACC")
#                 org_id = conf.get("PUB_CONF", "PY_COM")
#             except:
#                 Account = ''
#                 org_id = ''
#             # try:
#             js_to_py = {}
#             js_to_py['JsToPython'] = {}
#             js_to_py['JsToPython']['type'] = 'ChannelTj'
#             js_to_py['JsToPython']['channel'] = 4
#             data = json.dumps(js_to_py)
#             data = data.encode('utf-8')
#             url_to_js = 'http://127.0.0.1:' + str(port) + '/JsPython?account=' + str(Account)
#             tj_text = requests.post(url=url_to_js, data=data)
#             tj_str = tj_text.text
#             # print(tj_str)
#             if tj_str != str([]):
#                 tj_str = tj_str.replace("'", '"')
#                 tj_str_li_0 = tj_str.split(', "{"JsToPython": ')
#                 tj_str_li = []
#                 for index2, tj in enumerate(tj_str_li_0):
#                     if 0 < index2 < len(tj_str_li_0) - 1:
#                         tj = '{"JsToPython": ' + tj[:-1]
#                         # tj = "'" + tj + "'"
#                         # tj.insert(0, tj)
#                         tj_str_li.append(tj)
#                     elif index2 == 0:
#                         tj = tj[2:-1]
#                         if tj[-1] == '"':
#                             tj = tj[:-1]
#                         # tj = "'" + tj + "'"
#                         # tj.insert(0, tj)
#                         tj_str_li.append(tj)
#                     elif index2 == len(tj_str_li_0) - 1:
#                         tj = '{"JsToPython": ' + tj[:-2]
#                         # tj = "'" + tj + "'"
#                         # tj.insert(0, tj)
#                         tj_str_li.append(tj)
#
#                 for newtj in tj_str_li:
#                     # print(newtj)
#                     try:
#                         tempdata = json.loads(newtj)
#                         # print(newdata)
#                         tempdata = json.loads(tempdata)
#                         # print(n, newdata)
#                     except:
#                         tempdata = json.loads(newtj)
#                         # print(n, newdata)
#                     # print(88888, tempdata)
#                     all_tj.insert(0, tempdata)
#             # except:
#             #     pass
#             if len(all_tj) != 0:
#                 still_tj = 'gj still_tj---------------' + str(len(all_tj))
#                 logging.error(still_tj)
#                 newdata = all_tj.pop(0)
#             else:
#                 newdata = ''
#             # print(9999999, newdata)
#             try:
#                 try:
#                     if newdata['channelType'] == 4:   # 历史搜索条件（走上面第二个if）
#                         if tjgx_gj != str(newdata['jsonData']):
#                             tjgx_gj = str(newdata['jsonData'])
#                             tj_data = newdata['jsonData']
#
#                             tj_data = json.loads(tj_data)
#
#                             try:
#                                 jobid = tj_data['jobId']
#
#                                 search_value = module_gj_1.search_resume_gj(tj_data)
#                                 ss_num = module_gj_1.read_resume_gj(search_value, orgid=org_id, jobid=jobid, max_num=50)
#                                 sum_num = ss_num + sum_num
#
#                             except:
#                                 logging.exception("Exception Logged")
#                                 pass
#                 except:
#                     logging.error('tj----------channelType error...')
#                     pass
#                 try:
#                     if newdata['JsToPython']['channel'] == 4:   # 客户端新增（走上面第一个if）
#                         if tjgx_gj != str(newdata['JsToPython']['json']):
#                             tjgx_gj = str(newdata['JsToPython']['json'])
#                             tj_data = newdata['JsToPython']['json']
#
#                             try:
#                                 jobid = newdata['JsToPython']['json']['jobId']
#
#                                 search_value = module_gj_1.search_resume_gj(tj_data)
#                                 ss_num = module_gj_1.read_resume_gj(search_value, orgid=org_id, jobid=jobid, max_num=50)
#                                 sum_num = ss_num + sum_num
#
#                             except:
#                                 logging.exception("Exception Logged")
#                                 pass
#                 except:
#                     logging.error('tj----------channel error...')
#                     pass
#             except:
#                 pass
#             if sum_num >= 1000:
#                 go_on = False


# def scra_lp(module_lp_1):
    # search_value = module_lp_1.search_resume_lp('1')
    # ss_num = module_lp_1.read_resume_lp(searchValueHid=search_value, max_num=10)
    # print(ss_num)

    # global tjgx_lp
    # global login_lp
    # sum_num = 0
    # go_on = True
    # sjx = 1
    # yxz = 1
    # newdata_lp = get_tj(10)
    # if newdata_lp:
    #     all_tj = newdata_lp
    # else:
    #     all_tj = []
    # while not login_lp:
    #     time.sleep(60 * 15)
    #     try:
    #         conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    #         ini_p = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '/pyth/conf.ini'
    #         if r'\\' in ini_p:
    #             ini_p = ini_p.replace(r'\\', '/')
    #         conf.read(ini_p, encoding='utf-8')  # 文件路径
    #         login_lp_r = conf.get("config", "login_lp")
    #         if login_lp_r == 'True':
    #             cookies_str_lp = al_qf.get_cook_str('.liepin.com', cookies_basis_lp)
    #             module_lp_1 = Module_lp(cookies_str_lp)
    #             try:
    #                 module_lp_1.login_judge_lp()
    #                 login_lp = True
    #             except:
    #                 login_lp = False
    #     except:
    #         pass
    # while login_lp:
    #     time.sleep(60)
    #     if go_on:
    #         ini_path = os.getcwd() + os.sep + 'Config.ini'
    #         try:
    #             conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    #             conf.read(ini_path, encoding='utf-8')  # 文件路径
    #             port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
    #             port = int(port)
    #             Account = conf.get("PUB_CONF", "PY_ACC")
    #             org_id = conf.get("PUB_CONF", "PY_COM")
    #         except:
    #             Account = ''
    #             org_id = ''
    #         # try:
    #         js_to_py = {}
    #         js_to_py['JsToPython'] = {}
    #         js_to_py['JsToPython']['type'] = 'ChannelTj'
    #         js_to_py['JsToPython']['channel'] = 10
    #         data = json.dumps(js_to_py)
    #         data = data.encode('utf-8')
    #         url_to_js = 'http://127.0.0.1:' + str(port) + '/JsPython?account=' + str(Account)
    #         tj_text = requests.post(url=url_to_js, data=data)
    #         tj_str = tj_text.text
    #         # print(tj_str)
    #         if tj_str != str([]):
    #             tj_str = tj_str.replace("'", '"')
    #             tj_str_li_0 = tj_str.split(', "{"JsToPython": ')
    #             tj_str_li = []
    #             for index2, tj in enumerate(tj_str_li_0):
    #                 if 0 < index2 < len(tj_str_li_0) - 1:
    #                     tj = '{"JsToPython": ' + tj[:-1]
    #                     # tj = "'" + tj + "'"
    #                     # tj.insert(0, tj)
    #                     tj_str_li.append(tj)
    #                 elif index2 == 0:
    #                     tj = tj[2:-1]
    #                     if tj[-1] == '"':
    #                         tj = tj[:-1]
    #                     # tj = "'" + tj + "'"
    #                     # tj.insert(0, tj)
    #                     tj_str_li.append(tj)
    #                 elif index2 == len(tj_str_li_0) - 1:
    #                     tj = '{"JsToPython": ' + tj[:-2]
    #                     # tj = "'" + tj + "'"
    #                     # tj.insert(0, tj)
    #                     tj_str_li.append(tj)
    #
    #             for newtj in tj_str_li:
    #                 # print(newtj)
    #                 try:
    #                     tempdata = json.loads(newtj)
    #                     # print(newdata)
    #                     tempdata = json.loads(tempdata)
    #                     # print(n, newdata)
    #                 except:
    #                     tempdata = json.loads(newtj)
    #                     # print(n, newdata)
    #                 # print(88888, tempdata)
    #                 all_tj.insert(0, tempdata)
    #         # except:
    #         #     pass
    #         if len(all_tj) != 0:
    #             still_tj = 'lp still_tj---------------' + str(len(all_tj))
    #             logging.error(still_tj)
    #             newdata = all_tj.pop(0)
    #         else:
    #             newdata = ''
    #         # print(9999999, newdata)
    #         logging.error('Scrapy tj lp:' + str(newdata))
    #         try:
    #             try:
    #                 if newdata['channelType'] == 10:  # 历史搜索条件
    #                     if tjgx_lp != str(newdata['jsonData']):
    #                         tjgx_lp = str(newdata['jsonData'])
    #                         tj_data = newdata['jsonData']
    #                         tj_data = json.loads(tj_data)
    #                         try:
    #                             jobid = tj_data['jobId']
    #
    #                             search_value = module_lp_1.search_resume_lp(tj_data)
    #                             ss_num = module_lp_1.read_resume_lp(searchValueHid=search_value, orgid=org_id,
    #                                                                 jobid=jobid, max_num=50)
    #                             sum_num = ss_num + sum_num
    #                             logging.error("the history_tj_lp got jl number:" + str(ss_num))
    #                         except:
    #                             logging.exception("Exception Logged")
    #                             pass
    #
    #             except:
    #                 logging.error('no history tj lp ...')
    #                 pass
    #             try:
    #                 if newdata['JsToPython']['channel'] == 10:  # 新增条件
    #                     if tjgx_lp != str(newdata['JsToPython']['json']):
    #                         tjgx_lp = str(newdata['JsToPython']['json'])
    #                         tj_data = newdata['JsToPython']['json']
    #                         try:
    #                             jobid = newdata['JsToPython']['json']['jobId']
    #
    #                             search_value = module_lp_1.search_resume_lp(tj_data)
    #                             ss_num = module_lp_1.read_resume_lp(searchValueHid=search_value, orgid=org_id,
    #                                                                 jobid=jobid, max_num=50)
    #                             sum_num = ss_num + sum_num
    #                             logging.error("the current_tj_lp got jl number:" + str(ss_num))
    #                         except:
    #                             logging.exception("Exception Logged")
    #                             pass
    #             except:
    #                 logging.error('no current tj lp ...')
    #                 pass
    #         except:
    #             pass
    #         if sum_num >= 1000:
    #             go_on = False
    #
    #     time.sleep(8 * 60)


def login_sx():
    while True:
        time.sleep(1800)
        js_to_py = {}
        js_to_py['JsToPython'] = {}
        js_to_py['JsToPython']['type'] = 'isLogin_auto'
        js_to_py['JsToPython']['timestamp'] = 225656565
        js_to_py['JsToPython']['channels'] = [1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 16]
        data = json.dumps(js_to_py)
        data = data.encode('utf-8')
        # print(data)
        ini_path = os.getcwd() + os.sep + 'Config.ini'
        try:
            conf = configparser.ConfigParser(strict=False, allow_no_value=True)
            conf.read(ini_path, encoding='utf-8')  # 文件路径
            port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
            Account = conf.get("PUB_CONF", "PY_ACC")
            org_id = conf.get("PUB_CONF", "PY_COM")
            port = int(port)
        except:
            port = 8900
            Account = ''
        try:
            url_to_js = 'http://127.0.0.1:' + str(port) + '/JsPython?account=' + str(Account)
            requests.post(url=url_to_js, data=data)
        except:
            pass
def kill_self():
    while 1:
        time.sleep(60)
        p_list = []
        procs = psutil.process_iter()
        for proc in procs:
            name = proc.name()
            # print(name)
            p_list.append(name)
        if 'Mod_Main.exe' not in p_list:
            filebat = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'kp.bat'
            # print(filebat)
            subprocess.Popen(filebat, shell=True)

run_M()


