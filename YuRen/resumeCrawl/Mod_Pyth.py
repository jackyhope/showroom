# -*- coding: utf-8 -*-


'''

开启服务，负责接收插件发送的请求、根据请求获取指定招聘网站当前用户的信息及刷新职位、简历下载点数
负责查询并下载指定简历，负责将下载简历后的联系方式发送给客户端，负责实现版本自动更新

'''


from PIL import Image, ImageEnhance, ImageOps
import shutil
import logging
import requests
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

from lxml import etree
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
import al_qf
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
import psutil
import al_qf,zl_xghs,func_lg,func_zhyc,func_djw
from func_51 import Module_51, dl_51
from func_58 import Module_58
from func_hzrc import Module_hzrc
from func_lp import Module_lp, jx_lp_ss
from func_gj import Module_gj, jljx_gjw, jljx_gjw_jz
from func_boss import Module_boss
from func_sxs import Module_sxs
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.utils import parsedate
import uuid
from win32com import client as wc
import shutil
import zipfile
import urllib.request
from fontTools.ttLib import TTFont
import xml.etree.cElementTree as ET
import pythoncom
import platform
import getpass
import oss2
import execjs
import fitz
import glob
from settings import *
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
def judge_load_stat(download_dic):
    stat_dl = {}
    try:
        if download_dic['phone'] == '':
            stat_dl['stat'] = False
            stat_dl['msg'] = '该简历点数不足或下载失败'
        else:
            stat_dl['stat'] = True
            stat_dl['msg'] = ''
    except:
        stat_dl['stat'] = False
        stat_dl['msg'] = '该简历点数不足或下载失败'
    return stat_dl
class singleinstance:
    """ Limits application to single instance """

    def __init__(self):

        self.mutexname = "testmutex_{D0E858DweF-985E-4907we-B7FB-8D732C3modpyth}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def aleradyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)

    # def __del__(self):
    #     if self.mutex:
    #         CloseHandle(self.mutex)
try:
    myapp = singleinstance()

    # 检查是否已经有实例在运行了
    if myapp.aleradyrunning():
        # time.sleep(60)
        exit(0)
        # return None
    else:
        # 如果没有运行则正常运行程序
        pass
except:
    exit(0)

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
filedir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'logging'
filelog = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'logging' + os.sep + 'logging.log'
# print(new_tj)
if not os.path.exists(filedir):
    # print('文件夹', new_tj, '不存在，重新建立')
    # os.mkdir(file_path)
    os.makedirs(filedir)
else:
    shutil.rmtree(filedir)
    os.makedirs(filedir)
logging.basicConfig(
    level=logging.ERROR,  # 定义输出到文件的log级别，
    format='%(asctime)s : %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    filename=filelog,  # log文件名
    filemode='a')  # 写入模式“w”或“a”

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
    UPDATE_URL = conf_ini.get("INIT_START", "UPDATE_URL")
except:
    pass
try:
    wu_jl_url = RESUME_DOWNLOAD_URL
    code_url = RESUME_CODES_URL
    resp_code_page = requests.get(url=code_url)
    resp_code_page.encoding = 'utf-8'
    resp_code_dic = json.loads(resp_code_page.text)
    logging.error('have get code_dic')
except:
    logging.error('get code_dic false')
ini_path = os.getcwd() + os.sep + 'Config.ini'
try:
    logging.error('reading Configfile 1...')
    now_day = datetime.datetime.now().day
    today1 = str(datetime.datetime.now())[0:10]
    conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    conf.read(ini_path, encoding='utf-8')  # 文件路径
    # cq = conf.get("PUB_CONF", "PY_TIME")  # 获取指定section 的option值
    f = conf.read(ini_path)
    try:
        logging.error('reading Configfile 1...remove py_time')
        jieguo1 = conf.remove_option("PUB_CONF", "PY_TIME")  # 删除节内参数
        with open(ini_path, "w") as f:
            conf.write(f)
        # conf.write(open(ini_path, "w"))
    except:
        logging.exception("Exception Logged")
        # print('删除py_time失败')
        logging.error('reading Configfile 1...remove py_time fail')
        pass
    # conf.set("PUB_CONF", "PY_TIME", '')  # 修改参数（第一个参数为节点名称）
    # conf.write(open(ini_path, "r+"))
except:
    logging.exception("Exception Logged")
    logging.error('reading Configfile 1 fail...')
    pass
new_tj = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'pyth' + os.sep + 'new_tj'
# print(new_tj)
if not os.path.exists(new_tj):
    # print('文件夹', new_tj, '不存在，重新建立')
    # os.mkdir(file_path)
    os.makedirs(new_tj)
else:
    shutil.rmtree(new_tj)
    os.makedirs(new_tj)
logging.error('creat newtj_dir')
def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.mkdir(unziptodir)
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
            if not os.path.exists(ext_dir): os.mkdir(ext_dir)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = 'xFLQb;:e'
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    # 此处加密后转换为base64编码，返回
    return binascii.b2a_base64(en)
def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    secret_key = 'xFLQb;:e'
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    # 加密后的字符串，16进制
    # de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    # 8字符串，64位的
    # 此处先进性64位解base64码，然后解密des后返回
    de = k.decrypt(binascii.a2b_base64(s), padmode=PAD_PKCS5)
    return de
def jia_syh(dirgra):
    dirgra_s = dirgra
    dirgra_d = dirgra
    yk = True
    yk_s = []
    yk_m = []
    while yk:
        if ' ' in dirgra_s:
            dir_li = dirgra_s.split(os.sep)
            for dir1 in dir_li:
                if ' ' in dir1:
                    yk_s.append(dir1)
                    dir2 = '"' + dir1 + '"'
                    yk_m.append(dir2)
                    dirgra_s = dirgra_s.replace(dir1, 'nihao')
                    if ' ' not in dirgra:
                        yk = False
        else:
            yk = False
    leng = len(yk_m)
    for i in range(leng):
        dirgra_d = dirgra_d.replace(yk_s[i], yk_m[i])
    return dirgra_d

def WriteRestartCmd(exe_name):
    # 更新文件夹在当前目录的up_date目录下
    source_dir = os.getcwd() + os.sep + "Mod_Pyth" + os.sep + 'up_date' + os.sep + 'Mod_Pyth.exe'
    source_dir = jia_syh(source_dir)
    # print(source_dir)
    md_dir = os.getcwd() + os.sep + "Mod_Pyth" + os.sep + 'Mod_Pyth.exe'
    md_dir = jia_syh(md_dir)
    # print(md_dir)
    logging.error('write update_bat')
    b = open("up_date.bat", 'w')
    TempList = "@echo off \n"   # 关闭bat脚本的输出
    # TempList += "if not exist "+source_dir+" exit \n"    #新文件不存在,退出脚本执行
    TempList += "ping 0.0.0.0  -n 4 > null \n" #3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
    TempList += "del " + md_dir + "\n"    #删除当前文件
    TempList += "move /Y " + source_dir + " " + md_dir + "\n"    #更新当前文件
    TempList += "start " + md_dir    # 启动新程序
    b.write(TempList)
    b.close()
    logging.error('begin RestartCmd success')
    st = subprocess.STARTUPINFO
    st.dwFlags = subprocess.STARTF_USESHOWWINDOW
    st.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen("up_date.bat", stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
    # subprocess.Popen("up_date.bat")
    sys.exit()
kill_proc_li = ['Mod_Cj.exe','Mod_Ymjx.exe','Mod_Scpy.exe','phantomjs.exe']
def gx_main():
    for s_dir in kill_proc_li:
        source_dir = os.getcwd() + os.sep + "Mod_Pyth" + os.sep + 'up_date' + os.sep + s_dir
        if os.path.exists(source_dir):
            if s_dir != 'Mod_Ymjx.exe':
                md_dir = os.getcwd() + os.sep + "Mod_Pyth" + os.sep + s_dir
            else:
                md_dir = os.getcwd() + os.sep + "Mod_Ymjx" + os.sep + s_dir
            if os.path.exists(md_dir):
                os.remove(md_dir)
            shutil.copyfile(source_dir, md_dir)
            logging.error('copyfile {} success'.format(source_dir))
    logging.error('kill proc_li success')
    gx_file = "Mod_Pyth.exe"
    WriteRestartCmd(gx_file)

up_date_path = 'Mod_Pyth' + os.sep + 'up_date'
if not os.path.exists(up_date_path):
    # print('文件夹', up_date_path, '不存在，重新建立')
    #os.mkdir(file_path)
    os.makedirs(up_date_path)
now_time = datetime.datetime.now()
now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
ask_js = {
    "version_check": {
        "timestamp": now_time,
        "prodId": "9300",
        "version": "1.0.3",
    }
}
data = json.dumps(ask_js)
data = data.encode('utf-8')
str_en = des_encrypt(data)
url_up_date = UPDATE_URL
# url_up_date = 'http://114.55.73.58:9968/upgrade/pc'
# url_up_date = 'http://192.168.1.13:9970/upgrade/pc'
logging.error('xwgx beg')
xx = requests.post(url=url_up_date, data=str_en)  # 判断版本是否需要更新

str_de = des_descrypt(xx.text)
up_dict = json.loads(str_de.decode('utf-8'))
# print(url_up_date)
# print(up_dict)

try:
    gx_stat = up_dict['newVersion']
except:
    # logging.exception("Exception Logged")
    # print('没有更新的版本')
    gx_stat = 0

# time.sleep(1000)
class gx_MainApp(wx.App):
    def OnInit(self):
        # self.SetBackgroundColour('#ffffff')
        msgDialog = wx.MessageDialog(None, u'亲，程序需要更新，请在收到更新成功提示后重启……', u'温馨提示：', wx.YES_NO | wx.ICON_INFORMATION)
        if msgDialog.ShowModal() == wx.ID_NO:
            pass
        pass
        return True
class gxcg_MainApp(wx.App):
    def OnInit(self):
        # self.SetBackgroundColour('#ffffff')
        msgDialog = wx.MessageDialog(None, u'亲，更新成功，请30秒后重启……', u'温馨提示：', wx.YES_NO | wx.ICON_INFORMATION)
        if msgDialog.ShowModal() == wx.ID_NO:
            pass
        pass
        return True

if gx_stat:
    logging.error('xwgx true')
    xz_update = True
    while xz_update:
        try:
            ini_path = os.getcwd() + os.sep + 'Config.ini'
            # print(ini_path)
            try:
                now_day = datetime.datetime.now().day
                today1 = str(datetime.datetime.now())[0:10]
                conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                conf.read(ini_path, encoding='utf-8')  # 文件路径
                # cq = conf.get("PUB_CONF", "PY_TIME")  # 获取指定section 的option值
                # f = conf.read(ini_path)
                conf.set("PUB_CONF", "PY_TIME", today1)
                with open(ini_path, "w") as f:
                    conf.write(f)
                # conf.write(open(ini_path, "w"))
            except:
                logging.exception("Exception Logged")
                # traceback.print_exc()
                # print('打开配置文件失败')
            app = gx_MainApp()
            app.MainLoop()
            pkgUrl = up_dict['pkgUrl']
            logging.error(pkgUrl)
            # update_zip = requests.get(pkgUrl, timeout=1000)
            source_zip_update = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'up_date.zip'
            target_zip_update = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'up_date'
            logging.error(source_zip_update)
            logging.error(target_zip_update)
            urllib.request.urlretrieve(up_dict['pkgUrl'], source_zip_update)
            # print('下载更新包成功')
            update_wait_time = 0
            while update_wait_time <= 40:
                try:
                    time.sleep(5)
                    # with open(source_zip_update, 'wb') as up_zip:
                    #     up_zip.write(update_zip.content)
                    unzip_file(source_zip_update, target_zip_update)
                    logging.error('unzip_file success')
                    break
                except:
                    traceback.print_exc()
                    update_wait_time += 1
            os.remove(source_zip_update)
            logging.error('remove source_zip_update success')
            xz_update = False
        except:
            traceback.print_exc()
            logging.exception("Exception Logged")

    for proc in psutil.process_iter():
        if proc.name() in kill_proc_li:
            proc_name = proc.name()
            while True:
                try:
                    # print("pid-%d,name:%s" % (proc.pid, proc.name()))
                    cmd_str = 'taskkill /IM {} /T /F > null '.format(str(proc_name))
                    os.popen(cmd_str)
                    time.sleep(1)
                    proc_name_li = []
                    for proc in psutil.process_iter():
                        proc_name_li.append(proc.name())
                    if proc_name not in proc_name_li:
                        logging.error('kill process {} success'.format(str(proc_name)))
                        break
                except:
                    traceback.print_exc()
                    logging.exception("Exception Logged gx_process")
                    pass

    logging.error('kill proc_li success')
    app = gxcg_MainApp()
    app.MainLoop()

    try:
        gx_main()
    except:
        traceback.print_exc()
        logging.error('gx fail beacuse:')
        logging.exception('Exception Logged')
    sys.exit()
else:
    logging.error('not need gx')
    ini_path = os.getcwd() + os.sep + 'Config.ini'
    try:
        now_day = datetime.datetime.now().day
        today1 = str(datetime.datetime.now())[0:10]
        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
        conf.read(ini_path, encoding='utf-8')  # 文件路径
        # cq = conf.get("PUB_CONF", "PY_TIME")  # 获取指定section 的option值
        f = conf.read(ini_path)
        try:
            jieguo1 = conf.remove_option("PUB_CONF", "PY_TIME")  # 删除节内参数
            with open(ini_path, "w") as f:
                conf.write(f)
            # conf.write(open(ini_path, "w"))
        except:
            logging.exception("Exception Logged")
            # print('删除py_time失败')
            pass
        # conf.set("PUB_CONF", "PY_TIME", '')  # 修改参数（第一个参数为节点名称）
        # conf.write(open(ini_path, "r+"))
    except:
        logging.exception("Exception Logged")
        pass
if os.path.exists('Mod_Pyth/up_date/Mod_Scpy.exe'):
    os.remove('Mod_Pyth/up_date/Mod_Scpy.exe')
if os.path.exists('Mod_Pyth/up_date/Mod_Pyth.exe'):
    os.remove('Mod_Pyth/up_date/Mod_Pyth.exe')
if os.path.exists('Mod_Pyth/up_date/Mod_Cj.exe'):
    os.remove('Mod_Pyth/up_date/Mod_Cj.exe')
if os.path.exists('Mod_Pyth/up_date/Mod_Ymjx.exe'):
    os.remove('Mod_Pyth/up_date/Mod_Ymjx.exe')

now_osuser = getpass.getuser()
os_platform = platform.platform()
chrome_place = al_qf.get_chrome_cookies_place()

if 'Windows-XP' in os_platform:
    cookfile = r'C:\Documents and Settings\Administrator\Local Settings\Application Data\Google\Chrome\User Data\Default\Cookies'
else:
    cookfile = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Cookies'
print(now_osuser)
print(os_platform)
cookfile_li = []
last_cookfile = ''
try:
    conn = sqlite3.connect(cookfile)
except:
    traceback.print_exc()
    if now_osuser != 'Administrator':
        cookfile_1 = cookfile.replace('Administrator', now_osuser)
        cookfile_li.append(cookfile_1)
    if chrome_place[0][0] != 'C':
        cookfile_2 = cookfile.replace(cookfile[0], chrome_place[0][0], 1)
        cookfile_li.append(cookfile_2)
    for i in cookfile_li:
        try:
            conn = sqlite3.connect(i)
            cookfile = i
            break
        except:
            pass
if not cookfile:
    print('not find cookies_file')
    logging.error('not find cookies_file')
logging.error(cookfile)
# 初始化/更新配置文件
try:
    logging.error('init configfile...')
    try:
        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
        # print(ini_p)
        if r'\\' in ini_p:
            ini_p = ini_p.replace(r'\\', '/')
        conf.read(ini_p, encoding='utf-8')  # 文件路径
        cookieFile1 = conf.get('config', 'pro1')
        v_1 = conf.get('config', 'login_zl')
        v_2 = conf.get('config', 'login_51')
        v_3 = conf.get('config', 'login_58')
        v_4 = conf.get('config', 'login_gj')
        v_5 = conf.get('config', 'login_hzrc')
        v_6 = conf.get('config', 'login_boss')
        v_7 = conf.get('config', 'login_lp')
        v_8 = conf.get('config', 'login_lg')
        v_9 = conf.get('config', 'login_zhyc')
        v_10 = conf.get('config', 'login_sxs')
        v_11 = conf.get('config', 'login_djw')

        if cookieFile1 == cookfile:
            pass
        else:
            f = conf.read(ini_p)
            conf.set("config", "pro1", cookfile)  # 修改参数（第一个参数为节点名称）
            with open(ini_p, "w") as f:
                conf.write(f)
            # conf.write(open(ini_p, "w"))
    except:
        logging.exception("Exception Logged")
        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
        if r'\\' in ini_p:
            ini_p = ini_p.replace(r'\\', '/')
        al_qf.creat_ini(ini_p)
        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
        conf.read(ini_p, encoding='utf-8')  # 文件路径
        cookieFile1 = conf.get('config', 'pro1')
        if cookieFile1 == cookfile:
            pass
        else:
            f = conf.read(ini_p)
            conf.set("config", "pro1", cookfile)  # 修改参数（第一个参数为节点名称）
            with open(ini_p, "w") as f:
                conf.write(f)
            # conf.write(open(ini_p, "w"))
except:
    logging.exception("Exception Logged")
    logging.error('init configfile...fail')
try:
    curdir = path.dirname(path.realpath(__file__))
    sep = '/'

    # wu_url_init = 'http://192.168.1.42:9091/sys/searchSysSetChannelRules'


    # wu_cjbc_url = 'http://47.98.103.128:9090/resume/cleanoutResumes'
    # wu_url_init = 'http://47.98.103.128:9090/sys/searchSysSetChannelRules'
    # wu_cjxw_url = 'http://47.98.103.128:9090/resume/searchResumeStatusForPlugin'
    # wu_jl_url = 'http://47.98.103.128:9090/resume/cleanoutResumes'

    # 与客户端通信在下边
    # url_to_js = 'http://127.0.0.1:3366/PythonJs?account=' + str(Account)

    logging.error('run zl-----1')
    cookies_basis_zl = "dywez=95841923.1547435200.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; __utmz=269921210.1547435200.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sts_deviceid=1684a534fea6e-0ab02dcf65084c-424e0b28-1049088-1684a534feb60e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22132309766%22%2C%22%24device_id%22%3A%221684a534fd9da-0274ad56ba18a8-424e0b28-1049088-1684a534fdaa4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221684a534fd9da-0274ad56ba18a8-424e0b28-1049088-1684a534fdaa4%22%7D; NTKF_T2D_CLIENTID=guestFA8CA7AF-9669-9687-5EA4-4A538E9CE327; __utma=269921210.417566423.1547435200.1547454602.1547457867.5; x-zp-client-id=ffe77a3c-7cba-408f-8a18-ae64cb92fbb0; jobRiskWarning=true; dywea=95841923.1607334818358702800.1547435200.1550218963.1560414257.7; dywec=95841923; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; sts_sg=1; sts_sid=16b4ff000a42e6-0d2dfba4dbf9ff-651a107e-1049088-16b4ff000a5404; sts_chnlsid=Unknown; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1560414257; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1560414257; x-zp-device-id=472b20ab14de2a0d36d150b3f3769290; acw_tc=2760822515604142667813253e859845328f8e4c13c8d94c719953532c9356; JsNewlogin=3049230962; JSloginnamecookie=13018956681; JSShowname=""; login-type=b; zp-route-meta=uid=132309766,orgid=35828671; login_point=35828671; promoteGray=; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1560415456173943}; diagnosis=0; zp_src_url=https%3A%2F%2Frd5.zhaopin.com%2Fcustom%2Fsearch; rd_resume_srccode=402101; at=ac370e87e052453fb771eb18e8311287; Token=ac370e87e052453fb771eb18e8311287; rt=a3a3c7c4de7647f79a802de6dcc61387; JSpUserInfo=386b2e69567146655f700469436d5f6a586b4177566f42355975566b266925714a655e700669456d5a6a516b4877506f46355f75556b5b695071326522700869466d5b6a596b4477566f40355e755e6b5869597137651e7044695b6d086a066b1c775e6f23353d75506b5b69507136653b700869406d466a5d6b5177546f493553755f6b5b695071366523700869446d506a3c6b3077586f3a3520755c6b5c695f7146655f700669476d5b6a596b4a77306f243554755c6b516938713e65527005694e6d3e6a396b3f77586f41355a755d6b5b6953714e655a700369436d536a586b4a779; uiioit=37722066596355665567556653645672556654635766576754665e6420722066596354665e670; rd_resume_actionId=1560424893648132309766; dyweb=95841923.70.10.1560414257; sts_evtseq=89"
    cookies_str_zl = zl_xghs.get_cook_str('.zhaopin.com', cookies_basis_zl)
    # cookies_str_zl = zl_xghs.get_cook_str('.zhaopin.com', cookies_str_zl)
    logging.error('run zl sucess, to run 51-----1')


    cookies_basis_51 = 'guid=15126185243667940069; EhireGuid=57343d4ab9144eeaaac53570c55c6bd5; RememberLoginInfo=member_name=790EDF22D15A367144E78236FFD81B69&user_name=3F6D7EB2B10CC033; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0VmkU00uiAs0aQA-p00000aaJBdb00000X8ZxsW.THLZ_Q5n1VeHksK85ydEUhkGUhNxndqbusK15y7-uj-BP1fdnj0snvnzrjn0IHY4fW0knHI7wWRsrj-KwD7KwRDYnbfdn1n3rDwaP1Naw0K95gTqFhdWpyfqn10LP1T4PWbLPiusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqPHnzPWb%2526tpl%253Dtpl_10085_16624_12226%2526l%253D1502325280%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m4b66f41d%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D233%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dmonline_3_dg%2526inputT%253D4274%26%7C%26adsnum%3D789233; LangType=Lang=&Flag=1; 51job=cuid%3D52237061%26%7C%26cusername%3D13598213097%26%7C%26cpassword%3D%26%7C%26cname%3D%25D1%25EE%25D2%25F8%25B2%25A8%26%7C%26cemail%3D455471846%2540qq.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0g4r6HYlhTBg%26%7C%26cconfirmkey%3D4555sQmuzH7DE%26%7C%26cresumeids%3D.0Sy8EEE7wagc%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D45usYTv%252FFNEs.%26%7C%26to%3DXmMBaANjCz5cOlo2UTJRYwxzBjYANVU1AT5dNwE5BTQNNlA7D2QLOlF8XTALa1ViBT9UZQM0AWRdYlQ%252BATI%253D%26%7C%26; ps=us%3DXGUCawBgVn4CYVg2B2dXegIzBjVWYwZ9VWIBag0zBXkLMgBuUzALOgJnXzRRMAA7Vm0BOQA2UDJdY1Z4D0QANFxhAjEAFw%253D%253D%26%7C%26needv%3D0; _ujz=NTIyMzcwNjEw; AccessKey=d45a0618ef944d1; partner=baidupz; slife=lastlogindate%3D20180209%26%7C%26; ASP.NET_SessionId=tnj5cjfsmtf5h2nf3avtcvrc; HRUSERINFO=CtmID=2424128&DBID=2&MType=02&HRUID=2788355&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=hzjl340&IsStandard=0&LoginTime=02%2f09%2f2018+09%3a01%3a32&ExpireTime=02%2f09%2f2018+09%3a11%3a32&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=bf9abebe61bef674; KWD=SEARCH='
    cookies_str_51 = al_qf.get_cook_str('ehire.51job.com', cookies_basis_51)
    module_51_0 = Module_51(cookies_str_51)
    logging.error('run 51 sucess, to run 58-----1')

    cookies_basis_58 = '58home=hz; id58=c5/njVrkAq4CHw7fCy2pAg==; city=hz; 58tj_uuid=1f516501-df3b-4ebd-9c53-ecc7b1d9b885; als=0; commontopbar_myfeet_tooltip=end; xxzl_deviceid=Hb6BJKfGNnpCtcAZW5scSlpeq0arRmILCxjIJuH%2Bv2dVGVZgAb3wEV4Ca0Ot5vXV; xxzl_smartid=5df4462181a0e9a59ad660693e06180b; showOrder=1; showPTTip=1; ljrzfc=1; wmda_uuid=3bbb65d735f4aca3baf11990491e042a; wmda_new_uuid=1; wmda_visited_projects=%3B1731916484865; getKey=1; new_uv=18; utm_source=; spm=; init_refer=; new_session=0; ppStore_fingerprint=1E29E49F92B622558C0F49B1EEC5C6D071A46AB80C1100D2%EF%BC%BF1526605436746; PPU="UID=34650726585862&UN=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&TT=5a6401ac9086214f9d16ca3b1086d9e7&PBODY=Z8JmnhEeK5SxeIcyEEsZuf89rEIg-vcNBo40_0H-zkIWAdUIHCbzrQ5Q4XFC48aQrJWcGAMR7B-SUAL7zPYcbl4lIn9oaKBoEvC0g6rIRITDcj5qOOuP3efm-Koeua7KdCyiddcL-DbXX0teXQaq0ynbEV-OeY4OeQK-4vz5MIw&VER=1"; 58cooper="userid=34650726585862&username=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&cooperkey=e27167b5b83925fb7d570f5ce95666ab"; www58com="AutoLogin=true&UserID=34650726585862&UserName=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=887EB60F8846773DB0F871F4A103A2056CDD83AE89F6452A0&Phone=&WltUrl=&UserLoginVer=08CDD29DF3C97588732B3336A726CC43F&LT=1526605454806"; vip=vipusertype%3D0%26vipuserpline%3D0%26v%3D1%26vipkey%3D782bcfd78f29e63156ec0afa9efbfc25%26masteruserid%3D34650726585862; wmda_session_id_1731916484865=1526605965138-4d558735-cb44-1cac'
    cookies_str_58 = al_qf.get_cook_str('.58.com', cookies_basis_58)
    module_58_0 = Module_58(cookies_str_58)
    logging.error('run 58 sucess, to run hzrc-----1')

    cookies_basis_hzrc = 'UM_distinctid=163de889caed3-028b380ab63eff-44410a2e-100200-163de889caf41c; _ubm_id.d2cc513d10e26176994c26da25947ea2=1096e84c977a2486; longinUser=wb; Hm_lvt_46b0265c3ac55b35a0fc9e4683094a94=1528508654,1528685759; JSESSIONID=fFwgwAdo1QFX1mrVudLvHNpTntWrDysZgTlsfgj8A1c9cFn9Q-Cw!-196033929; CNZZDATA2145298=cnzz_eid%3D868844613-1528441555-null%26ntime%3D1529560309; _ubm_ses.d2cc513d10e26176994c26da25947ea2=*; Hm_lpvt_46b0265c3ac55b35a0fc9e4683094a94=1529563918'
    cookies_str_hzrc = al_qf.get_cook_str('.hzrc.com', cookies_basis_hzrc)
    module_hzrc_0 = Module_hzrc(cookies_str_hzrc)
    logging.error('run hzrc sucess, to run gj-----1')

    cookies_basis_gj = 'ganji_xuuid=c7dc72ef-60db-4264-aced-0a6a701c2cd3.1528708751959; ganji_uuid=7150266604199787963746; xxzl_deviceid=hNmWYgYm3yVBw3yuNYA%2BLPpzVYJGhHRfC9VGkavtS3QxEfmxbyvsUW%2F%2FIgzp8FIi; lg=1; NTKF_T2D_CLIENTID=guestA8ABE4E8-9FE5-DEC9-A48B-EE251D637B74; cityDomain=bj; citydomain=bj; 58tj_uuid=def2acb6-3e85-430a-8c40-c72caf90a077; als=0; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A31561918616%7D; use_https=1; new_uv=3; __utmc=32156897; __utmz=32156897.1529023568.3.3.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; nTalk_CACHE_DATA={uid:kf_10111_ISME9754_557709909}; username_login_n=15669087700; GanjiLoginType=0; __utma=32156897.1024205804.1528708769.1529023568.1529029837.4; GANJISESSID=shdb8t2vgn99tnkn0ofdcgrihf; sscode=9HsRkf041lVH%2BQf39HWsQh54; GanjiUserName=szfl666; GanjiUserInfo=%7B%22user_id%22%3A557709909%2C%22email%22%3A%22%22%2C%22username%22%3A%22szfl666%22%2C%22user_name%22%3A%22szfl666%22%2C%22nickname%22%3A%22%5Cu5e73%5Cu5b89%5Cu6768%5Cu9752%5Cu9752%22%7D; bizs=%5B3%5D; supercookie=AGH3AmN5BGN5WQtlMTMuAmRkMwNlLmOvLGp0ZTMzLzMyMJWvAJZ0BGH0LmpjMwSuMGR%3D; xxzl_smartid=46229e619fb608c62d39dc189295baf9; last_name=szfl666; ganji_login_act=1529044045164'
    cookies_str_gj = al_qf.get_cook_str('.ganji.com', cookies_basis_gj)
    module_gj_0 = Module_gj(cookies_str_gj)
    logging.error('run gj sucess, to run lp-----1')

    cookies_basis_lp = 'abtest=0; _fecdn_=1; __uuid=1530527233544.45; __tlog=1530527233545.26%7C00000000%7C00000000%7Cs_00_pz0%7Cs_00_pz0; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1530527234; _mscid=s_00_pz0; _uuid=5A88398AFFA848187736D9B9BF2D2CD8; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1530527255; user_name=%E9%83%AD%E5%AD%90%E6%A1%A2; lt_auth=6L5bbCcFxl76tnGKiGpet69N3dOtU27O9H9Y0RFV1oe%2BD%2F3i4PrlQwOErLIDxBIhlkt3JsULNLP%2B%0D%0AMOr5y3VD6UMTwGmnlYCxuuW70XweTedcdvmi0a72kMzZQslxnXEHyHBg8H9Okx31sUAhN9TvnF7I%0D%0Ap6HH7ral8vvE%0D%0A; UniqueKey=d4d47f8153c841621a667e00ad0d9493; user_kind=1; _l_o_L_=e3c9b446218c5b2bd4d47f8153c841621a667e00ad0d9493; login_temp=islogin; _e_ld_auth_=ac23e04875d8628e; b-beta2-config=%7B%22d%22%3A365%2C%22e%22%3A9612079%2C%22ejm%22%3A%221%22%2C%22n%22%3A%22%25E9%2583%25AD%25E5%25AD%2590%25E6%25A1%25A2%22%2C%22audit%22%3A%221%22%2C%22ecomp_id%22%3A9612079%2C%22photo%22%3A%22%2F%2Fimage0.lietou-static.com%2Fimg%2F5afa5b868e50d906233368cf04a.png%22%2C%22version%22%3A%222%22%2C%22hasPhoneNum%22%3A%221%22%2C%22v%22%3A%222%22%2C%22ecreate_time%22%3A%2220180702%22%2C%22p%22%3A%222%22%2C%22entry%22%3A%221%22%2C%22jz%22%3A%220%22%7D; imClientId=3a3ef6be625ffffc4462f629076d8d2a; imId=3a3ef6be625ffffc5da7d3574f2ad402; fe_lpt_jipinByOneGiveTwo=true; fe_lpt_resumeLib=true; fe_lpt_sevenAnniversaryBegin=true; fe_lpt_realname=true; JSESSIONID=24835A675443F7EA7CF7131A3639013B; __session_seq=34; __uv_seq=34'
    cookies_str_lp = al_qf.get_cook_str('.liepin.com', cookies_basis_lp)
    module_lp_0 = Module_lp(cookies_str_lp)
    logging.error('run lp sucess, to run boss-----1')

    cookies_basis_boss = 't=iGi5GHct1hJtEcXs; wt=iGi5GHct1hJtEcXs; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1531788978,1531874497; __c=1531874497; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCwtxAKnPLdPYamZHCAx0xu2z7FldlGtRqlEqZHkU2JxwW_10IbmDQVPG88TAoDGb%26wd%3D%26eqid%3D84749153000331aa000000045b4e8cbb; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1531874825; __a=6342634.1531788976.1531789284.1531874497.18.3.7.18'
    cookies_str_boss = al_qf.get_cook_str('.zhipin.com', cookies_basis_boss)
    module_boss_0 = Module_boss(cookies_str_boss)
    logging.error('run boss sucess, to run lg-----1')

    cookies_basis_lg ='user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
    cookies_str_lg = func_lg.get_cook_str(".lagou.com", cookies_basis_lg)
    logging.error('run lg sucess, to run zhyc-----1')

    cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
    cookies_str_zhyc = func_zhyc.get_cook_str(".chinahr.com", cookies_basis_zhyc)
    logging.error('run zhyc sucess, to run sxs-----1')

    cookies_basis_sxs = '__jsluid=b479516d6fb68b555bdf3b04d4d95aee; sxs_usr="2|1:0|10:1531880807|7:sxs_usr|24:dXNyX3lnbG92OGlhdnh5cg==|2a088019793e0f5181ca05d9c09de6b6511c9b0c35e8f00e1375e684b3f84a67"; userflag=company; SXS_XSESSION_ID="2|1:0|10:1531880807|15:SXS_XSESSION_ID|48:ZjAyNzI0NTYtYTJhYi00YjRlLWFkMGYtZTU1OGU4NzE2OThh|87ab5a1f8555f7dbbbacae30c510c055e7bfc75842456a8f43c4c5befad00ac7"; affefdgx=usr_yglov8iavxyr; SXS_XSESSION_ID_EXP="2|1:0|10:1531880807|19:SXS_XSESSION_ID_EXP|16:MTUzNDQ3MjgwNw==|5f37d54f26f71115fadb8462a3f777c2ea7e600f266699a0f4859f703d2abf75"; MEIQIA_EXTRA_TRACK_ID=17JF0z0rxLHrzun3hmKojCV9fxz; gr_cs1_57cc3437-e85d-4913-9e20-797e6c09a06e=user_id%3Anull; gr_session_id_96145fbb44e87b47_57cc3437-e85d-4913-9e20-797e6c09a06e=true; gr_session_id_96145fbb44e87b47=5d9cca33-8fd2-44e3-808e-792a4ab834e2; Hm_lvt_59802bedd38a5af834100b04592579e2=1531880789,1531905358; Hm_lpvt_59802bedd38a5af834100b04592579e2=1531905358; gr_session_id_96145fbb44e87b47_5d9cca33-8fd2-44e3-808e-792a4ab834e2=true; MEIQIA_VISIT_ID=17YDuEFXd92jqzS7Jak0VQMi5T8; SXS_VISIT_XSESSION_ID_V3.0="2|1:0|10:1531905511|26:SXS_VISIT_XSESSION_ID_V3.0|48:ZjAyNzI0NTYtYTJhYi00YjRlLWFkMGYtZTU1OGU4NzE2OThh|0d4f552f74fe5296028dc0e38f05db60fc3dee6640440954f2a4455ebcc15612"; SXS_VISIT_XSESSION_ID_V3.0_EXP="2|1:0|10:1531905511|30:SXS_VISIT_XSESSION_ID_V3.0_EXP|16:MTUzNDQ5NzUxMQ==|e158607ee0e678f5c72eaf35f30ed79d66771f180643b9133604feab50ca0054"'
    cookies_str_sxs = al_qf.get_cook_str('.shixiseng.com', cookies_basis_sxs)
    module_sxs_0 = Module_sxs(cookies_str_sxs)
    logging.error('run sxs sucess, to run djw-----1')

    cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532135172; login_email=3001261262%40qq.com; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
    cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
    logging.error('run djw sucess')



    login_zl = False
    login_51 = False
    login_58 = False
    login_gj = False
    login_hzrc = False
    login_lp = False
    login_lg = False
    login_zhyc = False
    login_boss = False
    login_sxs = False
    login_djw = False

    tj_zl = []
    tj_51 = []
    tj_58 = []
    tj_gj = []
    tj_hzrc = []
    tj_lp = []
    tj_lg = []
    tj_zhyc = []
    tj_boss = []
    tj_sxs = []
    tj_djw = []


except:
    traceback.print_exc()
    logging.exception("Exception Logged")
    logging.error('run channel llq------fail')


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST')
    ini_st = 0
    logging.error('beg serive')
    # 读取客户端配置文件
    ini_path = os.getcwd() + os.sep + 'Config.ini'
    try:
        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
        conf.read(ini_path, encoding='utf-8')  # 文件路径
        port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
        port = int(port)
        Account = conf.get("PUB_CONF", "PY_ACC")
        org_id = conf.get("PUB_CONF", "PY_COM")
        # orgid = org_id
    except:
        logging.exception("Exception Logged")
        Account = ''
        org_id = ''
    logging.error('Account------' + str(Account))
    logging.error('org_id------' + str(org_id))
    url_to_js = 'http://127.0.0.1:3366/PythonJs?account=' + str(Account)

    global tj_zl
    global tj_51
    global tj_58
    global tj_gj
    global tj_hzrc
    global tj_lp
    global tj_lg
    global tj_zhyc
    global tj_boss
    global tj_sxs
    global tj_djw


    global module_51_0
    mod_51_0 = module_51_0

    global module_58_0
    mod_58_0 = module_58_0

    global module_hzrc_0
    mod_hzrc_0 = module_hzrc_0

    global module_gj_0
    mod_gj_0 = module_gj_0

    global module_lp_0
    mod_lp_0 = module_lp_0

    global module_boss_0
    mod_boss_0 = module_boss_0

    global module_sxs_0
    mod_sxs_0 = module_sxs_0

    global login_zl
    global login_51
    global login_58
    global login_gj
    global login_hzrc
    global login_lp
    global login_lg
    global login_zhyc
    global login_boss
    global login_sxs
    global login_djw

    tjgx_zl = ''
    tjgx_51 = ''
    tjgx_58 = ''
    tjgx_gj = ''
    tjgx_hzrc = ''
    tjgx_lp = ''
    tjgx_lg = ''
    tjgx_zhyc = ''
    tjgx_boss = ''
    tjgx_sxs = ''
    tjgx_djw = ''

    # 初始化时获取登录状态
    logging.error('init get login y/n...')
    login = {}
    login['PythonToJs'] = {}
    login['PythonToJs']['channels'] = []
    for i in range(1, 20):
        # 1智联2前程3同城
        if i == 1:
            zl_log = {}
            try:
                cookies_str_zl_yb = "dywez=95841923.1547435200.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; __utmz=269921210.1547435200.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sts_deviceid=1684a534fea6e-0ab02dcf65084c-424e0b28-1049088-1684a534feb60e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22132309766%22%2C%22%24device_id%22%3A%221684a534fd9da-0274ad56ba18a8-424e0b28-1049088-1684a534fdaa4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221684a534fd9da-0274ad56ba18a8-424e0b28-1049088-1684a534fdaa4%22%7D; NTKF_T2D_CLIENTID=guestFA8CA7AF-9669-9687-5EA4-4A538E9CE327; __utma=269921210.417566423.1547435200.1547454602.1547457867.5; x-zp-client-id=ffe77a3c-7cba-408f-8a18-ae64cb92fbb0; jobRiskWarning=true; dywea=95841923.1607334818358702800.1547435200.1550218963.1560414257.7; dywec=95841923; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; sts_sg=1; sts_sid=16b4ff000a42e6-0d2dfba4dbf9ff-651a107e-1049088-16b4ff000a5404; sts_chnlsid=Unknown; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1560414257; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1560414257; x-zp-device-id=472b20ab14de2a0d36d150b3f3769290; acw_tc=2760822515604142667813253e859845328f8e4c13c8d94c719953532c9356; JsNewlogin=3049230962; JSloginnamecookie=13018956681; JSShowname=""; login-type=b; zp-route-meta=uid=132309766,orgid=35828671; login_point=35828671; promoteGray=; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1560415456173943}; diagnosis=0; zp_src_url=https%3A%2F%2Frd5.zhaopin.com%2Fcustom%2Fsearch; rd_resume_srccode=402101; at=ac370e87e052453fb771eb18e8311287; Token=ac370e87e052453fb771eb18e8311287; rt=a3a3c7c4de7647f79a802de6dcc61387; JSpUserInfo=386b2e69567146655f700469436d5f6a586b4177566f42355975566b266925714a655e700669456d5a6a516b4877506f46355f75556b5b695071326522700869466d5b6a596b4477566f40355e755e6b5869597137651e7044695b6d086a066b1c775e6f23353d75506b5b69507136653b700869406d466a5d6b5177546f493553755f6b5b695071366523700869446d506a3c6b3077586f3a3520755c6b5c695f7146655f700669476d5b6a596b4a77306f243554755c6b516938713e65527005694e6d3e6a396b3f77586f41355a755d6b5b6953714e655a700369436d536a586b4a779; uiioit=37722066596355665567556653645672556654635766576754665e6420722066596354665e670; rd_resume_actionId=1560424893648132309766; dyweb=95841923.70.10.1560414257; sts_evtseq=89"
                cookies_str_zl = zl_xghs.get_cook_str('.zhaopin.com', cookies_str_zl_yb)
                # print(cookies_str_zl)
                login_judge_res = zl_xghs.login_judge_zl(cookies_str_zl)  # 判断是否登陆
                logging.error('zl_login return :' + str(login_judge_res))
                login_zl = True
                zl_log['id'] = 1
                zl_log['isLogin'] = True
                login['PythonToJs']['channels'].append(zl_log)
                # print('已登录')
            except:
                # traceback.print_exc()
                logging.exception("Exception Logged")
                zl_log['id'] = 1
                zl_log['isLogin'] = False
                login['PythonToJs']['channels'].append(zl_log)
                # print('登录不成功')
        elif i == 2:
            qc_log = {}
            try:
                login_51_data = mod_51_0.login_judge_51()
                logging.error('qc_login return :' + str(login_51_data))
                login_51 = True
                qc_log['id'] = 2
                qc_log['isLogin'] = True
                login['PythonToJs']['channels'].append(qc_log)
            except:
                logging.error("51 login fail")
                qc_log['id'] = 2
                qc_log['isLogin'] = False
                login['PythonToJs']['channels'].append(qc_log)
        elif i == 3:
            tc_log = {}
            try:
                login_58_data = mod_58_0.login_judge_58()
                logging.error('tc_login return :' + str(login_58_data))
                if login_58_data:
                    login_58 = True
                    tc_log['id'] = 3
                    tc_log['isLogin'] = True
                    login['PythonToJs']['channels'].append(tc_log)
                else:
                    logging.error("58 login fail")
                    tc_log['id'] = 3
                    tc_log['isLogin'] = False
                    login['PythonToJs']['channels'].append(tc_log)
            except:
                logging.error("58 login fail")
                tc_log['id'] = 3
                tc_log['isLogin'] = False
                login['PythonToJs']['channels'].append(tc_log)
        elif i == 5:
            hzrc_log = {}
            try:
                login_hzrc_data = mod_hzrc_0.login_judge_hzrc()
                logging.error('hzrc_login return can_download_num:' + str(login_hzrc_data))
                login_hzrc = True
                hzrc_log['id'] = 5
                hzrc_log['isLogin'] = True
                login['PythonToJs']['channels'].append(hzrc_log)
            except:
                logging.error("hzrc login fail")
                hzrc_log['id'] = 5
                hzrc_log['isLogin'] = False
                login['PythonToJs']['channels'].append(hzrc_log)
        elif i == 4:
            gj_log = {}
            try:
                login_gj_data = mod_gj_0.login_judge_gj()
                logging.error('gj_login return resumeDownloadCount:' + str(login_gj_data))
                login_51 = True
                gj_log['id'] = 4
                gj_log['isLogin'] = True
                login['PythonToJs']['channels'].append(gj_log)
            except:
                logging.error("gj login fail")
                gj_log['id'] = 4
                gj_log['isLogin'] = False
                login['PythonToJs']['channels'].append(gj_log)
        elif i == 8:
            boss_log = {}
            try:
                login_boss_data = mod_boss_0.login_judge_boss()
                logging.error('boss_login return :' + str(login_boss_data))
                login_boss = True
                boss_log['id'] = 8
                boss_log['isLogin'] = True
                login['PythonToJs']['channels'].append(boss_log)
            except:
                logging.error("boss login fail")
                boss_log['id'] = 8
                boss_log['isLogin'] = False
                login['PythonToJs']['channels'].append(boss_log)
        elif i == 10:
            lp_log = {}
            try:
                login_lp_data = mod_lp_0.login_judge_lp()
                logging.error('lp_login return :' + str(login_lp_data))
                login_lp = True
                lp_log['id'] = 10
                lp_log['isLogin'] = True
                login['PythonToJs']['channels'].append(lp_log)
            except:
                logging.error("lp login fail")
                lp_log['id'] = 10
                lp_log['isLogin'] = False
                login['PythonToJs']['channels'].append(lp_log)
        elif i == 13:
            lg_log = {}
            try:
                cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
                cookies_str_lg = func_lg.get_cook_str("easy.lagou.com", cookies_basis_lg)
                login_lg_data = func_lg.login_judge_lg(cookies_str_lg)  # 判断是否登陆
                logging.error('lg_login return UserConpanyId:' + str(login_lg_data))
                login_lg = True
                lg_log['id'] = 13
                lg_log['isLogin'] = True
                login['PythonToJs']['channels'].append(lg_log)
                # print('已登录')
            except:
                # traceback.print_exc()
                # logging.exception("Exception Logged")
                logging.error('lg_login return :' + str('fail'))
                lg_log['id'] = 13
                lg_log['isLogin'] = False
                login['PythonToJs']['channels'].append(lg_log)
                # print('登录不成功')
        elif i == 6:
            zhyc_log = {}
            try:
                cookies_basis_zhyc ='als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
                cookies_str_zhyc = func_zhyc.get_cook_str(".chinahr.com", cookies_basis_zhyc)
                login_zhyc_data = func_zhyc.login_judge_zhyc(cookies_str_zhyc)  # 判断是否登陆
                logging.error('zhyc_login return is_coin_user:' + str(login_zhyc_data))
                login_zhyc = True
                zhyc_log['id'] = 6
                zhyc_log['isLogin'] = True
                login['PythonToJs']['channels'].append(zhyc_log)
                # print('已登录')
            except:
                # traceback.print_exc()
                # logging.exception("Exception Logged")
                logging.error('zhyc_login return :' + str('fail'))
                zhyc_log['id'] = 6
                zhyc_log['isLogin'] = False
                login['PythonToJs']['channels'].append(zhyc_log)
                # print('登录不成功')
        elif i == 16:
            sxs_log = {}
            try:
                login_sxs_data = mod_sxs_0.login_judge_sxs()
                logging.error('sxs_login return :' + str(login_sxs_data))
                login_sxs = True
                sxs_log['id'] = 16
                sxs_log['isLogin'] = True
                login['PythonToJs']['channels'].append(sxs_log)
            except:
                logging.error("sxs login fail")
                sxs_log['id'] = 16
                sxs_log['isLogin'] = False
                login['PythonToJs']['channels'].append(sxs_log)
        elif i == 7:
            djw_log = {}
            try:
                cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532135172; login_email=3001261262%40qq.com; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
                cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
                login_djw_data = func_djw.login_judge_djw(cookies_str_djw)  # 判断是否登陆
                logging.error('djw_login return te_quan_quan:' + str(login_djw_data))
                login_djw = True
                djw_log['id'] = 7
                djw_log['isLogin'] = True
                login['PythonToJs']['channels'].append(djw_log)
                # print('已登录')
            except:
                # traceback.print_exc()
                logging.error('djw_login return :' + str('fail'))
                # logging.exception("Exception Logged")
                djw_log['id'] = 7
                djw_log['isLogin'] = False
                login['PythonToJs']['channels'].append(djw_log)
                # print('登录不成功')
    login['PythonToJs']['ok'] = True
    login['PythonToJs']['type'] = 'isLogin'
    login['PythonToJs']['timestamp'] = 12345678999
    print(login)
    data = json.dumps(login)
    data = data.encode('utf-8')
    # print(data)
    requests.post(url=url_to_js, data=data)
    logging.error('init get histort_tj ...')
    # 把登陆状态写进配置文件
    try:
        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
        if r'\\' in ini_p:
            ini_p = ini_p.replace(r'\\', '/')
        conf.read(ini_p, encoding='utf-8')  # 文件路径
        for log_stat in login['PythonToJs']['channels']:
            if log_stat['id'] == 1:
                conf.set("config", "login_zl", str(log_stat['isLogin']))
            elif log_stat['id'] == 2:
                conf.set("config", "login_51", str(log_stat['isLogin']))
            elif log_stat['id'] == 3:
                conf.set("config", "login_58", str(log_stat['isLogin']))
            elif log_stat['id'] == 4:
                conf.set("config", "login_gj", str(log_stat['isLogin']))
            elif log_stat['id'] == 5:
                conf.set("config", "login_hzrc", str(log_stat['isLogin']))
            elif log_stat['id'] == 8:
                conf.set("config", "login_boss", str(log_stat['isLogin']))
            elif log_stat['id'] == 10:
                conf.set("config", "login_lp", str(log_stat['isLogin']))
            elif log_stat['id'] == 13:
                conf.set("config", "login_lg", str(log_stat['isLogin']))
            elif log_stat['id'] == 6:
                conf.set("config", "login_zhyc", str(log_stat['isLogin']))
            elif log_stat['id'] == 16:
                conf.set("config", "login_sxs", str(log_stat['isLogin']))
            elif log_stat['id'] == 7:
                conf.set("config", "login_djw", str(log_stat['isLogin']))
        with open(ini_p, "w") as f:
            conf.write(f)
        # conf.write(open(ini_p, "w"))
    except:
        logging.exception("Exception Logged")
        # traceback.print_exc()
        pass
    # time.sleep(1000)
    # 初始化时获取以往搜索条件
    wu_tiaojian = {}
    # wu_tiaojian['orgId'] = '00000'
    wu_tiaojian['orgId'] = org_id
    # 搜索条件后---已获得登录状态的自动爬取
    # wu_tiaojian['channelType'] = 1
    data = json.dumps(wu_tiaojian)
    data = data.encode('utf-8')
    # resp_page = requests.post(url=wu_url_init, data=data)
    # print(resp_page.text)
    # with open('Mod_Pyth/pyth/ini_tj.txt', 'w+') as f_ini:
    #     f_ini.write(resp_page.text)
    # logging.error('writed tj ...')
    # 推荐方案列表，队列从列表中获取数据，没有就挂起等待
    # 同渠道有新的方案时，暂停旧的，执行新的
    # POST方式
    logging.error('run Scpy...')
    dir_Mc = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'Mod_Scpy.exe'
    if r'\\' in dir_Mc:
        dir_Mc = dir_Mc.replace(r'\\', '/')
    p = subprocess.Popen(dir_Mc, shell=True)
    active_raise_error_all = 0
    def do_POST(self):
        global active_raise_error_all
        global tj_zl
        global tj_51
        global tj_58
        global tj_gj
        global tj_hzrc
        global tj_lp
        global tj_lg
        global tj_zhyc
        global tj_boss
        global tj_sxs
        global tj_djw

        global login_zl
        global login_51
        global login_58
        global login_gj
        global login_hzrc
        global login_lp
        global login_lg
        global login_zhyc
        global login_boss
        global login_sxs
        global login_djw

        global module_51_0
        mod_51_0 = module_51_0

        global module_58_0
        mod_58_0 = module_58_0

        global module_hzrc_0
        mod_hzrc_0 = module_hzrc_0

        global module_gj_0
        mod_gj_0 = module_gj_0

        global module_lp_0
        mod_lp_0 = module_lp_0

        global module_boss_0
        mod_boss_0 = module_boss_0

        global module_sxs_0
        mod_sxs_0 = module_sxs_0

        org_id = testHTTPServer_RequestHandler.org_id
        # org_id = '111'
        Account = testHTTPServer_RequestHandler.Account
        # Account = 'test1'
        url_to_js = 'http://*****/PythonJs?account=' + str(Account)
        # url_to_me = 'http://*****'
        # print(url_to_js)
        # print(org_id)
        # print(Account)
        tjpd = 0
        # 接收返回模块
        try:
            # 类方法中调用类变量
            self.send_response(200, message=None)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # print(self.request)
            mpath, margs = splitquery(self.path)
            datas = self.rfile.read(int(self.headers['content-length']))
            # print('原始数据为：', datas)
            try:
                dee = base64.b64decode(datas)
                # print('直接base64解码后：', dee)
                datas = dee.decode('GB2312').encode('utf-8')
            except:
                # logging.exception("Exception Logged")
                pass
                # requests.post(url=url_to_me, data=datas)
            # else:
            #     pass
            try:
                newdata = json.loads(datas.decode('utf-8'))
                # print(newdata)
                newdata = json.loads(newdata)
                logging.error('getdata：' + str(newdata))
                # print(222222, newdata)
            except:
                # logging.exception("Exception Logged")
                newdata = json.loads(datas.decode('utf-8'))
                logging.error('getdata：' + str(newdata))
                # print(3333333, newdata)
            # 问号后的参数名name_json
            name_json = mpath.split('/')[1]
            # print(name_json)
            # print(type(name_json))
            # print(mpath)
            # print(margs)
            # print(datas)
            # print(type(datas))
            # 打印出post传递过来的参数
            # 将字符串转换为字典

            # print(type(newdata))
            if name_json == 'JsPython':
                for key in newdata.keys():
                    if key == 'ClientToPython':
                        try:
                            resp = {}
                            resp['ClientToPython'] = {}
                            resp['ClientToPython']['result'] = '0'
                            resp['ClientToPython']['desc'] = '正确'
                            data = json.dumps(resp)
                            res = data.encode('utf-8')
                            logging.error(str(resp))
                            if str(type(res)) == "<class 'bytes'>":
                                self.wfile.write(res)
                            else:
                                self.wfile.write(res.encode())
                            # print(key)
                            testHTTPServer_RequestHandler.org_id = newdata['ClientToPython']['LoginInit']['CompID']
                            testHTTPServer_RequestHandler.Account = newdata['ClientToPython']['LoginInit']['Account']
                        except:
                            logging.exception("Exception Logged")
                            logging.error('Client_fail')
                            pass
                    # elif key == 'JsToPython':
                    #     resp = {}
                    #     resp['JsToPython'] = {}
                    #     resp['JsToPython']['result'] = '0'
                    #     resp['JsToPython']['desc'] = '正确'
                    #     data = json.dumps(resp)
                    #     res = data.encode('utf-8')
                    #     if str(type(res)) == "<class 'bytes'>":
                    #         self.wfile.write(res)
                    #     else:
                    #         self.wfile.write(res.encode())
            else:
                pass
            # 处理、请求模块
            # 是否登录----老
            try:
                if newdata['JsToPython']['type'] == 'isLogin_auto':
                    login = {}
                    login['PythonToJs'] = {}
                    login['PythonToJs']['channels'] = []
                    logging.error('isLogin beg')
                    try:
                        for i in newdata['JsToPython']['channels']:
                            i = int(i)
                            # 1智联2前程3同城4赶集5杭州人才
                            if i == 1:
                                logging.error('isLogin beg 1...')
                                global login_zl
                                global cookies_str_zl
                                zl_log = {}
                                try:
                                    cookies_str_zl_yb = "JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976"
                                    cookies_str_zl = zl_xghs.get_cook_str('.zhaopin.com', cookies_str_zl_yb)
                                    zl_meta = list(zl_xghs.login_judge_zl(cookies_str_zl))[0]
                                    # print("验证登录成功")
                                    zl_log['id'] = 1
                                    login_zl = True
                                    zl_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(zl_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_zl", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                    pass
                                except:
                                    logging.exception("Exception Logged")
                                    login_zl = False
                                    # dri_zl_0.quit()
                                    zl_log['id'] = 1
                                    zl_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(zl_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_zl", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 2:
                                logging.error('isLogin beg 2...')
                                global login_51
                                qc_log = {}
                                try:
                                    cookies_str_51 = al_qf.get_cook_str('ehire.51job.com', cookies_basis_51)
                                    module_51_0 = Module_51(cookies_str_51)
                                    mod_51_0 = module_51_0
                                    mod_51_0.login_judge_51()
                                    qc_log['id'] = 2
                                    login_51 = True
                                    qc_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(qc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_51", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                                except:
                                    logging.error("51 login fail")
                                    login_51 = False
                                    qc_log['id'] = 2
                                    qc_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(qc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_51", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 3:
                                logging.error('isLogin beg 3...')
                                global login_58
                                tc_log = {}
                                try:
                                    cookies_str_58 = al_qf.get_cook_str('.58.com', cookies_basis_58)
                                    module_58_0 = Module_58(cookies_str_58)
                                    mod_58_0 = module_58_0
                                    new_login_58_data = mod_58_0.login_judge_58()
                                    if new_login_58_data:
                                        login_58 = True
                                        tc_log['id'] = 3
                                        tc_log['isLogin'] = True
                                        login['PythonToJs']['channels'].append(tc_log)
                                        try:
                                            conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                            ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                            if r'\\' in ini_p:
                                                ini_p = ini_p.replace(r'\\', '/')
                                            conf.read(ini_p, encoding='utf-8')  # 文件路径
                                            conf.set("config", "login_58", 'True')
                                            with open(ini_p, "w") as f:
                                                conf.write(f)
                                            # conf.write(open(ini_p, "w"))
                                        except:
                                            logging.exception("Exception Logged")
                                            pass
                                    else:
                                        logging.error("58 login fail")
                                        tc_log['id'] = 3
                                        tc_log['isLogin'] = False
                                        login['PythonToJs']['channels'].append(tc_log)
                                        try:
                                            conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                            ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                            if r'\\' in ini_p:
                                                ini_p = ini_p.replace(r'\\', '/')
                                            conf.read(ini_p, encoding='utf-8')  # 文件路径
                                            conf.set("config", "login_58", 'False')
                                            with open(ini_p, "w") as f:
                                                conf.write(f)
                                            # conf.write(open(ini_p, "w"))
                                        except:
                                            logging.exception("Exception Logged")
                                            pass
                                except:
                                    logging.error("58 login fail")
                                    login_58 = False
                                    tc_log['id'] = 3
                                    tc_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(tc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_58", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 5:
                                logging.error('isLogin beg 5...')
                                global login_hzrc
                                hzrc_log = {}
                                try:
                                    cookies_str_hzrc = al_qf.get_cook_str('.hzrc.com', cookies_basis_hzrc)
                                    module_hzrc_0 = Module_hzrc(cookies_str_hzrc)
                                    mod_hzrc_0 = module_hzrc_0
                                    mod_hzrc_0.login_judge_hzrc()
                                    hzrc_log['id'] = 5
                                    login_hzrc = True
                                    hzrc_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(hzrc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_hzrc", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                                except:
                                    logging.error("hzrc login fail")
                                    login_hzrc = False
                                    hzrc_log['id'] = 5
                                    hzrc_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(hzrc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_hzrc", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 4:
                                logging.error('isLogin beg 4...')
                                global login_gj
                                gj_log = {}
                                try:
                                    cookies_str_gj = al_qf.get_cook_str('.ganji.com', cookies_basis_gj)
                                    module_gj_0 = Module_gj(cookies_str_gj)
                                    mod_gj_0 = module_gj_0
                                    mod_gj_0.login_judge_gj()
                                    gj_log['id'] = 4
                                    login_gj = True
                                    gj_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(gj_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_gj", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                                except:
                                    logging.error("gj login fail")
                                    login_gj = False
                                    gj_log['id'] = 4
                                    gj_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(gj_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_gj", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 8:
                                logging.error('isLogin beg 8...')
                                boss_log = {}
                                try:
                                    cookies_str_boss = al_qf.get_cook_str('.zhipin.com', cookies_basis_boss)
                                    module_boss_0 = Module_boss(cookies_str_boss)
                                    mod_boss_0 = module_boss_0
                                    mod_boss_0.login_judge_boss()
                                    boss_log['id'] = 8
                                    login_boss = True
                                    boss_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(boss_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_boss", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                                except:
                                    logging.error("boss login fail")
                                    login_boss = False
                                    boss_log['id'] = 8
                                    boss_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(boss_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_boss", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 10:
                                logging.error('isLogin beg 10...')
                                global login_lp
                                lp_log = {}
                                try:
                                    cookies_str_lp = al_qf.get_cook_str('.liepin.com', cookies_basis_lp)
                                    module_lp_0 = Module_lp(cookies_str_lp)
                                    mod_lp_0 = module_lp_0
                                    mod_lp_0.login_judge_lp()
                                    lp_log['id'] = 10
                                    login_lp = True
                                    lp_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(lp_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_lp", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                                except:
                                    logging.error("lp login fail")
                                    login_lp = False
                                    lp_log['id'] = 10
                                    lp_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(lp_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_lp", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 13:
                                logging.error('isLogin beg 1...')
                                # global login_lg
                                # global cookies_str_lg
                                lg_log = {}
                                try:
                                    cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
                                    cookies_str_lg = func_lg.get_cook_str("easy.lagou.com", cookies_basis_lg)
                                    login_judge_res = func_lg.login_judge_lg(cookies_str_lg)  # 判断是否登陆
                                    # print("验证登录成功")
                                    lg_log['id'] = 13
                                    login_lg = True
                                    lg_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(lg_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_lg", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                    pass
                                except:
                                    logging.exception("Exception Logged")
                                    login_lg = False
                                    lg_log['id'] = 13
                                    lg_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(lg_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_lg", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 6:
                                logging.error('isLogin beg 1...')
                                # global login_zhyc
                                # global cookies_str_zhyc
                                zhyc_log = {}
                                try:
                                    cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
                                    cookies_str_zhyc = func_zhyc.get_cook_str(".chinahr.com", cookies_basis_zhyc)
                                    login_judge_res = func_zhyc.login_judge_zhyc(cookies_str_zhyc)  # 判断是否登陆
                                    # print("验证登录成功")
                                    zhyc_log['id'] = 6
                                    login_zhyc = True
                                    zhyc_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(zhyc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_zhyc", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                    pass
                                except:
                                    logging.exception("Exception Logged")
                                    login_zhyc = False
                                    zhyc_log['id'] = 6
                                    zhyc_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(zhyc_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_zhyc", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 16:
                                logging.error('isLogin beg 16...')
                                sxs_log = {}
                                try:
                                    cookies_str_sxs = al_qf.get_cook_str('.shixiseng.com', cookies_basis_sxs)
                                    module_sxs_0 = Module_sxs(cookies_str_sxs)
                                    mod_sxs_0 = module_sxs_0
                                    mod_sxs_0.login_judge_sxs()
                                    sxs_log['id'] = 16
                                    login_sxs = True
                                    sxs_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(sxs_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_sxs", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                                except:
                                    logging.error("sxs login fail")
                                    login_sxs = False
                                    sxs_log['id'] = 16
                                    sxs_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(sxs_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_sxs", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                            elif i == 7:
                                logging.error('isLogin beg 1...')
                                # global login_djw
                                # global cookies_str_djw
                                djw_log = {}
                                try:
                                    cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532135172; login_email=3001261262%40qq.com; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
                                    cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
                                    login_judge_res = func_djw.login_judge_djw(cookies_str_djw)  # 判断是否登陆
                                    # print("验证登录成功")
                                    djw_log['id'] = 7
                                    login_djw = True
                                    djw_log['isLogin'] = True
                                    login['PythonToJs']['channels'].append(djw_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_djw", 'True')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                    pass
                                except:
                                    logging.exception("Exception Logged")
                                    login_djw = False
                                    djw_log['id'] = 7
                                    djw_log['isLogin'] = False
                                    login['PythonToJs']['channels'].append(djw_log)
                                    try:
                                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                                        ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
                                        if r'\\' in ini_p:
                                            ini_p = ini_p.replace(r'\\', '/')
                                        conf.read(ini_p, encoding='utf-8')  # 文件路径
                                        conf.set("config", "login_djw", 'False')
                                        with open(ini_p, "w") as f:
                                            conf.write(f)
                                        # conf.write(open(ini_p, "w"))
                                    except:
                                        logging.exception("Exception Logged")
                                        pass
                        login['PythonToJs']['ok'] = True
                        login['PythonToJs']['type'] = 'isLogin'
                        login['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        data = json.dumps(login)
                        data = data.encode('utf-8')
                        print(data)
                        requests.post(url=url_to_js, data=data)
                        logging.error(str(login))
                        logging.error('isLogin sucess...')
                    except:
                        logging.exception("Exception Logged")
                        logging.error('isLogin fail...')
                        # print(info[0], ":", info[1])
            except:
                logging.exception("Exception Logged")
                pass
            # 是否登录
            try:
                if newdata['JsToPython']['type'] == 'isLogin':
                    try:
                        logging.error('get isLogin from config ...')
                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                        ini_p = os.getcwd() + os.sep + 'Mod_Pyth/pyth/conf.ini'
                        conf.read(ini_p, encoding='utf-8')
                        login_zl_st = conf.get("config", "login_zl")
                        login_51_st = conf.get("config", "login_51")
                        login_gj_st = conf.get("config", "login_gj")
                        login_58_st = conf.get("config", "login_58")
                        login_hzrc_st = conf.get("config", "login_hzrc")
                        login_lp_st = conf.get("config", "login_lp")
                        login_lg_st = conf.get("config", "login_lg")
                        login_zhyc_st = conf.get("config", "login_zhyc")
                        login_boss_st = conf.get("config", "login_boss")
                        login_sxs_st = conf.get("config", "login_sxs")
                        login_djw_st = conf.get("config", "login_djw")
                    except:
                        logging.exception("Exception Logged")
                        pass
                    login = {}
                    login['PythonToJs'] = {}
                    login['PythonToJs']['channels'] = []
                    logging.error('isLogin beg')
                    try:
                        for i in newdata['JsToPython']['channels']:
                            i = int(i)
                            # 1智联2前程3同城4赶集5杭州人才
                            if i == 1:
                                zl_log = {}
                                try:
                                    zl_log['id'] = 1
                                    zl_log['isLogin'] = True if login_zl_st == 'True' else False
                                    login['PythonToJs']['channels'].append(zl_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 2:
                                qc_log = {}
                                try:
                                    qc_log['id'] = 2
                                    qc_log['isLogin'] = True if login_51_st == 'True' else False
                                    login['PythonToJs']['channels'].append(qc_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 3:
                                tc_log = {}
                                try:
                                    tc_log['id'] = 3
                                    tc_log['isLogin'] = True if login_58_st == 'True' else False
                                    login['PythonToJs']['channels'].append(tc_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 5:
                                try:
                                    hzrc_log = {}
                                    hzrc_log['id'] = 5
                                    hzrc_log['isLogin'] = True if login_hzrc_st == 'True' else False
                                    login['PythonToJs']['channels'].append(hzrc_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 4:
                                gj_log = {}
                                try:
                                    gj_log['id'] = 4
                                    gj_log['isLogin'] = True if login_gj_st == 'True' else False
                                    login['PythonToJs']['channels'].append(gj_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 8:
                                boss_log = {}
                                try:
                                    boss_log['id'] = 8
                                    boss_log['isLogin'] = True if login_boss_st == 'True' else False
                                    login['PythonToJs']['channels'].append(boss_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 10:
                                lp_log = {}
                                try:
                                    lp_log['id'] = 10
                                    lp_log['isLogin'] = True if login_lp_st == 'True' else False
                                    login['PythonToJs']['channels'].append(lp_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 13:
                                lg_log = {}
                                try:
                                    lg_log['id'] = 13
                                    lg_log['isLogin'] = True if login_lg_st == 'True' else False
                                    login['PythonToJs']['channels'].append(lg_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 6:
                                zhyc_log = {}
                                try:
                                    zhyc_log['id'] = 6
                                    zhyc_log['isLogin'] = True if login_zhyc_st == 'True' else False
                                    login['PythonToJs']['channels'].append(zhyc_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 16:
                                sxs_log = {}
                                try:
                                    sxs_log['id'] = 16
                                    sxs_log['isLogin'] = True if login_sxs_st == 'True' else False
                                    login['PythonToJs']['channels'].append(sxs_log)
                                except:
                                    logging.exception("Exception Logged")
                            elif i == 7:
                                djw_log = {}
                                try:
                                    djw_log['id'] = 7
                                    djw_log['isLogin'] = True if login_djw_st == 'True' else False
                                    login['PythonToJs']['channels'].append(djw_log)
                                except:
                                    logging.exception("Exception Logged")
                        login['PythonToJs']['ok'] = True
                        login['PythonToJs']['type'] = 'isLogin'
                        login['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        data = json.dumps(login)
                        data = data.encode('utf-8')
                        print(data)
                        requests.post(url=url_to_js, data=data)
                        logging.error(str(login))
                        logging.error('isLogin sucess...')
                    except:
                        logging.exception("Exception Logged")
                        logging.error('isLogin fail...')
                        # print(info[0], ":", info[1])
            except:
                logging.exception("Exception Logged")
                pass
            # 剩余刷新次数
            try:
                if newdata['JsToPython']['type'] == 'job_channel_pointer':
                    try:
                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                        ini_p = os.getcwd() + os.sep + 'Mod_Pyth/pyth/conf.ini'
                        conf.read(ini_p, encoding='utf-8')
                        login_zl_st = conf.get("config", "login_zl")
                        login_51_st = conf.get("config", "login_51")
                        login_gj_st = conf.get("config", "login_gj")
                        login_58_st = conf.get("config", "login_58")
                        login_hzrc_st = conf.get("config", "login_hzrc")
                        login_lp_st = conf.get("config", "login_lp")
                        login_lg_st = conf.get("config", "login_lg")
                        login_zhyc_st = conf.get("config", "login_zhyc")
                        login_boss_st = conf.get("config", "login_boss")
                        login_sxs_st = conf.get("config", "login_sxs")
                        login_djw_st = conf.get("config", "login_djw")
                    except:
                        logging.exception("Exception Logged")
                        # traceback.print_exc()
                        pass
                    # print('开始获取')
                    to_js = {}
                    to_js['PythonToJs'] = {}
                    to_js['PythonToJs']['channels'] = []
                    logging.error('job_channel_pointer beg...')
                    try:
                        for i in newdata['JsToPython']['channels']:
                            i = int(i)
                            # 1智联2前程3同城
                            try:
                                if i == 1 and 'True' == login_zl_st:
                                    logging.error('job_channel_pointer beg 1...')
                                    zl_meta = list(zl_xghs.login_judge_zl(cookies_str_zl))[0]
                                    zhi_shua =zl_xghs.get_points(cookies_str_zl, zl_meta)[2]
                                    print(zhi_shua)
                                    zl = {}
                                    zl['point'] = int(zhi_shua)
                                    zl['channelId'] = 1
                                    to_js['PythonToJs']['channels'].append(zl)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 1...')
                                pass
                            try:
                                if i == 2 and 'True' == login_51_st:
                                    logging.error('job_channel_pointer beg 2...')
                                    qc = {}
                                    qc['point'] = -1
                                    qc['channelId'] = 2
                                    to_js['PythonToJs']['channels'].append(qc)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 2...')
                                pass
                            try:
                                if i == 5 and 'True' == login_hzrc_st:
                                    logging.error('job_channel_pointer beg 5...')
                                    hzrc = {}
                                    hzrc['point'] = -1
                                    hzrc['channelId'] = 5
                                    to_js['PythonToJs']['channels'].append(hzrc)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 5...')
                                pass
                            try:
                                if i == 4 and 'True' == login_gj_st:
                                    logging.error('job_channel_pointer beg 4...')
                                    point_0, point_1 = mod_gj_0.refresh_point_gj()
                                    gj = {}
                                    gj['point'] = point_1
                                    gj['channelId'] = 4
                                    to_js['PythonToJs']['channels'].append(gj)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 4...')
                                pass
                            try:
                                if i == 8 and 'True' == login_boss_st:
                                    logging.error('job_channel_pointer beg 8...')
                                    boss = {}
                                    boss['point'] = -1
                                    boss['channelId'] = 8
                                    to_js['PythonToJs']['channels'].append(boss)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 8...')
                                pass
                            try:
                                if i == 10 and 'True' == login_lp_st:
                                    logging.error('job_channel_pointer beg 10...')
                                    lp = {}
                                    lp['point'] = -1
                                    lp['channelId'] = 10
                                    to_js['PythonToJs']['channels'].append(lp)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 10...')
                                pass
                            try:
                                if i == 6 and 'True' == login_zhyc_st:
                                    logging.error('job_channel_pointer beg 6...')
                                    zhyc = {}
                                    zhyc['point'] = -1
                                    zhyc['channelId'] = 6
                                    to_js['PythonToJs']['channels'].append(zhyc)
                                    print(zhyc['point'])
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 6...')
                                pass
                            try:
                                if i == 16 and 'True' == login_sxs_st:
                                    logging.error('job_channel_pointer beg 16...')
                                    point_1 = mod_sxs_0.refresh_point_sxs()
                                    sxs = {}
                                    sxs['point'] = point_1
                                    sxs['channelId'] = 16
                                    to_js['PythonToJs']['channels'].append(sxs)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 16...')
                                pass
                            try:
                                if i == 3 and 'True' == login_58_st:
                                    logging.error('job_channel_pointer beg 16...')
                                    point_58_gjsxd = mod_58_0.login_judge_58()
                                    if point_58_gjsxd:
                                        tc_sxd = {}
                                        tc_sxd['point'] = point_58_gjsxd['gjsxd']
                                        tc_sxd['channelId'] = 3
                                        to_js['PythonToJs']['channels'].append(tc_sxd)
                                    else:
                                        logging.error('job_channel_pointer fail 3...')
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 3...')
                                pass
                            try:
                                if i == 7 and 'True' == login_djw_st:
                                    logging.error('job_channel_pointer beg 7...')
                                    cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532135172; login_email=3001261262%40qq.com; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
                                    cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
                                    zhi_shua =func_djw.zw_shua_xi(cookies_str_djw)
                                    print(zhi_shua)
                                    djw = {}
                                    djw['point'] = int(zhi_shua)
                                    djw['channelId'] = 1
                                    to_js['PythonToJs']['channels'].append(djw)
                            except:
                                # logging.exception("Exception Logged")
                                logging.error('job_channel_pointer fail 7...')
                                pass
                        to_js['PythonToJs']['ok'] = 'true'
                        to_js['PythonToJs']['type'] = 'job_channel_pointer'
                        data = json.dumps(to_js)
                        data = data.encode('utf-8')
                        print(data)
                        requests.post(url=url_to_js, data=data)
                        logging.error(str(to_js))
                        logging.error('job_channel_pointer sucess...')
                    except:
                        logging.exception("Exception Logged")
                        logging.error('job_channel_pointer fail...')
                        # print(info[0], ":", info[1])
            except:
                logging.exception("Exception Logged")
                pass
            # 客户端查询可用下载次数
            try:
                if newdata['JsToPython']['type'] == 'download_confrim':
                    logging.error('download_confrim beg...')
                    try:
                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                        ini_p = os.getcwd() + os.sep + 'Mod_Pyth/pyth/conf.ini'
                        conf.read(ini_p, encoding='utf-8')
                        channel_ini_dic[1] = conf.get("config", "login_zl")
                        channel_ini_dic[2] = conf.get("config", "login_51")
                        channel_ini_dic[4] = conf.get("config", "login_gj")
                        channel_ini_dic[3] = conf.get("config", "login_58")
                        channel_ini_dic[5] = conf.get("config", "login_hzrc")
                        channel_ini_dic[10] = conf.get("config", "login_lp")
                        channel_ini_dic[13] = conf.get("config", "login_lg")
                        channel_ini_dic[6] = conf.get("config", "login_zhyc")
                        channel_ini_dic[8] = conf.get("config", "login_boss")
                        channel_ini_dic[16] = conf.get("config", "login_sxs")
                        channel_ini_dic[7] = conf.get("config", "login_djw")
                    except:
                        logging.exception("Exception Logged")
                        # traceback.print_exc()
                        pass
                    if 'False' == channel_ini_dic[int(newdata['JsToPython']['channelId'])]:
                        active_raise_error_all = 1
                        raise active_raise_Error('channel {} not login'.format(str(newdata['JsToPython']['channelId'])))
                    if newdata['JsToPython']['channelId'] == 1:
                        try:
                            logging.error('download_confrim beg 1...')
                            resp_zl_sj = {}
                            resp_zl_sj['PythonToJs'] = {}
                            resp_zl_sj['PythonToJs']['payType'] = []
                            resp_zl_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_zl_sj['PythonToJs']['channelId'] = 1
                            resp_zl_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_zl_sj['PythonToJs']['type'] = 'download_confrim'
                            #获取total值，判断id是否可搜索出简历
                            zl_judge=zl_xghs.login_judge_zl(cookies_str_zl)
                            zl_meta,zl_com_name = zl_judge[0],zl_judge[1]
                            jl_id = newdata['JsToPython']['resumeId']
                            jl_total = zl_xghs.jx_idcz(cookies_str_zl,zl_meta,zl_com_name,jl_id)
                            num_total,dict_response = jl_total[0],jl_total[1]
                            points=zl_xghs.get_points(cookies_str_zl,zl_meta)
                            xzcs,zlb=points[0],points[1]
                            # print(num_total)
                            if num_total == 1:
                                # 确定下载简历剩余的次数
                                try:
                                    dict_zlxzcs = {}
                                    dict_zlxzcs['type'] = 2
                                    dict_zlxzcs['typeName'] = "剩余下载次数"
                                    dict_zlxzcs['totalCoin'] = xzcs
                                    print(xzcs)
                                    resp_zl_sj['PythonToJs']['payType'].append(dict_zlxzcs)
                                except:
                                    traceback.print_exc()
                                    logging.exception("Exception Logged")
                                    pass
                                # 确定智联币的剩余数量
                                try:
                                    dict_zlb = {}
                                    dict_zlb['type'] = 1
                                    dict_zlb['typeName'] = "剩余智联币"
                                    dict_zlb['totalCoin'] = zlb
                                    print(zlb)
                                    resp_zl_sj['PythonToJs']['payType'].append(dict_zlb)
                                except:
                                    traceback.print_exc()
                                    logging.exception("Exception Logged")
                                    pass
                            else:
                                resp_zl_sj = {}
                                resp_zl_sj['PythonToJs'] = {}
                                resp_zl_sj['PythonToJs']['payType'] = []
                                resp_zl_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                                resp_zl_sj['PythonToJs']['channelId'] = 1
                                resp_zl_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                                resp_zl_sj['PythonToJs']['type'] = 'download_confrim'
                                resp_zl_sj['PythonToJs']['ok'] = False
                                resp_zl_sj['PythonToJs']['msg'] = '没有该ID简历'
                                data = json.dumps(resp_zl_sj)
                                data = data.encode('utf-8')
                                # print(data)
                                requests.post(url=url_to_js, data=data)
                                logging.error('download_confrim fail 1...')
                            resp_zl_sj['PythonToJs']['ok'] = True
                            resp_zl_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_zl_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_zl_sj))
                            logging.error('download_confrim sucess 1...')
                        except:
                            logging.error(str(newdata))
                            traceback.print_exc()
                            logging.exception("Exception Logged")
                    elif newdata['JsToPython']['channelId'] == 2:
                        logging.error('download_confrim beg 2...')
                        resp_51_sj = {}
                        resp_51_sj['PythonToJs'] = {}
                        resp_51_sj['PythonToJs']['payType'] = []
                        resp_51_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_51_sj['PythonToJs']['channelId'] = 2
                        resp_51_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_51_sj['PythonToJs']['type'] = 'download_confrim'
                        try:
                            login_res_51 = mod_51_0.login_judge_51()
                            xzs_51 = login_res_51['resume_num']
                            # print(xzs_51)
                            if xzs_51:
                                dict_51xzcs = {}
                                dict_51xzcs['type'] = 2
                                dict_51xzcs['typeName'] = "剩余下载次数"
                                dict_51xzcs['totalCoin'] = xzs_51
                                resp_51_sj['PythonToJs']['payType'].append(dict_51xzcs)
                            resp_51_sj['PythonToJs']['ok'] = True
                            resp_51_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_51_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_51_sj))
                            logging.error('download_confrim sucess 2...')
                        except:
                            resp_51_sj = {}
                            resp_51_sj['PythonToJs'] = {}
                            resp_51_sj['PythonToJs']['payType'] = []
                            resp_51_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_51_sj['PythonToJs']['channelId'] = 2
                            resp_51_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_51_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_51_sj['PythonToJs']['ok'] = False
                            resp_51_sj['PythonToJs']['msg'] = '获取剩余简历点数失败'
                            data = json.dumps(resp_51_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(newdata))
                            logging.error('download_confrim fail 2...')
                    elif newdata['JsToPython']['channelId'] == 5:
                        logging.error('download_confrim beg 5...')
                        resp_hzrc_sj = {}
                        resp_hzrc_sj['PythonToJs'] = {}
                        resp_hzrc_sj['PythonToJs']['payType'] = []
                        resp_hzrc_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_hzrc_sj['PythonToJs']['channelId'] = 5
                        resp_hzrc_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_hzrc_sj['PythonToJs']['type'] = 'download_confrim'
                        try:
                            xzs_hzrc = mod_hzrc_0.login_judge_hzrc()
                            # print(xzs_hzrc)
                            dict_hzrcxzcs = {}
                            dict_hzrcxzcs['type'] = 2
                            dict_hzrcxzcs['typeName'] = "剩余下载次数"
                            dict_hzrcxzcs['totalCoin'] = xzs_hzrc
                            resp_hzrc_sj['PythonToJs']['payType'].append(dict_hzrcxzcs)
                            resp_hzrc_sj['PythonToJs']['ok'] = True
                            resp_hzrc_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_hzrc_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_hzrc_sj))
                            logging.error('download_confrim sucess 5...')
                        except:
                            # traceback.print_exc()
                            logging.error(str(newdata))
                            resp_hzrc_sj = {}
                            resp_hzrc_sj['PythonToJs'] = {}
                            resp_hzrc_sj['PythonToJs']['payType'] = []
                            resp_hzrc_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_hzrc_sj['PythonToJs']['channelId'] = 5
                            resp_hzrc_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_hzrc_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_hzrc_sj['PythonToJs']['ok'] = False
                            resp_hzrc_sj['PythonToJs']['msg'] = '获取剩余简历点数失败'
                            data = json.dumps(resp_hzrc_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 5...')
                    elif newdata['JsToPython']['channelId'] == 4:
                        logging.error('download_confrim beg 4...')
                        resp_gj_sj = {}
                        resp_gj_sj['PythonToJs'] = {}
                        resp_gj_sj['PythonToJs']['payType'] = []
                        resp_gj_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_gj_sj['PythonToJs']['channelId'] = 4
                        resp_gj_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_gj_sj['PythonToJs']['type'] = 'download_confrim'
                        try:
                            login_res_gj = mod_gj_0.login_judge_gj()
                            xzs_gj = login_res_gj['resume_num']
                            dict_gjxzcs = {}
                            dict_gjxzcs['type'] = 2
                            dict_gjxzcs['typeName'] = "剩余下载次数"
                            dict_gjxzcs['totalCoin'] = xzs_gj
                            resp_gj_sj['PythonToJs']['payType'].append(dict_gjxzcs)
                            resp_gj_sj['PythonToJs']['ok'] = True
                            resp_gj_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_gj_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_gj_sj))
                            logging.error('download_confrim sucess 4...')
                        except:
                            logging.error(str(newdata))
                            resp_gj_sj = {}
                            resp_gj_sj['PythonToJs'] = {}
                            resp_gj_sj['PythonToJs']['payType'] = []
                            resp_gj_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_gj_sj['PythonToJs']['channelId'] = 4
                            resp_gj_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_gj_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_gj_sj['PythonToJs']['ok'] = False
                            resp_gj_sj['PythonToJs']['msg'] = '获取剩余简历点数失败'
                            data = json.dumps(resp_gj_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 4...')
                    elif newdata['JsToPython']['channelId'] == 8:
                        logging.error('download_confrim beg 8...')
                        try:
                            mod_boss_0.login_judge_boss()
                            resp_boss_sj = {}
                            resp_boss_sj['PythonToJs'] = {}
                            resp_boss_sj['PythonToJs']['payType'] = []
                            resp_boss_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_boss_sj['PythonToJs']['channelId'] = 8
                            resp_boss_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_boss_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_boss_sj['PythonToJs']['ok'] = False
                            resp_boss_sj['PythonToJs']['msg'] = '该渠道暂时不提供下载简历功能'
                            data = json.dumps(resp_boss_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('no need download_confrim 8...')
                        except:
                            logging.error(str(newdata))
                            resp_boss_sj = {}
                            resp_boss_sj['PythonToJs'] = {}
                            resp_boss_sj['PythonToJs']['payType'] = []
                            resp_boss_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_boss_sj['PythonToJs']['channelId'] = 8
                            resp_boss_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_boss_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_boss_sj['PythonToJs']['ok'] = False
                            resp_boss_sj['PythonToJs']['msg'] = 'boss直聘登录状态失效'
                            data = json.dumps(resp_boss_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 8...')
                    elif newdata['JsToPython']['channelId'] == 3:
                        logging.error('download_confrim beg 3...')
                        resp_58_sj = {}
                        resp_58_sj['PythonToJs'] = {}
                        resp_58_sj['PythonToJs']['payType'] = []
                        resp_58_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_58_sj['PythonToJs']['channelId'] = 3
                        resp_58_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_58_sj['PythonToJs']['type'] = 'download_confrim'
                        try:
                            cookies_str_58 = al_qf.get_cook_str('.58.com', cookies_basis_58)
                            module_58_0 = Module_58(cookies_str_58)
                            mod_58_0 = module_58_0
                            jlxzd_58 = mod_58_0.login_judge_58()
                            if jlxzd_58:
                                dict_58xzcs_2 = {}
                                dict_58xzcs_2['type'] = 2
                                dict_58xzcs_2['typeName'] = "全国简历点"
                                dict_58xzcs_2['totalCoin'] = jlxzd_58['qgjld']
                                resp_58_sj['PythonToJs']['payType'].append(dict_58xzcs_2)
                                dict_58xzcs_1 = {}
                                dict_58xzcs_1['type'] = 1
                                dict_58xzcs_1['typeName'] = "本地简历点"
                                dict_58xzcs_1['totalCoin'] = jlxzd_58['bdjld']
                                resp_58_sj['PythonToJs']['payType'].append(dict_58xzcs_1)
                                resp_58_sj['PythonToJs']['ok'] = True
                                resp_58_sj['PythonToJs']['msg'] = ''
                                data = json.dumps(resp_58_sj)
                                data = data.encode('utf-8')
                                # print(data)
                                requests.post(url=url_to_js, data=data)
                                logging.error(str(resp_58_sj))
                                logging.error('download_confrim sucess 3...')
                            else:
                                logging.error("58 get dl_point fail")

                        except:
                            logging.error(str(newdata))
                            # traceback.print_exc()
                            resp_58_sj = {}
                            resp_58_sj['PythonToJs'] = {}
                            resp_58_sj['PythonToJs']['payType'] = []
                            resp_58_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_58_sj['PythonToJs']['channelId'] = 3
                            resp_58_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_58_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_58_sj['PythonToJs']['ok'] = False
                            resp_58_sj['PythonToJs']['msg'] = '获取剩余简历点数失败'
                            data = json.dumps(resp_58_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 3...')
                    elif newdata['JsToPython']['channelId'] == 10:
                        logging.error('download_confrim beg 10...')
                        resp_lp_sj = {}
                        resp_lp_sj['PythonToJs'] = {}
                        resp_lp_sj['PythonToJs']['payType'] = []
                        resp_lp_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_lp_sj['PythonToJs']['channelId'] = 10
                        resp_lp_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_lp_sj['PythonToJs']['type'] = 'download_confrim'
                        try:
                            login_res_lp = mod_lp_0.login_judge_lp()
                            try:
                                # xzcs=zl_xghs.jx_xz_cs(cookies_str_zl,zl_meta)
                                xzcs = login_res_lp['CV_DOWNLOAD']
                                dict_lpxzcs = {}
                                dict_lpxzcs['type'] = 2
                                dict_lpxzcs['typeName'] = "剩余下载次数"
                                dict_lpxzcs['totalCoin'] = xzcs
                                # print(xzcs)
                                resp_lp_sj['PythonToJs']['payType'].append(dict_lpxzcs)
                            except:
                                logging.exception("Exception Logged")
                                pass
                            # 确定的剩余数量
                            try:
                                lb = login_res_lp['L_COIN']
                                dict_lb = {}
                                dict_lb['type'] = 1
                                dict_lb['typeName'] = "剩余猎币"
                                dict_lb['totalCoin'] = lb
                                # print(zlb)
                                resp_lp_sj['PythonToJs']['payType'].append(dict_lb)
                            except:
                                logging.exception("Exception Logged")
                                pass

                            resp_lp_sj['PythonToJs']['ok'] = True
                            resp_lp_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_lp_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_lp_sj))
                            logging.error('download_confrim sucess 10...')
                        except:
                            logging.error(str(newdata))
                            resp_lp_sj = {}
                            resp_lp_sj['PythonToJs'] = {}
                            resp_lp_sj['PythonToJs']['payType'] = []
                            resp_lp_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_lp_sj['PythonToJs']['channelId'] = 10
                            resp_lp_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_lp_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_lp_sj['PythonToJs']['ok'] = False
                            resp_lp_sj['PythonToJs']['msg'] = '获取剩余简历点数失败'
                            data = json.dumps(resp_lp_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 10...')
                    elif newdata['JsToPython']['channelId'] == 6:
                        logging.error('download_confrim beg 6...')
                        resp_zhyc_sj = {}
                        resp_zhyc_sj['PythonToJs'] = {}
                        resp_zhyc_sj['PythonToJs']['payType'] = []
                        resp_zhyc_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_zhyc_sj['PythonToJs']['channelId'] = 6
                        resp_zhyc_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_zhyc_sj['PythonToJs']['type'] = 'download_confrim'
                        try:
                            #英才币数量
                            cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
                            cookies_str_zhyc = func_zhyc.get_cook_str(".chinahr.com", cookies_basis_zhyc)
                            xzs_zhyc = func_zhyc.login_judge_zhyc(cookies_str_zhyc)
                            print(xzs_zhyc)
                            dict_zhycxzcs = {}
                            dict_zhycxzcs['type'] = 2
                            dict_zhycxzcs['typeName'] = "英才币数量"
                            dict_zhycxzcs['totalCoin'] = xzs_zhyc
                            resp_zhyc_sj['PythonToJs']['payType'].append(dict_zhycxzcs)

                            #下载点数
                            dict_dz = {}
                            ds=0
                            dict_dz['type'] = 1
                            dict_dz['typeName'] = "下载点数"
                            dict_dz['totalCoin'] = ds
                            resp_zhyc_sj['PythonToJs']['payType'].append(dict_dz)


                            resp_zhyc_sj['PythonToJs']['ok'] = True
                            resp_zhyc_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_zhyc_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_zhyc_sj))
                            logging.error('download_confrim sucess 6...')
                        except:
                            logging.error(str(newdata))
                            resp_zhyc_sj = {}
                            resp_zhyc_sj['PythonToJs'] = {}
                            resp_zhyc_sj['PythonToJs']['payType'] = []
                            resp_zhyc_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_zhyc_sj['PythonToJs']['channelId'] = 6
                            resp_zhyc_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_zhyc_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_zhyc_sj['PythonToJs']['ok'] = False
                            resp_zhyc_sj['PythonToJs']['msg'] = '获取剩余下载点数失败'
                            data = json.dumps(resp_zhyc_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            traceback.print_exc()
                            logging.error('download_confrim fail 6...')
                    elif newdata['JsToPython']['channelId'] == 16:
                        logging.error('download_confrim beg 16...')
                        try:
                            mod_sxs_0.login_judge_sxs()
                            resp_sxs_sj = {}
                            resp_sxs_sj['PythonToJs'] = {}
                            resp_sxs_sj['PythonToJs']['payType'] = []
                            resp_sxs_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_sxs_sj['PythonToJs']['channelId'] = 16
                            resp_sxs_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_sxs_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_sxs_sj['PythonToJs']['ok'] = False
                            resp_sxs_sj['PythonToJs']['msg'] = '该渠道暂时不提供下载简历功能'
                            data = json.dumps(resp_sxs_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('no need download_confrim 16...')
                        except:
                            logging.error(str(newdata))
                            resp_sxs_sj = {}
                            resp_sxs_sj['PythonToJs'] = {}
                            resp_sxs_sj['PythonToJs']['payType'] = []
                            resp_sxs_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_sxs_sj['PythonToJs']['channelId'] = 16
                            resp_sxs_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_sxs_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_sxs_sj['PythonToJs']['ok'] = False
                            resp_sxs_sj['PythonToJs']['msg'] = '实习僧登录状态失效'
                            data = json.dumps(resp_sxs_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 16...')
                    elif newdata['JsToPython']['channelId'] == 13:
                        logging.error('download_confrim beg 13...')
                        try:
                            resp_lg_sj = {}
                            resp_lg_sj['PythonToJs'] = {}
                            resp_lg_sj['PythonToJs']['payType'] = []
                            resp_lg_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_lg_sj['PythonToJs']['channelId'] = 13
                            resp_lg_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_lg_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_lg_sj['PythonToJs']['ok'] = False
                            resp_lg_sj['PythonToJs']['msg'] = '该渠道暂时不提供下载简历功能'
                            data = json.dumps(resp_lg_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('no need download_confrim 13...')
                        except:
                            logging.error(str(newdata))
                            logging.error('download_confrim fail 13...')
                    elif newdata['JsToPython']['channelId'] == 7:
                        try:
                            logging.error('download_confrim beg 7...')
                            resp_djw_sj = {}
                            resp_djw_sj['PythonToJs'] = {}
                            resp_djw_sj['PythonToJs']['payType'] = []
                            resp_djw_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_djw_sj['PythonToJs']['channelId'] = 7

                            resp_djw_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_djw_sj['PythonToJs']['type'] = 'download_confrim'


                            # 确定下载点数剩余数量

                            cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; login_email=3001261262%40qq.com; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532138260; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
                            cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
                            xz_num = func_djw.jl_ds(cookies_str_djw)
                            xzcs = xz_num[0]
                            dict_djwxzcs = {}
                            dict_djwxzcs['type'] = 2
                            dict_djwxzcs['typeName'] = "剩余下载点数"
                            dict_djwxzcs['totalCoin'] = xzcs
                            print(xzcs)
                            resp_djw_sj['PythonToJs']['payType'].append(dict_djwxzcs)
                            # 确定下载劵的剩余数量
                            djwb = xz_num[1]
                            dict_djwb = {}
                            dict_djwb['type'] = 1
                            dict_djwb['typeName'] = "剩余下载劵数"
                            dict_djwb['totalCoin'] = djwb
                            print(djwb)
                            resp_djw_sj['PythonToJs']['payType'].append(dict_djwb)

                            resp_djw_sj['PythonToJs']['ok'] = True
                            resp_djw_sj['PythonToJs']['msg'] = ''
                            data = json.dumps(resp_djw_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error(str(resp_djw_sj))
                            logging.error('download_confrim sucess 7...')
                        except:
                            logging.error(str(newdata))
                            resp_djw_sj = {}
                            resp_djw_sj['PythonToJs'] = {}
                            resp_djw_sj['PythonToJs']['payType'] = []
                            resp_djw_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            resp_djw_sj['PythonToJs']['channelId'] = 7
                            resp_djw_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                            resp_djw_sj['PythonToJs']['type'] = 'download_confrim'
                            resp_djw_sj['PythonToJs']['ok'] = False
                            resp_djw_sj['PythonToJs']['msg'] = '获取'
                            data = json.dumps(resp_djw_sj)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('download_confrim fail 1...')
                            traceback.print_exc()
                            logging.exception("Exception Logged")
            except:
                if active_raise_error_all:
                    login_stat = {}
                    login_stat['PythonToJs'] = {}
                    login_stat['PythonToJs']['payType'] = []
                    login_stat['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                    login_stat['PythonToJs']['channelId'] = newdata['JsToPython']['channelId']
                    login_stat['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                    login_stat['PythonToJs']['type'] = newdata['JsToPython']['type']
                    login_stat['PythonToJs']['ok'] = False
                    login_stat['PythonToJs']['msg'] = '渠道未登录，请登录后刷新状态再进行操作'
                    active_raise_error_all = 0
                    data = json.dumps(login_stat)
                    data = data.encode('utf-8')
                    # print(data)
                    requests.post(url=url_to_js, data=data)
                    logging.error(str(login_stat))
                logging.exception("Exception Logged")
                pass
            # 客户端下载简历
            try:
                if newdata['JsToPython']['type'] == 'download_resume':
                    download_resume_channel = int(newdata['JsToPython']['channelId'])
                    download__orgid = newdata['JsToPython']['orgId']
                    download__resumeid = newdata['JsToPython']['resumeId']
                    logging.error('download_resume beg...')
                    download_dic = {}
                    download_dic['channel'] = download_resume_channel
                    download_dic['orgId'] = download__orgid
                    download_dic['account'] = Account
                    download_dic['channelId'] = download__resumeid
                    download_dic['name'] = ''
                    download_dic['email'] = ''
                    download_dic['phone'] = ''
                    def resp_error_comm(newdata, download_resume_channel, msg):
                        resp_error = {}
                        resp_error['PythonToJs'] = {}
                        resp_error['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_error['PythonToJs']['channelId'] = download_resume_channel
                        resp_error['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_error['PythonToJs']['type'] = 'download_resume'
                        resp_error['PythonToJs']['ok'] = False
                        resp_error['PythonToJs']['msg'] = msg
                        data = json.dumps(resp_error)
                        data = data.encode('utf-8')
                        # print(data)
                        requests.post(url=url_to_js, data=data)

                    try:
                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                        ini_p = os.getcwd() + os.sep + 'Mod_Pyth/pyth/conf.ini'
                        conf.read(ini_p, encoding='utf-8')
                        channel_ini_dic[1] = conf.get("config", "login_zl")
                        channel_ini_dic[2] = conf.get("config", "login_51")
                        channel_ini_dic[4] = conf.get("config", "login_gj")
                        channel_ini_dic[3] = conf.get("config", "login_58")
                        channel_ini_dic[5] = conf.get("config", "login_hzrc")
                        channel_ini_dic[10] = conf.get("config", "login_lp")
                        channel_ini_dic[13] = conf.get("config", "login_lg")
                        channel_ini_dic[6] = conf.get("config", "login_zhyc")
                        channel_ini_dic[8] = conf.get("config", "login_boss")
                        channel_ini_dic[16] = conf.get("config", "login_sxs")
                        channel_ini_dic[7] = conf.get("config", "login_djw")
                    except:
                        logging.exception("Exception Logged")
                        # traceback.print_exc()
                        pass
                    if 'False' == channel_ini_dic[int(newdata['JsToPython']['channelId'])]:
                        active_raise_error_all = 1
                        raise active_raise_Error('channel {} not login'.format(str(newdata['JsToPython']['channelId'])))
                    if download_resume_channel == 1:
                        time_st=time.time()
                        logging.error('download_resume beg 1...')
                        resp_zl_xz = {}
                        resp_zl_xz['PythonToJs'] = {}
                        resp_zl_xz['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_zl_xz['PythonToJs']['channelId'] = 1
                        resp_zl_xz['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_zl_xz['PythonToJs']['type'] = 'download_resume'
                        # 判定ID可否搜索出对应简历
                        try:
                            zl_judge = zl_xghs.login_judge_zl(cookies_str_zl)
                            zl_meta, zl_com_name = zl_judge[0], zl_judge[1]
                            jl_id = newdata['JsToPython']['resumeId']
                            jl_total = zl_xghs.jx_idcz(cookies_str_zl, zl_meta, zl_com_name, jl_id)
                            num_total, dict_response = jl_total[0], jl_total[1]
                            # 模拟点击下载简历
                            if num_total == 1:
                                try:
                                    resp_zl_xz['PythonToJs']['ok'] = True
                                    resp_zl_xz['PythonToJs']['msg'] = ''
                                    pay_type = newdata['JsToPython']['payType']
                                    zl_jl=zl_xghs.jl_xiazai(cookies_str_zl,jl_id,pay_type,dict_response)
                                    print(zl_jl)
                                    try:
                                        resp_zl_xz['PythonToJs']['email'] = zl_jl['info']['email']
                                        download_dic['email'] = zl_jl['info']['email']
                                    except:
                                        pass
                                    try:
                                        resp_zl_xz['PythonToJs']['name'] = zl_jl['info']['name']
                                        download_dic['name'] = zl_jl['info']['name']
                                    except:
                                        pass
                                    try:
                                        resp_zl_xz['PythonToJs']['phone'] = zl_jl['info']['mobilephone']
                                        download_dic['phone'] = zl_jl['info']['mobilephone']
                                    except:
                                        pass
                                    final_send_stat = judge_load_stat(download_dic)

                                    if final_send_stat['stat']:
                                        data_wu = json.dumps(download_dic)
                                        data_wu = data_wu.encode('utf-8')
                                        # print(data_wu)
                                        lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                        logging.error('to_lix:' + str(lix_resp.text))
                                    else:
                                        resp_zl_xz['PythonToJs']['msg'] = "下载点数不足或解析失败"
                                        resp_zl_xz['PythonToJs']['ok'] = False
                                    # 给前端
                                    data = json.dumps(resp_zl_xz)
                                    data = data.encode('utf-8')
                                    # print(data)
                                    requests.post(url=url_to_js, data=data)
                                    time_end=time.time()
                                    print('共计花费时间：',str(time_end-time_st))
                                    logging.error('共计花费时间:{}'.format(str(time_end-time_st)))
                                    logging.error(str(resp_zl_xz))
                                    logging.error('download_resume sucess 1...')
                                except:
                                    traceback.print_exc()
                                    logging.exception("Exception Logged")

                            else:
                                resp_error_comm(newdata, download_resume_channel, '无此简历ID')
                                logging.error('download_resume 1 no jl for this id...')
                        except:
                            resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                            traceback.print_exc()
                            logging.error(str(newdata))
                            logging.exception("Exception Logged")
                    elif download_resume_channel == 2:
                        logging.error('download_resume beg 2...')
                        resp_51_sj = {}
                        resp_51_sj['PythonToJs'] = {}
                        resp_51_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_51_sj['PythonToJs']['channelId'] = 2
                        resp_51_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_51_sj['PythonToJs']['type'] = 'download_resume'
                        try:
                            download_response, details_response = mod_51_0.search_51(newdata['JsToPython']['resumeId'])  # 搜索简历id
                            if download_response and details_response:
                                if '成功下载1份简历' in download_response.text or '简历已在公司人才夹中' in download_response.text:
                                    text_tel = details_response.text
                                    try:
                                        resp_51_sj['PythonToJs']['ok'] = True
                                        resp_51_sj['PythonToJs']['msg'] = ''
                                        jl_51 = dl_51(text_tel)
                                        try:
                                            resp_51_sj['PythonToJs']['name'] = jl_51['info']['name']
                                            download_dic['name'] = jl_51['info']['name']
                                        except:
                                            pass
                                        try:
                                            resp_51_sj['PythonToJs']['email'] = jl_51['info']['email']
                                            download_dic['email'] = jl_51['info']['email']
                                        except:
                                            pass
                                        try:
                                            resp_51_sj['PythonToJs']['phone'] = jl_51['info']['phone']
                                            download_dic['phone'] = jl_51['info']['phone']
                                        except:
                                            pass

                                        final_send_stat = judge_load_stat(download_dic)

                                        if final_send_stat['stat']:
                                            data_wu = json.dumps(download_dic)
                                            data_wu = data_wu.encode('utf-8')
                                            # print(data_wu)
                                            lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                            logging.error('to_lix:' + str(lix_resp.text))
                                        else:
                                            resp_51_sj['PythonToJs']['ok'] = False
                                            resp_51_sj['PythonToJs']['msg'] = "下载点数不足或解析失败"

                                        data = json.dumps(resp_51_sj)
                                        data = data.encode('utf-8')
                                        requests.post(url=url_to_js, data=data)
                                        logging.error(str(data))
                                        logging.error(str(resp_51_sj))
                                        logging.error('download_resume sucess 2...')
                                    except:
                                        logging.exception("Exception Logged")
                                else:
                                    logging.exception("Exception Logged")
                                    logging.error('download_resume 2  this id get fail...')
                                    resp_error_comm(newdata, download_resume_channel, "下载点数不足或解析失败")
                                    logging.error('download_resume fail 2...')
                            else:
                                # logging.error('download_resume 2 not have this id ...')
                                resp_error_comm(newdata, download_resume_channel, '无此简历ID')
                                logging.error('download_resume 2 no jl for this id...')
                        except:
                            resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                            logging.error(str(newdata))
                            logging.exception("Exception Logged")
                    elif download_resume_channel == 5:
                        logging.error('download_resume beg 5...')
                        resp_hzrc_sj = {}
                        resp_hzrc_sj['PythonToJs'] = {}
                        resp_hzrc_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_hzrc_sj['PythonToJs']['channelId'] = 5
                        resp_hzrc_sj['PythonToJs']['type'] = 'download_resume'
                        if '---' in newdata['JsToPython']['resumeId']:
                            try:
                                acc200 = newdata['JsToPython']['resumeId'].split('---')[0]
                                acc210 = newdata['JsToPython']['resumeId'].split('---')[1]
                                hzrc_jl_data = mod_hzrc_0.search_hzrc(org_id, acc200, acc210)
                                # print(11111, hzrc_jl_data)
                                resp_hzrc_sj['PythonToJs']['ok'] = True
                                resp_hzrc_sj['PythonToJs']['msg'] = ''
                                try:
                                    resp_hzrc_sj['PythonToJs']['email'] = hzrc_jl_data['info']['email']
                                    download_dic['email'] = hzrc_jl_data['info']['email']
                                except:
                                    pass
                                try:
                                    resp_hzrc_sj['PythonToJs']['name'] = hzrc_jl_data['info']['name']
                                    download_dic['name'] = hzrc_jl_data['info']['name']
                                except:
                                    pass
                                try:
                                    resp_hzrc_sj['PythonToJs']['phone'] = hzrc_jl_data['info']['mobilephone']
                                    download_dic['phone'] = hzrc_jl_data['info']['mobilephone']
                                except:
                                    pass

                                final_send_stat = judge_load_stat(download_dic)

                                if final_send_stat['stat']:
                                    data_wu = json.dumps(download_dic)
                                    data_wu = data_wu.encode('utf-8')
                                    # print(data_wu)
                                    lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                    logging.error('to_lix:' + str(lix_resp.text))
                                else:
                                    resp_hzrc_sj['PythonToJs']['ok'] = False
                                    resp_hzrc_sj['PythonToJs']['msg'] = '下载点数不足或解析失败'

                                data = json.dumps(resp_hzrc_sj)
                                data = data.encode('utf-8')
                                requests.post(url=url_to_js, data=data)
                                logging.error(str(resp_hzrc_sj))
                                logging.error('download_resume sucess 5...')
                            except:
                                logging.error(str(newdata))
                                logging.exception("Exception Logged")
                                resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                                logging.error('download_resume fail 5...')
                        else:
                            resp_error_comm(newdata, download_resume_channel, '该简历不需下载，或者请联系管理员...')
                            logging.error('download_resume fail 5...')
                    elif download_resume_channel == 4:
                        logging.error('download_resume beg 4...')
                        resp_gj_sj = {}
                        resp_gj_sj['PythonToJs'] = {}
                        resp_gj_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_gj_sj['PythonToJs']['channelId'] = 4
                        resp_gj_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_gj_sj['PythonToJs']['type'] = 'download_resume'
                        try:
                            download_response, details_response = mod_gj_0.search_gj(newdata['JsToPython']['resumeId'])
                            resp_dic = json.loads(details_response)
                            if resp_dic['error'] == 'success':
                                gj_phone = resp_dic['data']['resume_info']['phone']
                                gj_email = resp_dic['data']['resume_info']['email']
                                if gj_phone:
                                    resp_gj_sj['PythonToJs']['phone'] = gj_phone
                                    download_dic['phone'] = gj_phone
                                if gj_email:
                                    resp_gj_sj['PythonToJs']['email'] = gj_email
                                    download_dic['email'] = gj_email
                                resp_gj_sj['PythonToJs']['ok'] = True
                                resp_gj_sj['PythonToJs']['msg'] = ''
                                try:
                                    try:
                                        jl_gj = jljx_gjw(text=download_response, ds=1, org_id=org_id, job_id='', lx=2)
                                    except:
                                        jl_gj = jljx_gjw_jz(text=download_response, ds=1, org_id=org_id, job_id='', lx=2)

                                    if gj_phone:
                                        jl_gj['info']['mobilephone'] = gj_phone
                                        if not download_dic['phone']:
                                            download_dic['phone'] = gj_phone
                                    if gj_email:
                                        jl_gj['info']['email'] = gj_email
                                        if not download_dic['email']:
                                            download_dic['email'] = gj_email
                                    try:
                                        resp_gj_sj['PythonToJs']['name'] = jl_gj['info']['name']
                                        if not download_dic['name']:
                                            download_dic['name'] = jl_gj['info']['name']
                                    except:
                                        pass

                                    final_send_stat = judge_load_stat(download_dic)

                                    if final_send_stat['stat']:
                                        data_wu = json.dumps(download_dic)
                                        data_wu = data_wu.encode('utf-8')
                                        # print(data_wu)
                                        lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                        logging.error('to_lix:' + str(lix_resp.text))
                                    else:
                                        resp_gj_sj['PythonToJs']['ok'] = False
                                        resp_gj_sj['PythonToJs']['msg'] = '下载点数不足或解析失败'

                                    data = json.dumps(resp_gj_sj)
                                    data = data.encode('utf-8')
                                    requests.post(url=url_to_js, data=data)
                                    logging.error(str(resp_gj_sj))
                                    logging.error('download_resume sucess 4...')
                                except:
                                    logging.error(str(newdata))
                                    logging.exception("Exception Logged")
                                    logging.error('download_resume 4  this id get fail...')
                                    resp_error_comm(newdata, download_resume_channel, '赶集网简历下载成功，解析失败')
                            else:
                                logging.error('download_resume 4  this id get fail...')
                                resp_error_comm(newdata, download_resume_channel, '下载点数不足或解析失败')
                                logging.error('download_resume fail 4...')
                        except:
                            traceback.print_exc()
                            logging.exception("Exception Logged")
                            logging.error('download_resume 4  this id get fail...')
                            resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                            logging.error('download_resume fail 4...')
                    elif download_resume_channel == 3:
                        logging.error('download_resume beg 3...')
                        resp_58_sj = {}
                        resp_58_sj['PythonToJs'] = {}
                        resp_58_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_58_sj['PythonToJs']['channelId'] = 3
                        resp_58_sj['PythonToJs']['type'] = 'download_resume'
                        if len(newdata['JsToPython']['resumeId']) > 50:
                            paytype_58 = newdata['JsToPython']['payType']
                            try:
                                jlid_58 = newdata['JsToPython']['resumeId']
                                dl_58_stat, jl_data_58 = mod_58_0.search_58(org_id, jlid_58, paytype_58)
                                print(dl_58_stat, jl_data_58)
                                try:
                                    logging.error(str(dl_58_stat) + str(jl_data_58))
                                except:
                                    pass
                                if dl_58_stat:
                                    resp_58_sj['PythonToJs']['ok'] = True
                                    resp_58_sj['PythonToJs']['msg'] = ''
                                    try:
                                        resp_58_sj['PythonToJs']['name'] = jl_data_58['info']['name']
                                        download_dic['name'] = jl_data_58['info']['name']
                                    except:
                                        pass
                                    try:
                                        resp_58_sj['PythonToJs']['phone'] = jl_data_58['info']['mobilephone']
                                        download_dic['phone'] = jl_data_58['info']['mobilephone']
                                    except:
                                        pass

                                    final_send_stat = judge_load_stat(download_dic)

                                    if final_send_stat['stat']:
                                        data_wu = json.dumps(download_dic)
                                        data_wu = data_wu.encode('utf-8')
                                        # print(data_wu)
                                        lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                        logging.error('to_lix:' + str(lix_resp.text))
                                    else:
                                        resp_58_sj['PythonToJs']['ok'] = False
                                        resp_58_sj['PythonToJs']['msg'] = '下载点数不足或解析失败'

                                    data = json.dumps(resp_58_sj)
                                    data = data.encode('utf-8')
                                    requests.post(url=url_to_js, data=data)
                                    logging.error(str(resp_58_sj))
                                    logging.error('download_resume sucess 3...')
                                elif '已删除' in jl_data_58:
                                    resp_error_comm(newdata, download_resume_channel, '该简历已删除')
                                elif '已' in jl_data_58:
                                    resp_error_comm(newdata, download_resume_channel, '该简历已收到或已下载')
                                elif '无' in jl_data_58:
                                    resp_error_comm(newdata, download_resume_channel, '下载点数不足或解析失败')
                                else:
                                    resp_error_comm(newdata, download_resume_channel, jl_data_58)
                            except:
                                logging.error(str(newdata))
                                logging.exception("Exception Logged")
                                resp_error_comm(newdata, download_resume_channel, '下载过程出现错误，或该简历不存在')
                                logging.error('download_resume fail 3...')
                        else:
                            resp_error_comm(newdata, download_resume_channel, '该简历不需下载，或者请联系管理员...')
                            logging.error('download_resume fail 3...')
                    elif download_resume_channel == 10:
                        logging.error('download_resume beg 10...')
                        resp_lp_sj = {}
                        resp_lp_sj['PythonToJs'] = {}
                        resp_lp_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_lp_sj['PythonToJs']['channelId'] = 10
                        resp_lp_sj['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_lp_sj['PythonToJs']['type'] = 'download_resume'
                        try:
                            if newdata['JsToPython']['payType'] == 2:
                                download_way = 2
                            elif newdata['JsToPython']['payType'] == 1:
                                download_way = 1
                            else:
                                download_way = 0
                            download_response, details_response = mod_lp_0.search_lp(
                                newdata['JsToPython']['resumeId'], download_way)  # 搜索简历id

                            if download_response and details_response:
                                resp_dic = json.loads(download_response.text)
                                if resp_dic['flag'] == 1:
                                    text_tel = details_response.text
                                    sel = Selector(text=text_tel)
                                    try:
                                        phone_and_email = sel.xpath(
                                            '//div[@class="individual-info float-left"]/ul[1]/li[4]/span[2]/em/text()').extract()
                                        phone_and_email = [i for i in phone_and_email if '不公开' not in i]
                                        if len(phone_and_email) == 1:
                                            if '@' in phone_and_email[0]:
                                                resp_lp_sj['PythonToJs']['email'] = phone_and_email[0]
                                                download_dic['email'] = phone_and_email[0]
                                                resp_lp_sj['PythonToJs']['phone'] = ''
                                                download_dic['phone'] = ''
                                            else:
                                                resp_lp_sj['PythonToJs']['phone'] = phone_and_email[0]
                                                download_dic['phone'] = phone_and_email[0]
                                                resp_lp_sj['PythonToJs']['email'] = ''
                                                download_dic['email'] = ''
                                        elif len(phone_and_email) == 2:
                                            resp_lp_sj['PythonToJs']['email'] = phone_and_email[1]
                                            download_dic['email'] = phone_and_email[1]
                                            resp_lp_sj['PythonToJs']['phone'] = phone_and_email[0]
                                            download_dic['phone'] = phone_and_email[0]
                                        else:
                                            resp_lp_sj['PythonToJs']['email'] = ''
                                            download_dic['email'] = ''
                                            resp_lp_sj['PythonToJs']['phone'] = ''
                                            download_dic['phone'] = ''
                                    except:
                                        logging.exception("Exception Logged")
                                        resp_lp_sj['PythonToJs']['email'] = ''
                                        download_dic['email'] = ''
                                        resp_lp_sj['PythonToJs']['phone'] = ''
                                        download_dic['phone'] = ''
                                    try:
                                        jl_lp = jx_lp_ss(text=text_tel, ds=1, org_id=org_id, job_id='', lx=2)
                                        logging.error(jl_lp)
                                        try:
                                            resp_lp_sj['PythonToJs']['name'] = jl_lp['info']['name']
                                            download_dic['name'] = jl_lp['info']['name']
                                        except:
                                            resp_lp_sj['PythonToJs']['name'] = ''
                                            download_dic['name'] = ''
                                            pass
                                        resp_lp_sj['PythonToJs']['ok'] = True
                                        resp_lp_sj['PythonToJs']['msg'] = ''

                                        final_send_stat = judge_load_stat(download_dic)

                                        if final_send_stat['stat']:
                                            data_wu = json.dumps(download_dic)
                                            data_wu = data_wu.encode('utf-8')
                                            # print(data_wu)
                                            lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                            logging.error('to_lix:' + str(lix_resp.text))
                                        else:
                                            resp_lp_sj['PythonToJs']['ok'] = False
                                            resp_lp_sj['PythonToJs']['msg'] = '下载点数不足或解析失败'

                                        data = json.dumps(resp_lp_sj)
                                        data = data.encode('utf-8')
                                        requests.post(url=url_to_js, data=data)
                                        logging.error(str(data))
                                        logging.error(str(resp_lp_sj))
                                        logging.error('download_resume sucess 10...')
                                    except:
                                        logging.exception("Exception Logged")
                                        logging.error('download_resume 10  this id get fail...')
                                        logging.error(text_tel)
                                        resp_error_comm(newdata, download_resume_channel, '猎聘网简历下载成功，解析失败')
                                        logging.error('download_resume fail 10...')
                                else:
                                    sel = Selector(text=details_response.text)
                                    msg = sel.xpath('//section[@class="operating"]/div[1]/text()')
                                    if msg:
                                        msg = msg.extract()[0]
                                    else:
                                        msg = '该猎聘网简历无法下载'
                                    logging.error('download_resume 10 this id get fail...')
                                    resp_error_comm(newdata, download_resume_channel, msg)
                                    logging.error('download_resume fail 10...')
                            else:
                                resp_error_comm(newdata, download_resume_channel, '无此简历ID')
                                logging.error('download_resume 10 no jl for this id...')
                        except:
                            resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                            logging.error(str(newdata))
                            logging.exception("Exception Logged")
                    elif download_resume_channel == 6:
                        logging.error('download_resume beg 6...')
                        resp_zhyc_xz = {}
                        resp_zhyc_xz['PythonToJs'] = {}
                        resp_zhyc_xz['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_zhyc_xz['PythonToJs']['channelId'] = 6
                        resp_zhyc_xz['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_zhyc_xz['PythonToJs']['type'] = 'download_resume'
                        try:
                            jl_id = newdata['JsToPython']['resumeId']
                            cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
                            cookies_str_zhyc = func_zhyc.get_cook_str(".chinahr.com", cookies_basis_zhyc)

                            xzs_zhyc = func_zhyc.login_judge_zhyc(cookies_str_zhyc)
                            print(xzs_zhyc)
                            #模拟点击下载简历
                            if int(xzs_zhyc) > 0:
                                try:
                                    resp_zhyc_xz['PythonToJs']['ok'] = True
                                    resp_zhyc_xz['PythonToJs']['msg'] = ''
                                    sleep(1)
                                    # 解析后的字典
                                    zhyc_jl = func_zhyc.jl_xiazai(cookies_str_zhyc,jl_id,org_id)
                                    # print("消耗下载次数")

                                    try:
                                        resp_zhyc_xz['PythonToJs']['email'] = zhyc_jl['info']['email']
                                        download_dic['email'] = zhyc_jl['info']['email']
                                    except:
                                        pass
                                    try:
                                        resp_zhyc_xz['PythonToJs']['name'] = zhyc_jl['info']['name']
                                        download_dic['name'] = zhyc_jl['info']['name']
                                    except:
                                        pass
                                    try:
                                        resp_zhyc_xz['PythonToJs']['phone'] = zhyc_jl['info']['mobilephone']
                                        download_dic['phone'] = zhyc_jl['info']['mobilephone']
                                    except:
                                        pass

                                    final_send_stat = judge_load_stat(download_dic)

                                    if final_send_stat['stat']:
                                        data_wu = json.dumps(download_dic)
                                        data_wu = data_wu.encode('utf-8')
                                        # print(data_wu)
                                        lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                        logging.error('to_lix:' + str(lix_resp.text))
                                    else:
                                        resp_zhyc_xz['PythonToJs']['ok'] = False
                                        resp_zhyc_xz['PythonToJs']['msg'] = '下载点数不足或解析失败'


                                    data = json.dumps(resp_zhyc_xz)
                                    data = data.encode('utf-8')
                                    requests.post(url=url_to_js, data=data)
                                    logging.error(str(resp_zhyc_xz))
                                    logging.error('download_resume sucess 1...')

                                except:
                                    traceback.print_exc()
                                    logging.exception("Exception Logged")

                            else:
                                resp_error_comm(newdata, download_resume_channel, '下载点数不足或解析失败')
                                logging.error('download_resume 1 no jl for this id...')
                        except:
                            resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                            logging.error(str(newdata))
                            traceback.print_exc()
                            logging.exception("Exception Logged")
                    elif download_resume_channel in [16, 8, 13]:
                        logging.error('download_resume beg 16...')
                        resp_sxs_sj = {}
                        resp_sxs_sj['PythonToJs'] = {}
                        resp_sxs_sj['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_sxs_sj['PythonToJs']['channelId'] = newdata['JsToPython']['timestamp']
                        resp_sxs_sj['PythonToJs']['resumeId'] = int(newdata['JsToPython']['channelId'])
                        resp_sxs_sj['PythonToJs']['type'] = 'download_resume'
                        resp_sxs_sj['PythonToJs']['ok'] = False
                        resp_sxs_sj['PythonToJs']['msg'] = '该渠道暂时不提供下载简历功能'
                        data = json.dumps(resp_sxs_sj)
                        data = data.encode('utf-8')
                        # print(data)
                        requests.post(url=url_to_js, data=data)
                        logging.error('no need download_resume 16...')
                    elif download_resume_channel == 7:
                        logging.error('download_resume beg 7...')
                        resp_djw_xz = {}
                        resp_djw_xz['PythonToJs'] = {}
                        resp_djw_xz['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                        resp_djw_xz['PythonToJs']['channelId'] = 7
                        resp_djw_xz['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                        resp_djw_xz['PythonToJs']['type'] = 'download_resume'
                        # 判定ID可否搜索出对应简历
                        try:
                            cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; login_email=3001261262%40qq.com; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532138260; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
                            cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
                            jl_id = newdata['JsToPython']['resumeId']
                            jl_total = func_djw.jl_idcx(cookies_str_djw, jl_id)

                            # 模拟点击下载简历
                            if jl_total == 1:
                                try:
                                    resp_djw_xz['PythonToJs']['ok'] = True
                                    resp_djw_xz['PythonToJs']['msg'] = ''
                                    pay_type = newdata['JsToPython']['payType']
                                    djw_jl = func_djw.jl_xiazai(cookies_str_djw, jl_id, pay_type)
                                    if 'sorry' in djw_jl:
                                        resp_error_comm(newdata, download_resume_channel, '下载点数不足或解析失败')
                                        logging.error('download_resume 7 no points for this id...')
                                    else:
                                        # 解析后的字典
                                        try:
                                            resp_djw_xz['PythonToJs']['email'] = djw_jl['email']
                                            download_dic['email'] = djw_jl['email']
                                        except:
                                            pass
                                        try:
                                            resp_djw_xz['PythonToJs']['name'] = djw_jl['name']
                                            download_dic['name'] = djw_jl['name']
                                        except:
                                            pass
                                        try:
                                            resp_djw_xz['PythonToJs']['phone'] = djw_jl['mobile']
                                            download_dic['phone'] = djw_jl['mobile']
                                        except:
                                            pass

                                        final_send_stat = judge_load_stat(download_dic)

                                        if final_send_stat['stat']:
                                            data_wu = json.dumps(download_dic)
                                            data_wu = data_wu.encode('utf-8')
                                            # print(data_wu)
                                            lix_resp = requests.post(url=wu_jl_url, data=data_wu)
                                            logging.error('to_lix:' + str(lix_resp.text))
                                        else:
                                            resp_djw_xz['PythonToJs']['ok'] = False
                                            resp_djw_xz['PythonToJs']['msg'] = '下载点数不足或解析失败'

                                        data = json.dumps(resp_djw_xz)
                                        data = data.encode('utf-8')
                                        requests.post(url=url_to_js, data=data)
                                        logging.error(str(resp_djw_xz))
                                        logging.error('download_resume sucess 7...')
                                except:
                                    resp_error_comm(newdata, download_resume_channel, '下载该简历异常')
                                    traceback.print_exc()
                                    logging.exception("Exception Logged")
                            else:
                                resp_error_comm(newdata, download_resume_channel, '无此简历ID')
                                logging.error('download_resume 7 no jl for this id...')
                        except:
                            logging.error(str(newdata))
                            traceback.print_exc()
                            resp_error_comm(newdata, download_resume_channel, '下载简历异常')
                            logging.exception("Exception Logged")
            except:
                if active_raise_error_all:
                    login_stat = {}
                    login_stat['PythonToJs'] = {}
                    login_stat['PythonToJs']['payType'] = []
                    login_stat['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                    login_stat['PythonToJs']['channelId'] = newdata['JsToPython']['channelId']
                    login_stat['PythonToJs']['resumeId'] = newdata['JsToPython']['resumeId']
                    login_stat['PythonToJs']['type'] = newdata['JsToPython']['type']
                    login_stat['PythonToJs']['ok'] = False
                    login_stat['PythonToJs']['msg'] = '渠道未登录，请登录后刷新状态再进行操作'
                    active_raise_error_all = 0
                    data = json.dumps(login_stat)
                    data = data.encode('utf-8')
                    # print(data)
                    requests.post(url=url_to_js, data=data)
                    logging.error(str(login_stat))
                traceback.print_exc()
                logging.exception("Exception Logged")
                pass
            # 刷新职位列表
            try:
                if newdata['JsToPython']['type'] == 'batch_job_sync':
                    logging.error('batch_job_sync beg...')
                    job_sync = {}
                    msg_desc = ''
                    try:
                        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                        ini_p = os.getcwd() + os.sep + 'Mod_Pyth/pyth/conf.ini'
                        conf.read(ini_p, encoding='utf-8')
                        login_zl_st = conf.get("config", "login_zl")
                        login_51_st = conf.get("config", "login_51")
                        login_58_st = conf.get("config", "login_58")
                        login_gj_st = conf.get("config", "login_gj")
                        login_hzrc_st = conf.get("config", "login_hzrc")
                        login_lp_st = conf.get("config", "login_lp")
                        login_sxs_st = conf.get("config", "login_sxs")
                        login_lg_st = conf.get("config", "login_lg")
                        login_zhyc_st = conf.get("config", "login_zhyc")
                        login_boss_st = conf.get("config", "login_boss")
                        login_djw_st = conf.get("config", "login_djw")
                    except:
                        logging.exception("Exception Logged")
                        traceback.print_exc()
                        pass
                    try:
                        sxsb_li = []
                        msg_desc = ''
                        for chan_zw in newdata['JsToPython']['Jobids']:
                            # print('渠道', chan_zw['channelId'])
                            # print('渠道ID', chan_zw['ids'])
                            # 刷新职位-----给定职位列表和是否全选---al=1为全选
                            if int(chan_zw['channelId']) == 1:
                                logging.error('batch_job_sync beg 1...')
                                if 'True' == login_zl_st:
                                    zl_sbzw = {}
                                    zl_sbzw['channelId'] = 1
                                    zl_sbzw['ids'] = []
                                    try:
                                        for JobID in chan_zw['ids']:
                                            try:
                                                zl_meta = list(zl_xghs.login_judge_zl(cookies_str_zl))[0]
                                                zlsx_resp = zl_xghs.zw_shua_xi(cookies_str_zl, zl_meta, JobID)
                                                if '"code":1' in zlsx_resp:
                                                    raise Exception('refresh fail')
                                            except:
                                                traceback.print_exc()
                                                zl_sbzw['ids'].append(JobID)
                                    except:
                                        pass
                                    if zl_sbzw['ids']:
                                        sxsb_li.append(zl_sbzw)
                                        # logging.exception("Exception Logged")
                                        logging.error('batch_job_sync fail 1...')
                                        msg_desc = msg_desc + '智联刷新职位失败   '
                            elif int(chan_zw['channelId']) == 2:
                                logging.error('batch_job_sync beg 2...')
                                if 'True' == login_51_st:
                                # if 'True' == 'True':
                                    qc_sbzw = {}
                                    qc_sbzw['channelId'] = 2
                                    qc_sbzw['ids'] = []
                                    for JobID in chan_zw['ids']:
                                        try:
                                            resp_code = mod_51_0.refresh_job_51(JobID)
                                            if not resp_code:
                                                qc_sbzw['ids'].append(JobID)
                                        except:
                                            logging.exception("Exception Logged")
                                            qc_sbzw['ids'].append(JobID)
                                    if qc_sbzw['ids']:
                                        sxsb_li.append(qc_sbzw)
                                        logging.error('batch_job_sync fail 2...')
                                        msg_desc = msg_desc + '前程无忧刷新职位失败   '
                            elif int(chan_zw['channelId']) == 3:
                                try:
                                    logging.error('batch_job_sync beg 3...')
                                    if 'True' == login_58_st:
                                    # if 'True' == 'True':
                                        tc_sbzw = {}
                                        tc_sbzw['channelId'] = 3
                                        tc_sbzw['ids'] = []
                                        for JobID in chan_zw['ids']:
                                            try:
                                                resp_code = mod_58_0.refresh_job_58(JobID)
                                                if not resp_code:
                                                    tc_sbzw['ids'].append(JobID)
                                            except:
                                                logging.exception("Exception Logged")
                                                tc_sbzw['ids'].append(JobID)
                                                continue
                                        # print(666666, tc_sbzw['ids'])
                                        if tc_sbzw['ids']:
                                            sxsb_li.append(tc_sbzw)
                                            logging.error('batch_job_sync fail 3...')
                                            msg_desc = msg_desc + '58同城刷新职位失败   '
                                except:
                                    traceback.print_exc()
                            elif int(chan_zw['channelId']) == 4:
                                logging.error('batch_job_sync beg 4...')
                                if 'True' == login_gj_st:
                                # if 'True' == 'True':
                                    gj_sbzw = {}
                                    gj_sbzw['channelId'] = 4
                                    gj_sbzw['ids'] = []
                                    for JobID in chan_zw['ids']:
                                        try:
                                            resp_code = mod_gj_0.refresh_job_gj(JobID)
                                            if str(resp_code) != '0':
                                                gj_sbzw['ids'].append(JobID)
                                        except:
                                            traceback.print_exc()
                                            logging.exception("Exception Logged")
                                            gj_sbzw['ids'].append(JobID)
                                    # print('gj_id', gj_sbzw['ids'])
                                    if gj_sbzw['ids']:
                                        # print(666)
                                        sxsb_li.append(gj_sbzw)
                                        logging.error('batch_job_sync fail 4...')
                                        msg_desc = msg_desc + '赶集网刷新职位失败   '
                            elif int(chan_zw['channelId']) == 5:
                                logging.error('batch_job_sync beg 5...')
                                if 'True' == login_hzrc_st:
                                # if 'True' == 'True':
                                    hzrc_sbzw = {}
                                    hzrc_sbzw['channelId'] = 5
                                    hzrc_sbzw['ids'] = []

                                    for JobID in chan_zw['ids']:
                                        try:
                                            mod_hzrc_0.refresh_job_hzrc(JobID)
                                        except:
                                            hzrc_sbzw['ids'].append(JobID)
                                    if hzrc_sbzw['ids']:
                                        sxsb_li.append(hzrc_sbzw)
                                        # logging.exception("Exception Logged")
                                        logging.error('batch_job_sync fail 5...')
                                        msg_desc = msg_desc + '杭州人才网刷新职位失败   '
                            elif int(chan_zw['channelId']) == 10:
                                logging.error('batch_job_sync beg 10...')
                                if 'True' == login_lp_st:
                                # if 'True' == 'True':
                                    lp_sbzw = {}
                                    lp_sbzw['channelId'] = 10
                                    lp_sbzw['ids'] = []
                                    for JobID in chan_zw['ids']:
                                        try:
                                            resp_code = mod_lp_0.refresh_job_lp(JobID)
                                            if resp_code != 1:
                                                lp_sbzw['ids'].append(JobID)
                                        except:
                                            logging.exception("Exception Logged")
                                            lp_sbzw['ids'].append(JobID)
                                    if lp_sbzw['ids']:
                                        sxsb_li.append(lp_sbzw)
                                        logging.error('batch_job_sync fail 10...')
                                        msg_desc = msg_desc + '猎聘网刷新职位失败   '
                            elif int(chan_zw['channelId']) == 6:
                                logging.error('batch_job_sync beg 6...')
                                # if 'True' == login_zhyc_st:
                                if 'True' == 'True':
                                    zhyc_sbzw = {}
                                    zhyc_sbzw['channelId'] = 6
                                    zhyc_sbzw['ids'] = []
                                    try:
                                        for JobID in chan_zw['ids']:
                                            try:
                                                cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
                                                cookies_str_zhyc = func_zhyc.get_cook_str(".chinahr.com",cookies_basis_zhyc)
                                                zhyc_resp = func_zhyc.zw_shua_xi(cookies_str_zhyc,JobID)
                                                if '<title>企业登录-中华英才网</title>' in zhyc_resp:
                                                    raise Exception('zhycw sx fail')
                                            except:
                                                zhyc_sbzw['ids'].append(JobID)
                                    except:
                                        pass
                                    if zhyc_sbzw['ids']:
                                        sxsb_li.append(zhyc_sbzw)
                                        # logging.exception("Exception Logged")
                                        logging.error('batch_job_sync fail 6...')
                                        msg_desc = msg_desc + '中华英才刷新职位失败   '
                            elif int(chan_zw['channelId']) == 16:
                                logging.error('batch_job_sync beg 16...')
                                if 'True' == login_sxs_st:
                                # if 'True' == 'True':
                                    sxs_sbzw = {}
                                    sxs_sbzw['channelId'] = 16
                                    sxs_sbzw['ids'] = []
                                    for JobID in chan_zw['ids']:
                                        try:
                                            resp_code = mod_sxs_0.refresh_job_sxs(JobID)
                                            if not resp_code:
                                                sxs_sbzw['ids'].append(JobID)
                                        except:
                                            logging.exception("Exception Logged")
                                            sxs_sbzw['ids'].append(JobID)
                                    if sxs_sbzw['ids']:
                                        sxsb_li.append(sxs_sbzw)
                                        logging.error('batch_job_sync fail 16...')
                                        msg_desc = msg_desc + '实习僧刷新职位失败   '
                            elif int(chan_zw['channelId']) == 7:
                                logging.error('batch_job_sync beg 7...')
                                if 'True' == login_djw_st:
                                # if 'True' == 'True':
                                    djw_sbzw = {}
                                    djw_sbzw['channelId'] = 7
                                    djw_sbzw['ids'] = []
                                    try:
                                        for JobID in chan_zw['ids']:
                                            try:
                                                cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; login_email=3001261262%40qq.com; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532138260; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
                                                cookies_str_djw = func_djw.get_cook_str(".dajie.com", cookies_basis_djw)
                                                func_djw.zw_sx(cookies_str_djw,JobID)
                                            except:
                                                djw_sbzw['ids'].append(JobID)
                                    except:
                                        pass
                                    if djw_sbzw['ids']:
                                        sxsb_li.append(djw_sbzw)
                                        # logging.exception("Exception Logged")
                                        logging.error('batch_job_sync fail 7...')
                                        msg_desc = msg_desc + '大街网刷新职位失败   '
                            elif int(chan_zw['channelId']) == 8:
                                if 'True' == login_boss_st:
                                # if 'True' == 'True':
                                    boss_sbzw = {}
                                    boss_sbzw['channelId'] = 8
                                    boss_sbzw['ids'] = []
                                    if int(chan_zw['channelId']) == 8:
                                        logging.error('batch_job_sync beg 8...')
                                        sxsb_li.append(boss_sbzw)
                                        logging.error('batch_job_sync fail 8...')
                                        msg_desc = msg_desc + 'boss直聘不提供刷新职位功能   '
                        if not sxsb_li:
                            # print(888888)
                            job_sync['PythonToJs'] = {}
                            job_sync['PythonToJs']['type'] = 'batch_job_sync'
                            job_sync['PythonToJs']['ok'] = True
                            job_sync['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            data = json.dumps(job_sync)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('batch_job_sync all sucess...')
                        else:
                            # print(9999999999)
                            job_sync['PythonToJs'] = {}
                            job_sync['PythonToJs']['type'] = 'batch_job_sync'
                            job_sync['PythonToJs']['ok'] = False
                            job_sync['PythonToJs']['msg'] = msg_desc
                            job_sync['PythonToJs']['fails'] = sxsb_li
                            job_sync['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                            data = json.dumps(job_sync)
                            data = data.encode('utf-8')
                            # print(data)
                            requests.post(url=url_to_js, data=data)
                            logging.error('batch_job_sync have some fail ...')
                    except:
                        # print(1010101010)
                        # logging.exception("Exception Logged")
                        logging.error('batch_job_sync fail...')
                        # print(info[0], ":", info[1])
            except:
                logging.exception("Exception Logged")
                pass
            # 条件查询数据更新
            try:
                if newdata['JsToPython']['type'] == 'channel_upgrade':
                    logging.error('channel_upgrade beg...')
                    # print('00000000000000', newdata)
                    if newdata['JsToPython']['channel'] == 1:
                        tj_zl.append(str(newdata))
                        logging.error('zl tj write in :' + str(newdata))
                        # with open('pyth/new_tj/ini_tj1.txt', 'w+') as f_ini:
                        #     f_ini.write(str(newdata))
                    if newdata['JsToPython']['channel'] == 2:
                        tj_51.append(str(newdata))
                        logging.error('qc tj write in :' + str(newdata))
                        # with open('pyth/new_tj/ini_tj2.txt', 'w+') as f_ini:
                        #     f_ini.write(str(newdata))
                    chan_upg = {}
                    chan_upg['PythonToJs'] = {}
                    chan_upg['PythonToJs']['type'] = 'channel_upgrade'
                    chan_upg['PythonToJs']['ok'] = True
                    chan_upg['PythonToJs']['timestamp'] = newdata['JsToPython']['timestamp']
                    data = json.dumps(chan_upg)
                    data = data.encode('utf-8')
                    # print(data)
                    requests.post(url=url_to_js, data=data)
            except:
                logging.exception("Exception Logged")
                # logging.error('channel_upgrade fail ...')
                pass
            # 获取新设的条件
            try:
                if newdata['JsToPython']['type'] == 'ChannelTj':
                    logging.error('ChannelTj beg...')
                    if newdata['JsToPython']['channel'] == 1:
                        # print('智联有新条件：', tj_zl)
                        data = json.dumps(tj_zl)
                        res = data.encode('utf-8')
                        if str(type(res)) == "<class 'bytes'>":
                            self.wfile.write(res)
                        else:
                            self.wfile.write(res.encode())
                        tj_zl = []
                    if newdata['JsToPython']['channel'] == 2:
                        # print('前程有新条件：', tj_51)
                        data = json.dumps(tj_51)
                        res = data.encode('utf-8')
                        if str(type(res)) == "<class 'bytes'>":
                            self.wfile.write(res)
                        else:
                            self.wfile.write(res.encode())
                        tj_51 = []

            except:
                logging.exception("Exception Logged")
                # logging.error('ChannelTj fail...')
                pass

        except IOError:
            logging.error('waring not possible wrong...')


def run():
    ini_path = os.getcwd() + os.sep + 'Config.ini'
    try:
        conf = configparser.ConfigParser(strict=False, allow_no_value=True)
        conf.read(ini_path, encoding='utf-8')  # 文件路径
        port = conf.get("PUB_CONF", "PY_PORT")  # 获取指定section 的option值
        port = int(port)
    except:
        logging.exception("Exception Logged")
        port = 8900
    logging.error('starting server...')
    # Server settings
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    logging.error('starting server sucess...')
    httpd.serve_forever()
# if __name__ == '__main__':

try:
    run()
except:
    logging.exception("Exception Logged")
    logging.error('run run() fail')


