# -*- coding: utf-8 -*-：


import traceback
from scrapy.selector import Selector
import re
import logging
import requests,datetime
from urllib import request
from urllib import parse
import json
import time
from settings import *
from al_qf import *
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
wu_jl_url = RESUME_DOWNLOAD_URL  # 客户端下载简历
wu_code_url = RESUME_CODES_URL

ini_file = os.getcwd() + os.sep + 'plugin' + os.sep + 'config.ini'
file_cj_dir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep +'Mod_Cj'

resp_code_page = requests.get(url=wu_code_url)
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


class Module_lg(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_lg, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': get_useragent(),
            'Host': '.lagou.com',
        }
    def get_url(self,url):
        if 'https://' not in url:
            url = url.replace('http://', 'https://')
        print('最初url:', url)
        cookies_basis_lg1 = 'WEBTJ-ID=20180829135252-165843de2ad210-090b78647005c-9393265-1296000-165843de2ae138; JSESSIONID=ABAAABAAAGFABEF4A64C4B16FA3F604CC9DA888E4CB2EB1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; TG-TRACK-CODE=index_user; user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644; gate_login_token=698b8e2141e952828d32f2882b133246c5c747cabedc94dc26e6e9780e5022f4'
        cookies_str_lg1 = get_cook_str("www.lagou.com", cookies_basis_lg1)

        cookies_basis_lg2 = 'JSESSIONID=ABAAABAAAGHAABH688B3AE9316DC4CC3E06A0924BEE2640; user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.3.1173048019.1535530109; _gat=1; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; TG-TRACK-CODE=undefined; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; ticketGrantingTicketId=_CAS_TGT_TGT-6fca1068a003410f875b66236d549e01-20180829160849-_CAS_TGT_; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644'
        cookies_str_lg2 = get_cook_str("passport.lagou.com", cookies_basis_lg2)

        cookies_basis_lg3 = 'user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; JSESSIONID=ABAAABAABCBABEH74BEE5676F9A466A1A56B697BC20DAA7; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; _ga=GA1.3.1173048019.1535530109; _gat=1; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644; Hm_lvt_b53988385ecf648a7a8254b14163814d=1535522015,1535527088,1535527152,1535530126; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1535530126; gate_login_token=698b8e2141e952828d32f2882b133246c5c747cabedc94dc26e6e9780e5022f4'
        cookies_str_lg3 = get_cook_str("easy.lagou.com", cookies_basis_lg3)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

        cookie_dic1 = Cookie_str2dict(cookies_str_lg1).merge() if bool(cookies_str_lg1) else dict()
        cookie_jar1 = requests.utils.cookiejar_from_dict(cookie_dic1, cookiejar=None, overwrite=True)

        session1 = requests.Session()
        session1.headers = headers
        session1.cookies = cookie_jar1

        cookie_dic2 = Cookie_str2dict(cookies_str_lg2).merge() if bool(cookies_str_lg2) else dict()
        cookie_jar2 = requests.utils.cookiejar_from_dict(cookie_dic2, cookiejar=None, overwrite=True)

        session2 = requests.Session()
        session2.headers = headers
        session2.cookies = cookie_jar2

        cookie_dic3 = Cookie_str2dict(cookies_str_lg3).merge() if bool(cookies_str_lg3) else dict()
        cookie_jar3 = requests.utils.cookiejar_from_dict(cookie_dic3, cookiejar=None, overwrite=True)

        session3 = requests.Session()
        session3.headers = headers
        session3.cookies = cookie_jar3

        while True:
            if '://www.lagou.com' in url:
                response = session1.get(url=url, allow_redirects=False)
            elif '://passport.lagou.com' in url:
                response = session2.get(url=url, allow_redirects=False)
            elif '://easy.lagou.com' in url:
                response = session3.get(url=url, allow_redirects=False)

            try:
                url = response.headers['Location']
                print(url)
            except:
                break
        return url
    def login_judge_lg(self,cook_str):
        url_login = "https://easy.lagou.com/dashboard/index.htm?from=c_index"
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': get_useragent(),
            'Cookie': cook_str,
            'Host': 'easy.lagou.com',
        }
        login_html = requests.get(url=url_login, headers=headers).text
        # print(login_html)
        conpanyid = login_html.split('id="UserConpanyId" value="')[1].split('"')[0]
        # print(conpanyid)
        return conpanyid

    def get_cj_source_jl(self, jl_id):
        cj_jl_url = 'https://easy.lagou.com/resume/{}.pdfa'.format(jl_id)
        login_html_0 = self.session.get(url=cj_jl_url,headers=self.headers)
        print(login_html_0)

    def get_email_jl(self, eamil_jl_url, org_id='', dt='', Email=''):
        # xx = self.get_url(eamil_jl_url)
        # print(666666, xx)
        # time.sleep(1000)
        try:
            if 'https://' not in eamil_jl_url:
                url = eamil_jl_url.replace('http://', 'https://')

            cookies_basis_lg1 = 'WEBTJ-ID=20180829135252-165843de2ad210-090b78647005c-9393265-1296000-165843de2ae138; JSESSIONID=ABAAABAAAGFABEF4A64C4B16FA3F604CC9DA888E4CB2EB1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; TG-TRACK-CODE=index_user; user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644; gate_login_token=698b8e2141e952828d32f2882b133246c5c747cabedc94dc26e6e9780e5022f4'
            cookies_str_lg1 = get_cook_str("www.lagou.com", cookies_basis_lg1)

            cookies_basis_lg2 = 'JSESSIONID=ABAAABAAAGHAABH688B3AE9316DC4CC3E06A0924BEE2640; user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.3.1173048019.1535530109; _gat=1; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; TG-TRACK-CODE=undefined; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; ticketGrantingTicketId=_CAS_TGT_TGT-6fca1068a003410f875b66236d549e01-20180829160849-_CAS_TGT_; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644'
            cookies_str_lg2 = get_cook_str("passport.lagou.com", cookies_basis_lg2)

            cookies_basis_lg3 = 'user_trace_token=20180829160832-30dcb785-0ae8-4ca5-a050-61a8c0507154; _ga=GA1.2.1173048019.1535530109; _gid=GA1.2.64786880.1535530109; X_HTTP_TOKEN=8fa775ef749ce12a41118ceff9547062; LGSID=20180829160832-b8922cd3-ab62-11e8-b255-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fcan%2Fnew%2Findex.htm%3Fcan%3Dtrue%26stage%3DNEW%26needQueryAmount%3Dtrue; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature%3D0C2F7796B53DF4EE36BD12720529F1DA%26service%3Dhttps%25253A%25252F%25252Feasy.lagou.com%25252Fcan%25252Fnew%25252Findex.htm%25253Fcan%25253Dtrue%252526stage%25253DNEW%252526needQueryAmount%25253Dtrue%26action%3Dlogin%26serviceId%3Daccount%26ts%3D1535530105881; LGUID=20180829160832-b8923178-ab62-11e8-b255-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535530109; LG_LOGIN_USER_ID=9adb411f8e94c87d70baa74c47cf06433a34ce57bbf62a8a6409ebacaa587ffd; _putrc=F3EC4483D6493723123F89F2B170EADC; JSESSIONID=ABAAABAABCBABEH74BEE5676F9A466A1A56B697BC20DAA7; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; mds_login_authToken="E2J3xFuUg0XRZTyiXF21o62E5j3JC1FphFcgvZvoowRXYA6podqGq7yzj1Wz07QEr4ZTx1bqk1iTiR1oVncYu7vA/fQd0njq2ogHFSFC3oYTL218LyzrD5FmxOWon7up2/cHEpiMc+fgcyWWwb9sfzgUjBjVahMPD0BdXDqczuF4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; gray=resume; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%2C%22first_id%22%3A%2216584ba4aa419f-0e3d8c23fe796d-9393265-1296000-16584ba4aa559d%22%7D; _ga=GA1.3.1173048019.1535530109; _gat=1; LGRID=20180829160849-c2c7ebfa-ab62-11e8-b255-5254005c3644; Hm_lvt_b53988385ecf648a7a8254b14163814d=1535522015,1535527088,1535527152,1535530126; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1535530126; gate_login_token=698b8e2141e952828d32f2882b133246c5c747cabedc94dc26e6e9780e5022f4'
            cookies_str_lg3 = get_cook_str("easy.lagou.com", cookies_basis_lg3)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            }

            cookie_dic1 = Cookie_str2dict(cookies_str_lg1).merge() if bool(cookies_str_lg1) else dict()
            cookie_jar1 = requests.utils.cookiejar_from_dict(cookie_dic1, cookiejar=None, overwrite=True)

            session1 = requests.Session()
            session1.headers = headers
            session1.cookies = cookie_jar1

            cookie_dic2 = Cookie_str2dict(cookies_str_lg2).merge() if bool(cookies_str_lg2) else dict()
            cookie_jar2 = requests.utils.cookiejar_from_dict(cookie_dic2, cookiejar=None, overwrite=True)

            session2 = requests.Session()
            session2.headers = headers
            session2.cookies = cookie_jar2

            cookie_dic3 = Cookie_str2dict(cookies_str_lg3).merge() if bool(cookies_str_lg3) else dict()
            cookie_jar3 = requests.utils.cookiejar_from_dict(cookie_dic3, cookiejar=None, overwrite=True)

            session3 = requests.Session()
            session3.headers = headers
            session3.cookies = cookie_jar3

            while True:
                if '://www.lagou.com' in url:
                    response = session1.get(url=url, allow_redirects=False)
                elif '://passport.lagou.com' in url:
                    response = session2.get(url=url, allow_redirects=False)
                elif '://easy.lagou.com' in url:
                    response = session3.get(url=url, allow_redirects=False)

                try:
                    url = response.headers['Location']
                    # print(url)
                except:
                    break

            login_html_0 = response.text
            # dir_url_1 = login_html_0.hea
            # jia = 'https://easy.lagou.com/can/new/details.htm?u=IwEca01TN5A05dM1egQe0y3Dx3'
            # login_html_1 = self.session.get(url=final_url, allow_redirects=True, timeout=6)
            # print(login_html_1.text)
            final_url = response.url
            print(final_url)
            try:
                try:
                    json_url = final_url.split('directRid=')[1]
                    if '&' in json_url:
                        json_url = final_url.split('&')[0]
                except:
                    traceback.print_exc()
                    # time.sleep(1000)
                    return None
                json_url = 'https://easy.lagou.com/resume/order/' + json_url + '.json'
                pattern_data_0 = re.compile(r"window.X_Anti_Forge_Code = '(.*?)';")
                # print(login_html_0)
                text_code = pattern_data_0.search(login_html_0).groups()
                code_str = text_code[0].replace("'", '')
                pattern_data_1 = re.compile(r"window.X_Anti_Forge_Token = '(.*?)';")
                text_token = pattern_data_1.search(login_html_0).groups()
                token_str = text_token[0].replace("'", '')
                new_headers = session3.headers
                new_headers['X-Anit-Forge-Code'] = code_str
                new_headers['X-Anit-Forge-Token'] = token_str
                new_headers['Referer'] = final_url
                # print(json_url)
                # exit()
                login_html_1 = session3.post(url=json_url, headers=new_headers)
                # print(66666666666, new_headers)
                # print(login_html_1.text)
                dict_jl_lg = json.loads(login_html_1.text)
                print(9999, dict_jl_lg)
                if int(dict_jl_lg['state']) == 1:
                    # print(666)
                    dict_jl_lg = dict_jl_lg['content']['data']
                    lg_jl_data = self.jl_jx_email(dict_jl_lg, org_id='', dt='')
                    # try:
                    #     conf = configparser.ConfigParser(strict=False, allow_no_value=True)
                    #     conf.read(ini_file, encoding='utf-8')  # 文件路径
                    #     org_id = conf.get("config", "orgid")
                    # except:
                    #     logging.exception("Exception Logged")
                    try:
                        lg_jl_data['org']['org_id'] = org_id
                        lg_jl_data['info']['plugin_url'] = final_url
                        lg_jl_data['org']['original_email'] = Email
                        # print(final_url)
                        save_channel = lg_jl_data['info']['channel']
                        jl_data_1 = convert_code(lg_jl_data, resp_code_dic, channelid=save_channel)

                        cj_file = file_cj_dir + os.sep + str(int(time.time() * 10000)) + '.txt'
                        with open(cj_file, 'w+', errors='ignore') as f_Cj:
                            f_Cj.write(str(jl_data_1))
                        print('准备获取原始简历')
                    except:
                        logging.exception("Exception Logged")

                    return lg_jl_data
            except:
                traceback.print_exc()
                # time.sleep(1000)
                logging.exception("Exception Logged")
        except:
            traceback.print_exc()
            # time.sleep(1000)
            pass


    def jl_jx_email(self, dict_jl_lg, org_id='', dt=''):
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

# cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
# cookies_str_lg = get_cook_str(".lagou.com", cookies_basis_lg)
# Lg = Module_lg(cookies_str_lg)
#
# url11 = 'http://www.lagou.com/corpResume/resumeView.html?deliverId=1014444365840408576'
# xx = Lg.get_email_jl(url11)
# print(xx)
#判断是否登录，获取指定参数
def login_judge_lg(cook_str):
    url_login="https://easy.lagou.com/dashboard/index.htm?from=c_index"
    headers={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Cache-Control':'max-age=0',
    'User-Agent': get_useragent(),
    'Cookie': cook_str,
    'Host': 'easy.lagou.com',
    }
    login_html=requests.get(url=url_login,headers=headers).text
    # print(login_html)
    conpanyid=login_html.split('id="UserConpanyId" value="')[1].split('"')[0]
    # print(conpanyid)
    return conpanyid


#获取点数
def zw_sx_cs(cook_str):
    url_sx="https://easy.lagou.com/position/batchRefreshInfo.json"
    headers={
    'accept':'*/*',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cook_str,
    'Host': 'easy.lagou.com',
    'Origin': 'https: // easy.lagou.com',
    'Referer': 'https://easy.lagou.com/position/my_online_positions.htm?pageNo=1&citys=&channelTypes=&firstTypes=&keyword=',
    'User-Agent': get_useragent()
    }
    sx_html=requests.post(url=url_sx,headers=headers).text
    print(sx_html)
    dict_sx=json.loads(sx_html)
    freeRefreshNum=dict_sx['content']['data']['freeRefreshNum']
    print(freeRefreshNum)

#职位刷新
def zw_shua_xi(cook_str):
    url_zw_sx="https://easy.lagou.com/parentPosition/multiChannel/statistics.json"
    headers = {
        'accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '49',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cook_str,
        'Host': 'easy.lagou.com',
        'Origin': 'https://easy.lagou.com',
        'Referer': 'https://easy.lagou.com/position/my_online_positions.htm?pageNo=1&citys=&channelTypes=&firstTypes=&keyword=',
        'User-Agent': get_useragent()
    }
    for_data={'needCandidateNum':'true','parentIds':'5131019,5131190'}
    zw_sx_html = requests.post(url=url_zw_sx, headers=headers,data=for_data).text
    print(zw_sx_html)

#获取沟通点数


# #询问函数
# def ask_new(jls, orgid, jobid):
#     flag = True
#     today=str(datetime.date.today())
#     resp_li_all = []
#     now_num = len(jls)
#     # print(now_num)
#     if now_num == 0:
#         flag = False
#     # 余数
#     ys = now_num % 10
#     if ys != 0:
#         cs = int(now_num / 10) + 1
#     else:
#         cs = int(now_num / 10)
#     # print(cs)
#     # 每个页面，询问次数
#     for i in range(1, cs + 1):
#         if i == 1 and flag:
#             pos = []
#             Towu_jl = []
#             jl_d = 1
#             if now_num >= 10:
#                 li_en = jls[0:i * 10]
#             else:
#                 li_en = jls
#             for jl in li_en:
#                 try:
#                     # modifyDate = "20" + jl["modifyDate"]
#                     # if modifyDate == today:
#                     content = {}
#                     content['orgId'] = orgid   # 企业id
#                     content['jobId'] = jobid
#                     content['channel'] = 13
#                     # content['channelUpdateTime'] = td_date
#                     content['channelResumeId'] = jl["id"]
#                     content['downloadStatus'] = 0
#                     content['resumeType'] = 2
#                     Towu_jl.append(content)
#                     # else:
#                     #     flag = False
#                 except:
#                         pos.append(len(Towu_jl))
#                         content = {}
#                         content['orgId'] = orgid
#                         content['jobId'] = '000'
#                         content['channel'] = 1
#                         content['channelUpdateTime'] = '2018-01-01'
#                         content['channelResumeId'] = '111111'
#                         content['downloadStatus'] = 1
#                         content['resumeType'] = 1
#                         Towu_jl.append(content)
#
#             #print(Towu_jl)
#             # 将dict类型的数据转成str
#             data = json.dumps(Towu_jl)
#             data = data.encode('utf-8')
#             resp_page = requests.post(url=wu_jlxw_url, data=data)
#         elif 1 < i < cs and flag:
#             pos = []
#             jl_d = i
#             Towu_jl = []
#             for jl in jls[(i - 1) * 10:i * 10]:
#                 try:
#
#                     # modifyDate = "20" + jl["modifyDate"]
#                     # if modifyDate == today:
#                     content = {}
#                     content['orgId'] = orgid
#                     content['jobId'] = jobid
#                     content['channel'] = 1
# #                     content['channelUpdateTime'] = td_date
#                     content['channelResumeId'] = jl["id"]
#                     content['downloadStatus'] = 0
#                     content['resumeType'] = 2
#                     Towu_jl.append(content)
#                     # else:
#                     #     flag = False
#                 except:
#                     pos.append(len(Towu_jl))
#                     content = {}
#                     content['orgId'] = orgid
#                     content['jobId'] = '000'
#                     content['channel'] = 13
#                     content['channelUpdateTime'] = '2018-01-01'
#                     content['channelResumeId'] = '111111'
#                     content['downloadStatus'] = 1
#                     content['resumeType'] = 1
#                     Towu_jl.append(content)
#                 # print(Towu_jl)
#                 # 将dict类型的数据转成str
#             data = json.dumps(Towu_jl)
#             data = data.encode('utf-8')
#             resp_page = requests.post(url=wu_jlxw_url, data=data)
#         elif i == cs and flag:
#             pos = []
#             jl_d = i
#             Towu_jl = []
#             for jl in jls[(i - 1) * 10:]:
#                 try:
#                     # info_ele = jl.xpath('./td[@class="Common_list_table-id-text"]/span/@id')[0]
#                     # chanl_id = info_ele.split('spanB')[1]
#                     # td_date = jl.xpath('./td[9]/text()')[0]
#                     # modifyDate = "20" + jl["modifyDate"]
# #                     if modifyDate == today:
# #                         content = {}
# #                         content['orgId'] = orgid
# #                         content['jobId'] = jobid
# #                         content['channel'] = 1
# #                         # content['channelUpdateTime'] = today
# #                         content['channelResumeId'] = jl["id"]
# #                         content['downloadStatus'] = 0
# #                         content['resumeType'] = 2
# #                         Towu_jl.append(content)
# #                     else:
# #                         flag = False
# #                 except:
# #                     pos.append(len(Towu_jl))
# #                     content = {}
# #                     content['orgId'] = orgid
# #                     content['jobId'] = '000'
# #                     content['channel'] = 1
# #                     content['channelUpdateTime'] = '2018-01-01'
# #                     content['channelResumeId'] = '111111'
# #                     content['downloadStatus'] = 1
# #                     content['resumeType'] = 1
# #                     Towu_jl.append(content)
# #     #             # print(Towu_jl)
# #     #             # 将dict类型的数据转成str
# #             data = json.dumps(Towu_jl)
# #             data = data.encode('utf-8')
# #             resp_page = requests.post(url=wu_jlxw_url, data=data)
# #         # resp_page = [1]
# #         xd = resp_page.text
# #             # print(xd)
# #             # print(Towu_jl)
# #         xxx = xd.replace(', ', '-').replace(' ', '').replace('[', '').replace(']', '')
# #         resp_li = xxx.split('-')
# #         resp_li_all.extend(resp_li)
# #         # resp_li = ['1', '1', '1']
# #     return resp_li_all
#
#
#
# #根据搜索条件找推荐简历

def jl_tuijian(cook_str):
    flag = True
    page=1
    yxz_num = 0
    while flag:
        try:
            url_ss="https://easy.lagou.com/search/result.json?"
            page_num=str(page)
            headers_ss={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Cookie':'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Faccount.lagou.com%2Fv2%2Faccount%2FmodifyPwd.html; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1530837723603%26serviceId%3Daccount%26service%3Dhttps%25253A%25252F%25252Faccount.lagou.com%25252Fv2%25252Faccount%25252FmodifyPwd.html%26action%3Dlogin%26signature%3D07E438E452F7D7CF5CFDDBDBCF3115A5; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; gate_login_token=ac6b0b8b1f2d9fd654f1c14439f0614d8c1e4c900c2f0469de4912fd5e322fca; JSESSIONID=ABAAABAABEJAAGB4388F421569C236C3321A5587730EB54; mds_login_authToken="JXQGZc3wjskW0rpDmKE21UJDosEEK3JrJ+SHhMenXtYHDFVKGkkaQQiWRk/14ddeqVJGX4uHCkg3lEvxJHI5h50Y7LiUM2663rDKQDS2o21ch8yM/TP9b1TpBAI7n7JYUaFCTf6A0Xo8EcNkyPiXpx33rebW9bXqHA9EVLTIqhh4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; index_location_city=%E6%9D%AD%E5%B7%9E; _gat=1; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1221870295.1530599240; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530750676,1530752513,1530776510,1530789547; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530839164; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1530839169; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530779790,1530783470,1530791548,1530838877; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1530839220; LGSID=20180706084204-66ffe021-80b5-11e8-bee5-525400f775ce; LGRID=20180706090710-e932c4cd-80b8-11e8-98e3-5254005c3644; gray=resume',
                'Host': 'easy.lagou.com',
                'Referer': 'https://easy.lagou.com/search/result.htm?pageNo=1&keyword=%E7%88%AC%E8%99%AB&city=%E4%B8%8A%E6%B5%B7&education=%E6%9C%AC%E7%A7%91%E5%8F%8A%E4%BB%A5%E4%B8%8A&workYear=1%E5%B9%B4-3%E5%B9%B4&expectSalary=10k-15k&industryField=%E9%87%91%E8%9E%8D',
                'User-Agent': get_useragent(),
                # 'X-Anit-Forge-Code': '0',
                # 'X-Anit-Forge-Token': 'None',
                # 'X-Requested-With':'XMLHttpRequest'

            }
            data_ss={
                # 'education':'本科及以上',
                # 'city':'上海',
                'pageNo':page_num,
                'workYear':'1年-3年',
                'keyword':'爬虫',
                # 'expectSalary':'10k-15k',
                # 'industryField':'金融,电商'
            }

            data = parse.urlencode(data_ss).encode('utf-8')
            request_li = request.Request(url=url_ss, headers=headers_ss,data=data)
            reponse_li = request.urlopen(request_li).read()
            json_li_text = reponse_li.decode('utf-8', errors='ignore')
            print(json_li_text)
            dict_result=json.loads(json_li_text)
            result=dict_result['content']['data']['result']['searchResult']['result']
            # print(result)

            # 判断是否存在下一页
            if len(result) == 15:
                print("下一页")
                page = page + 1
            elif len(result) < 15:
                flag = False
                # print("跳出")

            #************************************************************************
            # 询问函数
            # resp_li_all = ask_new(result, orgid, job_id)
            resp_li_all=['0','1','1','0','1','0','1','0','0','0','0','0','0','0','0']
            #************************************************************************
            data_wu_lg = []
            for li_index, resp_li in enumerate(resp_li_all):
                    # print("判断通过")
                for jl_index,dict_jl_xx in enumerate(result):
                    if resp_li == '1' and li_index == jl_index:
                        resumeFetchKey=dict_jl_xx["resumeFetchKey"]
                        url_jl='http://easy.lagou.com/search/resume/fetchResume.htm?resumeFetchKey='+resumeFetchKey
                        headers_jl={
                        'User-Agent': get_useragent(),
                        'Cookie':'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Faccount.lagou.com%2Fv2%2Faccount%2FmodifyPwd.html; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1530837723603%26serviceId%3Daccount%26service%3Dhttps%25253A%25252F%25252Faccount.lagou.com%25252Fv2%25252Faccount%25252FmodifyPwd.html%26action%3Dlogin%26signature%3D07E438E452F7D7CF5CFDDBDBCF3115A5; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; gate_login_token=ac6b0b8b1f2d9fd654f1c14439f0614d8c1e4c900c2f0469de4912fd5e322fca; JSESSIONID=ABAAABAABEJAAGB4388F421569C236C3321A5587730EB54; mds_login_authToken="JXQGZc3wjskW0rpDmKE21UJDosEEK3JrJ+SHhMenXtYHDFVKGkkaQQiWRk/14ddeqVJGX4uHCkg3lEvxJHI5h50Y7LiUM2663rDKQDS2o21ch8yM/TP9b1TpBAI7n7JYUaFCTf6A0Xo8EcNkyPiXpx33rebW9bXqHA9EVLTIqhh4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; index_location_city=%E6%9D%AD%E5%B7%9E; _gat=1; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1221870295.1530599240; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530750676,1530752513,1530776510,1530789547; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530839164; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1530839169; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530779790,1530783470,1530791548,1530838877; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1530839220; LGSID=20180706084204-66ffe021-80b5-11e8-bee5-525400f775ce; LGRID=20180706090710-e932c4cd-80b8-11e8-98e3-5254005c3644; gray=resume',
                        }
                        time.sleep(random.uniform(5, 10))
                        htm_text = requests.get(url=url_jl, headers=headers_jl).text
                        try:
                            lg_data=jl_jx(dict_jl_xx, htm_text)
                            data_wu_lg.append(lg_data)
                            print(lg_data)
                        except:
                            pass
                        if len(data_wu_lg) == 3:
                            data = json.dumps(data_wu_lg)
                            data = data.encode('utf-8')
                            resp_page = requests.post(url=wu_jl_url, data=data)
                            # print('3个了')
                            yxz_num = yxz_num + 3
                            # print(yxz_num)
                            if yxz_num >= 50:
                                # print('够50个了', '**'*100)
                                flag = False
                                return yxz_num
                            data_wu_lg = []

            if len(data_wu_lg) == 3 or len(data_wu_lg) == 0:
                pass
            else:
                yxz_num = len(data_wu_lg) + yxz_num
                data = json.dumps(data_wu_lg)
                data = data.encode('utf-8')
                resp_page = requests.post(url=wu_jl_url, data=data)
                # print('不够我也传了')
        except:
            flag = False
            traceback.print_exc()
            logging.exception("Exception Logged")
            pass

    return yxz_num

#简历解析
def jl_jx(dict_jl,jl_text):
    sel_jx = Selector(text=jl_text)
    # 开始解析
    lg_data = {}
    # 简历主表
    try:
        lg_data['info'] = {}
        lg_data['info']['channel'] = 13
        lg_data['info']['channel_resume_id'] = dict_jl["resumeFetchKey"].strip()
        lg_data['info']['name'] = dict_jl["name"].strip()
        try:
            lg_data['info']['birth_year'] = int(dict_jl["birthday"].split(".")[0].strip())
            lg_data['info']['start_working_year'] = lg_data['info']['birth_year']+int(dict_jl["workYear"].split("年")[0].strip())
        except:
            pass
        lg_data['info']['degree'] = dict_jl["highesteducation"].strip()
        lg_data['info']['sex'] = dict_jl["sex"].strip()
        lg_data['info']['current_address'] = sel_jx.xpath('string(//span[@class="base_info"]/em[@class="mr0 d"])').extract()[0].strip()
    except:
        pass

    # 求职意向
    try:
        lg_data['objective'] = {}
        lg_data['objective']['self_evaluation'] = dict_jl["myRemark"].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("<p>", "").replace("</p>", "")
    except:
        pass
    try:
        salary = dict_jl["expectJob"]["salarys"]   # 薪资要求
        if '保密' in salary or '面议' in salary:
            lg_data['objective']['expected_salary_lower'] = int(0)
            lg_data['objective']['expected_salary_upper'] = int(0)
        elif '-' in salary:
            lg_data['objective']['expected_salary_lower'] = int(salary.replace("k", "").split('-')[0].strip())*1000
            lg_data['objective']['expected_salary_upper'] = int(salary.replace("k", "").split('-')[1].strip())*1000
        elif "以" in salary:
            lg_data['objective']['expected_salary_lower'] = int(salary.replace("k", "").split('以')[0].strip())*1000
            lg_data['objective']['expected_salary_upper'] = int(salary.replace("k", "").split('以')[0].strip())*1000
    except:
        pass
    try:
        lg_data['objective']['expected_address'] = []  # 期望工作地点
        expected_address = dict_jl['expectJob']['city']
        lg_data['objective']['expected_address'].append(expected_address)

        lg_data['objective']['expected_job_title'] = []  # 期望职业
        expected_job_title = dict_jl['expectJob']['positionName'].replace("<em>","").replace("</em>","")
        lg_data['objective']['expected_job_title'].append(expected_job_title)
    except:
        pass
    try:
        lg_data['objective']['job_nature'] = []  # 工作性质
        job_nature = sel_jx.xpath('string(//span[@class="mr_job_type"])').extract()[0].strip()
        lg_data['objective']['job_nature'].append(job_nature)
    except:
        pass

    #求职状态
    try:
        work_status=sel_jx.xpath('string(//li[@class="mr_expect_job_li"]/span)').extract()[0].strip()
        lg_data['objective']['work_status'] = work_status.split(",")[0].replace(" ","")
    except:
        pass

    # 工作经历
    try:
        WorkExperience = dict_jl["workexperiences"]
        if str(WorkExperience) != "[]":
            lg_data['jobs'] = []
            for job_xinxi in WorkExperience[0:]:
                train_dic = {}
                try:
                    train_dic['company'] = job_xinxi["companyname"]  # 公司名称
                    train_dic['job_title'] = job_xinxi["positionname"].replace("<em>","").replace("</em>","") # 职位名称
                    train_dic['during_start'] = job_xinxi["startdate"].replace(".","-").split(" ")[0] + "-01"  # 开始时间
                except:
                    pass
                try:
                    enddate = job_xinxi["enddate"].split(" ")[0]  # 结束时间
                    if enddate == "" or  "至今" in enddate :
                        train_dic['during_end'] = "9999-01-01"
                    else:
                        train_dic['during_end'] = enddate
                except:
                    pass
                try:
                    train_dic['job_content'] = job_xinxi["workcontent"].replace("\r", "").replace("\n","").replace("\t", "").replace("<p>","").replace("</p>", "").replace("<br />", "").replace("<em>","").replace("</em>","").strip()  # 工作内容
                except:
                    pass
                lg_data['jobs'].append(train_dic)

    except:
        pass

    # 项目经历
    try:
        pan_dun=sel_jx.xpath('string(//div[@id="projectExperience"])').extract()[0].strip()
        if pan_dun != "":
            lg_data['projects'] = []
            for pro_in in sel_jx.xpath('//div[@id="projectExperience"]//div[@class="list_show"]/div'):
                pro_dic = {}
                pro_dic['title'] = pro_in.xpath('string(div/div/div/a)').extract()[0].strip() # 项目名称
                pro_dic['description'] = pro_in.xpath('string(div[@class="mr_content_m ueditor_unparse"])').extract()[0].replace("\r", "").replace("\n","").replace("\t", "").strip()  # 项目描述

                date_ti=pro_in.xpath('string(div/div/span)').extract()[0].strip()
                pro_dic['during_start'] = date_ti.split("-")[0].replace(".","-").replace(" ","")+"-01"  # 开始时间
                DateEnd = date_ti.split("-")[1].replace(".","-")+"-01"  # 结束时间
                if "至今" in DateEnd:
                    pro_dic['during_end'] = "9999-01-01"
                else:
                    pro_dic['during_end'] = DateEnd
                lg_data['projects'].append(pro_dic)
    except:
        pass

    # 教育经历
    try:
        EducationExperience = dict_jl["educationexperiences"]
        if str(EducationExperience) != "[]":
            lg_data['educations'] = []
            try:
                for edu_dict_jl in EducationExperience[0:]:
                    edu_dic = {}
                    edu_dic['school'] = edu_dict_jl["schoolname"]  # 学校名称
                    edu_dic['major'] = edu_dict_jl["professional"]  # 专业名称
                    edu_dic['degree'] = edu_dict_jl["education"]  # 学历
                    edu_dic['during_start'] = edu_dict_jl["startdate"].replace(" ","")+"-09-01" # 开始时间
                    DateEnd = edu_dict_jl["enddate"].replace(" ","")+"-06-01"  # 结束时间
                    if DateEnd == "06-01" or "至今" in DateEnd:
                        edu_dic['during_end'] = "9999-01-01"
                    else:
                        edu_dic['during_end'] = DateEnd
                    lg_data['educations'].append(edu_dic)
            except:
                traceback.print_exc()
                pass
    except:
        pass

    # 语言及技能
    try:
        pan_1=sel_jx.xpath('string(//div[@id="skillsAssess"])').extract()[0].strip()
        if pan_1 != "":
            lg_data['languages'] = []
            for langu_in in sel_jx.xpath('//div[@id="skillsAssess"]/div/div[@class="mr_moudle_content"]/div'):
                langu_dic = {}
                langu_dic['skill'] = langu_in.xpath('string(span[@class="mr_skill_name"])').extract()[0].strip()  # 技能名称
                langu_dic['level'] = langu_in.xpath('string(span[@class="mr_skill_level"])').extract()[0].strip()  # 掌握程度
                lg_data['languages'].append(langu_dic)
    except:
        pass

    # # org
    # zl_data['org'] = {}
    # zl_data['org']['resume_type'] = resume_type
    # zl_data['org']['org_id'] = org_id
    # try:
    #     if zl_data['info']['mobilephone']:
    #         zl_data['org']['download_status'] = 1
    # except:
    #     zl_data['org']['download_status'] = 0
    # # 推荐时间
    # zl_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    #
    # # 工作ID
    # try:
    #     if job_id != "":
    #         zl_data['org']['job_id'] = job_id
    # except:
    #     pass
    #     # print(zl_data)

    return lg_data



# cook_yb='user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
#
#
# cook_str=get_cook_str(hostKey=".lagou.com",cook_yb=cook_yb)
#
# print(cook_str)

# login_judge_lg(cook_yb)
