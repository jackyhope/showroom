# -*- coding: utf-8 -*-
# Author: Zhy

'''

获取各大招聘网站的职位信息,接收 网站、城市(到县区)、公司名称信息,
实时爬取所有符合要求的职位信息,清洗后发送给指定接口;
支持的网站有：智联、前程、58、赶集、中华英才、杭州人才、大街、直聘、内推、猎聘、中国人才热线、拉勾、汽车人才、实习僧、脉脉

'''


import requests,datetime
import socket
import random,queue
import json
import shutil
import base64
from lxml import etree
from fontTools.ttLib import TTFont
import traceback
import time
import urllib
from scrapy import Selector

from urllib import parse
from urllib.request import urlopen
import re
import logging
import os
import shutil
import threading
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3
import platform
from config import *
#import getpassgbk
# job_save_url = 'http://192.168.1.9:9021/crawler/saveJob2Lib'
# job_save_url = 'http://192.168.1.111:8080/crawler/saveJob2Lib'
job_save_url = '******'



def xh_pd_re(pos_url,data,headers):
    num=0
    flag = True
    while flag:
        try:
            if num<10:
                num=num+1
                if data == '':
                    job_xq_text = requests.get(url=pos_url,headers=headers,proxies=proxies,timeout=3)
                else:
                    job_xq_text = requests.get(url=pos_url,params=data,headers=headers,proxies=proxies,timeout=3)
                flag = False
                if '页面找不到啦' in job_xq_text:
                    break
                elif job_xq_text == '':
                    pass
                else:
                    return job_xq_text
            else:
                flag = False
        except:
            # traceback.print_exc()
            pass
def xh_pd_req(pos_url,data,headers):
    num=0
    flag = True
    while flag:
        try:
            if num<10:

                if data == '':
                    job_xq_text = requests.get(url=pos_url,headers=headers,timeout=3)
                else:
                    job_xq_text = requests.get(url=pos_url,params=data,headers=headers,timeout=3)

                # print(job_xq_text.status_code)
                # print('----'*50)
                # print(job_xq_text.text)

                if job_xq_text.status_code  == 200:
                    # print('aaaa')
                    return job_xq_text.text
                else:
                    num = num + 1
                    time.sleep(random.uniform(1,1.5))
                    # print('111')
                    continue

            else:
                flag = False
        except:
            # traceback.print_exc()
            pass
def lg_get_cookie(url_sy,url_lg_zw,data):
    num = 0
    flag = True
    while flag:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
            }
            # response = xh_pd_re(pos_url=url_sy,data='',headers=headers)
            response = requests.get(url=url_sy,headers=headers,proxies=proxies)
            # groups = re.search(r'JSESSIONID=(\w+?);.*?SEARCH_ID=(\w+?);', response.headers.get('Set-Cookie')).groups()
            # print(groups)
            # cookie = 'JSESSIONID={}; SEARCH_ID={}'.format(groups[0], groups[1])
            cookie=response.headers.get('Set-Cookie')
            # print('cookie')
            headers_1 = {
                'Cookie': cookie,
                # 'Cookie': 'JSESSIONID=ABAAABAABEEAAJA0C3365A3F055D37B6570746468567221; user_trace_token=20190716092759-f25ae197-a768-11e9-a4e3-5254005c3644; LGUID=20190716092759-f25ae608-a768-11e9-a4e3-5254005c3644; index_location_city=%E6%9D%AD%E5%B7%9E; X_MIDDLE_TOKEN=fcbd320d8579c5594cfa83bc79eaad77; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E7%25BD%2591%25E6%2598%2593%3Fcity%3D%25E6%259D%25AD%25E5%25B7%259E%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_search; SEARCH_ID=bd7b9b76aed7428e832464987a8d644a; X_HTTP_TOKEN=674749d2f5312e5925354236517175606925e727d1; _gid=GA1.2.1305690215.1563240480; _ga=GA1.2.43761467.1563240480; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1563240480; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1563245353; LGSID=20190716104621-e49f06ac-a773-11e9-a4e3-5254005c3644; LGRID=20190716104913-4b46c2b6-a774-11e9-a4e3-5254005c3644',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Content-Length': '49',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Anit-Forge-Token': 'None',
                'X-Requested-With': 'XMLHttpRequest',
                # 'Upgrade-Insecure-Requests': '1',
                'Host': 'www.lagou.com',
                # 'Connection': 'keep-alive',
                'Origin': 'https://www.lagou.com',
                'Referer': url_sy,
                # 'X-Anit-Forge-Code': '0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
            }
            html_li_text = requests.post(url=url_lg_zw, headers=headers_1, data=data, proxies=proxies).text
            print(html_li_text)
            if num < 10:
                num = num + 1
                if '您操作太频繁,请稍后再访问' in html_li_text:
                    time.sleep(random.uniform(3,5))
                    continue
                else:
                    return html_li_text

            else:
                flag = False
                return html_li_text

        except:
            traceback.print_exc()


def parse_ssx_xml(font_xml_file):
    xml = etree.parse(font_xml_file)
    root = xml.getroot()
    font_dict = {}
    all_data = root.xpath('//cmap/cmap_format_4/map')
    for index, data in enumerate(all_data):
        font_value = data.attrib.get('name')[3:].lower()
        font_key = data.attrib.get('code')[2:].lower()
        contour_list = []
        if index == 0:
            continue
        font_dict[font_key] = font_value
    return font_dict
def handl_sxs_font(url):
    xz_font_file = True
    retry_t = 0
    while xz_font_file:
        r = requests.get(url, headers=head_reqst())
        r.encoding = 'utf-8'
        text = r.text
        # print(r.text)
        file_path = os.getcwd() + os.sep + str(time.time())
        # print(file_path)
        if not os.path.exists(file_path):
            # print('文件夹', file_path, '不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(file_path)
        else:
            shutil.rmtree(file_path)
            os.makedirs(file_path)
        sel = Selector(text=text)
        stonefont_url = text.split('{font-family:myFont; src: url("')[1].split('")}')[0]
        # print(999, stonefont_url)
        file_name = file_path + os.sep + 'all.txt'
        # 把字体文件的下载链接保存在本地
        try:
            with open(file_name, 'a+') as f:
                if '.eot' in stonefont_url:
                    continue
                elif 'data:application/octet-stream' in stonefont_url:
                    # stonefont_url = stonefont_url.split('font-family:"customfont"; src:url(')[1].split(')')[0]
                    f.write(stonefont_url + '\n')
                else:
                    print(stonefont_url)
                    print('请注意，出现新字体。。。')
            xz_font_file = False
            if stonefont_url:
                fontwoff_name = file_path + os.sep + '1.woff'
                fontxml_name = file_path + os.sep + '1_1.xml'
                urllib.request.urlretrieve(stonefont_url, fontwoff_name)
                # 整个if下部分为解析字体文件
                font = TTFont(fontwoff_name)
                # print('font对象：', font)
                font.saveXML(fontxml_name)
                # fontxml_name = '1532069096795_1.xml'
                font_dic = parse_ssx_xml(fontxml_name)
                re_font = r"&#x([0-9a-f]{4})"
                pattern_font = re.compile(re_font)
                font_code_set = set(pattern_font.findall(text))
                font_dic_sxs = {'30':'0',
                                '31':'1',
                                '32':'2',
                                '33':'3',
                                '34':'4',
                                '35':'5',
                                '36':'6',
                                '37':'7',
                                '38':'8',
                                '39':'9',
                                '4e00':'一',
                                '5e08':'师',
                                '58':'X',
                                '4f1a':'会',
                                '56db':'四',
                                '8ba1':'计',
                                '8d22':'财',
                                '573a':'场',
                                '44':'D',
                                '48':'H',
                                '4c':'L',
                                '50':'P',
                                '54':'T',
                                '8058':'聘',
                                '62db':'招',
                                '5de5':'工',
                                '64':'d',
                                '5468':'周',
                                '6c':'l',
                                '7aef':'端',
                                '70':'p',
                                '5e74':'年',
                                '68':'h',
                                '78':'x',
                                '8bbe':'设',
                                '7a0b':'程',
                                '4e8c':'二',
                                '4e94':'五',
                                '5929':'天',
                                '74':'t',
                                '43':'C',
                                '47':'G',
                                '524d':'前',
                                '4b':'K',
                                '4f':'O',
                                '7f51':'网',
                                '53':'S',
                                '57':'W',
                                '63':'c',
                                '67':'g',
                                '6b':'k',
                                '6f':'o',
                                '73':'s',
                                '77':'w',
                                '5e7f':'广',
                                '5e02':'市',
                                '6708':'月',
                                '4e2a':'个',
                                '42':'B',
                                '46':'F',
                                '544a':'告',
                                '4e':'N',
                                '52':'R',
                                '56':'V',
                                '5a':'Z',
                                '4f5c':'作',
                                '62':'b',
                                '66':'f',
                                '6a':'j',
                                '6e':'n',
                                '72':'r',
                                '76':'v',
                                '7a':'z',
                                '4e09':'三',
                                '4e92':'互',
                                '751f':'生',
                                '4eba':'人',
                                '653f':'政',
                                '41':'A',
                                '4a':'J',
                                '45':'E',
                                '49':'I',
                                '4ef6':'件',
                                '4d':'M',
                                '884c':'行',
                                '51':'Q',
                                '55':'U',
                                '59':'Y',
                                '61':'a',
                                '65':'e',
                                '69':'i',
                                '6d':'m',
                                '8f6f':'软',
                                '71':'q',
                                '75':'u',
                                '94f6':'银',
                                '79':'y',
                                '8054':'联',}
                for font_code in font_code_set:
                    sub_before = "&#x" + font_code
                    # print(font_code)
                    try:
                        text = text.replace(sub_before, font_dic_sxs[font_dic[font_code]])
                    except:
                        pass

                shutil.rmtree(file_path)
                return text
        except:
            shutil.rmtree(file_path)
            traceback.print_exc()
            time.sleep(random.uniform(3, 5))
            retry_t = retry_t + 1
            if retry_t >= 10:
                xz_font_file = False
def get_date(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)
def zwjx_51(text,compName ):
    sel = Selector(text=text)
    rms_job_detail = {}
    rms_job_detail['channel'] = 2
    rms_job_detail['jobLabel'] = []
    rms_job_detail['status'] = 1
    rms_job_detail['scrapy_state'] = 1
    rms_job_detail['companyName'] = compName
    # rms_job_detail['orgId'] = orgid
    # rms_job_detail['hrAcc'] = hr_acc
    # rms_job_detail['refreshTime'] = rt
    try:
        rms_job_detail['jobTitle'] = sel.xpath('//div[@class="tHeader tHjob"]/div/div[@class="cn"]/h1/text()').extract()[0].strip()
        rms_job_detail['id'] = sel.xpath('//div[@class="tHeader tHjob"]/div/div[@class="cn"]/h1/input[@name="hidJobID"]/@value').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    try:
        two_line_str = sel.xpath('//div[@class="com_tag"]/p')
        # qyxz = ['国企', '民营', '外资', '合资', '上市', '创业', '外企', '政府', '事业', '非营']
        qyxz = ['民营公司','国企','合资','外资（欧美）','外资（非欧美）','外企代表处','上市公司','政府机关','事业单位','创业公司','非盈利组织']
        for qyxg in two_line_str:
            company_in=qyxg.xpath('string()').extract()[0].strip()
            if company_in in qyxz:
                rms_job_detail['companyNature'] = company_in
            elif '-' in company_in or '人' in company_in:
                rms_job_detail['companyScale'] = company_in
            else:
                rms_job_detail['companyIndustry'] = company_in.split(',')
    except:
        traceback.print_exc()
        pass
    try:
        sala_text = sel.xpath('//div[@class="tHeader tHjob"]/div/div[@class="cn"]/strong/text()').extract()[0].strip()
        # print(sala_text)
        if '-' in sala_text:
            sala_digit=sala_text.replace("千/月","").replace("万/月","").replace("万/年","")

            if '月' in sala_text:
                if '千' in sala_text:
                    rms_job_detail['salaryLower'] = int(float(sala_digit.split('-')[0]) * 1000)
                    rms_job_detail['salaryUpper'] = int(float(sala_digit.split('-')[1]) * 1000)
                elif '万' in sala_text:
                    rms_job_detail['salaryLower'] = int(float(sala_digit.split('-')[0]) * 10000)
                    rms_job_detail['salaryUpper'] = int(float(sala_digit.split('-')[1]) * 10000)
            elif '年' in sala_text:
                    rms_job_detail['salaryLower'] = int(round(float(sala_digit.split('-')[0]) * 10000 / 12))
                    rms_job_detail['salaryUpper'] = int(round(float(sala_digit.split('-')[1]) * 10000 / 12))
        else:
            re_zw = r'(\d{1,4})'
            zw_list = re.findall(re_zw, sala_text, re.S | re.M)
            sala_digit = zw_list[0]
            if '月' in sala_text:
                if '千' in sala_text:
                    rms_job_detail['salaryLower'] = int(float(sala_digit) * 1000)
                    rms_job_detail['salaryUpper'] = int(float(sala_digit) * 1000)
                elif '万' in sala_text:
                    rms_job_detail['salaryLower'] = int(float(sala_digit) * 10000)
                    rms_job_detail['salaryUpper'] = int(float(sala_digit) * 10000)
            elif '年' in sala_text:
                    rms_job_detail['salaryLower'] = int(round(float(sala_digit) * 10000 / 12))
                    rms_job_detail['salaryUpper'] = int(round(float(sala_digit) * 10000 / 12))
            elif '日' in sala_text:
                rms_job_detail['salaryLower'] = int(round(float(sala_digit) * 22.5))
                rms_job_detail['salaryUpper'] = int(round(float(sala_digit) * 22.5))
            elif '时' in sala_text:
                rms_job_detail['salaryLower'] = int(round(float(sala_digit) * 8 * 22.5))
                rms_job_detail['salaryUpper'] = int(round(float(sala_digit) * 8 * 22.5))
    except:
        traceback.print_exc()
        pass
    try:
        address= sel.xpath('string(//div[@class="tHeader tHjob"]/div/div[@class="cn"]/p[@class="msg ltype"]/@title)').extract()[0].strip()
        rms_job_detail['address'] = address.split('|')[0].replace('\xa0','')
    except:
        traceback.print_exc()
        pass
    try:
        xx_dz = sel.xpath('string(//div[@class="bmsg inbox"]/p[@class="fp"])').extract()[0].strip()
        rms_job_detail['addressDetail'] = xx_dz.split('上班地址：', 1)[1].replace(' ','')
    except:
        traceback.print_exc()
        pass
    try:
        degree=['初中及以下','中技','中专','高中','大专','本科','MBA','硕士','博士']
        job_in= sel.xpath('string(//div[@class="tHeader tHjob"]/div/div[@class="cn"]/p[@class="msg ltype"]/@title)').extract()[0].strip()
        for job_info in job_in.split('|'):

            if '经验' in job_info:
                    if '无' in job_info:
                        rms_job_detail['workExperienceLower'] = ''
                        rms_job_detail['workExperienceUpper'] = ''
                    elif '年' in job_info:
                        if '-' in job_info:
                            rms_job_detail['workExperienceLower'] = job_info.replace('年经验','').split('-')[0].strip()
                            rms_job_detail['workExperienceUpper'] = job_info.replace('年经验','').split('-')[1].strip()
                        elif '以上' in job_info:
                            rms_job_detail['workExperienceLower'] = job_info.replace('年以上经验','').split('-')[0].strip()
                            rms_job_detail['workExperienceUpper'] = ''
                        else:
                            rms_job_detail['workExperienceLower'] = job_info.replace('年经验', '').strip()
                            rms_job_detail['workExperienceUpper'] = job_info.replace('年经验', '').strip()
            elif '人' in job_info:
                rms_job_detail['recruitmentSum'] = job_info.replace('招', '').replace('人', '').strip()
            elif job_info.strip() in degree:
                rms_job_detail['degree'] = job_info.strip()
            elif '发布' in job_info:
                rms_job_detail['refreshTime'] = '2018-'+ job_info.replace('发布','').strip()
    except:
        traceback.print_exc()
        pass

    try:
        xpa_znlb = 'string(//div[@class="bmsg job_msg inbox"]/div[@class="mt10"]/p)'
        xpa_zwms = '//div[@class="bmsg job_msg inbox"]/p'
        znlb_str = sel.xpath(xpa_znlb).extract()[0].strip()
        znlb_str = znlb_str.split('职能类别：')[1]
        rms_job_detail['jobCategory'] = znlb_str.replace("\n", "").replace("\r\n", "").replace("\r", "").replace(r'\t', '').replace("\t","").strip()
    except:
        traceback.print_exc()
        pass
    try:
        zwms_li = []
        for zwms_p in sel.xpath(xpa_zwms):
            zwms_p_str = zwms_p.xpath('string(.)').extract()[0].strip()
            zwms_li.append(zwms_p_str)
        rms_job_detail['jobDescription'] = ''.join(zwms_li)
    except:
        traceback.print_exc()
        pass
    try:
        rms_job_detail['companyIntroduction'] = sel.xpath('string(//div[@class="tmsg inbox"])').extract()[0].replace(' ', '').replace('\xa0','').strip()
    except:
        pass
    rms_job_detail['jobNature'] = ["全职"]
    try:
        job_La=sel.xpath('//div[@class="jtag"]/div/span')
        for job_Label in job_La:
            jobLabel=job_Label.xpath('string()').extract()[0].strip()
            rms_job_detail['jobLabel'].append(jobLabel)
    except:
        traceback.print_exc()
        pass
    return rms_job_detail
def zwjx_xzl(text,compName):
    sel = Selector(text=text)
    zl_zwxq = {}
    zl_zwxq['channel'] = 1
    zl_zwxq['status'] = 1
    zl_zwxq['scrapy_state'] = 1
    zl_zwxq['companyName'] = compName
    #id
    try:
        content=sel.xpath('string(//div[@class="gengduo"]/a/@href)').extract()[0].strip()
        zl_zwxq['id'] =content.split('pid=')[1].split("&")[0].strip()
    except:
        traceback.print_exc()
        pass
    # 工作名称
    try:
        zl_zwxq['jobTitle'] = sel.xpath('string(//div[@class="main1 cl main1-stat"]/div/ul/li/h1)').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 工作标签
    try:
        zl_zwxq['jobLabel'] = []
        jobLabel=text.split("var JobWelfareTab = '")[1].split("';")[0].replace(' ','')
        zl_zwxq['jobLabel']=jobLabel.split(",")
    except:
        traceback.print_exc()
        pass
    # 薪资
    try:
        salary= sel.xpath('string(//div[@class="l info-money"]/strong)').extract()[0].strip()
        zl_zwxq['salaryLower'] = int(salary.split('-')[0])
        zl_zwxq['salaryUpper'] = int(salary.split('-')[1].split('元')[0])
    except:
        traceback.print_exc()
        pass
    #地址
    try:
        zl_zwxq['address']= sel.xpath('string(//div[@class="info-three l"]/span[1])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 经验
    ts_list = ['经验不限', '无经验', '不限']
    try:
        workExperience= sel.xpath('string(//div[@class="info-three l"]/span[2])').extract()[0].strip()
        if workExperience in ts_list:
            zl_zwxq['workExperienceLower'] = ''
            zl_zwxq['workExperienceLower'] = ''
        elif '1年以下' in workExperience:
            zl_zwxq['workExperienceLower'] = 0
            zl_zwxq['workExperienceLower'] = 1
        elif '10年以上' in workExperience:
            zl_zwxq['workExperienceLower'] = 10
            zl_zwxq['workExperienceUpper'] = ''
        else:
            zl_zwxq['workExperienceLower'] = int(workExperience.replace('年', '').split('-')[0].strip())
            zl_zwxq['workExperienceUpper'] = int(workExperience.replace('年', '').split('-')[1].strip())
    except:
        traceback.print_exc()
        pass
    # 学历
    try:
        degree= sel.xpath('string(//div[@class="info-three l"]/span[3])').extract()[0].strip()
        if '不限'in degree:
            zl_zwxq['degree'] = '不限'
        else:
            zl_zwxq['degree'] = degree
    except:
        traceback.print_exc()
        pass
    # 招聘人数
    try:
        recruitmentSum = sel.xpath('string(//div[@class="info-three l"]/span[4])').extract()[0].strip()
        zl_zwxq['recruitmentSum'] = recruitmentSum.replace('招','').replace('人','')
    except:
        traceback.print_exc()
        pass
    # 职位性质
    try:
        zl_zwxq['jobNature'] = ['全职']
    except:
        traceback.print_exc()
        pass
    #职位描述
    try:
        jobDescription = sel.xpath('string(//div[@class="pos-ul"])').extract()[0].strip()
        zl_zwxq['jobDescription'] = jobDescription.replace(" ", "").replace("\n", "").replace("\r\n", "").replace("\r", "").replace(r'\t', '').replace("\t","").replace("\xa0","").strip()
    except:
        traceback.print_exc()
        pass
    #工作详细地址
    try:
        addressDetail = sel.xpath('string(//p[@class="add-txt"])').extract()[0].strip()
        zl_zwxq['addressDetail'] = addressDetail.replace(" ", "").replace("\n", "").replace("\r\n", "").replace("\r", "").replace(r'\t', '').replace("\t","").replace("\xa0","").strip()
    except:
        traceback.print_exc()
        pass
    # 公司简介
    try:
        companyIntroduction = sel.xpath('string(//div[@class="intro-content"])').extract()[0].strip()
        zl_zwxq['companyIntroduction'] = companyIntroduction.replace(" ", "").replace("\n", "").replace("\r\n", "").replace("\r", "").replace(r'\t', '').replace("\t", "").replace("\xa0","").strip()
    except:
        traceback.print_exc()
        pass
    # 公司行业
    try:
        zl_zwxq['companyIndustry']=[]
        zl_zwxq['companyIndustry'].append(sel.xpath('string(//ul[@class="promulgator-ul cl"]/li[1]/strong/a)').extract()[0].strip())
    except:
        traceback.print_exc()
        pass
    # 公司性质
    try:
        zl_zwxq['companyNature'] = sel.xpath('string(//ul[@class="promulgator-ul cl"]/li[2]/strong)').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 公司规模
    try:
        zl_zwxq['companyScale'] = sel.xpath('string(//ul[@class="promulgator-ul cl"]/li[3]/strong)').extract()[0].strip()
    except:
        traceback.print_exc()
        pass

    return zl_zwxq
def zwjx_zl(text, compName):
    sel = Selector(text=text)
    zl_zwxq = {}
    zl_zwxq['channel'] = 1
    zl_zwxq['status'] = 1
    zl_zwxq['scrapy_state'] = 1
    zl_zwxq['jobLabel'] = []
    zl_zwxq['companyName'] = compName
    #id
    try:
        content=sel.xpath('string(//div[@id="job-xszwtj"]/form/p/a/@href)').extract()[0].strip()
        zl_zwxq['id'] =content.split('pid=')[1].split("&")[0].strip()
    except:
        traceback.print_exc()
        pass
    # 工作名称
    try:
        zl_zwxq['jobTitle'] = sel.xpath('string(//div[@class="inner-left fl"]/h1)').extract()[0].strip()
    except:
        traceback.print_exc()
        pass

    # 工作标签
    try:
        zl_zwxq['jobLabel'] = []
        for wel in sel.xpath('//div[@class="inner-left fl"]/div[@class="welfare-tab-box"]/span'):
            zl_zwxq['jobLabel'].append(wel.xpath('string(.)').extract()[0].strip())
    except:
        traceback.print_exc()
        pass
    # 工作描述
    try:
        for ll in sel.xpath('//div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li'):
            if '职位月薪：' in ll.xpath('descendant::span/text()').extract()[0]:
                zwyx = ll.xpath('string()').extract()[0].split('职位月薪：')[1]
                if '以' not in zwyx:
                    zwyx = zwyx.split('元')[0]
                    zl_zwxq['salaryLower'] = int(zwyx.split('-')[0].strip())
                    zl_zwxq['salaryUpper'] = int(zwyx.split('-')[1].strip())
                else:
                    zwyx = zwyx.split('元')[0]
                    zl_zwxq['salaryLower'] = int(zwyx.strip())
                    zl_zwxq['salaryUpper'] = int(zwyx.strip())

            if '工作地点：' in ll.xpath('descendant::span/text()').extract()[0]:
                zl_zwxq['address'] = ll.xpath('string()').extract()[0].split('工作地点：')[1].strip().split(' ')[0]

            if '工作性质：' in ll.xpath('descendant::span/text()').extract()[0]:
                gzxz_txt = ll.xpath('string()').extract()[0]
                gzxz = gzxz_txt.split('工作性质：')[1].strip()
                if '全' in gzxz and '兼' in gzxz:
                    zl_zwxq['jobNature'] = ['全职', '兼职']
                elif '全' in gzxz:
                    zl_zwxq['jobNature'] = ['全职']
                elif '兼' in gzxz:
                    zl_zwxq['jobNature'] = ['兼职']


            if '工作年限：' in ll.xpath('descendant::span/text()').extract()[0] or '工作经验：' in ll.xpath('descendant::span/text()').extract()[0]:
                try:
                    gznx = ll.xpath('string()').extract()[0].split('工作年限：')[1].strip()
                except:
                    gznx = ll.xpath('string()').extract()[0].split('工作经验：')[1].strip()
                ts_list = ['经验不限','无经验','不限']
                if gznx in ts_list:
                    zl_zwxq['workExperienceLower'] = ''
                    zl_zwxq['workExperienceUpper'] = ''
                elif gznx == '1年以下':
                    zl_zwxq['workExperienceLower'] = 0
                    zl_zwxq['workExperienceUpper'] = 1
                elif gznx == '10年以上':
                    zl_zwxq['workExperienceLower'] = 10
                    zl_zwxq['workExperienceUpper'] = ''
                else:
                    zl_zwxq['workExperienceLower'] = int(gznx.replace('年', '').split('-')[0].strip())
                    zl_zwxq['workExperienceUpper'] = int(gznx.replace('年', '').split('-')[1].strip())

            if '最低学历：' in ll.xpath('descendant::span/text()').extract()[0]:
                zl_zwxq['degree'] = ll.xpath('string()').extract()[0].split('最低学历：')[1].strip()

            if '招聘人数：' in ll.xpath('descendant::span/text()').extract()[0]:
                zl_zwxq['recruitmentSum'] = ll.xpath('string()').extract()[0].split('招聘人数：')[1].strip().replace('人', '')

            if '职位类别：' in ll.xpath('descendant::span/text()').extract()[0]:
                zl_zwxq['jobCategory'] = ll.xpath('string()').extract()[0].split('职位类别：')[1].strip()
    except:
        pass
    try:
        desc_text = sel.xpath('string(//div[@class="tab-cont-box"]/div[@class="tab-inner-cont"])').extract()[0]
        zl_zwxq['jobDescription'] = desc_text.replace("\r", "").replace("\\", "").replace("查看职位地图", "").replace("\n","").replace("\r\n", "").replace("\xa0","").replace("》》在线沟通《《","").replace("点击此处可优先面试","").strip()
        xpa_gsbk = '//div[@class="company-box"]/ul[@class="terminal-ul clearfix terminal-company mt20"]/li'
        for gsbk in sel.xpath(xpa_gsbk):
            if '公司规模' in gsbk.xpath('string(.)').extract()[0]:
                zl_zwxq['companyScale'] = gsbk.xpath('string(.)').extract()[0].split('公司规模：')[1].strip()
            if '公司性质' in gsbk.xpath('string(.)').extract()[0]:
                zl_zwxq['companyNature'] = gsbk.xpath('string(.)').extract()[0].split('公司性质：')[1].strip()
            if '公司行业' in gsbk.xpath('string(.)').extract()[0]:
                zl_zwxq['companyIndustry'] = []
                gshy_str = gsbk.xpath('string(.)').extract()[0].split('公司行业：')[1].strip()
                zl_zwxq['companyIndustry'].append(gshy_str)
    except:
        traceback.print_exc()
        pass
    # 假地址
    try:
        jdz_li = zl_zwxq['jobDescription'].split('工作地址')
        zl_zwxq['addressDetail'] = jdz_li[-1].replace("查看职位地图", "").replace("：", "").strip()
    except:
        traceback.print_exc()
        pass

    # print(zl_zwxq)
    return zl_zwxq
def zwjx_58(text, compName):
    tc_job_detail = {}
    tc_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    tc_job_detail['jobLabel'] = []
    tc_job_detail['status'] = 1
    tc_job_detail['scrapy_state'] = 1
    tc_job_detail['channel'] = 3

    # 工作名称
    try:
        tc_job_detail['jobTitle'] = sel_jx.xpath('string(//div[@class="item_con pos_info"]/span)').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 工作ID
    try:
        job_id_str = sel_jx.xpath('//a[@class="pos_right_operate jubao"]/@href').extract()[0]
        tc_job_detail['id'] = job_id_str.split('infoid=')[1]
    except:
        traceback.print_exc()
        pass
    # 工作地址
    try:
        text_adress = sel_jx.xpath('string(//div[@class ="pos-area"]/span[1])').extract()[0].strip()
        tc_job_detail['address'] = text_adress.replace("\r\n", "").replace("\t", "").replace(" ", "").replace("\r",
                                                                                                              "").replace(
            "\n", "")
    except:
        traceback.print_exc()
        pass
    # 工作详细地址
    try:
        tc_job_detail['addressDetail'] = sel_jx.xpath('string(//div[@class ="pos-area"]/span[2])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 公司行业
    try:
        tc_job_detail['companyIndustry'] = sel_jx.xpath('string(//p[@class ="comp_baseInfo_belong"])').extract()[
            0].strip()
        tc_job_detail['companyIndustry'] = tc_job_detail['companyIndustry'].split('+')
    except:
        traceback.print_exc()
        pass
    # 公司规模
    try:
        tc_job_detail['companyScale'] = sel_jx.xpath('string(//p[@class ="comp_baseInfo_scale"])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 公司介绍
    try:
        tc_job_detail['companyIntroduction'] = sel_jx.xpath('string(//div[@class ="shiji"])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 职位描述
    try:
        job_desc = sel_jx.xpath('string(//div[@class ="des"])').extract()[0].strip()
        tc_job_detail['jobDescription'] = job_desc.replace("\r\n", "").replace("\r", "").replace("\n", "").replace(" ","").replace("\xa0", "")
    except:
        traceback.print_exc()
        pass
    # 职位性质
    # tc_job_detail['jobNature'] = sel_jx.xpath('string(//div[@class="pos_base_info"]/span)').extract()[0].strip()
    tc_job_detail['jobNature'] = ["全职"]
    # 工作标贴，列表格式
    try:
        tc_job_detail['jobLabel'] = []
        for wel in sel_jx.xpath('//div[@class="pos_welfare"]/span'):
            tc_job_detail['jobLabel'].append(wel.xpath('string()').extract()[0].strip())
        if not tc_job_detail['jobLabel']:
            tc_job_detail['jobLabel'] = []
    except:
        pass
    # 薪资
    try:
        xpa_qwxz = 'string(//div[@class="pos_base_info"]/span[@class="pos_salary"])'
        sala_text = sel_jx.xpath(xpa_qwxz).extract()[0].strip()
        # print(sala_text)
        if "元" in sala_text:
            salary_lower = sala_text.split('-')[0].strip()
            tc_job_detail['salaryLower'] = int(salary_lower)
            salary_upper = sala_text.split('-')[1].split("元")[0]
            tc_job_detail['salaryUpper'] = int(salary_upper)
        elif "面议" in sala_text:
            tc_job_detail['salaryLower'] = int(0)
            tc_job_detail['salaryUpper'] = int(0)
    except:
        traceback.print_exc()
        pass

    # 工作经验
    try:
        gzjy_58 = sel_jx.xpath('string(//span[@class="item_condition border_right_None"])').extract()[0].strip()
        if "不限" in gzjy_58:
            tc_job_detail['workExperienceLower'] = ''
            tc_job_detail['workExperienceUpper'] = ''

        elif "年" in gzjy_58:
            if "-" in gzjy_58:
                # experience_lower = gzjy_58.split('-')[0].strip()
                experience_lower = gzjy_58.split('年')[0].split('-')[0].strip()
                tc_job_detail['workExperienceLower'] = int(experience_lower)
                experience_upper = gzjy_58.split('年')[0].split('-')[1].strip()
                tc_job_detail['workExperienceUpper'] = int(experience_upper)
            elif "1年以下" in gzjy_58:
                tc_job_detail['workExperienceLower'] = 0
                tc_job_detail['workExperienceUpper'] = 1
            elif "以上" in gzjy_58:
                experience = gzjy_58.split('年')[0].strip()
                tc_job_detail['workExperienceLower'] = int(experience)
                tc_job_detail['workExperienceUpper'] = ''
    except:
        traceback.print_exc()
        pass

    # 招聘人数
    try:
        zprs_str = sel_jx.xpath('string(//span[@class="item_condition pad_left_none"])').extract()[0].strip()
        if "若干" in zprs_str:
            tc_job_detail['recruitmentSum'] = "若干"
        else:
            recruitment_sum = zprs_str.replace("招", "").replace("人", "").strip()
            tc_job_detail['recruitmentSum'] = recruitment_sum
    except:
        traceback.print_exc()
        pass

    # 学历
    try:
        degree = sel_jx.xpath('string(//span[@class="item_condition"])').extract()[0].strip()
        if "不限" in degree:
            tc_job_detail['degree'] = "不限"
        else:
            tc_job_detail['degree'] = degree
    except:
        traceback.print_exc()
        pass
    # 职位类别
    try:
        jobCategory = sel_jx.xpath('string(//span[@class="pos_title"])').extract()[0].strip()
        tc_job_detail['jobCategory'] = jobCategory
    except:
        traceback.print_exc()
        pass
    # 刷新时间
    try:
        refreshTime = sel_jx.xpath('string(//span[@class="pos_base_num pos_base_update"]/span)').extract()[0].strip()
        if '今天' in refreshTime or '小时'in refreshTime:
            tc_job_detail['jobCategory'] = str(datetime.datetime.today()).split(' ')[0]
        elif '昨天' in refreshTime:
            tc_job_detail['jobCategory'] = str(datetime.datetime.today()+datetime.timedelta(-1)).split(' ')[0]
        elif '前天' in refreshTime:
            tc_job_detail['jobCategory'] = str(datetime.datetime.today()+datetime.timedelta(-2)).split(' ')[0]
        else:
            tc_job_detail['jobCategory'] = refreshTime.split(" ")[0].strip()

    except:
        traceback.print_exc()
        pass

    return tc_job_detail
def zwjx_gj(text,compName):
    '''
    :param html_zw: 职位详情HTML
    :gj_job_detail{}:存储对应职位详情的字典
    :return: 返回解析完成后的字典
    '''
    gj_job_detail = {}
    gj_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    gj_job_detail['jobLabel'] = []
    gj_job_detail['status'] = 1
    gj_job_detail['scrapy_state'] = 1
    gj_job_detail['channel'] = 4
    #工作名称：
    gj_job_detail["jobTitle"] = sel_jx.xpath('string(//div[@class="title-line clearfix"]/p)').extract()[0].strip()
    #工作ID：
    gj_job_detail["id"] = sel_jx.xpath('string(//div[@class="module-right-ad"]/div/div/p/span)').extract()[0].strip()
    #工作性质:
    gj_job_detail["jobNature"] = ["全职"]
    #职位类别：
    gj_job_detail["jobCategory"] = sel_jx.xpath('string(//div[@class="title-line clearfix"]/h2)').extract()[0].strip()
    #工作地址：
    adress= sel_jx.xpath('string(//p[@class="detail-map-top"])').extract()[0].strip()
    gj_job_detail["address"] = adress.replace(" ", "").split("-")[0]
    gj_job_detail["addressDetail"]=adress.replace(" ","")
    #刷新时间
    try:
        refreshTime=sel_jx.xpath('string(//div[@class="first-line"]/p/span[1])').extract()[0].strip()
        refreshTime=refreshTime.replace("更新：","")
        if  "-" in refreshTime:
            if len(refreshTime.split('-')) == 3:
                gj_job_detail["refreshTime"] = "20" + refreshTime
            elif len(refreshTime.split('-')) == 2:
                gj_job_detail["refreshTime"] = "2018-" + refreshTime
        elif "刚刚" or "分钟" or "小时"  in refreshTime:
            today = str(datetime.date.today())
            gj_job_detail["refreshTime"] = today
        elif "昨天" in refreshTime:
            gj_job_detail["refreshTime"] =str(get_date(1)).split(" ")[0]
        elif "前天" in refreshTime:
            gj_job_detail["refreshTime"] =str(get_date(2)).split(" ")[0]

    except:
        pass
    #职位标贴
    for wel in sel_jx.xpath('//ul[@class="welfare-line clearfix"]/li'):
        gj_job_detail['jobLabel'].append(wel.xpath('string()').extract()[0].strip())
    if not gj_job_detail['jobLabel']:
        gj_job_detail['jobLabel'] = []
    #职位描述
    jobDescription=sel_jx.xpath('string(//div[@class="description-content"])').extract()[0].strip()
    gj_job_detail["jobDescription"]=jobDescription.replace("\r","").replace("\n","").replace("\t","").replace(" ","")
    #公司行业、性质、规模、介绍
    gj_job_detail["companyScale"] = sel_jx.xpath('string(//div[@class="introduce"]/span[1])').extract()[0].strip()
    gj_job_detail["companyNature"] = sel_jx.xpath('string(//div[@class="introduce"]/span[2])').extract()[0].strip()

    gj_job_detail["companyNature"] = sel_jx.xpath('string(//div[@class="introduce"]/span[2])').extract()[0].strip()
    companyIndustry = sel_jx.xpath('string(//div[@class="introduce"]/span[3])').extract()[0].strip()
    gj_job_detail["companyIndustry"] = []
    gj_job_detail['companyIndustry'].append(companyIndustry)
    companyIntroduction = sel_jx.xpath('string(//div[@class="info-text"]/div)').extract()[0].strip()
    gj_job_detail["companyIntroduction"] = companyIntroduction.replace("更多>" ,"").replace("\r","").replace("\n","").replace("\t","").replace(" ","")
    #学历、招聘人数、工作经验
    try:
        for job_in in sel_jx.xpath('//div[@class="description-label"]/span'):
            job_intr=job_in.xpath('string()').extract()[0].strip()
            if "人" in job_intr:
                gj_job_detail["recruitmentSum"] = job_intr.replace("招","").replace("人","")
                if "不限" in job_intr:
                    gj_job_detail["recruitmentSum"] = "不限"
            elif "学历" in job_intr:
                gj_job_detail["degree"] = job_intr.replace("要求", "").replace("学历", "")
                if "不限" in job_intr:
                    gj_job_detail["degree"] = "不限"
            elif "经验" in job_intr:
                if "不限" in job_intr:
                    gj_job_detail["workExperienceLower"] = ''
                    gj_job_detail["workExperienceUpper"] = ''
                elif "1年以内" in job_intr:
                    gj_job_detail["workExperienceLower"] = 0
                    gj_job_detail["workExperienceUpper"] = 1
                elif "-" in job_intr:
                    gj_job_detail["workExperienceLower"] = int(job_intr.split("-")[0].replace("要求", ""))
                    gj_job_detail["workExperienceUpper"] = int(job_intr.split("-")[1].split("年")[0])
                elif "以上"in job_intr:
                    gj_job_detail["workExperienceLower"] = 10
                    gj_job_detail["workExperienceUpper"] = ''
    except:
        pass
    #薪资
    try:
        salary=sel_jx.xpath('string(//div[@class="salary-line"]/b)').extract()[0].strip()
        if "面议" in salary:
            gj_job_detail["salaryLower"] = int(0)
            gj_job_detail["salaryUpper"] = int(0)
        elif "-" in salary:
            gj_job_detail["salaryLower"] = int(salary.split("-")[0])
            gj_job_detail["salaryUpper"] = int(salary.split("-")[1])
        elif "以" in salary:
            gj_job_detail["salaryLower"] = int(salary.split("以")[0])
            gj_job_detail["salaryUpper"] = int(salary.split("以")[0])
    except:
        pass
    # 输出
    return gj_job_detail
    # print(json.dumps(gj_job_detail, ensure_ascii=False))
def zwjx_hzrc(text, compName):
    '''
    :param html_zw: 职位详情HTML
    :hzrc_job_detail{}:存储对应职位详情的字典
    :return: 返回解析完成后的字典
    '''
    hzrc_job_detail = {}
    hzrc_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    hzrc_job_detail['jobLabel'] = []                  # 职位标贴
    hzrc_job_detail['status'] = 1
    hzrc_job_detail['scrapy_state'] = 1
    hzrc_job_detail['channel'] = 5
    #职位标贴
    try:
        for jl in sel_jx.xpath('//div[@class="postpointdiv"]/ul/li'):
            jobLabel=jl.xpath('string()').extract()[0].strip()
            hzrc_job_detail['jobLabel'].append(jobLabel)
    except:
        traceback.print_exc()
        pass
    # 工作名称：
    try:
        hzrc_job_detail["jobTitle"] = sel_jx.xpath('string(//div[@class="postselfdiv"]/div/span[@class="postname"])').extract()[0].strip()
    except:
        pass
    # 工作ID：
    try:
        id = sel_jx.xpath('string(//div[@class="postselfdiv"]/div/span[@class="postname"]/@onclick)').extract()[0].strip()
        hzrc_job_detail["id"] = id.split("('")[1].split("')")[0]
    except:
        pass
    for job_in in sel_jx.xpath('//div[@class="postdetaildiv"]/div'):
        job_intr = job_in.xpath('string()').extract()[0].strip()
        job_ti=job_in.xpath('string(descendant::div[1])').extract()[0].strip()
        #工作地址
        if "工作地点" in job_ti:
            try:
                if "省" in job_intr:
                    hzrc_job_detail["address"] = job_intr.replace("工作地点","").split("省")[1].split("市")[0].strip()
                elif "市" in job_intr:
                    hzrc_job_detail["address"] = job_intr.replace("工作地点","").split("市")[0].strip()
                hzrc_job_detail["addressDetail"] = job_intr.replace("工作地点","").strip()
            except:
                pass
        #职位类别
        elif "职位类别" in job_intr:
            try:
                hzrc_job_detail["jobCategory"] = job_intr.replace("职位类别", "").strip()
            except:
                pass
        #招聘人数
        elif "招聘人数" in job_intr:
            try:
                hzrc_job_detail["recruitmentSum"] = job_intr.replace("招聘人数", "").replace("人","").strip()
                if "不限"in job_intr:
                    hzrc_job_detail["recruitmentSum"] = 0
            except:
                pass
        #工作性质
        elif "工作性质" in job_intr:
            try:
                hzrc_job_detail["jobNature"]=[]
                jobNature = job_intr.replace("工作性质","").replace("均可","").strip()
                for job_na in jobNature.split("/")[0:]:
                    hzrc_job_detail["jobNature"].append(job_na)
            except:
                pass
        # 职位描述
        elif "职位描述" in job_intr:
            try:
                hzrc_job_detail["jobDescription"] = job_intr.replace("职位描述", "").replace("\r", "").replace("\n","").replace("\t","").replace(" ","")
            except:
                pass
        #学历
        elif "学历" in job_intr:
            try:
                if "不限" in job_intr:
                    hzrc_job_detail["degree"] = "不限"
                elif "其他" in job_intr:
                    hzrc_job_detail["degree"] = "不限"
                elif "大学" in job_intr:
                    hzrc_job_detail["degree"] = job_intr.replace("学历", "").replace("大学", "").strip()
                elif "普通高中" in job_intr:
                    hzrc_job_detail["degree"] = job_intr.replace("学历", "").replace("普通", "").strip()
                else:
                    hzrc_job_detail["degree"] = job_intr.replace("学历", "").strip()
            except:
                pass
        #工作经验
        elif "工作经验" in job_intr:
            try:
                if "无要求" in job_intr or "不限" in job_intr :
                    hzrc_job_detail["workExperienceLower"] = ''
                    hzrc_job_detail["workExperienceUpper"] = ''

                elif "在读生"in job_intr or "应届生"in job_intr :
                    hzrc_job_detail["workExperienceLower"] = int(0)
                    hzrc_job_detail["workExperienceUpper"] = int(0)
                elif "年" in job_intr:
                        if "-" in job_intr:
                            hzrc_job_detail["workExperienceLower"] = int(job_intr.replace("工作经验","").split("-")[0].strip())
                            hzrc_job_detail["workExperienceUpper"] = int(job_intr.replace("工作经验","").split("-")[1].replace("年","").strip())
                        elif "以" in job_intr:
                            hzrc_job_detail["workExperienceLower"] = int(job_intr.replace("工作经验", "").split("年")[0].strip())
                            hzrc_job_detail["workExperienceUpper"] = ''
                        else:
                            hzrc_job_detail["workExperienceLower"] = int(job_intr.replace("工作经验", "").replace("年","").strip())
                            hzrc_job_detail["workExperienceUpper"] = int(job_intr.replace("工作经验", "").replace("年","").strip())
            except:
                pass
            #薪资
        elif "薪资" in job_intr:
            try:
                if "面议" in job_intr:
                    hzrc_job_detail["salaryLower"] = int(0)
                    hzrc_job_detail["salaryUpper"] = int(0)
                elif "-" in job_intr:
                    hzrc_job_detail["salaryLower"] = int(job_intr.replace("薪资","").replace("￥","").split("-")[0].strip())
                    hzrc_job_detail["salaryUpper"] = int(job_intr.replace("薪资","").split("-")[1].strip())
                elif "以" in job_intr:
                    hzrc_job_detail["salaryLower"] = int(job_intr.replace("薪资", "").replace("￥", "").split("以")[0].strip())
                    hzrc_job_detail["salaryUpper"] = int(job_intr.replace("薪资", "").replace("￥", "").split("以")[0].strip())
            except:
                pass
        #刷新时间
    try:
        refreshTime=sel_jx.xpath('string(//div[@class="postewm"]/div/span)').extract()[0].strip()
        hzrc_job_detail["refreshTime"] =refreshTime.split("发布时间：")[1].split("浏览")[0].strip()
    except:
        pass
    # #详细地址
    # try:
    #     addressDetail = sel_jx.xpath('string(//div[@class="postcontact"]/span[@style="display: block;float: left;"])').extract()[0].strip()
    #     hzrc_job_detail["addressDetail"] = addressDetail.split("详细地址：")[1].strip()
    # except:
    #     pass
    for com_in in sel_jx.xpath('//div[@class="comcondiv"]/div/div'):
        com_intr = com_in.xpath('string()').extract()[0].strip()
        try:
            #公司行业
            if "行业" in com_intr:
                if com_intr.replace("行业","").strip() != "":
                    hzrc_job_detail["companyIndustry"]=[]
                    companyIndustry = com_intr.replace("行业","").strip()
                    hzrc_job_detail["companyIndustry"].append(companyIndustry)

            #公司性质
            # elif "类型" in com_intr:
            #     hzrc_job_detail["companyNature"] = com_intr.replace("类型","").strip()
            # 公司规模
            elif "规模" in com_intr:
                if com_intr.replace("规模", "").strip() != "" :
                    hzrc_job_detail["companyScale"] = com_intr.replace("规模", "").strip()
        except:
            pass
    # zw_data_hzrc=json.dumps(hzrc_job_detail, ensure_ascii=False)
    # print(zw_data_hzrc)
    return hzrc_job_detail
def zwjx_lg(text,compName,zw_data):
    lg_job_detail = {}
    lg_job_detail['companyName'] = compName
    lg_job_detail['jobLabel'] = []
    lg_job_detail['status'] = 1
    lg_job_detail['scrapy_state'] = 1
    lg_job_detail['channel'] = 13
    sel_jx = Selector(text=zw_data)
    # 工作名称：
    try:
        lg_job_detail["jobTitle"] = text['positionName'].replace("\u200b","").strip()
    except:
        traceback.print_exc()
        pass
    # 工作ID：
    try:
        lg_job_detail["id"] = str(text['positionId']).strip()
    except:
        traceback.print_exc()
        pass
    #刷新时间
    try:
        refreshTime=text['createTime'].strip()
        lg_job_detail["refreshTime"] =refreshTime.split(" ")[0].strip()
    except:
        traceback.print_exc()
        pass
    #地址
    try:
        lg_job_detail["address"]= text['city'].strip()
    except:
        traceback.print_exc()
        pass
    #职位标贴
    try:
        if ',' in text['positionAdvantage']:
            jobLabel=text['positionAdvantage'].split(',')
        elif '、'in text['positionAdvantage']:
            jobLabel = text['positionAdvantage'].split('、')
        elif ' 'in text['positionAdvantage']:
            jobLabel = text['positionAdvantage'].split(' ')
        else:
            lg_job_detail['jobLabel'].append(text['positionAdvantage'])
        for wel in jobLabel:
            lg_job_detail['jobLabel'].append(wel.strip())
        if not lg_job_detail['jobLabel']:
            lg_job_detail['jobLabel'] = []
    except:
        # traceback.print_exc()
        pass
    #薪资
    try:
        salary= text['salary'].strip()
        if "面议" in salary:
            lg_job_detail["salaryLower"] = int(0)
            lg_job_detail["salaryUpper"] = int(0)
        elif "-" in salary:
            lg_job_detail["salaryLower"] = int(salary.replace("k","").replace("K","").split("-")[0].strip())*1000
            lg_job_detail["salaryUpper"] = int(salary.replace("k","").replace("K","").split("-")[1].strip())*1000
        elif "以" in salary:
            lg_job_detail["salaryLower"] = int(salary.split("k")[0].split("K")[0].strip())*1000
            lg_job_detail["salaryUpper"] = int(salary.split("k")[0].split("K")[0].strip())*1000
    except:
        traceback.print_exc()
        pass
    #工作性质
    try:
        lg_job_detail["jobNature"] = []
        jobNature=text["jobNature"]
        lg_job_detail["jobNature"].append(jobNature)
    except:
        traceback.print_exc()
        pass

    #学历
    try:
        degree=text["education"]
        if "不限" in degree or "其他" in degree:
            lg_job_detail["degree"] = "不限"
        elif "及以" in degree:
            lg_job_detail["degree"] = degree.split("及以")[0].strip()
        else:
            lg_job_detail["degree"] = degree.strip()
    except:
        traceback.print_exc()
        pass
    # 经验
    try:
        workExperience = text["workYear"]
        if "应届" in workExperience :
            lg_job_detail["workExperienceLower"] = int(0)
            lg_job_detail["workExperienceUpper"] = int(0)
        elif "不限" in workExperience:
            lg_job_detail["workExperienceLower"] = ''
            lg_job_detail["workExperienceUpper"] = ''
        elif "1年以下"in workExperience:
            lg_job_detail["workExperienceLower"] = 0
            lg_job_detail["workExperienceUpper"] = 1
        elif "10年以上" in workExperience:
            lg_job_detail["workExperienceLower"] = 10
            lg_job_detail["workExperienceUpper"] = ''
        elif "-" in workExperience:
            lg_job_detail["workExperienceLower"] = int(workExperience.split("-")[0].strip())
            lg_job_detail["workExperienceUpper"] = int(workExperience.split("-")[1].replace("年", "").strip())
    except:
        traceback.print_exc()
        pass
    #公司行业
    try:
        companyIndustry=text["industryField"].split(',')
        lg_job_detail["companyIndustry"] = []
        for wel in companyIndustry:
            lg_job_detail['companyIndustry'].append(wel.strip())
        if not lg_job_detail['companyIndustry']:
            lg_job_detail['companyIndustry'] = []
    except:
        traceback.print_exc()
        pass
    #公司规模
    try:
        lg_job_detail["companyScale"] = text['companySize'].strip()
    except:
        traceback.print_exc()
        pass

    # 职位类别
    # try:
    #     lg_job_detail["jobCategory"] = text['companySize'].strip()
    # except:
    #     traceback.print_exc()
    #     pass

    #职位描述
    try:
        jobDescription=sel_jx.xpath('string(//dd[@class="job_bt"]/div)').extract()[0].strip()
        lg_job_detail["jobDescription"] = jobDescription.replace("职位描述", "").replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("\ufeff","").replace("\xa0","")
    except:
        traceback.print_exc()
        pass
    # 详细地址
    try:
        addressDetail=sel_jx.xpath('string(//div[@class="work_addr"])').extract()[0].strip()
        lg_job_detail["addressDetail"] = addressDetail.replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "").replace("查看地图","").strip()
    except:
        traceback.print_exc()
        pass
    return lg_job_detail
def zwjx_lp(text,compName):
    lp_job_detail = {}
    lp_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    lp_job_detail['jobLabel'] = []
    lp_job_detail['status'] = 1
    lp_job_detail['scrapy_state'] = 1
    lp_job_detail['channel'] = 10
    # 工作名称：
    try:
        lp_job_detail["jobTitle"] = sel_jx.xpath('string(//div[@class="title-info"]/h1)').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 工作ID：
    try:
        lp_job_detail["id"] = text.split('ejob_id=')[1].split('&')[0]
    except:
        traceback.print_exc()
        pass
    #刷新时间
    try:
        refreshTime=sel_jx.xpath('string(//p[@class="basic-infor"]/time)').extract()[0].strip()
        if '小时' in refreshTime or "分钟" in refreshTime or '刚刚'in refreshTime:
            lp_job_detail["refreshTime"] =str(datetime.date.today())
        elif "昨天" in refreshTime:
            lp_job_detail["refreshTime"] = str(get_date(1)).split(" ")[0]
        elif "前天" in refreshTime:
            lp_job_detail["refreshTime"] = str(get_date(2)).split(" ")[0]
        else:
            lp_job_detail["refreshTime"] =refreshTime.replace("发布于：","").strip()
    except:
        traceback.print_exc()
        pass
    #地址
    try:
        adress= sel_jx.xpath('string(//p[@class="basic-infor"]/span/a)').extract()[0].strip()
        if "-" in adress:
            lp_job_detail["address"] = adress.split("-")[0]
        else:
            lp_job_detail["address"] = adress
    except:
        traceback.print_exc()
        pass
    #职位标贴
    try:
        for wel in sel_jx.xpath('//ul[@class="comp-tag-list clearfix"]/li'):
            lp_job_detail['jobLabel'].append(wel.xpath('string()').extract()[0].strip())
        if not lp_job_detail['jobLabel']:
            lp_job_detail['jobLabel'] = []
    except:
        traceback.print_exc()
        pass
    #薪资
    try:
        salary= sel_jx.xpath('string(//p[@class="job-item-title"])').extract()[0].strip()
        if "面议" in salary:
            lp_job_detail["salaryLower"] = int(0)
            lp_job_detail["salaryUpper"] = int(0)
        elif "-" in salary:
            lp_job_detail["salaryLower"] = int(salary.split("-")[0].strip())*833
            lp_job_detail["salaryUpper"] = int(salary.split("-")[1].split("万")[0].strip())*833
        elif "以" in salary:
            lp_job_detail["salaryLower"] = int(salary.split("万")[0].strip())*833
            lp_job_detail["salaryUpper"] = int(salary.split("万")[0].strip())*833
    except:
        traceback.print_exc()
        pass
    #工作性质
    lp_job_detail["jobNature"] = []
    lp_job_detail["jobNature"].append('全职')
    #职位描述
    try:
        jobDescription=sel_jx.xpath('string(//div[@class="job-item main-message job-description"]/div)').extract()[0].strip()
        lp_job_detail["jobDescription"] = jobDescription.replace("职位描述", "").replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("\ufeff","").replace("\xa0","")
    except:
        traceback.print_exc()
        pass
    #公司介绍
    try:
        companyIntroduction = sel_jx.xpath('string(//div[@class="info-word"])').extract()[0].strip()
        lp_job_detail["companyIntroduction"] = companyIntroduction.replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\ufeff","")
    except:
        traceback.print_exc()
        pass
    #学历
    try:
        degree=sel_jx.xpath('string(//div[@class="job-qualifications"]/span[1])').extract()[0].strip()
        if "不限" in degree or "其他" in degree:
            lp_job_detail["degree"] = "不限"
        elif "统招" in degree:
            lp_job_detail["degree"] = degree.replace("统招","").strip()
        elif "及以上" in degree:
            lp_job_detail["degree"] = degree.split("及以上")[0].strip()
        else:
            lp_job_detail["degree"] = degree.strip()
    except:
        traceback.print_exc()
        pass
    # 经验
    try:
        workExperience = sel_jx.xpath('string(//div[@class="job-qualifications"]/span[2])').extract()[0].strip()
        if "应届" in workExperience or "在读生" in workExperience:
            lp_job_detail["workExperienceLower"] = int(0)
            lp_job_detail["workExperienceUpper"] = int(0)
        elif "不限" in workExperience:
            lp_job_detail["workExperienceLower"] = ''
            lp_job_detail["workExperienceUpper"] = ''
        elif "年" in workExperience:
            if "-" in workExperience:
                lp_job_detail["workExperienceLower"] = int(workExperience.split("-")[0].strip())
                lp_job_detail["workExperienceUpper"] = int(workExperience.split("-")[1].replace("年", "").strip())
            elif "以上" in workExperience:
                lp_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].strip())
                lp_job_detail["workExperienceUpper"] = ''

    except:
        traceback.print_exc()
        pass

    for com_in in sel_jx.xpath('//ul[@class="new-compintro"]/li'):
        com_intr = com_in.xpath('string()').extract()[0].strip()
        #公司行业
        try:
            if "行业" in com_intr:
                if com_intr.replace("行业：", "").strip() != "":
                    lp_job_detail["companyIndustry"] = []
                    companyIndustry = com_intr.replace("行业：", "").strip()
                    lp_job_detail["companyIndustry"].append(companyIndustry)
            elif "规模" in com_intr:
                if com_intr.replace("公司规模：", "").strip() != "" :
                    lp_job_detail["companyScale"] = com_intr.replace("公司规模：", "").strip()
            elif "公司地址" in com_intr:
                if com_intr.replace("公司地址：", "").strip() != "" :
                    lp_job_detail["addressDetail"] = com_intr.replace("公司地址：", "").strip()
        except:
            traceback.print_exc()
            pass
    return lp_job_detail
def zwjx_dj(text,compName,zw_data):
    dj_job_detail = {}
    dj_job_detail['companyName'] = compName
    dj_job_detail['jobLabel'] = []
    dj_job_detail['status'] = 1
    dj_job_detail['scrapy_state'] = 1
    dj_job_detail['channel'] = 7
    sel_jx = Selector(text=zw_data)
    # 工作名称：
    try:
        dj_job_detail["jobTitle"] = text['jobName'].replace("\u200b","").strip()
    except:
        pass
    # 工作ID：
    try:
        dj_job_detail["id"] = str(text['jobseq']).strip()
    except:
        pass

    #地址
    try:
        dj_job_detail["address"]= text['pubCity'].strip()
    except:
        pass

    #薪资
    try:
        salary= text['salary'].strip()
        if "面议" in salary:
            dj_job_detail["salaryLower"] = int(0)
            dj_job_detail["salaryUpper"] = int(0)
        elif "月" in salary:
            if "-" in salary:
                dj_job_detail["salaryLower"] = int(salary.replace("k","").replace("K","").split("-")[0].strip())*1000
                dj_job_detail["salaryUpper"] = int(salary.replace("k","").replace("/月","").replace("K","").split("-")[1].strip())*1000
            elif "以" in salary:
                dj_job_detail["salaryLower"] = int(salary.split("k")[0].split("K")[0].strip())*1000
                dj_job_detail["salaryUpper"] = int(salary.split("k")[0].split("K")[0].strip())*1000
        elif "天" in salary:
            if "-" in salary:
                dj_job_detail["salaryLower"] = int(salary.replace("元","").split("-")[0].strip())*30
                dj_job_detail["salaryUpper"] = int(salary.replace("元","").replace("/天","").split("-")[1].strip())*30
            elif "以" in salary:
                dj_job_detail["salaryLower"] = int(salary.split("元")[0].strip())*30
                dj_job_detail["salaryUpper"] = int(salary.split("元")[0].strip())*30
            else:
                dj_job_detail["salaryLower"] = int(salary.split("元")[0].strip())*30
                dj_job_detail["salaryUpper"] = int(salary.split("元")[0].strip())*30
    except:
        pass
    #招聘人数
    try:
        recruitmentSum = sel_jx.xpath('string(//div[@class="job-msg-center"]/ul/li[@class="recruiting"]/span)').extract()[0].strip()
        dj_job_detail["recruitmentSum"] = recruitmentSum.replace("人","").replace(" ","").replace("\xa0","")
    except:
        pass
    #工作性质
    try:
        jobNature = sel_jx.xpath('string(//span[@class="blue-icon"])').extract()[0].strip()
        dj_job_detail["jobNature"] = []
        dj_job_detail["jobNature"].append(jobNature.replace("（","").replace("）",""))
    except:
        pass
    #职位标贴
    try:
        for job_Label in sel_jx.xpath('//div[@class="job-msg-bottom"]/ul/li'):
            jobLabel = job_Label.xpath('string()').extract()[0].strip()
            dj_job_detail['jobLabel'].append(jobLabel)
    except:
        pass
    # 工作详细地址
    try:
        addressDetail = sel_jx.xpath('string(//div[@class="ads-msg"]/span)').extract()[0].strip()
        dj_job_detail["addressDetail"] = addressDetail.replace(" ", "").replace("\xa0", "")
    except:
        pass
    #学历
    try:
        degree=text["pubEdu"]
        if "不限" in degree or "其他" in degree:
            dj_job_detail["degree"] = "不限"
        elif "及以" in degree:
            dj_job_detail["degree"] = degree.split("及以")[0].strip()
        else:
            dj_job_detail["degree"] = degree.strip()
    except:
        pass
    # 经验
    try:
        workExperience = text["pubEx"]
        if "应届" in workExperience or "在读生" in workExperience:
            dj_job_detail["workExperienceLower"] = int(0)
            dj_job_detail["workExperienceUpper"] = int(0)
        elif "不限" in workExperience:
            dj_job_detail["workExperienceLower"] = ''
            dj_job_detail["workExperienceUpper"] = ''
        elif "年" in workExperience:
            if "-" in workExperience:
                dj_job_detail["workExperienceLower"] = int(workExperience.split("-")[0].strip())
                dj_job_detail["workExperienceUpper"] = int(workExperience.split("-")[1].replace("年", "").strip())
            elif "以上" in workExperience:
                dj_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].strip())
                dj_job_detail["workExperienceUpper"] = ''

    except:
        # traceback.print_exc()
        pass
    #公司行业
    try:
        companyIndustry=text["industryName"].strip()
        dj_job_detail["companyIndustry"] = []
        dj_job_detail['companyIndustry'].append(companyIndustry)
        if not dj_job_detail['companyIndustry']:
            dj_job_detail['companyIndustry'] = []
    except:
        pass
    #公司规模
    try:
        dj_job_detail["companyScale"] = text['scaleName'].replace(" ","").strip()
    except:
        pass
    # 公司性质
    try:
        for wel in sel_jx.xpath('//div[@class="i-corp-base-info"]/ul/li'):
            if "性质" in wel.xpath('string()').extract()[0].strip():
                dj_job_detail["companyNature"] = wel.xpath('string(span)').extract()[0].strip()
    except:
        pass

    #职位描述
    try:
        jobDescription=sel_jx.xpath('string(//div[@id="jp_maskit"])').extract()[0].strip()
        dj_job_detail["jobDescription"] = jobDescription.split("职位职责：")[1].replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("\ufeff","").replace("\xa0","")
    except:
        pass

    # 公司介绍
    try:
        companyIntroduction = sel_jx.xpath('string(//div[@class="i-corp-desc"])').extract()[0].strip()
        dj_job_detail["companyIntroduction"] = companyIntroduction.replace("\r", "").replace("\n",
                                                                                                     "").replace(
            "\t", "").replace(" ", "").replace("\ufeff", "").replace("\xa0", "")
    except:
        pass

    return dj_job_detail
def zwjx_zp(text,compName):
    '''
    :param html_zw: 职位详情HTML
    :zp_job_detail{}:存储对应职位详情的字典
    :return: 返回解析完成后的字典
    '''
    zp_job_detail = {}
    zp_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    zp_job_detail['jobLabel'] = []
    zp_job_detail['status'] = 1
    zp_job_detail['scrapy_state'] = 1
    zp_job_detail['channel'] = 8
    #工作名称：
    try:
        zp_job_detail["jobTitle"] = sel_jx.xpath('string(//div[@class="job-primary detail-box"]/div[@class="info-primary"]/div/h1)').extract()[0].strip()
    except:
        pass
    #工作ID：
    try:
        jobId=sel_jx.xpath('string(//div[@class="smallbanner"]/div/div/div/a/@ka)').extract()[0].strip()
        zp_job_detail["id"] =jobId.split("tosign_")[1]
    except:
        pass
    #工作性质:
    zp_job_detail["jobNature"] = ["全职"]
    #工作地址：
    try:
        adress= sel_jx.xpath('string(//div[@class="job-primary detail-box"]/div[@class="info-primary"]/p)').extract()[0].strip()
        zp_job_detail["address"] = adress.split("城市：")[1].split("经验：")[0].strip()
        zp_job_detail["addressDetail"]=sel_jx.xpath('string(//div[@class="location-address"])').extract()[0].replace(" ","").strip()
    except:
        pass
    #职位标贴
    try:
        for wel in sel_jx.xpath('//div[@class="detail-content"]/div/div[@class="job-tags"]/span'):
            zp_job_detail['jobLabel'].append(wel.xpath('string()').extract()[0].strip())
        if not zp_job_detail['jobLabel']:
            zp_job_detail['jobLabel'] = []
    except:
        pass
    #职位描述
    try:
        jobDescription = sel_jx.xpath('string(//div[@class="detail-content"]/div[@class="job-sec"]/div[@class="text"])').extract()[0].strip()
        zp_job_detail["jobDescription"] = jobDescription.replace("\r", "").replace("\n", "").replace("\t", "").replace(" ","").replace("\xa0","")
    except:
        pass
    #公司行业、介绍
    try:
        companyIndustry = sel_jx.xpath('string(//div[@class="info-company"]/p/a)').extract()[0].strip()
        zp_job_detail["companyIndustry"] =[]
        zp_job_detail["companyIndustry"].append(companyIndustry)
    except:
        pass
    try:
        companyIntroduction = sel_jx.xpath('string(//div[@class="job-sec company-info"]/div)').extract()[0].strip()
        zp_job_detail["companyIntroduction"] = companyIntroduction.replace("更多>", "").replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "").replace("\xa0","")
    except:
        pass
    #学历、工作经验
    try:
        for job_in in sel_jx.xpath('//div[@class="job-primary detail-box"]/div[@class="info-primary"]/p'):
            job_intr = job_in.xpath('string()').extract()[0].strip()

            if "学历"in job_intr:
                try:
                    zp_job_detail["degree"]=job_intr.split("学历：")[1].strip()
                except:
                    pass
                if "不限" in job_intr:
                    zp_job_detail["degree"] = "不限"
            try:
                if "经验"in job_intr:
                    if "不限" in job_intr:
                        zp_job_detail["workExperienceLower"] = ''
                        zp_job_detail["workExperienceUpper"] = ''
                    elif '应届生' in job_intr:
                        zp_job_detail["workExperienceLower"] = 0
                        zp_job_detail["workExperienceUpper"] = 0
                    elif '1年以内' in job_intr:
                        zp_job_detail["workExperienceLower"] = 0
                        zp_job_detail["workExperienceUpper"] = 1
                    elif "-" in job_intr:
                        workExperience=job_intr.split("经验：")[1].split("年")[0].strip()
                        zp_job_detail["workExperienceLower"] = int(workExperience.split("-")[0].strip())
                        zp_job_detail["workExperienceUpper"] = int(workExperience.split("-")[1].strip())
                    elif "10年以上" in job_intr:
                        zp_job_detail["workExperienceLower"] = 10
                        zp_job_detail["workExperienceUpper"] = ''
            except:
                pass
    except:
        pass
    #工资
    try:
        salary=sel_jx.xpath('string(//div[@class="job-primary detail-box"]/div/div[@class="name"]/span)').extract()[0].strip()
        if  "-" in salary:
            zp_job_detail["salaryLower"] = int(salary.split("-")[0].replace("K","").strip())*1000
            zp_job_detail["salaryUpper"] = int(salary.split("-")[1].replace("K","").strip())*1000
        elif  "面议" in salary:
            zp_job_detail["salaryLower"] = int(0)
            zp_job_detail["salaryUpper"] = int(0)
        elif "以"in salary:
            zp_job_detail["salaryLower"] = int(salary.split("以")[0].replace("K", "").strip()) * 1000
            zp_job_detail["salaryUpper"] = int(salary.split("以")[0].replace("K", "").strip()) * 1000
    except:
        pass
    #刷新时间
    try:
        refreshTime=sel_jx.xpath('string(//div[@class="job-author"]/span)').extract()[0].strip()
        zp_job_detail["refreshTime"] = refreshTime.split("于")[1].split(" ")[0]
    except:
        pass
    #职位类别
    try:
        zp_job_detail["jobCategory"] = sel_jx.xpath('string(//div[@class="info-primary"]/div[@class ="job-tags"]/span)').extract()[0].strip()
    except:
        pass
    #公司性质、规模
    try:
        comp= sel_jx.xpath('//div[@class="info-company"]/p[1]').extract()[0]
        zp_job_detail["companyNature"] = comp.split('<em class="vline"></em>')[0].split('<p>')[1]
        zp_job_detail["companyScale"] = comp.split('<em class="vline"></em>')[1]
    except:
        pass
    #招聘人数
    #输出
    return zp_job_detail
def zwjx_sxs(text,compName):
    sxs_job_detail = {}
    sxs_job_detail['companyName'] = compName
    sxs_job_detail['workExperienceLower'] = ''
    sxs_job_detail['workExperienceUpper'] = ''
    sel_jx = Selector(text=text)
    sxs_job_detail['jobLabel'] = []
    sxs_job_detail['status'] = 1
    sxs_job_detail['scrapy_state'] = 1
    sxs_job_detail['channel'] = 16
    # 工作名称：
    try:
        sxs_job_detail["jobTitle"] = sel_jx.xpath('string(//div[@class="new_job_name"])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    # 工作ID：
    try:
        id_href= sel_jx.xpath('string(//link[@rel="alternate"]/@href)').extract()[0].strip()
        sxs_job_detail["id"] = id_href.split("intern/")[1]
    except:
        traceback.print_exc()
        pass
    #刷新时间
    try:
        refreshTime=sel_jx.xpath('string(//div[@class="job_date "]/span[1])').extract()[0].strip()
        if '小时' in refreshTime or "分钟" in refreshTime or '刚刚'in refreshTime or '今天'in refreshTime:
            sxs_job_detail["refreshTime"] =str(datetime.date.today())
        elif "昨天" in refreshTime:
            sxs_job_detail["refreshTime"] = str(get_date(1)).split(" ")[0]
        elif "前天" in refreshTime:
            sxs_job_detail["refreshTime"] = str(get_date(2)).split(" ")[0]
        else:
            sxs_job_detail["refreshTime"] =refreshTime.split(" ")[0].strip()
    except:
        traceback.print_exc()
        pass
    #地址
    try:
        adress= sel_jx.xpath('string(//div[@class="job_msg"]/span[@class="job_position"])').extract()[0].strip()
        if "-" in adress:
            sxs_job_detail["address"] = adress.split("-")[0]
        else:
            sxs_job_detail["address"] = adress
    except:
        traceback.print_exc()
        pass
    #职位标贴
    try:
        job_good = sel_jx.xpath('string(//div[@class="job_good"])').extract()[0].strip()
        if "+" in job_good:
            jobLabel=job_good.replace("职位诱惑：","").replace("。","").split("+")
        elif " " in job_good:
            jobLabel = job_good.replace("职位诱惑：", "").replace("。", "").split(" ")
        elif "、" in job_good:
            jobLabel = job_good.replace("职位诱惑：", "").replace("。", "").split("、")
        elif "，" in job_good:
            jobLabel = job_good.replace("职位诱惑：", "").replace("。", "").split("，")
        elif "；" in job_good:
            jobLabel = job_good.replace("职位诱惑：", "").replace("。", "").split("；")
        elif "#" in job_good:
            jobLabel = job_good.replace("职位诱惑：", "").replace("。", "").split("#")
        elif job_good != "":
            sxs_job_detail['jobLabel'].append(job_good.replace("职位诱惑：", "").replace("。", ""))
        for wel in jobLabel:
            sxs_job_detail['jobLabel'].append(wel.strip())
        if not sxs_job_detail['jobLabel']:
            sxs_job_detail['jobLabel'] = []
    except:
        pass
    #薪资
    try:
        salary= sel_jx.xpath('string(//div[@class="job_msg"]/span[@class="job_money cutom_font"])').extract()[0].strip()
        if "面议" in salary:
            sxs_job_detail["salaryLower"] = int(0)
            sxs_job_detail["salaryUpper"] = int(0)
        elif "-" in salary:
            sxs_job_detail["salaryLower"] = int(salary.split("-")[0].strip())*22.5
            sxs_job_detail["salaryUpper"] = int(salary.split("-")[1].split("／天")[0].strip())*22.5
        elif "以" in salary:
            sxs_job_detail["salaryLower"] = int(salary.replace("／天",'').strip())*22.5
            sxs_job_detail["salaryUpper"] = int(salary.replace("／天","").strip())*22.5
    except:
        pass
    #工作性质
    sxs_job_detail["jobNature"] = []
    sxs_job_detail["jobNature"].append('实习')
    #职位描述
    try:
        jobDescription=sel_jx.xpath('string(//div[@class="job_part"]/div[@class="job_detail"])').extract()[0].strip()
        sxs_job_detail["jobDescription"] = jobDescription.replace("职位描述", "").replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("\ufeff","").replace("\xa0","")
    except:
        traceback.print_exc()
        pass
    #公司介绍
    try:
        companyIntroduction = sel_jx.xpath('string(//div[@class="con-job con-com_introduce"]/div[@class="job_detail"])').extract()[0].strip()
        sxs_job_detail["companyIntroduction"] = companyIntroduction.replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\ufeff","")
    except:
        traceback.print_exc()
        pass
    #学历
    try:
        degree=sel_jx.xpath('string(//span[@class="job_academic"]/span[1])').extract()[0].strip()
        if "不限" in degree or "其他" in degree:
            sxs_job_detail["degree"] = "不限"
        elif "统招" in degree:
            sxs_job_detail["degree"] = degree.replace("统招","").strip()
        elif "及以上" in degree:
            sxs_job_detail["degree"] = degree.split("及以上")[0].strip()
        elif degree != "":
            sxs_job_detail["degree"] = degree.strip()
    except:
        traceback.print_exc()
        pass

    # 公司地址
    try:
        addressDetail = sel_jx.xpath('string(//div[@class="job_com_position"]/span[@class="com_position"])').extract()[0].strip()
        sxs_job_detail["addressDetail"] = addressDetail.replace("\r", "").replace("\n", "").replace(
            "\t", "").replace(" ", "").replace("\xa0", "").replace("\ufeff", "")
    except:
        traceback.print_exc()
        pass
    try:
        for com_in in sel_jx.xpath('//div[@class="job_detail job_detail_msg"]/span'):
            com_intr = com_in.xpath('string()').extract()[0].strip()
            #公司行业
            try:
                # if "行业" in com_intr:
                #     if com_intr.replace("行业：", "").strip() != "":
                #         sxs_job_detail["companyIndustry"] = []
                #         companyIndustry = com_intr.replace("行业：", "").strip()
                #         sxs_job_detail["companyIndustry"].append(companyIndustry)
                if "人" in com_intr:
                        sxs_job_detail["companyScale"] = com_intr.strip()

            except:
                traceback.print_exc()
                pass
    except:
        pass
    return sxs_job_detail
def zwjx_zhyc(text, compName):
    zhyc_job_detail = {}
    zhyc_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    zhyc_job_detail['jobLabel'] = []
    zhyc_job_detail['status'] = 1
    zhyc_job_detail['scrapy_state'] = 1
    zhyc_job_detail['channel'] = 6
    # 工作名称：
    try:
        zhyc_job_detail["jobTitle"] = sel_jx.xpath('string(//div[@class="job_left"]/h1)').extract()[0].strip()
    except:
        pass
    # 工作ID：
    try:
        zhyc_job_detail["id"] = sel_jx.xpath('string(//div[@class="job_container"]/@infoid)').extract()[0].strip()
    except:
        pass
    # 工作地址：
    try:
        adress = sel_jx.xpath('string(//span[@class="job_address"])').extract()[0]
        zhyc_job_detail["address"] = adress.split("\t")[0]
        zhyc_job_detail["addressDetail"] = adress.split("\t")[1]
    except:
        pass
    # 职位标贴
    try:
        for wel in sel_jx.xpath('//div[@class="job_item_2"]/span[@class="job_tag"]'):
            if wel.xpath('string()').extract()[0].strip() != "更多":
                zhyc_job_detail['jobLabel'].append(wel.xpath('string()').extract()[0].strip())
        if not zhyc_job_detail['jobLabel']:
            zhyc_job_detail['jobLabel'] = []
    except:
        pass
    #职位描述
    try:
        jobDescription = sel_jx.xpath('string(//div[@class="desc_text"])').extract()[0].strip()
        zhyc_job_detail["jobDescription"] = jobDescription.replace("\r", "").replace("\n", "").replace("\t", "").replace(" ","").replace('\xa0','')
    except:
        pass
    #公司行业、介绍
    try:
        companyIndustry= sel_jx.xpath('string(//span[@class="job_enterprisetype"])').extract()[0].strip()
        zhyc_job_detail["companyScale"] = companyIndustry.split('|')[1].strip()
        zhyc_job_detail["companyIndustry"] =companyIndustry.split('|')[0].replace(' ','').split('+')
    except:
        pass
    try:
        companyIntroduction = sel_jx.xpath('string(//div[@class="details_text"])').extract()[0].strip()
        zhyc_job_detail["companyIntroduction"] = companyIntroduction.replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "")
    except:
        pass
    #薪资
    try:
        salary =sel_jx.xpath('string(//span[@class="job_salary"])').extract()[0].strip()
        if  "-" in salary:
            zhyc_job_detail["salaryLower"] = int(salary.split("-")[0])
            zhyc_job_detail["salaryUpper"] = int(salary.split("-")[1].replace('元/月','').replace(' ',''))
        elif  "面议" in salary:
            zhyc_job_detail["salaryLower"] = int(0)
            zhyc_job_detail["salaryUpper"] = int(0)
        elif "以"in salary:
            zhyc_job_detail["salaryLower"] = int(salary.split("以")[0])
            zhyc_job_detail["salaryUpper"] = int(salary.split("以")[0])
    except:
        pass
    #工作性质
    try:
        zhyc_job_detail["jobNature"].append('全职')
    except:
        pass
    #学历、工作经验
    try:

        job_req=sel_jx.xpath('string(//span[@class="job_addr"])').extract()[0].strip()
        degree=job_req.split("|")[2].strip()
        if "不限" in degree or "其他" in degree :
            zhyc_job_detail["degree"]= "不限"
        else:
            zhyc_job_detail["degree"] = degree
    except:
        pass
    workExperience = job_req.split("|")[1].strip()
    try:
        if "不限" in workExperience :
            zhyc_job_detail["workExperienceLower"] = ''
            zhyc_job_detail["workExperienceUpper"] = ''
        elif "应届" in workExperience:
            zhyc_job_detail["workExperienceLower"] = 0
            zhyc_job_detail["workExperienceUpper"] = 0
        elif "1年以下" in workExperience:
            zhyc_job_detail["workExperienceLower"] = 0
            zhyc_job_detail["workExperienceUpper"] = 1
        elif "-" in workExperience:
            zhyc_job_detail["workExperienceLower"] = int(workExperience.replace("年","").replace("经验","").split("-")[0].strip())
            zhyc_job_detail["workExperienceUpper"] = int(workExperience.replace("年","").replace("经验","").split("-")[1].strip())
        elif "以上" in workExperience:
            zhyc_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].strip())
            zhyc_job_detail["workExperienceUpper"] = ''
        else:
            zhyc_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].strip().strip())
            zhyc_job_detail["workExperienceUpper"] = int(workExperience.split("年")[0].strip().strip())
    except:
            traceback.print_exc()
            pass
    #职位类别
    try:
        zhyc_job_detail["jobCategory"] = job_req.split("|")[-1].strip()
        zhyc_job_detail["recruitmentSum"] = job_req.split("|")[-2].strip()
    except:
        pass


    return zhyc_job_detail
'''中华英才旧版'''
def zwjx_zhyc_0(text, compName):

    zhyc_job_detail = {}
    zhyc_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    zhyc_job_detail['jobLabel'] = []
    zhyc_job_detail['status'] = 1
    zhyc_job_detail['scrapy_state'] = 1
    zhyc_job_detail['channel'] = 6
    # 工作名称：
    try:
        zhyc_job_detail["jobTitle"] = sel_jx.xpath('string(//span[@class="job_name"])').extract()[0].strip()
    except:
        pass
    # 工作ID：
    try:
        id = sel_jx.xpath('string(//div[@class="job_profile jpadding"]/div/@onclick)').extract()[0].strip()
        zhyc_job_detail["id"] = id.split("jobid=")[1].split("&gtid=")[0]
    except:
        pass
    # 工作地址：
    try:
        adress = sel_jx.xpath('string(//div[@class="job_require"]/span[@class="job_loc"])').extract()[0]
        zhyc_job_detail["address"] = adress.split(" ")[0]
    except:
        pass
    # 职位标贴
    try:
        for wel in sel_jx.xpath('//div[@class="job_fit_tags"]/ul/li'):
            if wel.xpath('string()').extract()[0].strip() != "更多":
                zhyc_job_detail['jobLabel'].append(wel.xpath('string()').extract()[0].strip())
        if not zhyc_job_detail['jobLabel']:
            zhyc_job_detail['jobLabel'] = []
    except:
        pass
    #职位描述
    try:
        jobDescription = sel_jx.xpath('string(//div[@class="job_intro_wrap"])').extract()[0].strip()
        zhyc_job_detail["jobDescription"] = jobDescription.replace("\r", "").replace("\n", "").replace("\t", "").replace(" ","").replace('\xa0','')
    except:
        pass
    #公司行业、介绍
    try:
        companyIndustry= sel_jx.xpath('string(//div[@class="compny_tag"]/span[@class="job_loc"])').extract()[0].strip()
        zhyc_job_detail["companyIndustry"] =[]
        zhyc_job_detail["companyIndustry"].append(companyIndustry)
    except:
        pass
    try:
        companyIntroduction = sel_jx.xpath('string(//div[@class="company_service"])').extract()[0].strip()
        zhyc_job_detail["companyIntroduction"] = companyIntroduction.replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "")
    except:
        pass
    #薪资
    try:
        job_req =sel_jx.xpath('string(//div[@class="job_require"])').extract()[0].strip()
        salary=job_req.split("|")[0].strip()
        if  "-" in salary:
            zhyc_job_detail["salaryLower"] = int(salary.split("-")[0])
            zhyc_job_detail["salaryUpper"] = int(salary.split("-")[1])
        elif  "面议" in salary:
            zhyc_job_detail["salaryLower"] = int(0)
            zhyc_job_detail["salaryUpper"] = int(0)
        elif "以"in salary:
            zhyc_job_detail["salaryLower"] = int(salary.split("以")[0])
            zhyc_job_detail["salaryUpper"] = int(salary.split("以")[0])
    except:
        pass
    #工作性质
    try:
        jobNature=job_req.split("|")[2].strip()
        zhyc_job_detail["jobNature"] = []
        zhyc_job_detail["jobNature"].append(jobNature)

    except:
        pass
    #学历、工作经验
    try:
        degree=job_req.split("|")[3].strip()
        if "不限" in degree or "其他" in degree :
            zhyc_job_detail["degree"]= "不限"
        else:
            zhyc_job_detail["degree"] = degree
    except:
        pass
    workExperience = job_req.split("|")[4].strip()
    try:
        if "不限" in workExperience :
            zhyc_job_detail["workExperienceLower"] = ''
            zhyc_job_detail["workExperienceUpper"] = ''
        elif "应届" in workExperience:
            zhyc_job_detail["workExperienceLower"] = 0
            zhyc_job_detail["workExperienceUpper"] = 0
        elif "1年以下" in workExperience:
            zhyc_job_detail["workExperienceLower"] = 0
            zhyc_job_detail["workExperienceUpper"] = 1
        elif "-" in workExperience:
            zhyc_job_detail["workExperienceLower"] = int(workExperience.replace("年","").split("经验")[1].split("-")[0].strip())
            zhyc_job_detail["workExperienceUpper"] = int(workExperience.replace("年","").split("经验")[1].split("-")[1].strip())
        elif "以上" in workExperience:
            zhyc_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].split("经验")[1].strip())
            zhyc_job_detail["workExperienceUpper"] = ''
        else:
            zhyc_job_detail["workExperienceLower"] = int(workExperience.replace("年","").split("经验")[1].strip())
            zhyc_job_detail["workExperienceUpper"] = int(workExperience.replace("年","").split("经验")[1].strip())
    except:
        traceback.print_exc()
        pass
    #公司性质、规模
    try:
        zhyc_job_detail["companyNature"] = sel_jx.xpath('string(//div[@class="compny_tag"]/span[2])').extract()[0].strip()
    except:
        pass
    try:
        companyScale=sel_jx.xpath('string(//div[@class="compny_tag"]/span[3])').extract()[0].strip()
        zhyc_job_detail["companyScale"] = companyScale.replace("规模","").replace(" ","")
    except:
        pass
    #职位类别、详情地址、招聘人数
    return zhyc_job_detail
def zwjx_qcrc(text,compName):
    sel_jx = Selector(text=text)
    html = etree.HTML(text)
    rms_job_detail = dict()
    rms_job_detail['companyName'] = compName
    rms_job_detail['jobLabel'] = []
    rms_job_detail['scrapy_state'] = 1
    rms_job_detail['channel'] = 15
    rms_job_detail['status'] = 1
    rms_job_detail['jobNature'] = ['全职']
    try:
        id=sel_jx.xpath('string(//div[@class="apply_list"]/a/input/@onclick)').extract()[0].strip()
        rms_job_detail['id'] = id.split("('")[1].split("',")[0].strip()
    except:
        traceback.print_exc()
    try:
        rms_job_detail['jobTitle'] = html.xpath('//div[@class="Process_Engineer_left fl"]/div[@class="process_engineertop"]/div[@class="process_engineertopbag"]/h5[@class="process_title"]/text()')[0].strip()
    except:
        traceback.print_exc()
    try:
        process_engineerfonts = html.xpath('//div[@class="Process_Engineer_left fl"]/div[@class="process_engineertop"]/div[@class="process_engineerfonts"]')[0]
        try:
            salary = process_engineerfonts.xpath('./div[@class="process_engineer_fontstop ovh"]/p[1]/text()')[0].strip()
            if salary == '面议':
                rms_job_detail['salaryLower'] = 0
                rms_job_detail['salaryUpper'] = 0
            elif "-" in salary:
                salary = re.search(r'(\d+)-(\d+)元', salary).groups()
                rms_job_detail['salaryLower'] = salary[0]
                rms_job_detail['salaryUpper'] = salary[1]
            else:
                salary = salary.split('元')[0].strip()
                rms_job_detail['salaryLower'] = int(salary)
                rms_job_detail['salaryUpper'] = int(salary)
        except:
            traceback.print_exc()

        try:
            work_experience = process_engineerfonts.xpath('./div[@class="process_engineer_fontstop ovh"]/span[2]/text()')[0].strip()
            if work_experience in ['应届毕业生', '在读学生']:
                rms_job_detail['workExperienceLower'] = 0
                rms_job_detail['workExperienceUpper'] = 0
            elif "不限" in work_experience:
                rms_job_detail['workExperienceLower'] = ''
                rms_job_detail['workExperienceUpper'] = ''
            else:
                rms_job_detail['workExperienceLower'] = re.search(r'(\d+)年以上', work_experience).group(1)
                rms_job_detail['workExperienceUpper'] = ''
        except:
            traceback.print_exc()
        address = process_engineerfonts.xpath('./div[@class="process_engineer_fontstop ovh"]/span[1]/i/text()')[0].strip()
        # rms_job_detail['address'] = [i.strip() for i in address]
        rms_job_detail['address'] = address.strip()
        rms_job_detail['degree'] = process_engineerfonts.xpath('./div[@class="process_engineer_fontstop ovh"]/span[3]/text()')[0].strip()
        job_category = process_engineerfonts.xpath('./div[@class="process_engineer_fontstop ovh"]/span[4]/text()')
        if job_category:
            rms_job_detail['jobCategory'] = job_category[0].strip()

        job_label = process_engineerfonts.xpath('./ul[@class="process_engineer_fontlist"]/li/text()')
        if job_label:
            rms_job_detail['jobLabel'] = [i.strip() for i in job_label]

        rms_job_detail['refreshTime'] = process_engineerfonts.xpath('./p[@class="process_titlein"]/text()')[0][0: -2]
    except:
        traceback.print_exc()
    try:
        job_description = html.xpath(
            '//div[@class="Process_Engineer_left fl"]/div[@class="description"]/div[@class="description_listind"]/div[@class="process_title_listin"]/h5[contains(text(), "职位描述")]//following-sibling::div[@class="description_list"]/p/text()')
        if job_description:
            rms_job_detail['jobDescription'] = ''.join([i.strip() for i in job_description])
    except:
        traceback.print_exc()
    try:
        group_1 = html.xpath('//div[@class="Process_Engineer_right fl"]/div[@class="Process_engineer_top"]')[0]
        # rms_job_detail['companyName'] = group_1.xpath('./h5[1]/a/text()')[0].strip()
        company_nature = group_1.xpath('./div[@class="fl postion_title_r"]/p/img[contains(@src, "icom_leftin")]//following-sibling::span/text()')
        if company_nature:
            rms_job_detail['companyNature'] = company_nature[0].strip()
        company_scale = group_1.xpath('./div[@class="fl postion_title_r"]/p/img[contains(@src, "icom_li")]//following-sibling::span/text()')
        if company_scale:
            rms_job_detail['companyScale'] = company_scale[0].strip()
        address_detail = group_1.xpath('./div[@class="fl postion_title_r"]/p/img[contains(@src, "icom_map")]//following-sibling::span/text()')
        if address_detail:
            rms_job_detail['addressDetail'] = address_detail[0].strip()
    except:
        traceback.print_exc()

    return rms_job_detail
def zwjx_rcrx(text,compName):
    sel = Selector(text=text)
    zgrcrx_zwxq = {}
    zgrcrx_zwxq['channel'] = 12
    zgrcrx_zwxq['scrapy_state'] = 1
    zgrcrx_zwxq['status'] = 1
    zgrcrx_zwxq['jobLabel'] = []
    zgrcrx_zwxq['jobNature'] = []
    zgrcrx_zwxq['companyName'] = compName
    xl_li = ['初中', '高中', '中技', '中专', '大专', '本科', '硕士', '博士']
    jn_li = ['全职', '兼职', '实习', '应届毕业生']
    # id
    content = sel.xpath('//input[@id="hidJobPostID"]/@value').extract()[0].strip()
    zgrcrx_zwxq['id'] = content.strip()

    # 工作名称
    zgrcrx_zwxq['jobTitle'] = sel.xpath('//input[@id="hidJobName"]/@value').extract()[0].strip()
    zgrcrx_zwxq['address'] = sel.xpath('//div[@class="area-jobintro f_l"]/@title').extract()[0].strip()

    # 工作标签
    try:
        zgrcrx_zwxq['jobLabel'] = []
        for wel in sel.xpath('//div[@class="mdl-jobintro"]/ul[@class="taglist-jobintro clearfix"]/li'):
            zgrcrx_zwxq['jobLabel'].append(wel.xpath('string(.)').extract()[0].strip())
    except:
        pass

    # 工作描述
    try:
        for ll in sel.xpath('//div[@class="mdl-jobintro"]/ul[@class="require-jobintro clearfix"]/li'):
            l1str = ll.xpath('string(.)').extract()[0].replace('/', '').strip().replace('/', '')
            # print(l1str)
            if 'k' in l1str and '-' in l1str:
                zgrcrx_zwxq['salaryLower'] = int(l1str.split('-')[0].strip())*1000
                zgrcrx_zwxq['salaryUpper'] = int(l1str.split('-')[1].replace('k', '').strip())*1000
            elif 'k以' in l1str:
                zgrcrx_zwxq['salaryLower'] = int(l1str.split('k以')[0].strip())
                zgrcrx_zwxq['salaryUpper'] = int(l1str.split('k以')[0].strip())
            elif l1str[:2] in xl_li:
                zgrcrx_zwxq['degree'] = l1str[:2]
            elif '经验' in l1str:
                wy_str = l1str.split('年')[0].replace('经验', '')
                if '不限' in wy_str:
                    zgrcrx_zwxq['workExperienceLower'] = ''
                    zgrcrx_zwxq['workExperienceUpper'] = ''
                else:
                    wy_int = int(wy_str)
                    zgrcrx_zwxq['workExperienceLower'] = wy_int
                    zgrcrx_zwxq['workExperienceUpper'] = ''
            elif '人' in l1str:
                zgrcrx_zwxq['recruitmentSum'] = l1str.replace('人', '')
            elif ' ' in l1str:
                zgrcrx_zwxq['jobNature'] = l1str.aplit(' ')
            elif l1str in jn_li:
                zgrcrx_zwxq['jobNature'].append(l1str)
    except:
        traceback.print_exc()
        pass
    try:
        zgrcrx_zwxq['companyIndustry'] = sel.xpath('//a[@class="link-combscintro"]/text()').extract()[0].strip()
    except:
        pass
    try:
        scale_str = sel.xpath('//i[@class="icon-comscope"]/parent::li/text()').extract()[0].strip()
        scale_str = re.findall(r'(\d.+?)', scale_str)[0]
        zgrcrx_zwxq['companyScale'] = scale_str
    except:
        pass
    try:
        zgrcrx_zwxq['companyIndustry'] = []
        gshy_str = sel.xpath('//a[@class="link-combscintro"]/text()').extract()[0].strip()
        zgrcrx_zwxq['companyIndustry'].append(gshy_str)
    except:
        pass
    try:
        gsxz_str = sel.xpath('//i[@class="icon-comattr"]/parent::li/text()').extract()[0].strip()
        zgrcrx_zwxq['companyNature'] = gsxz_str
    except:
        pass
    # 详细地址
    try:
        zgrcrx_zwxq['addressDetail'] = sel.xpath('//input[@id="hidCompanyDizhi"]/@value').extract()[0].strip()
    except:
        pass
    try:
        desc_str = sel.xpath('string(//div[@class="coninfo-jobdesc"])').extract()[0].strip()
        zgrcrx_zwxq['jobDescription'] = desc_str.replace('\r', '').replace('\r\n', '').replace('\n', '').replace(' ', '')
    except:
        pass
    # print(zgrcrx_zwxq)
    return zgrcrx_zwxq
def zwjx_mm(text,compName,zw_data):
    mm_job_detail = {}
    mm_job_detail['companyName'] = compName
    mm_job_detail['jobLabel'] = []
    mm_job_detail['status'] = 1
    mm_job_detail['scrapy_state'] = 1
    mm_job_detail['channel'] = 17
    sel_jx = Selector(text=zw_data)
    # 工作名称：
    try:
        mm_job_detail["jobTitle"] = text['title'].replace("\u200b","").strip()
    except:
        traceback.print_exc()
        pass
    # 工作ID：
    # try:
        # mm_job_detail["id"] = str(text['positionId']).strip()
    # except:
    #     traceback.print_exc()
    #     pass
    # 刷新时间
    try:
        mm_job_detail["refreshTime"] =text['lastmod'].strip()
    except:
        traceback.print_exc()
        pass
    #地址
    try:
        mm_job_detail["address"]= text['location'].strip()
    except:
        traceback.print_exc()
        pass
    #职位标贴
    # try:
    #     if ',' in text['positionAdvantage']:
    #         jobLabel=text['positionAdvantage'].split(',')
    #     elif '、'in text['positionAdvantage']:
    #         jobLabel = text['positionAdvantage'].split('、')
    #     elif ' 'in text['positionAdvantage']:
    #         jobLabel = text['positionAdvantage'].split(' ')
    #     else:
    #         mm_job_detail['jobLabel'].append(text['positionAdvantage'])
    #     for wel in jobLabel:
    #         mm_job_detail['jobLabel'].append(wel.strip())
    #     if not mm_job_detail['jobLabel']:
    #         mm_job_detail['jobLabel'] = []
    # except:
        # traceback.print_exc()
        # pass
    #薪资
    try:
        salary= text['salary'].strip()
        if "面议" in salary:
            mm_job_detail["salaryLower"] = int(0)
            mm_job_detail["salaryUpper"] = int(0)
        elif "-" in salary:
            mm_job_detail["salaryLower"] = int(salary.split("-")[0].strip())
            mm_job_detail["salaryUpper"] = int(salary.split("-")[1].strip())
        elif "以" in salary:
            mm_job_detail["salaryLower"] = int(salary.split("以")[0].strip())
            mm_job_detail["salaryUpper"] = int(salary.split("以")[0].strip())
    except:
        traceback.print_exc()
        pass
    #工作性质
    try:
        mm_job_detail["jobNature"] = []
        jobNature=text["type"]
        mm_job_detail["jobNature"].append(jobNature)
    except:
        traceback.print_exc()
        pass

    #学历
    try:
        degree=text["education"]
        if "不限" in degree or "其他" in degree:
            mm_job_detail["degree"] = "不限"
        elif "以" in degree:
            mm_job_detail["degree"] = degree.split("以")[0].strip()
        else:
            mm_job_detail["degree"] = degree.strip()
    except:
        traceback.print_exc()
        pass
    # 经验
    try:
        workExperience = text["experience"]
        if "应届" in workExperience or "在读生" in workExperience:
            mm_job_detail["workExperienceLower"] = int(0)
            mm_job_detail["workExperienceUpper"] = int(0)
        elif "不限" in workExperience:
            mm_job_detail["workExperienceLower"] = ''
            mm_job_detail["workExperienceUpper"] = ''
        elif "1年以下" in workExperience:
            mm_job_detail["workExperienceLower"] = 0
            mm_job_detail["workExperienceUpper"] = 1
        elif "-" in workExperience:
            mm_job_detail["workExperienceLower"] = int(workExperience.split("-")[0].strip())
            mm_job_detail["workExperienceUpper"] = int(workExperience.split("-")[1].replace("年", "").strip())
        elif "以上" in workExperience:
            mm_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].strip())
            mm_job_detail["workExperienceUpper"] = ''
        else:
            mm_job_detail["workExperienceLower"] = int(workExperience.replace("年", "").strip())
            mm_job_detail["workExperienceUpper"] = int(workExperience.replace("年", "").strip())
    except:
        traceback.print_exc()
        pass
    #公司行业
    # try:
    #     companyIndustry=text["industryField"].split(',')
    #     mm_job_detail["companyIndustry"] = []
    #     for wel in companyIndustry:
    #         mm_job_detail['companyIndustry'].append(wel.strip())
    #     if not mm_job_detail['companyIndustry']:
    #         mm_job_detail['companyIndustry'] = []
    # except:
    #     traceback.print_exc()
    #     pass
    #公司规模
    # try:
    #     mm_job_detail["companyScale"] = text['companySize'].strip()
    # except:
    #     traceback.print_exc()
    #     pass

    # 职位类别
    try:
        mm_job_detail["jobCategory"] = text['jobfirstclass'].strip()
    except:
        traceback.print_exc()
        pass
    #公司介绍
    try:
        mm_job_detail["companyIntroduction"] = text['companydescription'].replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "").strip()
    except:
        traceback.print_exc()
        pass

    #职位描述
    try:
        jobDescription=sel_jx.xpath('string(//div[@class="job-description"]/div/p)').extract()[0].strip()
        mm_job_detail["jobDescription"] = jobDescription.replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("\ufeff","").replace("\xa0","")
    except:
        traceback.print_exc()
        pass
    # 详细地址
    try:
        addressDetail=sel_jx.xpath('string(//div[@class="job-addr"]/p[2])').extract()[0].strip()
        mm_job_detail["addressDetail"] = addressDetail.replace("\r", "").replace("\n","").replace("\t", "").replace(" ", "").replace("查看地图","").strip()
    except:
        traceback.print_exc()
        pass
    return mm_job_detail
def zwjx_nt(text, compName):
    nt_job_detail = {}
    nt_job_detail['companyName'] = compName
    sel_jx = Selector(text=text)
    #nt_job_detail['jobLabel'] = []                  # 职位标贴
    nt_job_detail['status'] = 1
    nt_job_detail['channel'] = 9
    #工作名称：
    try:
        jobTitle= sel_jx.xpath('string(//div[@class="c333 font26"])').extract()[0].strip()
        nt_job_detail["jobTitle"] = jobTitle.split("】")[-1].strip()
    except:
        traceback.print_exc()
        pass
    #工作ID：
    try:
        jobId = sel_jx.xpath('string(//ul[@class="nav navbar-nav pull-right"]/li[2]/a[1]/@href)').extract()[0].strip()
        nt_job_detail["id"] = jobId.split("j%2F")[1].strip()
    except:
        traceback.print_exc()
        pass
    #刷新时间
    try:
        refreshTime=sel_jx.xpath('string(//div[@class="col-sm-8 main"]/div[@class="mt10"]/span)').extract()[0].strip()
        nt_job_detail["refreshTime"] ="2018-"+ refreshTime.replace("发布","").strip()
    except:
        traceback.print_exc()
        pass
    #职位类别
    nt_job_detail["jobNature"] =["全职"]
    #职位描述
    try:
        jobDescription = sel_jx.xpath('string(//div[@class="mb20 jobdetailcon"])').extract()[0].strip()
        nt_job_detail["jobDescription"] = jobDescription.replace("\r", "").replace("\n","").replace("\t","").replace(" ","").replace('\xa0','').strip()
    except:
        traceback.print_exc()
        pass
    #公司行业
    try:
        nt_job_detail["companyIndustry"] =[sel_jx.xpath('string(//div[@class="col-xs-8"]/div[1])').extract()[0].strip()]
    except:
        traceback.print_exc()
        pass
    #公司性质
    try:
        nt_job_detail["companyNature"] = sel_jx.xpath('string(//div[@class="col-xs-8"]/div[2])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    #公司规模
    try:
        nt_job_detail["companyScale"] = sel_jx.xpath('string(//div[@class="col-xs-8"]/div[3])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    #工作详细地址
    try:
        nt_job_detail["addressDetail"] = sel_jx.xpath('string(//div[@class="col-md-4 sider pl25"]/div[3])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    #薪资
    try:
        salary=sel_jx.xpath('string(//span[@class="orange mr10"])').extract()[0].strip()
        if "面议" in salary:
            nt_job_detail["salaryLower"] = int(0)
            nt_job_detail["salaryUpper"] = int(0)
        elif "-" in salary:
            nt_job_detail["salaryLower"] = int(salary.replace("k","").split("-")[0].strip())*1000
            nt_job_detail["salaryUpper"] = int(salary.replace("k","").split("-")[1].strip())*1000
        elif "以" in salary:
            nt_job_detail["salaryLower"] = int(salary.replace("k","").split("以")[0].strip())*1000
            nt_job_detail["salaryUpper"] = int(salary.replace("k","").split("以")[0].strip())*1000
    except:
        traceback.print_exc()
        pass
    #工作经验
    try:
        workExperience = sel_jx.xpath('string(//div[@class="font16 mt10 mb10"]/span[@data-default="年限不限"])').extract()[0].strip()
        if "应届" in workExperience or '-1年' in workExperience:
            nt_job_detail["workExperienceLower"] = 0
            nt_job_detail["workExperienceUpper"] = 0
        elif "不限" in workExperience or "-年" in workExperience:
            nt_job_detail["workExperienceLower"] = ''
            nt_job_detail["workExperienceUpper"] = ''

        elif "年" in workExperience:
                if "-" in workExperience:
                    nt_job_detail["workExperienceLower"] = int(workExperience.replace("年","").split("-")[0].strip())
                    nt_job_detail["workExperienceUpper"] = int(workExperience.replace("年","").split("-")[1].strip())
                elif "以上" in workExperience:
                    nt_job_detail["workExperienceLower"] = int(workExperience.split("年")[0].strip())
                    nt_job_detail["workExperienceUpper"] = ''
    except:
        traceback.print_exc()
        pass
    #学历
    try:
        degree=sel_jx.xpath('string(//div[@class="font16 mt10 mb10"]/span[@data-default="学历不限"])').extract()[0].strip()
        if degree == "":
            nt_job_detail["degree"] = "不限"
        else:
            nt_job_detail["degree"] = degree
    except:
        traceback.print_exc()
        pass
    #工作地址
    try:
        nt_job_detail["address"] = sel_jx.xpath('string(//div[@class="font16 mt10 mb10"]/span[@class="mr10"][3])').extract()[0].strip()
    except:
        traceback.print_exc()
        pass
    #招聘人数、职位类别、职位标贴、公司介绍
    return nt_job_detail

def get_zlzw(compName, provName, cityName, countyName,cityName_0, channelid=1):
    dict_city={'广安': {'code': '814'}, '五家渠': {'code': '10178'}, '鸡西': {'code': '624'}, '阿勒泰': {'code': '903'}, '西平': {'code': '10059'}, '呼和浩特': {'code': '587'}, '辽阳': {'code': '608'}, '淮安': {'code': '643'}, '聊城': {'code': '716'}, '肇东': {'code': '10510'}, '重庆': {'code': '551', 'sublist': {'丰都县': '2342', '长寿区': '2325', '酉阳县': '2350', '双桥区': '2328', '綦江县': '2336', '巫山县': '2344', '荣昌县': '2331', '重庆': '551', '秀山土家族苗族自治县': '2434', '九龙坡区': '2316', '南岸区': '2314', '秀山县': '2349', '北部新区': '2360', '永川区': '2323', '渝中区': '2312', '武隆县': '2347', '南川区': '2330', '万盛区': '2329', '云阳县': '2339', '石柱土家族自治县': '2433', '大渡口区': '2317', '黔江区': '2322', '彭水苗族土家族自治县': '2436', '江北区': '2313', '潼南县': '2335', '沙坪坝区': '2315', '大足县': '2332', '奉节县': '2343', '渝北区': '2318', '江津区': '2326', '壁山县': '2333', '忠县': '2337', '合川区': '2327', '北碚区': '2320', '城口县': '2346', '开县': '2338', '铜梁县': '2334', '酉阳土家族苗族自治县': '2435', '石柱县': '2348', '彭水县': '2351', '梁平县': '2340', '巫溪县': '2345', '涪陵区': '2324', '垫江县': '2341', '巴南区': '2319', '万州区': '2321'}}, '衢州': {'code': '660'}, '阿坝藏族羌族自治州': {'code': '819'}, '孝感': {'code': '743'}, '威海': {'code': '711'}, '运城': {'code': '583'}, '淮南': {'code': '667'}, '河南': {'code': '545'}, '平度': {'code': '10173'}, '日本': {'code': '505'}, '公主岭': {'code': '10122'}, '鹤山': {'code': '10138'}, '锦州': {'code': '605'}, '十堰': {'code': '738'}, '台山': {'code': '10112'}, '晋江': {'code': '10148'}, '三亚': {'code': '800'}, '海北藏族自治州': {'code': '880'}, '盱眙': {'code': '10152'}, '德宏傣族景颇族自治州': {'code': '842'}, '迪庆藏族自治州': {'code': '845'}, '瑞典': {'code': '521'}, '德国': {'code': '496'}, '大庆': {'code': '627'}, '加拿大': {'code': '488'}, '黄岛': {'code': '10026'}, '厦门': {'code': '682', 'sublist': {'海沧区': '2267', '集美区': '2266', '翔安区': '2269', '厦门': '682', '思明区': '2264', '湖里区': '2265', '同安区': '2268'}}, '西安': {'code': '854', 'sublist': {'蓝田县': '2079', '西安': '854', '周至县': '2080', '沣渭新区': '2083', '新城区': '2070', '高新技术产业开发区': '2368', '阎良区': '2077', '雁塔区': '2073', '曲江新区': '2370', '浐灞生态区': '2371', '西安国家民用航天产业基地': '2373', '长安区': '2076', '户县': '2081', '未央区': '2074', '经济技术开发区': '2369', '灞桥区': '2075', '莲湖区': '2072', '临潼区': '2078', '高陵县': '2082', '阎良国家航空高新技术产业基地': '2372', '国际港务区': '2374', '碑林区': '2071'}}, '南非': {'code': '519'}, '平顶山': {'code': '722'}, '香河': {'code': '10167'}, '东方': {'code': '10187'}, '开原': {'code': '10144'}, '希腊': {'code': '497'}, '镇江': {'code': '646'}, '阿根廷': {'code': '481'}, '宁夏': {'code': '559'}, '焦作': {'code': '726'}, '上海': {'code': '538', 'sublist': {'奉贤区': '2035', '闸北区': '2025', '松江区': '2033', '宝山区': '2029', '浦东新区': '2031', '金山区': '2032', '杨浦区': '2027', '闵行区': '2028', '普陀区': '2024', '青浦区': '2034', '虹口区': '2026', '黄浦区': '2019', '上海': '538', '徐汇区': '2021', '崇明县': '2036', '长宁区': '2022', '静安区': '2023', '嘉定区': '2030'}}, '澄迈': {'code': '10190'}, '成都': {'code': '801', 'sublist': {'金牛区': '2109', '武侯区': '2110', '彭州市': '2379', '邛崃市': '2377', '新都区': '2114', '青羊区': '2107', '青白江区': '2113', '蒲江县': '2120', '锦江区': '2108', '成都': '801', '大邑县': '2119', '双流县': '2116', '崇州市': '2378', '成华区': '2111', '都江堰市': '2380', '金堂县': '2118', '高新区': '2381', '温江区': '2115', '新津县': '2121', '郫县': '2117', '龙泉驿区': '2112'}}, '烟台': {'code': '707', 'sublist': {'烟台': '707', '海阳市': '2556', '芝罘区': '2545', '牟平区': '2547', '龙口市': '2550', '蓬莱市': '2553', '福山区': '2546', '莱阳市': '2551', '莱州市': '2552', '开发区': '2558', '莱山区': '2548', '栖霞市': '2555', '长岛县': '2549', '高新区': '2557', '招远市': '2554'}}, '汉中': {'code': '860'}, '公安': {'code': '10057'}, '常德': {'code': '755'}, '德州': {'code': '715'}, '岳阳': {'code': '754'}, '玉林': {'code': '793'}, '萍乡': {'code': '693'}, '江西': {'code': '543'}, '沙特阿拉伯': {'code': '517'}, '尚志': {'code': '10160'}, '上虞': {'code': '10130'}, '方家山': {'code': '10158'}, '象山': {'code': '10154'}, '宜昌': {'code': '739'}, '潍坊': {'code': '708'}, '邯郸': {'code': '568'}, '汕头': {'code': '767'}, '云南': {'code': '554'}, '洛阳': {'code': '721'}, '喀什': {'code': '899'}, '万宁': {'code': '10186'}, '海口': {'code': '799'}, '松原': {'code': '619'}, '乐清': {'code': '10089'}, '黔东南苗族侗族自治州': {'code': '829'}, '莱芜': {'code': '713'}, '尼日利亚': {'code': '915'}, '兰州': {'code': '864'}, '巴中': {'code': '817'}, '菏泽': {'code': '718'}, '南阳': {'code': '731'}, '本溪': {'code': '603'}, '三明': {'code': '684'}, '丹东': {'code': '604'}, '朝阳': {'code': '611'}, '兴城': {'code': '10023'}, '余姚': {'code': '10085'}, '鹰潭': {'code': '696'}, '马来西亚': {'code': '508'}, '常州': {'code': '638'}, '乐山': {'code': '810'}, '南充': {'code': '811'}, '通化': {'code': '617'}, '永嘉': {'code': '10091'}, '宜春': {'code': '699'}, '四川': {'code': '552'}, '九江': {'code': '694'}, '西宁': {'code': '878'}, '如皋': {'code': '10051'}, '梧州': {'code': '788'}, '百色': {'code': '794'}, '七台河': {'code': '630'}, '宣城': {'code': '680'}, '拉萨': {'code': '847'}, '英国': {'code': '527'}, '果洛藏族自治州': {'code': '883'}, '吉林': {'code': '614'}, '北海': {'code': '789'}, '贵阳': {'code': '822', 'sublist': {'南明区': '2522', '清镇市': '2527', '息烽县': '2529', '白云区': '2525', '贵阳': '822', '乌当区': '2526', '开阳县': '2530', '修文县': '2528', '观山湖区（金阳新区）': '2524', '花溪区': '2523', '云岩区': '2521'}}, '燕郊开发区': {'code': '10050'}, '加纳': {'code': '914'}, '信阳': {'code': '733'}, '宁德': {'code': '690'}, '神农架': {'code': '10179'}, '黄石': {'code': '737'}, '池州': {'code': '679'}, '临沂': {'code': '714'}, '即墨': {'code': '10097'}, '内江': {'code': '809'}, '印度': {'code': '500'}, '固安': {'code': '10142'}, '广德': {'code': '10181'}, '保山': {'code': '834'}, '抚州': {'code': '700'}, '牡丹江': {'code': '631'}, '泉港区': {'code': '686'}, '乌海': {'code': '589'}, '乌克兰': {'code': '525'}, '绥芬河': {'code': '10161'}, '黑龙江': {'code': '537'}, '溧阳': {'code': '10150'}, '山西': {'code': '533'}, '泉州': {'code': '685'}, '晋城': {'code': '580'}, '其他': {'code': '512'}, '临汾': {'code': '585'}, '防城港': {'code': '790'}, '中卫': {'code': '906'}, '琼海': {'code': '10153'}, '秦皇岛': {'code': '567'}, '荣成': {'code': '912'}, '葡萄牙': {'code': '515'}, '鹤岗': {'code': '625'}, '南通': {'code': '641'}, '巴音郭楞蒙古自治州': {'code': '896'}, '湖南': {'code': '547'}, '长葛': {'code': '10137'}, '阿联酋': {'code': '526'}, '银川': {'code': '886'}, '杨凌': {'code': '10470'}, '石河子': {'code': '10061'}, '张家港': {'code': '652'}, '连云港': {'code': '642'}, '广东': {'code': '548'}, '安阳': {'code': '723'}, '双鸭山': {'code': '626'}, '匈牙利': {'code': '498'}, '温州': {'code': '655'}, '榆林': {'code': '861'}, '永济': {'code': '910'}, '徐州': {'code': '637'}, '驻马店': {'code': '735'}, '奎屯': {'code': '10164'}, '中山': {'code': '780'}, '邢台': {'code': '569'}, '陵水黎族自治县': {'code': '10197'}, '凤阳': {'code': '10069'}, '张掖': {'code': '870'}, '科威特': {'code': '507'}, '满洲里': {'code': '10157'}, '南平': {'code': '688'}, '白山': {'code': '618'}, '蚌埠': {'code': '666'}, '黄冈': {'code': '745'}, '河源': {'code': '776'}, '阿拉善盟': {'code': '598'}, '黑河': {'code': '632'}, '海宁': {'code': '10133'}, '衡阳': {'code': '752'}, '宝鸡': {'code': '856'}, '保加利亚': {'code': '487'}, '桐乡': {'code': '10127'}, '莱西': {'code': '10174'}, '潮州': {'code': '781'}, '南京': {'code': '635', 'sublist': {'雨花台区': '2093', '高淳县': '2096', '建邺区': '2087', '栖霞区': '2092', '六合区': '2091', '南京': '635', '鼓楼区': '2088', '秦淮区': '2086', '玄武区': '2084', '江宁区': '2094', '溧水县': '2095', '浦口区': '2090'}}, '乌鲁木齐': {'code': '890'}, '齐齐哈尔': {'code': '623'}, '清远': {'code': '778'}, '阿拉尔': {'code': '10176'}, '新加坡': {'code': '518'}, '黄南藏族自治州': {'code': '881'}, '玉溪': {'code': '833'}, '太仓': {'code': '911'}, '乳山': {'code': '10060'}, '哈尔滨': {'code': '622', 'sublist': {'平房区': '2275', '香坊区': '2273', '道里区': '2271', '松北区': '2274', '阿城区': '2277', '通河县': '2431', '宾县': '2428', '依兰县': '2427', '巴彦县': '2429', '呼兰区': '2276', '哈尔滨': '622', '道外区': '2272', '五常市': '2424', '南岗区': '2270', '木兰县': '2430', '方正县': '2426', '延寿县': '2432'}}, '达州': {'code': '815'}, '贵港': {'code': '792'}, '平湖': {'code': '10052'}, '和田': {'code': '900'}, '抚顺': {'code': '602'}, '宁波': {'code': '654', 'sublist': {'江北区': '3005', '海曙区': '3003', '宁海县': '3372', '江东区': '3004', '北仑区': '3006', '象山县': '3373', '慈溪市': '3370', '奉化区': '3001', '高新区': '3008', '镇海区': '3007', '余姚市': '3371', '鄞州区': '3002'}}, '兴安盟': {'code': '594'}, '济南': {'code': '702', 'sublist': {'平阴县': '2103', '商河县': '2105', '济阳县': '2104', '长清区': '2102', '章丘市': '2471', '济南': '702', '天桥区': '2099', '历下区': '2098', '高新区': '2376', '历城区': '2101', '槐荫区': '2100', '市中区': '2097'}}, '福安': {'code': '10020'}, '鹤壁': {'code': '724'}, '临高': {'code': '10191'}, '潜江': {'code': '10169'}, '慈溪': {'code': '10086'}, '陇南': {'code': '875'}, '胶南': {'code': '10172'}, '漯河': {'code': '729'}, '许昌': {'code': '728'}, '保亭黎族苗族自治县': {'code': '10193'}, '韶关': {'code': '764'}, '茂名': {'code': '771'}, '义乌': {'code': '10004'}, '自贡': {'code': '802'}, '遂宁': {'code': '808'}, '龙川': {'code': '10120'}, '日喀则': {'code': '850'}, '捷克': {'code': '491'}, '株洲': {'code': '750'}, '新余': {'code': '695'}, '吕梁': {'code': '586'}, '比利时': {'code': '485'}, '塞浦路斯': {'code': '490'}, '舟山': {'code': '661'}, '和顺': {'code': '10082'}, '双城': {'code': '10159'}, '柳州': {'code': '786'}, '东阳': {'code': '10056'}, '马鞍山': {'code': '668'}, '咸阳': {'code': '857'}, '周口': {'code': '734'}, '海西蒙古族藏族自治州': {'code': '885'}, '绵阳': {'code': '806'}, '湘西土家族苗族自治州': {'code': '762'}, '温岭': {'code': '10129'}, '扬中': {'code': '10124'}, '昭通': {'code': '835'}, '意大利': {'code': '504'}, '荷兰': {'code': '509'}, '宜城': {'code': '10171'}, '杭州': {'code': '653', 'sublist': {'上城区': '2233', '淳安县': '2242', '余杭区': '2240', '拱墅区': '2236', '萧山区': '2239', '下沙': '2457', '西湖区': '2237', '江干区': '2235', '临安市': '2479', '杭州': '653', '桐庐县': '2241', '建德市': '2409', '富阳市': '2478', '滨江区': '2238', '下城区': '2234'}}, '洋浦': {'code': '907'}, '河池': {'code': '796'}, '乌苏': {'code': '10166'}, '保定': {'code': '570'}, '爱尔兰': {'code': '502'}, '越南': {'code': '529'}, '永州': {'code': '759'}, '石家庄': {'code': '565', 'sublist': {'赞皇县': '2419', '桥东区': '2289', '平山县': '2301', '井陉县': '2420', '赵县': '2417', '深泽县': '2415', '长安区': '2288', '元氏县': '2302', '石家庄': '565', '鹿泉市': '2299', '桥西区': '2290', '裕华区': '2292', '无极县': '2416', '新乐市': '2298', '正定县': '2300', '晋州市': '2297', '高邑县': '2418', '井陉矿区': '2294', '新华区': '2291', '藁城市': '2296', '东开发区': '2293', '栾城县': '2412', '灵寿县': '2414', '辛集市': '2295', '行唐县': '2413'}}, '哈密': {'code': '893'}, '西藏': {'code': '555'}, '瑞安': {'code': '10128'}, '宿迁': {'code': '648'}, '三河': {'code': '10170'}, '黔南布依族苗族自治州': {'code': '830'}, '钦州': {'code': '791'}, '海阳': {'code': '10146'}, '金华': {'code': '659'}, '挪威': {'code': '511'}, '眉山': {'code': '812'}, '惠州': {'code': '773', 'sublist': {'惠阳区': '2247', '仲恺区': '3253', '博罗县': '3255', '龙门县': '3257', '惠城区': '2246', '大亚湾区': '3254', '惠东县': '3256'}}, '乌兰察布': {'code': '596'}, '泸州': {'code': '804'}, '西班牙': {'code': '520'}, '六盘水': {'code': '823'}, '冰岛': {'code': '499'}, '郑州': {'code': '719', 'sublist': {'郑东新区 ': '2199', '管城区': '2196', '经开区': '2203', '荥阳市': '2402', '新郑市': '2399', '金水区': '2197', '航空港区': '2445', '郑州': '719', '巩义市': '2444', '新密市': '2401', '上街区': '2205', '登封市': '2400', '中原区': '2194', '惠济区': '2198', '高新区': '2204', '二七区': '2195', '中牟县': '2403'}}, '吴忠': {'code': '888'}, '武穴': {'code': '10139'}, '晋中': {'code': '582'}, '济宁': {'code': '709'}, '漳州': {'code': '687'}, '辽宁': {'code': '535'}, '赣州': {'code': '697'}, '龙岩': {'code': '689'}, '阜新': {'code': '607'}, '兴平': {'code': '10058'}, '淄博': {'code': '704'}, '三门': {'code': '10145'}, '忻州': {'code': '584'}, '廊坊': {'code': '574'}, '塞内加尔': {'code': '919'}, '衡水': {'code': '575'}, '泰兴': {'code': '10149'}, '美国': {'code': '528'}, '文昌': {'code': '10185'}, '朔州': {'code': '581'}, '庆阳': {'code': '873'}, '江门': {'code': '769'}, '芬兰': {'code': '494'}, '新疆': {'code': '560'}, '淮北': {'code': '669'}, '定西': {'code': '874'}, '呼伦贝尔': {'code': '593'}, '宿州': {'code': '675'}, '莆田': {'code': '683'}, '天门': {'code': '10140'}, '伊春': {'code': '628'}, '滁州': {'code': '673'}, '宜宾': {'code': '813'}, '铜陵': {'code': '670'}, '红河哈尼族彝族自治州': {'code': '837'}, '阿克苏': {'code': '897'}, '渭南': {'code': '858'}, '湛江': {'code': '770'}, '定安': {'code': '10188'}, '吐鲁番': {'code': '892'}, '鄂尔多斯': {'code': '592'}, '昆明': {'code': '831'}, '陕西': {'code': '556'}, '武威': {'code': '869'}, '永康': {'code': '10055'}, '新西兰': {'code': '510'}, '德阳': {'code': '805'}, '资阳': {'code': '818'}, '通州': {'code': '10155'}, '城阳': {'code': '10096'}, '内蒙古': {'code': '534'}, '高邮': {'code': '10126'}, '句容': {'code': '10028'}, '思茅': {'code': '839'}, '以色列': {'code': '503'}, '金湖': {'code': '10175'}, '法国': {'code': '495'}, '武汉': {'code': '736', 'sublist': {'黄陂区': '2068', '武汉吴家山经济技术开发区': '2367', '江汉区': '2058', '蔡甸区': '2064', '东西湖区': '2065', '江岸区': '2057', '武昌区': '2061', '汉阳区': '2060', '青山区': '2062', '武汉经济技术开发区': '2365', '汉南区': '2066', '洪山区': '2063', '新洲区': '2069', '江夏区': '2067', '东湖新技术开发区': '2366', '硚口区': '2059', '武汉': '736'}}, '海东': {'code': '879'}, '昌江黎族自治县': {'code': '10195'}, '长治': {'code': '579'}, '全国': {'code': '489'}, '湖州': {'code': '657'}, '雅安': {'code': '816'}, '湖北': {'code': '546'}, '江阴': {'code': '651'}, '泰国': {'code': '523'}, '新乡': {'code': '725'}, '克拉玛依': {'code': '891'}, '赤峰': {'code': '590'}, '波兰': {'code': '514'}, '葫芦岛': {'code': '612'}, '埃及': {'code': '493'}, '图木舒克': {'code': '10177'}, '肥城': {'code': '10099'}, '石嘴山': {'code': '887'}, '江苏': {'code': '539'}, '普宁': {'code': '10113'}, '佳木斯': {'code': '629'}, '那曲': {'code': '851'}, '宿松': {'code': '10182'}, '开封': {'code': '720'}, '广元': {'code': '807'}, '天水': {'code': '868'}, '林芝': {'code': '853'}, '昌吉回族自治州': {'code': '894'}, '深圳': {'code': '765', 'sublist': {'南山区': '2039', '龙岗区': '2042', '福田区': '2037', '深圳': '765', '光明新区': '2044', '坪山新区': '2043', '宝安区': '2041', '罗湖区': '2038', '盐田区': '2040', '大鹏新区': '2362', '龙华新区': '2361'}}, '遵化': {'code': '10143'}, '印度尼西亚': {'code': '501'}, '盘锦': {'code': '609'}, '延安': {'code': '859'}, '甘肃': {'code': '557'}, '大理白族自治州': {'code': '841'}, '长沙': {'code': '749', 'sublist': {'长沙县': '2406', '长沙': '749', '浏阳市': '2408', '天心区': '2225', '雨花区': '2228', '宁乡县': '2407', '芙蓉区': '2224', '岳麓区': '2226', '开福区': '2227', '望城区': '2405'}}, '丹阳': {'code': '10114'}, '汕尾': {'code': '775'}, '盐城': {'code': '644'}, '胶州': {'code': '10156'}, '瑞士': {'code': '522'}, '郴州': {'code': '758'}, '合肥': {'code': '664', 'sublist': {'新站综合开发试验区': '2358', '庐阳区': '2352', '蜀山区': '2354', '经济技术开发区': '2356', '滨湖新区': '2357', '瑶海区': '2353', '政务文化新区': '2437', '高新区': '2359', '包河区': '2355', '北城新区': '2438', '合肥': '664'}}, '诸暨': {'code': '10131'}, '商丘': {'code': '732'}, '奥地利': {'code': '483'}, '东营': {'code': '706'}, '安哥拉': {'code': '913'}, '三门峡': {'code': '730'}, '南沙开发区': {'code': '10117'}, '无锡': {'code': '636', 'sublist': {'滨湖区': '2517', '崇安区': '2514', '宜兴市': '2513', '锡山区': '2520', '惠山区': '2519', '无锡新区': '2518', '南长区': '2515', '江阴市': '2512', '北塘区': '2516'}}, '铜川': {'code': '855'}, '嘉善': {'code': '10067'}, '香港': {'code': '561'}, '阿里': {'code': '852'}, '襄阳': {'code': '740'}, '安庆': {'code': '671'}, '俄罗斯联邦': {'code': '516'}, '常熟': {'code': '650'}, '崇左': {'code': '905'}, '河北': {'code': '532'}, '恩施土家族苗族自治州': {'code': '748'}, '巴基斯坦': {'code': '513'}, '邵阳': {'code': '753'}, '福州': {'code': '681', 'sublist': {'平潭县': '2261', '闽清县': '2260', '连江县': '2258', '闽侯县': '2256', '福清': '2473', '永泰县': '2259', '马尾区': '2254', '鼓楼区': '2251', '仓山区': '2253', '长乐': '2472', '晋安区': '2255', '台江区': '2252', '罗源县': '2257', '福州': '681'}}, '沧州': {'code': '573'}, '克孜勒苏柯尔克孜自治州': {'code': '898'}, '阳江': {'code': '777'}, '临夏回族自治州': {'code': '876'}, '辽源': {'code': '616'}, '乐东黎族自治县': {'code': '10196'}, '大同': {'code': '577'}, '张家界': {'code': '756'}, '南宁': {'code': '785'}, '荆门': {'code': '742'}, '浙江': {'code': '540'}, '屯昌': {'code': '10189'}, '开平': {'code': '10118'}, '昌图': {'code': '10080'}, '张家口': {'code': '571'}, '贵州': {'code': '553'}, '金昌': {'code': '866'}, '五指山': {'code': '10184'}, '丹麦': {'code': '492'}, '嘉兴': {'code': '656'}, '贺州': {'code': '795'}, '丽水': {'code': '663'}, '酒泉': {'code': '872'}, '平凉': {'code': '871'}, '肇庆': {'code': '772'}, '沈阳': {'code': '599', 'sublist': {'新民市': '2383', '皇姑区': '2128', '于洪区': '2133', '沈阳': '599', '辽中县': '2384', '沈北新区': '2134', '大东区': '2129', '铁西区': '2130', '康平县': '2385', '棋盘山开发区': '2382', '法库县': '2386', '东陵区（浑南新区）': '2132', '和平区': '2126', '沈河区': '2127', '苏家屯区': '2135'}}, '攀枝花': {'code': '803'}, '吉林': {'code': '536'}, '柬埔寨': {'code': '930'}, '台湾省': {'code': '563'}, '绍兴': {'code': '658'}, '承德': {'code': '572'}, '鄂州': {'code': '741'}, '南昌': {'code': '691', 'sublist': {'青山湖区': '2539', '西湖区': '2537', '南昌': '691', '安义县': '2544', '南昌县': '2541', '新建县': '2542', '东湖区': '2536', '进贤县': '2543', '青云谱区': '2538', '湾里区': '2540'}}, '大连': {'code': '600', 'sublist': {'大连': '600', '庄河市': '2396', '甘井子区': '2184', '中山区': '2182', '沙河口区': '2183', '瓦房店市': '2395', '西岗区': '2181', '长海县': '2397', '金州区 ': '2188', '开发区': '2186', '旅顺口区': '2187', '高新园区': '2185', '长兴岛': '2398', '普兰店市': '2394'}}, '四平': {'code': '615'}, '包头': {'code': '588'}, '儋州': {'code': '10183'}, '嘉峪关': {'code': '865'}, '昌都': {'code': '848'}, '巴西': {'code': '486'}, '玉树藏族自治州': {'code': '884'}, '巴彦淖尔': {'code': '597'}, '白银': {'code': '867'}, '铁岭': {'code': '610'}, '广西': {'code': '549'}, '澳大利亚': {'code': '482'}, '济源': {'code': '10044'}, '玉环县': {'code': '909'}, '白沙黎族自治县': {'code': '10194'}, '伊犁哈萨克自治州': {'code': '901'}, '濮阳': {'code': '727'}, '唐山': {'code': '566'}, '曲靖': {'code': '832'}, '娄底': {'code': '761'}, '安徽': {'code': '541'}, '延边朝鲜族自治州': {'code': '621'}, '青岛': {'code': '703', 'sublist': {'胶州市': '2160', '即墨市': '2161', '平度市': '2162', '保税区': '2391', '城阳区': '2159', '市南区': '2153', '青岛': '703', '市北区（新行政区）': '2154', '黄岛区（新行政区）': '2157', '青岛高新技术产业开发区': '2393', '崂山区': '2158', '青岛经济技术开发区': '2392', '李沧区': '2156', '莱西市': '2164'}}, '咸宁': {'code': '746'}, '简阳': {'code': '10201'}, '峨眉': {'code': '10065'}, '韩国': {'code': '506'}, '亳州': {'code': '678'}, '海南': {'code': '550'}, '坦桑尼亚': {'code': '916'}, '山东': {'code': '544'}, '普洱': {'code': '10163'}, '梅州': {'code': '774'}, '靖江': {'code': '649'}, '广州': {'code': '763', 'sublist': {'越秀区': '2045', '天河区': '2048', '广州': '763', '白云区': '2049', '花都区': '2051', '海珠区': '2046', '萝岗区': '2053', '黄埔区': '2050', '番禺区': '2052', '荔湾区': '2047', '增城': '2475', '南沙区': '2054', '从化': '2474'}}, '长春': {'code': '613', 'sublist': {'经济开发区': '2146', '农安县': '2390', '长春': '613', '双阳区': '2148', '南关区': '2140', '高新开发区': '2145', '榆树市': '2387', '朝阳区': '2142', '二道区': '2143', '汽车产业开发区': '2147', '九台市': '2388', '德惠市': '2389', '绿园区': '2144', '宽城区': '2141'}}, '滨州': {'code': '717'}, '珠海': {'code': '766'}, '博尔塔拉蒙古自治州': {'code': '895'}, '佛山': {'code': '768', 'sublist': {'顺德区': '2560', '三水区': '2534', '佛山': '768', '禅城区': '2531', '南海区': '2562', '高明区': '2535'}}, '阜阳': {'code': '674'}, '国外': {'code': '480'}, '凉山彝族自治州': {'code': '821'}, '澳门': {'code': '562'}, '荆州': {'code': '744'}, '安顺': {'code': '825'}, '北京': {'code': '530', 'sublist': {'门头沟区': '2016', '北京': '530', '平谷区': '2015', '石景山区': '2008', '延庆县': '2018', '朝阳区': '2006', '丰台区': '2007', '房山区': '2011', '大兴区': '2012', '东城区': '2001', '怀柔区': '2014', '通州区': '2009', '崇文区': '2003', '海淀区': '2005', '昌平区': '2013', '密云县': '2017', '宣武区': '2004', '西城区': '2002', '顺义区': '2010'}}, '益阳': {'code': '757'}, '台州': {'code': '662'}, '黔西南布依族苗族自治州': {'code': '827'}, '云浮': {'code': '783'}, '宁海': {'code': '10134'}, '乌干达': {'code': '917'}, '昆山': {'code': '640'}, '塔城': {'code': '902'}, '兖州': {'code': '10116'}, '龙泉': {'code': '10180'}, '泰安': {'code': '710'}, '太原': {'code': '576', 'sublist': {'万柏林区': '2505', '晋源区': '2506', '清徐县': '2507', '古交市': '2510', '尖草坪区': '2504', '杏花岭区': '2503', '迎泽区': '2502', '太原': '576', '小店区': '2501', '娄烦县': '2509', '阳曲县': '2508'}}, '锡林郭勒盟': {'code': '595'}, '阳泉': {'code': '578'}, '上饶': {'code': '701'}, '六安': {'code': '677'}, '黄山': {'code': '672'}, '琼中黎族苗族自治县': {'code': '10192'}, '山南': {'code': '849'}, '固原': {'code': '889'}, '扬州': {'code': '645'}, '来宾': {'code': '904'}, '毕节': {'code': '828'}, '吉安': {'code': '698'}, '青海': {'code': '558'}, '揭阳': {'code': '782'}, '怀化': {'code': '760'}, '海南藏族自治州': {'code': '882'}, '苏州': {'code': '639', 'sublist': {'工业园区': '2218', '吴江区': '2561', '姑苏区': '2511', '吴中区': '2216', '高新区': '2404', '虎丘区': '2215', '苏州': '639', '相城区': '2217'}}, '土耳其': {'code': '524'}, '东莞': {'code': '779'}, '启东': {'code': '10136'}, '商洛': {'code': '863'}, '泰州': {'code': '647'}, '天津': {'code': '531', 'sublist': {'武清区': '2176', '东丽区': '2172', '北辰区': '2175', '津南区': '2174', '蓟县': '2180', '宝坻区': '2177', '西青区': '2173', '静海县': '2178', '宁河县': '2179', '和平区': '2165', '南开区': '2168', '河北区': '2169', '天津': '531', '河东区': '2166', '滨海新区': '2171', '红桥区': '2170', '河西区': '2167'}}, '西双版纳傣族自治州': {'code': '840'}, '日照': {'code': '712'}, '楚雄彝族自治州': {'code': '836'}, '甘南藏族自治州': {'code': '877'}, '仙桃': {'code': '10168'}, '福建': {'code': '542'}, '巢湖': {'code': '676'}, '遵义': {'code': '824'}, '绥化': {'code': '633'}, '西昌': {'code': '10104'}, '鞍山': {'code': '601'}, '宜兴': {'code': '10049'}, '景德镇': {'code': '692'}, '乌审旗': {'code': '10031'}, '安达': {'code': '10081'}, '枣庄': {'code': '705'}, '白俄罗斯': {'code': '484'}, '临沧': {'code': '846'}, '大兴安岭': {'code': '634'}, '德清': {'code': '10151'}, '文山壮族苗族自治州': {'code': '838'}, '安康': {'code': '862'}, '丽江': {'code': '843'}, '湘潭': {'code': '751'}, '甘孜藏族自治州': {'code': '820'}, '营口': {'code': '606'}, '海城': {'code': '10070'}, '铜仁': {'code': '826'}, '桂林': {'code': '787'}, '白城': {'code': '620'}, '怒江傈僳族自治州': {'code': '844'}, '通辽': {'code': '591'}, '阿尔及利亚': {'code': '918'}, '芜湖': {'code': '665'}, '随州': {'code': '747'}}
    flag_next_zl = True
    p = 1
    start=0
    judge=0
    total = 0
    job_save_zl = []
    while flag_next_zl:
        try:
            url_zl_zwss = "https://fe-api.zhaopin.com/c/i/sou?"
            try:
                jl=dict_city[cityName]['code']
            except:
                judge = 1
                break
            if countyName != "":
                try:
                    re=dict_city[cityName]['sublist'][countyName]
                    city_id=re
                except:
                    city_id = jl
                    re=''
                    pass
            else:
                re=''
                city_id=jl
            data_li = {
                'start':str(start),
                'pageSize': '60',
                'cityId':city_id ,
                'kw': compName,
                'kt': '3',
                'lastUrlQuery': {"jl": jl, "re": re,"p": p, "kw": compName}}
            html_li_text =xh_pd_req(pos_url=url_zl_zwss,data=data_li,headers=head_reqst())
            print(html_li_text)
            if 'numFound' in html_li_text:
                dict_jl = json.loads(html_li_text)
                result=dict_jl['data']['results']
                print(len(result))
                #页码判断
                try:
                    if len(result) < 60:
                        flag_next_zl = False
                    else:
                        p = p + 1
                        start=start+60
                        if p > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                            flag_next_zl = False
                except:
                    traceback.print_exc()
                    break
                #获取详情页面
                for jl in result:
                    com_name=jl['company']['name']
                    time.sleep(random.uniform(0.3, 0.6))
                    if com_name == compName:
                        try:
                            job_url_1 = jl['positionURL']
                            job_zl_text=xh_pd_req(pos_url=job_url_1,data='',headers=head_reqst())
                            # print(job_zl_text)
                            zw_data_zl = zwjx_xzl(text=job_zl_text, compName=compName)
                            zw_data_zl['type'] = 'job'
                            zw_data_zl['channel'] = channelid
                            zw_data_zl['companyName'] = compName
                            zw_data_zl['province'] = provName
                            zw_data_zl['city'] = cityName_0
                            zw_data_zl['county'] = countyName
                            print("zl---------", zw_data_zl)
                            job_save_zl.append(zw_data_zl)
                        except:
                            pass
                    #发送数据
                    if len(job_save_zl) == 3:
                        total=total+3
                        data = json.dumps(job_save_zl)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('zl_jobl----2')
                        job_save_zl = []
                if len(job_save_zl) == 3 or len(job_save_zl) == 0:
                    pass
                else:
                    total = total + len(job_save_zl)
                    data = json.dumps(job_save_zl)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('zl_jobl----yfs')
            else:
                break
        except:
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_qczw(compName, provName, cityName, countyName,cityName_0, channelid=2):
    area_dic = {
        '北京': '010000', '东城区': '030803', '西城区': '010200', '朝阳区': '240201', '丰台区': '010600', '石景山区': '010700', '海淀区': '010800', '门头沟区': '010900', '房山区': '011000', '通州区': '011100', '顺义区': '011200', '昌平区': '011300', '大兴区': '011400', '怀柔区': '011500', '平谷区': '011600', '密云区': '011700', '延庆区': '011800', '上海': '020000', '黄浦区': '020100', '徐汇区': '020300', '长宁区': '020400', '静安区': '020500', '普陀区': '020600', '虹口区': '020800', '杨浦区': '020900', '浦东新区': '021000', '闵行区': '021100', '宝山区': '021200', '嘉定区': '021300', '金山区': '021400', '松江区': '021500', '青浦区': '021600', '奉贤区': '021800', '崇明区': '021900', '广东省': '030000', '广州': '030200', '越秀区': '030201', '荔湾区': '030202', '海珠区': '030203', '天河区': '030204', '白云区': '030205', '黄埔区': '030206', '番禺区': '030207', '花都区': '030208', '南沙区': '030209', '增城': '030211', '从化': '030212', '惠州': '030300', '汕头': '030400', '珠海': '030500', '香洲区': '030501', '斗门区': '030502', '金湾区': '030503', '横琴新区': '030504', '高栏港经济区': '030505', '珠海高新区': '030506', '珠海保税区': '030507', '万山海洋开发试验区': '030508', '佛山': '030600', '禅城区': '030601', '顺德区': '030602', '南海区': '030603', '三水区': '030604', '高明区': '030605', '中山': '030700', '东莞': '030800', '莞城区': '030801', '南城区': '030802', '万江区': '030804', '石碣镇': '030805', '石龙镇': '030806', '茶山镇': '030807', '石排镇': '030808', '企石镇': '030809', '横沥镇': '030810', '桥头镇': '030811', '谢岗镇': '030812', '东坑镇': '030813', '常平镇': '030814', '寮步镇': '030815', '大朗镇': '030816', '麻涌镇': '030817', '中堂镇': '030818', '高埗镇': '030819', '樟木头镇': '030820', '大岭山镇': '030821', '望牛墩镇': '030822', '黄江镇': '030823', '洪梅镇': '030824', '清溪镇': '030825', '沙田镇': '030826', '道滘镇': '030827', '塘厦镇': '030828', '虎门镇': '030829', '厚街镇': '030830', '凤岗镇': '030831', '长安镇': '030832', '松山湖区': '030833', '韶关': '031400', '江门': '031500', '湛江': '031700', '肇庆': '031800', '清远': '031900', '潮州': '032000', '河源': '032100', '揭阳': '032200', '茂名': '032300', '汕尾': '032400', '梅州': '032600', '开平': '032700', '阳江': '032800', '云浮': '032900', '深圳': '040000', '福田区': '040100', '罗湖区': '040200', '南山区': '040300', '盐田区': '040400', '宝安区': '040500', '龙岗区': '040600', '光明新区': '040700', '坪山区': '040800', '大鹏新区': '040900', '龙华新区': '041000', '天津': '050000', '和平区': '230204', '河东区': '050200', '河西区': '050300', '南开区': '050400', '河北区': '050500', '红桥区': '050600', '东丽区': '050700', '西青区': '050800', '津南区': '050900', '北辰区': '051000', '武清区': '051100', '宝坻区': '051200', '滨海新区': '051300', '宁河区': '051400', '静海区': '051500', '蓟州区': '051600', '重庆': '060000', '渝中区': '060100', '大渡口区': '060200', '江北区': '080303', '沙坪坝区': '060400', '合川区': '060600', '渝北区': '060700', '永川区': '060800', '巴南区': '060900', '南川区': '061000', '九龙坡区': '061100', '万州区': '061200', '涪陵区': '061300', '黔江区': '061400', '南岸区': '061500', '北碚区': '061600', '长寿区': '061700', '江津区': '061900', '綦江区': '062000', '潼南区': '062100', '铜梁区': '062200', '大足区': '062300', '荣昌区': '062400', '璧山区': '062500', '垫江县': '062600', '丰都县': '062700', '忠县': '062800', '石柱县': '062900', '城口县': '063000', '彭水县': '063100', '梁平区': '063200', '酉阳县': '063300', '开州区': '063400', '秀山县': '063500', '巫溪县': '063600', '巫山县': '063700', '奉节县': '063800', '武隆区': '063900', '云阳县': '064000', '江苏省': '070000', '南京': '070200', '玄武区': '070201', '秦淮区': '070203', '建邺区': '070204', '鼓楼区': '110201', '浦口区': '070207', '六合区': '070208', '栖霞区': '070209', '雨花台区': '070210', '江宁区': '070211', '溧水区': '070212', '高淳区': '070213', '苏州': '070300', '姑苏区': '070301', '吴中区': '070303', '相城区': '070304', '吴江区': '070305', '工业园区': '070306', '高新区': '170214', '无锡': '070400', '梁溪区': '070401', '滨湖区': '070404', '无锡新区': '070405', '惠山区': '070406', '锡山区': '070407', '宜兴市': '070408', '江阴市': '070409', '常州': '070500', '天宁区': '070501', '钟楼区': '070502', '新北区': '070504', '武进区': '070505', '金坛区': '070506', '溧阳市': '070507', '昆山': '070600', '常熟': '070700', '扬州': '070800', '南通': '070900', '镇江': '071000', '徐州': '071100', '连云港': '071200', '盐城': '071300', '张家港': '071400', '太仓': '071600', '泰州': '071800', '淮安': '071900', '宿迁': '072000', '丹阳': '072100', '泰兴': '072300', '靖江': '072500', '浙江省': '080000', '杭州': '080200', '拱墅区': '080201', '上城区': '080202', '下城区': '080203', '江干区': '080204', '西湖区': '130202', '滨江区': '080206', '余杭区': '080207', '萧山区': '080208', '临安区': '080209', '富阳区': '080210', '建德市': '080211', '桐庐县': '080212', '淳安县': '080213', '宁波': '080300', '海曙区': '080301', '北仑区': '080304', '镇海区': '080305', '鄞州区': '080306', '慈溪市': '080307', '余姚市': '080308', '奉化区': '080309', '宁海县': '080310', '象山县': '080311', '温州': '080400', '绍兴': '080500', '金华': '080600', '嘉兴': '080700', '台州': '080800', '湖州': '080900', '丽水': '081000', '舟山': '081100', '衢州': '081200', '义乌': '081400', '海宁': '081600', '四川省': '090000', '成都': '090200', '青羊区': '090201', '锦江区': '090202', '金牛区': '090203', '武侯区': '090204', '成华区': '090205', '龙泉驿区': '090206', '青白江区': '090207', '新都区': '090208', '温江区': '090209', '都江堰市': '090210', '彭州市': '090211', '邛崃市': '090212', '崇州市': '090213', '金堂县': '090214', '双流区': '090215', '郫都区': '090216', '大邑县': '090217', '蒲江县': '090218', '新津县': '090219', '简阳市': '090221', '绵阳': '090300', '乐山': '090400', '泸州': '090500', '德阳': '090600', '宜宾': '090700', '自贡': '090800', '内江': '090900', '攀枝花': '091000', '南充': '091100', '眉山': '091200', '广安': '091300', '资阳': '091400', '遂宁': '091500', '广元': '091600', '达州': '091700', '雅安': '091800', '西昌': '091900', '巴中': '092000', '甘孜': '092100', '阿坝': '092200', '凉山': '092300', '海南省': '100000', '海口': '100200', '三亚': '100300', '洋浦经济开发区': '100400', '文昌': '100500', '琼海': '100600', '万宁': '100700', '儋州': '100800', '东方': '100900', '五指山': '101000', '定安': '101100', '屯昌': '101200', '澄迈': '101300', '临高': '101400', '三沙': '101500', '琼中': '101600', '保亭': '101700', '白沙': '101800', '昌江': '101900', '乐东': '102000', '陵水': '102100', '福建省': '110000', '福州': '110200', '台江区': '110202', '仓山区': '110203', '马尾区': '110204', '晋安区': '110205', '闽侯县': '110206', '连江县': '110207', '罗源县': '110208', '闽清县': '110209', '永泰县': '110210', '平潭县': '110211', '福清市': '110212', '长乐市': '110213', '厦门': '110300', '泉州': '110400', '漳州': '110500', '莆田': '110600', '三明': '110700', '南平': '110800', '宁德': '110900', '龙岩': '111000', '山东省': '120000', '济南': '120200', '历下区': '120201', '市中区': '120202', '槐荫区': '120203', '天桥区': '120204', '历城区': '120205', '长清区': '120206', '平阴县': '120207', '济阳县': '120208', '商河县': '120209', '章丘区': '120210', '青岛': '120300', '市南区': '120301', '市北区': '120302', '黄岛区': '120303', '崂山区': '120304', '城阳区': '120305', '李沧区': '120306', '胶州市': '120307', '即墨区': '120308', '平度市': '120309', '莱西市': '120310', '烟台': '120400', '潍坊': '120500', '威海': '120600', '淄博': '120700', '临沂': '120800', '济宁': '120900', '东营': '121000', '泰安': '121100', '日照': '121200', '德州': '121300', '菏泽': '121400', '滨州': '121500', '枣庄': '121600', '聊城': '121700', '莱芜': '121800', '江西省': '130000', '南昌': '130200', '东湖区': '130201', '青云谱区': '130203', '湾里区': '130204', '青山湖区': '130205', '南昌县': '130206', '新建区': '130207', '安义县': '130208', '进贤县': '130209', '红谷滩新区': '130210', '九江': '130300', '景德镇': '130400', '萍乡': '130500', '新余': '130600', '鹰潭': '130700', '赣州': '130800', '吉安': '130900', '宜春': '131000', '抚州': '131100', '上饶': '131200', '广西': '140000', '南宁': '140200', '桂林': '140300', '柳州': '140400', '北海': '140500', '玉林': '140600', '梧州': '140700', '防城港': '140800', '钦州': '140900', '贵港': '141000', '百色': '141100', '河池': '141200', '来宾': '141300', '崇左': '141400', '贺州': '141500', '安徽省': '150000', '合肥': '150200', '瑶海区': '150201', '庐阳区': '150202', '蜀山区': '150203', '包河区': '150204', '经开区': '170215', '滨湖新区': '150206', '新站区': '150207', '政务区': '150209', '北城新区': '150210', '巢湖市': '150211', '长丰县': '150212', '肥东县': '150213', '肥西县': '150214', '庐江县': '150215', '芜湖': '150300', '安庆': '150400', '马鞍山': '150500', '蚌埠': '150600', '阜阳': '150700', '铜陵': '150800', '滁州': '150900', '黄山': '151000', '淮南': '151100', '六安': '151200', '宣城': '151400', '池州': '151500', '宿州': '151600', '淮北': '151700', '亳州': '151800', '河北省': '160000', '雄安新区': '160100', '石家庄': '160200', '廊坊': '160300', '保定': '160400', '唐山': '160500', '秦皇岛': '160600', '邯郸': '160700', '沧州': '160800', '张家口': '160900', '承德': '161000', '邢台': '161100', '衡水': '161200', '燕郊开发区': '161300', '河南省': '170000', '郑州': '170200', '中原区': '170201', '二七区': '170202', '管城回族区': '170203', '金水区': '170204', '上街区': '170205', '惠济区': '170206', '中牟县': '170207', '巩义市': '170208', '荥阳市': '170209', '新密市': '170210', '新郑市': '170211', '登封市': '170212', '郑东新区': '170213', '郑州航空港区': '170216', '洛阳': '170300', '开封': '170400', '焦作': '170500', '南阳': '170600', '新乡': '170700', '周口': '170800', '安阳': '170900', '平顶山': '171000', '许昌': '171100', '信阳': '171200', '商丘': '171300', '驻马店': '171400', '漯河': '171500', '濮阳': '171600', '鹤壁': '171700', '三门峡': '171800', '济源': '171900', '邓州': '172000', '湖北省': '180000', '武汉': '180200', '江岸区': '180201', '江汉区': '180202', '硚口区': '180203', '汉阳区': '180204', '武昌区': '180205', '青山区': '180206', '洪山区': '180207', '东西湖区': '180208', '汉南区': '180209', '蔡甸区': '180210', '江夏区': '180211', '黄陂区': '180212', '新洲区': '180213', '武汉经济开发区': '180214', '东湖新技术产业开发区': '180215', '宜昌': '180300', '黄石': '180400', '襄阳': '180500', '十堰': '180600', '荆州': '180700', '荆门': '180800', '孝感': '180900', '鄂州': '181000', '黄冈': '181100', '随州': '181200', '咸宁': '181300', '仙桃': '181400', '潜江': '181500', '天门': '181600', '神农架': '181700', '恩施': '181800', '湖南省': '190000', '长沙': '190200', '芙蓉区': '190201', '天心区': '190202', '岳麓区': '190203', '开福区': '190204', '雨花区': '190205', '望城区': '190206', '长沙县': '190207', '宁乡县': '190208', '浏阳市': '190209', '株洲': '190300', '湘潭': '190400', '衡阳': '190500', '岳阳': '190600', '常德': '190700', '益阳': '190800', '郴州': '190900', '邵阳': '191000', '怀化': '191100', '娄底': '191200', '永州': '191300', '张家界': '191400', '湘西': '191500', '陕西省': '200000', '西安': '200200', '莲湖区': '200201', '新城区': '200202', '碑林区': '200203', '灞桥区': '200204', '未央区': '200205', '雁塔区': '200206', '阎良区': '200207', '临潼区': '200208', '长安区': '200209', '蓝田县': '200210', '周至县': '200211', '鄠邑区': '200212', '高陵区': '200213', '高新技术产业开发区': '240208', '经济技术开发区': '240207', '曲江文化新区': '200216', '浐灞生态区': '200217', '国家民用航天产业基地': '200218', '西咸新区': '200219', '西安阎良航空基地': '200220', '西安国际港务区': '200221', '咸阳': '200300', '宝鸡': '200400', '铜川': '200500', '延安': '200600', '渭南': '200700', '榆林': '200800', '汉中': '200900', '安康': '201000', '商洛': '201100', '杨凌': '201200', '山西省': '210000', '太原': '210200', '运城': '210300', '大同': '210400', '临汾': '210500', '长治': '210600', '晋城': '210700', '阳泉': '210800', '朔州': '210900', '晋中': '211000', '忻州': '211100', '吕梁': '211200', '黑龙江省': '220000', '哈尔滨': '220200', '道里区': '220201', '南岗区': '220202', '道外区': '220203', '平房区': '220204', '松北区': '220205', '香坊区': '220206', '呼兰区': '220207', '阿城区': '220208', '依兰县': '220209', '方正县': '220210', '宾县': '220211', '巴彦县': '220212', '木兰县': '220213', '通河县': '220214', '延寿县': '220215', '双城区': '220216', '尚志市': '220217', '五常市': '220218', '伊春': '220300', '绥化': '220400', '大庆': '220500', '齐齐哈尔': '220600', '牡丹江': '220700', '佳木斯': '220800', '鸡西': '220900', '鹤岗': '221000', '双鸭山': '221100', '黑河': '221200', '七台河': '221300', '大兴安岭': '221400', '辽宁省': '230000', '沈阳': '230200', '大东区': '230201', '浑南区': '230202', '康平县': '230203', '皇姑区': '230205', '沈北新区': '230206', '沈河区': '230207', '苏家屯区': '230208', '铁西区': '230209', '于洪区': '230210', '法库县': '230211', '辽中区': '230212', '新民市': '230213', '大连': '230300', '西岗区': '230301', '中山区': '230302', '沙河口区': '230303', '甘井子区': '230304', '旅顺口区': '230305', '金州区': '230306', '瓦房店市': '230307', '普兰店区': '230308', '庄河市': '230309', '长海县': '230310', '高新园区': '230312', '长兴岛': '230313', '大连保税区': '230314', '鞍山': '230400', '营口': '230500', '抚顺': '230600', '锦州': '230700', '丹东': '230800', '葫芦岛': '230900', '本溪': '231000', '辽阳': '231100', '铁岭': '231200', '盘锦': '231300', '朝阳': '231400', '阜新': '231500', '吉林省': '240000', '长春': '240200', '南关区': '240202', '宽城区': '240203', '二道区': '240204', '绿园区': '240205', '双阳区': '240206', '净月经济开发区': '240209', '汽车产业开发区': '240210', '榆树市': '240211', '九台区': '240212', '德惠市': '240213', '农安县': '240214', '吉林': '240300', '辽源': '240400', '通化': '240500', '四平': '240600', '松原': '240700', '延吉': '240800', '白山': '240900', '白城': '241000', '延边': '241100', '云南省': '250000', '昆明': '250200', '五华区': '250201', '盘龙区': '250202', '官渡区': '250203', '西山区': '250204', '东川区': '250205', '呈贡区': '250206', '晋宁区': '250207', '富民县': '250208', '宜良县': '250209', '石林彝族自治县': '250210', '嵩明县': '250211', '禄劝县': '250212', '寻甸县': '250213', '安宁市': '250214', '曲靖': '250300', '玉溪': '250400', '大理': '250500', '丽江': '250600', '红河州': '251000', '普洱': '251100', '保山': '251200', '昭通': '251300', '文山': '251400', '西双版纳': '251500', '德宏': '251600', '楚雄': '251700', '临沧': '251800', '怒江': '251900', '迪庆': '252000', '贵州省': '260000', '贵阳': '260200', '遵义': '260300', '六盘水': '260400', '安顺': '260500', '铜仁': '260600', '毕节': '260700', '黔西南': '260800', '黔东南': '260900', '黔南': '261000', '甘肃省': '270000', '兰州': '270200', '金昌': '270300', '嘉峪关': '270400', '酒泉': '270500', '天水': '270600', '武威': '270700', '白银': '270800', '张掖': '270900', '平凉': '271000', '定西': '271100', '陇南': '271200', '庆阳': '271300', '临夏': '271400', '甘南': '271500', '内蒙古': '280000', '呼和浩特': '280200', '赤峰': '280300', '包头': '280400', '通辽': '280700', '鄂尔多斯': '280800', '巴彦淖尔': '280900', '乌海': '281000', '呼伦贝尔': '281100', '乌兰察布': '281200', '兴安盟': '281300', '锡林郭勒盟': '281400', '阿拉善盟': '281500', '宁夏': '290000', '银川': '290200', '吴忠': '290300', '中卫': '290400', '石嘴山': '290500', '固原': '290600', '西藏': '300000', '拉萨': '300200', '日喀则': '300300', '林芝': '300400', '山南': '300500', '昌都': '300600', '那曲': '300700', '阿里': '300800', '新疆': '310000', '乌鲁木齐': '310200', '克拉玛依': '310300', '喀什地区': '310400', '伊犁': '310500', '阿克苏': '310600', '哈密': '310700', '石河子': '310800', '阿拉尔': '310900', '五家渠': '311000', '图木舒克': '311100', '昌吉': '311200', '阿勒泰': '311300', '吐鲁番': '311400', '塔城': '311500', '和田': '311600', '克孜勒苏柯尔克孜': '311700', '巴音郭楞': '311800', '博尔塔拉': '311900', '青海省': '320000', '西宁': '320200', '海东': '320300', '海西': '320400', '海北': '320500', '黄南': '320600', '海南': '320700', '果洛': '320800', '玉树': '320900', '香港': '330000', '澳门': '340000', '台湾': '350000', '国外': '360000', '亚洲': '361000', '日本': '361001', '韩国': '361002', '马来西亚': '361003', '新加坡': '361004', '泰国': '361005', '菲律宾': '361006', '印度尼西亚': '361007', '斯里兰卡': '361008', '印度': '361009', '缅甸': '361010', '越南': '361011', '朝鲜': '361012', '哈萨克斯坦': '361013', '乌兹别克斯坦': '361014', '伊朗': '361015', '伊拉克': '361016', '阿富汗': '361017', '巴基斯坦': '361018', '土耳其': '361019', '科威特': '361020', '沙特阿拉伯': '361021', '蒙古': '361022', '孟加拉国': '361023', '欧洲': '362000', '英国': '362001', '法国': '362002', '德国': '362003', '意大利': '362004', '西班牙': '362005', '葡萄牙': '362006', '爱尔兰': '362007', '波兰': '362008', '挪威': '362009', '瑞典': '362010', '芬兰': '362011', '奥地利': '362012', '乌克兰': '362013', '白俄罗斯': '362014', '保加利亚': '362015', '罗马尼亚': '362016', '匈牙利': '362017', '希腊': '362018', '俄罗斯': '362019', '瑞士': '362020', '丹麦': '362021', '比利时': '362022', '荷兰': '362023', '美洲': '363000', '美国': '363001', '加拿大': '363002', '墨西哥': '363003', '巴西': '363004', '阿根廷': '363005', '智利': '363006', '秘鲁': '363007', '哥伦比亚': '363008', '委内瑞拉': '363009', '玻利维亚': '363010', '非洲': '364000', '埃及': '364001', '南非': '364002', '苏丹': '364003', '阿尔及利亚': '364004', '埃塞俄比亚': '364005', '肯尼亚': '364006', '赞比亚': '364007', '坦桑尼亚': '364008', '马达加斯加': '364009', '莫桑比克': '364010', '安哥拉': '364011', '加纳': '364012', '摩洛哥': '364013', '尼日利亚': '364014', '大洋洲': '365000', '澳大利亚': '365001', '新西兰': '365002', '其他': '366000', '珠三角': '01'}
    url_qc_zwss = "https://search.51job.com/list/"
    page_num = 1
    job_save_51 = []
    total =0
    flag_next = True
    judge = 0
    while flag_next:
        time.sleep(2)
        try:
            try:
                jobs_url_li = []
                d_pos = {"kw111": compName}
                postdata_str = parse.urlencode(d_pos).encode('utf-8')
                postdata_str = str(postdata_str).replace('%', '%25')
                postdata_str = postdata_str.split('kw111=')[1][:-1]
                url_qc_zws = url_qc_zwss + str(area_dic[cityName]) + ',000000,0000,00,9,99,' + postdata_str + ',2,' + str(page_num) + '.html'
                print('qc------------' + url_qc_zws)
            except:
                traceback.print_exc()
                flag_next = False
                judge=1
                break
            logging.error(url_qc_zws)
            try:
                html_li_text_1=xh_pd_re(pos_url=url_qc_zws,data='',headers=head_reqst())
                html_li_text_1.encoding = 'gbk'
                html_li_text=html_li_text_1.text
                # print(html_li_text)
            except:
                traceback.print_exc()
                flag_next = False
                break
            # request_li = request.Request(url=url_qc_zws, headers=head_reqst())
            # reponse_li = urlopen(request_li,timeout=3).read()
            # html_li_text = reponse_li.decode('gbk', errors='ignore')
            if compName in html_li_text:
                sel = Selector(text=html_li_text)
                xpa_jobs = '//div[@id="resultList"]/div[@class="el"]'
                jobs_li = sel.xpath(xpa_jobs)
                # print(len(jobs_li))
                for index,job_1 in enumerate(jobs_li):
                    # print(index)
                    xpa_job_gsmc = 'span[contains(@class,"t2")]/a/text()'
                    job_gsmc = job_1.xpath(xpa_job_gsmc).extract()[0].strip()
                    if job_gsmc == compName:
                        xpa_job_url = 'p[contains(@class,"t1")]/span/a/@href'
                        job_url = job_1.xpath(xpa_job_url).extract()[0].strip()
                        jobs_url_li.append(job_url)
                        # print(job_url)
                if not sel.xpath('//div[@class="dw_page"]/descendant::a[contains(text(),"下一页")]'):
                    flag_next = False
                else:
                    page_num = page_num + 1
                    if page_num >50:
                        flag_next = False
                for job_xq_url in jobs_url_li:
                    time.sleep(random.uniform(0.3, 0.6))
                    try:
                        job_xq_text_1 = xh_pd_re(pos_url=job_xq_url, data='', headers=head_reqst())
                        job_xq_text_1.encoding = 'gbk'
                        job_xq_text = job_xq_text_1.text

                        # request_job_xq = request.Request(url=job_xq_url, headers=head_reqst())
                        # request_job_xq = urlopen(request_job_xq,timeout=3).read()
                        # job_xq_text = request_job_xq.decode('gbk', errors='ignore')
                        # print(job_xq_text)
                        zw_data_51 = zwjx_51(text=job_xq_text, compName=compName)
                        zw_data_51['type'] = 'job'
                        zw_data_51['channel'] = channelid
                        zw_data_51['companyName'] = compName
                        zw_data_51['province'] = provName
                        zw_data_51['city'] = cityName_0
                        zw_data_51['county'] = countyName
                        print('51-------',zw_data_51)
                        job_save_51.append(zw_data_51)
                    except:
                        traceback.print_exc()
                        pass
                    if len(job_save_51) == 3:
                        total= total + 3
                        data = json.dumps(job_save_51)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('qc_jobl----3')
                        job_save_51 = []
                if len(job_save_51) == 3 or len(job_save_51) == 0:
                    pass
                else:
                    total = total + len(job_save_51)
                    data = json.dumps(job_save_51)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('qc_jobl----yfs')
        except:
            traceback.print_exc()
            flag_next = False
            logging.exception("Exception Logged")
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_58zw(compName, provName, cityName, countyName,cityName_0, channelid=3):
    cityList_dic = {'南京': {'sublist': {'南京周边': 'nanjing', '浦口': 'pukouqu', '高淳': 'gaochunxian', '鼓楼': 'gulouqu', '玄武': 'xuanwuqu', '江宁': 'jiangning', '雨花台': 'yuhuatai', '下关': 'xiaguan', '大厂': 'dachangqu', '溧水': 'lishuixian', '栖霞': 'qixiaqu', '建邺': 'jianye', '白下': 'baixia', '六合': 'liuhequ', '秦淮': 'qinhuai'}, 'code': 'nj'}, '宿州': {'sublist': {'泗县': 'sixian', '灵璧': 'lingbi', '萧县': 'xiaoxian', '墉桥': 'yongqiao', '其他': 'suzhoushi', '砀山': 'dangshan'}, 'code': 'suzhou'}, '浮梁': {'sublist': {'其他': 'fuliangxianqt', '城区': 'fuliangxiancq'}, 'code': 'fuliangxian'}, '沂南': {'sublist': {'其他': 'yinanxianqt', '城区': 'yinanxiancq'}, 'code': 'yinanxian'}, '玉林': {'sublist': {'兴业': 'xingyexian', '玉州': 'yuzhouqu', '博白': 'bobaixianyl', '福绵': 'fumianqu', '陆川': 'luchuanxian', '容县': 'rongxianq', '玉林周边': 'yulinzhoubian', '北流': 'beiliushiyl'}, 'code': 'yulin'}, '龙口': {'sublist': {'南山': 'ytns', '新区': 'ytxq', '东城区': 'ytdcq', '东海': 'ytdh', '西城区': 'ytxcq'}, 'code': 'longkou'}, '澄迈': {'sublist': {'金江镇': 'jinjiangz', '澄迈周边': 'chengmaizb', '加乐镇': 'jiale', '老城镇': 'laochengz', '永发镇': 'yongfa', '文儒镇': 'wenru', '瑞溪镇': 'ruixiz'}, 'code': 'cm'}, '岳阳': {'sublist': {'君山': 'junshan', '岳阳楼': 'yueyanglou', '云溪': 'yunxi', '汨罗': 'miluo', '临湘': 'linxiang', '其他': 'yueyang'}, 'code': 'yy'}, '固始': {'sublist': {'其他': 'gushixianqt', '城区': 'gushixiancq'}, 'code': 'gushixian'}, '怒江': {'sublist': {'怒江周边': 'nujiangzhoubian', '福贡': 'fugongxian', '贡山': 'gongshanxian', '碧江': 'bijiangxian', '泸水': 'lushuixian', '兰坪县': 'nujianglpx'}, 'code': 'nujiang'}, '淮南': {'sublist': {'潘集': 'panjiqu', '大通': 'datongquq', '谢家集': 'xiejiaji', '田家庵': 'tianjiaan', '毛集实验区': 'maojiqu', '凤台': 'fengtaixian', '寿县': 'shouxian', '八公山': 'bagongshan'}, 'code': 'hn'}, '高唐': {'sublist': {'鱼邱湖街道': 'lcyqhjd', '汇鑫街道': 'lchxjd', '人和街道': 'lcrhjd'}, 'code': 'gaotang'}, '昌邑': {'sublist': {'其他': 'changyishiqt', '城区': 'changyishicq'}, 'code': 'changyishi'}, '肇庆': {'sublist': {'端州': 'duanzhou', '怀集': 'huaiji', '四会': 'sihui', '封开': 'fengkai', '广宁': 'guangning', '高要': 'gaoyao', '德庆': 'deqingxian', '其他': 'zhaoqing', '鼎湖': 'dinghu'}, 'code': 'zq'}, '商丘': {'sublist': {'柘城': 'zhecheng', '梁园': 'liangyuan', '民权': 'minquan', '宁陵': 'ningling', '夏邑': 'xiayi', '永城': 'yongchengsq', '其他': 'shangqiu', '睢县': 'suixiansq', '睢阳': 'suiyang', '虞城': 'yucheng'}, 'code': 'sq'}, '义乌': {'sublist': {'江东': 'ywjiangdong', '城西': 'ywchengxi', '北苑': 'ywbeiyuan', '廿三里': 'ersanli', '义乌周边': 'yiwuzhoub', '稠江': 'choujiang', '义乌市区': 'yiwsq', '后宅': 'houzhai', '稠城': 'choucheng'}, 'code': 'yiwu'}, '金湖': {'sublist': {'其他': 'jinhuqt', '城区': 'jinhucq'}, 'code': 'jinhu'}, '营口': {'sublist': {'站前': 'zhanqianqu', '老边': 'laobian', '大石桥': 'dashiqiao', '其它': 'yingkou', '盖州': 'gaizhou', '熊岳镇': 'xiongyuezhen', '西市': 'xishi', '鲅鱼圈': 'bayuquan'}, 'code': 'yk'}, '悉尼': {'sublist': {}, 'code': 'glsydney'}, '铜川': {'sublist': {'王益': 'wangyiqu', '铜川周边': 'tongchuanzhoubian', '宜君': 'yijunxian', '开发区': 'tckaifa', '耀州': 'yaozhouqu', '印台': 'yintaiqu'}, 'code': 'tc'}, '安达': {'sublist': {'其他': 'andaqita', '城区': 'andachengqu'}, 'code': 'shanda'}, '盱眙': {'sublist': {'其他': 'xuyiqt', '城区': 'xuyicq'}, 'code': 'xuyi'}, '佛山': {'sublist': {'佛山周边': 'foshan', '南海': 'nanhai', '高明': 'gaoming', '三水': 'sanshui', '禅城': 'chancheng', '顺德': 'shundeshiqu'}, 'code': 'fs'}, '朔州': {'sublist': {'山阴': 'shanyin', '朔城': 'shuocheng', '右玉': 'youyu', '怀仁': 'huairen', '应县': 'yingx', '平鲁': 'pingluq', '朔州周边': 'shuozhouzhoubian'}, 'code': 'shuozhou'}, '保亭': {'sublist': {'加茂镇': 'jiamao', '新政镇': 'xinzhengz', '什玲镇': 'shenling', '保城镇': 'baocheng', '保亭周边': 'baotingzb', '三道镇': 'sandao', '响水镇': 'xiangshuiz'}, 'code': 'baoting'}, '万宁': {'sublist': {'后安镇': 'houan', '大茂镇': 'damao', '山根镇': 'snageng', '和乐镇': 'hele', '万城镇': 'wangchengz', '龙滚镇': 'longgun', '万宁周边': 'wanningzb'}, 'code': 'wanning'}, '赤壁': {'sublist': {'其他': 'chibishiqt', '城区': 'chibishicq'}, 'code': 'chibishi'}, '拉萨': {'sublist': {'墨竹工卡': 'mozhugongka', '当雄': 'dangxiong', '林周': 'linzhouxian', '其它': 'lasaqita', '曲水': 'qushui', '堆龙德庆': 'duilongdeqing', '尼木': 'nimu', '城关': 'chengguan', '达孜': 'dazi'}, 'code': 'lasa'}, '新安': {'sublist': {'其他': 'lyxinanqt', '城区': 'lyxinancq'}, 'code': 'lyxinan'}, '桐乡': {'sublist': {'桐乡周边': 'tongxzb', '西栅': 'xish', '东栅': 'dongsh', '乌镇': 'wuzh', '濮院': 'jxpy', '博物馆': 'bowwg', '桐乡市区': 'tongxsq'}, 'code': 'tongxiang'}, '扶余': {'sublist': {'其他': 'fuyuxianqt', '城区': 'fuyuxiancq'}, 'code': 'fuyuxian'}, '丽江': {'sublist': {'宁蒗': 'ninglangxian', '永胜': 'yongshengxian', '玉龙': 'yulongxian', '华坪': 'huapingxian', '古城': 'guchengqu'}, 'code': 'lj'}, '简阳': {'sublist': {'简城街道': 'jianchengjiedao', '杨柳街道': 'yangliujiedao', '其他': 'jianyangshiqita', '十里坝街道': 'shilibajiedao', '射洪坝街道': 'shehongbajiedao'}, 'code': 'jianyangshi'}, '滑县': {'sublist': {'其他': 'huaxianqt', '城区': 'huaxiancq'}, 'code': 'huaxian'}, '高平': {'sublist': {'其他': 'gaopingqt', '城区': 'gaopingcq'}, 'code': 'gaoping'}, '定州': {'sublist': {'北城': 'beichengqu', '西城': 'xichengqu', '其他': 'dingzhouqita', '南城': 'nanchengqu'}, 'code': 'dingzhou'}, '吴忠': {'sublist': {'盐池': 'yanchi', '红寺堡': 'hongsipu', '利通': 'litong', '吴忠周边': 'wuzhongzhoubian', '青铜峡': 'qingtongxia', '太阳山': 'taiyangshan', '同心': 'tongxin'}, 'code': 'wuzhong'}, '大竹': {'sublist': {'其他': 'dazuqt', '城区': 'dazucq'}, 'code': 'dazu'}, '青岛': {'sublist': {'城阳': 'chengyang', '李沧': 'licang', '崂山': 'laoshan', '黄岛': 'huangdao', '胶南': 'jiaonan', '四方': 'sifang', '市南': 'shinan', '市北': 'shibei', '莱西': 'laixi', '即墨': 'jimo', '平度': 'pingdu', '青岛周边': 'qingdao', '胶州': 'jiaozhou'}, 'code': 'qd'}, '射阳': {'sublist': {'其他': 'sheyangqt', '城区': 'sheyangcq'}, 'code': 'sheyang'}, '湛江': {'sublist': {'麻章': 'mazhang', '廉江': 'lianjiang', '霞山': 'xiashan', '开发区': 'kaifaq', '赤坎': 'chikan', '吴川': 'wuchuanshi', '遂溪': 'suixixian', '坡头': 'potou', '其他': 'zhanjiangshi', '徐闻': 'xuwenxian', '雷州': 'leizhou'}, 'code': 'zhanjiang'}, '深圳': {'sublist': {'宝安': 'baoan', '坪山新区': 'pingshanxinqu', '盐田': 'yantian', '南山': 'nanshan', '大鹏新区': 'dapengxq', '福田': 'futian', '龙华新区': 'szlhxq', '布吉': 'buji', '光明新区': 'guangmingxinqu', '深圳周边': 'shenzhenzhoubian', '罗湖': 'luohu', '龙岗区': 'longgang'}, 'code': 'sz'}, '武穴': {'sublist': {'其他': 'wuxueshiqt', '城区': 'wuxueshicq'}, 'code': 'wuxueshi'}, '滨州': {'sublist': {'邹平': 'binzhouzouping', '无棣': 'wudibz', '阳信': 'yangxin', '惠民': 'huiminxian', '博兴': 'boxingbz', '其他': 'binzhou', '沾化': 'zhanhua', '滨城': 'bincheng'}, 'code': 'bz'}, '阿拉善盟': {'sublist': {'阿拉善盟周边': 'alashanmengzhoubian', '阿拉善右旗': 'alashanyouqi', '额济纳旗': 'ejinaqi', '阿拉善左旗': 'alashanzuoqi'}, 'code': 'alsm'}, '孟津': {'sublist': {'其他': 'mengjinquqt', '城区': 'mengjinqucq'}, 'code': 'mengjinqu'}, '杞县': {'sublist': {'泥沟乡': 'nigouxiang', '城关镇': 'chengguanzhen', '其他': 'qixianqita', '五里河镇': 'wulihezhen'}, 'code': 'qixianqu'}, '重庆': {'sublist': {'沙坪坝': 'shapingba', '两江新区': 'liangjiangxinqu', '永川': 'yongchuan', '璧山': 'bishanxian', '重庆周边': 'chongqing', '万州': 'wanzhou', '石柱': 'cqshizhu', '九龙坡': 'jiulongpo', '合川': 'hechuan', '南岸': 'nanan', '长寿': 'changshou', '北碚': 'beibei', '江北': 'jiangbei', '涪陵': 'fuling', '巴南': 'banan', '渝中': 'yuzhong', '大渡口': 'dadukou', '渝北': 'yubei'}, 'code': 'cq'}, '单县': {'sublist': {'园艺街道': 'yuanyijiedao', '东城街道': 'dongchengjiedao', '南城街道': 'sxnanchengjiedao', '其他': 'danxianqita', '北城街道': 'sxbeichengjiedao'}, 'code': 'shanxian'}, '攀枝花': {'sublist': {'西区': 'xiq', '米易': 'miyixian', '东区': 'dongq', '盐边': 'yanbianxian', '仁和': 'renhequ'}, 'code': 'panzhihua'}, '鹤壁': {'sublist': {'淇滨': 'qibinqu', '淇县': 'qixianqhb', '山城': 'shanchengqu', '鹤山': 'heshanqu', '浚县': 'xunxianhb'}, 'code': 'hb'}, '孟州': {'sublist': {'其他': 'mengzhouqt', '城区': 'mengzhoucq'}, 'code': 'mengzhou'}, '吉安': {'sublist': {'万安': 'wananxian', '井冈山': 'jinggangshanshi', '峡江': 'xijiangxian', '吉水': 'jishuixian', '庐陵新区': 'lulingxinqu', '永丰': 'yongfengxian', '吉州': 'jizhouqu', '永新': 'yongxinxian', '遂川': 'suichuanxian', '吉安县': 'jianxian', '新干': 'xinganx', '安福': 'anfuxian', '泰和': 'taihexian', '青原': 'qingyuanqu'}, 'code': 'ja'}, '北京': {'sublist': {'密云': 'miyun', '平谷': 'pinggu', '丰台': 'fengtai', '燕郊': 'bjyanjiao', '东城': 'dongcheng', '石景山': 'shijingshan', '通州': 'tongzhouqu', '西城': 'xicheng', '延庆': 'yanqing', '宣武': 'xuanwu', '北京周边': 'beijingzhoubian', '门头沟': 'mentougou', '朝阳': 'chaoyang', '顺义': 'shunyi', '崇文': 'chongwen', '海淀': 'haidian', '房山': 'fangshan', '怀柔': 'huairou', '大兴': 'daxing', '昌平': 'changping'}, 'code': 'bj'}, '广安': {'sublist': {'邻水': 'linshuixian', '广安城北': 'guanganchengbei', '广安城南': 'guanganchengnan', '武胜': 'wushengxian', '广安': 'guangan', '岳池': 'yuechixian', '其他': 'qitaq', '华蓥': 'huayingshi'}, 'code': 'ga'}, '云梦': {'sublist': {'其他': 'yunmengqt', '城区': 'yunmengcq'}, 'code': 'yunmeng'}, '乌鲁木齐': {'sublist': {'水磨沟': 'shuitanggou', '天山': 'tianshan', '达坂城': 'dabancheng', '新市': 'wlmqxinshi', '乌鲁木齐县': 'wulumuqixian', '乌鲁木齐周边': 'wlmqzb', '开发区': 'kaifaarea', '头屯河': 'toutunhequ', '沙依巴克': 'shayibake', '米东区': 'midongdistrict'}, 'code': 'xj'}, '佳木斯': {'sublist': {'永红': 'yonghongqu', '抚远': 'fuyuanxian', '向阳': 'xiangyq', '同江': 'tongjiangshi', '东风': 'dongfengqu', '前进': 'qianjinqu', '郊区': 'jiaoqu', '桦南': 'huananxian', '桦川': 'huachuanxian', '富锦': 'fujinshi', '汤原': 'tangyuanxian'}, 'code': 'jms'}, '安岳': {'sublist': {'其他': 'anyuexianqita', '城区': 'anyuechengqu'}, 'code': 'anyuexian'}, '江门': {'sublist': {'新会': 'xinhui', '蓬江': 'pengjiang', '江海': 'jianghai', '南新': 'nanxin', '恩平': 'enping', '台山': 'taishanshi', '北新': 'beixin', '鹤山': 'heshan', '开平': 'kaipingshijm', '江门周边': 'jiangmen'}, 'code': 'jm'}, '阳江': {'sublist': {'岗侨': 'gangqiaoqu', '高新区': 'gaoxinquw', '阳西': 'yangxixian', '阳东': 'yangdongxian', '江城': 'jiangchengqu', '海陵': 'hailingqu', '阳春': 'yangchunshi'}, 'code': 'yj'}, '巴音郭楞': {'sublist': {'和静': 'hejx', '焉耆': 'yanqx', '博湖': 'byglbh', '库尔勒': 'kuerleshi', '和硕': 'byglhs', '若羌': 'byglrq', '且末': 'bygljm', '巴州周边': 'bazhouzhoubian', '轮台': 'luntx', '尉犁': 'weilx'}, 'code': 'bygl'}, '阜新': {'sublist': {'彰武': 'zhangwu', '清河门': 'qinghemen', '阜新周边': 'fuxinzhoubian', '新邱': 'xinqiu', '海州': 'haizhouq', '太平': 'taipingq', '细河': 'xihe', '阜新县': 'fuxinx'}, 'code': 'fx'}, '阿勒泰': {'sublist': {'福海': 'altfh', '布尔津': 'altbej', '吉木乃': 'altjmn', '阿勒泰市区': 'altsq', '青河': 'altqh', '哈巴河': 'althbh', '富蕴': 'altfy'}, 'code': 'alt'}, '旧金山': {'sublist': {}, 'code': 'glsanfrancisco'}, '云浮': {'sublist': {'云安': 'yuanan', '郁南': 'yunan', '云城': 'yuanchengq', '新兴': 'xinxingx', '罗定': 'luoding', '云浮周边': 'yuanfuzhoubian'}, 'code': 'yf'}, '金华': {'sublist': {'磐安': 'panan', '永康': 'jinhuayongkang', '武义县': 'wuyixjh', '浦江县': 'pujiang', '义乌': 'yiwushi', '东阳': 'dongyangqu', '其他': 'jinhua', '金华市区': 'wuchengqu', '兰溪': 'lanxi'}, 'code': 'jh'}, '玉溪': {'sublist': {'易门': 'yimen', '峨山': 'eshanxian', '江川': 'jiangchuan', '澄江': 'chengjiang', '通海': 'tonghai', '其它': 'yuxi', '元江': 'yuanjiang', '新平': 'xinpingxian', '华宁': 'huaning', '红塔': 'hongta'}, 'code': 'yx'}, '株洲': {'sublist': {'株洲县': 'zhuzhouxian', '芦淞': 'lusong', '石峰': 'shifeng', '茶陵': 'chaling', '攸县': 'zzyouxianzz', '其他': 'zhuzhoushi', '天元': 'tianyuan', '荷塘': 'hetang', '醴陵市': 'zhuzhoujiling', '炎陵': 'yanlingxianx'}, 'code': 'zhuzhou'}, '兴安盟': {'sublist': {'突泉': 'tuquan', '扎赉特旗': 'zalanteqi', '兴安盟周边': 'xinganmengzhoubian', '科尔沁右翼中旗': 'keerqinyouyizhongqi', '科尔沁右翼前旗': 'keerqinyouyiqianqi', '乌兰浩特': 'wulanhaote', '阿尔山': 'aershan'}, 'code': 'xam'}, '昆明': {'sublist': {'五华': 'wuhua', '昆明周边': 'kunming', '安宁': 'anningshikm', '盘龙': 'panlong', '西山': 'xishan', '呈贡': 'chenggong', '官渡': 'guandu'}, 'code': 'km'}, '寿光': {'sublist': {'台头': 'taitou', '留吕': 'liulv', '文家': 'wenjia', '其它': 'shouguangshi'}, 'code': 'shouguang'}, '乳山': {'sublist': {'银滩': 'whyantan', '其他': 'rushanshiqita', '城区': 'rushanchengqu', '市区': 'whsq'}, 'code': 'rushan'}, '克拉玛依': {'sublist': {'白碱滩': 'baijiantan', '克拉玛依区': 'kelamayiqu', '其它': 'kelamayi', '乌尔禾': 'wuerhe', '独山子': 'dushanzi'}, 'code': 'klmy'}, '南平': {'sublist': {'顺昌': 'shunchang', '建阳': 'jianyangs', '南平周边': 'nanpingzhoubian', '邵武': 'shaowu', '建瓯': 'jianou', '延平': 'yanping', '武夷山': 'wuyishanshi'}, 'code': 'np'}, '常宁': {'sublist': {'其他': 'changningshiqt', '城区': 'changningshicq'}, 'code': 'changningshi'}, '甘孜': {'sublist': {'德格': 'degexian', '丹巴': 'danbaxian', '甘孜县': 'ganzixian', '甘孜周边': 'ganzizhoubian', '康定': 'kangdingxian', '泸定': 'ludingxian'}, 'code': 'ganzi'}, '邵阳': {'sublist': {'隆回': 'longhuixian', '邵东': 'shaodongxiansy', '武冈': 'wugangshi', '北塔': 'beitaqu', '双清': 'shuangqingqu', '洞口': 'dongkouxian', '绥宁': 'suiningqu', '新宁': 'xinningxian', '邵阳县': 'shaoyangxiansy', '大祥': 'daxiangqu', '新邵': 'xinjunxian', '城步县': 'shaoyangcbx'}, 'code': 'shaoyang'}, '六盘水': {'sublist': {'水城': 'shuicheng', '六盘水周边': 'liupanshuizb', '六枝特区': 'liuzhi', '盘县': 'panx', '钟山': 'zhongshanq'}, 'code': 'lps'}, '运城': {'sublist': {'盐湖': 'yanhu', '新绛': 'xinjiangxian', '永济': 'yongji', '芮城': 'ruicheng', '其它': 'yunchengshi', '闻喜': 'wenxi', '临猗': 'yclinyi', '河津': 'hejin', '稷山': 'jishan', '万荣': 'wanrong'}, 'code': 'yuncheng'}, '中山': {'sublist': {'黄圃': 'zshuangpu', '中山周边': 'zhongshan', '石岐': 'shiqi', '小榄': 'zsxiaolan', '南头': 'zsnantou', '坦洲': 'zstanzhou', '火炬开发区': 'huojukfq', '港口': 'zsgangkou', '三乡': 'zssanxiang', '东区': 'zsdongqu', '横栏': 'zshenglan', '西区': 'zsxiqu', '古镇': 'zsguzhen', '沙溪': 'zsshaxi', '大涌': 'zsdayong', '南朗': 'zsnanlang', '南区': 'nanqu', '东凤': 'zsdongfeng', '东升': 'zsdongsheng', '五桂山': 'wuguishan'}, 'code': 'zs'}, '抚顺': {'sublist': {'高湾新区': 'gaowanxinqu', '胜利': 'fsshengli', '开发区': 'fskaifa', '顺城': 'shuncheng', '新宾': 'xinbin', '抚顺': 'fushunxian', '新抚': 'xinfuqu', '东洲': 'dongzhou', '望花': 'wanghua', '李石开发区': 'lishikaifaqu', '其他': 'fushunshi', '清原': 'fsqingyuan'}, 'code': 'fushun'}, '通许': {'sublist': {'通许县': 'tongxux'}, 'code': 'tongxuxian'}, '枝江': {'sublist': {'其他': 'zhijiangqt', '城区': 'zhijiangcq'}, 'code': 'zhijiang'}, '三明': {'sublist': {'清流': 'qingliuxian', '尤溪': 'youxi', '梅列': 'meilie', '三明周边': 'sanming', '将乐': 'jianglexian', '泰宁': 'tainingxian', '三元': 'sanyuan', '大田': 'datianxian', '宁化': 'ninghua', '建宁': 'jianningxian', '沙县': 'shaxian', '永安': 'yongansm', '明溪': 'mingxi'}, 'code': 'sm'}, '武汉': {'sublist': {'蔡甸': 'caidian', '江夏': 'jiangxia', '汉南': 'hannan', '沌口开发区': 'whtkfq', '江汉': 'jianghan', '青山': 'whqingshanqu', '汉阳': 'hanyang', '武汉周边': 'wuhan', '江岸': 'jiangan', '东西湖': 'dongxihu', '黄陂': 'huangpo', '硚口': 'qiaokou', '武昌': 'wuchang', '洪山': 'hongshan', '新洲': 'xinzhouqu'}, 'code': 'wh'}, '雅安': {'sublist': {'名山': 'mingshanxian', '芦山': 'lusx', '雅安周边': 'yaanzhoubian', '天全': 'tianquanxian', '宝兴': 'baoxingxian', '荥经': 'xingjingxian', '雨城': 'yuchengqu', '石棉': 'shimianxian', '汉源': 'hanyuanxian'}, 'code': 'ya'}, '台州': {'sublist': {'椒江': 'jiaojiang', '黄岩': 'huangyan', '天台': 'tiantai', '温岭': 'wenlingqu', '路桥': 'luqiao', '玉环县': 'taizhouyuhuan', '三门': 'sanmen', '仙居': 'xianju', '其他': 'taizhoushi', '临海': 'taizhoulinhai'}, 'code': 'tz'}, '栖霞': {'sublist': {'其他': 'qixiaqt', '城区': 'qixiacq'}, 'code': 'qixia'}, '安陆': {'sublist': {'其他': 'anluqt', '城区': 'anlucq'}, 'code': 'anlu'}, '上饶': {'sublist': {'上饶周边': 'shangraozhoubian', '余干': 'yugan', '广丰': 'guangfeng', '信州': 'xinzhouq', '鄱阳': 'poyang', '上饶县': 'shangraox', '玉山': 'yushanx', '德兴': 'dexing'}, 'code': 'sr'}, '如皋': {'sublist': {'其它': 'rugaoqita', '如皋市区': 'rugaoshiqu'}, 'code': 'rugao'}, '黄山': {'sublist': {'黄山风景区': 'huangshanfjq', '歙县': 'shex', '黟县': 'yix', '黄山': 'huangshanq', '祁门': 'qimen', '休宁': 'xiuning', '徽州': 'huizhouq', '黄山周边': 'huangshanzhoubian', '屯溪': 'taipq'}, 'code': 'huangshan'}, '浚县': {'sublist': {'其他': 'junxianqt', '城区': 'junxiancq'}, 'code': 'junxian'}, '启东': {'sublist': {'其它': 'qidongqita', '启东市区': 'qidongshiqu'}, 'code': 'qidong'}, '姜堰': {'sublist': {'三水街道': 'sanshuijiedao', '其他': 'jiangyanqita', '罗塘街道': 'luotangjiedao'}, 'code': 'jiangyan'}, '海西': {'sublist': {'格尔木': 'geermushihx', '都兰': 'dulan', '德令哈': 'delinghashi', '乌兰': 'wulan', '天峻': 'tianjun', '海西周边': 'haixizhoubian'}, 'code': 'hx'}, '凉山': {'sublist': {'会东': 'huid', '布拖': 'butuo', '会理': 'huili', '凉山周边': 'liangshanzhoubian', '西昌': 'xichangshi', '德昌': 'dechang', '甘洛': 'ganluo'}, 'code': 'liangshan'}, '珠海': {'sublist': {'高新区': 'zhgxq', '金湾': 'jinwan', '香洲': 'xiangzhou', '珠海周边': 'zhuhai', '斗门': 'doumen', '坦洲': 'zhtanzhou', '横琴': 'zhhq'}, 'code': 'zh'}, '松原': {'sublist': {'农业高新产业开发区': 'nongyequ', '乾安': 'qiananxian', '宁江': 'ningjiangxian', '长岭': 'changlingxiansy', '前郭': 'guoerls', '扶余': 'fuyuxiansy', '经济技术开发区': 'jingjijs'}, 'code': 'songyuan'}, '成都': {'sublist': {'锦江': 'jinjiang', '崇州': 'cdchongzhou', '温江': 'wenjiang', '郫县': 'pixian', '新都': 'xindu', '青羊': 'qingyangqu', '青白江': 'qingbaijiang', '都江堰': 'dujiangyanshi', '天府新区': 'cdtfxq', '蒲江': 'cdpujiang', '大邑': 'cddayi', '新津': 'xinjin', '双流': 'shuangliu', '金牛': 'jinniu', '龙泉驿': 'longquanyi', '高新西区': 'gaoxinxiqu', '成华': 'chenghua', '邛崃市': 'cdqls', '高新区': 'cdgaoxin', '金堂': 'jintang', '武侯': 'wuhou', '成都周边': 'chengdu'}, 'code': 'cd'}, '安丘': {'sublist': {'其他': 'anqiuqt', '城区': 'anqiucq'}, 'code': 'anqiu'}, '冷水江': {'sublist': {'其他': 'lengshuijiangshiqt', '城区': 'lengshuijiangshicq'}, 'code': 'lengshuijiangshi'}, '徐州': {'sublist': {'丰县': 'xzfengx', '鼓楼': 'xzgulou', '铜山': 'xztongshan', '贾汪': 'jiawang', '徐州周边': 'xuzhou', '邳州': 'pizhouqu', '九里': 'jiuli', '金山桥开发区': 'jsqkfq', '新城区': 'xchengqu', '云龙': 'yunlong', '沛县': 'peixianqu', '睢宁': 'xzsuining', '泉山': 'quanshan', '新沂': 'xinyiqu'}, 'code': 'xz'}, '达州': {'sublist': {'通川': 'tongchuanqu', '达县': 'daxian', '万源': 'wanyuanshi', '达州周边': 'dazhouzhoubian', '宣汉': 'xuanhandz', '大竹': 'dazudz', '开江': 'kaijiang', '渠县': 'quxdz'}, 'code': 'dazhou'}, '淇县': {'sublist': {'其他': 'qixianqqt', '城区': 'qixianqcq'}, 'code': 'qixianq'}, '开封': {'sublist': {'龙亭': 'longtingqu', '兰考': 'lankaoxiankf', '金明': 'jinmingqu', '尉氏': 'weishixiankf', '禹王台': 'yuwangtai', '顺河': 'shunhequ', '杞县': 'kaifengqixian', '通许': 'tongxuxiankf', '开封县': 'kaifengxian', '鼓楼': 'gulouquyu'}, 'code': 'kaifeng'}, '武威': {'sublist': {'古浪': 'gulang', '天祝': 'tianzx', '武威周边': 'wuweizhoubian', '民勤': 'minqin', '凉州': 'liangzhou'}, 'code': 'wuwei'}, '湘西': {'sublist': {'永顺': 'yongshunx', '泸溪': 'luxix', '古丈': 'guzhang', '凤凰': 'fenghuang', '龙山': 'longshanx', '花垣': 'huayuanx', '吉首': 'jishou', '保靖': 'baojing', '湘西周边': 'xiangxizhoubian'}, 'code': 'xiangxi'}, '图木舒克': {'sublist': {'金墩': 'jindun', '皮恰克松地': 'piqiakesongdi', '盖米里克': 'gaimilike', '图木休克': 'tumuxiuke', '图木舒克周边': 'tumushukezb', '其盖麦旦': 'qigaimaidan'}, 'code': 'tmsk'}, '沛县': {'sublist': {'沛县市区': 'peixianshiqu', '其它': 'peixianqita'}, 'code': 'xzpeixian'}, '永春': {'sublist': {'其他': 'yongchunxianqt', '城区': 'yongchunxiancq'}, 'code': 'yongchunxian'}, '锡林郭勒': {'sublist': {'西乌珠穆沁旗': 'xwzmqq', '镶黄旗': 'xianghuangqi', '正镶白旗': 'zhengxiangbaiqi', '阿巴嘎旗': 'abagaqi', '苏尼特右旗': 'suniteyouqi', '正蓝旗': 'zhenglanqi', '苏尼特左旗': 'sunitezuoqi', '太仆寺旗': 'taipusiqi', '锡林浩特': 'xilinhaoteshi', '东县': 'dongxian', '多伦': 'duolunxian', '东乌珠穆沁旗': 'dwzmqq', '二连浩特': 'erlianhaoteshi'}, 'code': 'xl'}, '广州': {'sublist': {'南沙': 'nanshagz', '黄埔': 'huangpugz', '荔湾': 'liwan', '佛山': 'foshanqu', '从化周边': 'conghuazhoubian', '白云': 'baiyun', '越秀': 'yuexiu', '东莞': 'dongguanqu', '萝岗': 'luoganggz', '花都': 'huadugz', '天河': 'tianhe', '海珠': 'haizhu', '增城': 'zengcheng', '番禺': 'panyu', '经济开发区': 'jingjikaifaqu', '从化': 'conghua', '横沥': 'hengligz', '广州周边': 'guangzhouzhoubian', '南沙周边': 'nanshazhoubian'}, 'code': 'gz'}, '贺州': {'sublist': {'富川': 'fuchuan', '昭平': 'zhaoping', '平桂': 'pinggui', '八步': 'babu', '钟山': 'zhongshanx', '贺州周边': 'hezhouzhoubian'}, 'code': 'hezhou'}, '华容': {'sublist': {'其他': 'huarongqt', '城区': 'huarongcq'}, 'code': 'huarong'}, '乌兰察布': {'sublist': {'凉城': 'liangchengx', '集宁': 'jiningq', '兴和': 'xinghe', '商都': 'sangdu', '化德': 'huade', '卓资': 'zuozhi', '丰镇': 'fengzhen', '乌兰察布周边': 'wulanchabuzhoubian'}, 'code': 'wlcb'}, '荣成': {'sublist': {'港湾街道': 'gangwanjiedao', '其他': 'rongchengshiqita', '东山街道': 'rcdongshanjiedao', '虎山镇': 'whhsz', '港西': 'gangxi', '大疃镇': 'whdtz', '桃园街道': 'rctaoyuanjiedao', '市区': 'whrcsq', '王连街道': 'wanglianjiedao', '石岛': 'shidao', '人和镇': 'whrhz', '宁津街道': 'ningjinjiedao', '斥山街道': 'chishanjiedao'}, 'code': 'rongcheng'}, '开平': {'sublist': {'三江': 'sanjiangjm', '南岛': 'nandao', '迳头': 'jingtoujm', '幸福': 'xingfujm', '水口': 'shuikoujm', '侨园': 'qiaoyuan', '祥龙': 'xianglong', '曙光西': 'shuguangxi', '开平周边': 'kaipingzb', '新昌': 'xinchangjm', '新海': 'xinhai', '曙光东': 'shuguangdong', '荻海': 'dihai'}, 'code': 'kaipingshi'}, '南安': {'sublist': {'南安市区': 'nananshiqu', '其它': 'nananqita'}, 'code': 'nananshi'}, '德宏': {'sublist': {'盈江': 'yingjiangxian', '陇川': 'longchuanxian', '瑞丽': 'ruilishi', '芒市': 'dhms', '德宏周边': 'dehongzhoubian', '潞西': 'luxishi', '梁河': 'lianghexian'}, 'code': 'dh'}, '济宁': {'sublist': {'梁山': 'liangshanxjn', '北湖新区': 'jiningbhxq', '兖州': 'yanzhou', '金乡': 'jinxiang', '鱼台': 'yutai', '任城': 'rencheng', '济宁周边': 'jiningshi', '汶上': 'wenshangjn', '邹城': 'jiningzoucheng', '嘉祥': 'jiaxiang', '高新区': 'jininggxq', '微山': 'weishanjn', '市中': 'jnshizhongqu', '曲阜': 'qufu', '泗水': 'sishui'}, 'code': 'jining'}, '渑池': {'sublist': {'其他': 'yingchixianqt', '城区': 'yingchixiancq'}, 'code': 'yingchixian'}, '湖州': {'sublist': {'安吉县': 'huzhouanji', '其他': 'huzhoushi', '德清': 'deqingqu', '南浔': 'nanxun', '吴兴': 'wuxing', '长兴': 'changxingqu'}, 'code': 'huzhou'}, '长兴': {'sublist': {'长兴市区': 'changxingshiqu', '其它': 'chongxingqita'}, 'code': 'changxing'}, '晋江': {'sublist': {'SM广场': 'smguangchang', '体育中心': 'qztyzx', '阳光广场': 'yangguanggc', '晋江周边': 'jinjiangzb'}, 'code': 'jinjiangshi'}, '雄安新区': {'sublist': {'容城': 'xionganrongcheng', '安新': 'anxin', '其他': 'xionganxinquqita', '雄县': 'xionganxiongxian'}, 'code': 'xionganxinqu'}, '青州': {'sublist': {'云门山街道': 'yunmenshanjiedao', '其他': 'qingzhoushiqita', '黄楼街道': 'huangloujiedao', '益都街道': 'yidongjiedao', '王府街道': 'wangfujiedao'}, 'code': 'qingzhou'}, '利津': {'sublist': {'其他': 'lijinqt', '城区': 'lijincq'}, 'code': 'lijin'}, '乌海': {'sublist': {'滨河东区': 'wuhaibhdq', '滨河西区': 'wuhaibhxq', '乌达': 'wudaqu', '海勃湾': 'haibowan', '海南': 'hainanqu'}, 'code': 'wuhai'}, '大庆': {'sublist': {'红岗': 'honggang', '大同': 'datong', '让胡路': 'ranghulu', '萨尔图': 'saertu', '其他': 'daqing', '龙凤': 'longfeng'}, 'code': 'dq'}, '泰安': {'sublist': {'肥城': 'taianfeicheng', '东平': 'dongpingta', '泰安周边': 'taian', '泰山区': 'taishanqu', '岱岳区': 'daiyue', '宁阳': 'ningyangta', '新泰': 'taianxintai'}, 'code': 'ta'}, '曹县': {'sublist': {'郑庄街道办': 'zhengzhuangjiedaoban', '倪集街道办': 'nijijiedaoban', '磐石街道办': 'panshijiedaoban', '其他': 'caoxianqita', '青菏街道办': 'qinghejiedaoban', '曹城街道办': 'caochengjiedaoban'}, 'code': 'caoxian'}, '五家渠': {'sublist': {'101团': 'yilingyituan', '103团': 'yilingsantuan', '青湖路': 'qinghulu', '102团': 'yilingertuan', '人民路': 'renml', '军垦路': 'junkenlu', '五家渠周边': 'wujiaquzhoubian'}, 'code': 'wjq'}, '济南': {'sublist': {'高新': 'gaoxinqujn', '长清': 'changqingqv', '天桥': 'tianqiao', '章丘': 'zhangqiushi', '历下': 'lixia', '济南周边': 'jinanzhoubian', '商河': 'shanghe', '历城': 'licheng', '济阳': 'jiyang', '平阴': 'pingyin', '市中': 'jnshizhong', '槐荫': 'huaiyinqu'}, 'code': 'jn'}, '呼伦贝尔': {'sublist': {'额尔古纳': 'eerguna', '满洲里': 'manzhouli', '扎兰屯': 'zalantun', '根河': 'genhe', '牙克石': 'yakeshi', '海拉尔': 'hailaerq', '呼伦贝尔周边': 'hulunbeierzhoubian'}, 'code': 'hlbe'}, '茂名': {'sublist': {'电白': 'dianbai', '化州': 'huazhou', '茂南': 'maonan', '高州': 'gaozhou', '茂港': 'maogang', '其他': 'maoming', '信宜': 'xinyi'}, 'code': 'mm'}, '宜春': {'sublist': {'丰城': 'fengchengshiyc', '奉新': 'fengxin', '高安': 'gaoanyc', '其它': 'yichunshi', '袁州': 'yuanzhou', '上高': 'shanggao', '宜丰': 'yifeng', '万载': 'wangzai', '樟树': 'zhangshuyc'}, 'code': 'yichun'}, '亳州': {'sublist': {'利辛': 'lixinxian', '蒙城': 'mengchengxian', '谯城': 'qiaochengqu', '涡阳': 'woyangxian'}, 'code': 'bozhou'}, '沂源': {'sublist': {'其他': 'yiyuanxianqt', '城区': 'yiyuanxiancq'}, 'code': 'yiyuanxian'}, '东明': {'sublist': {'其他': 'dongmingqt', '城区': 'dongmingcq'}, 'code': 'dongming'}, '唐山': {'sublist': {'曹妃甸': 'caofeidian', '路南': 'lunan', '路北': 'lubei', '海港开发区': 'haigangqu', '迁西': 'qianxixiants', '古冶': 'guye', '高新区': 'gxq', '丰南': 'fengnan', '开平': 'kaiping', '南堡开发区': 'nanbaoqu', '其他': 'tangshan', '遵化': 'zunhuats', '迁安': 'tangshanqianan', '丰润': 'fengrun'}, 'code': 'ts'}, '延安': {'sublist': {'延川': 'yanchuanxian', '子长': 'zichangxian', '洛川': 'luochuanxian', '富县': 'fuxian', '黄陵': 'huanglingxian', '吴起': 'wuqixian', '黄龙': 'huanglongxian', '志丹': 'zhidanxian', '宝塔': 'baotaqu', '甘泉': 'ganquanxian', '宜川': 'yichuanxian', '安塞': 'anzaixian', '延长': 'yanchangxian'}, 'code': 'yanan'}, '燕郊': {'sublist': {'燕郊镇': 'yanjiaozhen', '城区': 'lfcq', '迎宾路': 'lfybl', '大厂': 'lfdc', '其他': 'yanjiaoqita', '东市区': 'lfdsq', '潮白河': 'lfcbh', '燕顺路': 'lfysl'}, 'code': 'lfyanjiao'}, '鹰潭': {'sublist': {'贵溪': 'guixi', '龙虎山': 'longhushan', '月湖': 'yuehu', '其他': 'yingtanqita', '余江': 'yujiangyt'}, 'code': 'yingtan'}, '广水': {'sublist': {'其他': 'guangshuishiqt', '城区': 'guangshuishicq'}, 'code': 'guangshuishi'}, '石河子': {'sublist': {'红山': 'hongshans', '向阳': 'xiangyangs', '老街': 'laojie', '东城': 'dongchengs', '石河子周边': 'shihezizb', '新城': 'xinchengs'}, 'code': 'shz'}, '新昌': {'sublist': {'其他': 'xinchangqt', '城区': 'xinchangcq'}, 'code': 'xinchang'}, '潮州': {'sublist': {'饶平': 'raoping', '枫溪': 'fengxi', '潮州周边': 'chaozhouzhoubian', '潮安': 'chaoan', '湘桥': 'xiangqiao'}, 'code': 'chaozhou'}, '邵阳县': {'sublist': {'其他': 'shaoyangxianqt', '城区': 'shaoyangxiancq'}, 'code': 'shaoyangxian'}, '邯郸': {'sublist': {'永年县': 'yongnian', '邯郸周边': 'handan', '磁县': 'cixianhd', '成安县': 'cax', '涉县': 'shexianhd', '肥乡县': 'feixx', '魏县': 'weix', '大名县': 'dmx', '高开区': 'gkq', '临漳县': 'linzhang', '峰峰矿区': 'fengfengkuang', '武安市': 'handanwuan', '邯山': 'hanshan', '丛台': 'congtai', '邯郸县': 'handanxian', '复兴': 'fuxing'}, 'code': 'hd'}, '博罗': {'sublist': {'园洲': 'hzyuanzhou', '石湾': 'hzshiwan', '博罗周边': 'boluozb', '龙溪': 'hzlongxi', '罗阳': 'hzluoyang'}, 'code': 'boluo'}, '淮北': {'sublist': {'烈山': 'lieshanqu', '相山': 'xiangshanqu', '淮北周边': 'huaibeizb', '濉溪': 'suixix', '杜集': 'dujiqu'}, 'code': 'huaibei'}, '武义县': {'sublist': {'牛头山森林公园': 'niutssl', '城郊': 'jhwycj', '城东': 'jhwycd', '郭洞景区': 'guodjq', '武义茶城': 'wuycc', '壶山公园': 'hushgy', '城南': 'jhwycn', '武义周边': 'jhwyzb', '城北': 'jhwycb', '寿仙谷': 'shouxg', '清风寨': 'qingfz'}, 'code': 'wuyix'}, '黄骅': {'sublist': {'其他': 'huanghuaqt', '城区': 'huanghuacq'}, 'code': 'huanghua'}, '平湖': {'sublist': {'东湖景区': 'donghjq', '莫氏庄园': 'moszy', '九龙山海滨浴场': 'jiulshb', '平湖周边': 'pinghuzb'}, 'code': 'pinghushi'}, '石狮': {'sublist': {'石狮服装城': 'shishifzc', '石狮周边': 'shishizb'}, 'code': 'shishi'}, '阿坝': {'sublist': {'茂县': 'maoxian', '松潘': 'songpanxian', '汶川县': 'wenchuanxian', '小金': 'xiaojinxian', '九寨沟': 'jiuzhaigouxian', '马尔康': 'maerkangxian', '阿坝周边': 'abazhoubian'}, 'code': 'ab'}, '府谷': {'sublist': {'其他': 'fuguqita', '城区': 'fuguchengqu'}, 'code': 'fugu'}, '西安': {'sublist': {'长安': 'changanlu', '新城': 'xaxincheng', '沣渭新区': 'fengweixinq', '灞桥': 'baqiao', '雁塔': 'yanta', '临潼': 'lintong', '莲湖': 'lianhu', '碑林': 'beilin', '阎良': 'yanliang', '高新区': 'xagx', '杨凌': 'yangling', '西安周边': 'xianzhoubian', '曲江新区': 'qujiangxinq', '未央': 'weiyang'}, 'code': 'xa'}, '巴彦淖尔': {'sublist': {'五原': 'wuyuan', '乌拉特中旗': 'wulatezhongqi', '磴口': 'dengkou', '临河': 'linheq', '杭锦后旗': 'hangjinhouqi', '巴彦周边': 'bayanzhoubian', '乌拉特前旗': 'wulateqianqi', '乌拉特后旗': 'wulatehouqi'}, 'code': 'bycem'}, '巴中': {'sublist': {'平昌': 'pingchangxian', '通江': 'tongjiangxian', '巴中周边': 'bazhongzhoubian', '经开区': 'jingkaiqubz', '巴州': 'bazhouqu', '南江': 'nanjiangxian', '恩阳': 'enyang'}, 'code': 'bazhong'}, '安康': {'sublist': {'汉阴县': 'ankanghyx', '汉滨': 'hanbin', '紫阳': 'ziyang', '岚皋': 'langao', '宁陕县': 'ankangnsx', '镇坪': 'zhenping', '旬阳': 'xunyangxian', '平利县': 'ankangplx', '其他': 'ankangshi', '白河县': 'ankangbhx', '石泉县': 'ankangsqx'}, 'code': 'ankang'}, '包头': {'sublist': {'青山': 'qingshanqu', '土默特右旗': 'tmtyq', '稀土高新区': 'xitgxq', '达尔罕茂明安联合旗': 'daerhanqi', '东河': 'donghe', '白云矿区': 'baiyunkuang', '九原': 'jiuyuan', '昆都仑区': 'kundoulun', '固阳': 'guy', '包头周边': 'baotou', '石拐': 'shiguai', '滨河新区': 'btbhx'}, 'code': 'bt'}, '文昌': {'sublist': {'文昌周边': 'wenchangzb', '文城镇': 'wencheng', '东路镇': 'donglu', '蓬莱镇': 'penglaiz', '重兴镇': 'chongxing', '潭牛镇': 'tanniu', '会文镇': 'huiwen'}, 'code': 'wenchang'}, '灌云': {'sublist': {'侍庄街道': 'shizhuangjiedao', '其他': 'guanyunxianqita', '城区': 'guanyunchengqu'}, 'code': 'guanyun'}, '益阳': {'sublist': {'南县': 'nanxianyy', '安化': 'anhua', '桃江': 'taojiang', '资阳': 'ziyangq', '沅江': 'yuanjiangsyy', '赫山': 'heshanq', '益阳周边': 'yiyangzhoubian'}, 'code': 'yiyang'}, '宜宾': {'sublist': {'珙县': 'gongxian', '宜宾县': 'yibinxian', '高县': 'gaoxian', '翠屏': 'cuipingqu', '长宁': 'changningxyb', '江安': 'jianganxian', '屏山': 'pingshanxian', '兴文': 'xingwenxian', '筠连': 'junlianxian', '南溪': 'nanxixian'}, 'code': 'yb'}, '汕尾': {'sublist': {'汕尾城区': 'shanweicq', '陆丰': 'lufengshisw', '陆河': 'luhexian', '汕尾周边': 'shanweizb', '海丰县': 'shanweihaifeng'}, 'code': 'sw'}, '永康': {'sublist': {'江南街道': 'ykjiangnanjiedao', '西城街道': 'xichengjiedao', '芝英街道': 'zhiyingjiedao', '东城街道': 'ykdongchengjiedao', '永康市区': 'jhyksq', '其他': 'yongkangshiqita', '永康周边': 'jhykzb'}, 'code': 'yongkang'}, '湘潭': {'sublist': {'湘潭周边': 'xiangtanqita', '湘乡': 'xiangxiang', '湘潭县': 'xiangtanxian', '岳塘': 'yuetang', '韶山': 'shaoshan', '雨湖': 'yuhu', '九华经济开发区': 'jiuhuajingjikfq'}, 'code': 'xiangtan'}, '福州': {'sublist': {'台江': 'taijiang', '罗源': 'luoyuanxian', '连江': 'lianjiangxian', '闽侯': 'minhouxian', '晋安': 'jinanqu', '福清': 'fuqingshi', '福州周边': 'fuzhouzb', '鼓楼': 'fzgulou', '马尾': 'mayi', '长乐': 'changleshi', '平潭': 'pingtanxian', '永泰': 'yongtaixian', '闽清': 'minqingxian', '仓山': 'cangshan'}, 'code': 'fz'}, '黄石': {'sublist': {'花湖': 'hshh', '团城山': 'tuanchengshan', '阳新': 'hsyangxin', '其它': 'huangshi', '黄石港': 'huangshigang', '西塞山': 'xisaishan', '铁山': 'tieshan', '大冶': 'daye', '下陆': 'xialu'}, 'code': 'hshi'}, '孝义': {'sublist': {'其他': 'xiaoyiqt', '城区': 'xiaoyicq'}, 'code': 'xiaoyi'}, '桐城': {'sublist': {'兴尔旺': 'xingerwang', '黄甲': 'huangjia', '文昌': 'wenchangs', '范岗': 'fangang', '唐湾': 'tangwan', '开发区': 'kaifaqutc', '龙眠': 'longmian', '双港': 'shuanggangtc', '桐城周边': 'tongchengzb', '嬉子湖': 'xizihu', '金神': 'jinshen', '青草': 'qingcao', '新渡': 'xindutc', '孔城': 'kongcheng', '吕亭': 'lvting', '大关': 'daguantc'}, 'code': 'tongcheng'}, '琼海': {'sublist': {'中原镇': 'zhongyuanz', '石壁镇': 'shibi', '阳江镇': 'yangjiang', '嘉积镇': 'jiaji', '琼海周边': 'qionghaizb', '万泉镇': 'wangquan', '博鳌镇': 'boao'}, 'code': 'qh'}, '格尔木': {'sublist': {'其他': 'geermushiqt', '城区': 'geermushicq'}, 'code': 'geermushi'}, '宁德': {'sublist': {'周宁': 'zhouningxian', '屏南': 'pingnanxianq', '霞浦': 'xiapuxian', '古田': 'gutianxian', '福安': 'fuanshind', '柘荣': 'zhenrongxian', '蕉城': 'jiaochengqu', '寿宁': 'shouningxian', '福鼎': 'fudingshind'}, 'code': 'nd'}, '邳州': {'sublist': {'邳州市区': 'pizhoushiqu', '其它': 'pizhouqita'}, 'code': 'pizhou'}, '建湖': {'sublist': {'建湖市区': 'jianhushiqu', '其它': 'jianghuqita'}, 'code': 'jianhu'}, '莘县': {'sublist': {'东鲁街道': 'lcdljd', '莘亭街道': 'lcxtjd', '莘州街道': 'lcxzjd', '燕塔街道': 'lcytjd'}, 'code': 'shenxian'}, '自贡': {'sublist': {'大安': 'daanqu', '沿滩': 'yantanqu', '荣县': 'rongxian', '贡井': 'gongjingqu', '自流井': 'ziliujing', '自贡周边': 'zigongzb', '富顺': 'fsx'}, 'code': 'zg'}, '邹城': {'sublist': {'千泉街道': 'qianquanjiedao', '凫山街道': 'fushanjiedao', '钢山街道': 'gangshanjiedao', '其他': 'zouchengshiqita'}, 'code': 'zoucheng'}, '乐山': {'sublist': {'五通桥': 'wutongqiao', '峨边': 'ebian', '沙湾': 'shawan', '夹江': 'jiaj', '沐川': 'muchuan', '马边': 'mab', '峨眉山': 'emeishan', '市中区': 'lsshizhong', '乐山周边': 'leshan', '井研': 'jingyan', '犍为': 'jianwei'}, 'code': 'ls'}, '双鸭山': {'sublist': {'友谊': 'youyix', '饶河': 'raohe', '宝清': 'baoqing', '双鸭山周边': 'shuangyashanzb', '岭东': 'lingdong', '四方台': 'sifangtai', '集贤': 'jixian', '尖山': 'jianshan', '宝山': 'baoshanqu'}, 'code': 'sys'}, '肇东': {'sublist': {'其他': 'zhaodongqita', '城区': 'zhaodongchengqu'}, 'code': 'shzhaodong'}, '肇州': {'sublist': {'其他': 'zhaozhouqita', '城区': 'zhaozhouchengqu'}, 'code': 'zhaozhou'}, '儋州': {'sublist': {'儋州周边': 'tanzhouzb', '那大镇': 'nada', '大成镇': 'dachengz', '雅星镇': 'yaxing', '南丰镇': 'nanfengz', '兰洋镇': 'lanyang', '和庆镇': 'heqing'}, 'code': 'danzhou'}, '盘锦': {'sublist': {'双台子': 'shuangtaizi', '兴隆台': 'xinglongtai', '大洼': 'dawa', '盘山': 'panshan', '其它': 'panjin'}, 'code': 'pj'}, '尉氏': {'sublist': {'尉氏县': 'wxshixian'}, 'code': 'weishixian'}, '西双版纳': {'sublist': {'勐海': 'menghaixian', '西双版纳周边': 'xishuangbannazhoubian', '景洪': 'jinggongshi', '勐腊': 'menglaxian'}, 'code': 'bn'}, '黑河': {'sublist': {'孙吴': 'sunwu', '北安': 'beian', '五大连池': 'wudalianchi', '爱辉': 'aihui', '嫩江': 'nenjiang', '黑河周边': 'heihezb', '逊克': 'xunke'}, 'code': 'heihe'}, '连云港': {'sublist': {'灌南县': 'lianyugangguannan', '赣榆': 'ganyu', '新浦': 'xinpu', '东海': 'donghaiqu', '其它': 'lianyungang', '灌云县': 'lianyungangguanyun', '连云': 'lianyun', '海州': 'haizhou'}, 'code': 'lyg'}, '响水': {'sublist': {'其他': 'xiangshuiqt', '城区': 'xiangshuicq'}, 'code': 'xiangshui'}, '章丘': {'sublist': {'水寨镇': 'shuizhaizhen', '普集镇': 'pujizhen', '刁镇': 'diaozhen', '相公庄镇': 'xianggongzhuang', '章丘': 'zhangqiushiqu', '其他': 'zhangqiuqita', '绣惠镇': 'xiuhuizhen', '高官寨镇': 'gaoguanzhai', '辛寨乡': 'xinzhaixiang', '官庄乡': 'guanzhuangxiang'}, 'code': 'zhangqiu'}, '钦州': {'sublist': {'浦北': 'pubeixian', '市区': 'qzshiqu', '灵山': 'lingshanxian', '钦南': 'qinnanqu', '钦北': 'qinbeiqu'}, 'code': 'qinzhou'}, '定西': {'sublist': {'通渭': 'tongwei', '定西周边': 'dingxizhoubian', '临洮': 'lintao', '漳县': 'zhangxian', '渭源': 'weiyuanx', '岷县': 'minxian', '安定': 'anding', '陇西': 'longxix'}, 'code': 'dx'}, '温岭': {'sublist': {'温岭市区': 'wenlingshiqu', '其它': 'wenlingqita'}, 'code': 'wenling'}, '宁波': {'sublist': {'宁海': 'ninghaixian', '江东': 'jiangdong', '象山': 'xiangshanqunew', '海曙': 'haishu', '镇海': 'zhenhai', '鄞州': 'yinzhou', '慈溪': 'cixiqu', '高新区': 'nbgxq', '余姚': 'yuyaoqu', '江北': 'jiangbeiqu', '奉化': 'fenghua', '北仑': 'beilun', '宁波周边': 'ningbo'}, 'code': 'nb'}, '黔南': {'sublist': {'龙里': 'longli', '三都': 'sandushuizu', '贵定': 'guiding', '都匀': 'duyun', '惠水': 'huishui', '独山': 'dushan', '瓮安': 'wengan', '福泉': 'fuquan', '平塘': 'pingtang', '长顺': 'changshun', '荔波': 'libo', '罗甸': 'luodian', '黔南周边': 'qiannanzb'}, 'code': 'qn'}, '宝应县': {'sublist': {'其他': 'baoyingxianqita', '城区': 'baoyingchengqu', '宝应县周边': 'baoyingxzb'}, 'code': 'baoyingx'}, '长垣': {'sublist': {'魏庄街道': 'weizhuangjiedao', '蒲东街道': 'pudongjiedao', '其他': 'changyuanxianqita', '南蒲街道': 'cynanpujiedao', '蒲北街道': 'pubeijiedao', '蒲西街道': 'puxijiedao'}, 'code': 'changyuan'}, '红河': {'sublist': {'石屏': 'shipingxian', '金平': 'jinpingxian', '河口': 'hekouxian', '泸西': 'luxixian', '建水': 'jianshuixian', '蒙自': 'mengzixian', '个旧': 'gejiushi', '元阳': 'yuanyangxian', '弥勒': 'milexianhh', '红河县': 'honghexian', '开远': 'kaiyuanshi', '绿春': 'lvchunxian', '屏边': 'pingbianxian'}, 'code': 'honghe'}, '诸暨': {'sublist': {'诸暨市区': 'shujishiqu', '枫桥镇': 'fengqiaozhen', '大唐镇': 'datangzhenzhuji', '街亭镇': 'jietingzhen', '其它': 'zhujiqita', '五泄镇': 'wuxiezhen', '店口镇': 'diankouzhen'}, 'code': 'zhuji'}, '遵化': {'sublist': {'其他': 'zunhuaqt', '城区': 'zunhuacq'}, 'code': 'zunhua'}, '阳谷': {'sublist': {'狮子楼街道': 'lcszljd', '侨润街道': 'lcqrjd', '博济桥街道': 'lcbjqjd'}, 'code': 'yanggu'}, '昌乐': {'sublist': {'其他': 'changleqt', '城区': 'changlecq'}, 'code': 'changle'}, '澳门': {'sublist': {'嘉模堂': 'jiamotangqu', '风顺堂': 'fengshuntangqu', '花地玛堂': 'huadimatangqu', '望德堂': 'wangdetangqu', '圣安多尼堂区': 'shenganduonitangqu', '大堂': 'datangqu', '路氹城': 'ludangcheng', '澳门周边': 'aomenzhoubian', '圣方济各堂': 'shengfanggetangqu'}, 'code': 'am'}, '宝鸡': {'sublist': {'眉县': 'meixian', '岐山': 'qishanxian', '渭滨': 'weibin', '凤县': 'fengxian', '其它': 'baojishi', '陈仓': 'chencang', '金台': 'jintai'}, 'code': 'baoji'}, '商水': {'sublist': {'其他': 'shangshuiqt', '城区': 'shangshuicq'}, 'code': 'shangshui'}, '杭州': {'sublist': {'淳安': 'chunan', '江干': 'jianggan', '余杭': 'yuhang', '拱墅': 'gongshu', '富阳': 'fuyangshi', '西湖': 'xihuqu', '临安': 'linanshi', '杭州周边': 'hangzhou', '上城': 'hzshangcheng', '桐庐': 'tonglu', '下城': 'xiacheng', '滨江': 'binjiang', '建德': 'jiandeshi', '萧山': 'xiaoshan'}, 'code': 'hz'}, '临汾': {'sublist': {'曲沃': 'quwo', '侯马': 'houma', '霍州': 'huozhou', '其它': 'linfenshi', '洪洞': 'hongdong', '尧都': 'yaodou', '古县': 'lfguxian', '襄汾': 'xiangfen', '翼城': 'lfyicheng'}, 'code': 'linfen'}, '垦利': {'sublist': {'胜坨': 'shengtuo', '兴隆街': 'xinglongjie', '垦利街': 'kenlijie', '董集': 'dongjixiang', '黄河口': 'huanghekou', '永安': 'yongankl', '垦利周边': 'kenlizhoubian', '郝家': 'haojia'}, 'code': 'kl'}, '辽阳': {'sublist': {'灯塔': 'dengtaly', '文圣': 'wensheng', '太子河': 'taizihe', '弓长岭': 'gongchangling', '其它': 'liaoyangshi', '宏伟': 'hongwei', '白塔': 'baita', '辽阳县': 'liaoyangxian'}, 'code': 'liaoyang'}, '临沧': {'sublist': {'双江': 'shuanjiang', '凤庆': 'fengqing', '临沧周边': 'lincangzhoubian', '永德': 'yongde', '临翔': 'linx', '沧源': 'cangyuan', '镇康': 'zhentang', '耿马': 'gengma', '云县': 'yunx'}, 'code': 'lincang'}, '嘉兴': {'sublist': {'嘉兴市区': 'jiaxsq', '秀洲': 'xiuzhou', '南湖': 'nanhu', '嘉善': 'jiashanqu', '海宁': 'hainingqu', '桐乡': 'tongxiangqu', '经济开发区': 'jingjikfq', '嘉兴周边': 'jiaxing', '平湖': 'jxpinghu', '海盐': 'haiyanjx'}, 'code': 'jx'}, '保山': {'sublist': {'隆阳': 'longyangqu', '腾冲': 'tengchongxian', '施甸': 'shidianxian', '昌宁': 'changningxian', '龙陵': 'longlingxian'}, 'code': 'bs'}, '温哥华': {'sublist': {}, 'code': 'glvancouver'}, '敦煌': {'sublist': {'其他': 'dunhuangqita', '城区': 'dunhuangchengqu'}, 'code': 'dunhuang'}, '汉川': {'sublist': {'仙女山街道': 'xiannvshanjiedao', '其他': 'hanchuanshiqita', '城区': 'hanchuanchengqu'}, 'code': 'hanchuan'}, '恩施': {'sublist': {'咸丰': 'xianfengxian', '利川': 'lichuanshi', '宣恩': 'xuanenxian', '鹤峰': 'hefengxian', '来凤': 'laifengxian', '恩施市': 'enshishi', '建始': 'jianshixian', '巴东': 'badongxian'}, 'code': 'es'}, '微山': {'sublist': {'其他': 'weishanqt', '城区': 'weishancq'}, 'code': 'weishan'}, '阿拉尔': {'sublist': {'金银川路': 'jinyinchuanlu', '青松路': 'qingsonglu', '阿拉尔周边': 'alaerzhoubian', '幸福路': 'xingfulu', '南口': 'nankoua', '团场': 'tuanchang'}, 'code': 'ale'}, '扬中': {'sublist': {'扬中市区': 'yangzhongshiqu', '其它': 'yangzhongqita'}, 'code': 'yangzhong'}, '清迈': {'sublist': {}, 'code': 'glchiangmai'}, '南县': {'sublist': {'其他': 'nanxianqt', '城区': 'nanxiancq'}, 'code': 'nanxian'}, '三门峡': {'sublist': {'陕县': 'shanxiansmx', '灵宝': 'smxlingbao', '义马': 'yimashi', '开发区': 'kaifaqu', '卢氏': 'lushixian', '渑池': 'mianchixiansmx', '湖滨': 'hubinqu'}, 'code': 'smx'}, '馆陶': {'sublist': {'柴堡镇': 'chaibuzhen', '王桥乡': 'wangqiaoxiang', '馆陶镇': 'guantaozhen', '魏僧寨镇': 'weizengzhai', '路桥乡': 'luqiaoxiang', '南徐村乡': 'nanxucun', '寿山寺乡': 'shoushansi', '馆陶': 'guantaoxian', '房寨镇': 'fangzhaizhen'}, 'code': 'gt'}, '铁岭': {'sublist': {'调兵山': 'diaobingshan', '西丰': 'xifengxian', '昌图': 'changtuxian', '银州': 'yinzq', '铁岭县': 'tielingxian', '清河': 'qinghequ', '开原': 'kaiyuantl'}, 'code': 'tl'}, '丰城': {'sublist': {'其他': 'fengchengshiqt', '城区': 'fengchengshicq'}, 'code': 'fengchengshi'}, '永新': {'sublist': {'永新县城': 'yxxchengqu', '南路片乡镇': 'nanlupianxz', '北路片乡镇': 'beilupianxz', '东路片乡镇': 'donglupianxz', '西路片乡镇': 'xilupianxz', '永新县周边': 'yxxzhoubian'}, 'code': 'yxx'}, '洛杉矶': {'sublist': {}, 'code': 'gllosangeles'}, '承德': {'sublist': {'围场': 'weichangxian', '兴隆': 'xinglongxian', '双滦': 'shuangluan', '宽城': 'kuanchengxian', '承德周边': 'chengdezb', '承德市': 'chengdeshi', '营子': 'yingzi', '滦平': 'luanpingxian', '开发区': 'cdkaifaqu', '丰宁': 'fengningxian', '隆化': 'longhuaxian', '平泉': 'pingquanxian', '双桥': 'cdshuangqiao', '承德县': 'chengdexian'}, 'code': 'chengde'}, '临海': {'sublist': {'邵家渡街道': 'shaojiadongjiedao', '江南街道': 'jiangnanjiedao', '古城街道': 'guchengjiedao', '大洋街道': 'dayangjiedao', '杜桥镇': 'dongqiaozhen', '大田街道': 'datianjiedao', '其他': 'linhaishiqita'}, 'code': 'linhai'}, '上海': {'sublist': {'静安': 'jingan', '闵行': 'minxing', '黄浦': 'huangpu', '杨浦': 'yangpu', '卢湾': 'luwan', '青浦': 'qingpu', '普陀': 'putuo', '嘉定': 'jiading', '宝山': 'baoshan', '虹口': 'hongkou', '松江': 'songjiang', '长宁': 'changning', '金山': 'jinshan', '崇明': 'chongming', '奉贤': 'fengxiansh', '徐汇': 'xuhui', '闸北': 'zhabei', '上海周边': 'shanghaizhoubian', '浦东': 'pudongxinqu', '南汇': 'nanhui'}, 'code': 'sh'}, '崇左': {'sublist': {'大新': 'daxinx', '宁明': 'ningming', '江州': 'jiangzhou', '凭祥': 'pingxiangs', '崇左周边': 'chongzuozhoubian', '扶绥': 'fusui', '龙州': 'longzhou', '天等': 'tiandeng'}, 'code': 'chongzuo'}, '苏州': {'sublist': {'太仓': 'taicangshi', '平江': 'pingjiangqu', '工业园': 'gongyeyuan', '吴江': 'wujiangshi', '常熟': 'changshushi', '高新区': 'sugaoxinqu', '苏州周边': 'suzhouqita', '相城': 'xiangchengqua', '金阊': 'jinchangquyu', '沧浪': 'canglang', '昆山': 'suzhoukunshan', '张家港': 'zhangjiagangshi', '吴中': 'wuzhongqu'}, 'code': 'su'}, '汕头': {'sublist': {'金平': 'jinping', '南澳': 'nanao', '濠江': 'haojiang', '潮南': 'chaonan', '潮阳': 'stchaoyang', '澄海': 'chenghai', '其他': 'shantou', '龙湖': 'longhu'}, 'code': 'st'}, '白城': {'sublist': {'大安': 'daanshi', '镇赉': 'zhenlaixian', '洮南': 'taonan', '白城周边': 'bcqita', '洮北': 'taobei', '白城': 'baichengshi', '通榆': 'tongyuxian'}, 'code': 'bc'}, '随县': {'sublist': {'其他': 'suixiaqt', '城区': 'suixiacq'}, 'code': 'suixia'}, '霍邱': {'sublist': {'户胡': 'huhu', '长集': 'changjiz', '新店': 'xindianz', '霍邱周边': 'huoqiuzb', '河口': 'hekouz', '姚李': 'yaoli', '周集': 'zhouji', '马店': 'madianz', '城关': 'chengguanz', '众兴': 'zongxing'}, 'code': 'hq'}, '舞钢': {'sublist': {'其他': 'wugangqt', '城区': 'wugangcq'}, 'code': 'wugang'}, '全国': {'sublist': {'北京': 'beijingshi', '上海': 'shanghaishi', '天津': 'tianjinshi', '广州': 'guangzhoushi', '深圳': 'shenzhenshi'}, 'code': 'quanguo'}, '榆林': {'sublist': {'府谷': 'fuguxian', '定边': 'dingbianxian', '其它': 'yls', '靖边': 'jingbianxian', '横山': 'hengshanx', '榆阳': 'yuyang', '佳县': 'sxjx', '绥德': 'suide', '神木': 'yulinshenmu', '米脂': 'mizhi'}, 'code': 'yl'}, '永州': {'sublist': {'冷水滩': 'lengshuitangqu', '宁远': 'ningyuan', '江永': 'jiangyong', '新田': 'xintian', '江华': 'jianghua', '祁阳': 'qiyangyz', '东安': 'donganxian', '道县': 'daoxiang', '蓝山': 'langshan', '零陵': 'linglingqu', '双牌': 'shuangpai'}, 'code': 'yongzhou'}, '老河口': {'sublist': {'其他': 'laohekouqt', '城区': 'laohekoucq'}, 'code': 'laohekou'}, '永城': {'sublist': {'其他': 'yongchengqt', '城区': 'yongchengcq'}, 'code': 'yongcheng'}, '南昌': {'sublist': {'东湖': 'donghu', '高新开发区': 'gaoxinkfq', '新建区': 'xinjian', '西湖': 'xihu', '红谷滩新区': 'honggutanxin', '小蓝经济开发区': 'ncxl', '昌北经济开发区': 'nccbjjkfq', '青山湖': 'qingshanhuqu', '青云谱': 'qingyunpu', '南昌周边': 'nanchang', '象湖': 'ncxianghu', '南昌县': 'nanchangxian', '湾里': 'wailiqu'}, 'code': 'nc'}, '衡水': {'sublist': {'故城': 'guchengxian', '冀州': 'jizhou', '景县': 'jingxian', '深州': 'hsshenzhou', '饶阳': 'raoyang', '武强': 'wuqiang', '阜城': 'fucheng', '武邑县': 'hswy', '安平': 'anping', '开发区': 'kaifq', '枣强': 'zaoqiang', '其他': 'hengshui', '桃城': 'taocheng'}, 'code': 'hs'}, '菏泽': {'sublist': {'郓城': 'hzychz', '单县': 'hezeshanxian', '曹县': 'hezecaoxian', '定陶': 'dingtao', '其它': 'hezeshi', '鄄城': 'juanchenghz', '开发区': 'hzkaifaqu', '牡丹': 'mudanqu', '东明': 'dongminghz', '成武': 'chengwu', '巨野': 'juyehz'}, 'code': 'heze'}, '衡阳': {'sublist': {'蒸湘': 'zhengxiang', '立新开发区': 'lixinkfq', '衡阳周边': 'hengyang', '石鼓': 'shigu', '雁峰': 'yanfeng', '南岳': 'nanyue', '珠晖': 'zhuhui', '华新开发区': 'huaxinkfq'}, 'code': 'hy'}, '上杭': {'sublist': {'其他': 'shanghangxianqt', '城区': 'shanghangxiancq'}, 'code': 'shanghangxian'}, '葫芦岛': {'sublist': {'绥中': 'suizhong', '龙港': 'longgangq', '北港工业区': 'beiganggongye', '建昌': 'jianchang', '南票': 'nanpiao', '开发区': 'hldkaifaqu', '兴城': 'xingcheng', '葫芦岛周边': 'huludaozhoubian', '连山': 'lianshan'}, 'code': 'hld'}, '娄底': {'sublist': {'冷水江': 'lengshuijiangshild', '新化': 'xinhuaxian', '娄星': 'louxingqu', '涟源': 'lianyuanshild', '娄底周边': 'loudizb', '双峰': 'shuangfengxianld'}, 'code': 'ld'}, '大同': {'sublist': {'浑源': 'hunyuanxian', '天镇': 'tianzhenxian', '大同': 'datongqu', '城区': 'chengquxian', '广灵': 'guanglingxian', '灵丘': 'lingqiuxian', '新荣': 'xinrongqu', '左云': 'zuoyunxian', '矿区': 'kuangqu', '阳高': 'yanggaoxian', '南郊': 'nanjiaoqu'}, 'code': 'dt'}, '衢州': {'sublist': {'龙游': 'longyouxian', '开化': 'kaihuaxian', '常山': 'changshanxian', '衢江': 'qujiangqu', '巨化': 'juhuaxian', '柯城': 'kechengqu', '江山': 'jiangshanshiqz'}, 'code': 'quzhou'}, '平凉': {'sublist': {'崇信': 'chongxinxian', '庄浪': 'zhuanglangxian', '泾川': 'jingchuanxian', '灵台': 'lingtaixian', '华亭': 'huatingxian', '崆峒': 'kongtongqu', '静宁': 'jingningxian'}, 'code': 'pl'}, '邓州': {'sublist': {'其他': 'dengzhouqt', '城区': 'dengzhoucq'}, 'code': 'dengzhou'}, '公主岭': {'sublist': {'怀德镇': 'huaidezhen', '范家屯': 'gzlfanjiatun', '公主岭': 'gongzhulingshiqu', '双城堡': 'shuangchengbao', '秦家屯': 'qinjiatun', '其他': 'gongzhulingshiqita', '大榆树镇': 'dayushuzhen'}, 'code': 'gongzhuling'}, '磐石': {'sublist': {'其他': 'panshiqt', '城区': 'panshicq'}, 'code': 'panshi'}, '芜湖': {'sublist': {'无为': 'whwuwei', '弋江': 'yijiang', '芜湖县': 'wuhuxian', '繁昌': 'fanchang', '三山': 'sanshan', '其他': 'wuhuqita', '鸠江': 'jiujiangqu', '镜湖': 'jinghu', '南陵': 'nanling'}, 'code': 'wuhu'}, '伦敦': {'sublist': {}, 'code': 'glgreaterlondon'}, '句容': {'sublist': {'其他': 'jurongqita', '城区': 'jurongchengqu'}, 'code': 'jurong'}, '枣庄': {'sublist': {'峄城': 'zzyicheng', '薛城': 'xuecheng', '山亭': 'shanting', '台儿庄': 'taierzhuang', '滕州': 'zaozhuangtengzhou', '市中区': 'shizhongqu', '其他': 'zaozhuangshi'}, 'code': 'zaozhuang'}, '景德镇': {'sublist': {'浮梁': 'fuliangxianjdz', '珠山': 'zhushanqu', '乐平市': 'jingdezhenleping', '昌江': 'changjiangqu'}, 'code': 'jdz'}, '其他': {'sublist': {'西藏': 'xizang', '湖南': 'hunan', '辽宁': 'liaoning', '青海': 'qinghai', '内蒙': 'neimenggu', '福建': 'fujian', '山东': 'shandong', '四川': 'sichuan', '河南': 'henan', '湖北': 'hubei', '海南': 'hainans', '江苏': 'jiangsu', '吉林': 'jilinsheng', '云南': 'yunnan', '安徽': 'anhui', '江西': 'jiangxi', '广西': 'guangxi', '宁夏': 'ningxia', '河北': 'hebei', '广东': 'guangdong', '新疆': 'xinjiang', '浙江': 'zhejiang'}, 'code': 'cn'}, '昆山': {'sublist': {'蓬朗镇': 'szplz', '老城区': 'laochengq', '陆家': 'lujias', '昆山周边': 'kunshansu', '巴城': 'chengxisu', '玉山城北': 'chengbeisu', '张浦': 'zhangpus', '周市': 'chengdongsu', '玉山城东': 'yushancd', '玉山城西': 'yushancx', '花桥': 'huaqiaos', '锦溪': 'szjx', '周庄': 'szzz', '淀山湖': 'szdsh', '千灯': 'qiandengs', '玉山城南': 'chengnansu'}, 'code': 'szkunshan'}, '祁阳': {'sublist': {'其他': 'qiyangqt', '城区': 'qiyangcq'}, 'code': 'qiyang'}, '茌平': {'sublist': {'信发街道': 'lcxfjd', '振兴街道': 'lczxjd'}, 'code': 'chiping'}, '武安': {'sublist': {'其他': 'wuanshiqita', '城区': 'wuanchengqu'}, 'code': 'wuan'}, '樟树': {'sublist': {'其他': 'zhangshuqt', '城区': 'zhangshucq'}, 'code': 'zhangshu'}, '香港': {'sublist': {'中西': 'zhongxi', '沙田': 'shatian', '九龙城': 'jiulongcheng', '观塘': 'guantang', '湾仔': 'wanzai', '离岛': 'lidao', '其它': 'xianggang', '屯门': 'tunmen', '荃湾': 'quanwan', '黄大仙': 'huangdaxian', '东区': 'dongqu'}, 'code': 'hk'}, '冠县': {'sublist': {'清泉街道': 'lcqqjd', '崇文街道': 'lccwjd', '烟庄街道': 'lcyzjd'}, 'code': 'guanxian'}, '金昌': {'sublist': {'金川': 'jinchangshiqu', '河西堡': 'hexibao', '永昌': 'yongchangxian'}, 'code': 'jinchang'}, '灌南': {'sublist': {'其他': 'guannanxianqita', '城区': 'guannanchengqu'}, 'code': 'guannan'}, '长宁': {'sublist': {'其他': 'changningxqt', '城区': 'changningxcq'}, 'code': 'changningx'}, '铜陵': {'sublist': {'铜陵县': 'tonglingx', '狮子山': 'shizishan', '铜陵周边': 'tonglingzhoubian', '郊区': 'jiaoq', '枞阳': 'zongyang', '铜官山': 'tongguanshan'}, 'code': 'tongling'}, '丹东': {'sublist': {'东港': 'donggang', '宽甸': 'kuandian', '元宝': 'yuanbao', '振兴': 'zhenxing', '凤城': 'fengchengdd', '振安': 'zhenan', '其他': 'dandongqita'}, 'code': 'dandong'}, '东京': {'sublist': {}, 'code': 'gltokyo'}, '汝州': {'sublist': {'临汝镇': 'linruzhen', '其他': 'ruzhoushiqita', '汝南街道': 'runanjiedao', '煤山街道': 'meishanjiedao'}, 'code': 'ruzhou'}, '潜江': {'sublist': {'广华街道': 'guanghuajd', '周矶街道': 'zhoujijiedao', '潜江周边': 'qianjiangzb', '杨市街道': 'yangshijiedao', '园林街道': 'yuanlinjiedao', '泽口街道': 'zekoujiedao'}, 'code': 'qianjiang'}, '桦甸': {'sublist': {'其他': 'huadianqt', '城区': 'huadiancq'}, 'code': 'huadian'}, '汶上': {'sublist': {'其他': 'wenshangqt', '城区': 'wenshangcq'}, 'code': 'wenshang'}, '合肥': {'sublist': {'高新': 'hfgaoxin', '滨湖新区': 'hfbinghu', '庐阳': 'luyang', '经开': 'hfjingkai', '北城新区': 'hfbcxq', '瑶海': 'yaohai', '合肥周边': 'hefei', '蜀山': 'shushanqu', '政务': 'hfzhengwu', '新站': 'hfxinzhan', '包河': 'baohe'}, 'code': 'hf'}, '郑州': {'sublist': {'二七': 'eqi', '管城区': 'guancheng', '中原': 'zhongyuan', '经开区': 'zzjingkaiq', '高新区': 'zzgaoxin', '郑州周边': 'zhengzhou', '航空港': 'zzhkg', '上街': 'shangjiequzz', '金水': 'jinshui', '惠济': 'huiji', '郑东新区': 'zhengdongxinqu'}, 'code': 'zz'}, '鄂尔多斯': {'sublist': {'其它': 'eerduosi', '杭锦旗': 'hangjinqi', '东胜': 'dongshengqu', '达拉特旗': 'dalateqi', '鄂托克前旗': 'etuokeqianqi', '准格尔旗': 'zhungeerqi', '康巴什区': 'kangbsq', '鄂托克旗': 'etuokeqi', '乌审旗': 'wushenqi', '伊金霍洛旗': 'yijinhuoluoqi'}, 'code': 'erds'}, '瓦房店': {'sublist': {'东岗镇': 'donggangzhen', '复州城镇': 'fuzhoucheng', '瓦房店': 'wafangdianshi', '得利寺镇': 'delisi', '老虎屯镇': 'laohutun', '太阳街道': 'taiyangjie', '其他': 'wafangdianqita', '长兴岛': 'changxingdao'}, 'code': 'wfd'}, '京山': {'sublist': {'其他': 'jingshanxianqt', '城区': 'jingshanxiancq'}, 'code': 'jingshanxian'}, '射洪': {'sublist': {'其他': 'shehongxianqt', '城区': 'shehongxiancq'}, 'code': 'shehongxian'}, '随州': {'sublist': {'随县': 'suixiansz', '随州周边': 'suizhouzb', '曾都': 'zengduqu', '广水': 'guangshuishisz'}, 'code': 'suizhou'}, '黔东南': {'sublist': {'台江': 'taijiangx', '剑河': 'jianhe', '从江': 'congjiang', '天柱': 'tianzhux', '黎平': 'liping', '锦屏': 'jinpingx', '丹寨': 'danzhai', '黔东南周边': 'qdnzhoubian', '凯里': 'kaili', '黄平': 'huangping', '镇远': 'zhenyuan', '施秉': 'shibing', '雷山': 'leishan', '三穗': 'sansui', '榕江': 'rongjiang', '岑巩': 'cengong', '麻江': 'majiang'}, 'code': 'qdn'}, '仁怀': {'sublist': {'坛厂街道': 'tanchangjiedao', '中枢街道': 'zhongshujiedao', '鲁班街道': 'lubanjiedao', '其他': 'renhuaishiqita', '苍龙街道': 'canglongjiedao', '盐津街道': 'yanjinjiedao'}, 'code': 'renhuaishi'}, '周口': {'sublist': {'太康': 'taikangzk', '西华': 'xihua', '商水': 'shangshuizk', '郸城': 'dancheng', '扶沟': 'fugou', '淮阳': 'huaiyang', '沈丘': 'shenqiuzk', '川汇': 'chuanhui', '鹿邑': 'luyizk', '其他': 'zhoukou', '项城市': 'zhoukouxiangcheng'}, 'code': 'zk'}, '驻马店': {'sublist': {'西平': 'xiping', '汝南': 'runan', '遂平': 'suiping', '确山': 'queshan', '上蔡': 'shangcai', '新蔡': 'xincai', '平舆': 'pingyu', '正阳': 'zhengyangxian', '驿城': 'yichengqu', '其他': 'zhumadian', '泌阳': 'biyang'}, 'code': 'zmd'}, '防城港': {'sublist': {'东兴': 'dongxings', '上思': 'shangshi', '防城': 'fangcheng', '港口': 'gangkou', '防城港周边': 'fangchenggangzhoubian'}, 'code': 'fcg'}, '绵阳': {'sublist': {'游仙': 'youxian', '经开区': 'jingkaiqu', '三台县': 'santaixian', '绵阳周边': 'mianyangshi', '科创园区': 'kechuangyuanqu', '涪城': 'fuchengqu', '江油': 'jiangyou', '高新区': 'mygaoxinqu'}, 'code': 'mianyang'}, '辽源': {'sublist': {'东辽': 'dongliao', '西安区': 'liaoyuanxaq', '龙山': 'longshan', '东丰': 'dongfengxian', '其它': 'liaoyuanqita'}, 'code': 'liaoyuan'}, '石家庄': {'sublist': {'井陉矿区': 'jingjingkuangqu', '新华': 'sjzxinhua', '正定': 'zhengdingxian', '长安': 'changan', '石家庄周边': 'shijiazhuang', '开发区': 'sjzkaifaqu', '藁城': 'gaocheng', '桥西': 'qiaoxi', '裕华': 'yuhua', '鹿泉': 'luquan', '栾城': 'luanchengxian', '桥东': 'qiaodong'}, 'code': 'sjz'}, '长岭': {'sublist': {'其他': 'changlingxianqt', '城区': 'changlingxiancq'}, 'code': 'changlingxian'}, '吉林': {'sublist': {'磐石': 'panshijl', '船营': 'chuanying', '龙潭': 'longtan', '丰满': 'fengman', '吉林周边': 'jljilin', '舒兰': 'shulan', '蛟河': 'jiaohe', '永吉': 'yongj', '昌邑': 'changyi', '桦甸': 'huadianjl'}, 'code': 'jl'}, '涉县': {'sublist': {'其他': 'shexianqt', '城区': 'shexiancq'}, 'code': 'shexian'}, '平顶山': {'sublist': {'新华': 'xinhuaqu', '平顶山周边': 'pingdingshan', '湛河': 'zhanhe', '舞钢': 'wugangpds', '石龙': 'shilong', '汝州市': 'pingdingshanruzhou', '卫东': 'weidong'}, 'code': 'pds'}, '吕梁': {'sublist': {'临县': 'lvlianglx', '兴县': 'lvliangxx', '柳林': 'liulinll', '中阳': 'zhongyang', '孝义': 'xiaoyill', '其他': 'lvliangshi', '离石': 'lishi', '文水': 'wenshui', '交城': 'jiaocheng', '交口县': 'lvliangjkx', '方山县': 'lvliangfsx', '石楼县': 'lvliangslx', '岚县': 'lvlianglanxian', '汾阳': 'fenyang'}, 'code': 'lvliang'}, '襄阳': {'sublist': {'高新区': 'gaoxq', '鱼梁洲': 'yuliangz', '襄州': 'xiangyangqu', '宜城': 'yichengshixf', '枣阳市': 'xiangyagnzaoyang', '樊城': 'xfxiangcheng', '老河口': 'laohekouxf', '襄阳周边': 'xiangfan', '襄城': 'xiangcheng'}, 'code': 'xf'}, '遂宁': {'sublist': {'遂宁周边': 'suiningzb', '射洪': 'shehongxiansn', '大英': 'dayingxian', '蓬溪': 'pengxixian', '安居': 'anjuqu', '船山': 'chuanshanqu'}, 'code': 'suining'}, '海丰': {'sublist': {'鹅埠': 'ebu', '小漠': 'xiaomo', '公平镇': 'gongpingzhen', '平东': 'pingdong', '公平': 'gongping', '城东': 'chengdongs', '联安': 'lianan', '大湖': 'dahu', '海丰周边': 'qitahf', '莲花山': 'lianhuashan', '联安镇': 'liananzhen', '附城': 'fuchengs', '可塘': 'ketang', '附城镇': 'fuchengzhen', '海城': 'xianchenghf', '可塘镇': 'ketangzhen', '陶河镇': 'taohezhen', '海城镇': 'haichengzhen', '赤坑镇': 'chikengzhen', '赤坑': 'chikeng', '黄羌': 'huangqiang', '陶河': 'taohe', '梅陇镇': 'meilongzhen', '梅陇': 'meilong', '鲘门': 'houmen', '其他': 'haifengxianqita', '赤石': 'chishi'}, 'code': 'haifengxian'}, '兴化': {'sublist': {'兴化市区': 'xinghuashiqu', '其它': 'xinghuaqita'}, 'code': 'xinghuashi'}, '天水': {'sublist': {'甘谷': 'ganguxin', '张家川': 'zhangjiachun', '天水': 'tianshuishi', '秦安': 'qinanxian', '清水': 'qingshuixian', '麦积': 'maijiqu', '武山': 'wushanxian', '秦州': 'qinzhouqu'}, 'code': 'tianshui'}, '阿克苏': {'sublist': {'阿瓦提': 'awatixian', '阿克苏市': 'aksakss', '新和': 'xinhexian', '温宿': 'wensuxian', '乌什': 'wushixian', '拜城': 'baichengxian', '柯坪': 'kepingxian', '阿克苏周边': 'akeshuzhoubian', '沙雅': 'shayaxian', '库车': 'kuchexian'}, 'code': 'aks'}, '牡丹江': {'sublist': {'宁安': 'ninganshi', '林口县': 'mdjlkx', '穆棱': 'muling', '绥芬河': 'suifenhe', '东宁县': 'mdjdnx', '阳明': 'yangming', '东安': 'dongan', '海林': 'hailin', '其他': 'mudanjiang', '爱民': 'aimin', '西安': 'muxian'}, 'code': 'mdj'}, '吐鲁番': {'sublist': {'七泉湖镇': 'qiquanhuzhen', '吐鲁番周边': 'tulufanzhoubian', '老城路': 'laochenglu', '大河沿镇': 'daheyanzhen', '鄯善县': 'tlfssx', '托克逊县': 'tlftkxx', '高昌路': 'gaochanglu'}, 'code': 'tlf'}, '荆州': {'sublist': {'洪湖': 'honghu', '监利': 'jianli', '松滋': 'songzijz', '公安': 'gongan', '石首': 'shishou', '荆州': 'jingjingzhou', '江陵': 'jiangling', '其他': 'jingzhouqita', '沙市': 'shashiqu'}, 'code': 'jingzhou'}, '内江': {'sublist': {'威远': 'weiyuan', '资中': 'zizhong', '其它': 'neijiangshi', '隆昌': 'longchang', '东兴': 'dongxing', '市中区': 'shizhong'}, 'code': 'scnj'}, '沭阳': {'sublist': {'沭城镇': 'lysczhen'}, 'code': 'shuyang'}, '喀什': {'sublist': {'疏勒': 'shulexian', '叶城': 'yechengxian', '泽普': 'zepuxian', '塔什库尔干': 'tashikuergan', '莎车': 'shachexian', '喀什': 'kashishi', '麦盖提': 'maigaitixian', '喀什周边': 'kashizhoubian', '岳普湖': 'yuepuhuxian', '伽师': 'jiashixian', '英吉沙': 'yingjishaxian', '疏附': 'shufuxian', '巴楚': 'bachuxian'}, 'code': 'ks'}, '沈丘': {'sublist': {'其他': 'shenqiuqt', '城区': 'shenqiucq'}, 'code': 'shenqiu'}, '威海': {'sublist': {'乳山市': 'weihairushan', '经区': 'jingqu', '高区': 'gaoqu', '其他': 'weihaishi', '荣成': 'weihairongcheng', '环翠': 'huancui', '文登': 'wendeng'}, 'code': 'weihai'}, '郴州': {'sublist': {'临武': 'linwu', '宜章': 'yizhang', '北湖': 'beihuqu', '永兴': 'yongxingcz', '其它': 'chenzhoushi', '资兴': 'zixingcz', '桂阳': 'czguiyangcz', '嘉禾': 'jiahe', '苏仙': 'suxian'}, 'code': 'chenzhou'}, '广元': {'sublist': {'广元周边': 'guangyuanzhoubian', '青川': 'qingchuanxian', '剑阁': 'jiangexian', '苍溪': 'cangxixian', '元坝': 'yuanbaqu', '旺苍': 'wangcangqu', '朝天': 'chaotianqu', '利州': 'lizhouqu'}, 'code': 'guangyuan'}, '漳州': {'sublist': {'芗城': 'xiangchengqu', '云霄县': 'zzyxx', '东山': 'dongshanxian', '诏安': 'zhaoan', '漳浦': 'zhangpuzz', '华安县': 'zzhax', '长泰县': 'zzctx', '南靖县': 'zznjx', '平和': 'pinghe', '龙海市': 'zhangzhoulonghai', '角美': 'zzlckfq', '龙文': 'longwen', '其他': 'zhangzhoushi'}, 'code': 'zhangzhou'}, '台山': {'sublist': {'海宴': 'haiyanz', '大江': 'dajiang', '广海': 'guanghai', '赤溪': 'chixi', '白沙': 'baishaz', '北陡': 'beidou', '都斛': 'duhu', '深井': 'shenjing', '三合': 'sanhez', '端芬': 'duanfen', '台山周边': 'taishanzb', '冲蒌': 'chongwei', '川岛': 'chuandao', '斗山': 'doushan', '四九': 'sijiu'}, 'code': 'taishan'}, '迁安': {'sublist': {'其他': 'qiananshiqita', '城区': 'qiananchengqu'}, 'code': 'qianan'}, '秦皇岛': {'sublist': {'海港': 'haigang', '南戴河': 'ndh', '卢龙': 'lulong', '抚宁': 'funing', '青龙': 'qinglong', '昌黎': 'changli', '开发区': 'kfq', '北戴河': 'beidaihe', '其他': 'qinhuangdao', '山海关': 'shanhaiguan'}, 'code': 'qhd'}, '龙岩': {'sublist': {'漳平': 'zhangpingshi', '连城': 'lianchengxian', '长汀': 'changtingxian', '上杭': 'shanghangxianly', '武平': 'wupingxian', '永定': 'yongdingxian', '新罗': 'xinluoqu'}, 'code': 'ly'}, '祁东': {'sublist': {'其他': 'qidongxianqt', '城区': 'qidongxiancq'}, 'code': 'qidongxian'}, '盐城': {'sublist': {'阜宁': 'funingxianyc', '建湖': 'jianhuqu', '滨海': 'binhai', '响水': 'xiangshuiyc', '亭湖': 'tinghu', '盐都': 'yandou', '其他': 'yanchengshi', '东台': 'dongtaiqu', '射阳': 'sheyangyc', '大丰': 'dafengshi'}, 'code': 'yancheng'}, '山南': {'sublist': {'扎囊': 'zhanangxian', '乃东': 'naidongxian', '桑日': 'sangrixian', '贡嘎': 'gonggaxian', '琼结': 'qiongjiexian', '山南周边': 'shannanzhoubian'}, 'code': 'sn'}, '临猗': {'sublist': {'临晋镇': 'linjinzhen', '孙吉镇': 'sunjizhen', '北景乡': 'beijingxiang', '耽子镇': 'danzizhen', '七级镇': 'qijizhen', '角杯乡': 'jiaobeixiang', '嵋阳镇': 'emeizhen', '庙上乡': 'miaoshangxiang', '三管镇': 'sanguanzhen', '猗氏镇': 'yishizhen', '楚候乡': 'chuhouxiang', '北辛乡': 'beixinxiang', '东张镇': 'dongzhangzhen'}, 'code': 'linyixian'}, '温县': {'sublist': {'其他': 'wenxianqt', '城区': 'wenxiancq'}, 'code': 'wenxian'}, '宜昌': {'sublist': {'西陵': 'xiling', '远安': 'yuananxian', '宜都': 'yiduqu', '当阳': 'dangyangyc', '五峰': 'wufengxian', '枝江': 'zhijiangyc', '秭归': 'ziguixian', '点军': 'dianjun', '伍家岗': 'wujiagang', '夷陵': 'yiling', '宜昌周边': 'yichangqita', '葛洲坝': 'ycgzb', '猇亭': 'xiaoting', '东山': 'dongs', '长阳': 'changyang', '兴山': 'xingshanxian'}, 'code': 'yc'}, '安庆': {'sublist': {'宜秀': 'yixiu', '大观': 'daguanqu', '宿松': 'susong', '潜山': 'qianshanxian', '迎江': 'yingjiang', '怀宁': 'huaining', '其他': 'anqingqita', '桐城': 'tongchengshi', '岳西': 'yuexi'}, 'code': 'anqing'}, '海宁': {'sublist': {'钱塘江北岸': 'qiantjba', '西山公园': 'xsgy', '盐官古城': 'yanggc', '海宁潮': 'hainc', '海宁周边': 'hainzb'}, 'code': 'haining'}, '汉中': {'sublist': {'佛坪县': 'hanzhongfpx', '南郑': 'nanzheng', '留坝县': 'hanzhonglbx', '洋县': 'yangxian', '西乡': 'xixiang', '汉台': 'hantai', '宁强县': 'hanzhongnqx', '镇巴县': 'hanzhongzbx', '城固': 'chenggu', '其他': 'hanzhongshi', '勉县': 'mianxian', '略阳': 'lueyang'}, 'code': 'hanzhong'}, '南城': {'sublist': {'其他': 'nanchengxqt', '城区': 'nanchengxcq'}, 'code': 'nanchengx'}, '招远': {'sublist': {'大秦家': 'daqinjia', '其他': 'zhaoyuanshiqita', '梦芝': 'mengzhi', '泉山': 'zhaoyuanquanshan', '罗峰': 'luofeng'}, 'code': 'zhaoyuan'}, '怀化': {'sublist': {'鹤城': 'hecheng', '会同': 'huitong', '中方': 'zhongfang', '其它': 'huaihua', '沅陵': 'yuanling', '洪江': 'hongjiang', '溆浦': 'xupuxian', '辰溪': 'chenxi'}, 'code': 'hh'}, '昌都': {'sublist': {'丁青': 'dingqingxian', '贡觉': 'gongjuexian', '类乌齐': 'leiwuqixian', '江达': 'jiangdaxian', '昌都': 'changduxian', '昌都周边': 'changduzhoubian'}, 'code': 'changdu'}, '镇江': {'sublist': {'镇江新区': 'zhenjiangxinqu', '京口': 'jingkou', '丹阳': 'danyangqu', '扬中': 'yangzhongsq', '句容': 'zjjurong', '其他': 'zhenjiangqita', '丹徒': 'dantu', '润州': 'runzhou'}, 'code': 'zj'}, '神农架': {'sublist': {'阳日镇': 'yangrizhen', '红坪镇': 'hongpingzhen', '神农架周边': 'shennongjiazb', '木鱼镇': 'muyuzhen', '松柏镇': 'songbozhen'}, 'code': 'snj'}, '曼谷': {'sublist': {}, 'code': 'glbangkok'}, '瑞安': {'sublist': {'仙降': 'raxianjiang', '安阳': 'raanyang', '东山': 'radongshan', '龙湖': 'ralonghu', '玉海': 'rayuhai', '曹村': 'racaocun', '锦湖': 'rajinhu', '汀田': 'ratingtian', '碧山': 'rabishan', '飞云': 'rafeiyun', '马屿': 'ramayu', '上望': 'rashangwang', '瑞安周边': 'raruianzhoubian', '塘下': 'ratangxia', '平阳坑': 'rapingyangkeng', '陶山': 'rataoshan', '湖岭': 'rahuling', '莘塍': 'raxinsheng', '潘岱': 'rapandai'}, 'code': 'ruiancity'}, '陇南': {'sublist': {'文县': 'wenx', '两当': 'liangdang', '成县': 'chengx', '武都': 'wudu', '宕昌': 'dangchang', '陇南周边': 'longnanzhoubian', '徽县': 'huix'}, 'code': 'ln'}, '肥城': {'sublist': {'城区': 'feichengchengqu', '其他': 'feichengshiqita', '西城区': 'taianxcq', '北城区': 'taianbcq', '南城区': 'taianncq', '中心区': 'taianzxq', '新城街道': 'xincjd', '东城区': 'taiandcq', '肥城周边': 'feiczb', '老城街道': 'laocjd'}, 'code': 'feicheng'}, '无锡': {'sublist': {'北塘': 'beitang', '新区': 'wxxinqu', '无锡周边': 'wuxi', '惠山': 'huishanq', '南长': 'nanchangqu', '崇安': 'chongan', '江阴': 'jiangyin', '滨湖': 'binhu', '锡山': 'xishanqu', '宜兴': 'yixingshi'}, 'code': 'wx'}, '扬州': {'sublist': {'维扬': 'weiyangqu', '邗江': 'hanjiang', '宝应': 'yangzhoubaoying', '仪征': 'yizheng', '江都': 'jiangdou', '广陵': 'guangling', '扬州周边': 'yangzhouqita', '高邮': 'gaoyou'}, 'code': 'yz'}, '南通': {'sublist': {'开发区': 'kfaqu', '南通周边': 'nantong', '港闸': 'gangzha', '崇川': 'chongchuan', '如皋': 'rugaoqu', '海安': 'haianqu', '海门': 'haimenqu', '如东': 'rudongqu', '通州': 'tongzhou', '启东': 'qidongqu'}, 'code': 'nt'}, '迪拜': {'sublist': {}, 'code': 'gldubai'}, '鸡西': {'sublist': {'滴道': 'didaoqu', '鸡东': 'jidongxian', '梨树': 'lishuqu', '鸡冠': 'jiguanqu', '城子河': 'chengzihequ', '虎林': 'hulinshi', '密山': 'mishanshi', '麻山': 'mashanquxian', '恒山': 'hengshanqu'}, 'code': 'jixi'}, '邢台': {'sublist': {'南和': 'nanhe', '平乡': 'pingxiangxian', '南宫': 'nangong', '邢台县': 'xingtaixian', '其他': 'xingtai', '桥东': 'qiaodongqu', '清河': 'xtqinghe', '沙河': 'shaheshixt', '桥西': 'qiaoxiqu'}, 'code': 'xt'}, '泉州': {'sublist': {'石狮': 'shishiqu', '德化': 'dehuaxian', '南安': 'nananqunew', '金门县': 'qzjmx', '泉州周边': 'quanzhouzb', '安溪': 'anxixianqz', '惠安': 'huianxian', '晋江': 'jinjiangqunew', '桥南片区': 'qiaonanpianqu', '鲤城': 'qzlicheng', '洛江': 'luojiang', '台商投资区': 'qztstzq', '丰泽': 'fengze', '永春': 'yongchunxianqz', '泉港': 'quangang'}, 'code': 'qz'}, '莱芜': {'sublist': {'高新区': 'gaoxinquq', '钢城': 'gangchengqu', '雪野旅游区': 'xueyelvyou', '莱城': 'laichengqu'}, 'code': 'lw'}, '柳州': {'sublist': {'城中': 'chengzhongqu', '三江': 'sanjiangxian', '融安': 'ronganxian', '柳城': 'liuchengxian', '柳江': 'liujiangxian', '柳南': 'liunanqu', '鱼峰': 'yufengqu', '鹿寨': 'luzhaixian', '柳北': 'liubeiqu', '融水': 'rongshuixian'}, 'code': 'liuzhou'}, '齐齐哈尔': {'sublist': {'碾子山': 'nianzishan', '建华': 'jianhua', '龙沙': 'longsha', '其它': 'qqhe', '讷河': 'nehe', '铁锋': 'tiefeng', '昂昂溪': 'angangxi', '泰来': 'tailai', '富拉尔基': 'fulaerji', '梅里斯': 'meilisi'}, 'code': 'qqhr'}, '新沂': {'sublist': {'其它': 'xinyiqita', '新沂市区': 'xinyishiqu'}, 'code': 'xinyishi'}, '灵宝': {'sublist': {'其他': 'lingbaoshiqita', '城区': 'lingbaochengqu'}, 'code': 'lingbaoshi'}, '大连': {'sublist': {'西岗': 'xigang', '金州': 'jinzhouqu', '开发区': 'daliankfq', '庄河': 'zhuanghe', '普兰店': 'dlpulandian', '沙河口': 'shahekou', '瓦房店': 'wafangdian', '旅顺': 'lvshunkou', '甘井子': 'ganjingziqu', '大连周边': 'dalian', '中山': 'zhongshanqu', '高新园': 'gaoxinyuanqu'}, 'code': 'dl'}, '温州': {'sublist': {'瑞安': 'ruian', '瓯海': 'ouhai', '温州周边': 'wenzhou', '文成': 'wenchengxian', '洞头': 'dongtouxian', '泰顺': 'taishunxian', '乐清': 'yueqing', '永嘉': 'yongjiaxian', '苍南县': 'wenzhoucangnan', '龙湾': 'longwan', '平阳': 'pingyangxianwz', '鹿城': 'lucheng'}, 'code': 'wz'}, '清远': {'sublist': {'清新': 'qingxinxian', '英德': 'yingdeshi', '阳山': 'yangshanxian', '佛冈': 'fogangxian', '连南': 'liannanxian', '清城': 'qingchengqu', '连山': 'lianshanxian', '连州': 'lianzhoushi'}, 'code': 'qingyuan'}, '河池': {'sublist': {'河池学院': 'hechixueyuan', '凤山': 'fengshanxian', '大化': 'dahuaxian', '宜州': 'yizhoushi', '罗城': 'luochengxian', '都安': 'duanxian', '天峨': 'tianexian', '南丹': 'nandanxian', '环江': 'huanjiangxian', '金城江': 'jinchengjianqu', '巴马': 'bamaxian', '东兰': 'donglanxian'}, 'code': 'hc'}, '鄂州': {'sublist': {'华容': 'huarongqu', '梁子湖': 'liangzihuqu', '鄂州周边': 'erzhouzb', '鄂城区': 'erchengqu'}, 'code': 'ez'}, '临沂': {'sublist': {'临沂周边': 'linyishi', '沂水': 'yishui', '河东': 'hedongqu', '兰山': 'lanshanqu', '开发区': 'lykaifaqu', '兰陵': 'cangshanxian', '费县': 'feixian', '平邑': 'pingyily', '沂南': 'yinanxianly', '高新区': 'lygaoxinqu', '北城新区': 'lybcxqu', '临沭': 'linshu', '罗庄': 'luozhuang', '蒙阴': 'mengyinxian', '郯城': 'tanchengly', '莒南': 'junan'}, 'code': 'linyi'}, '鄢陵': {'sublist': {'陈店乡': 'chendianxiang', '彭店乡': 'pengdianxiang', '只乐乡': 'zhilexiang', '南坞乡': 'nanwuxiang', '柏梁镇': 'boliangzhen', '马坊乡': 'mafangxiang', '张桥乡': 'zhangqiaoxiang', '陶城乡': 'taochengxiang', '马栏镇': 'malanzhen', '望田镇': 'wangtianzhen', '大马乡': 'damaxiang', '安陵镇': 'anlingzhen'}, 'code': 'yanling'}, '丹阳': {'sublist': {'丹阳市区': 'danyangshiqu', '其它': 'danyangqita'}, 'code': 'danyang'}, '商洛': {'sublist': {'山阳': 'shanyangx', '商南': 'sangnan', '柞水': 'zuoshui', '洛南': 'luonan', '镇安': 'zhenanx', '丹凤': 'danfeng', '商洛周边': 'sangluozhoubian', '商州': 'shangzhou'}, 'code': 'sl'}, '日土': {'sublist': {}, 'code': 'rituxian'}, '永兴': {'sublist': {'其他': 'yongxingqt', '城区': 'yongxingcq'}, 'code': 'yongxing'}, '克孜勒苏': {'sublist': {'阿合奇': 'aheqixian', '阿图什': 'atushishi', '克孜勒苏周边': 'kezileshuzhoubian', '乌恰': 'wuqiaxian'}, 'code': 'kzls'}, '醴陵': {'sublist': {'来龙门街道': 'lailongmenjiedao', '国瓷街道': 'guocijiedao', '阳三石街道': 'yangsanshijiedao', '其他': 'lilingqita', '白兔潭镇': 'baitutanzhen', '仙岳山街道': 'xianyueshanjiedao'}, 'code': 'liling'}, '凤城': {'sublist': {'其他': 'fengchengqt', '城区': 'fengchengcq'}, 'code': 'fengcheng'}, '十堰': {'sublist': {'竹山': 'zhushan', '张湾': 'zhangwan', '郧阳区': 'yunxian', '房县': 'fangxian', '武当山': 'sywds', '郧西': 'yunxixian', '竹溪': 'zhuxi', '丹江口': 'danjiangkou', '十堰周边': 'shiyanshi', '茅箭': 'maojian', '白浪经济开发区': 'sybljjkfq'}, 'code': 'shiyan'}, '鹤岗': {'sublist': {'南山': 'nanshanquq', '绥滨': 'suibinxian', '向阳': 'xiangyangquq', '东山': 'dongshanqu', '工农': 'gongnongqu', '萝北': 'luobeixian', '兴安': 'xinganqu', '兴山': 'xingshanqu'}, 'code': 'hegang'}, '新泰': {'sublist': {'府前大街': 'taianfqdj', '杏山路': 'taianxsl', '体育场': 'taiantiyuchang', '青云街道': 'qingyjd', '新泰周边': 'xintzb', '平阳河': 'taianpyh', '青云大厦': 'taianqyds', '其他': 'xintaishiqita', '客运中心': 'taiankyzx', '小协': 'taianxx', '新汶街道': 'xinwenjd'}, 'code': 'xintai'}, '三沙': {'sublist': {'中沙群岛': 'zsqd', '南沙群岛': 'nsqd', '西沙群岛': 'xsqd'}, 'code': 'sansha'}, '库尔勒': {'sublist': {'和静': 'hejx', '焉耆': 'yanqx', '博湖': 'byglbh', '库尔勒': 'kuerleshi', '和硕': 'byglhs', '若羌': 'byglrq', '且末': 'bygljm', '巴州周边': 'bazhouzhoubian', '轮台': 'luntx', '尉犁': 'weilx'}, 'code': 'kel'}, '首尔': {'sublist': {}, 'code': 'glseoul'}, '宿迁': {'sublist': {'宿豫/宿城': 'sucheng', '沭阳': 'sqshuyang', '泗洪县': 'suqiansihong', '泗阳县': 'suqiansiyang'}, 'code': 'suqian'}, '梨树县': {'sublist': {'其他': 'lishuqt', '城区': 'lishucq'}, 'code': 'lishu'}, '大悟': {'sublist': {'其他': 'dawuqt', '城区': 'dawucq'}, 'code': 'dawu'}, '弥勒': {'sublist': {'其他': 'milexianqt', '城区': 'milexiancq'}, 'code': 'milexian'}, '七台河': {'sublist': {'勃利': 'boli', '新兴': 'xinxing', '茄子河': 'qiezihe', '七台河周边': 'qitaihezb', '桃山': 'taoshan'}, 'code': 'qth'}, '沙河': {'sublist': {'其他': 'shaheshiqt', '城区': 'shaheshicq'}, 'code': 'shaheshi'}, '沧州': {'sublist': {'新华': 'czxinhua', '沧县': 'cangxiancz', '献县': 'czxianxian', '黄骅': 'huanghuacz', '孟村': 'mengcun', '海兴': 'haixing', '泊头': 'botou', '任丘市': 'cangzhourenqiu', '吴桥': 'wuqiao', '盐山': 'yanshanxian', '青县': 'qingxian', '运河': 'yunhe', '河间': 'hejiancz', '南皮': 'nanpi', '其他': 'cangzhoushi', '肃宁': 'suning', '东光': 'dongguang'}, 'code': 'cangzhou'}, '淄博': {'sublist': {'开发区': 'kaifaquyu', '临淄': 'linzi', '其他': 'zibo', '高青': 'gaoqingxian', '博山': 'boshan', '周村': 'zhoucun', '沂源': 'yiyuanxianzb', '桓台县': 'zibohengtai', '淄川': 'zichuan', '张店': 'zhangdian'}, 'code': 'zb'}, '无为': {'sublist': {'其他': 'wuweiqita', '城区': 'wuweichengqu'}, 'code': 'wuweixian'}, '林芝': {'sublist': {'林芝周边': 'linzhizb', '朗县': 'langxian', '察隅': 'chayuxian', '米林': 'milinxian', '波密': 'bomixian', '林芝': 'linzhixian', '八一镇': 'bayizhen', '墨脱': 'motuoxian', '工布江达': 'gongbujiangdax'}, 'code': 'linzhi'}, '本溪': {'sublist': {'其它': 'benxishi', '明山': 'mingshan', '平山': 'pingshanqu', '本溪县': 'bxbenxi', '桓仁': 'huanren', '南芬': 'nanfen', '溪湖': 'bxxihu'}, 'code': 'benxi'}, '厦门': {'sublist': {'海沧': 'haicang', '杏林': 'xmxl', '湖里': 'huli', '翔安': 'xiangan', '集美': 'jimei', '厦门周边': 'xiamenzhoubian', '思明': 'siming', '同安': 'tongan'}, 'code': 'xm'}, '北票': {'sublist': {'其他': 'beipiaoqt', '城区': 'beipiaocq'}, 'code': 'beipiao'}, '南阳': {'sublist': {'淅川': 'xichuanxian', '社旗': 'sheqixian', '邓州': 'dengzhouny', '镇平': 'zhenpingxian', '新野': 'xinyeny', '南召': 'nanzhaoxian', '西峡': 'xixiax', '宛城': 'wancheng', '唐河': 'tanghe', '卧龙': 'wolong', '油田': 'youtianqu', '其他': 'nanyang', '内乡': 'neixiangxian', '方城': 'fangchengxian', '桐柏': 'tongbaixian'}, 'code': 'ny'}, '曲靖': {'sublist': {'麒麟': 'qilinqu', '师宗': 'shizongxian', '陆良': 'luliangxian', '沾益': 'zhanyixian', '罗平': 'luopingxian', '会泽': 'huizexian', '宣威': 'xuanwushiqj', '马龙': 'malongxian', '富源': 'qjfuyuanxian'}, 'code': 'qj'}, '孝昌': {'sublist': {'其他': 'xiaochangqt', '城区': 'xiaochangcq'}, 'code': 'xiaochang'}, '中卫': {'sublist': {'海原': 'haiyuan', '沙坡头': 'shapotou', '中卫周边': 'zhongweizhoubian', '中宁': 'zhongning'}, 'code': 'zw'}, '纽约': {'sublist': {}, 'code': 'glnewyork'}, '清徐': {'sublist': {'杨房乡': 'yangfangxiang', '西谷乡': 'xiguxiang', '王答乡': 'wangdaxiang', '集义乡': 'jiyixiang', '东于镇': 'dongyuzhen', '马峪乡': 'mayuxiang', '柳杜乡': 'liuduxiang', '清源镇': 'qingyuanzhen', '高花乡': 'gaohuaxiang', '盂封镇': 'yufengzhen', '清徐周边': 'qingxuzb', '徐沟镇': 'xugouzhen'}, 'code': 'qingxu'}, '舟山': {'sublist': {'定海': 'dinghaiqu', '普陀': 'putuoqu', '嵊泗': 'shengsixian', '岱山': 'daishanxian'}, 'code': 'zhoushan'}, '分宜': {'sublist': {'其他': 'fenyiqt', '城区': 'fenyicq'}, 'code': 'fenyi'}, '乐陵': {'sublist': {'其他': 'lelingqt', '城区': 'lelingcq'}, 'code': 'leling'}, '新野': {'sublist': {'其他': 'xinyeqt', '城区': 'xinyecq'}, 'code': 'xinye'}, '通化': {'sublist': {'集安': 'jian', '梅河口': 'meihekouth', '辉南': 'huinanx', '二道江': 'erdaojiang', '通化周边': 'tonghuazhoubian', '东昌': 'dongchang', '通化': 'tonghuax', '柳河': 'liuhe'}, 'code': 'th'}, '五指山': {'sublist': {'毛阳镇': 'maoyang', '番阳镇': 'fanyang', '冲山镇': 'chongshan', '五指山周边': 'wuzhishanzb', '南圣镇': 'nansheng'}, 'code': 'wzs'}, '梁山': {'sublist': {'其他': 'liangshanxqt', '城区': 'liangshanxcq'}, 'code': 'liangshanx'}, '桂林': {'sublist': {'秀峰': 'xiufeng', '叠彩': 'diecai', '象山': 'xiangshan', '七星': 'qixing', '桂林周边': 'guilin', '八里街': 'balijie', '兴安县': 'xanxian', '阳朔县': 'yangsx', '灵川': 'lingchuanc', '临桂': 'linguic', '雁山': 'yanshan'}, 'code': 'gl'}, '信阳': {'sublist': {'羊山新区': 'yangshanxinqu', '潢川': 'huangchuanxian', '罗山': 'luoshanxian', '淮滨': 'huaibinxianxy', '新县': 'xinxian', '息县': 'xixianqu', '浉河': 'shihequ', '商城': 'shangchengquq', '固始': 'gushixiangs', '光山': 'guangshanxian', '平桥': 'pingqiaoqu', '信阳市区': 'xinyangshi'}, 'code': 'xy'}, '揭阳': {'sublist': {'普宁': 'puning', '揭西': 'jiexi', '榕城': 'rongchengqu', '揭东': 'jiedong', '其他': 'jieyang', '惠来': 'huilai'}, 'code': 'jy'}, '齐河': {'sublist': {'其他': 'qiheqt', '城区': 'qihecq'}, 'code': 'qihe'}, '柳林': {'sublist': {'其他': 'liulinqt', '城区': 'liulincq'}, 'code': 'liulin'}, '伊犁': {'sublist': {'阿勒泰': 'aletaishi', '奎屯': 'kuitunshi', '乌苏': 'wusushi', '塔城': 'tachengshi', '伊犁周边': 'yilizhoubian', '伊宁': 'yiningshi'}, 'code': 'yili'}, '赵县': {'sublist': {'北王里镇': 'beiwanglizhen', '韩村镇': 'hancunzhen', '新寨店镇': 'xinzhaidianzhen', '赵州镇': 'zhaozhouzhen', '王西章乡': 'wangxizhangxiang', '谢庄乡': 'xiezhuangxiang', '前大章乡': 'qiandazhangxiang', '南柏舍镇': 'nanbaishezhen', '沙河店镇': 'shahedianzhen', '高村乡': 'gaocunxiang', '范庄镇': 'fanzhuangzhen'}, 'code': 'zx'}, '蓬莱': {'sublist': {'紫荆山街道': 'zijingshanjiedao', '其他': 'penglaishiqita', '登州街道': 'dengzhoujiedao', '新港街道': 'xingangjiedao'}, 'code': 'penglai'}, '神木': {'sublist': {'神木镇': 'shenmuzhen', '其他': 'shenmuxianqita', '大柳塔镇': 'daliutazhen'}, 'code': 'shenmu'}, '东方': {'sublist': {'新龙镇': 'xinlong', '大田镇': 'datian', '感城镇': 'gancheng', '东方周边': 'dongfangzb', '八所镇': 'basuo', '三家镇': 'sanjia', '板桥镇': 'banqiaoz', '东河镇': 'donghez', '四更镇': 'sigeng'}, 'code': 'df'}, '银川': {'sublist': {'其它': 'yinchuanqita', '西夏': 'xixia', '永宁': 'yongningxian', '贺兰': 'helan', '灵武': 'lingwu', '兴庆': 'xingqing', '金凤': 'jinfeng'}, 'code': 'yinchuan'}, '清镇': {'sublist': {'其他': 'qingzhenqt', '城区': 'qingzhencq'}, 'code': 'qingzhen'}, '聊城': {'sublist': {'临清县': 'liaochenglinqing', '东阿': 'donga', '开发区': 'lckfq', '东昌府': 'dongchangfu', '莘县': 'shenxianlc', '茌平县': 'liaochengchiping', '阳谷': 'yanggulc', '其他': 'liaocheng', '高唐': 'gaotanglc', '冠县': 'guanxianlc'}, 'code': 'lc'}, '晋城': {'sublist': {'沁水': 'qinshui', '泽州': 'zezhoujc', '城区': 'chengqu', '开发区': 'kaifa', '陵川': 'lingchuan', '高平': 'gaopingjc', '其他': 'jinchengshi', '阳城': 'yangcheng'}, 'code': 'jincheng'}, '海东': {'sublist': {'化隆': 'lualong', '互助': 'huzhu', '海东周边': 'haidongzhoubian', '乐都': 'ledu', '民和': 'minhe', '平安': 'pingan', '循化': 'xunhua'}, 'code': 'haidong'}, '如东': {'sublist': {'如东市区': 'rudongshiqu', '其它': 'rudongqita'}, 'code': 'rudong'}, '东至': {'sublist': {'其他': 'dongzhiqita', '城区': 'dongzhichengqu'}, 'code': 'dongzhi'}, '禹州': {'sublist': {'鸿畅镇': 'hongchangzhen', '火龙镇': 'huolongzhen', '方山镇': 'fangshanzhen', '神后镇': 'shenhouzhen', '文殊镇': 'wenshuzhen', '夏都办': 'xiaduban', '颍川办': 'yingchuanban', '无梁镇': 'wuliangzhen', '钧台办': 'diaotaiban', '古城镇': 'guchengzhenz', '其他': 'qitaa', '梁北镇': 'liangbeizhen', '韩城办': 'hanchengban', '顺店镇': 'shundianzhen'}, 'code': 'yuzhou'}, '谷城': {'sublist': {'其他': 'guchengqt', '城区': 'guchengcq'}, 'code': 'gucheng'}, '新加坡': {'sublist': {}, 'code': 'glsingapore'}, '正定': {'sublist': {'新城铺镇': 'xinchengpu', '新安镇': 'xinan', '正定镇': 'zhengding', '南楼乡': 'nanlou', '南牛乡': 'nanniu', '曲阳桥乡': 'quyangqiao', '其他': 'zhengdingshi', '诸福屯镇': 'zhufutun', '北早现乡': 'beizaoxian'}, 'code': 'zd'}, '庆阳': {'sublist': {'镇原': 'zheny', '合水': 'heshui', '庆阳周边': 'qingyangzhoubian', '正宁': 'zhengning', '宁县': 'ningx', '庆城': 'qingcheng', '华池': 'huachi', '西峰': 'xifengq', '环县': 'huanx'}, 'code': 'qingyang'}, '普洱': {'sublist': {'镇沅': 'zhenyuanxian', '普洱周边': 'puerzhoubian', '宁洱': 'ningerxian', '景东': 'jingdongxian', '墨江': 'mojiangxian', '思茅': 'simaoqu', '景谷': 'jingguxian'}, 'code': 'pe'}, '仙桃': {'sublist': {'毛嘴': 'maozui', '剅河': 'douhe', '三伏潭': 'sanfutan', '胡场': 'huchang', '市区': 'xtsq', '郑场': 'zhengchang', '仙桃周边': 'xiantaozb', '长埫口': 'changshangkou'}, 'code': 'xiantao'}, '烟台': {'sublist': {'大学城': 'ytdaxue', '招远市': 'yantaizhaoyuan', '烟台周边': 'yantan', '高新区': 'ytgaoxin', '莱州': 'yantailaizhou', '长岛': 'changdao', '蓬莱市': 'yantaipenglai', '牟平': 'mouping', '龙口': 'longkouqu', '莱阳': 'laiyangyt', '芝罘': 'zhifu', '福山': 'fushan', '莱山': 'laishan', '开发区': 'ytkaifaqu', '栖霞': 'qixiayt', '海阳': 'hyang'}, 'code': 'yt'}, '临清': {'sublist': {'新华路街道': 'lcxhljd', '青年路街道': 'lcqnljd', '先锋路街道': 'lcxfljd', '大辛庄街道': 'lcdxzjd'}, 'code': 'linqing'}, '宁国': {'sublist': {'宁国市区': 'ningguoshiqu', '其它': 'ningguoqita'}, 'code': 'ningguo'}, '双峰': {'sublist': {'其他': 'shuangfengxianqt', '城区': 'shuangfengxiancq'}, 'code': 'shuangfengxian'}, '大丰': {'sublist': {'大中': 'dfdazhong', '南阳': 'nanyangz', '开发区': 'kaifaquz', '方强': 'fangqiang', '草堰': 'caoyan', '裕华': 'yuhuaz', '万盈': 'wanying', '大桥': 'daqiao', '新丰': 'xinfengz', '大丰周边': 'dafengzb', '白驹': 'baiju', '小海': 'xiaohai', '大丰港': 'dafenggang', '三龙': 'sanlong', '西团': 'xituan', '刘庄': 'liuzhuang'}, 'code': 'dafeng'}, '慈溪': {'sublist': {'慈溪市区': 'cixishiqu', '其它': 'cixiqita'}, 'code': 'cixi'}, '江山': {'sublist': {'其他': 'jiangshanshiqt', '城区': 'jiangshanshicq'}, 'code': 'jiangshanshi'}, '呼和浩特': {'sublist': {'呼和浩特周边': 'huhehaote', '如意开发区': 'ruyi', '清水河': 'qsh', '武川': 'wc', '玉泉': 'yuquan', '金山开发区': 'jinshankfq', '金川开发区': 'jinchuan', '和林格尔': 'hlge', '金桥开发区': 'jinqiaokfq', '回民': 'huimin', '赛罕': 'saihan', '托克托': 'tkt', '新城': 'xinchengqu', '土默特左': 'tmtz'}, 'code': 'hu'}, '龙海': {'sublist': {'其他': 'longhaishiqita', '城区': 'longhaichengqu'}, 'code': 'longhai'}, '安溪': {'sublist': {'其他': 'anxixianqt', '城区': 'anxixiancq'}, 'code': 'anxixian'}, '宁阳': {'sublist': {'西关': 'taianxg', '八仙桥街道': 'bxqjd', '东关': 'taiandg', '北关': 'taianbg', '宁阳县周边': 'ningyxzb', '县政府': 'taianxzf', '文庙街道': 'wenmjd', '四中': 'taiansz', '宁阳一中': 'taiannyyz', '南关': 'taiannanguan'}, 'code': 'ningyang'}, '东海': {'sublist': {'东海市区': 'donghaishiqu', '其它': 'donghaiqita'}, 'code': 'donghai'}, '济源': {'sublist': {'双桥街道': 'shuangqiaojd', '济水街道': 'jishuijd', '天坛街道': 'tiantanjd', '龙泉街道': 'longquanjd', '北海街道': 'beihaijd', '济源周边': 'jiyuanzb'}, 'code': 'jiyuan'}, '海盐': {'sublist': {'其他': 'haiyanqt', '城区': 'haiyancq'}, 'code': 'haiyan'}, '赤峰': {'sublist': {'元宝山': 'yuanbaoshan', '敖汉旗': 'aohanqi', '林西': 'linxi', '松山': 'songshan', '红山': 'hshan', '新城区': 'cfxinchengqu', '喀喇沁旗': 'keciqinqi', '其他': 'cfqita', '翁牛特旗': 'wengniuteqi', '宁城': 'ningchengxian'}, 'code': 'chifeng'}, '涿州': {'sublist': {'清凉寺街道': 'qingliangsijiedao', '双塔街道': 'shuangtajiedao', '桃园街道': 'taoyuanjiedao', '其他': 'tunzhouqita', '高新开发区': 'tzgaoxinkaifaqu'}, 'code': 'zhuozhou'}, '莆田': {'sublist': {'湄洲岛': 'meizhoudao', '荔城': 'lichengqu', '黄瓜岛': 'huangguadao', '秀屿': 'xiuyuqu', '涵江': 'hanjiangqu', '城厢': 'chengxiangqu', '南日岛': 'nanridao', '仙游': 'xianyouxian'}, 'code': 'pt'}, '孝感': {'sublist': {'云梦': 'yunmengxg', '大悟': 'dawuxg', '孝南': 'xiaonan', '安陆': 'anluxg', '汉川市': 'xiaoganhanchuan', '其他': 'xiaoganqita', '孝昌': 'xiaochangxg', '应城': 'yingcheng'}, 'code': 'xiaogan'}, '东营': {'sublist': {'垦利县': 'kenli', '东营区': 'dongying', '河口': 'hekou', '广饶': 'dongyingguangrao', '利津': 'lijindy', '其他': 'dongyingshi'}, 'code': 'dy'}, '海安': {'sublist': {'海安市区': 'haianshiqu', '其它': 'haianqita'}, 'code': 'haian'}, '咸阳': {'sublist': {'乾县': 'qianxian', '彬县': 'xybinxian', '三原': 'sanyuanxian', '旬邑': 'xunyixian', '兴平': 'sanpingshi', '礼泉': 'liquanxian', '秦都': 'qinduqu', '长武': 'changwuxian', '永寿': 'yongshouxian', '淳化': 'chunhuaxian', '泾阳': 'jingyangxian', '渭城': 'weichengquyu', '武功': 'wugongxian'}, 'code': 'xianyang'}, '沅江': {'sublist': {'其他': 'yuanjianqt', '城区': 'yuanjiangscq'}, 'code': 'yuanjiangs'}, '郓城': {'sublist': {'其他': 'hzycqt', '城区': 'hzyccq'}, 'code': 'hzyc'}, '天津': {'sublist': {'北辰': 'beichentj', '红桥': 'hongqiaotj', '河东': 'hedong', '塘沽': 'tanggu', '东丽': 'donglitj', '武清': 'wuqing', '开发区': 'tjkaifaqu', '津南': 'jinnantj', '天津周边': 'tianjin', '河西': 'hexi', '西青': 'xiqingtj', '蓟县': 'jianxiantj', '静海': 'jinghaiqu', '南开': 'nankai', '大港': 'dagang', '宝坻': 'baodi', '和平': 'heping', '宁河': 'ninghexian', '河北': 'hebeiqu', '汉沽': 'hangu'}, 'code': 'tj'}, '衡东': {'sublist': {'其他': 'hengdongqt', '城区': 'hengdongcq'}, 'code': 'hengdong'}, '沧县': {'sublist': {'其他': 'cangxianqt', '城区': 'cangxiancq'}, 'code': 'cangxian'}, '邹平': {'sublist': {'黛溪街道': 'daixijiedao', '西董街道': 'xidongjiedao', '黄山街道': 'huangshanjiedao', '好生街道': 'haoshengjiedao', '其他': 'zoupingxianqita', '高新街道': 'gaoxinjiedao'}, 'code': 'zouping'}, '香河': {'sublist': {'高速口': 'gaosukou', '好百年家具城': 'haobainianjiajucheng', '人民公园': 'renmingongyuanxh', '938总站': '938zongzhan', '新广场物美': 'xinguangchangwumei', '安平镇': 'anpingzhen', '三小二中': 'sanxiaoerzhong', '天下第一城': 'tianxiadiyicheng', '鑫亿隆文化广场': 'xinyilongwenhuaguangchang', '华联县医院': 'hualianxianyiyuan', '香河一中': 'xiangheyizhong'}, 'code': 'xianghe'}, '楚雄': {'sublist': {'永仁': 'yongrenxian', '大姚': 'dayaoxian', '姚安': 'yaoanxian', '牟定': 'moudingxian', '楚雄': 'chuxiongshi', '南华': 'nanhuaxian', '武定': 'wudingxian', '禄丰': 'lufengxian', '双柏': 'shuangbaixian', '元谋': 'yuanmouxian'}, 'code': 'cx'}, '伊川': {'sublist': {'其他': 'yichuanqt', '城区': 'yichuancq'}, 'code': 'yichuan'}, '慈利': {'sublist': {'其他': 'cilixianqt', '城区': 'cilixiancq'}, 'code': 'cilixian'}, '淮安': {'sublist': {'淮阴': 'huaiyin', '盱眙': 'xuyiha', '洪泽': 'hongze', '清浦': 'qingpuqu', '淮安区': 'chuzhouqu', '其他': 'huaian', '经济开发区': 'hajjkfq', '金湖': 'jinhuha', '清河': 'haqinghe', '涟水': 'lianshui'}, 'code': 'ha'}, '玉环': {'sublist': {'大麦屿街道': 'damaiyujiedao', '坎门街道': 'kanmenjiedao', '其他': 'yuhuanxianqita', '玉城街道': 'yuchengjiedao'}, 'code': 'yuhuan'}, '乐平': {'sublist': {'塔山街道': 'tashanjiedao', '洎阳街道': 'lpjiyangjiedao', '其他': 'lepingshiqita'}, 'code': 'lepingshi'}, '黄南': {'sublist': {'黄南周边': 'huangnanzhoubian', '同仁': 'tongren', '尖扎': 'jianzha', '泽库': 'zeku', '河南县': 'henanx'}, 'code': 'huangnan'}, '锦州': {'sublist': {'黑山': 'heishanshi', '经济开发区': 'jingjikaifaq', '凌海': 'linghaishi', '义县': 'yixian', '太和': 'taihequ', '松山新区': 'songshanxinqu', '古塔': 'gutaqu', '北镇': 'beizhenshi', '凌河': 'linghequ'}, 'code': 'jinzhou'}, '临夏': {'sublist': {'永靖': 'yongjingxian', '和政': 'hezhengxian', '康乐': 'kanglexian', '积石': 'jishixian', '临夏': 'linxiaxian', '临夏市': 'linxialxs', '广河': 'guanghexian', '东乡': 'dongxiangxian'}, 'code': 'linxia'}, '邵东': {'sublist': {'其他': 'shaodongxianqt', '城区': 'shaodongxiancq'}, 'code': 'shaodongxian'}, '福安': {'sublist': {'其他': 'fuanshiqt', '城区': 'fuanshicq'}, 'code': 'fuanshi'}, '漯河': {'sublist': {'源汇': 'yuanhuiqu', '临颍': 'linyingxian', '高新区': 'gaoxinqu', '郾城': 'yanchengqu', '舞阳': 'wuyangxian', '召陵': 'zhaolingqu'}, 'code': 'luohe'}, '果洛': {'sublist': {'果洛周边': 'guoluozhoubian', '甘德': 'gande', '久治': 'jiuzhi', '玛沁': 'maqin', '班玛': 'banma', '玛多': 'maduo', '达日': 'dari'}, 'code': 'guoluo'}, '张家界': {'sublist': {'慈利': 'cilixianzjj', '桑植': 'sangzhixian', '永定': 'yongdingqu', '武陵源': 'wulingyuanqu'}, 'code': 'zjj'}, '许昌': {'sublist': {'许昌县': 'xuchang', '长葛': 'changgeshi', '魏都': 'weidou', '其他': 'xuchangshi', '鄢陵': 'yanlingxian', '禹州': 'yuzhoushi', '襄城': 'xiangchengxian'}, 'code': 'xc'}, '阜阳': {'sublist': {'颍东': 'yingdongqu', '颍州': 'yingzhouqu', '颍上': 'yingshangxian', '颍泉': 'yingquanqu', '太和': 'taihex', '界首': 'jieshoushi', '经济开发区': 'jingjiq', '阜南': 'funanxian', '临泉': 'linquanxian'}, 'code': 'fy'}, '延边': {'sublist': {'珲春': 'huichun', '图们': 'tumen', '和龙': 'helong', '汪清': 'wangqing', '龙井': 'longjing', '敦化': 'dunhua', '延吉': 'yanji', '其他': 'yanbianshi', '安图': 'antu'}, 'code': 'yanbian'}, '海南': {'sublist': {'同德': 'tongdexian', '海南周边': 'hainanzhoubian', '贵南': 'guinanxian', '兴海': 'xinghaixian', '贵德': 'guidexian', '共和': 'gonghexian'}, 'code': 'hainan'}, '海拉尔': {'sublist': {'其他': 'hailaer', '海拉尔城区': 'hailaercheng'}, 'code': 'hlr'}, '滕州': {'sublist': {'北辛街道': 'beixinjiedao', '荆河街道': 'jinghejiedao', '其他': 'tengzhoushiqita', '善南街道': 'shannanjiedao', '龙泉街道': 'longquanjiedao'}, 'code': 'tengzhou'}, '资阳': {'sublist': {'乐至': 'lezhixian', '简阳市': 'luoyangjianyang', '雁江': 'yanjiangqu', '安岳县': 'ziyanganyue'}, 'code': 'zy'}, '屯昌': {'sublist': {'枫木镇': 'fengmu', '屯昌周边': 'tunchangzb', '坡心镇': 'poxin', '新兴镇': 'xinxingzh', '南坤镇': 'nankun', '西昌镇': 'xichang', '屯城镇': 'tuncheng', '乌坡镇': 'wupo', '南吕镇': 'nanlv'}, 'code': 'tunchang'}, '陵水': {'sublist': {'文罗镇': 'wenluo', '陵水周边': 'lingshuizb', '光坡镇': 'guangpo', '隆广镇': 'longguang', '三才镇': 'sancai', '椰林镇': 'yelin', '英州镇': 'yingzhouz'}, 'code': 'lingshui'}, '资兴': {'sublist': {'其他': 'zixingqt', '城区': 'zixingcq'}, 'code': 'zixing'}, '武夷山': {'sublist': {'新丰': 'xinfengjie', '崇安': 'chonganjie', '星村镇': 'xingcunzhen', '武夷': 'wuyijie', '兴田镇': 'xingtianzhen', '五夫镇': 'wufuzhen', '武夷山周边': 'wuyishanzhoubian'}, 'code': 'wuyishan'}, '奥克兰': {'sublist': {}, 'code': 'glauckland'}, '六安': {'sublist': {'舒城': 'shuchengxian', '霍山': 'huoshanxian', '霍邱县': 'huoqiuxian', '金寨': 'jinzhaixian', '裕安': 'yuanquq', '六安市区': 'liuanshiqu', '金安': 'jinanquq'}, 'code': 'la'}, '赣州': {'sublist': {'定南': 'dingnan', '寻乌': 'xunwu', '崇义': 'chongyi', '于都': 'yudu', '瑞金': 'ruijin', '开发区': 'ganzkfq', '章贡': 'zhanggong', '信丰': 'xinfengq', '站北区': 'ganzzbq', '安远': 'anyuanq', '上犹': 'shangyou', '南康': 'nankang', '章江新区': 'ganzzjxq', '兴国': 'xingguo', '会昌': 'huichang', '石城': 'shicheng', '大余': 'dayuq', '龙南': 'longnan', '全南': 'quannan', '赣县': 'ganxianq', '宁都': 'ningdu', '健康路': 'gzjkl'}, 'code': 'ganzhou'}, '张家口': {'sublist': {'高新区': 'zjkgaoxin', '张北县': 'zhangbeixian', '宣化区': 'xuanhua', '万全': 'wanquanxian', '蔚县': 'weixian', '桥东': 'zjkqiaodong', '怀来': 'huailai', '桥西': 'zjkqiaoxi', '其他': 'zhangjiakou', '宣化县': 'xuanhuaxian'}, 'code': 'zjk'}, '莱州': {'sublist': {'金仓街道': 'jincangjiedao', '文昌路街道': 'wenchanglujiedao', '文峰路街道': 'wenfenglujiedao', '永安路街道': 'yonganlujiedao', '其他': 'laizhoushiqita', '三山岛街道': 'sanshandaojiedao', '城港路街道': 'chengganglujiedao'}, 'code': 'laizhou'}, '黔西南': {'sublist': {'黔西南周边': 'qianxinanzb', '兴义': 'xingyi', '册亨': 'ceheng', '普安': 'puan', '望谟': 'wangmo', '贞丰': 'zhenfeng', '兴仁': 'xingren', '晴隆': 'qinglongx', '安龙': 'anlong'}, 'code': 'qxn'}, '襄垣': {'sublist': {'其他': 'xiangyuanxianqt', '城区': 'xiangyuanxiancq'}, 'code': 'xiangyuanxian'}, '庄河': {'sublist': {'普兰店': 'pulandianshi', '城子坦镇': 'chengzitan', '双塔镇': 'shuangtazhen', '杨树房镇': 'yangshufang', '皮口镇': 'pikou', '安波镇': 'anbo', '其他': 'pulandian', '大刘家镇': 'daliujia'}, 'code': 'pld'}, '萍乡': {'sublist': {'湘东': 'xiangdong', '莲花': 'lianhuaxian', '其它': 'pingxiang', '芦溪': 'luxi', '上栗': 'shangli', '安源': 'anyuan'}, 'code': 'px'}, '安宁': {'sublist': {'安宁周边': 'anningzb', '昆钢': 'kungang', '太平新城': 'taipingxincheng', '温泉': 'kmwenquan', '安宁新区': 'anxinqu', '安宁市区': 'anshiqu'}, 'code': 'anningshi'}, '攸县': {'sublist': {'其他': 'zzyouxianqt', '城区': 'zzyouxiancq'}, 'code': 'zzyouxian'}, '无棣': {'sublist': {'其他': 'wudiqt', '城区': 'wudicq'}, 'code': 'wudi'}, '池州': {'sublist': {'青阳': 'qingyangx', '东至': 'czdongzhi', '池州周边': 'chizhouzhoubian', '贵池': 'guichi', '石台': 'shitai'}, 'code': 'chizhou'}, '三亚': {'sublist': {'吉阳区': 'syjyq', '天涯区': 'sytyq', '凤凰镇': 'fenghuangzhen', '海棠区': 'syhtq', '三亚周边': 'syzb', '河西': 'hexiquyu', '崖州区': 'syyzq'}, 'code': 'sanya'}, '日喀则': {'sublist': {'昂仁': 'angrenxian', '定日': 'dingrixian', '白朗': 'bailangxian', '定结': 'dingjiexian', '日喀则周边': 'rikezezhoubian', '岗巴': 'gangbaxian', '日喀则市': 'rkzrkzs'}, 'code': 'rkz'}, '磁县': {'sublist': {'其他': 'cixianqt', '城区': 'cixiancq'}, 'code': 'cixian'}, '白山': {'sublist': {'江源': 'jiangyuan', '临江': 'linjiangs', '长白': 'changbaix', '抚松': 'fusong', '八道江': 'badaojiang', '靖宇': 'jingyux', '白山周边': 'baishanzhoubian'}, 'code': 'baishan'}, '琼中': {'sublist': {'营根镇': 'yinggen', '湾岭镇': 'wanling', '黎母山镇': 'limushan', '长征镇': 'changzhen', '红毛镇': 'hongmao', '中平镇': 'zhongping', '琼中周边': 'qiongzhongzb', '和平镇': 'hepingz'}, 'code': 'qiongzhong'}, '安吉': {'sublist': {'灵峰街道': 'lingfengjiedao', '孝源街道': 'xiaoyuanjiedao', '其他': 'anjixianqita', '昌硕街道': 'changshuojiedao', '递铺街道': 'dipujiedao'}, 'code': 'anji'}, '范县': {'sublist': {'其他': 'fanxianqt', '城区': 'fanxiancq'}, 'code': 'fanxian'}, '海口': {'sublist': {'美兰': 'meilan', '琼山': 'qiongshan', '龙华': 'longhuaqu', '海口周边': 'haikouqita', '秀英': 'xiuying'}, 'code': 'haikou'}, '漳浦': {'sublist': {'其他': 'zhangpuqt', '城区': 'zhangpucq'}, 'code': 'zhangpu'}, '太原': {'sublist': {'迎泽': 'yingze', '万柏林': 'wanbolin', '杏花岭': 'xinghualing', '晋源': 'jinyuan', '太原周边': 'taiyuan', '小店': 'xiaodian', '尖草坪': 'jiancaoping'}, 'code': 'ty'}, '新余': {'sublist': {'分宜': 'fenyixy', '渝水': 'yushui', '仙女湖': 'xiannvhu', '新余周边': 'xinyuzhoubian'}, 'code': 'xinyu'}, '长葛': {'sublist': {'建设路街道': 'jianshelujd', '长社路街道': 'changshelu', '金桥路街道': 'jinqiaolu', '长兴路街道': 'changxinglu', '长葛周边': 'changgezb'}, 'code': 'changge'}, '霸州': {'sublist': {'市政府': 'shizhengfubz', '霸州一中': 'bazhouyizhong', '霸州一小': 'bazhouyixiao', '第五小学': 'diwuxiaoxue', '明珠超市': 'mingzhuchaoshi', '湿地公园': 'shidigogyuan', '汽车站': 'qichezhanbz', '火车站': 'huochezhanbz', '廊坊第四人民医院': 'disirenminyiyuan', '锦绣华府': 'jinxiuhuafu', '孔雀城': 'kongquechengbz'}, 'code': 'bazhou'}, '任丘': {'sublist': {'永丰路街道': 'yongfenglujiedao', '西环路街道': 'xihuanlujiedao', '其他': 'renqiushiqita', '新华路街道': 'xinhualujiedao', '中华路街道': 'zhonghualujiedao'}, 'code': 'renqiu'}, '天长': {'sublist': {'天长市区': 'tianchangshiqu', '其它': 'tianchangqita'}, 'code': 'tianchang'}, '诸城': {'sublist': {'石桥子镇': 'shiqiaozi', '百尺河镇': 'baichihe', '辛兴镇': 'xinxingz', '龙都街道': 'longduj', '枳沟镇': 'zhigou', '皇华镇': 'huanghuaz', '密州街道': 'mizhouj', '程戈庄镇': 'chenggezhuang', '相州镇': 'xiangzhouz', '舜王街道': 'shunwangj', '昌城镇': 'changchengz', '桃林乡': 'taolinx', '贾悦镇': 'jiayuez'}, 'code': 'zc'}, '桂阳': {'sublist': {'其他': 'czguiyangqt', '城区': 'czguiyangcq'}, 'code': 'czguiyang'}, '眉山': {'sublist': {'洪雅': 'hongyaxian', '彭山': 'pengshanxian', '眉山周边': 'meishanzhoubian', '东坡': 'dongpoqu', '仁寿县': 'meishanrenshou', '青神': 'qingshenxian', '丹棱': 'danlingxian'}, 'code': 'ms'}, '黄冈': {'sublist': {'黄梅': 'huangmeixian', '武穴': 'wuxueshihg', '麻城': 'machengshi', '罗田': 'luotianxian', '蕲春': 'qichenxian', '浠水': 'xishuixian', '黄州': 'huangzhouqu', '团风': 'tuanfengxian', '英山': 'yingshanxian', '龙感湖': 'longganhuqu', '红安': 'honganxian'}, 'code': 'hg'}, '阜宁': {'sublist': {'其他': 'funingxianqt', '城区': 'funingxiancq'}, 'code': 'funingxian'}, '宜城': {'sublist': {'其他': 'yichengshiqt', '城区': 'yichengshicq'}, 'code': 'yichengshi'}, '兰州': {'sublist': {'兰州周边': 'lanzhou', '新区': 'lzxq', '红古': 'honggu', '安宁': 'anning', '七里河': 'qilihe', '西固': 'xigu', '城关': 'chengguanqv'}, 'code': 'lz'}, '昌吉': {'sublist': {'呼图壁': 'hutubishi', '阜康': 'fukangshi', '吉木萨尔': 'jimusaerxian', '木垒': 'muleixian', '玛纳斯': 'manasixian', '奇台': 'qitaixian', '昌吉': 'changjishi'}, 'code': 'changji'}, '开原': {'sublist': {'其他': 'kaiyuanqt', '城区': 'kaiyuancq'}, 'code': 'kaiyuan'}, '韶关': {'sublist': {'南雄': 'nanxiong', '仁化': 'renhua', '乳源': 'ruyuan', '翁源县': 'sgwyx', '新丰': 'xinfeng', '始兴': 'shixing', '其它': 'shaoguan', '乐昌': 'lechang', '北江': 'beijiang', '武江': 'wujiangqu', '曲江': 'qujiang', '浈江': 'zhenjiang'}, 'code': 'sg'}, '改则': {'sublist': {'改则县政府': 'gaizexianzhengfu', '改则县卫生局': 'gaizexianweishengju'}, 'code': 'gaizexian'}, '泗洪': {'sublist': {'其他': 'sihongqita', '城区': 'sihongchengqu'}, 'code': 'sihong'}, '石嘴山': {'sublist': {'石嘴山周边': 'shizuishanzhoubian', '大武口': 'dawukou', '惠农': 'huinong', '平罗': 'pingluo'}, 'code': 'szs'}, '莒县': {'sublist': {'其他': 'lvxianqita', '城区': 'lvxianchengqu'}, 'code': 'juxian'}, '巨野': {'sublist': {'其他': 'juyeqt', '城区': 'juyecq'}, 'code': 'juye'}, '高安': {'sublist': {'其他': 'gaoanqt', '城区': 'gaoancq'}, 'code': 'gaoan'}, '和田': {'sublist': {'和田县': 'hetianxian', '策勒': 'celexian', '和田周边': 'hetianzhoubian', '洛浦': 'luopuxian', '民丰': 'minfengxian', '墨玉': 'moyuxian', '皮山': 'pishanxian', '于田': 'yutx'}, 'code': 'ht'}, '项城': {'sublist': {'其他': 'xiangchengshiqita', '城区': 'xiangchengchengqu'}, 'code': 'xiangchengshi'}, '定边': {'sublist': {'其他': 'dingbianqita', '城区': 'dingbianchengqu'}, 'code': 'dingbian'}, '桓台': {'sublist': {'桓台二中': 'zbhengtaierzhong', '少海公园': 'zbshgy', '渔洋街': 'zbyyj', '老公园巡警大队': 'zblgyxjdd', '桓台一中': 'zbhengtaiyizhong', '兴桓路': 'zbxhl', '第一小学': 'zbdyxx', '公安街': 'zbgaj', '红莲湖': 'zbhlh', '索镇街道': 'suozhenjiedao', '惠仟佳': 'zbhqj', '实验中学': 'zbsyzx', '中心路': 'zbzxl', '第二小学': 'zbdexx', '镇南大街': 'zbzndj', '喜乐佳': 'zbxlj', '少海路': 'zbshl', '张北路': 'zbzbl', '东岳路': 'zbdyl', '信誉楼': 'zbxyl', '少海街道': 'shaohaijiedao', '世纪中学': 'zbsjzx', '建设街': 'zbjsj', '车站': 'zbht', '其他': 'zbhtqt', '桓台银座': 'zbhtyz', '建校': 'zbjx'}, 'code': 'huantaixian'}, '韩城': {'sublist': {'太史大街': 'taishidajie', '桢州大街': 'zhenzhoudj', '韩城周边': 'hanchengzb'}, 'code': 'hancheng'}, '大兴安岭': {'sublist': {'漠河': 'mohe', '塔河': 'tahe', '加格达奇': 'jiagedaqi', '呼玛': 'huma', '新林': 'xinlin', '呼中': 'huzhong', '大兴安岭周边': 'daxinganlingzb', '松岭': 'songling'}, 'code': 'dxal'}, '鞍山': {'sublist': {'铁东': 'tiedong', '台安': 'taianxian', '铁西': 'tiexi', '岫岩': 'xiuyan', '鞍山周边': 'anshan', '海城': 'haicheng', '立山': 'lishan', '千山': 'qianshan'}, 'code': 'as'}, '宣汉': {'sublist': {'其他': 'xuanhanqt', '城区': 'xuanhancq'}, 'code': 'xuanhan'}, '常州': {'sublist': {'戚墅堰': 'qishuyan', '金坛': 'changzhoujintan', '溧阳': 'liyangqu', '武进': 'wujin', '天宁': 'tianning', '钟楼': 'zhonglou', '常州周边': 'changzhou', '新北': 'xinbei'}, 'code': 'cz'}, '靖边': {'sublist': {'其他': 'jingbianqita', '城区': 'jingbianchengqu'}, 'code': 'jingbian'}, '广汉': {'sublist': {'其他': 'guanghanshiqita', '中心城区': 'ghzhongxinchengqu', '雒城镇': 'luochengzhen'}, 'code': 'guanghanshi'}, '禹城': {'sublist': {'其他': 'yuchengshiqt', '城区': 'yuchengshicq'}, 'code': 'yuchengshi'}, '东台': {'sublist': {'东台市区': 'dongtaishiqu', '其它': 'dongtaiqita'}, 'code': 'dongtai'}, '梅州': {'sublist': {'五华': 'wuhuaxian', '兴宁': 'xingningshi', '梅州周边': 'meizhouzb', '梅县': 'meixianm', '平远': 'pingyuanxian', '蕉岭': 'jiaolingxian', '丰顺': 'fengshunxian', '大埔': 'dapuxian', '梅江': 'meijiangqu'}, 'code': 'mz'}, '玉树': {'sublist': {'玉树周边': 'yushuzhoubian', '杂多': 'zaduo', '玉树': 'yushux', '曲麻莱': 'qumalai', '称多': 'chengduo', '囊谦': 'nangqian', '治多': 'zhiduo'}, 'code': 'ys'}, '阳泉': {'sublist': {'盂县': 'yuxian', '城区': 'chengquq', '平定': 'pingdingxian', '市辖区': 'yqsxq', '郊区': 'jiaoquq', '矿区': 'kuangquq'}, 'code': 'yq'}, '桂平': {'sublist': {'其他': 'guipingquqt', '城区': 'guipingqucq'}, 'code': 'guipingqu'}, '惠州': {'sublist': {'惠东': 'huidongqu', '仲恺': 'zkai', '惠州周边': 'huizhoushi', '惠阳': 'huiyang', '龙门': 'longmen', '惠城': 'huicheng', '大亚湾': 'dayawan', '博罗': 'boluoqu'}, 'code': 'huizhou'}, '惠东': {'sublist': {'黄埠': 'huangbu', '巽寮': 'xunliao', '大岭': 'daling', '惠东周边': 'huidongzb', '平山': 'hzpingshan'}, 'code': 'huidong'}, '甘南': {'sublist': {'迭部': 'diebu', '玛曲': 'maqu', '碌曲': 'luqu', '夏河': 'xiahe', '临潭': 'lintan', '合作': 'hezuo', '卓尼': 'zuoni', '甘南周边': 'gannanzhoubian', '舟曲': 'zhouqu'}, 'code': 'gn'}, '余姚': {'sublist': {'余姚市区': 'yuyaoshiqu', '其它': 'yuyaoqita'}, 'code': 'yuyao'}, '晋中': {'sublist': {'榆次': 'yuciqu', '平遥': 'pingyaoxian', '左权': 'zuoquanxian', '灵石': 'lingshixian', '开发区': 'kaifaquq', '祁县': 'qixian', '昔阳': 'xiyangxian', '和顺': 'heshunxian', '太谷': 'taiguxian', '榆社': 'yushexian', '寿阳': 'shouyangxian', '介休': 'jiexiushi'}, 'code': 'jz'}, '嘉善': {'sublist': {'西塘': 'xitangnew', '梅花庵': 'meihuannew', '姚庄镇': 'yaozhuangz', '罗星街道': 'luoxingjiedao', '大云镇': 'dayunzhen', '魏塘街道': 'weitangjiedao', '大云温泉': 'dywqnew', '天壬镇': 'tianrenzhen', '陶庄镇': 'taozhuangz', '惠民街道': 'huiminjiedao', '丁栅湿地': 'dssd', '干窑镇': 'ganyaozhen'}, 'code': 'jiashanx'}, '德州': {'sublist': {'德城': 'decheng', '禹城': 'yuchengshidz', '齐河': 'qihedz', '夏津': 'xiajin', '乐陵': 'laolingdz', '平原': 'pingyuan', '武城': 'wucheng', '宁津': 'ningjindz', '庆云': 'qingyun', '其他': 'dezhou', '陵县': 'lingxian', '临邑': 'linyixianqdz'}, 'code': 'dz'}, '太康': {'sublist': {'其他': 'taikangqt', '城区': 'taikangcq'}, 'code': 'taikang'}, '北海': {'sublist': {'北海周边': 'beihaizhoubian', '海城': 'haichengqu', '合浦': 'hepuxian', '铁山港区': 'tieshangangqu', '银海': 'yinhaiqu'}, 'code': 'bh'}, '河源': {'sublist': {'紫金': 'zijin', '龙川': 'longchuan', '河源周边': 'heyuanzhoubian', '东源': 'dongyuanx', '和平县': 'hepingx', '源城': 'yuancheng', '连平': 'lianping'}, 'code': 'heyuan'}, '常德': {'sublist': {'石门': 'shimen', '津市': 'jinshi', '澧县': 'lixiancd', '安乡': 'anxiang', '桃源': 'taoyuan', '鼎城': 'dingcheng', '其他': 'changdeshi', '武陵': 'wuling', '汉寿': 'hanshou', '临澧': 'linli'}, 'code': 'changde'}, '高密': {'sublist': {'密水街道': 'mishuijiedao', '其他': 'gaomishiqita', '咸家工业区': 'xianjiagongyequ', '醴泉街道': 'liquanjiedao', '朝阳街道': 'chaoyangjiedao'}, 'code': 'gaomi'}, '莫斯科': {'sublist': {}, 'code': 'glmoscow'}, '偃师': {'sublist': {'商城街道': 'shangchengjiedao', '其他': 'yanshiqita', '顾县镇': 'guxianzhen', '翟镇镇': 'dizhenzhen', '岳滩镇': 'yuetanzhen'}, 'code': 'yanshiqu'}, '沈阳': {'sublist': {'大东': 'dadong', '沈北新区': 'xinchengzi', '苏家屯': 'sujiatun', '东陵': 'dongling', '铁西': 'sytiexi', '沈阳周边': 'shenyang', '和平': 'syheping', '沈河': 'shenhe', '于洪': 'yuhong', '皇姑': 'huanggu', '浑南新区': 'shenyangshi'}, 'code': 'sy'}, '伊春': {'sublist': {'新青': 'xinqingqu', '西林': 'xilinqu', '南岔': 'nanchaqu', '友好': 'youhaoqu', '伊春周边': 'yichunzb', '伊春': 'yichunqu', '翠峦': 'cuiluanqu'}, 'code': 'yich'}, '绥化': {'sublist': {'安达': 'shandaxian', '望奎': 'shwangkui', '北林': 'shbeilin', '肇东': 'shzhaodongxian', '兰西': 'shlanxi', '绥棱': 'shsuileng', '青冈': 'shqinggang', '庆安': 'shqingan', '海伦': 'shhailun', '明水': 'shmingshui'}, 'code': 'suihua'}, '阳春': {'sublist': {'三甲镇': 'sanjiazhen', '河口镇': 'hekouzhen', '合水镇': 'heshuizhen', '松柏镇': 'songbaizhen', '双窖镇': 'shuangjiaozhen', '圭岗镇': 'guigangzhen', '马水镇': 'mashuizhen', '陂面镇': 'pomianzhen', '岗美镇': 'gangmeizhen', '潭水镇': 'tanshuizhen', '春城镇': 'chuncheng', '春湾镇': 'chunwanzhen', '永宁镇': 'yongningzhen', '石望镇': 'shiwangzhen', '八甲镇': 'bajiazhen', '河塱镇': 'helangzhen'}, 'code': 'yangchun'}, '蚌埠': {'sublist': {'淮上': 'huaishang', '五河': 'wuhe', '怀远': 'huaiyuan', '其他': 'bengbuqita', '禹会': 'yuhui', '龙子湖': 'longzihu', '固镇': 'guzhen', '蚌山': 'bangshan'}, 'code': 'bengbu'}, '四平': {'sublist': {'铁东': 'tiedongq', '范家屯': 'fanjiatun', '四平周边': 'sipingzhoubian', '铁西': 'tiexiq', '伊通县': 'yitong', '孤家子镇': 'spgjz', '榆树台镇': 'spystz', '公主岭': 'sipinggongzhuling', '双辽': 'shuangliao', '梨树县': 'lishusp'}, 'code': 'sp'}, '白银': {'sublist': {'靖远': 'jingyuan', '会宁': 'huining', '白银': 'baiyin', '平川': 'pingchuan', '白银周边': 'baiyinzhoubian', '景泰': 'jingtan'}, 'code': 'by'}, '多伦多': {'sublist': {}, 'code': 'gltoronto'}, '酒泉': {'sublist': {'敦煌': 'jqdunhuang', '阿克塞': 'akesai', '肃北': 'subei', '玉门': 'yumen', '酒泉': 'jiuquan', '金塔': 'jinta', '安西': 'anxi', '酒泉周边': 'jiuquanzhoubian'}, 'code': 'jq'}, '南漳': {'sublist': {'其他': 'nanzhangqt', '城区': 'nanzhangcq'}, 'code': 'nanzhang'}, '阿里': {'sublist': {'革吉': 'gejixian', '札达': 'zhadaxian', '普兰': 'pulanxian', '改则': 'aligaize', '噶尔': 'gaerxian', '措勤': 'cuoqinxian', '阿里周边': 'alizhoubian', '日土区': 'rituqu'}, 'code': 'al'}, '宣威': {'sublist': {'其他': 'xuanwushiqt', '城区': 'xuanwushicq'}, 'code': 'xuanwushi'}, '余江': {'sublist': {'其他': 'yujiangqt', '城区': 'yujiangcq'}, 'code': 'yujiang'}, '迁西': {'sublist': {'其他': 'qianxixianqt', '城区': 'qianxixiancq'}, 'code': 'qianxixian'}, '那曲': {'sublist': {'安多县': 'nqadx', '聂荣县': 'nqnrx', '申扎县': 'nqszx', '比如县': 'nqbrx', '嘉黎县': 'nqjlx', '班戈县': 'nqbgx', '古露镇': 'guluzhen', '那曲镇': 'naquzhen', '那曲周边': 'naquzhoubian', '罗玛镇': 'luomazhen', '索县': 'nqsx', '巴青县': 'nqbqx', '尼玛县': 'nqnmx'}, 'code': 'nq'}, '仁寿': {'sublist': {'其他': 'renshouxianqita', '城区': 'renshouchengqu'}, 'code': 'renshouxian'}, '溧阳': {'sublist': {'溧阳市区': 'liyangshiqu', '其它': 'liyangqita'}, 'code': 'liyang'}, '张北': {'sublist': {'大河': 'dahe', '海流图': 'hailiutu', '馒头营': 'mantouying', '公会': 'gonghui', '二台': 'ertai', '大囫囵': 'dahulun', '张北周边': 'zhangbeizb', '单晶河': 'danjinghe', '张北': 'zhangbeizhen', '油篓沟': 'youlougou', '台路沟': 'tailugou', '两面井': 'liangmianjing', '二泉井': 'erquanjing'}, 'code': 'zhangbei'}, '松滋': {'sublist': {'其他': 'songziqt', '城区': 'songzicq'}, 'code': 'songzi'}, '沁阳': {'sublist': {'其他': 'qinyangqt', '城区': 'qinyangcq'}, 'code': 'qinyang'}, '莱阳': {'sublist': {'其他': 'laiyangqt', '城区': 'laiyangcq'}, 'code': 'laiyang'}, '毕节': {'sublist': {'百里杜鹃': 'bjbldj', '赫章': 'hezhang', '威宁': 'weining', '黔西': 'qianxi', '织金': 'zhijin', '纳雍': 'nayong', '金沙': 'jinshax', '大方': 'dafang', '毕节周边': 'bijiezhoubian', '七星关': 'bjqxg'}, 'code': 'bijie'}, '马鞍山': {'sublist': {'博望区': 'masbwq', '含山': 'hanshanx', '其它': 'maanshan', '花山': 'huashanqu', '当涂': 'dangtu', '雨山': 'yushan', '和县': 'hexians', '金家庄': 'jinjiazhuang'}, 'code': 'mas'}, '象山': {'sublist': {'象山市区': 'xiangshanshiqu', '其它': 'xiangshanqita'}, 'code': 'xiangshanxian'}, '玉田': {'sublist': {'其他': 'yutianxianqt', '城区': 'yutianxiancq'}, 'code': 'yutianxian'}, '迪庆': {'sublist': {'德钦': 'deqinxian', '迪庆周边': 'diqingzhoubian', '维西傈': 'weixilixian', '香格里拉': 'xianggelilaxian'}, 'code': 'diqing'}, '巢湖': {'sublist': {'庐江': 'lujiang', '巢湖周边': 'chaohuzhoubian', '居巢': 'juchao'}, 'code': 'ch'}, '靖江': {'sublist': {'靖江市区': 'jingjiangshiqu', '其它': 'jingjiangqita'}, 'code': 'jingjiang'}, '滁州': {'sublist': {'滁州周边': 'chuzhouzhoubian', '来安': 'laian', '全椒': 'quanshu', '定远': 'dingyuan', '凤阳': 'fengyangx', '天长': 'tianchangqu', '南谯': 'nanqiaoq', '琅琊': 'langya', '明光': 'mingguan'}, 'code': 'chuzhou'}, '哈密': {'sublist': {'伊吾': 'yiwuxian', '哈密': 'hamishi', '巴里坤': 'balilkunzzx'}, 'code': 'hami'}, '三河': {'sublist': {'高楼镇': 'gaolouzhen', '齐心庄镇': 'qixinzhuangzhen', '李旗庄镇': 'liqizhuangzhen', '其他': 'sanheshiqita', '泃阳镇': 'juyangzhen'}, 'code': 'sanhe'}, '遵义': {'sublist': {'红花岗': 'honghuagangqu', '道真': 'daozhenxian', '汇川': 'huichuanqu', '新浦新区': 'xinpuxinqu', '湄潭': 'meitanxian', '播州区': 'bozhouqu', '务川': 'wuchuanxian', '习水': 'xishuix', '赤水': 'chishuishi', '余庆': 'yuqingxian', '正安': 'zhenganxian', '南白': 'zunyixian', '凤冈': 'fenggangxian', '桐梓': 'tongzixian', '仁怀市': 'zunyirenhuai', '绥阳': 'suiyangxian'}, 'code': 'zunyi'}, '铜仁': {'sublist': {'松桃': 'songtao', '思南': 'sinan', '沿河': 'yanhe', '德江': 'dejiang', '石阡': 'shiqian', '玉屏': 'yuping', '印江': 'yinjiang', '万山': 'wangshan', '碧江': 'trbj', '江口': 'jiangkou', '铜仁周边': 'tongrenzb'}, 'code': 'tr'}, '兰考': {'sublist': {'兰考县': 'lkaoxian', '空港': 'konggang'}, 'code': 'lankaoxian'}, '绍兴': {'sublist': {'袍江': 'paojiang', '新昌': 'xinchangsx', '嵊州': 'shengzhousx', '越城': 'yuecheng', '滨海': 'bhai', '上虞': 'shangyu', '诸暨': 'chujiqu', '其他': 'shaoxing', '柯桥': 'keqiao', '镜湖': 'sxjh'}, 'code': 'sx'}, '梧州': {'sublist': {'苍梧': 'cangwu', '藤县': 'tengxian', '万秀': 'wanxiu', '岑溪': 'cenxiwz', '其它': 'wuzhoushi', '长洲': 'changzhouqv', '蝶山': 'dieshan', '蒙山': 'mengshan'}, 'code': 'wuzhou'}, '大理': {'sublist': {'祥云': 'xiangyunxian', '永平': 'yongpingxian', '巍山': 'weishanzizhi', '洱源': 'eryuanxian', '弥渡': 'miduxian', '南涧': 'nanjianzizhi', '剑川': 'jianchuanxian', '云龙': 'yunlongxian', '大理市': 'dalishi', '宾川': 'binchuanxian', '漾濞': 'yangxianzizhi', '鹤庆': 'heqingxian'}, 'code': 'dali'}, '澧县': {'sublist': {'其他': 'lixianqt', '城区': 'lixiancq'}, 'code': 'lixian'}, '陆丰': {'sublist': {'南塘': 'nantang', '潭西': 'tanxi', '甲子': 'jiazi', '甲东': 'jiadong', '湖东': 'hudong', '陆丰周边': 'qitalf', '金厢': 'jinxiangs', '博美': 'swbomei', '河西': 'hexis', '大安': 'daans', '碣石': 'jieshi', '陂洋': 'piyang', '城东': 'chengdongss', '东海': 'xiancheng', '内湖': 'neihu', '上英': 'shangying', '甲西': 'jiaxi', '河东': 'hedongs', '西南': 'xinans', '桥冲': 'qiaochong', '八万': 'bawan'}, 'code': 'lufengshi'}, '明港': {'sublist': {'肖店': 'xiaodianqu', '平昌': 'pingchang', '明港': 'minggangqu', '王岗': 'wanggang', '甘岸': 'ganan', '兰店': 'landian', '刑集': 'xingji', '长台': 'changtaiqu', '查山': 'chashan'}, 'code': 'mg'}, '天门': {'sublist': {'杨林街道': 'yanglinjiedao', '竟陵街道': 'jinglingjiedao', '岳口街道': 'yuekoujiedao', '候口街道': 'houkoujiedao', '天门周边': 'tianmenzb'}, 'code': 'tm'}, '钟祥': {'sublist': {'其他': 'zhongxiangshiqt', '城区': 'zhongxiangshicq'}, 'code': 'zhongxiangshi'}, '平邑': {'sublist': {'其他': 'pingyiqt', '城区': 'pingyicq'}, 'code': 'pingyi'}, '海北': {'sublist': {'海北周边': 'haibeizhoubian', '门源': 'menyuan', '祁连': 'qilian', '刚察': 'gangcha', '海晏': 'haiyanx'}, 'code': 'haibei'}, '潍坊': {'sublist': {'潍城': 'weicheng', '坊子': 'fangzi', '经开区': 'jingkaiq', '滨海新区': 'wfbinhaixinqu', '奎文': 'kuiwen', '寿光': 'shouguangqu', '高密市': 'weifanggaomi', '昌乐': 'changlewf', '高新区': 'wfgaoxinqu', '安丘': 'anqiuwf', '昌邑': 'changyishiwf', '青州': 'weifangqingzhou', '诸城': 'zhucheng', '临朐': 'linquwf', '寒亭': 'hanting', '潍坊周边': 'weifang'}, 'code': 'wf'}, '鄄城': {'sublist': {'其他': 'juanchengqt', '城区': 'juanchengcq'}, 'code': 'juancheng'}, '丽水': {'sublist': {'景宁': 'jingningqu', '松阳': 'songyangqu', '缙云': 'jinyunqu', '遂昌': 'suiyangqu', '庆元': 'qingyuanquyu', '云和': 'yunhequ', '青田': 'qingtianqu', '龙泉': 'longquanqu', '莲都': 'lianduqu'}, 'code': 'lishui'}, '固原': {'sublist': {'固原': 'guyuanshi', '隆德': 'longdexian', '彭阳': 'pengyangxian', '海原': 'haiyuanxian', '西吉': 'xijixian', '泾源': 'jingyuanxian', '经济开发区': 'jingjikaifa', '原州': 'yuanzhouqu'}, 'code': 'guyuan'}, '泽州': {'sublist': {'其他': 'zezhouqt', '城区': 'zezhoucq'}, 'code': 'zezhou'}, '宜都': {'sublist': {'宜都市区': 'yidoushiqu', '其它': 'yidouqita'}, 'code': 'yidou'}, '睢县': {'sublist': {'其他': 'suixianqt', '城区': 'suixiancq'}, 'code': 'suixian'}, '洛阳': {'sublist': {'老城': 'laocheng', '瀍河': 'chanhehuizu', '伊川': 'yichuanly', '涧西': 'jianxi', '洛阳周边': 'luoyangshi', '伊滨': 'yibin', '汝阳': 'ruyang', '宜阳': 'lyyiyangly', '吉利': 'jiliqu', '洛龙': 'luolong', '偃师市': 'luoyangyanshi', '西工': 'xigongqu'}, 'code': 'luoyang'}, '南充': {'sublist': {'蓬安': 'penganxian', '高坪': 'gaopingqu', '顺庆': 'shunqingqu', '营山': 'yingshanxianq', '西充': 'xichongxian', '南部': 'nanbuxian', '仪陇': 'yilongxian', '南充周边': 'nanchongzb', '阆中': 'langzhongshi', '嘉陵': 'jialingqu'}, 'code': 'nanchong'}, '文山': {'sublist': {'马关': 'maguanxian', '麻栗坡': 'malipo', '文山': 'wenshanxian', '砚山': 'yanshanqu', '富宁': 'funingqu', '丘北': 'qiubeixian', '广南': 'guangnanxian', '西畴': 'xichouxian'}, 'code': 'ws'}, '荆门': {'sublist': {'掇刀': 'duodaoqu', '屈家岭管理区': 'qujialing', '京山': 'jingshanxianjm', '东宝': 'dongbaoqu', '沙洋': 'shayangxianjm', '钟祥': 'zhongxiangshijm'}, 'code': 'jingmen'}, '新乡': {'sublist': {'辉县': 'huixian', '新乡县': 'xinxiangxian', '卫滨': 'weibinqu', '牧野': 'muye', '卫辉': 'weihui', '其他': 'xinxiang', '长垣县': 'xianxiangchangyuan', '平原示范区': 'pingyuanshifanqu', '凤泉': 'fengquan', '红旗': 'hongqi'}, 'code': 'xx'}, '涟源': {'sublist': {'其他': 'lianyuanshiqt', '城区': 'lianyuanshicq'}, 'code': 'lianyuanshi'}, '濮阳': {'sublist': {'南乐': 'nanlexian', '范县': 'fanxianpy', '清丰': 'qingfengxian', '高新区': 'gaoxinquyu', '台前': 'taiqianxian', '其他': 'puyangqita', '华龙': 'hualongqu', '濮阳县': 'puyangxian'}, 'code': 'puyang'}, '海门': {'sublist': {'其它': 'haimenqita', '海门市区': 'haimenshiqu'}, 'code': 'haimen'}, '哈尔滨': {'sublist': {'香坊': 'xiangfang', '宾县': 'hebbinxian', '开发区': 'hrbkaifaqu', '巴彦': 'hebbayan', '哈尔滨周边': 'haerbin', '南岗': 'nangang', '江北': 'hrbjiangbei', '通河': 'hebtonghe', '方正': 'hebfangz', '道里': 'daoli', '道外': 'daowai', '木兰': 'hebmulan', '依兰': 'hebyilan'}, 'code': 'hrb'}, '德清': {'sublist': {'其它': 'deqingqita', '德清市区': 'deqingshiqu'}, 'code': 'deqing'}, '滦南': {'sublist': {'其他': 'luannanxianqt', '城区': 'luannanxiancq'}, 'code': 'luannanxian'}, '来宾': {'sublist': {'象州': 'xiangzhouxian', '武宣': 'wuxuanxian', '合山': 'heshanshi', '兴宾': 'xingbingqu', '金秀': 'jinxiuxian', '忻城': 'qichengxian', '来宾周边': 'laibinzhoubian'}, 'code': 'lb'}, '梅河口': {'sublist': {'其他': 'meihekouqt', '城区': 'meihekoucq'}, 'code': 'meihekou'}, '西宁': {'sublist': {'湟中': 'huangzhong', '大通': 'datongxian', '城中': 'chengzhong', '城东': 'chengdong', '湟源': 'huangyuan', '其它': 'xining', '城西': 'chengxi', '城北': 'chengbeiqu'}, 'code': 'xn'}, '博兴': {'sublist': {'其他': 'boxingqt', '城区': 'boxingcq'}, 'code': 'boxing'}, '其他海外城市': {'sublist': {}, 'code': 'city'}, '百色': {'sublist': {'右江': 'youjiangqu', '田阳': 'tianyangxian', '百色周边': 'baisezhoubian', '平果': 'pingguoxian', '隆林': 'longlinxian', '德保': 'debaoxian', '田东': 'tiandongxian'}, 'code': 'baise'}, '北流': {'sublist': {'其他': 'beiliushiqt', '城区': 'beiliushicq'}, 'code': 'beiliushi'}, '岑溪': {'sublist': {'其他': 'cenxiqt', '城区': 'cenxicq'}, 'code': 'cenxi'}, '宁津': {'sublist': {'其他': 'ningjinqt', '城区': 'ningjincq'}, 'code': 'ningjin'}, '河间': {'sublist': {'其他': 'hejianqt', '城区': 'hejiancq'}, 'code': 'hejian'}, '长春': {'sublist': {'高新': 'ccgaoxin', '榆树': 'yushu', '经开': 'jingkai', '汽车城': 'qichecheng', '宽城': 'kuancheng', '绿园': 'lvyuan', '德惠': 'dehui', '长春周边': 'changchun', '双阳': 'shuangyang', '南关': 'nanguan', '二道': 'erdao', '净月': 'jingyue', '农安': 'nongan', '九台': 'jiutai', '朝阳': 'chaoyangqu'}, 'code': 'cc'}, '临朐': {'sublist': {'其他': 'linquqt', '城区': 'linqucq'}, 'code': 'linqu'}, '湘阴': {'sublist': {'其他': 'xiangyinqt', '城区': 'xiangyincq'}, 'code': 'xiangyin'}, '进贤': {'sublist': {'其他': 'jinxianqt', '城区': 'jinxiancq'}, 'code': 'jinxian'}, '渭南': {'sublist': {'华阴': 'huayin', '韩城': 'wnhancheng', '临渭': 'linwei', '蒲城': 'pucheng', '潼关': 'tongguan', '渭南周边': 'weinan', '白水': 'baishui', '合阳': 'heyang', '大荔': 'dalixian', '澄城': 'chengcheng', '富平': 'fuping', '华县': 'wnhuaxian'}, 'code': 'wn'}, '枣阳': {'sublist': {'环城街道': 'huanchengjiedao', '南城街道': 'nanchengjiedao', '其他': 'zaoyangshiqita', '北城街道': 'beichengjiedao'}, 'code': 'zaoyang'}, '东莞': {'sublist': {'凤岗': 'fenggang', '长安': 'changanqv', '虎门': 'humen', '黄江': 'huangjiang', '石排': 'ship', '南城': 'nancheng', '常平': 'changpingshi', '石碣': 'shijie', '麻涌': 'macong', '松山湖': 'songsh', '望牛墩': 'wangniud', '道滘': 'daojiao', '谢岗': 'xiegang', '万江': 'wanjiang', '樟木头': 'zhangmutou', '沙田': 'shatianz', '塘厦': 'tangsha', '东莞周边': 'dongguan', '茶山': 'chashans', '东坑': 'dongk', '高埗': 'gaobus', '大朗': 'dalang', '洪梅': 'hongmei', '东城': 'dongchengqv', '桥头': 'qiaotouz', '寮步': 'liaobu', '莞城': 'guanchengshi', '中堂': 'zhongt', '大岭山': 'dalingshan', '企石': 'qishis', '其它': 'dongguanshi', '清溪': 'qingxi', '石龙': 'shilongs', '横沥': 'hengl', '厚街': 'houjie'}, 'code': 'dg'}, '东阳': {'sublist': {'江北': 'jhdyjb', '城东': 'jhdycd', '卢宅': 'jhdylz', '东阳周边': 'jhdyzb', '东阳市区': 'jhdysq', '横店': 'jhdyhd'}, 'code': 'dongyang'}, '渠县': {'sublist': {'其他': 'quxqt', '城区': 'quxcq'}, 'code': 'qux'}, '固安': {'sublist': {'长途汽车站': 'changtuqichezhanga', '古玩市场': 'guwanshichangga', '三小': 'sanxiaoga', '二中': 'erhzongga', '县一中': 'xianyizhonggalf', '英才中学': 'yingcaizhongxuega', '滨河公园': 'binhegognyuan', '人民医院': 'renminyiyuangalf', '牛驼温泉': 'niutuowenquanga', '四小': 'sixiaogalf', '县政府': 'xianzhengfuga', '工业园区': 'gongyeyuanquga', '一小城小': 'yixiaochengxiaoga', '民政局': 'minzhengjugalf', '孔雀城': 'kongquechengga'}, 'code': 'lfguan'}, '淮滨': {'sublist': {'其他': 'huaibinxianqt', '城区': 'huaibinxiancq'}, 'code': 'huaibinxian'}, '贵港': {'sublist': {'覃塘': 'qintangqu', '平南': 'pingnanxian', '港北': 'gangbeiqu', '港南': 'gangnanqu', '桂平': 'guipingqugg'}, 'code': 'gg'}, '苍南': {'sublist': {'莒溪': 'lvxizhen', '赤溪': 'chixizhen', '钱库镇': 'cnqiankuzhen', '龙港镇': 'cnlonggangzhen', '大渔': 'dayuzhen', '桥墩': 'qiaodunzhen', '宜山': 'yishanzhen', '金乡': 'jinxiangzhen', '苍南周边': 'cangnanzhoubian', '金乡镇': 'cnjinxiangzhen', '灵溪镇': 'cnlingxizhen', '沿浦': 'yanpuzhen', '钱库': 'qiankuzhen', '观美': 'guanmeizhen', '灵溪': 'lingxizhen', '矾山': 'fanshanzhen', '芦浦': 'lupuzhen', '宜山镇': 'cnyishanzhen', '炎亭': 'yantingzhen', '龙港': 'longgangzhen', '南宋': 'nansongzhen', '望里': 'wanglizhen', '马站镇': 'cnmazhanzhen', '舥艚': 'bacaozhen', '马站': 'mazhanzhen', '其他': 'cangnanxianqita', '霞关': 'xiaguanzhen', '藻溪': 'zaoxizhen'}, 'code': 'cangnanxian'}, '永安': {'sublist': {'其他': 'yonganqt', '城区': 'yongancq'}, 'code': 'yongan'}, '泸州': {'sublist': {'古蔺': 'gulinxian', '龙马潭': 'longmatanqu', '纳溪': 'naxiqu', '泸州周边': 'luzhouzb', '叙永': 'xuyongxian', '泸县': 'luxian', '合江': 'hejiangxian', '江阳': 'jiangyangqu'}, 'code': 'luzhou'}, '郯城': {'sublist': {'其他': 'tanchengqt', '城区': 'tanchengcq'}, 'code': 'tancheng'}, '朝阳': {'sublist': {'北票': 'beipiaocy', '龙城': 'longcheng', '朝阳县': 'chaoyangx', '朝阳周边': 'chaoyangzhoub', '建平': 'jiangping', '双塔': 'shuangtaq', '喀喇沁': 'kalaqin', '凌源': 'lingyuan'}, 'code': 'cy'}, '灯塔': {'sublist': {'其他': 'dengtaqt', '城区': 'dengtacq'}, 'code': 'dengta'}, '福鼎': {'sublist': {'其他': 'fudingshiqt', '城区': 'fudingshicq'}, 'code': 'fudingshi'}, '塔城': {'sublist': {'和布克赛尔': 'tachbkse', '托里': 'tactl', '乌苏市': 'tacwss', '裕民': 'tacym', '沙湾': 'tacsw', '塔城市': 'tacs'}, 'code': 'tac'}, '长治': {'sublist': {'长治县': 'changzhixian', '平顺': 'pingshunxian', '郊区': 'jiaoqushi', '武乡': 'wuxiangxian', '襄垣': 'xiangyuanxiancz', '沁源': 'qinyuanxian', '沁县': 'qinxian', '城区': 'chengqushi', '潞城': 'luchengshi', '黎城': 'lichengxian', '屯留': 'tunliuxian', '长子': 'zhangzixian', '壶关': 'huguanxian'}, 'code': 'changzhi'}, '博白': {'sublist': {'其他': 'bobaixianqt', '城区': 'bobaixiancq'}, 'code': 'bobaixian'}, '保定': {'sublist': {'白沟': 'bdbg', '新市': 'xinshiqu', '涿州市': 'daodingzhuozhou', '高碑店': 'gaobeidian', '保定周边': 'baoding', '北市': 'beishi', '安国': 'anguo', '定州': 'dingzhoushi', '高开': 'gaokaiqu', '南市': 'nanshiqu'}, 'code': 'bd'}, '泰州': {'sublist': {'姜堰': 'taizhoujiangyan', '泰兴': 'taixinqu', '靖江': 'jingjiangqu', '兴化': 'xinghuaqu', '高港': 'gaogang', '其他': 'taizhouqita', '海陵': 'hailing'}, 'code': 'taizhou'}, '和县': {'sublist': {'历阳镇': 'liyangzhen', '石杨镇': 'shiyangzhens', '乌江镇': 'wujiangzhen', '香泉镇': 'xiangquanzhen', '善厚镇': 'shanhouzhen', '姥桥镇': 'laoqiaozhen', '西埠镇': 'xibuzhen', '功桥镇': 'gongqiaozhen', '白桥镇': 'baiqiaozhen', '沈巷镇': 'shengangzhen'}, 'code': 'hexian'}, '咸宁': {'sublist': {'嘉鱼': 'jiayuxianxn', '咸宁周边': 'xianningzb', '通山': 'tongshanxian', '咸安': 'xiananqu', '崇阳': 'chongyangxian', '赤壁': 'chibishixn', '通城': 'tongchenxian'}, 'code': 'xianning'}, '广饶': {'sublist': {'其他': 'guangraoxianqita', '城区': 'guangraochengqu'}, 'code': 'guangrao'}, '白沙': {'sublist': {'牙叉镇': 'yacha', '白沙周边': 'baishazb', '七坊镇': 'qifang', '打安镇': 'daanzh', '邦溪镇': 'bangxi'}, 'code': 'baish'}, '嘉峪关': {'sublist': {'五一': 'wuyi', '新华': 'xinhua', '胜利': 'shengl', '前进': 'qianj', '镜铁山矿区': 'jingtieshan', '建设': 'jians', '嘉峪关周边': 'jiayuguanzhoubian'}, 'code': 'jyg'}, '嘉鱼': {'sublist': {'其他': 'jiayuxianqt', '城区': 'jiayuxiancq'}, 'code': 'jiayuxian'}, '宜阳': {'sublist': {'其他': 'lyyiyangqt', '城区': 'lyyiyangcq'}, 'code': 'lyyiyang'}, '林州': {'sublist': {'其他': 'linzhouqt', '城区': 'linzhoucq'}, 'code': 'linzhou'}, '平阳': {'sublist': {'南雁': 'nanyanzhen', '南麂': 'nanluzhen', '鹤溪': 'hexizhen', '腾蛟': 'tengjiaozhen', '水头': 'shuitouzhen', '钱仓': 'qiancangzhen', '昆阳': 'kunyangzhen', '山门': 'shanmenzhen', '顺溪': 'shunxizhen', '萧江': 'xiaojiangzhen', '郑楼': 'zhenglouzhen', '宋桥': 'songqiaozhen', '平阳周边': 'pingyanzhoubian', '宋埠': 'songbuzhen', '榆垟': 'yuyangzhen', '鳌江': 'aojiangzhen', '麻步': 'mabuzhen', '凤卧': 'fengwozhen'}, 'code': 'pingyangxian'}, '鹿邑': {'sublist': {'其他': 'luyiqt', '城区': 'luyicq'}, 'code': 'luyi'}, '长沙': {'sublist': {'开福': 'kaifu', '望城': 'cswc', '星沙': 'xingsha', '芙蓉': 'furong', '长沙周边': 'changsha', '岳麓': 'yuelu', '天心': 'tianxinqu', '雨花': 'csyuhua'}, 'code': 'cs'}, '泰兴': {'sublist': {'泰兴市区': 'taixinshiqu', '其它': 'taixinqita'}, 'code': 'taixing'}, '德阳': {'sublist': {'德阳周边': 'deyangzb', '绵竹': 'mianzhushi', '什邡': 'shenfangshi', '旌阳': 'jingyangqu', '广汉市': 'deyangguanghan', '罗江': 'luojiangxian', '中江': 'zhongjiangxian'}, 'code': 'deyang'}, '墨尔本': {'sublist': {}, 'code': 'glmelbourne'}, '张掖': {'sublist': {'民乐': 'minle', '肃南': 'sunan', '山丹': 'shandan', '临泽': 'linzhe', '张掖周边': 'zhangyezhoubian', '高台': 'gaotai'}, 'code': 'zhangye'}, '当阳': {'sublist': {'其他': 'dangyangqt', '城区': 'dangyangcq'}, 'code': 'dangyang'}, '泗阳': {'sublist': {'新袁新城': 'xinyuanxincheng', '众兴镇': 'zhongxingzhen', '其他': 'siyangqita', '王集新城': 'wangjixincheng'}, 'code': 'siyang'}, '沙洋': {'sublist': {'其他': 'shayangxianqt', '城区': 'shayangxiancq'}, 'code': 'shayangxian'}, '台湾': {'sublist': {'台南': 'tainan', '高雄': 'gaoxiong', '基隆': 'jilong', '其它': 'taiwan', '台中': 'taizhong', '台北': 'taibei'}, 'code': 'tw'}, '抚州': {'sublist': {'临川': 'linchuan', '抚州周边': 'fuzhouzhoubian', '乐安': 'lean', '崇仁': 'chongren', '南城': 'nanchengxfz', '东乡': 'dongxiang'}, 'code': 'fuzhou'}, '焦作': {'sublist': {'山阳': 'shanyang', '中站': 'zhongzhan', '修武': 'xiuwuxian', '武陟': 'wuzhixian', '解放': 'jiefangqu', '博爱': 'boaixian', '高新': 'gaoxin', '马村': 'macun', '沁阳': 'qinyangjz', '孟州': 'mengzhoujz', '其他': 'jiaozuoqita', '温县': 'wenxianjz'}, 'code': 'jiaozuo'}, '东平': {'sublist': {'龙山大街': 'taianlsdj', '稻香街': 'taiandxj', '东原路': 'taiandyl', '望山街': 'tiaanwsj', '东平县周边': 'dongpxzb', '佛山街': 'taianfsj', '东平街道': 'dongpjd', '东山路': 'taiandsl'}, 'code': 'dongping'}, '嵊州': {'sublist': {'其他': 'shengzhouqt', '城区': 'shengzhoucq'}, 'code': 'shengzhou'}, '定安': {'sublist': {'定城镇': 'dingchengz', '雷鸣镇': 'leiming', '龙湖镇': 'longhuz', '黄竹镇': 'huangzhu', '龙门镇': 'longmenz', '新竹镇': 'xinzhuz', '定安周边': 'dinganzb'}, 'code': 'da'}, '南宁': {'sublist': {'南宁周边': 'nanning', '兴宁': 'xingning', '西乡塘': 'xixiangtang', '良庆': 'liangqing', '江南': 'jiangnan', '青秀': 'qingxiu', '邕宁': 'yongning'}, 'code': 'nn'}, '忻州': {'sublist': {'宁武': 'ningwu', '原平': 'yuanping', '繁峙': 'fanzhi', '五台': 'wutaixian', '代县': 'daixian', '静乐': 'jingle', '其他': 'xinzhouqita', '定襄': 'dingxiang', '忻府': 'xinfu'}, 'code': 'xinzhou'}, '九江': {'sublist': {'德安': 'dean', '修水': 'xiushuixian', '都昌': 'duchangxian', '武宁': 'wuningxian', '开发区': 'jjkaifaqu', '九江周边': 'jiujiangshi', '九江县': 'jiujiangxian', '庐山': 'lushan', '瑞昌': 'ruichang', '湖口': 'hukouxian', '星子': 'xingzixian', '共青城': 'gongqing', '永修': 'yongxiuxian', '九瑞大道': 'jjjrdd', '彭泽': 'pengzexian', '浔阳区': 'xunyang', '九江市区': 'jiujiangshiqu'}, 'code': 'jj'}, '金坛': {'sublist': {'尧塘街道': 'yaotangjiedao', '东城街道': 'jtdongchengjiedao', '其他': 'jintanqita', '西城街道': 'jtxichengjiedao'}, 'code': 'jintan'}, '安阳': {'sublist': {'殷都': 'yindou', '安阳': 'anyangxian', '文峰': 'wenfeng', '北关': 'beiguan', '林州': 'linzhouay', '龙安': 'longan', '其他': 'anyangqita'}, 'code': 'ay'}, '通辽': {'sublist': {'通辽周边': 'tongliaozhoubian', '霍林郭勒': 'huolinguole', '扎鲁特旗': 'zaluteqi', '库伦旗': 'kulunqi', '科尔沁': 'keerqinqu', '开鲁': 'kailu', '奈曼旗': 'naimanqi', '科尔沁左翼后旗': 'keerqinyouyihouqi', '科尔沁左翼中旗': 'keerqinyouyizhongq'}, 'code': 'tongliao'}, '博尔塔拉': {'sublist': {'温泉': 'wenquanxian', '精河': 'jinghexian', '博乐': 'boleshi', '博州周边': 'bozhouzb'}, 'code': 'betl'}, '廊坊': {'sublist': {'霸州': 'bazhoulf', '香河': 'xianghelf', '永清': 'yongqing', '开发区': 'lfkaifaqu', '大城': 'dachengxian', '广阳': 'lfguangyang', '安次': 'anci', '大厂': 'dachang', '三河市': 'langfangsanhe', '燕郊': 'langfangyanjiao', '文安': 'lfwenan', '其他': 'langfang', '固安': 'lfguanlf'}, 'code': 'lf'}, '日照': {'sublist': {'莒县': 'rizhaolvxian', '东港': 'donggangqu', '五莲': 'wulian', '其它': 'rizhaoshi', '岚山': 'lanshan'}, 'code': 'rizhao'}, '昭通': {'sublist': {'巧家': 'qiaojiaxian', '昭通周边': 'zhaotongzhoubian', '彝良': 'yiliangxian', '永善': 'yongshanxian', '鲁甸': 'ludianxian', '昭阳': 'zhaoyangqu', '大关': 'daguanxian'}, 'code': 'zt'}, '安顺': {'sublist': {'平坝': 'pingbaxian', '紫云': 'asziyun', '普定县': 'pudingxian', '安顺周边': 'anshunzhoubian', '镇宁': 'aszhenning', '关岭': 'asguanling', '西秀': 'xixiuqu'}, 'code': 'anshun'}, '临邑': {'sublist': {'其他': 'linyixianqqt', '城区': 'linyixianqcq'}, 'code': 'linyixianq'}, '乐清': {'sublist': {'石帆': 'yqshifan', '湖雾': 'yqhuwu', '乐清周边': 'yqyueqingzhoubian', '虹桥': 'yqhongqiao', '淡溪': 'yqdanxi', '芙蓉': 'yqfurong', '柳市': 'yqliushi', '蒲岐': 'yqpuqi', '七里港': 'yqqiligang', '翁垟': 'yqwengxiang', '南塘': 'yqnantang', '大荆': 'yqdajing', '北白象': 'yqbeibaixiang', '清江': 'yqqingjiang', '磐石': 'yqpanshi', '南岳': 'yqnanyue', '仙溪': 'yqxianxi', '乐成': 'yqlecheng', '象阳': 'yqxiangyang', '白石': 'yqbaishi', '雁荡': 'yqyandang', '黄华': 'yqhuanghua'}, 'code': 'yueqingcity'}, '贵阳': {'sublist': {'乌当': 'wudang', '花溪': 'huaxi', '云岩': 'yunyan', '金阳新区': 'jinyangxinqu', '南明': 'nanming', '小河': 'xiaohequ', '白云': 'baiyunqv', '小河片': 'xiaohepian', '清镇': 'qingzhengy', '贵阳周边': 'guiyang'}, 'code': 'gy'}, '顺德': {'sublist': {'均安': 'junyan', '乐从': 'luochong', '龙江': 'longjiangz', '北滘': 'beijiao', '勒流': 'leliu', '伦教': 'lunjiao', '陈村': 'chencun', '容桂': 'yonggui', '大良': 'daliang', '顺德': 'shunde', '杏坛': 'xintan'}, 'code': 'sd'}, '宣城': {'sublist': {'广德': 'guangde', '旌德': 'jingde', '宣州': 'xuanzhou', '绩溪': 'jixixian', '其它': 'xuanchengshi', '郎溪': 'langxi', '泾县': 'hzjingxian', '宁国': 'ningguoqu'}, 'code': 'xuancheng'}}
    page_num = 1
    judge = 0
    total = 0
    jobs_url_li = []
    job_save_58 = []
    flag_next = True
    job_linshi=[]
    job_linshi_id = []
    fan_ye=0

    while flag_next:
        time.sleep(2)
        try:
            try:
                city_jc = cityList_dic[cityName]['code']
            except:
                traceback.print_exc()
                judge = 1
                break
            d_pos = {"kw111": compName}
            postname = parse.urlencode(d_pos).encode('utf-8')
            postname = str(postname).split('kw111=')[1][:-1]
            if countyName != '':
                try:
                    county_jc=cityList_dic[cityName]['sublist'][countyName]
                    url_58_zwss = 'http://' + city_jc + '.58.com/'+ county_jc +'/job/pn' + str(page_num) + '/?key=' + str(postname)+'&final=1&jump=1'
                except:
                    try:
                        county_Name = countyName.replace('区','')
                        county_jc = cityList_dic[cityName]['sublist'][county_Name]
                        url_58_zwss = 'http://' + city_jc + '.58.com/' + county_jc + '/job/pn' + str(page_num) + '/?key=' + str(postname)+'&final=1&jump=1'
                    except:
                        url_58_zwss = 'http://' + city_jc + '.58.com/job/pn' + str(page_num) + '/?key=' + str(postname)+'&final=1&jump=1'
                        pass
            else:
                url_58_zwss = 'http://' + city_jc + '.58.com/job/pn' + str(page_num) + '/?key=' + str(postname)+'&final=1&jump=1'
            print('58----', url_58_zwss)

            try:
                html_li_text=xh_pd_req(pos_url=url_58_zwss,data='',headers=head_reqst())
                # print(html_li_text)

            except:
                traceback.print_exc()
                flag_next = False
                break
            # request_li = request.Request(url=url_58_zwss, headers=head_reqst())
            # reponse_li = request.urlopen(request_li,timeout=3).read()
            # html_li_text = reponse_li.decode('utf-8', errors='ignore')
            # print(html_li_text)
            if '58同城' in html_li_text:
                sel = Selector(text=html_li_text)
                xpa_58job_li = '//ul[@id="list_con"]/li'
                for job_58 in sel.xpath(xpa_58job_li):
                    job58_name = job_58.xpath('div[@class="item_con job_comp"]/div[@class="comp_name"]/a/@title').extract()[0]
                    if job58_name == compName:
                        job58_url = \
                        job_58.xpath('div[@class="item_con job_title"]/div[@class="job_name clearfix"]/a/@href').extract()[0]
                        # print(job58_url)
                        job58_id=job58_url.split("entinfo=")[1].split("_q")[0]
                        if 'http' not in job58_url:
                            job58_url = 'http://' + job58_url

                        #如果链接为一条新的链接
                        if job58_id not in job_linshi:
                            fan_ye=1
                            jobs_url_li.append(job58_url)
                            job_linshi.append(job58_id)
                            job_linshi_id.append(job58_id)
                        else:
                            fan_ye=0
                            flag_next = False

                #判断是否进入下一页
                try:
                    if fan_ye != 0 and job_linshi_id != []:
                        # print("下一页")
                        page_num=page_num+1
                        if page_num >50:
                            flag_next = False
                    else:
                        flag_next = False
                    job_linshi_id = []
                except:
                    flag_next = False
                    pass
        except:
            flag_next = False
            logging.exception("Exception Logged")
            pass
    try:
        for index, job58_url1 in enumerate(jobs_url_li):
            # print(index)
            time.sleep(random.uniform(0.3, 0.6))
            try:
                job_xq_text=xh_pd_req(pos_url=job58_url1,data='',headers=head_reqst())
                # request_job_xq = request.Request(url=job58_url1, headers=head_reqst())
                # response_job_xq = request.urlopen(request_job_xq,timeout=3).read()
                # job_xq_text = response_job_xq.decode('utf-8', errors='ignore')
            except:
                logging.exception("Exception Logged")
                continue
            try:
                # print(job_xq_text)
                zw_data_58 = zwjx_58(text=job_xq_text, compName=compName)
                zw_data_58['type'] = 'job'
                zw_data_58['channel'] = channelid
                zw_data_58['companyName'] = compName
                zw_data_58['province'] = provName
                zw_data_58['city'] = cityName_0
                zw_data_58['county'] = countyName
                print('58-------', zw_data_58)
                job_save_58.append(zw_data_58)
            except:
                logging.exception("Exception Logged")
                sj_str = str(int(time.time() * 1000))
                logging.error('58_job_jx_fail----' + sj_str)

            if len(job_save_58) == 3:
                total=total + 3
                data = json.dumps(job_save_58)
                data = data.encode('utf-8')
                requests.post(url=job_save_url, data=data)
                logging.error('58_jobl----3')
                job_save_58 = []
        if len(job_save_58) == 3 or len(job_save_58) == 0:
            pass
        else:
            total = total + len(job_save_58)
            data = json.dumps(job_save_58)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
            logging.error('58_jobl----yfs')
    except:
        logging.exception("Exception Logged")
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_gjzw(compName, provName, cityName, countyName,cityName_0, channelid=4):
    dict_city = {'乐山': {'sublist': {'夹江': 'jiajiang', '马边': 'mabian', '沙湾': 'shawan', '峨眉山': 'emeishan', '市中': 'shizhong', '五通桥': 'wutongqiao', '井研': 'jingyan', '峨边': 'ebian', '犍为': 'jianwei', '金口河': 'jinkouhe', '沐川': 'muchuan'}, 'code': 'leshan'}, '阿拉尔': {'sublist': {'团场': 'tuanchang', '南口街道': 'nankoujiedao', '阿拉尔周边': 'alaerzhoubian', '青松路街道': 'qingsonglujiedao', '幸福路街道': 'xingfulujiedao', '金银川路街道': 'jinyinchuanlujiedao'}, 'code': 'alaer'}, '玉溪': {'sublist': {'新平': 'xinping', '华宁': 'huaning', '红塔': 'hongta', '峨山': 'eshan', '易门': 'yimen', '通海': 'tonghai', '江川': 'jiangchuan', '澄江': 'chengjiang', '元江': 'yuanjiang'}, 'code': 'yuxi'}, '乌海': {'sublist': {'乌达': 'wuda', '海南': 'hainan', '海勃湾': 'haibowan'}, 'code': 'wuhai'}, '林芝': {'sublist': {'林芝县': 'linzhixian', '波密': 'bomi', '墨脱': 'motuo', '朗县': 'langxian', '工布江达': 'gongbujiangda', '察隅': 'chayu', '米林': 'milin'}, 'code': 'linzhi'}, '焦作': {'sublist': {'武陟': 'wuzhi', '解放': 'jiefang', '修武': 'xiuwu', '马村': 'macun', '博爱': 'boai', '山阳': 'shanyang', '高新': 'gaoxin', '中站': 'zhongzhan', '沁阳': 'qinyang', '孟州': 'mengzhou', '温县': 'wenxian'}, 'code': 'jiaozuo'}, '图木舒克': {'sublist': {'喀拉拜勒镇': 'kalabailezhen', '金墩': 'jindun', '皮恰克松地': 'piqiakesongdi', '图木休克': 'tumuxiuke', '图木舒克市区': 'tumushukeshiqu', '盖米里克': 'gaimilike', '其盖麦旦': 'qigaimaidan', '图木舒克周边': 'tumushukezhoubian', '永安坝': 'yonganba'}, 'code': 'tumushuke'}, '宁波': {'sublist': {'海曙': 'haishu', '奉化': 'fenghua', '鄞州': 'yinzhou', '余姚': 'yuyao', '宁海': 'ninghai', '象山': 'xiangshan', '江东': 'jiangdong', '镇海': 'zhenhai', '江北': 'jiangbei', '慈溪': 'cixi', '北仑': 'beilun', '甬江': 'yongjiang'}, 'code': 'nb'}, '株洲': {'sublist': {'醴陵': 'liling', '芦淞': 'lusong', '荷塘': 'hetang', '炎陵': 'yanling', '天元': 'tianyuan', '株洲县': 'zhuzhou', '茶陵': 'chaling', '石峰': 'shifeng', '攸县': 'youxian'}, 'code': 'zhuzhou'}, '淄博': {'sublist': {'临淄': 'linzi', '桓台': 'huantai', '淄川': 'zichuan', '周村': 'zhoucun', '高新区': 'gaoxinqu', '高青': 'gaoqing', '沂源': 'yiyuan', '张店': 'zhangdian', '博山': 'boshan'}, 'code': 'zibo'}, '克拉玛依': {'sublist': {'克拉玛依区': 'kelamayi', '白碱滩': 'baijiantan', '独山子': 'dushanzi', '乌尔禾': 'wuerhe'}, 'code': 'kelamayi'}, '潜江': {'sublist': {'张金': 'jinzhen', '浩口': 'haokou', '周矶': 'zhouji', '熊口': 'xiongkou', '竹根滩': 'zhugentan', '广华': 'guanghua', '积玉口': 'jiyukou', '龙湾': 'longwan', '杨市': 'yangshi', '园林': 'yuanlin', '王场': 'wangchang', '老新': 'laoxin', '泽口': 'zekou', '渔洋': 'yuyang', '高石碑': 'gaoshibei'}, 'code': 'qianjiang'}, '咸阳': {'sublist': {'乾县': 'qianxian', '彬县': 'binxian', '泾阳': 'jingyang', '永寿': 'yongshou', '杨陵': 'yangling', '武功': 'wugong', '渭城': 'weicheng', '旬邑': 'xunyi', '礼泉': 'liquan', '兴平': 'xingping', '长武': 'changwu', '三原': 'sanyuan', '淳化': 'chunhua', '秦都': 'qindou'}, 'code': 'xianyang'}, '定西': {'sublist': {'临洮': 'lintao', '岷县': 'minxian', '安定': 'anding', '陇西': 'longxi', '渭源': 'weiyuan', '通渭': 'tongwei', '漳县': 'zhangxian'}, 'code': 'dingxi'}, '锡林郭勒': {'sublist': {'苏尼特左': 'sunitezuo', '太仆寺': 'taipusi', '正镶白': 'zhengxiangbai', '苏尼特右': 'suniteyou', '镶黄': 'xianghuang', '二连浩特': 'erlianhaote', '西乌珠穆沁': 'xiwuzhumuqin', '阿巴嘎': 'abaga', '东乌珠穆沁': 'dongwuzhumuqin', '正蓝': 'zhenglan', '多伦': 'duolun', '锡林浩特': 'xilinhaote'}, 'code': 'xilinguole'}, '三亚': {'sublist': {'亚龙湾': 'yalongwan', '河东': 'hedong', '海棠湾': 'haitangwan', '三亚湾': 'sanyawan', '凤凰': 'fenghuang', '吉阳': 'jiyang', '凤凰岛': 'fenghuangdao', '河西': 'hexi', '田独': 'tiandu', '天涯': 'tianya', '育才': 'yucai', '崖城': 'yacheng', '大东海': 'dadonghai'}, 'code': 'sanya'}, '中卫': {'sublist': {'中宁': 'zhongning', '沙坡头': 'shapotou', '海原': 'haiyuan'}, 'code': 'zhongwei'}, '淮南': {'sublist': {'潘集': 'panji', '凤台': 'fengtai', '寿县': 'shouxian', '田家庵': 'tianjiaan', '八公山': 'bagongshan', '谢家集': 'xiejiaji', '大通': 'datong'}, 'code': 'huainan'}, '阜新': {'sublist': {'清河门': 'qinghemen', '细河': 'xihe', '海州': 'haizhou', '新邱': 'xinqiu', '阜新县': 'fuxin', '太平': 'taiping', '彰武': 'zhangwu'}, 'code': 'fuxin'}, '淮安': {'sublist': {'洪泽': 'hongze', '盱眙': 'xuyi', '涟水': 'lianshui', '经济开发区': 'jingjikaifaqu', '淮阴': 'huaiyin', '清浦': 'qingpu', '楚州': 'chuzhou', '清河': 'qinghe', '金湖': 'jinhu'}, 'code': 'huaian'}, '昌吉': {'sublist': {'昌吉市': 'changji', '吉木萨尔': 'jimusaer', '呼图壁': 'hutubi', '米泉': 'miquan', '阜康': 'fukang', '奇台': 'qitai', '玛纳斯': 'manasi', '木垒': 'mulei'}, 'code': 'changji'}, '三门峡': {'sublist': {'卢氏': 'lushi', '湖滨': 'hubin', '灵宝': 'lingbao', '陕县': 'shanxian', '渑池': 'mianchi', '义马': 'yima'}, 'code': 'sanmenxia'}, '吉安': {'sublist': {'泰和': 'taihe', '永新': 'yongxin', '青原': 'qingyuan', '遂川': 'suichuan', '万安': 'wanan', '吉州': 'jizhou', '永丰': 'yongfeng', '吉安县': 'jianxian', '安福': 'anfu', '峡江': 'xiajiang', '吉水': 'jishui', '新干': 'xingan', '井冈山': 'jinggangshan'}, 'code': 'jian'}, '益阳': {'sublist': {'桃江': 'taojiang', '安化': 'anhua', '沅江': 'yuanjiang', '资阳': 'ziyang', '赫山': 'heshan', '南县': 'nanxian'}, 'code': 'yiyang'}, '深圳': {'sublist': {'南山': 'nanshan', '福田': 'futian', '龙华新区': 'longhuaxinqu', '盐田': 'yantian', '罗湖': 'luohu', '坪山新区': 'pingshanxinqu', '深圳周边': 'shenzhenzhoubian', '大鹏新区': 'dapengxinqu', '宝安': 'baoan', '龙岗': 'longgang', '光明新区': 'guangmingxinqu'}, 'code': 'sz'}, '晋城': {'sublist': {'泽州': 'zezhou', '陵川': 'lingchuan', '阳城': 'yangcheng', '沁水': 'qinshui', '城区': 'chengqu', '高平': 'gaoping'}, 'code': 'jincheng'}, '宿迁': {'sublist': {'宿豫': 'suyu', '泗洪': 'sihong', '泗阳': 'siyang', '宿城区': 'suchengqu', '沭阳': 'shuyang'}, 'code': 'suqian'}, '九江': {'sublist': {'永修': 'yongxiu', '都昌': 'douchang', '彭泽': 'pengze', '修水': 'xiushui', '瑞昌': 'ruichang', '庐山': 'lushan', '浔阳': 'xunyang', '湖口': 'hukou', '德安': 'dean', '九江县': 'jiujiang', '星子': 'xingzi', '武宁': 'wuning'}, 'code': 'jiujiang'}, '保定': {'sublist': {'保定周边': 'baodingzhoubian', '高阳': 'gaoyang', '涿州': 'zhuozhou', '高碑店': 'gaobeidian', '新市区': 'xinshi', '满城': 'mancheng', '阜平': 'fuping', '涞源': 'laiyuan', '蠡县': 'lixian', '徐水': 'xushui', '南市区': 'nanshi', '清苑': 'qingyuan', '安新': 'anxin', '曲阳': 'quyang', '望都': 'wangdou', '高开区': 'gaokai', '容城': 'rongcheng', '北市区': 'beishi', '顺平': 'shunping', '唐县': 'tangxian', '博野': 'boye', '易县': 'yixian', '雄县': 'xiongxian', '定州': 'dingzhou', '定兴': 'dingxing', '涞水': 'laishui', '安国': 'anguo'}, 'code': 'baoding'}, '河池': {'sublist': {'宜州': 'yizhou', '环江': 'huanjiang', '南丹': 'nandan', '大化': 'dahua', '巴马': 'bama', '凤山': 'fengshan', '天峨': 'tiane', '都安': 'douan', '东兰': 'donglan', '罗城': 'luocheng', '金城江': 'jinchengjiang'}, 'code': 'hechi'}, '马鞍山': {'sublist': {'含山县': 'hanshanxian', '花山': 'huashan', '当涂': 'dangtu', '和县': 'hexian', '雨山': 'yushan', '博望': 'bowang', '金家庄': 'jinjiazhuang'}, 'code': 'maanshan'}, '济宁': {'sublist': {'邹城': 'zoucheng', '嘉祥': 'jiaxiang', '任城': 'rencheng', '金乡': 'jinxiang', '汶上': 'wenshang', '鱼台': 'yutai', '微山': 'weishan', '梁山': 'liangshan', '泗水': 'sishui', '兖州': 'yanzhou', '市中': 'shizhong', '曲阜': 'qufu'}, 'code': 'jining'}, '巴中': {'sublist': {'平昌': 'pingchang', '巴州': 'bazhou', '南江': 'nanjiang', '通江': 'tongjiang'}, 'code': 'bazhong'}, '黔东南': {'sublist': {'麻江': 'majiang', '台江': 'taijiang', '施秉': 'shibing', '镇远': 'zhenyuan', '从江': 'congjiang', '三穗': 'sansui', '剑河': 'jianhe', '榕江': 'rongjiang', '黎平': 'liping', '雷山': 'leishan', '凯里': 'kaili', '丹寨': 'danzhai', '岑巩': 'cengong', '天柱': 'tianzhu', '黄平': 'huangping', '锦屏': 'jinping'}, 'code': 'qiandongnan'}, '潮州': {'sublist': {'湘桥': 'xiangqiao', '饶平': 'raoping', '潮安': 'chaoan'}, 'code': 'chaozhou'}, '太原': {'sublist': {'万柏林': 'wanbailin', '清徐': 'qingxu', '小店': 'xiaodian', '杏花岭': 'xinghualing', '古交': 'gujiao', '阳曲': 'yangqu', '迎泽': 'yingze', '娄烦': 'loufan', '尖草坪': 'jiancaoping', '晋源': 'jinyuan'}, 'code': 'ty'}, '榆林': {'sublist': {'北郊': 'beijiao', '靖边': 'jingbian', '南郊': 'nanjiao', '定边': 'dingbian', '吴堡': 'wubao', '开发区': 'kaifaqu', '榆阳': 'yuyang', '神木': 'shenmu', '绥德': 'suide', '市中心': 'shizhongxin', '清涧': 'qingjian', '佳县': 'jiaxian', '府谷': 'fugu', '米脂': 'mizhi', '横山': 'hengshan', '子洲': 'zizhou', '西沙': 'xisha', '东沙': 'dongsha'}, 'code': 'sxyulin'}, '防城港': {'sublist': {'港口': 'gangkou', '东兴': 'dongxing', '上思': 'shangsi', '防城': 'fangcheng'}, 'code': 'fangchenggang'}, '驻马店': {'sublist': {'遂平': 'suiping', '新蔡': 'xincai', '驿城': 'yicheng', '确山': 'queshan', '正阳': 'zhengyang', '西平': 'xiping', '平舆': 'pingyu', '汝南': 'runan', '上蔡': 'shangcai', '泌阳': 'miyang'}, 'code': 'zhumadian'}, '邵阳': {'sublist': {'洞口': 'dongkou', '新邵': 'xinshao', '城步': 'chengbu', '北塔': 'beita', '大祥': 'daxiang', '隆回': 'longhui', '邵东': 'shaodong', '邵阳县': 'shaoyangxian', '武冈': 'wugang', '绥宁': 'suining', '双清': 'shuangqing', '新宁': 'xinning'}, 'code': 'shaoyang'}, '东营': {'sublist': {'利津': 'lijin', '广饶': 'guangrao', '河口': 'hekou', '垦利': 'kenli', '东营区': 'dongying'}, 'code': 'dongying'}, '赣州': {'sublist': {'瑞金': 'ruijin', '于都': 'yudou', '大余': 'dayu', '宁都': 'ningdou', '定南': 'dingnan', '信丰': 'xinfeng', '开发区': 'kaifaqu', '南康': 'nankang', '上犹': 'shangyou', '安远': 'anyuan', '全南': 'quannan', '章贡': 'zhanggong', '会昌': 'huichang', '寻乌': 'xunwu', '石城': 'shicheng', '龙南': 'longnan', '崇义': 'chongyi', '赣县': 'ganxian', '兴国': 'xingguo'}, 'code': 'ganzhou'}, '廊坊': {'sublist': {'固安': 'guan', '大厂': 'dachang', '燕郊': 'yanjiao', '三河': 'sanhe', '霸州': 'bazhou', '永清': 'yongqing', '开发区': 'kaifaqu', '文安': 'wenan', '广阳区': 'guangyang', '安次区': 'anci', '香河': 'xianghe', '大城': 'dacheng'}, 'code': 'langfang'}, '香港': {'sublist': {'湾仔区': 'wanzai', '黄大仙区': 'huangdaxian', '南区': 'nanqu', '离岛区': 'lidao', '大埔区': 'dapu', '观塘区': 'guangtang', '中西区': 'zhongxi', '沙田区': 'shatian', '深水埗区': 'shengshuibu', '油尖旺区': 'youjianwang', '元朗区': 'yuanlang', '荃湾区': 'quanwan', '九龙城区': 'jiulong', '西贡区': 'xigong', '屯门区': 'tuimen', '北区': 'beiqu', '东区': 'dongqu', '葵青区': 'kuiqing'}, 'code': 'xianggang'}, '日喀则': {'sublist': {'日喀则市': 'rikazeshi', '南木林': 'nanmulin', '定结': 'dingjie', '聂拉木': 'nielamu', '萨迦': 'sajia', '仁布': 'renbu', '谢通门': 'xietongmen', '萨嘎': 'saga', '康马': 'kangma', '江孜': 'jiangzi', '定日': 'dingri', '拉孜': 'lazi', '吉隆': 'jilong', '岗巴': 'gangba', '亚东': 'yadong', '仲巴': 'zhongba', '白朗': 'bailang', '昂仁': 'angren'}, 'code': 'rikaze'}, '无锡': {'sublist': {'崇安': 'chongan', '滨湖': 'binhu', '锡山': 'xishan', '宜兴': 'yixing', '南长': 'nanchang', '江阴': 'jiangyin', '惠山': 'huishan', '新区': 'xinqu', '北塘': 'beitang'}, 'code': 'wx'}, '渭南': {'sublist': {'华县': 'huaxian', '华阴': 'huayin', '白水': 'baishui', '韩城': 'hancheng', '富平': 'fuping', '合阳': 'heyang', '大荔': 'dali', '临渭': 'linwei', '澄城': 'chengcheng', '潼关': 'tongguan', '蒲城': 'pucheng'}, 'code': 'weinan'}, '辽源': {'sublist': {'东辽': 'dongliao', '西安区': 'xianqu', '东丰': 'dongfeng', '龙山区': 'longshanqu'}, 'code': 'liaoyuan'}, '滨州': {'sublist': {'无棣': 'wuli', '邹平': 'zouping', '滨城': 'bincheng', '沾化': 'zhanhua', '惠民': 'huimin', '阳信': 'yangxin', '博兴': 'boxing'}, 'code': 'binzhou'}, '吕梁': {'sublist': {'文水': 'wenshui', '柳林': 'liulin', '兴县': 'xingxian', '方山': 'fangshan', '临县': 'linxian', '交口': 'jiaokou', '汾阳': 'fenyang', '离石': 'lishi', '交城': 'jiaocheng', '岚县': 'lanxian', '石楼': 'shilou', '孝义': 'xiaoyi', '中阳': 'zhongyang'}, 'code': 'lvliang'}, '阿拉善': {'sublist': {'阿拉善右': 'alashanyou', '阿拉善左': 'alashanzuo', '额济纳': 'ejina'}, 'code': 'alashan'}, '泸州': {'sublist': {'古蔺': 'gulin', '泸县': 'luxian', '江阳': 'jiangyang', '合江': 'hejiang', '叙永': 'xuyong', '纳溪': 'naxi', '龙马潭': 'longmatan'}, 'code': 'luzhou'}, '白山': {'sublist': {'八道江区': 'badaojiangqu', '江源区': 'jiangyuanqu', '抚松县': 'fusongxian', '长白': 'zhangbai', '临江市': 'linjiangshi', '靖宇县': 'jingyuxian'}, 'code': 'baishan'}, '铜仁': {'sublist': {'玉屏': 'yuping', '石阡': 'shiqian', '印江': 'yinjiang', '铜仁市': 'tongren', '沿河': 'yanhe', '松桃': 'songtao', '德江': 'dejiang', '江口': 'jiangkou', '万山': 'wanshan', '思南': 'sinan'}, 'code': 'tongren'}, '昆明': {'sublist': {'富民': 'fumin', '安宁': 'anning', '晋宁': 'jinning', '呈贡': 'chenggong', '石林': 'shilin', '嵩明': 'songming', '东川': 'dongchuan', '禄劝': 'luquan', '宜良': 'yiliang', '西山': 'xishan', '盘龙': 'panlong', '官渡': 'guandu', '寻甸': 'xundian', '五华': 'wuhua'}, 'code': 'km'}, '葫芦岛': {'sublist': {'连山': 'lianshan', '建昌': 'jianchang', '兴城': 'xingcheng', '龙港': 'longgang', '绥中': 'suizhong', '南票': 'nanpiao'}, 'code': 'huludao'}, '威海': {'sublist': {'环翠': 'huancui', '文登': 'wendeng', '高区': 'gaoqu', '经区': 'jingqu', '荣成': 'rongcheng', '乳山': 'rushan'}, 'code': 'wei'}, '忻州': {'sublist': {'繁峙': 'fanzhi', '宁武': 'ningwu', '岢岚': 'kelan', '忻府': 'xinfu', '保德': 'baode', '五寨': 'wuzhai', '静乐': 'jingle', '代县': 'daixian', '神池': 'shenchi', '偏关': 'pianguan', '定襄': 'dingxiang', '河曲': 'hequ', '五台': 'wutai', '原平': 'yuanping'}, 'code': 'xinzhou'}, '大连': {'sublist': {'中山': 'zhongshan', '西岗': 'xigang', '普兰店': 'pulandian', '长海': 'changhai', '开发区': 'kaifa', '沙河口': 'shahekou', '甘井子': 'ganjingzi', '金州': 'jinzhou', '旅顺口': 'lvshunkou', '瓦房店': 'wafangdian', '大连周边': 'dalianzhoubian', '庄河': 'zhuanghe', '高新园区': 'gaoxinyuanqu'}, 'code': 'dl'}, '即墨': {'sublist': {'鳌山卫镇': 'aoshanweizhen', '宝龙城市广场': 'jimobaolongchengshiguangchang', '店集镇': 'dianjizhen', '南泉镇': 'nanquanzhen', '通济': 'tongji', '田横镇': 'tianhengzhen', '潮海': 'chaohai', '温泉镇': 'wenquanzhen', '其他': 'jimoqita', '华山镇': 'huashanzhen', '普东镇镇': 'pudongzhenzhen', '北安': 'beian', '丰城镇': 'fengchengzhen', '龙泉镇': 'longquanzhen', '泊岚镇': 'bolanzhen', '王村镇': 'wangcunzhen', '七级镇': 'qijizhen', '灵山镇': 'lingshanzhen', '蓝村镇': 'lancunzhen', '和平区': 'hepingqu', '联通大厦': 'liantongdasha', '大信镇': 'daxinzhen', '开发区': 'kaifaqu', '大润发': 'darunfa', '刘家庄': 'liujiazhuang', '金口镇': 'jinkouzhen', '新汽车站': 'xinqichezhan', '环秀': 'huanxiu', '即墨周边': 'jimozhoubian', '移风店镇': 'yifengdianzhen', '名都苑': 'mingdouyuan', '龙山': 'longshan'}, 'code': 'jimo'}, '张家界': {'sublist': {'慈利': 'cili', '桑植': 'sangzhi', '永定': 'yongding', '武陵源': 'wulingyuan'}, 'code': 'zhangjiajie'}, '牡丹江': {'sublist': {'穆棱': 'muleng', '林口': 'linkou', '东宁': 'dongning', '宁安': 'ningan', '爱民': 'aimin', '东安': 'dongan', '海林': 'hailin', '阳明': 'yangming', '绥芬河': 'suifenhe', '西安': 'xian'}, 'code': 'mudanjiang'}, '固原': {'sublist': {'泾源': 'jingyuan', '原州': 'yuanzhou', '隆德': 'longde', '西吉': 'xiji', '彭阳': 'pengyang'}, 'code': 'guyuan'}, '揭阳': {'sublist': {'榕城': 'rongcheng', '揭西': 'jiexi', '惠来': 'huilai', '普宁': 'puning', '揭东': 'jiedong'}, 'code': 'jieyang'}, '果洛': {'sublist': {'班玛': 'banma', '久治': 'jiuzhi', '甘德': 'gande', '达日': 'dari', '玛多': 'maduo', '玛沁': 'maqin'}, 'code': 'guoluo'}, '聊城': {'sublist': {'高唐': 'gaotang', '冠县': 'guanxian', '莘县': 'shenxian', '茌平': 'chiping', '阳谷': 'yanggu', '临清': 'linqing', '开发区': 'liaochengkaifaqu', '东阿': 'donga', '东昌府': 'dongchangfu'}, 'code': 'liaocheng'}, '济南': {'sublist': {'章丘': 'zhangqiu', '槐荫': 'huaiyin', '平阴': 'pingyin', '商河': 'shanghe', '天桥': 'tianqiao', '济阳': 'jiyang', '历下': 'lixia', '长清': 'changqing', '其他': 'qita', '高新': 'gaoxin', '历城': 'licheng', '市中': 'shizhong'}, 'code': 'jn'}, '菏泽': {'sublist': {'郓城': 'yuncheng', '定陶': 'dingtao', '曹县': 'caoxian', '单县': 'danxian', '牡丹': 'mudan', '东明': 'dongming', '鄄城': 'juancheng', '成武': 'chengwu', '巨野': 'juye'}, 'code': 'heze'}, '凉山': {'sublist': {'甘洛': 'ganluo', '德昌': 'dechang', '盐源': 'yanyuan', '会理': 'huili', '美姑': 'meigu', '西昌': 'xichang', '木里': 'muli', '喜德': 'xide', '普格': 'puge', '雷波': 'leibo', '布拖': 'butuo', '会东': 'huidong', '宁南': 'ningnan', '冕宁': 'mianning', '越西': 'yuexi', '金阳': 'jinyang', '昭觉': 'zhaojue'}, 'code': 'liangshan'}, '拉萨': {'sublist': {'城关': 'chengguan', '林周': 'linzhou', '当雄': 'dangxiong', '墨竹工卡': 'mozhugongka', '堆龙德庆': 'duilongdeqing', '曲水': 'qushui', '尼木': 'nimu', '达孜': 'dazi'}, 'code': 'xz'}, '绵阳': {'sublist': {'经开': 'jingkai', '平武': 'pingwu', '三台': 'santai', '科创园': 'kechuangyuan', '北川': 'beichuan', '梓潼': 'zitong', '盐亭': 'yanting', '安县': 'anxian', '高新': 'gaoxin', '涪城': 'fucheng', '游仙': 'youxian', '江油': 'jiangyou'}, 'code': 'mianyang'}, '鄂尔多斯': {'sublist': {'乌审': 'wushen', '东胜': 'dongsheng', '鄂托克前': 'etuokeqian', '伊金霍洛': 'yijinhuoluo', '准格尔': 'zhungeer', '杭锦': 'hangjin', '鄂托克': 'etuoke', '达拉特': 'dalate'}, 'code': 'eerduosi'}, '宝鸡': {'sublist': {'眉县': 'meixian', '陇县': 'longxian', '岐山': 'qishan', '麟游': 'linyou', '凤县': 'fengxian', '金台': 'jintai', '千阳': 'qianyang', '太白': 'taibai', '渭滨': 'weibin', '扶风': 'fufeng', '凤翔': 'fengxiang', '陈仓': 'chencang'}, 'code': 'baoji'}, '惠州': {'sublist': {'博罗': 'boluo', '惠州周边': 'huizhouzhoubian', '仲恺区': 'zhongkaiqu', '惠阳': 'huiyang', '龙门': 'longmen', '惠城': 'huicheng', '大亚湾区': 'dayawanqu', '惠东': 'huidong'}, 'code': 'huizhou'}, '漳州': {'sublist': {'龙海': 'longhai', '云霄': 'yunxiao', '长泰': 'changtai', '东山': 'dongshan', '平和': 'pinghe', '漳浦': 'zhangpu', '华安': 'huaan', '龙文': 'longwen', '南靖': 'nanjing', '其他': 'qita', '诏安': 'zhaoan', '芗城': 'xiangcheng', '角美': 'jiaomei'}, 'code': 'zhangzhou'}, '安顺': {'sublist': {'关岭': 'guanling', '西秀': 'xixiu', '平坝': 'pingba', '镇宁': 'zhenning', '普定': 'puding', '紫云': 'ziyun'}, 'code': 'anshun'}, '黄山': {'sublist': {'屯溪': 'tunxi', '徽州': 'huizhou', '祁门': 'qimen', '黄山区': 'huangshan', '黟县': 'yixian', '歙县': 'xixian', '休宁': 'xiuning'}, 'code': 'huangshan'}, '天门': {'sublist': {'卢市': 'lushi', '彭市': 'pengshi', '拖市': 'tuoshi', '竟陵': 'jingling', '干驿': 'qianyi', '麻洋': 'mayang', '候口': 'houkou', '小板': 'xiaoban', '汪场': 'wangchang', '胡市': 'hushi', '皂市': 'zaoshi', '渔薪': 'yuxin', '佛子山': 'fozishan', '净潭': 'jingtan', '石河': 'shihe', '张港': 'zhanggang', '蒋场': 'jiangchang', '岳口': 'lekou', '杨林': 'yanglin', '马湾': 'mawan', '黄潭': 'huangtan', '九真': 'jiuzhen', '横林': 'henglin', '多祥': 'duoxiang', '多宝': 'duobao'}, 'code': 'tianmen'}, '济源': {'sublist': {'承留': 'chengliu', '轵城': 'zhicheng', '王屋': 'wangwu', '思礼': 'sili', '邵原': 'shaoyuan', '坡头': 'potou', '大峪': 'dayu', '天坛': 'tiantan', '玉泉': 'yuquan', '北海': 'beihai', '五龙口': 'wulongkou', '济水': 'jishui', '黎林': 'lilin', '沁园': 'qinyuan', '克井': 'kejing', '下冶': 'xiaye'}, 'code': 'jiyuan'}, '天津': {'sublist': {'西青': 'xiqing', '东丽': 'dongli', '大港': 'dagang', '宝坻': 'baodi', '静海': 'jinghai', '南开': 'nankai', '河东': 'hedong', '北辰': 'beichen', '开发区': 'kaifaqu', '宁河': 'ninghe', '和平': 'heping', '红桥': 'hongqiao', '汉沽': 'hangu', '河北': 'hebei', '津南': 'jinnan', '武清': 'wuqing', '河西': 'hexi', '滨海新区': 'binhaixinqu', '塘沽': 'tanggu', '蓟县': 'jixian', '天津周边': 'tianjinzhoubian'}, 'code': 'tj'}, '澳门': {'sublist': {'大堂': 'datang', '嘉模堂': 'jiamotang', '圣安多尼堂': 'shenganduonitang', '其他堂区': 'qitatang', '望德堂': 'wangdetang', '圣方济各堂': 'shengfangjigetang', '花地玛堂': 'huadimatang', '风顺堂': 'fengshuntang'}, 'code': 'aomen'}, '东莞': {'sublist': {'万江': 'wanjiang', '虎门': 'humen', '东城': 'dongcheng', '长安': 'changan', '松山湖': 'songshanhu', '塘厦': 'tangsha', '东坑': 'dongkeng', '寮步': 'liaobu', '樟木头': 'zhangmutou', '石排': 'shipai', '茶山': 'chashan', '莞城': 'guancheng', '望牛墩': 'wangniudun', '清溪': 'qingxi', '沙田': 'shatian', '凤岗': 'fenggang', '洪梅': 'hongmei', '南城': 'nancheng', '黄江': 'huangjiang', '企石': 'qishi', '横沥': 'hengli', '常平': 'changping', '麻涌': 'mayong', '桥头': 'qiaotou', '石碣': 'shijie', '大岭山': 'dalingshan', '厚街': 'houjie', '道滘': 'daorong', '大朗': 'dalang', '高埗': 'gaobu', '中堂': 'zhongtang', '谢岗': 'xiegang', '石龙': 'shilong'}, 'code': 'dg'}, '黑河': {'sublist': {'逊克': 'xunke', '孙吴': 'sunwu', '爱辉': 'aihui', '北安': 'beian', '嫩江': 'nenjiang', '五大连池': 'wudalianchi'}, 'code': 'heihe'}, '盘锦': {'sublist': {'双台子': 'shuangtaizi', '盘山': 'panshan', '兴隆台': 'xinglongtai', '大洼': 'dawa'}, 'code': 'panjin'}, '梅州': {'sublist': {'平远': 'pingyuan', '梅县': 'meixian', '大埔': 'dapu', '兴宁': 'xingning', '梅江': 'meijiang', '丰顺': 'fengshun', '五华': 'wuhua', '蕉岭': 'jiaoling'}, 'code': 'meizhou'}, '枣庄': {'sublist': {'峄城': 'yicheng', '市中': 'shizhong', '滕州': 'tengzhou', '台儿庄': 'taierzhuang', '山亭': 'shanting', '薛城': 'xuecheng'}, 'code': 'zaozhuang'}, '那曲': {'sublist': {'班戈': 'bange', '比如': 'biru', '巴青': 'baqing', '申扎': 'anzha', '索县': 'suoxian', '安多': 'anduo', '嘉黎': 'jiali', '双湖': 'shuanghu', '那曲县': 'naquxian', '尼玛': 'nima', '聂荣': 'nierong'}, 'code': 'naqu'}, '丽水': {'sublist': {'龙泉': 'longquan', '景宁': 'jingning', '遂昌': 'suichang', '缙云': 'jinyun', '松阳': 'songyang', '青田': 'pingtian', '庆元': 'qingyuan', '云和': 'yunhe', '莲都': 'liandu'}, 'code': 'lishui'}, '博尔塔拉': {'sublist': {'温泉': 'wenquan', '精河': 'jinghe', '博乐': 'bole'}, 'code': 'boertala'}, '昌都': {'sublist': {'洛隆': 'luolong', '左贡': 'zuogong', '江达': 'jiangda', '察雅': 'chaya', '类乌齐': 'leiwuqi', '昌都县': 'changduxian', '芒康': 'mangkang', '八宿': 'baxiu', '边坝': 'bianba', '贡觉': 'gongjiao', '丁青': 'dingqing'}, 'code': 'changdu'}, '沈阳': {'sublist': {'辽中': 'liaozhong', '康平': 'kangping', '沈北': 'shenbei', '皇姑': 'huanggu', '大东': 'dadong', '法库': 'faku', '和平': 'heping', '抚顺': 'fushun', '沈河': 'shenhe', '浑南': 'hunnan', '于洪': 'yuhong', '铁西': 'tiexi', '新民': 'xinmin', '东陵': 'dongling', '苏家屯': 'sujiatun'}, 'code': 'sy'}, '怀化': {'sublist': {'会同': 'huitong', '沅陵': 'yuanling', '中方': 'zhongfang', '新晃': 'xinhuang', '溆浦': 'xupu', '靖州': 'jingzhou', '麻阳': 'mayang', '辰溪': 'chenxi', '洪江': 'hongjiang', '通道': 'tongdao', '鹤城': 'hecheng', '芷江': 'zhijiang'}, 'code': 'huaihua'}, '哈尔滨': {'sublist': {'道里': 'daoli', '双城': 'shuangcheng', '道外': 'daowai', '南岗': 'nangang', '开发区': 'kaifaqu', '尚志': 'shangzhi', '五常': 'wuchang', '阿城': 'acheng', '平房': 'pingfang', '呼兰': 'hulan', '依兰': 'yilan', '宾县': 'binxian', '江北': 'songbei', '通河': 'tonghe', '木兰': 'mulan', '延寿': 'yanshou', '方正': 'fangzheng', '香坊': 'xiangfang', '巴彦': 'bayan'}, 'code': 'hrb'}, '红河': {'sublist': {'建水': 'jianshui', '蒙自': 'mengzi', '石屏': 'shiping', '个旧': 'gejiu', '河口': 'hekou', '弥勒': 'mile', '元阳': 'yuanyang', '泸西': 'luxi', '开远': 'kaiyuan', '金平': 'jinping', '红河县': 'honghe', '绿春': 'lvchun', '屏边': 'pingbian'}, 'code': 'honghe'}, '徐州': {'sublist': {'铜山': 'tongshan', '泉山': 'quanshan', '睢宁': 'suining', '云龙': 'yunlong', '贾汪': 'jiawang', '鼓楼': 'gulou', '新沂': 'xinyi', '新城区': 'xinchengqu', '沛县': 'peixian', '九里': 'jiuli', '金山桥开发区': 'jinshanqiaokaifaqu', '丰县': 'fengxian', '邳州': 'pizhou'}, 'code': 'xuzhou'}, '伊犁': {'sublist': {'新源': 'xinyuan', '伊宁市': 'yining', '察布查尔': 'chabu', '巩留': 'gongliu', '霍城': 'huocheng', '奎屯': 'kuitun', '特克斯': 'tekesi', '伊宁县': 'yiningxian', '尼勒克': 'nileke', '昭苏': 'zhaosu'}, 'code': 'yili'}, '舟山': {'sublist': {'定海': 'dinghai', '嵊泗': 'shengsi', '岱山': 'daishan', '普陀': 'putuo'}, 'code': 'zhoushan'}, '张掖': {'sublist': {'高台': 'gaotai', '肃南': 'sunan', '临泽': 'linze', '山丹': 'shandan', '甘州': 'ganzhou', '民乐': 'minle'}, 'code': 'zhangye'}, '鄂州': {'sublist': {'鄂城': 'echeng', '梁子湖': 'liangzihu', '华容': 'huarong'}, 'code': 'ezhou'}, '呼伦贝尔': {'sublist': {'满洲里': 'manzhouli', '新巴尔虎左': 'xinbaerhuzuo', '扎兰屯': 'zhalantun', '陈巴尔虎': 'chenbaerhu', '鄂温克族自治': 'ewenkezu', '鄂伦春自治': 'elunchun', '海拉尔': 'hailaer', '新巴尔虎右': 'xinbaerhuyou', '阿荣': 'arong', '牙克石': 'yakeshi', '额尔古纳': 'eerguna', '根河': 'genhe', '莫力达瓦达翰尔族': 'molidawadahanerzu'}, 'code': 'hulunbeier'}, '阜阳': {'sublist': {'颍泉': 'yingquan', '经济开发区': 'jingjikaifaqu', '阜南': 'funan', '颍东经济开发区': 'yingdongjingjikaifaqu', '颍州经济开发区': 'yingzhoujingjikaifaqu', '颍州': 'yingzhou', '颍东': 'yingdong', '临泉': 'linquan', '颍上': 'yingshang', '太和': 'taihe', '界首': 'jieshou', '颍泉经济开发区': 'yingquanjingjikaifaqu'}, 'code': 'fuyang'}, '银川': {'sublist': {'兴庆': 'xingqing', '西夏': 'xixia', '贺兰': 'helan', '永宁': 'yongning', '金凤': 'jinfeng', '灵武': 'lingwu'}, 'code': 'yc'}, '朔州': {'sublist': {'平鲁': 'pinglu', '应县': 'yingxian', '右玉': 'youyu', '朔城': 'shuocheng', '山阴': 'shanyin', '怀仁': 'huairen'}, 'code': 'shuozhou'}, '昆山': {'sublist': {'老城区': 'laochengqu', '花桥': 'huaqiao', '玉山城南': 'kunshanyushanchengnan', '千灯': 'qiandeng', '玉山城北': 'yushan', '玉山城西': 'kunshanyushanchengxi', '玉山城东': 'kunshanyushanchengdong', '周庄': 'zhouzhuang', '张浦': 'zhangpu', '周市': 'zhoushi', '淀山湖': 'dianshanhu', '锦溪': 'jinxi', '陆家': 'lujia', '巴城': 'bacheng', '其他': 'kunshanqita'}, 'code': 'kunshan'}, '铜陵': {'sublist': {'郊区': 'jiao', '铜陵县': 'tonglingxian', '狮子山': 'shizishan', '铜官山': 'tongguanshan'}, 'code': 'tongling'}, '德阳': {'sublist': {'广汉': 'guanghan', '旌阳': 'jingyang', '绵竹': 'mianzhu', '中江': 'zhongjiang', '什邡': 'shenfang', '罗江': 'luojiang'}, 'code': 'deyang'}, '湘西': {'sublist': {'古丈': 'guzhang', '花垣': 'huayuan', '吉首': 'jishou', '保靖': 'baojing', '泸溪': 'luxi', '凤凰': 'fenghuang', '永顺': 'yongshun', '龙山': 'longshan'}, 'code': 'xiangxi'}, '胶州': {'sublist': {'宝龙城市广场': 'jiaozhoubaolongchengshiguangchang', '胶东': 'jiaodong', '阜安': 'fuan', '胶北': 'jiaobei', '张应': 'zhangying', '三里河': 'sanlihe', '常州路': 'changzhoulu', '杭州路': 'jiaozhouhangzhoulu', '胶西': 'jiaoxi', '马店': 'madian', '铺集': 'puji', '云溪': 'yunxi', '胶莱': 'jiaolai', '中云': 'zhongyun', '杜村': 'ducun', '北关': 'beiguan', '南关': 'nanguan', '其他': 'jiaozhouqita', '李哥庄': 'ligezhuang', '锦州路': 'jinzhoulu', '南坦大街': 'nantandajie', '泸州路': 'luzhoulu'}, 'code': 'jiaozhou'}, '普洱': {'sublist': {'孟连': 'menglian', '景谷': 'jinggu', '景东': 'jingdong', '墨江': 'muojiang', '宁洱': 'ninger', '镇沅': 'zhenyuan', '西盟': 'ximeng', '澜沧': 'lancang', '思茅': 'maosi', '江城': 'jiangcheng'}, 'code': 'puer'}, '宜宾': {'sublist': {'屏山': 'pingshan', '珙县': 'gongxian', '兴文': 'xingwen', '江安': 'jiangan', '宜宾县': 'yibin', '筠连': 'junlian', '南溪': 'nanxi', '长宁': 'zhangning', '高县': 'gaoxian', '翠屏': 'cuiping'}, 'code': 'yibin'}, '迪庆': {'sublist': {'香格里拉': 'xianggelila', '维西': 'weixi', '德钦': 'deqin'}, 'code': 'diqing'}, '龙岩': {'sublist': {'上杭': 'shanghang', '新罗': 'xinluo', '永定': 'yongding', '长汀': 'changting', '漳平': 'zhangping', '连城': 'liancheng', '武平': 'wuping'}, 'code': 'longyan'}, '陇南': {'sublist': {'文县': 'wenxian', '礼县': 'lixian', '武都': 'wudou', '宕昌': 'dangchang', '康县': 'kangxian', '徽县': 'huixian', '成县': 'chengxian', '两当': 'liangdang', '西和': 'xihe'}, 'code': 'longnan'}, '泉州': {'sublist': {'泉港': 'quangang', '丰泽': 'fengze', '金门': 'jinmen', '惠安': 'huian', '永春': 'yongchun', '鲤城': 'licheng', '安溪': 'anxi', '石狮': 'shishi', '南安': 'nanan', '洛江': 'luojiang', '台商投资区': 'taishangtouziqu', '德化': 'dehua', '晋江': 'jinjiang'}, 'code': 'quanzhou'}, '四平': {'sublist': {'梨树': 'lishu', '双辽': 'shuangliao', '伊通': 'yitong', '公主岭': 'gongzhuling', '铁西区': 'tiexiqu', '铁东区': 'tiedongqu'}, 'code': 'siping'}, '白城': {'sublist': {'镇赉': 'zhenlai', '洮北区': 'taobeiqu', '大安': 'daan', '通榆': 'tongyu', '工业园区': 'gongyeyuanqu', '开发区': 'kaifaqu', '洮南': 'taonan'}, 'code': 'baicheng'}, '伊春': {'sublist': {'翠峦': 'cuiluan', '乌马河': 'wumahe', '新青': 'xinqing', '红星': 'hongxing', '美溪': 'meixi', '上甘岭': 'shangganling', '五营': 'wuying', '金山屯': 'jinshantun', '汤旺河': 'tangwanghe', '友好': 'youhao', '嘉荫': 'jiayin', '南岔': 'nancha', '铁力': 'tieli', '西林': 'xilin', '带岭': 'dailing', '乌伊岭': 'wuyiling', '伊春区': 'yichun'}, 'code': 'hljyichun'}, '荆州': {'sublist': {'洪湖': 'honghu', '石首': 'shishou', '公安': 'gongan', '松滋': 'songzi', '沙市': 'shashi', '荆州区': 'jingzhou', '监利': 'jianli', '江陵': 'jiangling'}, 'code': 'jingzhou'}, '杭州': {'sublist': {'富阳': 'fuyang', '临安': 'linan', '建德': 'jiande', '江干': 'jianggan', '拱墅': 'gongshu', '上城': 'shangcheng', '桐庐': 'tonglu', '淳安': 'chunan', '杭州周边': 'hangzhouzhoubian', '下城': 'xiacheng', '萧山': 'xiaoshan', '滨江': 'binjiang', '西湖': 'xihu', '余杭': 'yuhang'}, 'code': 'hz'}, '贺州': {'sublist': {'八步': 'babu', '钟山': 'zhongshan', '富川': 'fuchuan', '昭平': 'zhaoping'}, 'code': 'hezhou'}, '黔西南': {'sublist': {'兴仁': 'xingren', '兴义': 'xingyi', '贞丰': 'zhenfeng', '册亨': 'ceheng', '望谟': 'wangmo', '安龙': 'anlong', '普安': 'puan', '晴隆': 'qinglong'}, 'code': 'qianxinan'}, '攀枝花': {'sublist': {'西区': 'xiqu', '米易': 'miyi', '仁和': 'renhe', '东区': 'dongqu', '盐边': 'yanbian'}, 'code': 'panzhihua'}, '肇庆': {'sublist': {'广宁': 'guangning', '鼎湖': 'dinghu', '端州': 'duanzhou', '高要': 'gaoyao', '四会': 'sihui', '德庆': 'deqing', '封开': 'fengkai', '怀集': 'huaiji'}, 'code': 'zhaoqing'}, '塔城': {'sublist': {'塔城市': 'tacheng', '裕民': 'yumin', '乌苏': 'wusu', '额敏': 'emin', '和布克赛尔': 'hebukesaier', '沙湾': 'shawan', '托里': 'tuoli'}, 'code': 'tacheng'}, '长春': {'sublist': {'九台': 'jiutai', '绿园': 'lvyuan', '宽城': 'kuancheng', '经开': 'jingkai', '德惠': 'dehui', '双阳': 'shuangyang', '南关': 'nanguan', '汽车城': 'qichecheng', '其他': 'qita', '农安': 'nongan', '二道': 'erdao', '高新': 'gaoxin', '朝阳': 'chaoyang', '榆树': 'yushu', '净月': 'jingyue'}, 'code': 'cc'}, '蚌埠': {'sublist': {'五河': 'wuhe', '禹会': 'yuhui', '怀远': 'huaiyuan', '龙子湖': 'longzihu', '固镇': 'guzhen', '蚌山': 'bengshan', '淮上': 'huaishang'}, 'code': 'bengbu'}, '汕头': {'sublist': {'潮阳': 'chaoyang', '金平': 'jinping', '龙湖': 'longhu', '濠江': 'haojiang', '澄海': 'chenghai', '潮南': 'chaonan', '南澳': 'nanao'}, 'code': 'shantou'}, '来宾': {'sublist': {'象州': 'xiangzhou', '忻城': 'xincheng', '金秀': 'jinxiu', '武宣': 'wuxuan', '兴宾': 'xingbin', '合山': 'heshan'}, 'code': 'laibin'}, '厦门': {'sublist': {'同安': 'tongan', '杏林': 'xinglin', '厦门周边': 'shamenzhoubian', '集美': 'jimei', '翔安': 'xiangan', '湖里': 'huli', '海沧': 'haicang', '思明': 'siming'}, 'code': 'xm'}, '曲靖': {'sublist': {'罗平': 'luoping', '师宗': 'shizong', '宣威': 'xuanwei', '会泽': 'huize', '沾益': 'zhayi', '陆良': 'luliang', '麒麟': 'qilin', '富源': 'fuyuan', '马龙': 'malong'}, 'code': 'qujing'}, '芜湖': {'sublist': {'无为': 'wuwei', '芜湖县': 'wuhuxian', '三山': 'sanshan', '弋江': 'yijiang', '鸠江': 'jiujiang', '繁昌': 'fanchang', '镜湖': 'jinghu', '南陵': 'nanling'}, 'code': 'wuhu'}, '泰州': {'sublist': {'兴化': 'xinghua', '姜堰': 'jiangyan', '海陵': 'hailing', '靖江': 'jingjiang', '泰兴': 'taixing', '高港': 'gaogang'}, 'code': 'jstaizhou'}, '江门': {'sublist': {'台山': 'taishan', '江海': 'jianghai', '开平': 'kaiping', '蓬江': 'pengjiang', '鹤山': 'heshan', '恩平': 'enping', '新会': 'xinhui'}, 'code': 'jiangmen'}, '苏州': {'sublist': {'太仓': 'taicang', '常熟': 'changshu', '昆山': 'kunshan', '相城': 'xiangcheng', '新区': 'xinqu', '吴江': 'wujiang', '园区': 'yuanqu', '张家港': 'zhangjiagang', '平江': 'pingjiang', '金阊': 'jinchang', '沧浪': 'canglang', '吴中': 'wuzhong'}, 'code': 'su'}, '郴州': {'sublist': {'宜章': 'yizhang', '北湖': 'beihu', '临武': 'linwu', '苏仙': 'suxian', '桂东': 'guidong', '汝城': 'rucheng', '桂阳': 'guiyang', '永兴': 'yongxing', '嘉禾': 'jiahe', '安仁': 'anren', '资兴': 'zixing'}, 'code': 'chenzhou'}, '钦州': {'sublist': {'灵山': 'lingshan', '浦北': 'pubei', '钦南': 'qinnan', '钦北': 'qinbei'}, 'code': 'qinzhou'}, '鹤岗': {'sublist': {'南山': 'nanshan', '兴山': 'xingshan', '兴安': 'xingan', '萝北': 'luobei', '东山': 'dongshan', '工农': 'gongnong', '绥滨': 'suibin', '向阳': 'xiangyang'}, 'code': 'hegang'}, '阿坝': {'sublist': {'汶川': 'wenchuan', '金川': 'jinchuan', '理县': 'lixian', '黑水': 'heishui', '小金': 'xiaojin', '壤塘': 'rangtang', '若尔盖': 'ruoergai', '马尔康': 'maerkang', '茂县': 'maoxian', '阿坝县': 'aba', '松潘': 'songpan', '红原': 'hongyuan', '九寨沟': 'jiuzhaigou'}, 'code': 'aba'}, '三明': {'sublist': {'梅列': 'meilie', '将乐': 'jiangle', '清流': 'qingliu', '永安': 'yongan', '大田': 'datian', '尤溪': 'youxi', '明溪': 'mingxi', '泰宁': 'taining', '三元': 'sanyuan', '宁化': 'ninghua', '建宁': 'jianning', '沙县': 'shaxian'}, 'code': 'sanming'}, '通化': {'sublist': {'东昌区': 'dongchangqu', '集安': 'jian', '通化县': 'tonghuaxian', '柳河': 'liuhe', '梅河口': 'meihekou', '二道江区': 'erdaojiangqu', '辉南': 'huinan'}, 'code': 'tonghua'}, '南平': {'sublist': {'政和': 'zhenghe', '松溪': 'songxi', '武夷山': 'wuyishan', '邵武': 'shaowu', '建阳': 'jianyang', '建瓯': 'jianou', '光泽': 'guangze', '延平': 'yanping', '顺昌': 'shunchang', '浦城': 'pucheng'}, 'code': 'nanping'}, '玉树': {'sublist': {'囊谦': 'nangqian', '杂多': 'zaduo', '曲麻莱': 'qumalai', '称多': 'chengduo', '玉树县': 'yushuxian', '治多': 'zhiduo'}, 'code': 'yushu'}, '阿里': {'sublist': {'札达': 'zhada', '日土': 'ritu', '革吉': 'geji', '噶尔': 'gaer', '改则': 'gaize', '措勤': 'cuoqin', '普兰': 'pulan'}, 'code': 'ali'}, '资阳': {'sublist': {'安岳': 'anyue', '雁江': 'yanjiang', '简阳': 'jianyang', '乐至': 'lezhi'}, 'code': 'ziyang'}, '齐齐哈尔': {'sublist': {'梅里斯': 'meilisi', '依安': 'yian', '富裕': 'fuyu', '龙江': 'longjiang', '拜泉': 'baiquan', '建华': 'jianhua', '克东': 'kedong', '碾子山': 'nianzishan', '讷河': 'nehe', '克山': 'keshan', '龙沙': 'longsha', '铁锋': 'tiefeng', '昂昂溪': 'angangxi', '泰来': 'tailai', '甘南': 'gannan', '富拉尔基': 'fulaerji'}, 'code': 'qiqihaer'}, '自贡': {'sublist': {'荣县': 'rongxian', '富顺': 'fushun', '大安': 'daan', '自流井': 'ziliujing', '沿滩': 'yantan', '贡井': 'gongjing'}, 'code': 'zigong'}, '柳州': {'sublist': {'柳南': 'liunan', '鱼峰': 'yufeng', '三江': 'sanjiang', '融安': 'rongan', '融水': 'rongshui', '柳江': 'liujiang', '柳城': 'liucheng', '鹿寨': 'luzhai', '城中': 'chengzhong', '柳北': 'liubei'}, 'code': 'liuzhou'}, '日照': {'sublist': {'山海天旅游度假区': 'shanhaitianluyoudujiaqu', '五莲': 'wulian', '莒县': 'juxian', '岚山': 'lanshan', '新市区': 'xinshiqu', '高新区': 'gaoxinqu', '开发区': 'kaifaqu', '石臼': 'shijiu', '东港': 'donggang'}, 'code': 'rizhao'}, '巴彦淖尔': {'sublist': {'磴口': 'dengkou', '乌拉特前': 'wulateqian', '杭锦后': 'hangjinhou', '乌拉特后': 'wulatehou', '乌拉特中': 'wulatezhong', '临河': 'linhe', '五原': 'wuyuan'}, 'code': 'bayannaoer'}, '鹤壁': {'sublist': {'山城': 'shancheng', '淇滨': 'qibin', '鹤山': 'heshan', '淇县': 'qixian', '浚县': 'junxian'}, 'code': 'hebi'}, '通辽': {'sublist': {'科尔沁左翼后': 'keerqinzuoyihou', '奈曼': 'naiman', '科尔沁': 'keerqin', '霍林郭勒': 'huolinguoleshi', '科尔沁左翼中': 'keerqinzuoyizhong', '扎鲁特': 'zhalute', '库伦': 'kulun', '开鲁': 'kailu'}, 'code': 'tongliao'}, '黔南': {'sublist': {'荔波': 'libo', '三都': 'sandou', '独山': 'dushan', '龙里': 'longli', '平塘': 'pingtang', '都匀': 'douyun', '罗甸': 'luodian', '贵定': 'guiding', '惠水': 'huishui', '瓮安': 'wengan', '长顺': 'changshun', '福泉': 'fuquan'}, 'code': 'qiannan'}, '张家口': {'sublist': {'赤城': 'chicheng', '怀来': 'huailai', '蔚县': 'weixian', '阳原': 'yangyuan', '宣化': 'xuanhua', '康保': 'kangbao', '万全': 'wanquan', '桥西区': 'qiaoxi', '桥东区': 'qiaodong', '张北': 'zhangbei', '怀安': 'huaian', '宣化区': 'xuanhuaqu', '尚义': 'shangyi', '涿鹿': 'zhuolu', '高新区': 'gaoxin', '崇礼': 'chongli', '下花园区': 'xiahuayuan', '沽源': 'guyuan'}, 'code': 'zhangjiakou'}, '淮北': {'sublist': {'濉溪': 'suixi', '相山': 'xiangshan', '烈山': 'lieshan', '杜集': 'duji'}, 'code': 'huaibei'}, '邯郸': {'sublist': {'高开区': 'gaokaiqu', '魏县': 'weixian', '峰峰矿区': 'fengfengkuang', '肥乡': 'feixiang', '复兴区': 'fuxing', '成安': 'chengan', '大名': 'daming', '曲周': 'quzhou', '涉县': 'shexian', '邯山区': 'hanshan', '邱县': 'qiuxian', '丛台区': 'congtai', '磁县': 'cixian', '临漳': 'linzhang', '鸡泽': 'jize', '永年': 'yongnian', '武安区': 'wuan', '馆陶': 'guantao', '广平': 'guangping', '邯郸县': 'handanxian'}, 'code': 'handan'}, '青岛': {'sublist': {'黄岛': 'huangdao', '市南': 'shinan', '青岛周边': 'qingdaozhoubian', '李沧': 'licang', '市北': 'shibei', '即墨': 'jimo', '崂山': 'laoshan', '胶州': 'jiaozhou', '莱西': 'laixi', '四方': 'sifang', '城阳': 'chengyang', '平度': 'pingdu', '胶南': 'jiaonan'}, 'code': 'qd'}, '本溪': {'sublist': {'平山': 'pingshan', '溪湖': 'xihu', '明山': 'mingshan', '南芬': 'nanfen', '桓仁': 'huanren', '本溪县': 'benxi'}, 'code': 'benxi'}, '汕尾': {'sublist': {'陆河': 'luhe', '城区': 'chengqu', '海丰': 'haifeng', '陆丰': 'lufeng'}, 'code': 'shanwei'}, '武汉': {'sublist': {'武昌': 'wuchang', '青山': 'qingshan', '汉南': 'hannan', '江岸': 'jiangan', '蔡甸': 'caidian', '新洲': 'xinzhou', '东西湖': 'dongxihu', '江夏': 'jiangxia', '江汉': 'jianghan', '沌口开发区': 'jingjijishukaifaqu', '硚口': 'qiaokou', '洪山': 'hongshan', '汉阳': 'hanyang', '黄陂': 'huangbei'}, 'code': 'wh'}, '西安': {'sublist': {'高陵': 'gaoling', '新城': 'xincheng', '浐灞': 'chanba', '沣渭新区': 'fengweixinqu', '户县': 'huxian', '长安': 'changan', '临潼': 'lintong', '未央': 'weiyang', '泾渭新区': 'jingweixinqu', '碑林': 'beilin', '莲湖': 'lianhu', '蓝田': 'lantian', '其他': 'qita', '阎良': 'yanliang', '高新': 'gaoxin', '雁塔': 'yanta', '周至': 'zhouzhi', '灞桥': 'baqiao', '曲江新区': 'qujiangxinqu'}, 'code': 'xa'}, '汉中': {'sublist': {'略阳': 'lueyang', '宁强': 'ningqiang', '佛坪': 'foping', '洋县': 'yangxian', '城固': 'chenggu', '勉县': 'mianxian', '汉台': 'hantai', '南郑': 'nanzheng', '西乡': 'xixiang', '留坝': 'liuba', '镇巴': 'zhenba'}, 'code': 'hanzhong'}, '宜春': {'sublist': {'铜鼓': 'tonggu', '宜丰': 'yifeng', '靖安': 'jingan', '上高': 'shanggao', '奉新': 'fengxin', '高安': 'gaoan', '樟树': 'zhangshu', '丰城': 'fengcheng', '袁州': 'yuanzhou', '万载': 'wanzai'}, 'code': 'jxyichun'}, '甘孜': {'sublist': {'白玉': 'baiyu', '丹巴': 'danba', '稻城': 'daocheng', '泸定': 'luding', '乡城': 'xiangcheng', '雅江': 'yajiang', '石渠': 'shiqu', '色达': 'seda', '得荣': 'derong', '甘孜县': 'ganzi', '道孚': 'daofu', '九龙': 'jiulong', '理塘': 'litang', '新龙': 'xinlong', '康定': 'kangding', '德格': 'dege', '炉霍': 'luhuo', '巴塘': 'batang'}, 'code': 'ganzi'}, '乌兰察布': {'sublist': {'察哈尔右翼前': 'chahaeryouyiqian', '察哈尔右翼后': 'chahaeryouyihou', '集宁': 'jining', '卓资': 'zhuozi', '四子王': 'siziwang', '丰镇': 'fengzhenshi', '察哈尔右翼中': 'chahaeryouyizhong', '商都': 'shangdou', '兴和': 'xinghe', '凉城': 'liangcheng', '化德': 'huade'}, 'code': 'wulanchabu'}, '平凉': {'sublist': {'华亭': 'huating', '灵台': 'lingtai', '静宁': 'jingning', '泾川': 'jingchuan', '崆峒': 'kongtong', '庄浪': 'zhuanglang', '崇信': 'chongxin'}, 'code': 'pingliang'}, '吐鲁番': {'sublist': {'鄯善': 'shanshan', '托克逊': 'tuokexun', '吐鲁番市': 'tulufan'}, 'code': 'tulufan'}, '海西': {'sublist': {'大柴旦行委': 'dachaidanhangwei', '格尔木': 'geermu', '德令哈': 'delingha', '冷湖行委': 'lenghuhangwei', '都兰': 'doulan', '茫崖行委': 'mangyahangwei', '天峻': 'tianjun', '乌兰': 'wulan'}, 'code': 'haixi'}, '西双版纳': {'sublist': {'景洪': 'jinghong', '勐腊': 'mengla', '勐海': 'menghai'}, 'code': 'xishuangbanna'}, '南宁': {'sublist': {'青秀': 'qingxiu', '江南': 'jiangnan', '武鸣': 'wuming', '横县': 'hengxian', '隆安': 'longan', '西乡塘': 'xixiangtang', '邕宁': 'yongning', '良庆': 'liangqing', '宾阳': 'binyang', '兴宁': 'xingning', '马山': 'mashan', '其他': 'qita', '上林': 'shanglin'}, 'code': 'nn'}, '金昌': {'sublist': {'金川': 'jinchuan', '永昌': 'yongchang'}, 'code': 'jinchang'}, '喀什': {'sublist': {'麦盖提': 'maigaiti', '喀什市': 'kashi', '疏附': 'shufu', '巴楚': 'bachu', '莎车': 'shache', '英吉沙': 'yingjisha', '岳普湖': 'yuepuhu', '塔什库尔': 'tashikuer', '叶城': 'yecheng', '疏勒': 'shule', '伽师': 'jiashi', '泽普': 'zepu'}, 'code': 'kashi'}, '延安': {'sublist': {'安塞': 'ansai', '洛川': 'luochuan', '黄陵': 'huangling', '宝塔': 'baota', '延川': 'yanchuan', '吴起': 'wuqi', '志丹': 'zhidan', '延长': 'yanchang', '宜川': 'yichuan', '黄龙': 'huanglong', '富县': 'fuxian', '甘泉': 'ganquan', '子长': 'zizhang'}, 'code': 'yanan'}, '新余': {'sublist': {'渝水': 'yushui', '分宜': 'fenyi'}, 'code': 'xinyu'}, '锦州': {'sublist': {'黑山': 'heishan', '北宁': 'beining', '经开区': 'jingkai', '松山新区': 'songshanxinqu', '太和': 'taihe', '义县': 'yixian', '凌海': 'linghai', '凌河': 'linghe', '古塔': 'guta'}, 'code': 'jinzhou'}, '丽江': {'sublist': {'古城': 'gucheng', '宁蒗': 'ninglang', '华坪': 'huaping', '玉龙': 'yulong', '永胜': 'yongsheng'}, 'code': 'lijiang'}, '鞍山': {'sublist': {'铁东': 'tiedong', '海城': 'haicheng', '立山': 'lishan', '铁西': 'tiexi', '千山': 'qianshan', '台安': 'taian', '岫岩': 'xiuyan'}, 'code': 'anshan'}, '商丘': {'sublist': {'睢阳': 'suiyang', '宁陵': 'ningling', '夏邑': 'xiayi', '睢县': 'suixian', '梁园': 'liangyuan', '永城': 'yongcheng', '柘城': 'zhecheng', '民权': 'minquan', '虞城': 'yucheng'}, 'code': 'shangqiu'}, '库尔勒': {'sublist': {'若羌': 'ruoqiang', '且末': 'qiemo', '和硕': 'heshuo', '尉犁': 'weili', '和静': 'hejing', '轮台': 'luntai', '博湖': 'bohu', '库尔勒周边': 'kuerlezhoubian', '焉耆': 'yanqi'}, 'code': 'kuerle'}, '临沧': {'sublist': {'沧源': 'cangyuan', '云县': 'yunxian', '耿马': 'gengma', '临翔': 'linxiang', '镇康': 'zhenkang', '双江': 'shuangjiang', '凤庆': 'fengqing', '永德': 'yongde'}, 'code': 'lincang'}, '平顶山': {'sublist': {'鲁山': 'lushan', '舞钢': 'wugang', '石龙': 'shilong', '卫东': 'weidong', '汝州': 'ruzhou', '宝丰': 'baofeng', '郏县': 'jiaxian', '新华': 'xinhua', '湛河': 'zhanhe', '叶县': 'yexian'}, 'code': 'pingdingshan'}, '连云港': {'sublist': {'连云': 'lianyun', '灌南': 'guannan', '海州': 'haizhou', '灌云': 'guanyun', '赣榆': 'ganyu', '东海': 'donghai', '新浦': 'xinpu'}, 'code': 'lianyungang'}, '十堰': {'sublist': {'张湾': 'zhangwan', '丹江口': 'danjiangkou', '竹溪': 'zhuxi', '郧县': 'yunxian', '房县': 'fangxian', '茅箭': 'maojian', '郧西': 'yunxi', '竹山': 'zhushan'}, 'code': 'shiyan'}, '德宏': {'sublist': {'潞西': 'luxi', '瑞丽': 'ruili', '盈江': 'yingjiang', '陇川': 'longchuan', '梁河': 'lianghe'}, 'code': 'dehong'}, '金华': {'sublist': {'兰溪': 'lanxi', '金东': 'jindong', '浦江': 'pujiang', '婺城': 'wucheng', '义乌': 'yiwu', '武义': 'wuyi', '东阳': 'dongyang', '磐安': 'panan', '永康': 'yongkang', '江南': 'jiangnan', '江北': 'jiangbei'}, 'code': 'jinhua'}, '常德': {'sublist': {'武陵': 'wuling', '石门': 'shimen', '澧县': 'lixian', '临澧': 'linli', '桃源': 'taoyuan', '安乡': 'anxiang', '汉寿': 'hanshou', '鼎城': 'dingcheng', '津市': 'jinshi'}, 'code': 'changde'}, '上海': {'sublist': {'嘉定': 'jiading', '青浦': 'qingpu', '徐汇': 'xuhui', '奉贤': 'fengxian', '卢湾': 'luwan', '崇明': 'chongming', '黄浦': 'huangpu', '闸北': 'zhabei', '长宁': 'changning', '静安': 'jingan', '普陀': 'putuo', '松江': 'songjiang', '上海周边': 'shanghaizhoubian', '浦东': 'pudongxinqu', '金山': 'jinshan', '南汇': 'nanhui', '宝山': 'baoshan', '闵行': 'minhang', '杨浦': 'yangpu', '虹口': 'hongkou'}, 'code': 'sh'}, '潍坊': {'sublist': {'坊子': 'fangzi', '安丘': 'anqiu', '昌乐': 'changle', '寿光': 'shouguang', '奎文': 'kuiwen', '高密': 'gaomi', '寒亭': 'hanting', '青州': 'qingzhou', '临朐': 'linqu', '潍城': 'weicheng', '诸城': 'zhucheng', '高新区': 'gaoxinqu', '滨海新区': 'binhaixinqu', '经开区': 'jingkaiqu', '昌邑': 'changyi'}, 'code': 'weifang'}, '武威': {'sublist': {'凉州': 'liangzhou', '民勤': 'minqin', '天祝': 'tianzhu', '古浪': 'gulang'}, 'code': 'wuwei'}, '黄南': {'sublist': {'泽库': 'zeku', '河南': 'henan', '同仁': 'tongren', '尖扎': 'jianzha'}, 'code': 'huangnan'}, '贵阳': {'sublist': {'乌当': 'wudang', '修文': 'xiuwen', '息烽': 'xifeng', '清镇': 'qingzhen', '小河': 'xiaohe', '云岩': 'yunyan', '白云': 'baiyun', '开阳': 'kaiyang', '金阳新区': 'jinyangxin', '南明': 'nanming', '小河片': 'xiaohepian', '花溪': 'huaxi'}, 'code': 'gy'}, '上饶': {'sublist': {'德兴': 'dexing', '广丰': 'guangfeng', '铅山': 'qianshan', '婺源': 'wuyuan', '玉山': 'yushan', '信州': 'xinzhou', '上饶县': 'shangrao', '弋阳': 'yiyang', '鄱阳': 'poyang', '万年': 'wannian', '余干': 'yugan', '横峰': 'hengfeng'}, 'code': 'shangrao'}, '毕节': {'sublist': {'金沙': 'jinsha', '毕节市': 'bijie', '纳雍': 'nayong', '七星关': 'qixingguan', '大方': 'dafang', '赫章': 'hezhang', '织金': 'zhijin', '威宁': 'weining', '黔西': 'qianxi'}, 'code': 'bijie'}, '岳阳': {'sublist': {'岳阳楼': 'yueyanglou', '临湘': 'linxiang', '平江': 'pingjiang', '君山': 'junshan', '云溪': 'yunxi', '湘阴': 'xiangyin', '岳阳县': 'yueyangxian', '汨罗': 'miluo', '华容': 'huarong'}, 'code': 'yueyang'}, '云浮': {'sublist': {'罗定': 'luoding', '郁南': 'yvnan', '新兴': 'xinxing', '云城': 'yuncheng', '云安': 'yunan'}, 'code': 'yunfu'}, '庆阳': {'sublist': {'合水': 'heshui', '环县': 'huanxian', '华池': 'huachi', '镇原': 'zhenyuan', '西峰': 'xifeng', '正宁': 'zhengning', '庆城': 'qingcheng', '宁县': 'ningxian'}, 'code': 'qingyang'}, '镇江': {'sublist': {'润州': 'runzhou', '丹阳': 'danyang', '京口': 'jingkou', '镇江新区': 'zhenjiangxinqu', '句容': 'jurong', '扬中': 'yangzhong', '丹徒': 'dantu'}, 'code': 'zhenjiang'}, '滁州': {'sublist': {'来安': 'laian', '明光': 'mingguang', '天长': 'tianzhang', '南谯': 'nanqiao', '全椒': 'quanjiao', '凤阳': 'fengyang', '定远': 'dingyuan', '琅琊': 'langya'}, 'code': 'chuzhou'}, '茂名': {'sublist': {'信宜': 'xinyi', '电白': 'dianbai', '化州': 'huazhou', '高州': 'gaozhou', '茂港': 'maogang', '茂南': 'maonan'}, 'code': 'maoming'}, '盐城': {'sublist': {'大丰': 'dafeng', '阜宁': 'funing', '响水': 'xiangshui', '东台': 'dongtai', '盐都': 'yandou', '建湖': 'jianhu', '亭湖': 'tinghu', '滨海': 'binhai', '射阳': 'sheyang'}, 'code': 'yancheng'}, '永州': {'sublist': {'新田': 'xintian', '冷水滩': 'lengshuitan', '祁阳': 'qiyang', '江华': 'jianghua', '双牌': 'shuangpai', '道县': 'daoxian', '江永': 'jiangyong', '东安': 'dongan', '蓝山': 'lanshan', '宁远': 'ningyuan', '零陵': 'lingling'}, 'code': 'yongzhou'}, '吉林': {'sublist': {'昌邑区': 'changyiqu', '舒兰': 'shulan', '桦甸': 'huadian', '永吉': 'yongji', '船营区': 'chuanyingqu', '丰满区': 'fengmanqu', '高新区': 'gaoxinqu', '经开区': 'jingkaiqu', '蛟河': 'jiaohe', '磐石': 'panshi', '龙潭区': 'longtanqu'}, 'code': 'jilin'}, '甘南': {'sublist': {'舟曲': 'zhouqu', '卓尼': 'zhuoni', '合作': 'hezuo', '夏河': 'xiahe', '碌曲': 'luqu', '临潭': 'lintan', '迭部': 'diebu', '玛曲': 'maqu'}, 'code': 'gannan'}, '丹东': {'sublist': {'凤城': 'fengcheng', '宽甸': 'kuandian', '元宝': 'yuanbao', '振兴': 'zhenxing', '振安': 'zhenan', '东港': 'donggang'}, 'code': 'dandong'}, '呼和浩特': {'sublist': {'赛罕': 'saihan', '新城': 'xincheng', '土默特左': 'tumotezuo', '武川': 'wuchuan', '和林格尔': 'helingeer', '玉泉': 'yuquan', '金桥开发区': 'jinqiaokaifaqu', '托克托': 'tuoketuo', '清水河': 'qingshuihe', '金川开发区': 'jinchuankaifaqu', '如意开发区': 'ruyikaifaqu', '回民': 'huimin', '金山开发区': 'jinshankaifaqu'}, 'code': 'nmg'}, '商洛': {'sublist': {'商南': 'shangnan', '商州': 'shangzhou', '镇安': 'zhenan', '山阳': 'shanyang', '丹凤': 'danfeng', '柞水': 'zhashui', '洛南': 'luonan'}, 'code': 'shangluo'}, '北京': {'sublist': {'顺义': 'shunyi', '宣武': 'xuanwu', '东城': 'dongcheng', '燕郊': 'yanjiao', '丰台': 'fengtai', '大兴': 'daxing', '朝阳': 'chaoyang', '北京周边': 'beijingzhoubian', '西城': 'xicheng', '密云': 'miyun', '昌平': 'changping', '房山': 'fangshan', '怀柔': 'huairou', '通州': 'tongzhou', '平谷': 'pinggu', '延庆': 'yanqing', '崇文': 'chongwen', '石景山': 'shijingshan', '海淀': 'haidian', '门头沟': 'mentougou'}, 'code': 'bj'}, '莆田': {'sublist': {'涵江': 'hanjiang', '仙游': 'xianyou', '秀屿': 'xiuyu', '城厢': 'chengxiang', '荔城': 'licheng'}, 'code': 'putian'}, '周口': {'sublist': {'扶沟': 'fugou', '郸城': 'dancheng', '淮阳': 'huaiyang', '项城': 'xiangcheng', '鹿邑': 'luyi', '太康': 'taikang', '商水': 'shangshui', '西华': 'xihua', '沈丘': 'shenqiu', '川汇': 'chuanhui'}, 'code': 'zhoukou'}, '南京': {'sublist': {'浦口': 'pukou', '大厂': 'dachang', '玄武': 'xuanwu', '白下': 'baixia', '六合': 'liuhe', '鼓楼': 'gulou', '高淳': 'gaochun', '下关': 'xiaguan', '秦淮': 'qinhuai', '栖霞': 'qixia', '溧水': 'lishui', '雨花台': 'yuhuatai', '南京周边': 'nanjingzhoubian', '建邺': 'jianye', '江宁': 'jiangning'}, 'code': 'nj'}, '常州': {'sublist': {'武进': 'wujin', '新北': 'xinbei', '金坛': 'jintan', '溧阳': 'liyang', '钟楼': 'zhonglou', '戚墅堰': 'qishuyan', '天宁': 'tianning'}, 'code': 'changzhou'}, '重庆': {'sublist': {'梁平': 'liangping', '黔江': 'qianjiang', '奉节': 'fengjie', '万盛': 'wansheng', '巫溪': 'wuxi', '江津': 'jiangjin', '合川': 'hechuan', '彭水': 'pengshui', '渝北': 'yubei', '巴南': 'banan', '铜梁': 'tongliang', '潼南': 'tongnan', '沙坪坝': 'shapingba', '长寿': 'changshou', '綦江': 'qijiang', '秀山': 'xiushan', '武隆': 'wulong', '璧山': 'bishan', '城口': 'chengkou', '大足': 'dazu', '涪陵': 'fuling', '南岸': 'nanan', '大渡口': 'dadukou', '渝中': 'yuzhong', '忠县': 'zhongxian', '丰都': 'fengdu', '两江新区': 'liangjiangxinqu', '双桥': 'shuangqiao', '南川': 'nanchuan', '万州': 'wanzhou', '北碚': 'beibei', '其他市县': 'qitashixian', '开县': 'kaixian', '巫山': 'wushan', '江北': 'jiangbei', '垫江': 'dianjiang', '云阳': 'yunyang', '酉阳': 'youyang', '石柱': 'shizhu', '永川': 'yongchuan', '荣昌': 'rongchang', '九龙坡': 'jiulongpo'}, 'code': 'cq'}, '鸡西': {'sublist': {'恒山': 'hengshan', '城子河': 'chengzihe', '麻山': 'mashan', '鸡冠': 'jiguan', '虎林': 'hulin', '滴道': 'didao', '鸡东': 'jidong', '梨树': 'lishu', '密山': 'mishan'}, 'code': 'jixi'}, '达州': {'sublist': {'万源': 'wanyuan', '大竹': 'dazhu', '开江': 'kaijiang', '渠县': 'quxian', '达县': 'daxian', '宣汉': 'xuanhan', '通川': 'tongchuan'}, 'code': 'dazhou'}, '成都': {'sublist': {'郫县': 'pixian', '邛崃': 'qionglai', '天府新区': 'tianfuxinqu', '金牛': 'jinniu', '温江': 'wenjiang', '双流': 'shuangliu', '青羊': 'qingyang', '崇州': 'chongzhou', '龙泉驿': 'longquanyi', '武侯': 'wuhou', '金堂': 'jintang', '新津': 'xinjin', '青白江': 'qingbaijiang', '都江堰': 'dujiangyan', '锦江': 'jinjiang', '高新西区': 'gaoxinxiqu', '蒲江': 'pujiang', '成华': 'chenghua', '新都': 'xindu', '彭州': 'pengzhou', '其他': 'qita', '高新': 'gaoxin', '大邑': 'dayi'}, 'code': 'cd'}, '广元': {'sublist': {'朝天': 'chaotian', '旺苍': 'wangcang', '苍溪': 'cangxi', '青川': 'qingchuan', '剑阁': 'jiange', '市中': 'shizhong', '元坝': 'yuanba'}, 'code': 'guangyuan'}, '五家渠': {'sublist': {'102团': '102tuan', '101团': '101tuan', '青湖路街道': 'qinghulujiedao', '军垦路街道': 'junkenlujiedao', '人民路街道': 'renminlujiedao', '五家渠周边': 'wujiaquzhoubian', '103团': '103tuan'}, 'code': 'wujiaqu'}, '衡水': {'sublist': {'武强': 'wuqiang', '景县': 'jingxian', '武邑': 'wuyixian', '故城': 'gucheng', '枣强': 'zaoqiang', '深州': 'shenzhen', '桃城区': 'taocheng', '阜城': 'fucheng', '冀州': 'jizhou', '饶阳': 'raoyang', '开发区': 'kaifaqu', '安平': 'anping'}, 'code': 'hengshui'}, '阳江': {'sublist': {'阳春': 'yangchun', '阳西': 'yangxi', '阳东': 'yangdong', '江城': 'jiangcheng'}, 'code': 'yangjiang'}, '怒江': {'sublist': {'福贡': 'fugong', '泸水': 'lushui', '兰坪': 'lanping', '贡山': 'gongshan'}, 'code': 'nujiang'}, '桂林': {'sublist': {'雁山': 'yanshan', '荔浦': 'lipu', '全州': 'quanzhou', '秀峰': 'xiufeng', '平乐': 'pingle', '永福': 'yongfu', '资源': 'ziyuan', '阳朔': 'yangshuo', '兴安': 'xingan', '七星': 'qixing', '灌阳': 'guanyang', '象山': 'xiangshan', '龙胜': 'longsheng', '恭城': 'gongcheng', '叠彩': 'diecai', '临桂': 'lingui', '灵川': 'lingchuan'}, 'code': 'gl'}, '临汾': {'sublist': {'襄汾': 'xiangfen', '安泽': 'anze', '蒲县': 'puxian', '永和': 'yonghe', '侯马': 'houma', '曲沃': 'quwo', '浮山': 'fushan', '洪洞': 'hongdong', '古县': 'guxian', '大宁': 'daning', '乡宁': 'xiangning', '汾西': 'fenxi', '霍州': 'huozhou', '翼城': 'yicheng', '隰县': 'xixian', '吉县': 'jixian', '尧都': 'yaodou'}, 'code': 'linfen'}, '文山': {'sublist': {'西畴': 'xichou', '砚山': 'yanshan', '富宁': 'funing', '广南': 'guangnan', '文山市': 'wenshan', '丘北': 'qiubei', '马关': 'maguan', '麻栗坡': 'malipo'}, 'code': 'wenshan'}, '六盘水': {'sublist': {'水城': 'shuicheng', '钟山': 'zhongshan', '六枝特区': 'liuzhite', '盘县': 'panxian'}, 'code': 'liupanshui'}, '天水': {'sublist': {'秦城': 'qinzhou', '甘谷': 'gangu', '张家川': 'zhangjiachuan', '清水': 'qingshui', '武山': 'wushan', '北道': 'beidao', '秦安': 'qinan'}, 'code': 'tianshui'}, '洛阳': {'sublist': {'偃师': 'yanshi', '涧西': 'jianxi', '西工': 'xigong', '瀍河': 'chanhe', '汝阳': 'ruyang', '洛宁': 'luoning', '伊川': 'yichuan', '洛龙': 'luolong', '宜阳': 'yiyang', '伊滨': 'yibin', '孟津': 'mengjin', '吉利': 'jili', '新安': 'xinan', '嵩县': 'songxian', '老城': 'laocheng', '栾川': 'luanchuan'}, 'code': 'luoyang'}, '南阳': {'sublist': {'南召': 'nanzhao', '唐河': 'tanghe', '方城': 'fangcheng', '内乡': 'neixiang', '镇平': 'zhenping', '邓州': 'dengzhou', '社旗': 'sheqi', '卧龙': 'wolong', '油田': 'youtian', '西峡': 'xixia', '淅川': 'xichuan', '宛城': 'wancheng', '桐柏': 'tongbai', '新野': 'xinye'}, 'code': 'nanyang'}, '宁德': {'sublist': {'寿宁': 'shouning', '蕉城': 'jiaocheng', '古田': 'gutian', '周宁': 'zhouning', '柘荣': 'zherong', '屏南': 'pingnan', '霞浦': 'xiapu', '福鼎': 'fuding', '福安': 'fuan'}, 'code': 'ningde'}, '玉林': {'sublist': {'陆川': 'luchuan', '博白': 'bobai', '玉州': 'yuzhou', '容县': 'rongxian', '北流': 'beiliu', '兴业': 'xingye'}, 'code': 'gxyulin'}, '临夏': {'sublist': {'永靖': 'yongjing', '临夏市': 'linxia', '广河': 'guanghe', '积石山': 'jishishan', '东乡': 'dongxiang', '康乐': 'kangle', '和政': 'hezheng'}, 'code': 'linxia'}, '大兴安岭': {'sublist': {'新林': 'xinlin', '呼中': 'huzhong', '加格达奇': 'jiagedaqi', '呼玛': 'huma', '漠河': 'mohe', '塔河': 'tahe', '松岭': 'songling'}, 'code': 'daxinganling'}, '双鸭山': {'sublist': {'宝清': 'baoqing', '四方台': 'sifangtai', '友谊': 'youyi', '集贤': 'jixian', '宝山': 'baoshan', '尖山': 'jianshan', '饶河': 'raohe', '岭东': 'lingdong'}, 'code': 'shuangyashan'}, '和田': {'sublist': {'和田县': 'hetianxian', '和田市': 'hetian', '民丰': 'minfeng', '墨玉': 'moyu', '策勒': 'cele', '于田': 'yutian', '洛浦': 'luopu', '皮山': 'pishan'}, 'code': 'hetian'}, '宜昌': {'sublist': {'夷陵': 'yiling', '五峰': 'wufeng', '长阳': 'zhangyang', '东山开发区': 'dongshankaifaqu', '伍家岗': 'wujiagang', '远安': 'yuanan', '点军': 'dianjun', '宜都': 'yidou', '枝江': 'zhijiang', '兴山': 'xingshan', '猇亭': 'xiaoting', '秭归': 'zigui', '当阳': 'dangyang', '西陵': 'xiling'}, 'code': 'yichang'}, '扬州': {'sublist': {'高邮': 'gaoyou', '仪征': 'yizheng', '江都': 'jiangdou', '宝应': 'baoying', '邗江': 'hanjiang', '广陵': 'guangling', '开发区': 'hanjiangqu', '维扬': 'weiyang'}, 'code': 'yangzhou'}, '海北': {'sublist': {'海晏': 'haiyan', '刚察': 'gangcha', '祁连': 'qilian', '门源': 'menyuan'}, 'code': 'haibei'}, '唐山': {'sublist': {'芦台农场': 'lutainongchang', '汉沽农场': 'hangunongchang', '滦南': 'luannan', '滦县': 'luanxian', '迁安': 'qianan', '海港开发区': 'haigangkaifa', '南堡开发区': 'nanpukaifa', '路北区': 'lubei', '曹妃甸': 'caofeidian', '迁西': 'qianxi', '古冶区': 'guye', '唐海': 'tanghai', '玉田': 'yutian', '丰润区': 'fengrun', '路南区': 'lunan', '丰南区': 'fengnan', '高新区': 'gaoxinqu', '乐亭': 'leting', '遵化': 'zunhua', '开平区': 'kaiping'}, 'code': 'tangshan'}, '阳泉': {'sublist': {'矿区': 'kuangqu', '城区': 'chengqu', '平定': 'pingding', '盂县': 'yuxian', '郊区': 'jiaoqu'}, 'code': 'yangquan'}, '亳州': {'sublist': {'涡阳': 'woyang', '蒙城': 'mengcheng', '谯城': 'qiaocheng', '利辛': 'lixin'}, 'code': 'bozhou'}, '温州': {'sublist': {'龙湾': 'longwan', '瑞安': 'ruian', '洞头': 'dongtou', '文成': 'wencheng', '平阳': 'pingyang', '乐清': 'leqing', '泰顺': 'taishun', '永嘉': 'yongjia', '鹿城': 'lucheng', '瓯海': 'ouhai', '苍南': 'cangnan'}, 'code': 'wenzhou'}, '绥化': {'sublist': {'安达': 'anda', '肇东': 'zhaodong', '明水': 'mingshui', '青冈': 'qinggang', '兰西': 'lanxi', '北林': 'beilin', '绥棱': 'suileng', '海伦': 'hailun', '望奎': 'wangkui', '庆安': 'qingan'}, 'code': 'suihua'}, '山南': {'sublist': {'乃东': 'naidong', '洛扎': 'luozha', '措美': 'cuomei', '错那': 'cuona', '琼结': 'qiongjie', '加查': 'jiacha', '曲松': 'qusong', '贡嘎': 'gongga', '扎囊': 'zhanang', '桑日': 'sangri', '浪卡子': 'langkazi', '隆子': 'longzi'}, 'code': 'shannan'}, '合肥': {'sublist': {'经开': 'jingkai', '蜀山': 'shushan', '巢湖': 'chaohu', '肥东': 'feidong', '政务': 'zhengwu', '滨湖': 'binhu', '庐阳': 'luyang', '瑶海': 'yaohai', '肥西': 'feixi', '长丰': 'zhangfeng', '高新': 'gaoxin', '新站': 'xinzhan', '包河': 'baohe'}, 'code': 'hf'}, '娄底': {'sublist': {'涟源': 'lianyuan', '新化': 'xinhua', '双峰': 'shuangfeng', '冷水江': 'lengshuijiang', '娄星': 'louxing'}, 'code': 'loudi'}, '北海': {'sublist': {'合浦': 'hepu', '海城': 'haicheng', '铁山港': 'tieshangang', '银海': 'yinhai'}, 'code': 'beihai'}, '抚顺': {'sublist': {'望花': 'wanghua', '东洲': 'dongzhou', '新宾': 'xinbin', '抚顺县': 'fushun', '新抚': 'xinfu', '顺城': 'shuncheng', '清原': 'qingyuan'}, 'code': 'fushun'}, '阿勒泰': {'sublist': {'布尔津': 'buerjin', '青河': 'qinghe', '福海': 'fuhai', '吉木乃': 'jimunai', '阿勒泰市': 'aletai', '哈巴河': 'habahe', '富蕴': 'fuyun'}, 'code': 'aletai'}, '安康': {'sublist': {'紫阳': 'ziyang', '汉阴': 'hanyin', '白河': 'baihe', '平利': 'pingli', '宁陕': 'ningshan', '石泉': 'shiquan', '旬阳': 'xunyang', '镇坪': 'zhenping', '岚皋': 'langao', '汉滨': 'hanbin'}, 'code': 'ankang'}, '七台河': {'sublist': {'新兴': 'xinxing', '茄子河': 'qiezihe', '勃利': 'boli', '桃山': 'taoshan'}, 'code': 'qitaihe'}, '秦皇岛': {'sublist': {'青龙': 'qinglong', '海港区': 'haigang', '抚宁': 'funing', '北戴河区': 'beidaihe', '卢龙': 'lulong', '开发区': 'kaifaqu', '昌黎': 'changli', '山海关区': 'shanhaiguan'}, 'code': 'qinhuangdao'}, '石嘴山': {'sublist': {'大武口': 'dawukou', '平罗': 'luoping', '惠农': 'huinong'}, 'code': 'shizuishan'}, '荆门': {'sublist': {'东宝': 'dongbao', '沙洋': 'shayang', '掇刀': 'duodao', '京山': 'jingshan', '钟祥': 'zhongxiang'}, 'code': 'jingmen'}, '保山': {'sublist': {'隆阳': 'longyang', '龙陵': 'longling', '昌宁': 'changning', '施甸': 'shidian', '腾冲': 'tengchong'}, 'code': 'baoshan'}, '包头': {'sublist': {'东河': 'donghe', '白云矿': 'baiyunkuang', '石拐': 'shiguai', '稀土高新区': 'xitugaoxinqu', '土默特右': 'tumoteyou', '固阳': 'guyang', '青山': 'qingshan', '包头周边': 'baotouzhoubian', '昆都仑': 'kundoulun', '滨河新区': 'binhexinqu', '九原': 'jiuyuan', '达茂': 'damao'}, 'code': 'baotou'}, '常熟': {'sublist': {'董浜': 'dongbang', '浜尚湖': 'bangshanghu', '虞山': 'changshuyushan', '辛庄': 'xinzhuang', '支塘': 'zhitang', '其他': 'changshuqita', '沙家': 'shajia', '古里': 'guli', '碧溪': 'bixi', '梅李': 'meili', '海虞': 'haiyu'}, 'code': 'changshu'}, '信阳': {'sublist': {'光山': 'guangshan', '羊山新区': 'yangshanxinqu', '浉河': 'shihe', '罗山': 'luoshan', '潢川': 'huangchuan', '平桥': 'pingqiao', '商城': 'shangcheng', '固始': 'gushi', '淮滨': 'huaibin', '息县': 'xixian', '新县': 'xinxian'}, 'code': 'xinyang'}, '梧州': {'sublist': {'蒙山': 'mengshan', '岑溪': 'cenxi', '万秀': 'wanxiu', '藤县': 'tengxian', '长洲': 'zhangzhou', '蝶山': 'dieshan', '苍梧': 'cangwu'}, 'code': 'wuzhou'}, '巴音郭楞': {'sublist': {'库尔勒': 'kuerle', '且末': 'qiemo', '和硕': 'heshuo', '尉犁': 'weili', '轮台': 'luntai', '若羌': 'ruoqiang', '和静': 'hejing', '博湖': 'bohu', '焉耆': 'yanqi'}, 'code': 'bayinguoleng'}, '白银': {'sublist': {'平川': 'pingchuan', '白银区': 'baiyinqu', '会宁': 'huining', '靖远': 'jingyuan', '景泰': 'jingtai'}, 'code': 'baiyin'}, '福州': {'sublist': {'长乐': 'changle', '罗源': 'luoyuan', '台江': 'taijiang', '连江': 'lianjiang', '福清': 'fuqing', '平潭': 'pingtan', '闽清': 'minqing', '鼓楼': 'gulou', '闽侯': 'minhou', '其他': 'qita', '永泰': 'yongtai', '晋安': 'jinan', '仓山': 'cangshan', '马尾': 'mawei'}, 'code': 'fz'}, '六安': {'sublist': {'裕安': 'yuan', '金安': 'jinan', '舒城': 'shucheng', '金寨': 'jinzhai', '霍邱': 'huoqiu', '寿县': 'shouxian', '霍山': 'huoshan'}, 'code': 'luan'}, '崇左': {'sublist': {'宁明': 'ningming', '龙州': 'longzhou', '大新': 'daxin', '天等': 'tiandeng', '江州': 'jiangzhou', '扶绥': 'fusui', '凭祥': 'pingxiang'}, 'code': 'chongzuo'}, '台州': {'sublist': {'温岭': 'wenling', '天台': 'tiantai', '仙居': 'xianju', '临海': 'linhai', '三门': 'sanmen', '路桥': 'luqiao', '黄岩': 'huangyan', '椒江': 'jiaojiang', '玉环': 'yuhuan'}, 'code': 'zjtaizhou'}, '兰州': {'sublist': {'城关': 'chengguan', '永登': 'yongdeng', '安宁': 'anning', '红古': 'honggu', '皋兰': 'gaolan', '西固': 'xigu', '榆中': 'yuzhong', '七里河': 'qilihe', '新区': 'xinqu'}, 'code': 'lz'}, '眉山': {'sublist': {'青神': 'qingshen', '东坡': 'dongpo', '丹棱': 'danleng', '洪雅': 'hongya', '仁寿': 'renshou', '彭山': 'pengshan'}, 'code': 'meishan'}, '临沂': {'sublist': {'平邑': 'pingyi', '罗庄': 'luozhuang', '郯城': 'tancheng', '沂水': 'yishui', '莒南': 'junan', '苍山': 'cangshan', '河东': 'hedong', '临港': 'lingangqu', '开发区': 'kaifaqu', '兰山': 'lanshan', '临沭': 'linshu', '北城新区': 'beichengxinqu', '高新区': 'gaoxinqu', '费县': 'feixian', '沂南': 'yinan', '蒙阴': 'mengyin'}, 'code': 'linyi'}, '遂宁': {'sublist': {'射洪': 'shehong', '大英': 'daying', '蓬溪': 'pengxi', '安居': 'anju', '船山': 'chuanshan'}, 'code': 'suining'}, '濮阳': {'sublist': {'范县': 'fanxian', '台前': 'taiqian', '南乐': 'nanle', '濮阳县': 'puyang', '华龙': 'hualong', '高新': 'gaoxin', '清丰': 'qingfeng'}, 'code': 'puyang'}, '湛江': {'sublist': {'坡头': 'potou', '雷州': 'leizhou', '吴川': 'wuchuan', '赤坎': 'chikan', '遂溪': 'suixi', '廉江': 'lianjiang', '徐闻': 'xuwen', '开发区': 'kaifaqu', '霞山': 'xiashan', '麻章': 'mazhang'}, 'code': 'zhanjiang'}, '铁岭': {'sublist': {'西丰': 'xifeng', '铁岭县': 'tieling', '昌图': 'changtu', '开原': 'kaiyuan', '清河': 'qinghe', '银州': 'yinzhou', '调兵山': 'diaobingshan'}, 'code': 'tieling'}, '义乌': {'sublist': {'廿三里': 'niansanli', '城西': 'chengxi', '江东街道': 'jiangdongjiedao', '稠江街道': 'choujiangjiedao', '其他': 'yiwuqita', '稠城街道': 'chouchengjiedao', '义乌周边': 'yiwuzhoubian', '后宅街道': 'houzhaijiedao', '北苑街道': 'beiyuanjiedao'}, 'code': 'yiwu'}, '新乡': {'sublist': {'凤泉': 'fengquan', '封丘': 'fengqiu', '长垣': 'changyuan', '获嘉': 'huojia', '延津': 'yanjin', '红旗': 'hongqi', '辉县': 'huixian', '原阳': 'yuanyang', '新乡县': 'xinxiang', '牧野': 'muye', '卫辉': 'weihui', '卫滨': 'weibin'}, 'code': 'xinxiang'}, '鹰潭': {'sublist': {'月湖': 'yuehu', '余江': 'yujiang', '贵溪': 'guixi'}, 'code': 'yingtan'}, '湘潭': {'sublist': {'九华经济开发区': 'jiuhuajingjikaifaqu', '湘乡': 'xiangxiang', '岳塘': 'yuetang', '湘潭周边': 'xiangtanzhoubian', '雨湖': 'yuhu', '韶山': 'shaoshan', '湘潭县': 'xiangtan'}, 'code': 'xiangtan'}, '西宁': {'sublist': {'城西': 'chengxi', '大通自治县': 'datongzizhixian', '生物园区': 'shengwuyuanqu', '城东': 'chengdong', '湟中': 'huangzhong', '城北': 'chengbei', '海湖新区': 'haihuxinqu', '湟源': 'huangyuan', '城中': 'chengzhong', '城南新区': 'chengnanxinqu'}, 'code': 'xn'}, '遵义': {'sublist': {'仁怀': 'renhuai', '道真': 'daozhen', '绥阳': 'suiyang', '凤冈': 'fenggang', '正安': 'zhengan', '汇川': 'huichuan', '务川': 'wuchuan', '遵义县': 'zunyixian', '余庆': 'yuqing', '习水': 'xishui', '湄潭': 'meitan', '桐梓': 'tongzi', '红花岗': 'honghuagang', '赤水': 'chishui'}, 'code': 'zunyi'}, '郫县': {'sublist': {'古城': 'guchenghezuo', '三道堰': 'sandaoyan', '唐元': 'tangyuan', '犀浦': 'xipu', '红光': 'hongguang', '花园': 'pixianhuayuan', '唐昌': 'tangchang', '新民场': 'xinminchang', '德源': 'deyuan', '安靖': 'anjing', '安德': 'ande', '郫筒': 'pitong', '友爱': 'youai', '其他': 'pixianqita', '团结': 'tuanjie'}, 'code': 'pixian'}, '承德': {'sublist': {'双桥区': 'shuangqiao', '鹰手营子': 'yingshouyingzi', '双滦区': 'shuangluan', '兴隆': 'xinglong', '开发区': 'kaifaqu', '宽城': 'kuancheng', '隆化': 'longhua', '平泉': 'pingquan', '承德县': 'chengdexian', '围场': 'weichang', '丰宁': 'fengning', '滦平': 'luanping'}, 'code': 'chengde'}, '许昌': {'sublist': {'长葛': 'zhangge', '鄢陵': 'yanling', '襄城': 'xiangcheng', '魏都': 'weidou', '许昌县': 'xuchang', '禹州': 'yuzhou'}, 'code': 'xuchang'}, '韶关': {'sublist': {'武江': 'wujiang', '南雄': 'nanxiong', '仁化': 'renhua', '曲江': 'qujiang', '乐昌': 'lechang', '翁源': 'wengyuan', '浈江': 'zhenjiang', '新丰': 'xinfeng', '乳源': 'ruyuan', '始兴': 'shixing'}, 'code': 'shaoguan'}, '抚州': {'sublist': {'南丰': 'nanfeng', '广昌': 'guangchang', '南城': 'nancheng', '黎川': 'lichuan', '崇仁': 'chongren', '资溪': 'zixi', '东乡': 'dongxiang', '宜黄': 'yihuang', '乐安': 'lean', '临川': 'linchuan', '金溪': 'jinxi'}, 'code': 'jxfuzhou'}, '南通': {'sublist': {'如东': 'rudong', '崇川': 'chongchuan', '海门': 'haimen', '通州': 'tongzhou', '如皋': 'rugao', '港闸': 'gangzha', '开发区': 'kaifaqu', '海安': 'haian', '启东': 'qidong'}, 'code': 'nantong'}, '赤峰': {'sublist': {'巴林左': 'balinzuo', '新城': 'xincheng', '林西': 'linxi', '元宝山': 'yuanbaoshan', '克什克腾': 'keshinketeng', '宁城': 'ningcheng', '敖汉': 'aohan', '巴林右': 'balinyou', '喀喇沁': 'kalaqin', '松山': 'songshan', '红山': 'hongshan', '翁牛特': 'wengniute', '阿鲁科尔沁': 'alukeerqin'}, 'code': 'chifeng'}, '萍乡': {'sublist': {'湘东': 'xiangdong', '芦溪': 'luxi', '安源': 'anyuan', '上栗': 'shangli', '莲花': 'lianhua'}, 'code': 'pingxiang'}, '咸宁': {'sublist': {'嘉鱼': 'jiayu', '咸安': 'xianan', '通山': 'tongshan', '通城': 'tongcheng', '赤壁': 'chibi', '崇阳': 'chongyang'}, 'code': 'xianning'}, '清远': {'sublist': {'连山': 'lianshan', '连南': 'liannan', '阳山': 'yangshan', '清新': 'qingxin', '英德': 'yingde', '清城': 'qingcheng', '佛冈': 'fogang', '连州': 'lianzhou'}, 'code': 'qingyuan'}, '长沙': {'sublist': {'星沙': 'shaxing', '天心': 'tianxin', '望城': 'wangcheng', '浏阳': 'liuyang', '长沙县': 'changshaxian', '岳麓': 'yuelu', '宁乡': 'ningxiang', '芙蓉': 'furong', '雨花': 'yuhua', '其他': 'qita', '开福': 'kaifu'}, 'code': 'cs'}, '安阳': {'sublist': {'文峰': 'wenfeng', '安阳县': 'anyang', '滑县': 'huaxian', '北关': 'beiguan', '殷都': 'yindou', '林州': 'linzhou', '内黄': 'neihuang', '汤阴': 'tangyin', '龙安': 'longan'}, 'code': 'anyang'}, '海南州': {'sublist': {'同德': 'tongde', '贵南': 'guinan', '贵德': 'guide', '共和': 'gonghe', '兴海': 'xinghai'}, 'code': 'hainanzhou'}, '百色': {'sublist': {'那坡': 'napo', '德保': 'debao', '田林': 'tianlin', '隆林': 'longlin', '凌云': 'lingyun', '乐业': 'leye', '靖西': 'jingxi', '田东': 'tiandong', '田阳': 'tianyang', '西林': 'xilin', '平果': 'pingguo', '右江': 'youjiang'}, 'code': 'baise'}, '随州': {'sublist': {'广水': 'guangshui', '曾都': 'cengdou'}, 'code': 'suizhou'}, '佛山': {'sublist': {'高明': 'gaoming', '禅城': 'chancheng', '南海': 'nanhai', '三水': 'sanshui', '顺德': 'shunde'}, 'code': 'foshan'}, '嘉峪关': {'sublist': {'长城区': 'changcheng', '雄关区': 'xiongguan', '镜铁区': 'jingtie'}, 'code': 'jiayuguan'}, '昭通': {'sublist': {'镇雄': 'zhenxiong', '威信': 'weixin', '鲁甸': 'ludian', '绥江': 'suijiang', '彝良': 'yiliang', '盐津': 'yanjin', '永善': 'yongshan', '巧家': 'qiaojia', '昭阳': 'zhaoyang', '大关': 'daguan', '水富': 'shuifu'}, 'code': 'zhaotong'}, '贵港': {'sublist': {'桂平': 'guiping', '港北': 'gangbei', '平南': 'pingnan', '覃塘': 'tantang', '港南': 'gangnan'}, 'code': 'guigang'}, '池州': {'sublist': {'石台': 'shitai', '贵池': 'guichi', '东至': 'dongzhi', '青阳': 'qingyang'}, 'code': 'chizhou'}, '松原': {'sublist': {'宁江区': 'ningjiangqu', '乾安': 'qianan', '扶余': 'fuyu', '长岭': 'changling', '前郭尔罗斯': 'qianguoerluosi'}, 'code': 'songyuan'}, '晋中': {'sublist': {'昔阳': 'xiyang', '太谷': 'taigu', '祁县': 'qixian', '榆次': 'yuci', '左权': 'zuoquan', '寿阳': 'shouyang', '榆社': 'yushe', '平遥': 'pingyao', '和顺': 'heshun', '介休': 'jiexiu', '灵石': 'lingshi'}, 'code': 'jinzhong'}, '漯河': {'sublist': {'召陵': 'zhaoling', '临颍': 'linying', '郾城': 'yancheng', '舞阳': 'wuyang', '源汇': 'yuanhui'}, 'code': 'luohe'}, '阿克苏': {'sublist': {'柯坪': 'keping', '沙雅': 'shaya', '拜城': 'baicheng', '库车': 'kuche', '温宿': 'wensu', '阿瓦提': 'awati', '新和': 'xinhe', '乌什': 'wushen', '阿克苏市': 'akesu'}, 'code': 'akesu'}, '衢州': {'sublist': {'衢江': 'qujiang', '柯城': 'kecheng', '江山': 'jiangshan', '常山': 'changshan', '开化': 'kaihua', '龙游': 'longyou'}, 'code': 'quzhou'}, '广安': {'sublist': {'华蓥': 'huaying', '广安区': 'guangan', '岳池': 'yuechi', '武胜': 'wusheng', '广安城南': 'guanganchengnan', '广安城北': 'guanganchengbei', '邻水': 'linshui'}, 'code': 'guangan'}, '长治': {'sublist': {'沁源': 'qinyuan', '屯留': 'tunliu', '襄垣': 'xiangyuan', '平顺': 'pingshun', '城区': 'chengqu', '潞城': 'lucheng', '武乡': 'wuxiang', '长子': 'changzi', '长治县': 'zhangzhixian', '郊区': 'jiaoqu', '沁县': 'qinxian', '黎城': 'licheng', '壶关': 'huguan'}, 'code': 'changzhi'}, '延边': {'sublist': {'和龙': 'helong', '安图': 'antu', '图们': 'tumen', '敦化': 'dunhua', '延吉': 'yanji', '汪清': 'wangqing', '珲春': 'huichun', '龙井': 'longjing'}, 'code': 'yanbian'}, '楚雄': {'sublist': {'永仁': 'yongren', '元谋': 'yuanmou', '牟定': 'mouding', '南华': 'nanhua', '禄丰': 'lufeng', '双柏': 'shuangbai', '大姚': 'dayao', '武定': 'wuding', '楚雄市': 'chuxiong', '姚安': 'yaoan'}, 'code': 'chuxiong'}, '河源': {'sublist': {'龙川': 'longchuan', '源城': 'yuancheng', '东源': 'dongyuan', '紫金': 'zijin', '连平': 'lianping', '和平': 'heping'}, 'code': 'heyuan'}, '中山': {'sublist': {'小榄': 'xiaolan', '南朗': 'nanlang', '港口': 'gangkou', '横栏': 'henglan', '沙溪': 'shaxi', '神湾': 'shenwan', '火炬': 'huoju', '阜沙': 'fusha', '东凤': 'dongfeng', '西区': 'xiqu', '南区': 'nanqu', '南头': 'nantou', '大涌': 'dayong', '石岐': 'shiqi', '民众': 'minzhong', '东升': 'dongsheng', '黄圃': 'huangpu', '坦洲': 'tanzhou', '古镇': 'guzhen', '板芙': 'banfu', '五桂山': 'wuguishan', '东区': 'dongqu', '三乡': 'sanxiang', '三角': 'sanjiao'}, 'code': 'zhongshan'}, '烟台': {'sublist': {'莱阳': 'laiyang', '蓬莱': 'penglai', '莱州': 'laizhou', '开发区': 'kaifaqu', '莱山': 'laishan', '牟平': 'mouping', '长岛': 'changdao', '栖霞': 'qixia', '福山': 'fushan', '龙口': 'longkou', '高新': 'gaoxin', '芝罘': 'zhifu', '海阳': 'haiyang', '招远': 'zhaoyuan'}, 'code': 'yantai'}, '珠海': {'sublist': {'珠海周边': 'zhuhaizhoubian', '金湾': 'jinwan', '香洲': 'xiangzhou', '斗门': 'doumen'}, 'code': 'zhuhai'}, '衡阳': {'sublist': {'蒸湘': 'zhengxiang', '常宁': 'changning', '衡南': 'hengnan', '石鼓': 'shigu', '衡东': 'hengdong', '衡阳县': 'hengyang', '珠晖': 'zhuhui', '衡山': 'hengshan', '南岳': 'nanyue', '祁东': 'qidong', '耒阳': 'leiyang', '雁峰': 'yanfeng'}, 'code': 'hengyang'}, '孝感': {'sublist': {'孝南': 'xiaonan', '安陆': 'anlu', '大悟': 'dawu', '汉川': 'hanchuan', '云梦': 'yunmeng', '应城': 'yingcheng', '孝昌': 'xiaochang'}, 'code': 'xiaogan'}, '恩施': {'sublist': {'利川': 'lichuan', '宣恩': 'xuanen', '建始': 'jianshi', '鹤峰': 'hefeng', '咸丰': 'xianfeng', '来凤': 'laifeng', '巴东': 'badong', '恩施市': 'enshi'}, 'code': 'enshi'}, '襄阳': {'sublist': {'鱼梁洲': 'yuliangzhou', '谷城': 'gucheng', '宜城': 'yicheng', '南漳': 'nanzhang', '襄城': 'xiangcheng', '老河口': 'laohekou', '保康': 'baokang', '高新区': 'gaoxinqu', '襄州': 'xiangyang', '樊城': 'fancheng', '枣阳': 'zaoyang'}, 'code': 'xiangyang'}, '黄石': {'sublist': {'大冶': 'daye', '阳新': 'yangxin', '黄石港': 'huangshigang', '花湖': 'huahu', '下陆': 'xialu', '西塞山': 'xisaishan', '团城山': 'tuanchengshan', '铁山': 'tieshan'}, 'code': 'huangshi'}, '郑州': {'sublist': {'二七': 'erqi', '上街': 'shangjie', '中牟': 'zhongmou', '荥阳': 'xingyang', '新郑': 'xinzheng', '管城': 'guanchenghuizu', '惠济': 'huiji', '巩义': 'gongyi', '中原': 'zhongyuan', '金水': 'jinshui', '高新区': 'gaoxinqu', '登封': 'dengfeng', '经开区': 'jingkaiqu', '郑东': 'zhengdong', '新密': 'xinmi'}, 'code': 'zz'}, '泰安': {'sublist': {'泰山': 'taishan', '东平': 'dongping', '岱岳': 'daiyue', '新泰': 'xintai', '肥城': 'feicheng', '宁阳': 'ningyang'}, 'code': 'taian'}, '黄冈': {'sublist': {'团风': 'tuanfeng', '罗田': 'luotian', '麻城': 'macheng', '黄州': 'huangzhou', '黄梅': 'huangmei', '浠水': 'xishui', '蕲春': 'qichun', '武穴': 'wuxue', '英山': 'yingshan', '红安': 'hongan'}, 'code': 'huanggang'}, '南充': {'sublist': {'西充': 'xichong', '嘉陵': 'jialing', '蓬安': 'pengan', '顺庆': 'shunqing', '营山': 'yingshan', '阆中': 'langzhong', '仪陇': 'yilong', '南部': 'nanbu', '高坪': 'gaoping'}, 'code': 'nanchong'}, '琼海': {'sublist': {'龙江': 'longjiang', '会山': 'huishan', '石壁': 'shibi', '博鳌': 'boao', '长坡': 'changpo', '潭门': 'tanmen', '中原': 'zhongyuan', '万泉': 'wanquan', '大路': 'dalu', '嘉积': 'jiaji', '阳江': 'yangjiang', '塔洋': 'tayang'}, 'code': 'qh'}, '双流': {'sublist': {'牧马山': 'mumashan', '白家': 'baijia', '籍田': 'jitian', '其他': 'shuangliuqita', '华阳': 'huayang', '黄龙溪': 'huanglongxi', '煎茶': 'jiancha', '白沙': 'baisha', '文星': 'wenxing', '胜利': 'shengli', '金桥': 'jinqiao', '三星': 'shuangliusanxing', '永安': 'yongan', '航空港': 'hangkonggang', '兴隆': 'xinglong', '黄水': 'huangshui', '大林': 'dalin', '九江': 'jiujiang', '万安': 'wanan', '东升': 'dongsheng', '黄甲': 'huangjia', '永兴': 'yongxing', '合江': 'hejiang', '正兴': 'zhengxing', '公兴': 'gongxing', '太平': 'taiping', '彭镇': 'pengzhen', '新兴': 'shuangliuxinxing'}, 'code': 'shuangliu'}, '营口': {'sublist': {'鲅鱼圈': 'bayuquan', '西市': 'xishi', '盖州': 'gaizhou', '大石桥': 'dashiqiao', '老边': 'laobian', '站前': 'zhanqian'}, 'code': 'yingkou'}, '石家庄': {'sublist': {'桥西': 'qiaoxi', '灵寿': 'lingshou', '裕华': 'yuhua', '元氏': 'yuanshi', '长安': 'changan', '开发区': 'kaifaqu', '晋州': 'jinzhou', '井陉矿区': 'jingxingkuangqu', '无极': 'wuji', '深泽': 'shenze', '行唐': 'xingtang', '高邑': 'gaoyi', '正定': 'zhengding', '辛集': 'xinji', '赵县': 'zhaoxian', '平山': 'pingshan', '新乐': 'xinle', '栾城': 'luancheng', '井陉': 'jingxing', '桥东': 'qiaodong', '藁城': 'gaocheng', '石家庄周边': 'shijiazhuangzhoubian', '赞皇': 'zanhuang', '新华': 'xinhua', '鹿泉': 'luquan'}, 'code': 'sjz'}, '大庆': {'sublist': {'肇州': 'zhaozhou', '龙凤': 'longfeng', '大同': 'datong', '红岗': 'honggang', '萨尔图': 'saertu', '让胡路': 'ranghulu', '林甸': 'lindian', '肇源': 'zhaoyuan', '杜尔伯特': 'duerbote'}, 'code': 'daqing'}, '神农架': {'sublist': {'木鱼': 'muyu', '红坪': 'hongping', '宋洛': 'songluo', '松柏': 'songbai', '阳日': 'yangri', '新华': 'xinhua', '下谷平': 'xiaguoping', '九湖': 'jiuhu'}, 'code': 'shennongjia'}, '海东': {'sublist': {'平安': 'pingan', '互助': 'huzhu', '乐都': 'ledu', '民和': 'minhe', '化隆': 'hualong', '循化': 'xunhua'}, 'code': 'haidong'}, '巢湖': {'sublist': {'含山': 'hanshan', '居巢': 'juchao', '无为': 'wuwei', '庐江': 'lujiang', '和县': 'hexian'}, 'code': 'chaohu'}, '五指山': {'sublist': {'南圣镇': 'nanshengzhen', '冲山镇': 'chongshanzhen', '毛阳镇': 'maoyangzhen', '五指山周边': 'wuzhishanzhoubian', '番阳镇': 'fanyangzhen'}, 'code': 'wuzhishan'}, '雅安': {'sublist': {'名山': 'mingshan', '宝兴': 'baoxing', '天全': 'tianquan', '汉源': 'hanyuan', '石棉': 'shimian', '荥经': 'yingjing', '芦山': 'lushan', '雨城': 'yucheng'}, 'code': 'yaan'}, '哈密': {'sublist': {'伊吾': 'yiwu', '巴里坤': 'balikun', '哈密市': 'hami'}, 'code': 'hami'}, '朝阳': {'sublist': {'朝阳县': 'chaoyang', '龙城': 'longcheng', '凌源': 'lingyuan', '建平': 'jianping', '双塔': 'shuangta', '北票': 'beipiao', '喀喇沁左翼': 'kalaqinzuoyi'}, 'code': 'chaoyang'}, '德州': {'sublist': {'禹城': 'yucheng', '齐河': 'qihe', '武城': 'wucheng', '宁津': 'ningjin', '德城': 'decheng', '临邑': 'linyi', '平原': 'pingyuan', '夏津': 'xiajin', '陵县': 'lingxian', '庆云': 'qingyun', '乐陵': 'leling'}, 'code': 'dezhou'}, '海口': {'sublist': {'龙华': 'longhua', '秀英': 'xiuying', '美兰': 'meilan', '琼山': 'qiongshan', '其他': 'qita'}, 'code': 'hn'}, '儋州': {'sublist': {'雅星': 'yaxing', '大成': 'dacheng', '白马井': 'baimajing', '兰洋': 'lanyang', '海头': 'haitou', '南丰': 'nanfeng', '光村': 'guangcun', '峨蔓': 'eman', '木棠': 'mutang', '那大': 'nada', '洋浦经济开发区': 'yangpukaifaqu', '和庆': 'heqing'}, 'code': 'danzhou'}, '内江': {'sublist': {'威远': 'weiyuan', '东兴': 'dongxing', '资中': 'zizhong', '市中': 'shizhong', '隆昌': 'longchang'}, 'code': 'neijiang'}, '邢台': {'sublist': {'南宫': 'nangong', '广宗': 'guangzong', '南和': 'nanhe', '沙河': 'shahe', '清河': 'qinghe', '邢台县': 'xingtaixian', '平乡': 'pingxiang', '临城': 'lincheng', '新河': 'xinhe', '威县': 'weixian', '桥东区': 'qiaodong', '宁晋': 'ningjin', '临西': 'linxi', '巨鹿': 'julu', '桥西区': 'qiaoxi', '柏乡': 'baixiang', '内丘': 'neiqiu', '隆尧': 'longyao', '任县': 'renxian'}, 'code': 'xingtai'}, '绍兴': {'sublist': {'诸暨': 'zhuji', '上虞': 'shangyu', '新昌': 'xinchang', '柯桥区': 'shaoxing', '越城': 'yuecheng', '嵊州': 'shengzhou'}, 'code': 'shaoxing'}, '铜川': {'sublist': {'宜君': 'yijun', '印台': 'yintai', '耀州': 'yaozhou', '王益': 'wangyi'}, 'code': 'tongchuan'}, '吴忠': {'sublist': {'盐池': 'yanchi', '青铜峡': 'qingtongxia', '利通': 'litong', '同心': 'tongxin'}, 'code': 'wuzhong'}, '宿州': {'sublist': {'萧县': 'xiaoxian', '砀山': 'dangshan', '灵璧': 'lingbi', '埇桥': 'yongqiao', '泗县': 'sixian'}, 'code': 'ahsuzhou'}, '辽阳': {'sublist': {'灯塔': 'dengta', '白塔': 'baita', '弓长岭': 'gongzhangling', '太子河': 'taizihe', '宏伟': 'hongwei', '文圣': 'wensheng', '辽阳县': 'liaoyang'}, 'code': 'liaoyang'}, '大理': {'sublist': {'祥云': 'xiangyun', '漾濞': 'yangbi', '宾川': 'binzhou', '云龙': 'yunlong', '大理市': 'dali', '弥渡': 'midu', '巍山': 'weishan', '剑川': 'jianchuan', '永平': 'yongping', '洱源': 'eryuan', '南涧': 'nanjian', '鹤庆': 'heqing'}, 'code': 'dali'}, '沧州': {'sublist': {'吴桥': 'wuqiao', '孟村': 'mengcun', '海兴': 'haixing', '黄骅': 'huanghua', '新华区': 'xinhua', '泊头': 'botou', '盐山': 'yanshan', '运河区': 'yunhe', '沧县': 'cangxian', '河间': 'hejian', '肃宁': 'suning', '青县': 'qingxian', '南皮': 'nanpi', '献县': 'xianxian', '东光': 'dongguang', '任丘': 'renqiu'}, 'code': 'cangzhou'}, '仙桃': {'sublist': {'张沟': 'zhanggou', '西流河': 'xiliuhe', '长埫口': 'changtangkou', '工业园': 'gongyeyuan', '干河': 'ganhe', '彭场': 'pengchang', '毛嘴': 'maozui', '胡场': 'huchang', '沙嘴': 'shazui', '龙华山': 'longhuanshan', '剅河': 'louhe', '沙湖': 'sanhu', '杨林尾': 'yanglinwei', '郭河': 'guohe', '郑场': 'zhengchang', '沔城': 'miancheng', '通海口': 'tonghai', '三伏潭': 'sanfutan', '陈场': 'chenchang'}, 'code': 'xiantao'}, '慈溪': {'sublist': {'浒山': 'hushan', '宗汉': 'zonghan', '坎墩': 'kandun', '其他': 'cixiqita'}, 'code': 'cixi'}, '兴安': {'sublist': {'科尔沁右翼前': 'keerqinyouyiqian', '扎赉特': 'zhalaite', '乌兰浩特': 'wulanhaote', '科尔沁右翼中': 'keerqinyouyizhong', '阿尔山': 'aershan', '突泉': 'tuquan'}, 'code': 'xingan'}, '景德镇': {'sublist': {'珠山': 'zhushan', '昌江': 'changjiang', '乐平': 'leping', '浮梁': 'fuliang'}, 'code': 'jingdezhen'}, '运城': {'sublist': {'新绛': 'xinjiang', '河津': 'hejin', '垣曲': 'yuanqu', '平陆': 'pinglu', '夏县': 'xiaxian', '闻喜': 'wenxi', '临猗': 'linyi', '永济': 'yongji', '芮城': 'ruicheng', '万荣': 'wanrong', '盐湖': 'yanhu', '稷山': 'jishan', '绛县': 'jiangxian'}, 'code': 'yuncheng'}, '南昌': {'sublist': {'红谷滩新区': 'honggutanxinqu', '青山湖': 'qingshanhu', '昌北': 'changbei', '进贤': 'jinxian', '湾里': 'wanli', '青云谱': 'qingyunpu', '西湖': 'xihu', '东湖': 'donghu', '新建': 'xinjian', '高新区': 'gaoxinqu', '南昌县': 'nanchang', '安义': 'anyi'}, 'code': 'nc'}, '开封': {'sublist': {'兰考': 'lankao', '龙亭': 'longting', '通许': 'tongxu', '开封县': 'kaifeng', '鼓楼': 'gulou', '尉氏': 'weishi', '顺河': 'shunhe', '金明': 'jinming', '禹王台': 'yuwangtai', '杞县': 'qixian'}, 'code': 'kaifeng'}, '佳木斯': {'sublist': {'桦南': 'huanan', '郊区': 'jiaoqu', '前进': 'qianjin', '富锦': 'fujin', '同江': 'tongjiang', '抚远': 'fuyuan', '汤原': 'tangyuan', '桦川': 'huachuan', '向阳': 'xiangyang', '东风': 'dongfeng'}, 'code': 'jiamusi'}, '石河子': {'sublist': {'北泉': 'beiquan', '新城': 'xincheng', '东城': 'dongcheng', '石河子乡': 'shihezixiang', '老街': 'laojie', '红山': 'hongshan', '向阳': 'xiangyang'}, 'code': 'shihezi'}, '湖州': {'sublist': {'德清': 'deqing', '南浔': 'nanxun', '长兴': 'changxing', '吴兴': 'wuxing', '安吉': 'anji'}, 'code': 'huzhou'}, '大同': {'sublist': {'矿区': 'kuangqu', '南郊': 'nanjiao', '浑源': 'hunyuan', '左云': 'zuoyun', '大同县': 'datongxian', '阳高': 'yanggao', '城区': 'chengqu', '新荣': 'xinrong', '广灵': 'guangling', '天镇': 'tianzhen', '灵丘': 'lingqiu'}, 'code': 'datong'}, '宣城': {'sublist': {'泾县': 'jingxian', '广德': 'guangde', '宣州': 'xuanzhou', '绩溪': 'jixi', '旌德': 'jingde', '郎溪': 'langxi', '宁国': 'ningguo'}, 'code': 'xuancheng'}, '莱芜': {'sublist': {'莱城': 'laicheng', '钢城': 'gangcheng'}, 'code': 'laiwu'}, '广州': {'sublist': {'白云': 'baiyun', '番禺': 'fanyu', '荔湾': 'liwan', '经济开发区': 'jingjikaifa', '天河': 'tianhe', '佛山': 'foshan', '东莞': 'dongguan', '黄埔': 'huangpu', '广州周边': 'guangzhouzhoubian', '越秀': 'yuexiu', '海珠': 'haizhu', '南沙': 'nansha', '增城': 'zengcheng', '花都': 'huadou', '萝岗': 'luogang', '从化': 'conghua'}, 'code': 'gz'}, '克孜勒苏': {'sublist': {'乌恰': 'wuqia', '阿克陶': 'aketao', '阿合奇': 'aheqi', '阿图什': 'atushi'}, 'code': 'kezilesu'}, '嘉兴': {'sublist': {'南湖': 'nanhu', '平湖': 'pinghu', '桐乡': 'tongxiang', '经济开发区': 'jingjikaifaqu', '嘉善': 'jiashan', '海宁': 'haining', '海盐': 'haiyan', '秀洲': 'xiuzhou'}, 'code': 'jiaxing'}, '酒泉': {'sublist': {'敦煌': 'dunhuang', '阿克塞': 'akesai', '金塔': 'jinta', '肃州': 'suzhou', '瓜州': 'guazhou', '玉门': 'yumen', '肃北': 'subei'}, 'code': 'jiuquan'}, '安庆': {'sublist': {'迎江': 'yingjiang', '望江': 'wangjiang', '枞阳': 'congyang', '大观': 'daguan', '宿松': 'susong', '怀宁': 'huaining', '岳西': 'yuexi', '潜山': 'qianshan', '宜秀': 'yixiu', '太湖': 'taihu', '桐城': 'tongcheng'}, 'code': 'anqing'}, '乌鲁木齐': {'sublist': {'米东': 'midong', '头屯河': 'toutunhe', '东山': 'dongshan', '新市': 'xinshi', '沙依巴克': 'shayibake', '达坂城': 'dabancheng', '水磨沟': 'shuimogou', '乌鲁木齐县': 'wulumuqi', '天山': 'tianshan', '开发': 'kaifa'}, 'code': 'xj'}}
    job_save_gj = []
    page_number=1
    judge = 0
    total = 0
    flag_next = True
    while flag_next:
        time.sleep(1)
        try:
            jobs_url_li = []
            pn_number = str(0 + 32*(page_number - 1))
            try:
                city_jc = dict_city[cityName]['code']
            except:
                judge = 1
                break
            d_pos = {"kw111": compName}
            postname = parse.urlencode(d_pos).encode('utf-8')
            company_encode = str(postname).split('kw111=')[1][:-1]
            if countyName != '':
                try:
                    county_jc=dict_city[cityName]['sublist'][countyName]
                    url_gj_zwss = "http://" + city_jc + ".ganji.com/zhaopin/"+county_jc+"/s/f" + pn_number + "/_" + company_encode + "/"
                except:
                    try:
                        county_Name = countyName.replace('区','')
                        county_jc = dict_city[cityName]['sublist'][county_Name]
                        url_gj_zwss = "http://" + city_jc + ".ganji.com/zhaopin/" + county_jc + "/s/f" + pn_number + "/_" + company_encode + "/"
                    except:
                        url_gj_zwss = "http://" + city_jc + ".ganji.com/zhaopin/s/f" + pn_number + "/_" + company_encode + "/"
                        pass
            else:
                url_gj_zwss = "http://"+ city_jc +".ganji.com/zhaopin/s/f" + pn_number + "/_" + company_encode + "/"
            print('gj----',url_gj_zwss)

            try:
                html_li_text=xh_pd_req(pos_url=url_gj_zwss,data='',headers=head_reqst())
            except:
                flag_next = False
                break
            # request_li = request.Request(url=url_gj_zwss, headers=head_reqst())
            # reponse_li = urlopen(request_li,timeout=3).read()
            # html_li_text = reponse_li.decode('utf-8', errors='ignore')
            #print(html_li_text)
            if "赶集" in html_li_text:
                sel = Selector(text=html_li_text)
                job_gj_li = sel.xpath('//div[@id="list-job-id"]/dl')
                for job_gj in job_gj_li[0:]:
                    job_gj_na = job_gj.xpath('string(descendant::div[@class="fl j-title"]/a/@gjalog)').extract()[0]
                    try:
                        job_gj_name=job_gj_na.split('@kw=')[1].split('@num')[0]
                    except:
                        pass
                    if job_gj_name == compName:
                        job_gj_url = job_gj.xpath('string(descendant::div[@class="fl j-title"]/a/@href)').extract()[0]
                        if 'http' not in job_gj_url:
                            job_gj_url = "http://"+ city_jc +".ganji.com" + job_gj_url
                        jobs_url_li.append(job_gj_url)
                        # print(jobs_url_li)
                #判断是否进入下一页
                try:
                    if len(sel.xpath('//div[@id="list-job-id"]/dl')) < 32:
                         flag_next = False
                    else:
                         page_number = page_number + 1
                         # print('进入下一页')
                         if page_number >30 :                    #若总页数大于30页，默认进入了死循环，强制退出
                             print("爬取页数超过30页，强制退出")
                             flag_next = False
                except:
                    # traceback.print_exc()
                    flag_next = False
                    pass
                for index,job_gj_url1 in enumerate(jobs_url_li):
                     # print(index)
                     time.sleep(random.uniform(0.3, 0.6))
                     #print(job_gj_url1)
                     try:
                         # request_job_xq = request.Request(url=job_gj_url1, headers=head_reqst())
                         # request_job_xq = urlopen(request_job_xq,timeout=4).read()
                         # job_xq_text = request_job_xq.decode('utf-8', errors='ignore')
                         job_xq_text = xh_pd_req(pos_url=job_gj_url1, data='', headers=head_reqst())
                         zw_data_gj = zwjx_gj(text=job_xq_text, compName=compName)
                         zw_data_gj['type'] = 'job'
                         zw_data_gj['channel'] = channelid
                         zw_data_gj['companyName'] = compName
                         zw_data_gj['province'] = provName
                         zw_data_gj['city'] = cityName_0
                         zw_data_gj['county'] = countyName
                         print('gj-------',zw_data_gj)
                         job_save_gj.append(zw_data_gj)
                     except:
                         # traceback.print_exc()
                         logging.exception("Exception Logged")
                         sj_str = str(int(time.time() * 1000))
                         logging.error('gj_job_jx_fail----' + sj_str)

                     if len(job_save_gj) == 3:
                         total = total + 3
                         data = json.dumps(job_save_gj)
                         data = data.encode('utf-8')
                         requests.post(url=job_save_url, data=data)
                         logging.error('gj_jobl----3')
                         job_save_gj = []
                if len(job_save_gj) == 3 or len(job_save_gj) == 0:
                     pass
                else:
                     total = total + len(job_save_gj)
                     data = json.dumps(job_save_gj)
                     data = data.encode('utf-8')
                     requests.post(url=job_save_url, data=data)
                     logging.error('gj_jobl----yfs')
        except:
            logging.exception("Exception Logged")
            # traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_hzrczw(compName, provName, cityName, countyName,cityName_0, channelid=5):
    job_save_hzrc=[]
    page_number = 1
    judge = 0
    total = 0
    flag_next = True
    while flag_next:
        try:
            jobs_url_li=[]
            time.sleep(1)
            adress= (provName+cityName_0+countyName).strip()
            url_hzrc_zwss = "http://www.hzrc.com/ww/b/c/wwbc_result.html"
            print("hzrc----", url_hzrc_zwss)
            pageNo = str(page_number)
            fam_data = {
                "option": "",
                "type": "",
                "pageNo": pageNo,
                "ishcj": "",
                "aca111": "",
                "aab301": "330100000000",
                "acc217": "",
                "aac011": "",
                "aab056": "",
                "aab020": "",
                "acb241": "",
                "aae396": "",
                "acb239": "",
                "acb210s": "",
                "conditionsall": "",
                "addtosearch": "",
                "aca112": "",
                "aab010": adress,
                "keyword": compName
            }
            data = parse.urlencode(fam_data).encode('utf-8')
            try:
                html_li_text=xh_pd_req(pos_url=url_hzrc_zwss,data=data,headers=head_reqst())
            except:
                flag_next = False
                break
            # request_zw = request.Request(url=url_hzrc_zwss, data=data, headers=head_reqst())
            # html_li_text = request.urlopen(request_zw,timeout=3).read().decode('utf-8', errors='ignore')
            # print(html_li_text)
            if "杭州人才" in html_li_text:
                sel = Selector(text=html_li_text)
                job_hzrc_li = sel.xpath('//ul[@class="bg4_ul"]/li')
                for job_hzrc in job_hzrc_li[0:]:
                    job_hzrc_name = \
                    job_hzrc.xpath('string(//ul[@class="bg4_ul"]/li//div[@class="bg4_3"]/a/span)').extract()[0]
                    # print(job_hzrc_name)
                    if job_hzrc_name == compName:
                        job_hzrc_id = job_hzrc.xpath('string(div/div[@class="bg4_2"]/a/div/span/@id)').extract()[0]
                        job_hzrc_url = "http://www.hzrc.com/ww/b/c/wwbc_jobdeatils.html?acb210=" + job_hzrc_id
                        # print(job_hzrc_url)
                        jobs_url_li.append(job_hzrc_url)
                #判断是否进入下一页
                try:
                    if len(sel.xpath('//ul[@class="bg4_ul"]/li')) < 15:
                        flag_next = False
                    else:
                        # print("开始爬取第%s页"%page_number)
                        page_number = page_number + 1
                        if page_number > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                            # print("爬取页数超过30页，强制退出")
                            flag_next = False
                except:
                    traceback.print_exc()
                    logging.exception("Exception Logged")
                    flag_next = False
                    pass
                for job_url_1 in jobs_url_li[0:]:
                    # print(job_url_1)
                    time.sleep(random.uniform(0.3, 0.6))
                    try:
                        # request_jx = request.Request((job_url_1), headers=head_reqst())
                        # job_hzrc_text = request.urlopen(request_jx,timeout=4).read().decode('utf-8', errors='ignore')
                        job_hzrc_text = xh_pd_req(pos_url=job_url_1, data=data, headers=head_reqst())
                        zw_data_hzrc=zwjx_hzrc(text=job_hzrc_text, compName=compName)
                        zw_data_hzrc['type'] = 'job'
                        zw_data_hzrc['channel'] = channelid
                        zw_data_hzrc['companyName'] = compName
                        zw_data_hzrc['province'] = provName
                        zw_data_hzrc['city'] = cityName_0
                        zw_data_hzrc['county'] = countyName
                        print("hzrc---------",zw_data_hzrc)
                        job_save_hzrc.append(zw_data_hzrc)
                    except:
                        traceback.print_exc()
                        logging.exception("Exception Logged")
                        pass
                    if len(job_save_hzrc) == 3:
                        total = total+3
                        data = json.dumps(job_save_hzrc)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('hzrc_jobl----3')
                        job_save_hzrc = []
                if len(job_save_hzrc) == 3 or len(job_save_hzrc) == 0:
                    pass
                else:
                    total = total + len(job_save_hzrc)
                    data = json.dumps(job_save_hzrc)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('hzrc_jobl----yfs')
            elif "" == html_li_text:
                flag_next = False
        except:
            logging.exception("Exception Logged")
            # traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)

    print('爬取完成')
'''中华英才旧版'''
def get_zhyczw_0(compName, provName, cityName, countyName,cityName_0, channelid=6):
    #原始码表
    '''
    [{"id":"18","name":"安徽","mark":"A","en":"anhui","l2":[{"id":"193","name":"合肥","en":"hefei","l3":[{"id":"1891","name":"庐阳区","en":"luyangqu"},{"id":"1892","name":"瑶海区","en":"yaohaiqu"},{"id":"1893","name":"蜀山区","en":"shushanqu"},{"id":"1894","name":"包河区","en":"baohequ"},{"id":"1895","name":"长丰县","en":"changfengxian"},{"id":"1896","name":"肥东县","en":"feidongxian"},{"id":"1897","name":"肥西县","en":"feixixian"},{"id":"4163","name":"政务区","en":"zhengwuqu"},{"id":"4164","name":"滨湖区","en":"binghuqu"},{"id":"4165","name":"经开区","en":"jingkaiqu"},{"id":"4166","name":"高新区","en":"gaoxinqu"},{"id":"4167","name":"北城区","en":"beichengqu"}]},{"id":"194","name":"芜湖","en":"wuhu","l3":[{"id":"1898","name":"镜湖区","en":"jinghuqu"},{"id":"1899","name":"弋江区","en":"yijiangqu"},{"id":"1900","name":"鸠江区","en":"jiujiangqu"},{"id":"1901","name":"三山区","en":"sanshanqu"},{"id":"1902","name":"芜湖县","en":"wuhuxian"},{"id":"1903","name":"繁昌县","en":"fanchangxian"},{"id":"1904","name":"南陵县","en":"nanlingxian"}]},{"id":"195","name":"蚌埠","en":"bengbu","l3":[{"id":"1905","name":"蚌山区","en":"bangshanqu"},{"id":"1906","name":"龙子湖","en":"longzihu"},{"id":"1907","name":"禹会区","en":"yuhuiqu"},{"id":"1908","name":"淮上区","en":"huaishangqu"},{"id":"1909","name":"怀远县","en":"huaiyuanxian"},{"id":"1910","name":"五河县","en":"wuhexian"},{"id":"1911","name":"固镇县","en":"guzhenxian"}]},{"id":"196","name":"淮南","en":"huainan","l3":[{"id":"1912","name":"田家庵","en":"tianjiaan"},{"id":"1913","name":"大通区","en":"datongqu"},{"id":"1914","name":"谢家集","en":"xiejiaji"},{"id":"1915","name":"八公山","en":"bagongshan"},{"id":"1916","name":"潘集区","en":"panjiqu"},{"id":"1917","name":"凤台县","en":"fengtaixian"}]},{"id":"197","name":"马鞍山","en":"maanshan","l3":[{"id":"1918","name":"雨山区","en":"yushanqu"},{"id":"1919","name":"金家庄","en":"jinjiazhuang"},{"id":"1920","name":"花山区","en":"huashanqu"},{"id":"1921","name":"当涂县","en":"dangtuxian"}]},{"id":"198","name":"淮北","en":"huaibei","l3":[{"id":"1922","name":"相山区","en":"xiangshanqu"},{"id":"1923","name":"杜集区","en":"dujiqu"},{"id":"1924","name":"烈山区","en":"lieshanqu"},{"id":"1925","name":"濉溪县","en":"suixixian"}]},{"id":"199","name":"铜陵","en":"tongling","l3":[{"id":"1926","name":"铜官山","en":"tongguanshan"},{"id":"1927","name":"狮子山","en":"shizishan"},{"id":"1928","name":"郊　区","en":"jiao　qu"},{"id":"1929","name":"铜陵县","en":"tonglingxian"}]},{"id":"200","name":"安庆","en":"anqing","l3":[{"id":"1930","name":"迎江区","en":"yingjiangqu"},{"id":"1931","name":"大观区","en":"daguanqu"},{"id":"1932","name":"宜秀区","en":"yixiuqu"},{"id":"1933","name":"桐城","en":"tongchengshi"},{"id":"1934","name":"怀宁县","en":"huainingxian"},{"id":"1935","name":"枞阳县","en":"zongyangxian"},{"id":"1936","name":"潜山县","en":"qianshanxian"},{"id":"1937","name":"太湖县","en":"taihuxian"},{"id":"1938","name":"宿松县","en":"susongxian"},{"id":"1939","name":"望江县","en":"wangjiangxian"},{"id":"1940","name":"岳西县","en":"yuexixian"}]},{"id":"201","name":"黄山","en":"huangshan","l3":[{"id":"1941","name":"屯溪区","en":"tunxiqu"},{"id":"1942","name":"黄山区","en":"huangshanqu"},{"id":"1943","name":"徽州区","en":"huizhouqu"},{"id":"1944","name":"歙　县","en":"xi　xian"},{"id":"1945","name":"休宁县","en":"xiuningxian"},{"id":"1946","name":"黟　县","en":"yi　xian"},{"id":"1947","name":"祁门县","en":"qimenxian"}]},{"id":"202","name":"滁州","en":"chuzhou","l3":[{"id":"1948","name":"琅琊区","en":"langyaqu"},{"id":"1949","name":"南谯区","en":"nanqiaoqu"},{"id":"1950","name":"天长","en":"tianchangshi"},{"id":"1951","name":"明光","en":"mingguangshi"},{"id":"1952","name":"来安县","en":"laianxian"},{"id":"1953","name":"全椒县","en":"quanjiaoxian"},{"id":"1954","name":"定远县","en":"dingyuanxian"},{"id":"1955","name":"凤阳县","en":"fengyangxian"}]},{"id":"203","name":"阜阳","en":"fuyang","l3":[{"id":"1956","name":"颍州区","en":"yingzhouqu"},{"id":"1957","name":"颍东区","en":"yingdongqu"},{"id":"1958","name":"颍泉区","en":"yingquanqu"},{"id":"1959","name":"界首","en":"jieshoushi"},{"id":"1960","name":"临泉县","en":"linquanxian"},{"id":"1961","name":"太和县","en":"taihexian"},{"id":"1962","name":"阜南县","en":"funanxian"},{"id":"1963","name":"颍上县","en":"yingshangxian"}]},{"id":"204","name":"宿州","en":"sz","l3":[{"id":"1964","name":"埇桥区","en":"yongqiaoqu"},{"id":"1965","name":"砀山县","en":"dangshanxian"},{"id":"1966","name":"萧　县","en":"xiao　xian"},{"id":"1967","name":"灵璧县","en":"lingbixian"},{"id":"1968","name":"泗　县","en":"si　xian"}]},{"id":"205","name":"巢湖","en":"chaohu","l3":[{"id":"1969","name":"居巢区","en":"juchaoqu"},{"id":"1970","name":"庐江县","en":"lujiangxian"},{"id":"1971","name":"无为县","en":"wuweixian"},{"id":"1972","name":"含山县","en":"hanshanxian"},{"id":"1973","name":"和　县","en":"he　xian"}]},{"id":"206","name":"六安","en":"luan","l3":[{"id":"1974","name":"金安区","en":"jinanqu"},{"id":"1975","name":"裕安区","en":"yuanqu"},{"id":"1976","name":"寿　县","en":"shou　xian"},{"id":"1977","name":"霍邱县","en":"huoqiuxian"},{"id":"1978","name":"舒城县","en":"shuchengxian"},{"id":"1979","name":"金寨县","en":"jinzhaixian"},{"id":"1980","name":"霍山县","en":"huoshanxian"}]},{"id":"207","name":"亳州","en":"bozhou","l3":[{"id":"1981","name":"谯城区","en":"qiaochengqu"},{"id":"1982","name":"涡阳县","en":"woyangxian"},{"id":"1983","name":"蒙城县","en":"mengchengxian"},{"id":"1984","name":"利辛县","en":"lixinxian"}]},{"id":"208","name":"池州","en":"chizhou","l3":[{"id":"1985","name":"贵池区","en":"guichiqu"},{"id":"1986","name":"东至县","en":"dongzhixian"},{"id":"1987","name":"石台县","en":"shitaixian"},{"id":"1988","name":"青阳县","en":"qingyangxian"}]},{"id":"209","name":"宣城","en":"xuancheng","l3":[{"id":"1989","name":"宣州区","en":"xuanzhouqu"},{"id":"1990","name":"宁国","en":"ningguoshi"},{"id":"1991","name":"郎溪县","en":"langxixian"},{"id":"1992","name":"广德县","en":"guangdexian"},{"id":"1993","name":"泾　县","en":"jing　xian"},{"id":"1994","name":"绩溪县","en":"jixixian"},{"id":"1995","name":"旌德县","en":"jingdexian"}]}]},{"id":"44","name":"澳门特别行政区","mark":"A","en":"aomentebiexingzhengqu","l2":[{"id":"455","name":"澳门","en":"aomen","l3":[{"id":"4057","name":"澳门","en":"aomen"}]}]},{"id":"34","name":"北京","mark":"B","en":"beijingshi","l2":[{"id":"398","name":"北京","en":"beijing","l3":[{"id":"3545","name":"东城区","en":"dongchengqu"},{"id":"3546","name":"西城区","en":"xichengqu"},{"id":"3547","name":"崇文区","en":"chongwenqu"},{"id":"3548","name":"宣武区","en":"xuanwuqu"},{"id":"3549","name":"朝阳区","en":"chaoyangqu"},{"id":"3550","name":"丰台区","en":"fengtaiqu"},{"id":"3551","name":"石景山区","en":"shijingshanqu"},{"id":"3552","name":"海淀区","en":"haidianqu"},{"id":"3553","name":"门头沟区","en":"mentougouqu"},{"id":"3554","name":"房山区","en":"fangshanqu"},{"id":"3555","name":"通州区","en":"tongzhouqu"},{"id":"3556","name":"顺义区","en":"shunyiqu"},{"id":"3557","name":"昌平区","en":"changpingqu"},{"id":"3558","name":"大兴区","en":"daxingqu"},{"id":"3559","name":"怀柔区","en":"huairouqu"},{"id":"3560","name":"平谷区","en":"pingguqu"},{"id":"3561","name":"密云县","en":"miyunxian"},{"id":"3562","name":"延庆县","en":"yanqingxian"}]}]},{"id":"37","name":"重庆","mark":"C","en":"chongqing","l2":[{"id":"401","name":"重庆","en":"chongqing","l3":[{"id":"3600","name":"渝中区","en":"yuzhongqu"},{"id":"3601","name":"大渡口","en":"dadukou"},{"id":"3602","name":"江北区","en":"jiangbeiqu"},{"id":"3603","name":"沙坪坝","en":"shapingba"},{"id":"3604","name":"九龙坡","en":"jiulongpo"},{"id":"3605","name":"南岸区","en":"nananqu"},{"id":"3606","name":"北碚区","en":"beibeiqu"},{"id":"3607","name":"万盛区","en":"wanshengqu"},{"id":"3608","name":"双桥区","en":"shuangqiaoqu"},{"id":"3609","name":"渝北区","en":"yubeiqu"},{"id":"3610","name":"巴南区","en":"bananqu"},{"id":"3611","name":"万州区","en":"wanzhouqu"},{"id":"3612","name":"涪陵区","en":"fulingqu"},{"id":"3613","name":"黔江区","en":"qianjiangqu"},{"id":"3614","name":"长寿区","en":"changshouqu"},{"id":"3615","name":"江津区","en":"jiangjinqu"},{"id":"3616","name":"合川区","en":"hechuanqu"},{"id":"3617","name":"永川区","en":"yongchuanqu"},{"id":"3618","name":"南川区","en":"nanchuanqu"},{"id":"3619","name":"綦江县","en":"qijiangxian"},{"id":"3620","name":"潼南县","en":"tongnanxian"},{"id":"3621","name":"铜梁县","en":"tongliangxian"},{"id":"3622","name":"大足县","en":"dazuxian"},{"id":"3623","name":"荣昌县","en":"rongchangxian"},{"id":"3624","name":"璧山县","en":"bishanxian"},{"id":"3625","name":"垫江县","en":"dianjiangxian"},{"id":"3626","name":"武隆县","en":"wulongxian"},{"id":"3627","name":"丰都县","en":"fengdouxian"},{"id":"3628","name":"城口县","en":"chengkouxian"},{"id":"3629","name":"梁平县","en":"liangpingxian"},{"id":"3630","name":"开　县","en":"kai　xian"},{"id":"3631","name":"巫溪县","en":"wuxixian"},{"id":"3632","name":"巫山县","en":"wushanxian"},{"id":"3633","name":"奉节县","en":"fengjiexian"},{"id":"3634","name":"云阳县","en":"yunyangxian"},{"id":"3635","name":"忠　县","en":"zhong　xian"},{"id":"3636","name":"石柱土家族自治县","en":"shizhutujiazuzizhixian"},{"id":"3637","name":"彭水苗族土家族自治县","en":"pengshuimiaozutujiazuzizhixian"},{"id":"3638","name":"酉阳土家族苗族自治县","en":"youyangtujiazumiaozuzizhixian"},{"id":"3639","name":"秀山土家族苗族自治县","en":"xiushantujiazumiaozuzizhixian"}]}]},{"id":"19","name":"福建","mark":"F","en":"fujian","l2":[{"id":"210","name":"福州","en":"fuzhou","l3":[{"id":"1996","name":"鼓楼区","en":"gulouqu"},{"id":"1997","name":"台江区","en":"taijiangqu"},{"id":"1998","name":"仓山区","en":"cangshanqu"},{"id":"1999","name":"马尾区","en":"maweiqu"},{"id":"2000","name":"晋安区","en":"jinanqu"},{"id":"2001","name":"闽侯县","en":"minhouxian"},{"id":"2002","name":"连江县","en":"lianjiangxian"},{"id":"2003","name":"罗源县","en":"luoyuanxian"},{"id":"2004","name":"闽清县","en":"minqingxian"},{"id":"2005","name":"永泰县","en":"yongtaixian"},{"id":"2006","name":"平潭县","en":"pingtanxian"},{"id":"2007","name":"福清","en":"fuqingshi"},{"id":"2008","name":"长乐","en":"changleshi"}]},{"id":"211","name":"厦门","en":"xiamen","l3":[{"id":"2009","name":"思明区","en":"simingqu"},{"id":"2010","name":"海沧区","en":"haicangqu"},{"id":"2011","name":"湖里区","en":"huliqu"},{"id":"2012","name":"集美区","en":"jimeiqu"},{"id":"2013","name":"同安区","en":"tonganqu"},{"id":"2014","name":"翔安区","en":"xianganqu"}]},{"id":"212","name":"莆田","en":"putian","l3":[{"id":"2015","name":"城厢区","en":"chengxiangqu"},{"id":"2016","name":"涵江区","en":"hanjiangqu"},{"id":"2017","name":"荔城区","en":"lichengqu"},{"id":"2018","name":"秀屿区","en":"xiuyuqu"},{"id":"2019","name":"仙游县","en":"xianyouxian"}]},{"id":"213","name":"三明","en":"sanming","l3":[{"id":"2020","name":"梅列区","en":"meiliequ"},{"id":"2021","name":"三元区","en":"sanyuanqu"},{"id":"2022","name":"明溪县","en":"mingxixian"},{"id":"2023","name":"清流县","en":"qingliuxian"},{"id":"2024","name":"宁化县","en":"ninghuaxian"},{"id":"2025","name":"大田县","en":"datianxian"},{"id":"2026","name":"尤溪县","en":"youxixian"},{"id":"2027","name":"沙　县","en":"sha　xian"},{"id":"2028","name":"将乐县","en":"jianglexian"},{"id":"2029","name":"泰宁县","en":"tainingxian"},{"id":"2030","name":"建宁县","en":"jianningxian"},{"id":"2031","name":"永安","en":"yonganshi"},{"id":"2032","name":"泉州","en":"quanzhoushi"}]},{"id":"214","name":"泉州","en":"quanzhou","l3":[{"id":"2033","name":"鲤城区","en":"lichengqu"},{"id":"2034","name":"丰泽区","en":"fengzequ"},{"id":"2035","name":"洛江区","en":"luojiangqu"},{"id":"2036","name":"泉港区","en":"quangangqu"},{"id":"2037","name":"惠安县","en":"huianxian"},{"id":"2038","name":"安溪县","en":"anxixian"},{"id":"2039","name":"永春县","en":"yongchunxian"},{"id":"2040","name":"德化县","en":"dehuaxian"},{"id":"2041","name":"金门县","en":"jinmenxian"},{"id":"2042","name":"石狮","en":"shishishi"},{"id":"2043","name":"晋江","en":"jinjiangshi"},{"id":"2044","name":"南安","en":"nananshi"}]},{"id":"215","name":"漳州","en":"zhangzhou","l3":[{"id":"2045","name":"芗城区","en":"xiangchengqu"},{"id":"2046","name":"龙文区","en":"longwenqu"},{"id":"2047","name":"云霄县","en":"yunxiaoxian"},{"id":"2048","name":"漳浦县","en":"zhangpuxian"},{"id":"2049","name":"诏安县","en":"zhaoanxian"},{"id":"2050","name":"长泰县","en":"changtaixian"},{"id":"2051","name":"东山县","en":"dongshanxian"},{"id":"2052","name":"南靖县","en":"nanjingxian"},{"id":"2053","name":"平和县","en":"pinghexian"},{"id":"2054","name":"华安县","en":"huaanxian"},{"id":"2055","name":"龙海","en":"longhaishi"}]},{"id":"216","name":"南平","en":"nanping","l3":[{"id":"2056","name":"延平区","en":"yanpingqu"},{"id":"2057","name":"顺昌县","en":"shunchangxian"},{"id":"2058","name":"浦城县","en":"puchengxian"},{"id":"2059","name":"光泽县","en":"guangzexian"},{"id":"2060","name":"松溪县","en":"songxixian"},{"id":"2061","name":"政和县","en":"zhenghexian"},{"id":"2062","name":"邵武","en":"shaowushi"},{"id":"2063","name":"武夷山","en":"wuyishan"},{"id":"2064","name":"建瓯","en":"jianoushi"},{"id":"2065","name":"建阳","en":"jianyangshi"}]},{"id":"217","name":"龙岩","en":"longyan","l3":[{"id":"2066","name":"新罗区","en":"xinluoqu"},{"id":"2067","name":"长汀县","en":"changtingxian"},{"id":"2068","name":"永定县","en":"yongdingxian"},{"id":"2069","name":"上杭县","en":"shanghangxian"},{"id":"2070","name":"武平县","en":"wupingxian"},{"id":"2071","name":"连城县","en":"lianchengxian"},{"id":"2072","name":"漳平","en":"zhangpingshi"}]},{"id":"218","name":"宁德","en":"ningde","l3":[{"id":"2073","name":"蕉城区","en":"jiaochengqu"},{"id":"2074","name":"霞浦县","en":"xiapuxian"},{"id":"2075","name":"古田县","en":"gutianxian"},{"id":"2076","name":"屏南县","en":"pingnanxian"},{"id":"2077","name":"寿宁县","en":"shouningxian"},{"id":"2078","name":"周宁县","en":"zhouningxian"},{"id":"2079","name":"柘荣县","en":"zherongxian"},{"id":"2080","name":"福安","en":"fuanshi"},{"id":"2081","name":"福鼎","en":"fudingshi"}]}]},{"id":"31","name":"甘肃","mark":"G","en":"gansu","l2":[{"id":"368","name":"兰州","en":"lanzhou","l3":[{"id":"3346","name":"城关区","en":"chengguanqu"},{"id":"3347","name":"七里河","en":"qilihe"},{"id":"3348","name":"西固区","en":"xiguqu"},{"id":"3349","name":"安宁区","en":"anningqu"},{"id":"3350","name":"红古区","en":"hongguqu"},{"id":"3351","name":"永登县","en":"yongdengxian"},{"id":"3352","name":"皋兰县","en":"gaolanxian"},{"id":"3353","name":"榆中县","en":"yuzhongxian"}]},{"id":"369","name":"嘉峪关","en":"jiayuguan","l3":[{"id":"3354","name":"嘉峪关","en":"jiayuguanshi"}]},{"id":"370","name":"金昌","en":"jinchang","l3":[{"id":"3355","name":"金川区","en":"jinchuanqu"},{"id":"3356","name":"永昌县","en":"yongchangxian"}]},{"id":"371","name":"白银","en":"baiyin","l3":[{"id":"3357","name":"白银区","en":"baiyinqu"},{"id":"3358","name":"平川区","en":"pingchuanqu"},{"id":"3359","name":"靖远县","en":"jingyuanxian"},{"id":"3360","name":"会宁县","en":"huiningxian"},{"id":"3361","name":"景泰县","en":"jingtaixian"}]},{"id":"372","name":"天水","en":"tianshui","l3":[{"id":"3362","name":"秦州区","en":"qinzhouqu"},{"id":"3363","name":"麦积区","en":"maijiqu"},{"id":"3364","name":"清水县","en":"qingshuixian"},{"id":"3365","name":"秦安县","en":"qinanxian"},{"id":"3366","name":"甘谷县","en":"ganguxian"},{"id":"3367","name":"武山县","en":"wushanxian"},{"id":"3368","name":"张家川回族自治县","en":"zhangjiachuanhuizuzizhixian"}]},{"id":"373","name":"武威","en":"wuwei","l3":[{"id":"3369","name":"凉州区","en":"liangzhouqu"},{"id":"3370","name":"民勤县","en":"minqinxian"},{"id":"3371","name":"古浪县","en":"gulangxian"},{"id":"3372","name":"天祝藏族自治县","en":"tianzhuzangzuzizhixian"}]},{"id":"374","name":"张掖","en":"zhangye","l3":[{"id":"3373","name":"甘州区","en":"ganzhouqu"},{"id":"3374","name":"民乐县","en":"minlexian"},{"id":"3375","name":"临泽县","en":"linzexian"},{"id":"3376","name":"高台县","en":"gaotaixian"},{"id":"3377","name":"山丹县","en":"shandanxian"},{"id":"3378","name":"肃南裕固族自治县","en":"sunanyuguzuzizhixian"}]},{"id":"375","name":"平凉","en":"pingliang","l3":[{"id":"3379","name":"崆峒区","en":"kongtongqu"},{"id":"3380","name":"泾川县","en":"jingchuanxian"},{"id":"3381","name":"灵台县","en":"lingtaixian"},{"id":"3382","name":"崇信县","en":"chongxinxian"},{"id":"3383","name":"华亭县","en":"huatingxian"},{"id":"3384","name":"庄浪县","en":"zhuanglangxian"},{"id":"3385","name":"静宁县","en":"jingningxian"}]},{"id":"376","name":"酒泉","en":"jiuquan","l3":[{"id":"3386","name":"肃州区","en":"suzhouqu"},{"id":"3387","name":"玉门","en":"yumenshi"},{"id":"3388","name":"敦煌","en":"dunhuangshi"},{"id":"3389","name":"金塔县","en":"jintaxian"},{"id":"3390","name":"瓜州县","en":"guazhouxian"},{"id":"3391","name":"肃北蒙古族自治县","en":"subeimengguzuzizhixian"},{"id":"3392","name":"阿克塞哈萨克族自治县","en":"akesaihasakezuzizhixian"}]},{"id":"377","name":"庆阳","en":"qingyang","l3":[{"id":"3393","name":"西峰区","en":"xifengqu"},{"id":"3394","name":"庆城县","en":"qingchengxian"},{"id":"3395","name":"环　县","en":"huan　xian"},{"id":"3396","name":"华池县","en":"huachixian"},{"id":"3397","name":"合水县","en":"heshuixian"},{"id":"3398","name":"正宁县","en":"zhengningxian"},{"id":"3399","name":"宁　县","en":"ning　xian"},{"id":"3400","name":"镇原县","en":"zhenyuanxian"}]},{"id":"378","name":"定西","en":"dingxi","l3":[{"id":"3401","name":"安定区","en":"andingqu"},{"id":"3402","name":"通渭县","en":"tongweixian"},{"id":"3403","name":"陇西县","en":"longxixian"},{"id":"3404","name":"渭源县","en":"weiyuanxian"},{"id":"3405","name":"临洮县","en":"lintaoxian"},{"id":"3406","name":"漳　县","en":"zhang　xian"},{"id":"3407","name":"岷　县","en":"min　xian"}]},{"id":"379","name":"陇南","en":"longnan","l3":[{"id":"3408","name":"武都区","en":"wuduqu"},{"id":"3409","name":"成　县","en":"cheng　xian"},{"id":"3410","name":"文　县","en":"wen　xian"},{"id":"3411","name":"宕昌县","en":"dangchangxian"},{"id":"3412","name":"康　县","en":"kang　xian"},{"id":"3413","name":"西和县","en":"xihexian"},{"id":"3414","name":"礼　县","en":"li　xian"},{"id":"3415","name":"徽　县","en":"hui　xian"},{"id":"3416","name":"两当县","en":"liangdangxian"}]},{"id":"380","name":"临夏州","en":"linxiazhou","l3":[{"id":"3417","name":"临夏","en":"linxiashi"},{"id":"3418","name":"临夏县","en":"linxiaxian"},{"id":"3419","name":"康乐县","en":"kanglexian"},{"id":"3420","name":"永靖县","en":"yongjingxian"},{"id":"3421","name":"广河县","en":"guanghexian"},{"id":"3422","name":"和政县","en":"hezhengxian"},{"id":"3423","name":"东乡族自治县","en":"dongxiangzuzizhixian"},{"id":"3424","name":"积石山保安族东乡族撒","en":"jishishanbaoanzudongxiangzusa"}]},{"id":"381","name":"甘南州","en":"gannanzhou","l3":[{"id":"3425","name":"合作","en":"hezuoshi"},{"id":"3426","name":"临潭县","en":"lintanxian"},{"id":"3427","name":"卓尼县","en":"zhuonixian"},{"id":"3428","name":"舟曲县","en":"zhouquxian"},{"id":"3429","name":"迭部县","en":"diebuxian"},{"id":"3430","name":"玛曲县","en":"maquxian"},{"id":"3431","name":"碌曲县","en":"luquxian"},{"id":"3432","name":"夏河县","en":"xiahexian"}]}]},{"id":"25","name":"广东","mark":"G","en":"guangdong","l2":[{"id":"291","name":"广州","en":"guangzhou","l3":[{"id":"2709","name":"越秀区","en":"yuexiuqu"},{"id":"2710","name":"荔湾区","en":"liwanqu"},{"id":"2711","name":"海珠区","en":"haizhuqu"},{"id":"2712","name":"天河区","en":"tianhequ"},{"id":"2713","name":"白云区","en":"baiyunqu"},{"id":"2714","name":"黄埔区","en":"huangpuqu"},{"id":"2715","name":"番禺区","en":"fanyuqu"},{"id":"2716","name":"花都区","en":"huaduqu"},{"id":"2717","name":"南沙区","en":"nanshaqu"},{"id":"2718","name":"萝岗区","en":"luogangqu"},{"id":"2719","name":"增城","en":"zengchengshi"},{"id":"2720","name":"从化","en":"conghuashi"}]},{"id":"292","name":"深圳","en":"shenzhen","l3":[{"id":"2721","name":"福田区","en":"futianqu"},{"id":"2722","name":"罗湖区","en":"luohuqu"},{"id":"2723","name":"南山区","en":"nanshanqu"},{"id":"2724","name":"宝安区","en":"baoanqu"},{"id":"2725","name":"龙岗区","en":"longgangqu"},{"id":"2726","name":"盐田区","en":"yantianqu"},{"id":"4168","name":"布吉","en":"buji"},{"id":"4169","name":"坪山新区","en":"pingshanxinqu"},{"id":"4170","name":"光明新区","en":"guangmingxinqu"},{"id":"4171","name":"龙华新区","en":"longhuaxinqu"},{"id":"4172","name":"大鹏新区","en":"dapengxinqu"},{"id":"4173","name":"深圳周边","en":"shenzhenzhoubian"}]},{"id":"293","name":"珠海","en":"zhuhai","l3":[{"id":"2727","name":"香洲区","en":"xiangzhouqu"},{"id":"2728","name":"斗门区","en":"doumenqu"},{"id":"2729","name":"金湾区","en":"jinwanqu"}]},{"id":"294","name":"汕头","en":"shantou","l3":[{"id":"2730","name":"金平区","en":"jinpingqu"},{"id":"2731","name":"龙湖区","en":"longhuqu"},{"id":"2732","name":"濠江区","en":"haojiangqu"},{"id":"2733","name":"潮阳区","en":"chaoyangqu"},{"id":"2734","name":"潮南区","en":"chaonanqu"},{"id":"2735","name":"澄海区","en":"chenghaiqu"},{"id":"2736","name":"南澳县","en":"nanaoxian"}]},{"id":"295","name":"韶关","en":"shaoguan","l3":[{"id":"2737","name":"浈江区","en":"zhenjiangqu"},{"id":"2738","name":"武江区","en":"wujiangqu"},{"id":"2739","name":"曲江区","en":"qujiangqu"},{"id":"2740","name":"乐昌","en":"lechangshi"},{"id":"2741","name":"南雄","en":"nanxiongshi"},{"id":"2742","name":"始兴县","en":"shixingxian"},{"id":"2743","name":"仁化县","en":"renhuaxian"},{"id":"2744","name":"翁源县","en":"wengyuanxian"},{"id":"2745","name":"新丰县","en":"xinfengxian"},{"id":"2746","name":"乳源瑶族自治县","en":"ruyuanyaozuzizhixian"}]},{"id":"296","name":"佛山","en":"foshan","l3":[{"id":"2747","name":"禅城区","en":"chanchengqu"},{"id":"2748","name":"南海区","en":"nanhaiqu"},{"id":"2749","name":"顺德区","en":"shundequ"},{"id":"2750","name":"三水区","en":"sanshuiqu"},{"id":"2751","name":"高明区","en":"gaomingqu"}]},{"id":"297","name":"江门","en":"jiangmen","l3":[{"id":"2752","name":"江海区","en":"jianghaiqu"},{"id":"2753","name":"蓬江区","en":"pengjiangqu"},{"id":"2754","name":"新会区","en":"xinhuiqu"},{"id":"2755","name":"台山","en":"taishanshi"},{"id":"2756","name":"开平","en":"kaipingshi"},{"id":"2757","name":"鹤山","en":"heshanshi"},{"id":"2758","name":"恩平","en":"enpingshi"}]},{"id":"298","name":"湛江","en":"zhanjiang","l3":[{"id":"2759","name":"赤坎区","en":"chikanqu"},{"id":"2760","name":"霞山区","en":"xiashanqu"},{"id":"2761","name":"坡头区","en":"potouqu"},{"id":"2762","name":"麻章区","en":"mazhangqu"},{"id":"2763","name":"廉江","en":"lianjiangshi"},{"id":"2764","name":"雷州","en":"leizhoushi"},{"id":"2765","name":"吴川","en":"wuchuanshi"},{"id":"2766","name":"遂溪县","en":"suixixian"},{"id":"2767","name":"徐闻县","en":"xuwenxian"}]},{"id":"299","name":"茂名","en":"maoming","l3":[{"id":"2768","name":"茂南区","en":"maonanqu"},{"id":"2769","name":"茂港区","en":"maogangqu"},{"id":"2770","name":"高州","en":"gaozhoushi"},{"id":"2771","name":"化州","en":"huazhoushi"},{"id":"2772","name":"信宜","en":"xinyishi"},{"id":"2773","name":"电白县","en":"dianbaixian"}]},{"id":"300","name":"肇庆","en":"zhaoqing","l3":[{"id":"2774","name":"端州区","en":"duanzhouqu"},{"id":"2775","name":"鼎湖区","en":"dinghuqu"},{"id":"2776","name":"高要","en":"gaoyaoshi"},{"id":"2777","name":"四会","en":"sihuishi"},{"id":"2778","name":"广宁县","en":"guangningxian"},{"id":"2779","name":"怀集县","en":"huaijixian"},{"id":"2780","name":"封开县","en":"fengkaixian"},{"id":"2781","name":"德庆县","en":"deqingxian"}]},{"id":"301","name":"惠州","en":"huizhou","l3":[{"id":"2782","name":"惠城区","en":"huichengqu"},{"id":"2783","name":"惠阳区","en":"huiyangqu"},{"id":"2784","name":"博罗县","en":"boluoxian"},{"id":"2785","name":"惠东县","en":"huidongxian"},{"id":"2786","name":"龙门县","en":"longmenxian"}]},{"id":"302","name":"梅州","en":"meizhou","l3":[{"id":"2787","name":"梅江区","en":"meijiangqu"},{"id":"2788","name":"兴宁","en":"xingningshi"},{"id":"2789","name":"梅　县","en":"mei　xian"},{"id":"2790","name":"大埔县","en":"dabuxian"},{"id":"2791","name":"丰顺县","en":"fengshunxian"},{"id":"2792","name":"五华县","en":"wuhuaxian"},{"id":"2793","name":"平远县","en":"pingyuanxian"},{"id":"2794","name":"蕉岭县","en":"jiaolingxian"}]},{"id":"303","name":"汕尾","en":"shanwei","l3":[{"id":"2795","name":"城　区","en":"cheng　qu"},{"id":"2796","name":"陆丰","en":"lufengshi"},{"id":"2797","name":"海丰县","en":"haifengxian"},{"id":"2798","name":"陆河县","en":"luhexian"}]},{"id":"304","name":"河源","en":"heyuan","l3":[{"id":"2799","name":"源城区","en":"yuanchengqu"},{"id":"2800","name":"紫金县","en":"zijinxian"},{"id":"2801","name":"龙川县","en":"longchuanxian"},{"id":"2802","name":"连平县","en":"lianpingxian"},{"id":"2803","name":"和平县","en":"hepingxian"},{"id":"2804","name":"东源县","en":"dongyuanxian"}]},{"id":"305","name":"阳江","en":"yangjiang","l3":[{"id":"2805","name":"江城区","en":"jiangchengqu"},{"id":"2806","name":"阳春","en":"yangchunshi"},{"id":"2807","name":"阳西县","en":"yangxixian"},{"id":"2808","name":"阳东县","en":"yangdongxian"}]},{"id":"306","name":"清远","en":"qingyuan","l3":[{"id":"2809","name":"清城区","en":"qingchengqu"},{"id":"2810","name":"英德","en":"yingdeshi"},{"id":"2811","name":"连州","en":"lianzhoushi"},{"id":"2812","name":"佛冈县","en":"fogangxian"},{"id":"2813","name":"阳山县","en":"yangshanxian"},{"id":"2814","name":"清新县","en":"qingxinxian"},{"id":"2815","name":"连山壮族瑶族自治县","en":"lianshanzhuangzuyaozuzizhixian"},{"id":"2816","name":"连南瑶族自治县","en":"liannanyaozuzizhixian"}]},{"id":"307","name":"东莞","en":"dongguan","l3":[{"id":"4083","name":"莞城区","en":"guanchengqu"},{"id":"4084","name":"南城区","en":"nanchengqu"},{"id":"4085","name":"东城区","en":"dongchengqu"},{"id":"4086","name":"万江区","en":"wanjiangqu"},{"id":"4087","name":"虎门镇","en":"humenzhen"},{"id":"4088","name":"长安镇","en":"changanzhen"},{"id":"4089","name":"塘厦镇","en":"tangxiazhen"},{"id":"4090","name":"常平镇","en":"changpingzhen"},{"id":"4091","name":"厚街镇","en":"houjiezhen"},{"id":"4092","name":"凤岗镇","en":"fenggangzhen"},{"id":"4093","name":"清溪镇","en":"qingxizhen"},{"id":"4094","name":"寮步镇","en":"liaobuzhen"},{"id":"4095","name":"石碣镇","en":"shijiezhen"},{"id":"4096","name":"石龙镇","en":"shilongzhen"},{"id":"4097","name":"樟木头镇","en":"zhangmutouzhen"},{"id":"4098","name":"中堂镇","en":"zhongtangzhen"},{"id":"4099","name":"麻涌镇","en":"mayongzhen"},{"id":"4100","name":"大朗镇","en":"dalangzhen"},{"id":"4101","name":"大岭山镇","en":"dalingshanzhen"},{"id":"4102","name":"道窖镇","en":"daojiaozhen"},{"id":"4103","name":"茶山镇","en":"chashanzhen"},{"id":"4104","name":"高步镇","en":"gaobuzhen"},{"id":"4105","name":"横沥镇","en":"henglizhen"},{"id":"4106","name":"石排镇","en":"shipaizhen"},{"id":"4107","name":"东坑镇","en":"dongkengzhen"},{"id":"4108","name":"黄江镇","en":"huangjiangzhen"},{"id":"4109","name":"桥头镇","en":"qiaotouzhen"},{"id":"4110","name":"企石镇","en":"qishizhen"},{"id":"4111","name":"谢岗镇","en":"xiegangzhen"},{"id":"4112","name":"沙田镇","en":"shatianzhen"},{"id":"4113","name":"洪梅镇","en":"hongmeizhen"},{"id":"4114","name":"望牛墩镇","en":"wangniudunzhen"},{"id":"4115","name":"市区(除镇区)","en":"shiqu(chuzhenqu)"}]},{"id":"308","name":"中山","en":"zhongshan","l3":[{"id":"4059","name":"东区","en":"dongqu"},{"id":"4060","name":"南区","en":"nanqu"},{"id":"4061","name":"西区","en":"xiqu"},{"id":"4062","name":"石岐区","en":"shiqiqu"},{"id":"4063","name":"小榄镇","en":"xiaolanzhen"},{"id":"4064","name":"沙溪镇","en":"shaxizhen"},{"id":"4065","name":"南头镇","en":"nantouzhen"},{"id":"4066","name":"坦洲镇","en":"tanzhouzhen"},{"id":"4067","name":"东升镇","en":"dongshengzhen"},{"id":"4068","name":"南朗镇","en":"nanlangzhen"},{"id":"4069","name":"三乡镇","en":"sanxiangzhen"},{"id":"4070","name":"三角镇","en":"sanjiaozhen"},{"id":"4071","name":"五桂山","en":"wuguishan"},{"id":"4072","name":"东凤镇","en":"dongfengzhen"},{"id":"4073","name":"阜沙镇","en":"fushazhen"},{"id":"4074","name":"黄圃镇","en":"huangpuzhen"},{"id":"4075","name":"民众镇","en":"minzhongzhen"},{"id":"4076","name":"火炬区","en":"huojuqu"},{"id":"4077","name":"横栏镇","en":"henglanzhen"},{"id":"4078","name":"板芙镇","en":"banfuzhen"},{"id":"4079","name":"大涌镇","en":"dayongzhen"},{"id":"4080","name":"古镇","en":"guzhen"},{"id":"4081","name":"神湾镇","en":"shenwanzhen"},{"id":"4082","name":"港口镇","en":"gangkouzhen"}]},{"id":"456","name":"潮州","en":"chaozhou","l3":[{"id":"4116","name":"湘桥区","en":"xiangqiaoqu"},{"id":"4117","name":"潮安县","en":"chaoanxian"},{"id":"4118","name":"饶平县","en":"raopingxian"}]},{"id":"457","name":"揭阳","en":"jieyang","l3":[{"id":"4119","name":"榕城区","en":"rongchengqu"},{"id":"4120","name":"普宁","en":"puningshi"},{"id":"4121","name":"揭东县","en":"jiedongxian"},{"id":"4122","name":"揭西县","en":"jiexixian"},{"id":"4123","name":"惠来县","en":"huilaixian"}]},{"id":"458","name":"云浮","en":"yunfu","l3":[{"id":"4124","name":"云城区","en":"yunchengqu"},{"id":"4125","name":"罗定","en":"luodingshi"},{"id":"4126","name":"新兴县","en":"xinxingxian"},{"id":"4127","name":"郁南县","en":"yunanxian"},{"id":"4128","name":"云安县","en":"yunanxian"}]}]},{"id":"38","name":"广西壮族自治区","mark":"G","en":"guangxizhuangzuzizhiqu","l2":[{"id":"402","name":"南宁","en":"nanning","l3":[{"id":"3640","name":"青秀区","en":"qingxiuqu"},{"id":"3641","name":"兴宁区","en":"xingningqu"},{"id":"3642","name":"西乡塘区","en":"xixiangtangqu"},{"id":"3643","name":"良庆区（良庆镇）","en":"liangqingqu（liangqingzhen）"},{"id":"3644","name":"江南区","en":"jiangnanqu"},{"id":"3645","name":"邕宁区（蒲庙镇）","en":"yongningqu（pumiaozhen）"},{"id":"3646","name":"武鸣县（城厢镇）","en":"wumingxian（chengxiangzhen）"},{"id":"3647","name":"隆安县（城厢镇）","en":"longanxian（chengxiangzhen）"},{"id":"3648","name":"马山县（白山镇）","en":"mashanxian（baishanzhen）"},{"id":"3649","name":"上林县（大丰镇）","en":"shanglinxian（dafengzhen）"},{"id":"3650","name":"宾阳县（芦圩镇）","en":"binyangxian（luxuzhen）"},{"id":"3651","name":"横　县（横州镇）","en":"heng　xian（hengzhouzhen）"}]},{"id":"403","name":"柳州","en":"liuzhou","l3":[{"id":"3652","name":"城中区","en":"chengzhongqu"},{"id":"3653","name":"鱼峰区","en":"yufengqu"},{"id":"3654","name":"柳北区","en":"liubeiqu"},{"id":"3655","name":"柳南区","en":"liunanqu"},{"id":"3656","name":"柳江县（拉堡镇）","en":"liujiangxian（labaozhen）"},{"id":"3657","name":"柳城县（大埔镇）","en":"liuchengxian（dabuzhen）"},{"id":"3658","name":"鹿寨县（鹿寨镇）","en":"luzhaixian（luzhaizhen）"},{"id":"3659","name":"融安县（长安镇）","en":"ronganxian（changanzhen）"},{"id":"3660","name":"融水苗族自治县（融水）","en":"rongshuimiaozuzizhixian（rongshui）"},{"id":"3661","name":"三江侗族自治县（古宜）","en":"sanjiangdongzuzizhixian（guyi）"}]},{"id":"404","name":"桂林","en":"guilin","l3":[{"id":"3662","name":"象山区","en":"xiangshanqu"},{"id":"3663","name":"秀峰区","en":"xiufengqu"},{"id":"3664","name":"叠彩区","en":"diecaiqu"},{"id":"3665","name":"七星区","en":"qixingqu"},{"id":"3666","name":"雁山区","en":"yanshanqu"},{"id":"3667","name":"阳朔县（阳朔镇）","en":"yangshuoxian（yangshuozhen）"},{"id":"3668","name":"临桂县（临桂镇）","en":"linguixian（linguizhen）"},{"id":"3669","name":"灵川县（灵川镇）","en":"lingchuanxian（lingchuanzhen）"},{"id":"3670","name":"全州县（全州镇）","en":"quanzhouxian（quanzhouzhen）"},{"id":"3671","name":"平乐县（平乐镇）","en":"pinglexian（pinglezhen）"},{"id":"3672","name":"兴安县（兴安镇）","en":"xinganxian（xinganzhen）"},{"id":"3673","name":"灌阳县（灌阳镇）","en":"guanyangxian（guanyangzhen）"},{"id":"3674","name":"荔浦县（荔城镇）","en":"lipuxian（lichengzhen）"},{"id":"3675","name":"资源县（资源镇）","en":"ziyuanxian（ziyuanzhen）"},{"id":"3676","name":"永福县（永福镇）","en":"yongfuxian（yongfuzhen）"},{"id":"3677","name":"龙胜各族自治县（龙胜）","en":"longshenggezuzizhixian（longsheng）"},{"id":"3678","name":"恭城瑶族自治县（恭城）","en":"gongchengyaozuzizhixian（gongcheng）"}]},{"id":"405","name":"梧州","en":"wuzhou","l3":[{"id":"3679","name":"万秀区","en":"wanxiuqu"},{"id":"3680","name":"蝶山区","en":"dieshanqu"},{"id":"3681","name":"长洲区","en":"changzhouqu"},{"id":"3682","name":"岑溪（岑城镇）","en":"cenxishi（cenchengzhen）"},{"id":"3683","name":"苍梧县（龙圩镇）","en":"cangwuxian（longxuzhen）"},{"id":"3684","name":"藤　县（藤州镇）","en":"teng　xian（tengzhouzhen）"},{"id":"3685","name":"蒙山县（蒙山镇）","en":"mengshanxian（mengshanzhen）"}]},{"id":"406","name":"北海","en":"beihai","l3":[{"id":"3686","name":"海城区","en":"haichengqu"},{"id":"3687","name":"银海区","en":"yinhaiqu"},{"id":"3688","name":"铁山港区（南康镇）","en":"tieshangangqu（nankangzhen）"},{"id":"3689","name":"合浦县（廉州镇）","en":"hepuxian（lianzhouzhen）"}]},{"id":"407","name":"防城港","en":"fangchenggang","l3":[{"id":"3690","name":"港口区（渔洲坪街道）","en":"gangkouqu（yuzhoupingjiedao）"},{"id":"3691","name":"防城区（防城镇）","en":"fangchengqu（fangchengzhen）"},{"id":"3692","name":"东兴（东兴镇）","en":"dongxingshi（dongxingzhen）"},{"id":"3693","name":"上思县（思阳镇）","en":"shangsixian（siyangzhen）"}]},{"id":"408","name":"钦州","en":"qinzhou","l3":[{"id":"3694","name":"钦南区","en":"qinnanqu"},{"id":"3695","name":"钦北区","en":"qinbeiqu"},{"id":"3696","name":"灵山县（灵城镇）","en":"lingshanxian（lingchengzhen）"},{"id":"3697","name":"浦北县（小江镇）","en":"pubeixian（xiaojiangzhen）"}]},{"id":"409","name":"贵港","en":"guigang","l3":[{"id":"3698","name":"港北区（贵城街道）","en":"gangbeiqu（guichengjiedao）"},{"id":"3699","name":"港南区（桥圩镇）","en":"gangnanqu（qiaoxuzhen）"},{"id":"3700","name":"覃塘区（覃塘镇）","en":"tantangqu（tantangzhen）"},{"id":"3701","name":"桂平","en":"guipingshi"},{"id":"3702","name":"平南县（平南镇）","en":"pingnanxian（pingnanzhen）"}]},{"id":"410","name":"玉林","en":"yl","l3":[{"id":"3703","name":"玉州区（玉城街道）","en":"yuzhouqu（yuchengjiedao）"},{"id":"3704","name":"北流","en":"beiliushi"},{"id":"3705","name":"容　县（容州镇）","en":"rong　xian（rongzhouzhen）"},{"id":"3706","name":"陆川县（温泉镇）","en":"luchuanxian（wenquanzhen）"},{"id":"3707","name":"博白县（博白镇）","en":"bobaixian（bobaizhen）"},{"id":"3708","name":"兴业县（石南镇）","en":"xingyexian（shinanzhen）"}]},{"id":"411","name":"百色","en":"baise","l3":[{"id":"3709","name":"右江区（百色镇）","en":"youjiangqu（baisezhen）"},{"id":"3710","name":"凌云县（泗城镇）","en":"lingyunxian（sichengzhen）"},{"id":"3711","name":"平果县（马头镇）","en":"pingguoxian（matouzhen）"},{"id":"3712","name":"西林县（八达镇）","en":"xilinxian（badazhen）"},{"id":"3713","name":"乐业县（同乐镇）","en":"leyexian（tonglezhen）"},{"id":"3714","name":"德保县（城关镇）","en":"debaoxian（chengguanzhen）"},{"id":"3715","name":"田林县（乐里镇）","en":"tianlinxian（lelizhen）"},{"id":"3716","name":"田阳县（田州镇）","en":"tianyangxian（tianzhouzhen）"},{"id":"3717","name":"靖西县（新靖镇）","en":"jingxixian（xinjingzhen）"},{"id":"3718","name":"田东县（平马镇）","en":"tiandongxian（pingmazhen）"},{"id":"3719","name":"那坡县（城厢镇）","en":"napoxian（chengxiangzhen）"},{"id":"3720","name":"隆林各族自治县（新州）","en":"longlingezuzizhixian（xinzhou）"}]},{"id":"412","name":"贺州","en":"hezhou","l3":[{"id":"3721","name":"八步区（八步街道）","en":"babuqu（babujiedao）"},{"id":"3722","name":"钟山县（钟山镇）","en":"zhongshanxian（zhongshanzhen）"},{"id":"3723","name":"昭平县（昭平镇）","en":"zhaopingxian（zhaopingzhen）"},{"id":"3724","name":"富川瑶族自治县（富阳）","en":"fuchuanyaozuzizhixian（fuyang）"}]},{"id":"413","name":"河池","en":"hechi","l3":[{"id":"3725","name":"金城江区（金城江街道）","en":"jinchengjiangqu（jinchengjiangjiedao）"},{"id":"3726","name":"宜州（庆远镇）","en":"yizhoushi（qingyuanzhen）"},{"id":"3727","name":"天峨县（六排镇）","en":"tianexian（liupaizhen）"},{"id":"3728","name":"凤山县（凤城镇）","en":"fengshanxian（fengchengzhen）"},{"id":"3729","name":"南丹县（城关镇）","en":"nandanxian（chengguanzhen）"},{"id":"3730","name":"东兰县（东兰镇）","en":"donglanxian（donglanzhen）"},{"id":"3731","name":"都安瑶族自治县（安阳）","en":"douanyaozuzizhixian（anyang）"},{"id":"3732","name":"罗城仫佬族自治县（东）","en":"luochengmulaozuzizhixian（dong"},{"id":"3733","name":"巴马瑶族自治县（巴马","en":"bamayaozuzizhixian（bama"},{"id":"3734","name":"环江毛南族自治县（思","en":"huanjiangmaonanzuzizhixian（si"},{"id":"3735","name":"大化瑶族自治县（大化","en":"dahuayaozuzizhixian（dahua"}]},{"id":"414","name":"来宾","en":"laibin","l3":[{"id":"3736","name":"兴宾区","en":"xingbinqu"},{"id":"3737","name":"合山（岭南镇）","en":"heshanshi（lingnanzhen）"},{"id":"3738","name":"象州县（象州镇）","en":"xiangzhouxian（xiangzhouzhen）"},{"id":"3739","name":"武宣县（武宣镇）","en":"wuxuanxian（wuxuanzhen）"},{"id":"3740","name":"忻城县（城关镇）","en":"xinchengxian（chengguanzhen）"},{"id":"3741","name":"金秀瑶族自治县（金秀","en":"jinxiuyaozuzizhixian（jinxiu"}]},{"id":"415","name":"崇左","en":"chongzuo","l3":[{"id":"3742","name":"江州区（太平镇）","en":"jiangzhouqu（taipingzhen）"},{"id":"3743","name":"凭祥（凭祥镇）","en":"pingxiangshi（pingxiangzhen）"},{"id":"3744","name":"宁明县（城中镇）","en":"ningmingxian（chengzhongzhen）"},{"id":"3745","name":"扶绥县（新宁镇）","en":"fusuixian（xinningzhen）"},{"id":"3746","name":"龙州县（龙州镇）","en":"longzhouxian（longzhouzhen）"},{"id":"3747","name":"大新县（桃城镇）","en":"daxinxian（taochengzhen）"},{"id":"3748","name":"天等县（天等镇）","en":"tiandengxian（tiandengzhen）"}]}]},{"id":"28","name":"贵州","mark":"G","en":"guizhou","l2":[{"id":"333","name":"贵阳","en":"guiyang","l3":[{"id":"3022","name":"乌当区","en":"wudangqu"},{"id":"3023","name":"南明区","en":"nanmingqu"},{"id":"3024","name":"云岩区","en":"yunyanqu"},{"id":"3025","name":"花溪区","en":"huaxiqu"},{"id":"3026","name":"白云区","en":"baiyunqu"},{"id":"3027","name":"小河区","en":"xiaohequ"},{"id":"3028","name":"清镇","en":"qingzhenshi"},{"id":"3029","name":"开阳县","en":"kaiyangxian"},{"id":"3030","name":"息烽县","en":"xifengxian"},{"id":"3031","name":"修文县","en":"xiuwenxian"},{"id":"4131","name":"金阳新区","en":"jinyangxinqu"}]},{"id":"334","name":"六盘水","en":"liupanshui","l3":[{"id":"3032","name":"钟山区","en":"zhongshanqu"},{"id":"3033","name":"六枝特区","en":"liuzhitequ"},{"id":"3034","name":"水城县","en":"shuichengxian"},{"id":"3035","name":"盘　县","en":"pan　xian"}]},{"id":"335","name":"遵义","en":"zunyi","l3":[{"id":"3036","name":"红花岗区","en":"honghuagangqu"},{"id":"3037","name":"汇川区","en":"huichuanqu"},{"id":"3038","name":"赤水","en":"chishuishi"},{"id":"3039","name":"仁怀","en":"renhuaishi"},{"id":"3040","name":"遵义县","en":"zunyixian"},{"id":"3041","name":"桐梓县","en":"tongzixian"},{"id":"3042","name":"绥阳县","en":"suiyangxian"},{"id":"3043","name":"正安县","en":"zhenganxian"},{"id":"3044","name":"凤冈县","en":"fenggangxian"},{"id":"3045","name":"湄潭县","en":"meitanxian"},{"id":"3046","name":"余庆县","en":"yuqingxian"},{"id":"3047","name":"习水县","en":"xishuixian"},{"id":"3048","name":"道真仡佬族苗族自治县","en":"daozhenyilaozumiaozuzizhixian"},{"id":"3049","name":"务川仡佬族苗族自治县","en":"wuchuanyilaozumiaozuzizhixian"}]},{"id":"336","name":"安顺","en":"anshun","l3":[{"id":"3050","name":"西秀区","en":"xixiuqu"},{"id":"3051","name":"平坝县","en":"pingbaxian"},{"id":"3052","name":"普定县","en":"pudingxian"},{"id":"3053","name":"镇宁布依族苗族自治县","en":"zhenningbuyizumiaozuzizhixian"},{"id":"3054","name":"关岭布依族苗族自治县","en":"guanlingbuyizumiaozuzizhixian"},{"id":"3055","name":"紫云苗族布依族自治县","en":"ziyunmiaozubuyizuzizhixian"}]},{"id":"337","name":"铜仁地区","en":"tongrendiqu","l3":[{"id":"3056","name":"铜仁","en":"tongrenshi"},{"id":"3057","name":"江口县","en":"jiangkouxian"},{"id":"3058","name":"石阡县","en":"shiqianxian"},{"id":"3059","name":"思南县","en":"sinanxian"},{"id":"3060","name":"德江县","en":"dejiangxian"},{"id":"3061","name":"玉屏侗族自治县","en":"yupingdongzuzizhixian"},{"id":"3062","name":"印江土家族苗族自治县","en":"yinjiangtujiazumiaozuzizhixian"},{"id":"3063","name":"沿河土家族自治县","en":"yanhetujiazuzizhixian"},{"id":"3064","name":"松桃苗族自治县","en":"songtaomiaozuzizhixian"},{"id":"3065","name":"万山特区","en":"wanshantequ"}]},{"id":"338","name":"毕节地区","en":"bijiediqu","l3":[{"id":"3066","name":"毕节","en":"bijieshi"},{"id":"3067","name":"大方县","en":"dafangxian"},{"id":"3068","name":"黔西县","en":"qianxixian"},{"id":"3069","name":"金沙县","en":"jinshaxian"},{"id":"3070","name":"织金县","en":"zhijinxian"},{"id":"3071","name":"纳雍县","en":"nayongxian"},{"id":"3072","name":"赫章县","en":"hezhangxian"},{"id":"3073","name":"威宁彝族回族苗族自治","en":"weiningyizuhuizumiaozuzizhi"}]},{"id":"339","name":"黔西南州","en":"qianxinanzhou","l3":[{"id":"3074","name":"兴义","en":"xingyishi"},{"id":"3075","name":"兴仁县","en":"xingrenxian"},{"id":"3076","name":"普安县","en":"puanxian"},{"id":"3077","name":"晴隆县","en":"qinglongxian"},{"id":"3078","name":"贞丰县","en":"zhenfengxian"},{"id":"3079","name":"望谟县","en":"wangmoxian"},{"id":"3080","name":"册亨县","en":"cehengxian"},{"id":"3081","name":"安龙县","en":"anlongxian"}]},{"id":"340","name":"黔东南州","en":"qiandongnanzhou","l3":[{"id":"3082","name":"凯里","en":"kailishi"},{"id":"3083","name":"黄平县","en":"huangpingxian"},{"id":"3084","name":"施秉县","en":"shibingxian"},{"id":"3085","name":"三穗县","en":"sansuixian"},{"id":"3086","name":"镇远县","en":"zhenyuanxian"},{"id":"3087","name":"岑巩县","en":"cengongxian"},{"id":"3088","name":"天柱县","en":"tianzhuxian"},{"id":"3089","name":"锦屏县","en":"jinpingxian"},{"id":"3090","name":"剑河县","en":"jianhexian"},{"id":"3091","name":"台江县","en":"taijiangxian"},{"id":"3092","name":"黎平县","en":"lipingxian"},{"id":"3093","name":"榕江县","en":"rongjiangxian"},{"id":"3094","name":"从江县","en":"congjiangxian"},{"id":"3095","name":"雷山县","en":"leishanxian"},{"id":"3096","name":"麻江县","en":"majiangxian"},{"id":"3097","name":"丹寨县","en":"danzhaixian"}]},{"id":"341","name":"黔南州","en":"qiannanzhou","l3":[{"id":"3098","name":"都匀","en":"douyunshi"},{"id":"3099","name":"福泉","en":"fuquanshi"},{"id":"3100","name":"荔波县","en":"liboxian"},{"id":"3101","name":"贵定县","en":"guidingxian"},{"id":"3102","name":"瓮安县","en":"wenganxian"},{"id":"3103","name":"独山县","en":"dushanxian"},{"id":"3104","name":"平塘县","en":"pingtangxian"},{"id":"3105","name":"罗甸县","en":"luodianxian"},{"id":"3106","name":"长顺县","en":"changshunxian"},{"id":"3107","name":"龙里县","en":"longlixian"},{"id":"3108","name":"惠水县","en":"huishuixian"},{"id":"3109","name":"三都水族自治县","en":"sandoushuizuzizhixian"}]}]},{"id":"26","name":"海南","mark":"H","en":"hainan","l2":[{"id":"309","name":"海口","en":"haikou","l3":[{"id":"2819","name":"龙华区","en":"longhuaqu"},{"id":"2820","name":"秀英区","en":"xiuyingqu"},{"id":"2821","name":"琼山区","en":"qiongshanqu"},{"id":"2822","name":"美兰区","en":"meilanqu"}]},{"id":"310","name":"三亚","en":"sanya","l3":[{"id":"2823","name":"三亚","en":"sanyashi"}]}]},{"id":"45","name":"海外","mark":"H","en":"haiwai","l2":[{"id":"465","name":"海外","en":"haiwai"}]},{"id":"11","name":"河北","mark":"H","en":"hebei","l2":[{"id":"111","name":"石家庄","en":"shijiazhuang","l3":[{"id":"1111","name":"长安区","en":"changanqu"},{"id":"1112","name":"桥东区","en":"qiaodongqu"},{"id":"1113","name":"桥西区","en":"qiaoxiqu"},{"id":"1114","name":"新华区","en":"xinhuaqu"},{"id":"1115","name":"井陉矿区","en":"jingxingkuangqu"},{"id":"1116","name":"裕华区","en":"yuhuaqu"},{"id":"1117","name":"辛集","en":"xinjishi"},{"id":"1118","name":"藁城","en":"gaochengshi"},{"id":"1119","name":"晋州","en":"jinzhoushi"},{"id":"1120","name":"新乐","en":"xinleshi"},{"id":"1121","name":"鹿泉","en":"luquanshi"},{"id":"1122","name":"井陉县","en":"jingxingxian"},{"id":"1123","name":"正定县","en":"zhengdingxian"},{"id":"1124","name":"栾城县","en":"luanchengxian"},{"id":"1125","name":"行唐县","en":"xingtangxian"},{"id":"1126","name":"灵寿县","en":"lingshouxian"},{"id":"1127","name":"高邑县","en":"gaoyixian"},{"id":"1128","name":"深泽县","en":"shenzexian"},{"id":"1129","name":"赞皇县","en":"zanhuangxian"},{"id":"1130","name":"无极县","en":"wujixian"},{"id":"1131","name":"平山县","en":"pingshanxian"},{"id":"1132","name":"元氏县","en":"yuanshixian"},{"id":"1133","name":"赵　县","en":"zhao　xian"},{"id":"4161","name":"高新区","en":"gaoxinqu"}]},{"id":"112","name":"唐山","en":"tangshan","l3":[{"id":"1134","name":"路北区","en":"lubeiqu"},{"id":"1135","name":"路南区","en":"lunanqu"},{"id":"1136","name":"古冶区","en":"guyequ"},{"id":"1137","name":"开平区","en":"kaipingqu"},{"id":"1138","name":"丰南区","en":"fengnanqu"},{"id":"1139","name":"丰润区","en":"fengrunqu"},{"id":"1140","name":"遵化","en":"zunhuashi"},{"id":"1141","name":"迁安","en":"qiananshi"},{"id":"1142","name":"滦　县","en":"luan　xian"},{"id":"1143","name":"滦南县","en":"luannanxian"},{"id":"1144","name":"乐亭县","en":"letingxian"},{"id":"1145","name":"迁西县","en":"qianxixian"},{"id":"1146","name":"玉田县","en":"yutianxian"},{"id":"1147","name":"唐海县","en":"tanghaixian"}]},{"id":"113","name":"秦皇岛","en":"qinhuangdao","l3":[{"id":"1148","name":"海港区","en":"haigangqu"},{"id":"1149","name":"山海关区","en":"shanhaiguanqu"},{"id":"1150","name":"北戴河区","en":"beidaihequ"},{"id":"1151","name":"昌黎县","en":"changlixian"},{"id":"1152","name":"抚宁县","en":"funingxian"},{"id":"1153","name":"卢龙县","en":"lulongxian"},{"id":"1154","name":"青龙满族自治县","en":"qinglongmanzuzizhixian"}]},{"id":"114","name":"邯郸","en":"handan","l3":[{"id":"1155","name":"丛台区","en":"congtaiqu"},{"id":"1156","name":"邯山区","en":"hanshanqu"},{"id":"1157","name":"复兴区","en":"fuxingqu"},{"id":"1158","name":"峰峰矿区","en":"fengfengkuangqu"},{"id":"1159","name":"武安","en":"wuanshi"},{"id":"1160","name":"邯郸县","en":"handanxian"},{"id":"1161","name":"临漳县","en":"linzhangxian"},{"id":"1162","name":"成安县","en":"chenganxian"},{"id":"1163","name":"大名县","en":"damingxian"},{"id":"1164","name":"涉　县","en":"she　xian"},{"id":"1165","name":"磁　县","en":"ci　xian"},{"id":"1166","name":"肥乡县","en":"feixiangxian"},{"id":"1167","name":"永年县","en":"yongnianxian"},{"id":"1168","name":"邱　县","en":"qiu　xian"},{"id":"1169","name":"鸡泽县","en":"jizexian"},{"id":"1170","name":"广平县","en":"guangpingxian"},{"id":"1171","name":"馆陶县","en":"guantaoxian"},{"id":"1172","name":"魏　县","en":"wei　xian"},{"id":"1173","name":"曲周县","en":"quzhouxian"}]},{"id":"115","name":"邢台","en":"xingtai","l3":[{"id":"1174","name":"桥东区","en":"qiaodongqu"},{"id":"1175","name":"桥西区","en":"qiaoxiqu"},{"id":"1176","name":"南宫","en":"nangongshi"},{"id":"1177","name":"沙河","en":"shaheshi"},{"id":"1178","name":"邢台县","en":"xingtaixian"},{"id":"1179","name":"临城县","en":"linchengxian"},{"id":"1180","name":"内丘县","en":"neiqiuxian"},{"id":"1181","name":"柏乡县","en":"baixiangxian"},{"id":"1182","name":"隆尧县","en":"longyaoxian"},{"id":"1183","name":"任　县","en":"ren　xian"},{"id":"1184","name":"南和县","en":"nanhexian"},{"id":"1185","name":"宁晋县","en":"ningjinxian"},{"id":"1186","name":"巨鹿县","en":"juluxian"},{"id":"1187","name":"新河县","en":"xinhexian"},{"id":"1188","name":"广宗县","en":"guangzongxian"},{"id":"1189","name":"平乡县","en":"pingxiangxian"},{"id":"1190","name":"威　县","en":"wei　xian"},{"id":"1191","name":"清河县","en":"qinghexian"},{"id":"1192","name":"临西县","en":"linxixian"}]},{"id":"116","name":"保定","en":"baoding","l3":[{"id":"1193","name":"新区","en":"xinshiqu"},{"id":"1194","name":"北区","en":"beishiqu"},{"id":"1195","name":"南区","en":"nanshiqu"},{"id":"1196","name":"涿州","en":"zhuozhoushi"},{"id":"1197","name":"定州","en":"dingzhoushi"},{"id":"1198","name":"安国","en":"anguoshi"},{"id":"1199","name":"高碑店","en":"gaobeidianshi"},{"id":"1200","name":"满城县","en":"manchengxian"},{"id":"1201","name":"清苑县","en":"qingyuanxian"},{"id":"1202","name":"涞水县","en":"laishuixian"},{"id":"1203","name":"阜平县","en":"fupingxian"},{"id":"1204","name":"徐水县","en":"xushuixian"},{"id":"1205","name":"定兴县","en":"dingxingxian"},{"id":"1206","name":"唐　县","en":"tang　xian"},{"id":"1207","name":"高阳县","en":"gaoyangxian"},{"id":"1208","name":"容城县","en":"rongchengxian"},{"id":"1209","name":"涞源县","en":"laiyuanxian"},{"id":"1210","name":"望都县","en":"wangdouxian"},{"id":"1211","name":"安新县","en":"anxinxian"},{"id":"1212","name":"易　县","en":"yi　xian"},{"id":"1213","name":"曲阳县","en":"quyangxian"},{"id":"1214","name":"蠡　县","en":"li　xian"},{"id":"1215","name":"顺平县","en":"shunpingxian"},{"id":"1216","name":"博野县","en":"boyexian"},{"id":"1217","name":"雄　县","en":"xiong　xian"}]},{"id":"117","name":"张家口","en":"zhangjiakou","l3":[{"id":"1218","name":"桥西区","en":"qiaoxiqu"},{"id":"1219","name":"桥东区","en":"qiaodongqu"},{"id":"1220","name":"宣化区","en":"xuanhuaqu"},{"id":"1221","name":"下花园区","en":"xiahuayuanqu"},{"id":"1222","name":"宣化县","en":"xuanhuaxian"},{"id":"1223","name":"张北县","en":"zhangbeixian"},{"id":"1224","name":"康保县","en":"kangbaoxian"},{"id":"1225","name":"沽源县","en":"guyuanxian"},{"id":"1226","name":"尚义县","en":"shangyixian"},{"id":"1227","name":"蔚　县","en":"wei　xian"},{"id":"1228","name":"阳原县","en":"yangyuanxian"},{"id":"1229","name":"怀安县","en":"huaianxian"},{"id":"1230","name":"万全县","en":"wanquanxian"},{"id":"1231","name":"怀来县","en":"huailaixian"},{"id":"1232","name":"涿鹿县","en":"zhuoluxian"},{"id":"1233","name":"赤城县","en":"chichengxian"},{"id":"1234","name":"崇礼县","en":"chonglixian"}]},{"id":"118","name":"承德","en":"chengde","l3":[{"id":"1235","name":"双桥区","en":"shuangqiaoqu"},{"id":"1236","name":"双滦区","en":"shuangluanqu"},{"id":"1237","name":"鹰手营子矿区","en":"yingshouyingzikuangqu"},{"id":"1238","name":"承德县","en":"chengdexian"},{"id":"1239","name":"兴隆县","en":"xinglongxian"},{"id":"1240","name":"平泉县","en":"pingquanxian"},{"id":"1241","name":"滦平县","en":"luanpingxian"},{"id":"1242","name":"隆化县","en":"longhuaxian"},{"id":"1243","name":"丰宁满族自治县","en":"fengningmanzuzizhixian"},{"id":"1244","name":"宽城满族自治县","en":"kuanchengmanzuzizhixian"},{"id":"1245","name":"围场满族蒙古族自治县","en":"weichangmanzumengguzuzizhixian"}]},{"id":"119","name":"沧州","en":"cangzhou","l3":[{"id":"1246","name":"运河区","en":"yunhequ"},{"id":"1247","name":"新华区","en":"xinhuaqu"},{"id":"1248","name":"泊头","en":"botoushi"},{"id":"1249","name":"任丘","en":"renqiushi"},{"id":"1250","name":"黄骅","en":"huanghuashi"},{"id":"1251","name":"河间","en":"hejianshi"},{"id":"1252","name":"沧　县","en":"cang　xian"},{"id":"1253","name":"青　县","en":"qing　xian"},{"id":"1254","name":"东光县","en":"dongguangxian"},{"id":"1255","name":"海兴县","en":"haixingxian"},{"id":"1256","name":"盐山县","en":"yanshanxian"},{"id":"1257","name":"肃宁县","en":"suningxian"},{"id":"1258","name":"南皮县","en":"nanpixian"},{"id":"1259","name":"吴桥县","en":"wuqiaoxian"},{"id":"1260","name":"献　县","en":"xian　xian"},{"id":"1261","name":"孟村回族自治县","en":"mengcunhuizuzizhixian"}]},{"id":"120","name":"廊坊","en":"langfang","l3":[{"id":"1262","name":"安次区","en":"anciqu"},{"id":"1263","name":"广阳区","en":"guangyangqu"},{"id":"1264","name":"霸州","en":"bazhoushi"},{"id":"1265","name":"三河","en":"sanheshi"},{"id":"1266","name":"固安县","en":"guanxian"},{"id":"1267","name":"永清县","en":"yongqingxian"},{"id":"1268","name":"香河县","en":"xianghexian"},{"id":"1269","name":"大城县","en":"daichengxian"},{"id":"1270","name":"文安县","en":"wenanxian"},{"id":"1271","name":"大厂回族自治县","en":"dachanghuizuzizhixian"},{"id":"4144","name":"燕郊开发区","en":"yanjiaokaifaqu"}]},{"id":"121","name":"衡水","en":"hengshui","l3":[{"id":"1272","name":"桃城区","en":"taochengqu"},{"id":"1273","name":"冀州","en":"jizhoushi"},{"id":"1274","name":"深州","en":"shenzhoushi"},{"id":"1275","name":"枣强县","en":"zaoqiangxian"},{"id":"1276","name":"武邑县","en":"wuyixian"},{"id":"1277","name":"武强县","en":"wuqiangxian"},{"id":"1278","name":"饶阳县","en":"raoyangxian"},{"id":"1279","name":"安平县","en":"anpingxian"},{"id":"1280","name":"故城县","en":"guchengxian"},{"id":"1281","name":"景　县","en":"jing　xian"},{"id":"1282","name":"阜城县","en":"fuchengxian"}]}]},{"id":"22","name":"河南","mark":"H","en":"henan","l2":[{"id":"247","name":"郑州","en":"zhengzhou","l3":[{"id":"2331","name":"中原区","en":"zhongyuanqu"},{"id":"2332","name":"二七区","en":"erqiqu"},{"id":"2333","name":"管城区","en":"guanchengqu"},{"id":"2334","name":"金水区","en":"jinshuiqu"},{"id":"2335","name":"上街区","en":"shangjiequ"},{"id":"2336","name":"惠济区","en":"huijiqu"},{"id":"2337","name":"巩义","en":"gongyishi"},{"id":"2338","name":"荥阳","en":"xingyangshi"},{"id":"2339","name":"新密","en":"xinmishi"},{"id":"2340","name":"新郑","en":"xinzhengshi"},{"id":"2341","name":"登封","en":"dengfengshi"},{"id":"2342","name":"中牟县","en":"zhongmuxian"}]},{"id":"248","name":"开封","en":"kaifeng","l3":[{"id":"2343","name":"鼓楼区","en":"gulouqu"},{"id":"2344","name":"龙亭区","en":"longtingqu"},{"id":"2345","name":"顺河区","en":"shunhequ"},{"id":"2346","name":"禹王台","en":"yuwangtai"},{"id":"2347","name":"金明区","en":"jinmingqu"},{"id":"2348","name":"杞　县","en":"qi　xian"},{"id":"2349","name":"通许县","en":"tongxuxian"},{"id":"2350","name":"尉氏县","en":"weishixian"},{"id":"2351","name":"开封县","en":"kaifengxian"},{"id":"2352","name":"兰考县","en":"lankaoxian"}]},{"id":"249","name":"洛阳","en":"luoyang","l3":[{"id":"2353","name":"西工区","en":"xigongqu"},{"id":"2354","name":"老城区","en":"laochengqu"},{"id":"2355","name":"瀍河区","en":"chanhequ"},{"id":"2356","name":"涧西区","en":"jianxiqu"},{"id":"2357","name":"吉利区","en":"jiliqu"},{"id":"2358","name":"洛龙区","en":"luolongqu"},{"id":"2359","name":"偃师","en":"yanshishi"},{"id":"2360","name":"孟津县","en":"mengjinxian"},{"id":"2361","name":"新安县","en":"xinanxian"},{"id":"2362","name":"栾川县","en":"luanchuanxian"},{"id":"2363","name":"嵩县","en":"songxian"},{"id":"2364","name":"汝阳县","en":"ruyangxian"},{"id":"2365","name":"宜阳县","en":"yiyangxian"},{"id":"2366","name":"洛宁县","en":"luoningxian"},{"id":"2367","name":"伊川县","en":"yichuanxian"}]},{"id":"250","name":"平顶山","en":"pingdingshan","l3":[{"id":"2368","name":"新华区","en":"xinhuaqu"},{"id":"2369","name":"卫东区","en":"weidongqu"},{"id":"2370","name":"湛河区","en":"zhanhequ"},{"id":"2371","name":"石龙区","en":"shilongqu"},{"id":"2372","name":"舞钢","en":"wugangshi"},{"id":"2373","name":"汝州","en":"ruzhoushi"},{"id":"2374","name":"宝丰县","en":"baofengxian"},{"id":"2375","name":"叶　县","en":"ye　xian"},{"id":"2376","name":"鲁山县","en":"lushanxian"},{"id":"2377","name":"郏　县","en":"jia　xian"}]},{"id":"251","name":"焦作","en":"jiaozuo","l3":[{"id":"2378","name":"山阳区","en":"shanyangqu"},{"id":"2379","name":"解放区","en":"jiefangqu"},{"id":"2380","name":"中站区","en":"zhongzhanqu"},{"id":"2381","name":"马村区","en":"macunqu"},{"id":"2382","name":"沁阳","en":"qinyangshi"},{"id":"2383","name":"孟州","en":"mengzhoushi"},{"id":"2384","name":"修武县","en":"xiuwuxian"},{"id":"2385","name":"博爱县","en":"boaixian"},{"id":"2386","name":"武陟县","en":"wuzhixian"},{"id":"2387","name":"温　县","en":"wen　xian"}]},{"id":"252","name":"鹤壁","en":"hebi","l3":[{"id":"2388","name":"淇滨区","en":"qibinqu"},{"id":"2389","name":"山城区","en":"shanchengqu"},{"id":"2390","name":"鹤山区","en":"heshanqu"},{"id":"2391","name":"浚　县","en":"jun　xian"},{"id":"2392","name":"淇　县","en":"qi　xian"}]},{"id":"253","name":"新乡","en":"xinxiang","l3":[{"id":"2393","name":"卫滨区","en":"weibinqu"},{"id":"2394","name":"红旗区","en":"hongqiqu"},{"id":"2395","name":"凤泉区","en":"fengquanqu"},{"id":"2396","name":"牧野区","en":"muyequ"},{"id":"2397","name":"卫辉","en":"weihuishi"},{"id":"2398","name":"辉县","en":"huixianshi"},{"id":"2399","name":"新乡县","en":"xinxiangxian"},{"id":"2400","name":"获嘉县","en":"huojiaxian"},{"id":"2401","name":"原阳县","en":"yuanyangxian"},{"id":"2402","name":"延津县","en":"yanjinxian"},{"id":"2403","name":"封丘县","en":"fengqiuxian"},{"id":"2404","name":"长垣县","en":"changyuanxian"}]},{"id":"254","name":"安阳","en":"anyang","l3":[{"id":"2405","name":"北关区","en":"beiguanqu"},{"id":"2406","name":"文峰区","en":"wenfengqu"},{"id":"2407","name":"殷都区","en":"yindouqu"},{"id":"2408","name":"龙安区","en":"longanqu"},{"id":"2409","name":"林州","en":"linzhoushi"},{"id":"2410","name":"安阳县","en":"anyangxian"},{"id":"2411","name":"汤阴县","en":"tangyinxian"},{"id":"2412","name":"滑　县","en":"hua　xian"},{"id":"2413","name":"内黄县","en":"neihuangxian"}]},{"id":"255","name":"濮阳","en":"puyang","l3":[{"id":"2414","name":"华龙区","en":"hualongqu"},{"id":"2415","name":"清丰县","en":"qingfengxian"},{"id":"2416","name":"南乐县","en":"nanlexian"},{"id":"2417","name":"范　县","en":"fan　xian"},{"id":"2418","name":"台前县","en":"taiqianxian"},{"id":"2419","name":"濮阳县","en":"puyangxian"}]},{"id":"256","name":"许昌","en":"xuchang","l3":[{"id":"2420","name":"魏都区","en":"weidouqu"},{"id":"2421","name":"禹州","en":"yuzhoushi"},{"id":"2422","name":"长葛","en":"changgeshi"},{"id":"2423","name":"许昌县","en":"xuchangxian"},{"id":"2424","name":"鄢陵县","en":"yanlingxian"},{"id":"2425","name":"襄城县","en":"xiangchengxian"}]},{"id":"257","name":"漯河","en":"luohe","l3":[{"id":"2426","name":"源汇区","en":"yuanhuiqu"},{"id":"2427","name":"郾城区","en":"yanchengqu"},{"id":"2428","name":"召陵区","en":"zhaolingqu"},{"id":"2429","name":"舞阳县","en":"wuyangxian"},{"id":"2430","name":"临颍县","en":"linyingxian"}]},{"id":"258","name":"三门峡","en":"sanmenxia","l3":[{"id":"2431","name":"湖滨区","en":"hubinqu"},{"id":"2432","name":"义马","en":"yimashi"},{"id":"2433","name":"灵宝","en":"lingbaoshi"},{"id":"2434","name":"渑池县","en":"mianchixian"},{"id":"2435","name":"陕　县","en":"shan　xian"},{"id":"2436","name":"卢氏县","en":"lushixian"}]},{"id":"259","name":"南阳","en":"nanyang","l3":[{"id":"2437","name":"卧龙区","en":"wolongqu"},{"id":"2438","name":"宛城区","en":"wanchengqu"},{"id":"2439","name":"邓州","en":"dengzhoushi"},{"id":"2440","name":"南召县","en":"nanzhaoxian"},{"id":"2441","name":"方城县","en":"fangchengxian"},{"id":"2442","name":"西峡县","en":"xixiaxian"},{"id":"2443","name":"镇平县","en":"zhenpingxian"},{"id":"2444","name":"内乡县","en":"neixiangxian"},{"id":"2445","name":"淅川县","en":"xichuanxian"},{"id":"2446","name":"社旗县","en":"sheqixian"},{"id":"2447","name":"唐河县","en":"tanghexian"},{"id":"2448","name":"新野县","en":"xinyexian"},{"id":"2449","name":"桐柏县","en":"tongbaixian"}]},{"id":"260","name":"商丘","en":"shangqiu","l3":[{"id":"2450","name":"梁园区","en":"liangyuanqu"},{"id":"2451","name":"睢阳区","en":"huiyangqu"},{"id":"2452","name":"永城","en":"yongchengshi"},{"id":"2453","name":"民权县","en":"minquanxian"},{"id":"2454","name":"睢　县","en":"hui　xian"},{"id":"2455","name":"宁陵县","en":"ninglingxian"},{"id":"2456","name":"柘城县","en":"zhechengxian"},{"id":"2457","name":"虞城县","en":"yuchengxian"},{"id":"2458","name":"夏邑县","en":"xiayixian"}]},{"id":"261","name":"信阳","en":"xinyang","l3":[{"id":"2459","name":"浉河区","en":"shihequ"},{"id":"2460","name":"平桥区","en":"pingqiaoqu"},{"id":"2461","name":"罗山县","en":"luoshanxian"},{"id":"2462","name":"光山县","en":"guangshanxian"},{"id":"2463","name":"新　县","en":"xin　xian"},{"id":"2464","name":"商城县","en":"shangchengxian"},{"id":"2465","name":"固始县","en":"gushixian"},{"id":"2466","name":"潢川县","en":"huangchuanxian"},{"id":"2467","name":"淮滨县","en":"huaibinxian"},{"id":"2468","name":"息　县","en":"xi　xian"}]},{"id":"262","name":"周口","en":"zhoukou","l3":[{"id":"2469","name":"川汇区","en":"chuanhuiqu"},{"id":"2470","name":"项城","en":"xiangchengshi"},{"id":"2471","name":"扶沟县","en":"fugouxian"},{"id":"2472","name":"西华县","en":"xihuaxian"},{"id":"2473","name":"商水县","en":"shangshuixian"},{"id":"2474","name":"沈丘县","en":"shenqiuxian"},{"id":"2475","name":"郸城县","en":"danchengxian"},{"id":"2476","name":"淮阳县","en":"huaiyangxian"},{"id":"2477","name":"太康县","en":"taikangxian"},{"id":"2478","name":"鹿邑县","en":"luyixian"}]},{"id":"263","name":"驻马店","en":"zhumadian","l3":[{"id":"2479","name":"驿城区","en":"yichengqu"},{"id":"2480","name":"西平县","en":"xipingxian"},{"id":"2481","name":"上蔡县","en":"shangcaixian"},{"id":"2482","name":"平舆县","en":"pingyuxian"},{"id":"2483","name":"正阳县","en":"zhengyangxian"},{"id":"2484","name":"确山县","en":"queshanxian"},{"id":"2485","name":"泌阳县","en":"biyangxian"},{"id":"2486","name":"汝南县","en":"runanxian"},{"id":"2487","name":"遂平县","en":"suipingxian"},{"id":"2488","name":"新蔡县","en":"xincaixian"}]}]},{"id":"15","name":"黑龙江","mark":"H","en":"heilongjiang","l2":[{"id":"156","name":"哈尔滨","en":"haerbin","l3":[{"id":"1563","name":"松北","en":"songbei"},{"id":"1564","name":"道里","en":"daoli"},{"id":"1565","name":"南岗","en":"nangang"},{"id":"1566","name":"道外","en":"daowai"},{"id":"1567","name":"平房","en":"pingfang"},{"id":"1568","name":"香坊","en":"xiangfang"},{"id":"1569","name":"呼兰","en":"hulan"},{"id":"1570","name":"阿城","en":"acheng"},{"id":"1571","name":"双城","en":"shuangcheng"},{"id":"1572","name":"尚志","en":"shangzhi"},{"id":"1573","name":"五常","en":"wuchang"},{"id":"1574","name":"依兰","en":"yilan"},{"id":"1575","name":"方正","en":"fangzheng"},{"id":"1576","name":"宾县","en":"binxian"},{"id":"1577","name":"巴彦","en":"bayan"},{"id":"1578","name":"木兰","en":"mulan"},{"id":"1579","name":"通河","en":"tonghe"},{"id":"1580","name":"延寿","en":"yanshou"}]},{"id":"157","name":"齐齐哈尔","en":"qiqihaer","l3":[{"id":"1581","name":"龙沙","en":"longsha"},{"id":"1582","name":"建华","en":"jianhua"},{"id":"1583","name":"铁锋","en":"tiefeng"},{"id":"1584","name":"昂昂溪","en":"angangxi"},{"id":"1585","name":"富拉尔基","en":"fulaerji"},{"id":"1586","name":"碾子山","en":"nianzishan"},{"id":"1587","name":"梅里斯","en":"meilisi"},{"id":"1588","name":"讷河","en":"nehe"},{"id":"1589","name":"龙江","en":"longjiang"},{"id":"1590","name":"依安","en":"yian"},{"id":"1591","name":"泰来","en":"tailai"},{"id":"1592","name":"甘南","en":"gannan"},{"id":"1593","name":"富裕","en":"fuyu"},{"id":"1594","name":"克山","en":"keshan"},{"id":"1595","name":"克东","en":"kedong"},{"id":"1596","name":"拜泉","en":"baiquan"}]},{"id":"158","name":"鸡西","en":"jixi","l3":[{"id":"1597","name":"鸡冠区","en":"jiguanqu"},{"id":"1598","name":"恒山区","en":"hengshanqu"},{"id":"1599","name":"滴道区","en":"didaoqu"},{"id":"1600","name":"梨树区","en":"lishuqu"},{"id":"1601","name":"城子河区","en":"chengzihequ"},{"id":"1602","name":"麻山区","en":"mashanqu"},{"id":"1603","name":"虎林","en":"hulinshi"},{"id":"1604","name":"密山","en":"mishanshi"},{"id":"1605","name":"鸡东县","en":"jidongxian"}]},{"id":"159","name":"鹤岗","en":"hegang","l3":[{"id":"1606","name":"兴山区","en":"xingshanqu"},{"id":"1607","name":"向阳区","en":"xiangyangqu"},{"id":"1608","name":"工农区","en":"gongnongqu"},{"id":"1609","name":"南山区","en":"nanshanqu"},{"id":"1610","name":"兴安区","en":"xinganqu"},{"id":"1611","name":"东山区","en":"dongshanqu"},{"id":"1612","name":"萝北县","en":"luobeixian"},{"id":"1613","name":"绥滨县","en":"suibinxian"}]},{"id":"160","name":"双鸭山","en":"shuangyashan","l3":[{"id":"1614","name":"尖山区","en":"jianshanqu"},{"id":"1615","name":"岭东区","en":"lingdongqu"},{"id":"1616","name":"四方台区","en":"sifangtaiqu"},{"id":"1617","name":"宝山区","en":"baoshanqu"},{"id":"1618","name":"集贤县","en":"jixianxian"},{"id":"1619","name":"友谊县","en":"youyixian"},{"id":"1620","name":"宝清县","en":"baoqingxian"},{"id":"1621","name":"饶河县","en":"raohexian"}]},{"id":"161","name":"大庆","en":"daqing","l3":[{"id":"1622","name":"萨尔图区","en":"saertuqu"},{"id":"1623","name":"龙凤区","en":"longfengqu"},{"id":"1624","name":"让胡路区","en":"ranghuluqu"},{"id":"1625","name":"红岗区","en":"honggangqu"},{"id":"1626","name":"大同区","en":"datongqu"},{"id":"1627","name":"肇州县","en":"zhaozhouxian"},{"id":"1628","name":"肇源县","en":"zhaoyuanxian"},{"id":"1629","name":"林甸县","en":"lindianxian"},{"id":"1630","name":"杜尔伯特蒙古族自治县","en":"duerbotemengguzuzizhixian"}]},{"id":"162","name":"伊春","en":"yc","l3":[{"id":"1631","name":"伊春区","en":"yichunqu"},{"id":"1632","name":"南岔","en":"nancha"},{"id":"1633","name":"友好","en":"youhao"},{"id":"1634","name":"西林区","en":"xilinqu"},{"id":"1635","name":"翠峦区","en":"cuiluanqu"},{"id":"1636","name":"新青区","en":"xinqingqu"},{"id":"1637","name":"美溪区","en":"meixiqu"},{"id":"1638","name":"金山屯","en":"jinshantun"},{"id":"1639","name":"五营","en":"wuying"},{"id":"1640","name":"乌马河","en":"wumahe"},{"id":"1641","name":"汤旺河","en":"tangwanghe"},{"id":"1642","name":"带岭区","en":"dailingqu"},{"id":"1643","name":"乌伊岭","en":"wuyiling"},{"id":"1644","name":"红星区","en":"hongxingqu"},{"id":"1645","name":"上甘岭","en":"shangganling"},{"id":"1646","name":"铁力","en":"tielishi"},{"id":"1647","name":"嘉荫县","en":"jiayinxian"}]},{"id":"163","name":"佳木斯","en":"jiamusi","l3":[{"id":"1648","name":"前进区","en":"qianjinqu"},{"id":"1649","name":"向阳区","en":"xiangyangqu"},{"id":"1650","name":"东风区","en":"dongfengqu"},{"id":"1651","name":"郊区","en":"jiaoqu"},{"id":"1652","name":"同江","en":"tongjiangshi"},{"id":"1653","name":"富锦","en":"fujinshi"},{"id":"1654","name":"桦南县","en":"huananxian"},{"id":"1655","name":"桦川县","en":"huachuanxian"},{"id":"1656","name":"汤原县","en":"tangyuanxian"},{"id":"1657","name":"抚远县","en":"fuyuanxian"}]},{"id":"164","name":"七台河","en":"qitaihe","l3":[{"id":"1658","name":"桃山区","en":"taoshanqu"},{"id":"1659","name":"新兴区","en":"xinxingqu"},{"id":"1660","name":"茄子河区","en":"qiezihequ"},{"id":"1661","name":"勃利县","en":"bolixian"}]},{"id":"165","name":"牡丹江","en":"mudanjiang","l3":[{"id":"1662","name":"爱民区","en":"aiminqu"},{"id":"1663","name":"东安区","en":"donganqu"},{"id":"1664","name":"阳明区","en":"yangmingqu"},{"id":"1665","name":"西安区","en":"xianqu"},{"id":"1666","name":"绥芬河","en":"suifenheshi"},{"id":"1667","name":"海林","en":"hailinshi"},{"id":"1668","name":"宁安","en":"ninganshi"},{"id":"1669","name":"穆棱","en":"mulengshi"},{"id":"1670","name":"东宁县","en":"dongningxian"},{"id":"1671","name":"林口县","en":"linkouxian"}]},{"id":"166","name":"黑河","en":"heihe","l3":[{"id":"1672","name":"爱辉区","en":"aihuiqu"},{"id":"1673","name":"北安","en":"beianshi"},{"id":"1674","name":"五大连池","en":"wudalianchishi"},{"id":"1675","name":"嫩江县","en":"nenjiangxian"},{"id":"1676","name":"逊克县","en":"xunkexian"},{"id":"1677","name":"孙吴县","en":"sunwuxian"}]},{"id":"167","name":"绥化","en":"suihua","l3":[{"id":"1678","name":"北林区","en":"beilinqu"},{"id":"1679","name":"安达","en":"andashi"},{"id":"1680","name":"肇东","en":"zhaodongshi"},{"id":"1681","name":"海伦","en":"hailunshi"},{"id":"1682","name":"望奎县","en":"wangkuixian"},{"id":"1683","name":"兰西县","en":"lanxixian"},{"id":"1684","name":"青冈县","en":"qinggangxian"},{"id":"1685","name":"庆安县","en":"qinganxian"},{"id":"1686","name":"明水县","en":"mingshuixian"},{"id":"1687","name":"绥棱县","en":"suilengxian"}]},{"id":"168","name":"大兴安岭地区","en":"daxinganlingdiqu","l3":[{"id":"1688","name":"呼玛县","en":"humaxian"},{"id":"1689","name":"塔河县","en":"tahexian"},{"id":"1690","name":"漠河县","en":"mohexian"},{"id":"1691","name":"加格达奇区","en":"jiagedaqiqu"},{"id":"1692","name":"松岭区","en":"songlingqu"},{"id":"1693","name":"新林区","en":"xinlinqu"},{"id":"1694","name":"呼中区","en":"huzhongqu"}]}]},{"id":"23","name":"湖北","mark":"H","en":"hubei","l2":[{"id":"264","name":"武汉","en":"wuhan","l3":[{"id":"2489","name":"江岸","en":"jiangan"},{"id":"2490","name":"江汉","en":"jianghan"},{"id":"2491","name":"硚口","en":"qiaokou"},{"id":"2492","name":"汉阳","en":"hanyang"},{"id":"2493","name":"武昌","en":"wuchang"},{"id":"2494","name":"青山","en":"qingshan"},{"id":"2495","name":"洪山","en":"hongshan"},{"id":"2496","name":"东西湖","en":"dongxihu"},{"id":"2497","name":"汉南","en":"hannan"},{"id":"2498","name":"蔡甸","en":"caidian"},{"id":"2499","name":"江夏","en":"jiangxia"},{"id":"2500","name":"黄陂","en":"huangbei"},{"id":"2501","name":"新洲","en":"xinzhou"}]},{"id":"265","name":"黄石","en":"huangshi","l3":[{"id":"2502","name":"黄石港","en":"huangshigang"},{"id":"2503","name":"西塞山","en":"xisaishan"},{"id":"2504","name":"下陆","en":"xialu"},{"id":"2505","name":"铁山","en":"tieshan"},{"id":"2506","name":"大冶","en":"daye"},{"id":"2507","name":"阳新","en":"yangxin"}]},{"id":"266","name":"襄阳","en":"xiangyang","l3":[{"id":"2508","name":"襄城","en":"xiangcheng"},{"id":"2509","name":"樊城","en":"fancheng"},{"id":"2510","name":"襄州","en":"xiangzhou"},{"id":"2511","name":"老河口","en":"laohekou"},{"id":"2512","name":"枣阳","en":"zaoyang"},{"id":"2513","name":"宜城","en":"yicheng"},{"id":"2514","name":"南漳","en":"nanzhang"},{"id":"2515","name":"谷城","en":"gucheng"},{"id":"2516","name":"保康","en":"baokang"}]},{"id":"267","name":"十堰","en":"shiyan","l3":[{"id":"2517","name":"茅箭","en":"maojian"},{"id":"2518","name":"张湾","en":"zhangwan"},{"id":"2519","name":"丹江口","en":"danjiangkou"},{"id":"2520","name":"郧县","en":"yunxian"},{"id":"2521","name":"郧西","en":"yunxi"},{"id":"2522","name":"竹山","en":"zhushan"},{"id":"2523","name":"竹溪","en":"zhuxi"},{"id":"2524","name":"房县","en":"fangxian"}]},{"id":"268","name":"荆州","en":"jingzhou","l3":[{"id":"2525","name":"沙市","en":"shashi"},{"id":"2526","name":"荆州","en":"jingzhou"},{"id":"2527","name":"石首","en":"shishou"},{"id":"2528","name":"洪湖","en":"honghu"},{"id":"2529","name":"松滋","en":"songzi"},{"id":"2530","name":"公安","en":"gongan"},{"id":"2531","name":"监利","en":"jianli"},{"id":"2532","name":"江陵","en":"jiangling"}]},{"id":"269","name":"宜昌","en":"yichang","l3":[{"id":"2533","name":"西陵","en":"xiling"},{"id":"2534","name":"伍家岗","en":"wujiagang"},{"id":"2535","name":"点军","en":"dianjun"},{"id":"2536","name":"猇亭","en":"xiaoting"},{"id":"2537","name":"夷陵","en":"yiling"},{"id":"2538","name":"宜都","en":"yidou"},{"id":"2539","name":"当阳","en":"dangyang"},{"id":"2540","name":"枝江","en":"zhijiang"},{"id":"2541","name":"远安","en":"yuanan"},{"id":"2542","name":"兴山","en":"xingshan"},{"id":"2543","name":"秭归","en":"zigui"},{"id":"2544","name":"长阳","en":"changyang"},{"id":"2545","name":"五峰","en":"wufeng"}]},{"id":"270","name":"荆门","en":"jingmen","l3":[{"id":"2546","name":"东宝","en":"dongbao"},{"id":"2547","name":"掇刀","en":"duodao"},{"id":"2548","name":"钟祥","en":"zhongxiang"},{"id":"2549","name":"京山","en":"jingshan"},{"id":"2550","name":"沙洋","en":"shayang"}]},{"id":"271","name":"鄂州","en":"ezhou","l3":[{"id":"2551","name":"鄂城","en":"echeng"},{"id":"2552","name":"梁子湖","en":"liangzihu"},{"id":"2553","name":"华容","en":"huarong"}]},{"id":"272","name":"孝感","en":"xiaogan","l3":[{"id":"2554","name":"孝南","en":"xiaonan"},{"id":"2555","name":"应城","en":"yingcheng"},{"id":"2556","name":"安陆","en":"anlu"},{"id":"2557","name":"汉川","en":"hanchuan"},{"id":"2558","name":"孝昌","en":"xiaochang"},{"id":"2559","name":"大悟","en":"dawu"},{"id":"2560","name":"云梦","en":"yunmeng"}]},{"id":"273","name":"黄冈","en":"huanggang","l3":[{"id":"2561","name":"黄州","en":"huangzhou"},{"id":"2562","name":"麻城","en":"macheng"},{"id":"2563","name":"武穴","en":"wuxue"},{"id":"2564","name":"团风","en":"tuanfeng"},{"id":"2565","name":"红安","en":"hongan"},{"id":"2566","name":"罗田","en":"luotian"},{"id":"2567","name":"英山","en":"yingshan"},{"id":"2568","name":"浠水","en":"xishui"},{"id":"2569","name":"蕲春","en":"qichun"},{"id":"2570","name":"黄梅","en":"huangmei"}]},{"id":"274","name":"咸宁","en":"xianning","l3":[{"id":"2571","name":"咸安","en":"xianan"},{"id":"2572","name":"赤壁","en":"chibi"},{"id":"2573","name":"嘉鱼","en":"jiayu"},{"id":"2574","name":"通城","en":"tongcheng"},{"id":"2575","name":"崇阳","en":"chongyang"},{"id":"2576","name":"通山","en":"tongshan"}]},{"id":"275","name":"随州","en":"suizhou","l3":[{"id":"2577","name":"曾都","en":"zengdu"},{"id":"2578","name":"广水","en":"guangshui"}]},{"id":"276","name":"恩施州","en":"enshizhou","l3":[{"id":"2579","name":"恩施","en":"enshi"},{"id":"2580","name":"利川","en":"lichuan"},{"id":"2581","name":"建始","en":"jianshi"},{"id":"2582","name":"巴东","en":"badong"},{"id":"2583","name":"宣恩","en":"xuanen"},{"id":"2584","name":"咸丰","en":"xianfeng"},{"id":"2585","name":"来凤","en":"laifeng"},{"id":"2586","name":"鹤峰","en":"hefeng"}]}]},{"id":"24","name":"湖南","mark":"H","en":"hunan","l2":[{"id":"277","name":"长沙","en":"changsha","l3":[{"id":"2587","name":"芙蓉区","en":"furongqu"},{"id":"2588","name":"天心区","en":"tianxinqu"},{"id":"2589","name":"岳麓区","en":"yueluqu"},{"id":"2590","name":"开福区","en":"kaifuqu"},{"id":"2591","name":"雨花区","en":"yuhuaqu"},{"id":"2592","name":"浏阳","en":"liuyangshi"},{"id":"2593","name":"长沙县","en":"changshaxian"},{"id":"2594","name":"望城县","en":"wangchengxian"},{"id":"2595","name":"宁乡县","en":"ningxiangxian"}]},{"id":"278","name":"株洲","en":"zhuzhou","l3":[{"id":"2596","name":"荷塘区","en":"hetangqu"},{"id":"2597","name":"芦淞区","en":"lusongqu"},{"id":"2598","name":"石峰区","en":"shifengqu"},{"id":"2599","name":"天元区","en":"tianyuanqu"},{"id":"2600","name":"醴陵","en":"lilingshi"},{"id":"2601","name":"株洲县","en":"zhuzhouxian"},{"id":"2602","name":"攸　县","en":"you　xian"},{"id":"2603","name":"茶陵县","en":"chalingxian"},{"id":"2604","name":"炎陵县","en":"yanlingxian"}]},{"id":"279","name":"湘潭","en":"xiangtan","l3":[{"id":"2605","name":"雨湖区","en":"yuhuqu"},{"id":"2606","name":"岳塘区","en":"yuetangqu"},{"id":"2607","name":"湘乡","en":"xiangxiangshi"},{"id":"2608","name":"韶山","en":"shaoshanshi"},{"id":"2609","name":"湘潭县","en":"xiangtanxian"}]},{"id":"280","name":"衡阳","en":"hengyang","l3":[{"id":"2610","name":"珠晖区","en":"zhuhuiqu"},{"id":"2611","name":"雁峰区","en":"yanfengqu"},{"id":"2612","name":"石鼓区","en":"shiguqu"},{"id":"2613","name":"蒸湘区","en":"zhengxiangqu"},{"id":"2614","name":"南岳区","en":"nanyuequ"},{"id":"2615","name":"耒阳","en":"leiyangshi"},{"id":"2616","name":"常宁","en":"changningshi"},{"id":"2617","name":"衡阳县","en":"hengyangxian"},{"id":"2618","name":"衡南县","en":"hengnanxian"},{"id":"2619","name":"衡山县","en":"hengshanxian"},{"id":"2620","name":"衡东县","en":"hengdongxian"},{"id":"2621","name":"祁东县","en":"qidongxian"}]},{"id":"281","name":"邵阳","en":"shaoyang","l3":[{"id":"2622","name":"双清区","en":"shuangqingqu"},{"id":"2623","name":"大祥区","en":"daxiangqu"},{"id":"2624","name":"北塔区","en":"beitaqu"},{"id":"2625","name":"武冈","en":"wugangshi"},{"id":"2626","name":"邵东县","en":"shaodongxian"},{"id":"2627","name":"新邵县","en":"xinshaoxian"},{"id":"2628","name":"邵阳县","en":"shaoyangxian"},{"id":"2629","name":"隆回县","en":"longhuixian"},{"id":"2630","name":"洞口县","en":"dongkouxian"},{"id":"2631","name":"绥宁县","en":"suiningxian"},{"id":"2632","name":"新宁县","en":"xinningxian"},{"id":"2633","name":"城步自治县","en":"chengbuzizhixian"}]},{"id":"282","name":"岳阳","en":"yueyang","l3":[{"id":"2634","name":"岳阳楼","en":"yueyanglou"},{"id":"2635","name":"云溪区","en":"yunxiqu"},{"id":"2636","name":"君山区","en":"junshanqu"},{"id":"2637","name":"汨罗","en":"miluoshi"},{"id":"2638","name":"临湘","en":"linxiangshi"},{"id":"2639","name":"岳阳县","en":"yueyangxian"},{"id":"2640","name":"华容县","en":"huarongxian"},{"id":"2641","name":"湘阴县","en":"xiangyinxian"},{"id":"2642","name":"平江县","en":"pingjiangxian"}]},{"id":"283","name":"常德","en":"changde","l3":[{"id":"2643","name":"武陵区","en":"wulingqu"},{"id":"2644","name":"鼎城区","en":"dingchengqu"},{"id":"2645","name":"津市","en":"jinshishi"},{"id":"2646","name":"安乡县","en":"anxiangxian"},{"id":"2647","name":"汉寿县","en":"hanshouxian"},{"id":"2648","name":"澧　县","en":"li　xian"},{"id":"2649","name":"临澧县","en":"linlixian"},{"id":"2650","name":"桃源县","en":"taoyuanxian"},{"id":"2651","name":"石门县","en":"shimenxian"}]},{"id":"284","name":"张家界","en":"zhangjiajie","l3":[{"id":"2652","name":"永定区","en":"yongdingqu"},{"id":"2653","name":"武陵源","en":"wulingyuan"},{"id":"2654","name":"慈利县","en":"cilixian"},{"id":"2655","name":"桑植县","en":"sangzhixian"}]},{"id":"285","name":"益阳","en":"yiyang","l3":[{"id":"2656","name":"资阳区","en":"ziyangqu"},{"id":"2657","name":"赫山区","en":"heshanqu"},{"id":"2658","name":"沅江","en":"yuanjiangshi"},{"id":"2659","name":"南　县","en":"nan　xian"},{"id":"2660","name":"桃江县","en":"taojiangxian"},{"id":"2661","name":"安化县","en":"anhuaxian"}]},{"id":"286","name":"郴州","en":"chenzhou","l3":[{"id":"2662","name":"北湖区","en":"beihuqu"},{"id":"2663","name":"苏仙区","en":"suxianqu"},{"id":"2664","name":"资兴","en":"zixingshi"},{"id":"2665","name":"桂阳县","en":"guiyangxian"},{"id":"2666","name":"宜章县","en":"yizhangxian"},{"id":"2667","name":"永兴县","en":"yongxingxian"},{"id":"2668","name":"嘉禾县","en":"jiahexian"},{"id":"2669","name":"临武县","en":"linwuxian"},{"id":"2670","name":"汝城县","en":"ruchengxian"},{"id":"2671","name":"桂东县","en":"guidongxian"},{"id":"2672","name":"安仁县","en":"anrenxian"}]},{"id":"287","name":"永州","en":"yongzhou","l3":[{"id":"2673","name":"零陵区","en":"linglingqu"},{"id":"2674","name":"冷水滩","en":"lengshuitan"},{"id":"2675","name":"祁阳县","en":"qiyangxian"},{"id":"2676","name":"东安县","en":"donganxian"},{"id":"2677","name":"双牌县","en":"shuangpaixian"},{"id":"2678","name":"道　县","en":"dao　xian"},{"id":"2679","name":"江永县","en":"jiangyongxian"},{"id":"2680","name":"宁远县","en":"ningyuanxian"},{"id":"2681","name":"蓝山县","en":"lanshanxian"},{"id":"2682","name":"新田县","en":"xintianxian"},{"id":"2683","name":"江华自治县","en":"jianghuazizhixian"}]},{"id":"288","name":"怀化","en":"huaihua","l3":[{"id":"2684","name":"鹤城区","en":"hechengqu"},{"id":"2685","name":"洪江","en":"hongjiangshi"},{"id":"2686","name":"沅陵县","en":"yuanlingxian"},{"id":"2687","name":"辰溪县","en":"chenxixian"},{"id":"2688","name":"溆浦县","en":"xupuxian"},{"id":"2689","name":"中方县","en":"zhongfangxian"},{"id":"2690","name":"会同县","en":"huitongxian"},{"id":"2691","name":"麻阳自治县","en":"mayangzizhixian"},{"id":"2692","name":"新晃自治县","en":"xinhuangzizhixian"},{"id":"2693","name":"芷江自治县","en":"zhijiangzizhixian"},{"id":"2694","name":"靖州自治县","en":"jingzhouzizhixian"},{"id":"2695","name":"通道自治县","en":"tongdaozizhixian"}]},{"id":"289","name":"娄底","en":"loudi","l3":[{"id":"2696","name":"娄星区","en":"louxingqu"},{"id":"2697","name":"冷水江","en":"lengshuijiang"},{"id":"2698","name":"涟源","en":"lianyuanshi"},{"id":"2699","name":"双峰县","en":"shuangfengxian"},{"id":"2700","name":"新化县","en":"xinhuaxian"}]},{"id":"290","name":"湘西州","en":"xiangxizhou","l3":[{"id":"2701","name":"吉首","en":"jishoushi"},{"id":"2702","name":"泸溪县","en":"luxixian"},{"id":"2703","name":"凤凰县","en":"fenghuangxian"},{"id":"2704","name":"花垣县","en":"huayuanxian"},{"id":"2705","name":"保靖县","en":"baojingxian"},{"id":"2706","name":"古丈县","en":"guzhangxian"},{"id":"2707","name":"永顺县","en":"yongshunxian"},{"id":"2708","name":"龙山县","en":"longshanxian"}]}]},{"id":"14","name":"吉林","mark":"J","en":"jilin","l2":[{"id":"147","name":"长春","en":"changchun","l3":[{"id":"1502","name":"朝阳区","en":"chaoyangqu"},{"id":"1503","name":"南关区","en":"nanguanqu"},{"id":"1504","name":"宽城区","en":"kuanchengqu"},{"id":"1505","name":"二道区","en":"erdaoqu"},{"id":"1506","name":"绿园区","en":"lvyuanqu"},{"id":"1507","name":"双阳区","en":"shuangyangqu"},{"id":"1508","name":"德惠","en":"dehuishi"},{"id":"1509","name":"九台","en":"jiutaishi"},{"id":"1510","name":"榆树","en":"yushushi"},{"id":"1511","name":"农安县","en":"nonganxian"}]},{"id":"148","name":"吉林","en":"jilin","l3":[{"id":"1512","name":"船营区","en":"chuanyingqu"},{"id":"1513","name":"昌邑区","en":"changyiqu"},{"id":"1514","name":"龙潭区","en":"longtanqu"},{"id":"1515","name":"丰满区","en":"fengmanqu"},{"id":"1516","name":"蛟河","en":"jiaoheshi"},{"id":"1517","name":"桦甸","en":"huadianshi"},{"id":"1518","name":"舒兰","en":"shulanshi"},{"id":"1519","name":"磐石","en":"panshishi"},{"id":"1520","name":"永吉县","en":"yongjixian"}]},{"id":"149","name":"四平","en":"siping","l3":[{"id":"1521","name":"四平","en":"sipingshi"},{"id":"1522","name":"铁西区","en":"tiexiqu"},{"id":"1523","name":"铁东区","en":"tiedongqu"},{"id":"1524","name":"公主岭","en":"gongzhulingshi"},{"id":"1525","name":"双辽","en":"shuangliaoshi"},{"id":"1526","name":"梨树县","en":"lishuxian"},{"id":"1527","name":"伊通满族自治县","en":"yitongmanzuzizhixian"}]},{"id":"150","name":"辽源","en":"liaoyuan","l3":[{"id":"1528","name":"龙山区","en":"longshanqu"},{"id":"1529","name":"西安区","en":"xianqu"},{"id":"1530","name":"东丰县","en":"dongfengxian"},{"id":"1531","name":"东辽县","en":"dongliaoxian"}]},{"id":"151","name":"通化","en":"tonghua","l3":[{"id":"1532","name":"东昌区","en":"dongchangqu"},{"id":"1533","name":"二道江区","en":"erdaojiangqu"},{"id":"1534","name":"梅河口","en":"meihekoushi"},{"id":"1535","name":"集安","en":"jianshi"},{"id":"1536","name":"通化县","en":"tonghuaxian"},{"id":"1537","name":"辉南县","en":"huinanxian"},{"id":"1538","name":"柳河县","en":"liuhexian"}]},{"id":"152","name":"白山","en":"baishan","l3":[{"id":"1539","name":"八道江区","en":"badaojiangqu"},{"id":"1540","name":"江源区","en":"jiangyuanqu"},{"id":"1541","name":"临江","en":"linjiangshi"},{"id":"1542","name":"抚松县","en":"fusongxian"},{"id":"1543","name":"靖宇县","en":"jingyuxian"},{"id":"1544","name":"长白朝鲜族自治县","en":"changbaichaoxianzuzizhixian"}]},{"id":"154","name":"白城","en":"baicheng","l3":[{"id":"1550","name":"洮北区","en":"taobeiqu"},{"id":"1551","name":"洮南","en":"taonanshi"},{"id":"1552","name":"大安","en":"daanshi"},{"id":"1553","name":"镇赉县","en":"zhenlaixian"},{"id":"1554","name":"通榆县","en":"tongyuxian"}]},{"id":"155","name":"延边朝鲜族自治州","en":"yanbianchaoxianzuzizhizhou","l3":[{"id":"1555","name":"延吉","en":"yanjishi"},{"id":"1556","name":"图们","en":"tumenshi"},{"id":"1557","name":"敦化","en":"dunhuashi"},{"id":"1558","name":"珲春","en":"hunchunshi"},{"id":"1559","name":"龙井","en":"longjingshi"},{"id":"1560","name":"和龙","en":"helongshi"},{"id":"1561","name":"汪清县","en":"wangqingxian"},{"id":"1562","name":"安图县","en":"antuxian"}]}]},{"id":"16","name":"江苏","mark":"J","en":"jiangsu","l2":[{"id":"169","name":"南京","en":"nanjing","l3":[{"id":"1695","name":"玄武","en":"xuanwu"},{"id":"1696","name":"白下","en":"baixia"},{"id":"1697","name":"秦淮","en":"qinhuai"},{"id":"1698","name":"建邺","en":"jianye"},{"id":"1699","name":"鼓楼","en":"gulou"},{"id":"1700","name":"下关","en":"xiaguan"},{"id":"1701","name":"浦口","en":"pukou"},{"id":"1702","name":"栖霞","en":"qixia"},{"id":"1703","name":"雨花台","en":"yuhuatai"},{"id":"1704","name":"江宁","en":"jiangning"},{"id":"1705","name":"六合","en":"liuhe"},{"id":"1706","name":"溧水","en":"lishui"},{"id":"1707","name":"高淳","en":"gaochun"}]},{"id":"170","name":"无锡","en":"wuxi","l3":[{"id":"1708","name":"崇安","en":"chongan"},{"id":"1709","name":"南长","en":"nanchang"},{"id":"1710","name":"北塘","en":"beitang"},{"id":"1711","name":"滨湖","en":"binhu"},{"id":"1712","name":"锡山","en":"xishan"},{"id":"1713","name":"惠山","en":"huishan"},{"id":"1714","name":"江阴","en":"jiangyin"},{"id":"1715","name":"宜兴","en":"yixing"},{"id":"4143","name":"新区","en":"xinqu"}]},{"id":"171","name":"徐州","en":"xuzhou","l3":[{"id":"1716","name":"云龙","en":"yunlong"},{"id":"1717","name":"鼓楼","en":"gulou"},{"id":"1718","name":"九里","en":"jiuli"},{"id":"1719","name":"贾汪","en":"jiawang"},{"id":"1720","name":"泉山","en":"quanshan"},{"id":"1721","name":"新沂","en":"xinyi"},{"id":"1722","name":"邳州","en":"pizhou"},{"id":"1723","name":"丰县","en":"fengxian"},{"id":"1724","name":"沛县","en":"peixian"},{"id":"1725","name":"铜山","en":"tongshan"},{"id":"1726","name":"睢宁","en":"huining"}]},{"id":"172","name":"常州","en":"changzhou","l3":[{"id":"1727","name":"钟楼","en":"zhonglou"},{"id":"1728","name":"天宁","en":"tianning"},{"id":"1729","name":"戚墅堰","en":"qishuyan"},{"id":"1730","name":"新北","en":"xinbei"},{"id":"1731","name":"武进","en":"wujin"},{"id":"1732","name":"溧阳","en":"liyang"},{"id":"1733","name":"金坛","en":"jintan"}]},{"id":"173","name":"苏州","en":"suzhou","l3":[{"id":"1734","name":"金阊","en":"jinchang"},{"id":"1735","name":"沧浪","en":"canglang"},{"id":"1736","name":"平江","en":"pingjiang"},{"id":"1737","name":"虎丘","en":"huqiu"},{"id":"1738","name":"吴中","en":"wuzhong"},{"id":"1739","name":"相城","en":"xiangcheng"},{"id":"1740","name":"常熟","en":"changshu"},{"id":"1741","name":"张家港","en":"zhangjiagang"},{"id":"1742","name":"昆山","en":"kunshan"},{"id":"1743","name":"吴江","en":"wujiang"},{"id":"1744","name":"太仓","en":"taicang"},{"id":"4159","name":"高新区","en":"gaoxinqu"},{"id":"4160","name":"工业园区","en":"gongyeyuanqu"}]},{"id":"174","name":"南通","en":"nantong","l3":[{"id":"1745","name":"崇川","en":"chongchuan"},{"id":"1746","name":"港闸","en":"gangzha"},{"id":"1747","name":"启东","en":"qidong"},{"id":"1748","name":"如皋","en":"rugao"},{"id":"1749","name":"通州","en":"tongzhou"},{"id":"1750","name":"海门","en":"haimen"},{"id":"1751","name":"海安","en":"haian"},{"id":"1752","name":"如东","en":"rudong"}]},{"id":"175","name":"连云港","en":"lianyungang","l3":[{"id":"1753","name":"新浦","en":"xinpu"},{"id":"1754","name":"连云","en":"lianyun"},{"id":"1755","name":"海州","en":"haizhou"},{"id":"1756","name":"赣榆","en":"ganyu"},{"id":"1757","name":"东海","en":"donghai"},{"id":"1758","name":"灌云","en":"guanyun"},{"id":"1759","name":"灌南","en":"guannan"}]},{"id":"176","name":"淮安","en":"huaian","l3":[{"id":"1760","name":"清河","en":"qinghe"},{"id":"1761","name":"清浦","en":"qingpu"},{"id":"1762","name":"楚州","en":"chuzhou"},{"id":"1763","name":"淮阴","en":"huaiyin"},{"id":"1764","name":"涟水","en":"lianshui"},{"id":"1765","name":"洪泽","en":"hongze"},{"id":"1766","name":"盱眙","en":"xuyi"},{"id":"1767","name":"金湖","en":"jinhu"}]},{"id":"177","name":"盐城","en":"yancheng","l3":[{"id":"1768","name":"亭湖","en":"tinghu"},{"id":"1769","name":"盐都","en":"yandou"},{"id":"1770","name":"东台","en":"dongtai"},{"id":"1771","name":"大丰","en":"dafeng"},{"id":"1772","name":"响水","en":"xiangshui"},{"id":"1773","name":"滨海","en":"binhai"},{"id":"1774","name":"阜宁","en":"funing"},{"id":"1775","name":"射阳","en":"sheyang"},{"id":"1776","name":"建湖","en":"jianhu"}]},{"id":"178","name":"扬州","en":"yangzhou","l3":[{"id":"1777","name":"广陵","en":"guangling"},{"id":"1778","name":"邗江","en":"hanjiang"},{"id":"1779","name":"维扬区","en":"weiyangqu"},{"id":"1780","name":"仪征","en":"yizheng"},{"id":"1781","name":"高邮","en":"gaoyou"},{"id":"1782","name":"江都","en":"jiangdou"},{"id":"1783","name":"宝应","en":"baoying"}]},{"id":"179","name":"镇江","en":"zhenjiang","l3":[{"id":"1784","name":"京口","en":"jingkou"},{"id":"1785","name":"润州","en":"runzhou"},{"id":"1786","name":"丹徒","en":"dantu"},{"id":"1787","name":"丹阳","en":"danyang"},{"id":"1788","name":"扬中","en":"yangzhong"},{"id":"1789","name":"句容","en":"jurong"}]},{"id":"180","name":"泰州","en":"taizhou","l3":[{"id":"1790","name":"海陵","en":"hailing"},{"id":"1791","name":"高港","en":"gaogang"},{"id":"1792","name":"兴化","en":"xinghua"},{"id":"1793","name":"靖江","en":"jingjiang"},{"id":"1794","name":"泰兴","en":"taixing"},{"id":"1795","name":"姜堰","en":"jiangyan"}]},{"id":"181","name":"宿迁","en":"suqian","l3":[{"id":"1796","name":"宿城","en":"sucheng"},{"id":"1797","name":"宿豫","en":"suyu"},{"id":"1798","name":"沭阳","en":"shuyang"},{"id":"1799","name":"泗阳","en":"siyang"},{"id":"1800","name":"泗洪","en":"sihong"}]}]},{"id":"20","name":"江西","mark":"J","en":"jiangxi","l2":[{"id":"219","name":"南昌","en":"nanchang","l3":[{"id":"2082","name":"东湖区","en":"donghuqu"},{"id":"2083","name":"西湖区","en":"xihuqu"},{"id":"2084","name":"青云谱","en":"qingyunpu"},{"id":"2085","name":"湾里区","en":"wanliqu"},{"id":"2086","name":"青山湖","en":"qingshanhu"},{"id":"2087","name":"南昌县","en":"nanchangxian"},{"id":"2088","name":"新建县","en":"xinjianxian"},{"id":"2089","name":"安义县","en":"anyixian"},{"id":"2090","name":"进贤县","en":"jinxianxian"}]},{"id":"220","name":"景德镇","en":"jingdezhen","l3":[{"id":"2091","name":"珠山区","en":"zhushanqu"},{"id":"2092","name":"昌江区","en":"changjiangqu"},{"id":"2093","name":"乐平","en":"lepingshi"},{"id":"2094","name":"浮梁县","en":"fuliangxian"}]},{"id":"221","name":"萍乡","en":"pingxiang","l3":[{"id":"2095","name":"安源区","en":"anyuanqu"},{"id":"2096","name":"湘东区","en":"xiangdongqu"},{"id":"2097","name":"莲花县","en":"lianhuaxian"},{"id":"2098","name":"芦溪县","en":"luxixian"},{"id":"2099","name":"上栗县","en":"shanglixian"}]},{"id":"222","name":"九江","en":"jiujiang","l3":[{"id":"2100","name":"浔阳区","en":"xunyangqu"},{"id":"2101","name":"庐山区","en":"lushanqu"},{"id":"2102","name":"瑞昌","en":"ruichangshi"},{"id":"2103","name":"九江县","en":"jiujiangxian"},{"id":"2104","name":"武宁县","en":"wuningxian"},{"id":"2105","name":"修水县","en":"xiushuixian"},{"id":"2106","name":"永修县","en":"yongxiuxian"},{"id":"2107","name":"德安县","en":"deanxian"},{"id":"2108","name":"星子县","en":"xingzixian"},{"id":"2109","name":"都昌县","en":"douchangxian"},{"id":"2110","name":"湖口县","en":"hukouxian"},{"id":"2111","name":"彭泽县","en":"pengzexian"}]},{"id":"223","name":"新余","en":"xinyu","l3":[{"id":"2112","name":"渝水区","en":"yushuiqu"},{"id":"2113","name":"分宜县","en":"fenyixian"}]},{"id":"224","name":"鹰潭","en":"yingtan","l3":[{"id":"2114","name":"月湖区","en":"yuehuqu"},{"id":"2115","name":"贵溪","en":"guixishi"},{"id":"2116","name":"余江县","en":"yujiangxian"}]},{"id":"225","name":"赣州","en":"ganzhou","l3":[{"id":"2117","name":"章贡区","en":"zhanggongqu"},{"id":"2118","name":"瑞金","en":"ruijinshi"},{"id":"2119","name":"南康","en":"nankangshi"},{"id":"2120","name":"赣　县","en":"gan　xian"},{"id":"2121","name":"信丰县","en":"xinfengxian"},{"id":"2122","name":"大余县","en":"dayuxian"},{"id":"2123","name":"上犹县","en":"shangyouxian"},{"id":"2124","name":"崇义县","en":"chongyixian"},{"id":"2125","name":"安远县","en":"anyuanxian"},{"id":"2126","name":"龙南县","en":"longnanxian"},{"id":"2127","name":"定南县","en":"dingnanxian"},{"id":"2128","name":"全南县","en":"quannanxian"},{"id":"2129","name":"宁都县","en":"ningdouxian"},{"id":"2130","name":"于都县","en":"yudouxian"},{"id":"2131","name":"兴国县","en":"xingguoxian"},{"id":"2132","name":"会昌县","en":"huichangxian"},{"id":"2133","name":"寻乌县","en":"xunwuxian"},{"id":"2134","name":"石城县","en":"shichengxian"}]},{"id":"226","name":"吉安","en":"jian","l3":[{"id":"2135","name":"吉州区","en":"jizhouqu"},{"id":"2136","name":"青原区","en":"qingyuanqu"},{"id":"2137","name":"井冈山","en":"jinggangshan"},{"id":"2138","name":"吉安县","en":"jianxian"},{"id":"2139","name":"吉水县","en":"jishuixian"},{"id":"2140","name":"峡江县","en":"xiajiangxian"},{"id":"2141","name":"新干县","en":"xinganxian"},{"id":"2142","name":"永丰县","en":"yongfengxian"},{"id":"2143","name":"泰和县","en":"taihexian"},{"id":"2144","name":"遂川县","en":"suichuanxian"},{"id":"2145","name":"万安县","en":"wananxian"},{"id":"2146","name":"安福县","en":"anfuxian"},{"id":"2147","name":"永新县","en":"yongxinxian"}]},{"id":"227","name":"宜春","en":"yichun","l3":[{"id":"2148","name":"袁州区","en":"yuanzhouqu"},{"id":"2149","name":"丰城","en":"fengchengshi"},{"id":"2150","name":"樟树","en":"zhangshushi"},{"id":"2151","name":"高安","en":"gaoanshi"},{"id":"2152","name":"奉新县","en":"fengxinxian"},{"id":"2153","name":"万载县","en":"wanzaixian"},{"id":"2154","name":"上高县","en":"shanggaoxian"},{"id":"2155","name":"宜丰县","en":"yifengxian"},{"id":"2156","name":"靖安县","en":"jinganxian"},{"id":"2157","name":"铜鼓县","en":"tongguxian"},{"id":"2158","name":"袁州区","en":"yuanzhouqu"},{"id":"2159","name":"丰城","en":"fengchengshi"},{"id":"2160","name":"樟树","en":"zhangshushi"},{"id":"2161","name":"高安","en":"gaoanshi"},{"id":"2162","name":"奉新县","en":"fengxinxian"},{"id":"2163","name":"万载县","en":"wanzaixian"},{"id":"2164","name":"上高县","en":"shanggaoxian"},{"id":"2165","name":"宜丰县","en":"yifengxian"},{"id":"2166","name":"靖安县","en":"jinganxian"},{"id":"2167","name":"铜鼓县","en":"tongguxian"}]},{"id":"228","name":"抚州","en":"fz","l3":[{"id":"2168","name":"临川区","en":"linchuanqu"},{"id":"2169","name":"南城县","en":"nanchengxian"},{"id":"2170","name":"黎川县","en":"lichuanxian"},{"id":"2171","name":"南丰县","en":"nanfengxian"},{"id":"2172","name":"崇仁县","en":"chongrenxian"},{"id":"2173","name":"乐安县","en":"leanxian"},{"id":"2174","name":"宜黄县","en":"yihuangxian"},{"id":"2175","name":"金溪县","en":"jinxixian"},{"id":"2176","name":"资溪县","en":"zixixian"},{"id":"2177","name":"东乡县","en":"dongxiangxian"},{"id":"2178","name":"广昌县","en":"guangchangxian"}]},{"id":"229","name":"上饶","en":"shangrao","l3":[{"id":"2179","name":"信州区","en":"xinzhouqu"},{"id":"2180","name":"德兴","en":"dexingshi"},{"id":"2181","name":"上饶县","en":"shangraoxian"},{"id":"2182","name":"广丰县","en":"guangfengxian"},{"id":"2183","name":"玉山县","en":"yushanxian"},{"id":"2184","name":"铅山县","en":"qianshanxian"},{"id":"2185","name":"横峰县","en":"hengfengxian"},{"id":"2186","name":"弋阳县","en":"yiyangxian"},{"id":"2187","name":"余干县","en":"yuganxian"},{"id":"2188","name":"鄱阳县","en":"poyangxian"},{"id":"2189","name":"万年县","en":"wannianxian"},{"id":"2190","name":"婺源县","en":"wuyuanxian"}]}]},{"id":"13","name":"辽宁","mark":"L","en":"liaoning","l2":[{"id":"133","name":"沈阳","en":"shenyang","l3":[{"id":"1402","name":"沈河区","en":"shenhequ"},{"id":"1403","name":"和平区","en":"hepingqu"},{"id":"1404","name":"大东区","en":"dadongqu"},{"id":"1405","name":"皇姑区","en":"huangguqu"},{"id":"1406","name":"铁西区","en":"tiexiqu"},{"id":"1407","name":"苏家屯区","en":"sujiatunqu"},{"id":"1408","name":"东陵区","en":"donglingqu"},{"id":"1409","name":"沈北新区","en":"shenbeixinqu"},{"id":"1410","name":"于洪区","en":"yuhongqu"},{"id":"1411","name":"辽中县","en":"liaozhongxian"},{"id":"1412","name":"康平县","en":"kangpingxian"},{"id":"1413","name":"法库县","en":"fakuxian"},{"id":"1414","name":"新民","en":"xinminshi"}]},{"id":"134","name":"大连","en":"dalian","l3":[{"id":"1415","name":"西岗区","en":"xigangqu"},{"id":"1416","name":"中山区","en":"zhongshanqu"},{"id":"1417","name":"沙河口区","en":"shahekouqu"},{"id":"1418","name":"甘井子区","en":"ganjingziqu"},{"id":"1419","name":"旅顺口区","en":"lvshunkouqu"},{"id":"1420","name":"金州新区","en":"jinzhouxinqu"},{"id":"1421","name":"瓦房店","en":"wafangdianshi"},{"id":"1422","name":"普兰店","en":"pulandianshi"},{"id":"1423","name":"庄河","en":"zhuangheshi"},{"id":"1424","name":"长海县","en":"changhaixian"}]},{"id":"135","name":"鞍山","en":"anshan","l3":[{"id":"1425","name":"铁东区","en":"tiedongqu"},{"id":"1426","name":"铁西区","en":"tiexiqu"},{"id":"1427","name":"立山区","en":"lishanqu"},{"id":"1428","name":"千山区","en":"qianshanqu"},{"id":"1429","name":"海城","en":"haichengshi"},{"id":"1430","name":"台安县","en":"taianxian"},{"id":"1431","name":"岫岩满族自治县","en":"xiuyanmanzuzizhixian"},{"id":"4132","name":"高新区","en":"gaoxinqu"}]},{"id":"136","name":"抚顺","en":"fushun","l3":[{"id":"1432","name":"顺城区","en":"shunchengqu"},{"id":"1433","name":"新抚区","en":"xinfuqu"},{"id":"1434","name":"东洲区","en":"dongzhouqu"},{"id":"1435","name":"望花区","en":"wanghuaqu"},{"id":"1436","name":"抚顺县","en":"fushunxian"},{"id":"1437","name":"新宾满族自治县","en":"xinbinmanzuzizhixian"},{"id":"1438","name":"清原满族自治县","en":"qingyuanmanzuzizhixian"}]},{"id":"137","name":"本溪","en":"benxi","l3":[{"id":"1439","name":"平山区","en":"pingshanqu"},{"id":"1440","name":"溪湖区","en":"xihuqu"},{"id":"1441","name":"明山区","en":"mingshanqu"},{"id":"1442","name":"南芬区","en":"nanfenqu"},{"id":"1443","name":"本溪满族自治县","en":"benximanzuzizhixian"},{"id":"1444","name":"桓仁满族自治县","en":"huanrenmanzuzizhixian"}]},{"id":"138","name":"丹东","en":"dandong","l3":[{"id":"1445","name":"振兴区","en":"zhenxingqu"},{"id":"1446","name":"元宝区","en":"yuanbaoqu"},{"id":"1447","name":"振安区","en":"zhenanqu"},{"id":"1448","name":"东港","en":"donggangshi"},{"id":"1449","name":"凤城","en":"fengchengshi"},{"id":"1450","name":"宽甸满族自治县","en":"kuandianmanzuzizhixian"}]},{"id":"139","name":"锦州","en":"jinzhou","l3":[{"id":"1451","name":"太和区","en":"taihequ"},{"id":"1452","name":"古塔区","en":"gutaqu"},{"id":"1453","name":"凌河区","en":"linghequ"},{"id":"1454","name":"凌海","en":"linghaishi"},{"id":"1455","name":"北镇","en":"beizhenshi"},{"id":"1456","name":"黑山县","en":"heishanxian"},{"id":"1457","name":"义县","en":"yixian"},{"id":"4135","name":"开发区","en":"kaifaqu"},{"id":"4136","name":"松山新区","en":"songshanxinqu"},{"id":"4137","name":"龙栖湾开发新区","en":"longqiwankaifaxinqu"}]},{"id":"140","name":"营口","en":"yingkou","l3":[{"id":"1458","name":"站前区","en":"zhanqianqu"},{"id":"1459","name":"西市区","en":"xishiqu"},{"id":"1460","name":"鲅鱼圈区","en":"bayuquanqu"},{"id":"1461","name":"老边区","en":"laobianqu"},{"id":"1462","name":"盖州","en":"gaizhoushi"},{"id":"1463","name":"大石桥","en":"dashiqiaoshi"},{"id":"4133","name":"开发区","en":"kaifaqu"},{"id":"4134","name":"高新区","en":"gaoxinqu"}]},{"id":"141","name":"阜新","en":"fuxin","l3":[{"id":"1464","name":"海州区","en":"haizhouqu"},{"id":"1465","name":"新邱区","en":"xinqiuqu"},{"id":"1466","name":"太平区","en":"taipingqu"},{"id":"1467","name":"清河门区","en":"qinghemenqu"},{"id":"1468","name":"细河区","en":"xihequ"},{"id":"1469","name":"阜新蒙古族自治县","en":"fuxinmengguzuzizhixian"},{"id":"1470","name":"彰武县","en":"zhangwuxian"}]},{"id":"142","name":"辽阳","en":"liaoyang","l3":[{"id":"1471","name":"白塔区","en":"baitaqu"},{"id":"1472","name":"文圣区","en":"wenshengqu"},{"id":"1473","name":"宏伟区","en":"hongweiqu"},{"id":"1474","name":"弓长岭区","en":"gongchanglingqu"},{"id":"1475","name":"太子河区","en":"taizihequ"},{"id":"1476","name":"灯塔","en":"dengtashi"},{"id":"1477","name":"辽阳县","en":"liaoyangxian"}]},{"id":"143","name":"盘锦","en":"panjin","l3":[{"id":"1478","name":"兴隆台区","en":"xinglongtaiqu"},{"id":"1479","name":"双台子区","en":"shuangtaiziqu"},{"id":"1480","name":"大洼县","en":"dawaxian"},{"id":"1481","name":"盘山县","en":"panshanxian"}]},{"id":"144","name":"铁岭","en":"tieling","l3":[{"id":"1482","name":"银州区","en":"yinzhouqu"},{"id":"1483","name":"清河区","en":"qinghequ"},{"id":"1484","name":"调兵山","en":"tiaobingshanshi"},{"id":"1485","name":"开原","en":"kaiyuanshi"},{"id":"1486","name":"铁岭县","en":"tielingxian"},{"id":"1487","name":"西丰县","en":"xifengxian"},{"id":"1488","name":"昌图县","en":"changtuxian"}]},{"id":"145","name":"朝阳","en":"chaoyang","l3":[{"id":"1489","name":"双塔区","en":"shuangtaqu"},{"id":"1490","name":"龙城区","en":"longchengqu"},{"id":"1491","name":"北票","en":"beipiaoshi"},{"id":"1492","name":"凌源","en":"lingyuanshi"},{"id":"1493","name":"朝阳县","en":"chaoyangxian"},{"id":"1494","name":"建平县","en":"jianpingxian"},{"id":"1495","name":"喀喇沁左翼蒙古族自治","en":"kalaqinzuoyimengguzuzizhi"}]},{"id":"146","name":"葫芦岛","en":"huludao","l3":[{"id":"1496","name":"龙港区","en":"longgangqu"},{"id":"1497","name":"连山区","en":"lianshanqu"},{"id":"1498","name":"南票区","en":"nanpiaoqu"},{"id":"1499","name":"兴城","en":"xingchengshi"},{"id":"1500","name":"绥中县","en":"suizhongxian"},{"id":"1501","name":"建昌县","en":"jianchangxian"}]}]},{"id":"39","name":"内蒙古自治区","mark":"N","en":"neimengguzizhiqu","l2":[{"id":"416","name":"呼和浩特","en":"huhehaote","l3":[{"id":"3749","name":"回民区","en":"huiminqu"},{"id":"3750","name":"新城区","en":"xinchengqu"},{"id":"3751","name":"玉泉区","en":"yuquanqu"},{"id":"3752","name":"赛罕区","en":"saihanqu"},{"id":"3753","name":"土默特左旗","en":"tumotezuoqi"},{"id":"3754","name":"托克托县","en":"tuoketuoxian"},{"id":"3755","name":"和林格尔县","en":"helingeerxian"},{"id":"3756","name":"清水河县","en":"qingshuihexian"},{"id":"3757","name":"武川县","en":"wuchuanxian"}]},{"id":"417","name":"包头","en":"baotou","l3":[{"id":"3758","name":"昆都仑区","en":"kundoulunqu"},{"id":"3759","name":"东河区","en":"donghequ"},{"id":"3760","name":"青山区","en":"qingshanqu"},{"id":"3761","name":"石拐区","en":"shiguaiqu"},{"id":"3762","name":"白云矿区","en":"baiyunkuangqu"},{"id":"3763","name":"九原区","en":"jiuyuanqu"},{"id":"3764","name":"土默特右旗","en":"tumoteyouqi"},{"id":"3765","name":"固阳县","en":"guyangxian"},{"id":"3766","name":"达尔罕茂明安联合旗","en":"daerhanmaominganlianheqi"}]},{"id":"418","name":"乌海","en":"wuhai","l3":[{"id":"3767","name":"海勃湾区","en":"haibowanqu"},{"id":"3768","name":"海南区","en":"hainanqu"},{"id":"3769","name":"乌达区","en":"wudaqu"}]},{"id":"419","name":"赤峰","en":"chifeng","l3":[{"id":"3770","name":"红山区","en":"hongshanqu"},{"id":"3771","name":"元宝山区","en":"yuanbaoshanqu"},{"id":"3772","name":"松山区","en":"songshanqu"},{"id":"3773","name":"阿鲁科尔沁旗","en":"alukeerqinqi"},{"id":"3774","name":"巴林左旗","en":"balinzuoqi"},{"id":"3775","name":"巴林右旗","en":"balinyouqi"},{"id":"3776","name":"林西县","en":"linxixian"},{"id":"3777","name":"克什克腾旗","en":"keshenketengqi"},{"id":"3778","name":"翁牛特旗","en":"wengniuteqi"},{"id":"3779","name":"喀喇沁旗","en":"kalaqinqi"},{"id":"3780","name":"宁城县","en":"ningchengxian"},{"id":"3781","name":"敖汉旗","en":"aohanqi"}]},{"id":"420","name":"通辽","en":"tongliao","l3":[{"id":"3782","name":"科尔沁区","en":"keerqinqu"},{"id":"3783","name":"霍林郭勒","en":"huolinguoleshi"},{"id":"3784","name":"科尔沁左翼中旗","en":"keerqinzuoyizhongqi"},{"id":"3785","name":"科尔沁左翼后旗","en":"keerqinzuoyihouqi"},{"id":"3786","name":"开鲁县","en":"kailuxian"},{"id":"3787","name":"库伦旗","en":"kulunqi"},{"id":"3788","name":"奈曼旗","en":"naimanqi"},{"id":"3789","name":"扎鲁特旗","en":"zaluteqi"}]},{"id":"421","name":"鄂尔多斯","en":"eerduosi","l3":[{"id":"3790","name":"东胜区","en":"dongshengqu"},{"id":"3791","name":"达拉特旗","en":"dalateqi"},{"id":"3792","name":"准格尔旗","en":"zhungeerqi"},{"id":"3793","name":"鄂托克前旗","en":"etuokeqianqi"},{"id":"3794","name":"鄂托克旗","en":"etuokeqi"},{"id":"3795","name":"杭锦旗","en":"hangjinqi"},{"id":"3796","name":"乌审旗","en":"wushenqi"},{"id":"3797","name":"伊金霍洛旗","en":"yijinhuoluoqi"}]},{"id":"422","name":"呼伦贝尔","en":"hulunbeier","l3":[{"id":"3798","name":"海拉尔","en":"hailaer"},{"id":"3799","name":"满洲里","en":"manzhouli"},{"id":"3800","name":"牙克石","en":"yakeshi"},{"id":"3801","name":"扎兰屯","en":"zalantun"},{"id":"3802","name":"额尔古纳","en":"eerguna"},{"id":"3803","name":"根河","en":"genhe"},{"id":"3804","name":"阿荣旗","en":"arongqi"},{"id":"3805","name":"鄂伦春自治旗","en":"elunchunzizhiqi"},{"id":"3806","name":"鄂温克族自治旗","en":"ewenkezuzizhiqi"},{"id":"3807","name":"陈巴尔虎旗","en":"chenbaerhuqi"},{"id":"3808","name":"新巴尔虎左旗","en":"xinbaerhuzuoqi"},{"id":"3809","name":"新巴尔虎右旗","en":"xinbaerhuyouqi"}]},{"id":"423","name":"巴彦淖尔","en":"bayannaoer","l3":[{"id":"3810","name":"临河区","en":"linhequ"},{"id":"3811","name":"五原县","en":"wuyuanxian"},{"id":"3812","name":"磴口县","en":"dengkouxian"},{"id":"3813","name":"乌拉特前旗","en":"wulɑteqianqi"},{"id":"3814","name":"乌拉特中旗","en":"wulɑtezhongqi"},{"id":"3815","name":"乌拉特后旗","en":"wulɑtehouqi"},{"id":"3816","name":"杭锦后旗","en":"hangjinhouqi"}]},{"id":"424","name":"乌兰察布","en":"wulanchabu","l3":[{"id":"3817","name":"集宁区","en":"jiningqu"},{"id":"3818","name":"丰镇","en":"fengzhenshi"},{"id":"3819","name":"卓资县","en":"zhuozixian"},{"id":"3820","name":"化德县","en":"huadexian"},{"id":"3821","name":"商都县","en":"shangdouxian"},{"id":"3822","name":"兴和县","en":"xinghexian"},{"id":"3823","name":"凉城县","en":"liangchengxian"},{"id":"3824","name":"察哈尔右翼前旗","en":"chahaeryouyiqianqi"},{"id":"3825","name":"察哈尔右翼中旗","en":"chahaeryouyizhongqi"},{"id":"3826","name":"察哈尔右翼后旗","en":"chahaeryouyihouqi"},{"id":"3827","name":"四子王旗","en":"siziwangqi"}]},{"id":"425","name":"兴安盟","en":"xinganmeng","l3":[{"id":"3828","name":"乌兰浩特","en":"wulanhaoteshi"},{"id":"3829","name":"阿尔山","en":"aershanshi"},{"id":"3830","name":"科尔沁右翼前旗","en":"keerqinyouyiqianqi"},{"id":"3831","name":"科尔沁右翼中旗","en":"keerqinyouyizhongqi"},{"id":"3832","name":"扎赉特旗","en":"zalaiteqi"},{"id":"3833","name":"突泉县","en":"tuquanxian"}]},{"id":"426","name":"锡林郭勒盟","en":"xilinguolemeng","l3":[{"id":"3834","name":"二连浩特","en":"erlianhaote"},{"id":"3835","name":"锡林浩特","en":"xilinhaote"},{"id":"3836","name":"阿巴嘎旗","en":"abagaqi"},{"id":"3837","name":"苏尼特左旗","en":"sunitezuoqi"},{"id":"3838","name":"苏尼特右旗","en":"suniteyouqi"},{"id":"3839","name":"东乌珠穆沁旗","en":"dongwuzhumuqinqi"},{"id":"3840","name":"西乌珠穆沁旗","en":"xiwuzhumuqinqi"},{"id":"3841","name":"太仆寺旗","en":"taipusiqi"},{"id":"3842","name":"镶黄旗","en":"xianghuangqi"},{"id":"3843","name":"正镶白旗","en":"zhengxiangbaiqi"},{"id":"3844","name":"正蓝旗","en":"zhenglanqi"},{"id":"3845","name":"多伦","en":"duolun"}]},{"id":"427","name":"阿拉善盟","en":"alashanmeng","l3":[{"id":"3846","name":"阿拉善盟","en":"alashanmeng"},{"id":"3847","name":"阿拉善左旗","en":"alashanzuoqi"},{"id":"3848","name":"阿拉善右旗","en":"alashanyouqi"},{"id":"3849","name":"额济纳旗","en":"ejinaqi"}]}]},{"id":"41","name":"宁夏回族自治区","mark":"N","en":"ningxiahuizuzizhiqu","l2":[{"id":"435","name":"银川","en":"yinchuan","l3":[{"id":"3924","name":"兴庆区","en":"xingqingqu"},{"id":"3925","name":"金凤区","en":"jinfengqu"},{"id":"3926","name":"西夏区","en":"xixiaqu"},{"id":"3927","name":"永宁县","en":"yongningxian"},{"id":"3928","name":"贺兰县","en":"helanxian"},{"id":"3929","name":"灵武","en":"lingwushi"}]},{"id":"436","name":"石嘴山","en":"shizuishan","l3":[{"id":"3930","name":"大武口区","en":"dawukouqu"},{"id":"3931","name":"惠农区","en":"huinongqu"},{"id":"3932","name":"平罗县","en":"pingluoxian"}]},{"id":"437","name":"吴忠","en":"wuzhong","l3":[{"id":"3933","name":"利通区","en":"litongqu"},{"id":"3934","name":"盐池县","en":"yanchixian"},{"id":"3935","name":"同心县","en":"tongxinxian"},{"id":"3936","name":"青铜峡","en":"qingtongxiashi"}]},{"id":"438","name":"固原","en":"guyuan","l3":[{"id":"3937","name":"原州区","en":"yuanzhouqu"},{"id":"3938","name":"西吉县","en":"xijixian"},{"id":"3939","name":"隆德县","en":"longdexian"},{"id":"3940","name":"泾源县","en":"jingyuanxian"},{"id":"3941","name":"彭阳县","en":"pengyangxian"}]},{"id":"439","name":"中卫","en":"zhongwei","l3":[{"id":"3942","name":"沙坡头区","en":"shapotouqu"},{"id":"3943","name":"中宁县","en":"zhongningxian"},{"id":"3944","name":"海原县","en":"haiyuanxian"}]}]},{"id":"32","name":"青海","mark":"Q","en":"qinghai","l2":[{"id":"382","name":"西宁","en":"xining","l3":[{"id":"3433","name":"城东区","en":"chengdongqu"},{"id":"3434","name":"城中区","en":"chengzhongqu"},{"id":"3435","name":"城西区","en":"chengxiqu"},{"id":"3436","name":"城北区","en":"chengbeiqu"},{"id":"3437","name":"湟中县","en":"huangzhongxian"},{"id":"3438","name":"湟源县","en":"huangyuanxian"},{"id":"3439","name":"大通回族土族自治县","en":"datonghuizutuzuzizhixian"}]},{"id":"383","name":"海东地区","en":"haidongdiqu","l3":[{"id":"3440","name":"城东区","en":"chengdongqu"},{"id":"3441","name":"城中区","en":"chengzhongqu"},{"id":"3442","name":"城西区","en":"chengxiqu"},{"id":"3443","name":"城北区","en":"chengbeiqu"},{"id":"3444","name":"湟中县","en":"huangzhongxian"},{"id":"3445","name":"湟源县","en":"huangyuanxian"},{"id":"3446","name":"大通回族土族自治县","en":"datonghuizutuzuzizhixian"}]},{"id":"384","name":"海北州","en":"haibeizhou","l3":[{"id":"3447","name":"海晏县","en":"haiyanxian"},{"id":"3448","name":"祁连县","en":"qilianxian"},{"id":"3449","name":"刚察县","en":"gangchaxian"},{"id":"3450","name":"门源回族自治县","en":"menyuanhuizuzizhixian"}]},{"id":"385","name":"黄南州","en":"huangnanzhou","l3":[{"id":"3451","name":"同仁县","en":"tongrenxian"},{"id":"3452","name":"尖扎县","en":"jianzaxian"},{"id":"3453","name":"泽库县","en":"zekuxian"},{"id":"3454","name":"河南蒙古族自治县","en":"henanmengguzuzizhixian"}]},{"id":"386","name":"海南州","en":"hainanzhou","l3":[{"id":"3455","name":"共和县","en":"gonghexian"},{"id":"3456","name":"同德县","en":"tongdexian"},{"id":"3457","name":"贵德县","en":"guidexian"},{"id":"3458","name":"兴海县","en":"xinghaixian"},{"id":"3459","name":"贵南县","en":"guinanxian"}]},{"id":"387","name":"果洛州","en":"guoluozhou","l3":[{"id":"3460","name":"玛沁县","en":"maqinxian"},{"id":"3461","name":"班玛县","en":"banmaxian"},{"id":"3462","name":"甘德县","en":"gandexian"},{"id":"3463","name":"达日县","en":"darixian"},{"id":"3464","name":"久治县","en":"jiuzhixian"},{"id":"3465","name":"玛多县","en":"maduoxian"}]},{"id":"388","name":"玉树州","en":"yushuzhou","l3":[{"id":"3466","name":"玉树县","en":"yushuxian"},{"id":"3467","name":"杂多县","en":"zaduoxian"},{"id":"3468","name":"称多县","en":"chengduoxian"},{"id":"3469","name":"治多县","en":"zhiduoxian"},{"id":"3470","name":"囊谦县","en":"nangqianxian"},{"id":"3471","name":"曲麻莱县","en":"qumalaixian"}]},{"id":"389","name":"海西州","en":"haixizhou","l3":[{"id":"3472","name":"德令哈","en":"delinghashi"},{"id":"3473","name":"格尔木","en":"geermushi"},{"id":"3474","name":"乌兰县","en":"wulanxian"},{"id":"3475","name":"都兰县","en":"doulanxian"},{"id":"3476","name":"天峻县","en":"tianjunxian"},{"id":"3477","name":"冷湖行委","en":"lenghuxingwei"},{"id":"3478","name":"大柴旦行委","en":"dachaidanxingwei"},{"id":"3479","name":"茫崖行委","en":"mangyaxingwei"}]}]},{"id":"21","name":"山东","mark":"S","en":"shandong","l2":[{"id":"230","name":"济南","en":"jinan","l3":[{"id":"2191","name":"历下区","en":"lixiaqu"},{"id":"2192","name":"中区","en":"shizhongqu"},{"id":"2193","name":"槐荫区","en":"huaiyinqu"},{"id":"2194","name":"天桥区","en":"tianqiaoqu"},{"id":"2195","name":"历城区","en":"lichengqu"},{"id":"2196","name":"长清区","en":"changqingqu"},{"id":"2197","name":"章丘","en":"zhangqiushi"},{"id":"2198","name":"平阴县","en":"pingyinxian"},{"id":"2199","name":"济阳县","en":"jiyangxian"},{"id":"2200","name":"商河县","en":"shanghexian"}]},{"id":"231","name":"青岛","en":"qingdao","l3":[{"id":"2201","name":"南区","en":"shinanqu"},{"id":"2202","name":"北区","en":"shibeiqu"},{"id":"2203","name":"四方区","en":"sifangqu"},{"id":"2204","name":"黄岛区","en":"huangdaoqu"},{"id":"2205","name":"崂山区","en":"laoshanqu"},{"id":"2206","name":"李沧区","en":"licangqu"},{"id":"2207","name":"城阳区","en":"chengyangqu"},{"id":"2208","name":"胶州","en":"jiaozhoushi"},{"id":"2209","name":"即墨","en":"jimoshi"},{"id":"2210","name":"平度","en":"pingdushi"},{"id":"2211","name":"胶南","en":"jiaonanshi"},{"id":"2212","name":"莱西","en":"laixishi"}]},{"id":"232","name":"淄博","en":"zibo","l3":[{"id":"2213","name":"张店区","en":"zhangdianqu"},{"id":"2214","name":"淄川区","en":"zichuanqu"},{"id":"2215","name":"博山区","en":"boshanqu"},{"id":"2216","name":"临淄区","en":"linziqu"},{"id":"2217","name":"周村区","en":"zhoucunqu"},{"id":"2218","name":"桓台县","en":"huantaixian"},{"id":"2219","name":"高青县","en":"gaoqingxian"},{"id":"2220","name":"沂源县","en":"yiyuanxian"}]},{"id":"233","name":"枣庄","en":"zaozhuang","l3":[{"id":"2221","name":"市中区","en":"shizhongqu"},{"id":"2222","name":"薛城区","en":"xuechengqu"},{"id":"2223","name":"峄城区","en":"yichengqu"},{"id":"2224","name":"台儿庄区","en":"taierzhuangqu"},{"id":"2225","name":"山亭区","en":"shantingqu"},{"id":"2226","name":"滕州","en":"tengzhoushi"}]},{"id":"234","name":"东营","en":"dongying","l3":[{"id":"2227","name":"东营区","en":"dongyingqu"},{"id":"2228","name":"河口区","en":"hekouqu"},{"id":"2229","name":"垦利县","en":"kenlixian"},{"id":"2230","name":"利津县","en":"lijinxian"},{"id":"2231","name":"广饶县","en":"guangraoxian"},{"id":"4142","name":"经济开发区","en":"jingjikaifaqu"}]},{"id":"235","name":"烟台","en":"yantai","l3":[{"id":"2232","name":"芝罘区","en":"zhifuqu"},{"id":"2233","name":"福山区","en":"fushanqu"},{"id":"2234","name":"牟平区","en":"moupingqu"},{"id":"2235","name":"莱山区","en":"laishanqu"},{"id":"2236","name":"龙口","en":"longkoushi"},{"id":"2237","name":"莱阳","en":"laiyangshi"},{"id":"2238","name":"莱州","en":"laizhoushi"},{"id":"2239","name":"蓬莱","en":"penglaishi"},{"id":"2240","name":"招远","en":"zhaoyuanshi"},{"id":"2241","name":"栖霞","en":"qixiashi"},{"id":"2242","name":"海阳","en":"haiyangshi"},{"id":"2243","name":"长岛县","en":"changdaoxian"},{"id":"4138","name":"开发区","en":"kaifaqu"}]},{"id":"236","name":"潍坊","en":"weifang","l3":[{"id":"2244","name":"潍城区","en":"weichengqu"},{"id":"2245","name":"寒亭区","en":"hantingqu"},{"id":"2246","name":"坊子区","en":"fangziqu"},{"id":"2247","name":"奎文区","en":"kuiwenqu"},{"id":"2248","name":"青州","en":"qingzhoushi"},{"id":"2249","name":"诸城","en":"zhuchengshi"},{"id":"2250","name":"寿光","en":"shouguangshi"},{"id":"2251","name":"安丘","en":"anqiushi"},{"id":"2252","name":"高密","en":"gaomishi"},{"id":"2253","name":"昌邑","en":"changyishi"},{"id":"2254","name":"临朐县","en":"linquxian"},{"id":"2255","name":"昌乐县","en":"changlexian"},{"id":"4139","name":"滨海开发区","en":"binhaikaifaqu"}]},{"id":"237","name":"威海","en":"weihai","l3":[{"id":"2256","name":"环翠区","en":"huancuiqu"},{"id":"2257","name":"文登","en":"wendengshi"},{"id":"2258","name":"荣成","en":"rongchengshi"},{"id":"2259","name":"乳山","en":"rushanshi"},{"id":"4140","name":"经区","en":"jingqu"},{"id":"4141","name":"高区","en":"gaoqu"}]},{"id":"238","name":"济宁","en":"jining","l3":[{"id":"2260","name":"中区","en":"shizhongqu"},{"id":"2261","name":"任城区","en":"renchengqu"},{"id":"2262","name":"曲阜","en":"qufushi"},{"id":"2263","name":"兖州","en":"yanzhoushi"},{"id":"2264","name":"邹城","en":"zouchengshi"},{"id":"2265","name":"微山县","en":"weishanxian"},{"id":"2266","name":"鱼台县","en":"yutaixian"},{"id":"2267","name":"金乡县","en":"jinxiangxian"},{"id":"2268","name":"嘉祥县","en":"jiaxiangxian"},{"id":"2269","name":"汶上县","en":"wenshangxian"},{"id":"2270","name":"泗水县","en":"sishuixian"},{"id":"2271","name":"梁山县","en":"liangshanxian"}]},{"id":"239","name":"泰安","en":"taian","l3":[{"id":"2272","name":"泰山区","en":"taishanqu"},{"id":"2273","name":"岱岳区","en":"daiyuequ"},{"id":"2274","name":"新泰","en":"xintaishi"},{"id":"2275","name":"肥城","en":"feichengshi"},{"id":"2276","name":"宁阳县","en":"ningyangxian"},{"id":"2277","name":"东平县","en":"dongpingxian"}]},{"id":"240","name":"日照","en":"rizhao","l3":[{"id":"2278","name":"东港区","en":"donggangqu"},{"id":"2279","name":"岚山区","en":"lanshanqu"},{"id":"2280","name":"五莲县","en":"wulianxian"},{"id":"2281","name":"莒　县","en":"ju　xian"}]},{"id":"241","name":"莱芜","en":"laiwu","l3":[{"id":"2282","name":"莱城区","en":"laichengqu"},{"id":"2283","name":"钢城区","en":"gangchengqu"}]},{"id":"242","name":"临沂","en":"linyi","l3":[{"id":"2284","name":"兰山区","en":"lanshanqu"},{"id":"2285","name":"罗庄区","en":"luozhuangqu"},{"id":"2286","name":"河东区","en":"hedongqu"},{"id":"2287","name":"沂南县","en":"yinanxian"},{"id":"2288","name":"郯城县","en":"tanchengxian"},{"id":"2289","name":"沂水县","en":"yishuixian"},{"id":"2290","name":"苍山县","en":"cangshanxian"},{"id":"2291","name":"费　县","en":"fei　xian"},{"id":"2292","name":"平邑县","en":"pingyixian"},{"id":"2293","name":"莒南县","en":"junanxian"},{"id":"2294","name":"蒙阴县","en":"mengyinxian"},{"id":"2295","name":"临沭县","en":"linshuxian"}]},{"id":"243","name":"德州","en":"dezhou","l3":[{"id":"2296","name":"德城区","en":"dechengqu"},{"id":"2297","name":"乐陵","en":"lelingshi"},{"id":"2298","name":"禹城","en":"yuchengshi"},{"id":"2299","name":"陵　县","en":"ling　xian"},{"id":"2300","name":"宁津县","en":"ningjinxian"},{"id":"2301","name":"庆云县","en":"qingyunxian"},{"id":"2302","name":"临邑县","en":"linyixian"},{"id":"2303","name":"齐河县","en":"qihexian"},{"id":"2304","name":"平原县","en":"pingyuanxian"},{"id":"2305","name":"夏津县","en":"xiajinxian"},{"id":"2306","name":"武城县","en":"wuchengxian"}]},{"id":"244","name":"聊城","en":"liaocheng","l3":[{"id":"2307","name":"东昌府区","en":"dongchangfuqu"},{"id":"2308","name":"临清","en":"linqingshi"},{"id":"2309","name":"阳谷县","en":"yangguxian"},{"id":"2310","name":"莘　县","en":"shen　xian"},{"id":"2311","name":"茌平县","en":"chipingxian"},{"id":"2312","name":"东阿县","en":"dongexian"},{"id":"2313","name":"冠　县","en":"guan　xian"},{"id":"2314","name":"高唐县","en":"gaotangxian"}]},{"id":"245","name":"滨州","en":"binzhou","l3":[{"id":"2315","name":"滨城区","en":"binchengqu"},{"id":"2316","name":"惠民县","en":"huiminxian"},{"id":"2317","name":"阳信县","en":"yangxinxian"},{"id":"2318","name":"无棣县","en":"wudixian"},{"id":"2319","name":"沾化县","en":"zhanhuaxian"},{"id":"2320","name":"博兴县","en":"boxingxian"},{"id":"2321","name":"邹平县","en":"zoupingxian"}]},{"id":"246","name":"菏泽","en":"heze","l3":[{"id":"2322","name":"牡丹区","en":"mudanqu"},{"id":"2323","name":"曹　县","en":"cao　xian"},{"id":"2324","name":"单　县","en":"dan　xian"},{"id":"2325","name":"成武县","en":"chengwuxian"},{"id":"2326","name":"巨野县","en":"juyexian"},{"id":"2327","name":"郓城县","en":"yunchengxian"},{"id":"2328","name":"鄄城县","en":"juanchengxian"},{"id":"2329","name":"定陶县","en":"dingtaoxian"},{"id":"2330","name":"东明县","en":"dongmingxian"}]}]},{"id":"30","name":"陕西","mark":"S","en":"shanxi","l2":[{"id":"358","name":"西安","en":"xian","l3":[{"id":"3239","name":"未央区","en":"weiyangqu"},{"id":"3240","name":"新城区","en":"xinchengqu"},{"id":"3241","name":"碑林区","en":"beilinqu"},{"id":"3242","name":"莲湖区","en":"lianhuqu"},{"id":"3243","name":"灞桥区","en":"baqiaoqu"},{"id":"3244","name":"雁塔区","en":"yantaqu"},{"id":"3245","name":"阎良区","en":"yanliangqu"},{"id":"3246","name":"临潼区","en":"lintongqu"},{"id":"3247","name":"长安区","en":"changanqu"},{"id":"3248","name":"蓝田县","en":"lantianxian"},{"id":"3249","name":"周至县","en":"zhouzhixian"},{"id":"3250","name":"户　县","en":"hu　xian"},{"id":"3251","name":"高陵县","en":"gaolingxian"}]},{"id":"359","name":"铜川","en":"tongchuan","l3":[{"id":"3252","name":"耀州区","en":"yaozhouqu"},{"id":"3253","name":"王益区","en":"wangyiqu"},{"id":"3254","name":"印台区","en":"yintaiqu"},{"id":"3255","name":"宜君县","en":"yijunxian"}]},{"id":"360","name":"宝鸡","en":"baoji","l3":[{"id":"3256","name":"渭滨区","en":"weibinqu"},{"id":"3257","name":"金台区","en":"jintaiqu"},{"id":"3258","name":"陈仓区","en":"chencangqu"},{"id":"3259","name":"凤翔县","en":"fengxiangxian"},{"id":"3260","name":"岐山县","en":"qishanxian"},{"id":"3261","name":"扶风县","en":"fufengxian"},{"id":"3262","name":"眉　县","en":"mei　xian"},{"id":"3263","name":"陇　县","en":"long　xian"},{"id":"3264","name":"千阳县","en":"qianyangxian"},{"id":"3265","name":"麟游县","en":"linyouxian"},{"id":"3266","name":"凤　县","en":"feng　xian"},{"id":"3267","name":"太白县","en":"taibaixian"}]},{"id":"361","name":"咸阳","en":"xianyang","l3":[{"id":"3268","name":"秦都区","en":"qindouqu"},{"id":"3269","name":"杨陵区","en":"yanglingqu"},{"id":"3270","name":"渭城区","en":"weichengqu"},{"id":"3271","name":"兴平","en":"xingpingshi"},{"id":"3272","name":"三原县","en":"sanyuanxian"},{"id":"3273","name":"泾阳县","en":"jingyangxian"},{"id":"3274","name":"乾　县","en":"gan　xian"},{"id":"3275","name":"礼泉县","en":"liquanxian"},{"id":"3276","name":"永寿县","en":"yongshouxian"},{"id":"3277","name":"彬　县","en":"bin　xian"},{"id":"3278","name":"长武县","en":"changwuxian"},{"id":"3279","name":"旬邑县","en":"xunyixian"},{"id":"3280","name":"淳化县","en":"chunhuaxian"},{"id":"3281","name":"武功县","en":"wugongxian"}]},{"id":"362","name":"渭南","en":"weinan","l3":[{"id":"3282","name":"临渭区","en":"linweiqu"},{"id":"3283","name":"韩城","en":"hanchengshi"},{"id":"3284","name":"华阴","en":"huayinshi"},{"id":"3285","name":"华　县","en":"hua　xian"},{"id":"3286","name":"潼关县","en":"tongguanxian"},{"id":"3287","name":"大荔县","en":"dalixian"},{"id":"3288","name":"合阳县","en":"heyangxian"},{"id":"3289","name":"澄城县","en":"chengchengxian"},{"id":"3290","name":"蒲城县","en":"puchengxian"},{"id":"3291","name":"白水县","en":"baishuixian"},{"id":"3292","name":"富平县","en":"fupingxian"}]},{"id":"363","name":"延安","en":"yanan","l3":[{"id":"3293","name":"宝塔区","en":"baotaqu"},{"id":"3294","name":"延长县","en":"yanchangxian"},{"id":"3295","name":"延川县","en":"yanchuanxian"},{"id":"3296","name":"子长县","en":"zichangxian"},{"id":"3297","name":"安塞县","en":"ansaixian"},{"id":"3298","name":"志丹县","en":"zhidanxian"},{"id":"3299","name":"吴起县","en":"wuqixian"},{"id":"3300","name":"甘泉县","en":"ganquanxian"},{"id":"3301","name":"富　县","en":"fu　xian"},{"id":"3302","name":"洛川县","en":"luochuanxian"},{"id":"3303","name":"宜川县","en":"yichuanxian"},{"id":"3304","name":"黄龙县","en":"huanglongxian"},{"id":"3305","name":"黄陵县","en":"huanglingxian"}]},{"id":"364","name":"汉中","en":"hanzhong","l3":[{"id":"3306","name":"汉台区","en":"hantaiqu"},{"id":"3307","name":"南郑县","en":"nanzhengxian"},{"id":"3308","name":"城固县","en":"chengguxian"},{"id":"3309","name":"洋　县","en":"yang　xian"},{"id":"3310","name":"西乡县","en":"xixiangxian"},{"id":"3311","name":"勉　县","en":"mian　xian"},{"id":"3312","name":"宁强县","en":"ningqiangxian"},{"id":"3313","name":"略阳县","en":"lveyangxian"},{"id":"3314","name":"镇巴县","en":"zhenbaxian"},{"id":"3315","name":"留坝县","en":"liubaxian"},{"id":"3316","name":"佛坪县","en":"fopingxian"}]},{"id":"365","name":"榆林","en":"yulin","l3":[{"id":"3317","name":"榆阳区","en":"yuyangqu"},{"id":"3318","name":"神木县","en":"shenmuxian"},{"id":"3319","name":"府谷县","en":"fuguxian"},{"id":"3320","name":"横山县","en":"hengshanxian"},{"id":"3321","name":"靖边县","en":"jingbianxian"},{"id":"3322","name":"定边县","en":"dingbianxian"},{"id":"3323","name":"绥德县","en":"suidexian"},{"id":"3324","name":"米脂县","en":"mizhixian"},{"id":"3325","name":"佳　县","en":"jia　xian"},{"id":"3326","name":"吴堡县","en":"wubuxian"},{"id":"3327","name":"清涧县","en":"qingjianxian"},{"id":"3328","name":"子洲县","en":"zizhouxian"}]},{"id":"366","name":"安康","en":"ankang","l3":[{"id":"3329","name":"汉滨区","en":"hanbinqu"},{"id":"3330","name":"汉阴县","en":"hanyinxian"},{"id":"3331","name":"石泉县","en":"shiquanxian"},{"id":"3332","name":"宁陕县","en":"ningshanxian"},{"id":"3333","name":"紫阳县","en":"ziyangxian"},{"id":"3334","name":"岚皋县","en":"langaoxian"},{"id":"3335","name":"平利县","en":"pinglixian"},{"id":"3336","name":"镇坪县","en":"zhenpingxian"},{"id":"3337","name":"旬阳县","en":"xunyangxian"},{"id":"3338","name":"白河县","en":"baihexian"}]},{"id":"367","name":"商洛","en":"shangluo","l3":[{"id":"3339","name":"商州区","en":"shangzhouqu"},{"id":"3340","name":"洛南县","en":"luonanxian"},{"id":"3341","name":"丹凤县","en":"danfengxian"},{"id":"3342","name":"商南县","en":"shangnanxian"},{"id":"3343","name":"山阳县","en":"shanyangxian"},{"id":"3344","name":"镇安县","en":"zhenanxian"},{"id":"3345","name":"柞水县","en":"zhashuixian"}]}]},{"id":"12","name":"山西","mark":"S","en":"shanxi","l2":[{"id":"122","name":"太原","en":"taiyuan","l3":[{"id":"1283","name":"小店区","en":"xiaodianqu"},{"id":"1284","name":"迎泽区","en":"yingzequ"},{"id":"1285","name":"杏花岭区","en":"xinghualingqu"},{"id":"1286","name":"尖草坪区","en":"jiancaopingqu"},{"id":"1287","name":"万柏林区","en":"wanbolinqu"},{"id":"1288","name":"晋源区","en":"jinyuanqu"},{"id":"1289","name":"清徐县","en":"qingxuxian"},{"id":"1290","name":"阳曲县","en":"yangquxian"},{"id":"1291","name":"娄烦县","en":"loufanxian"},{"id":"1292","name":"古交","en":"gujiaoshi"}]},{"id":"123","name":"大同","en":"datong","l3":[{"id":"1293","name":"城　区","en":"cheng　qu"},{"id":"1294","name":"矿　区","en":"kuang　qu"},{"id":"1295","name":"南郊区","en":"nanjiaoqu"},{"id":"1296","name":"新荣区","en":"xinrongqu"},{"id":"1297","name":"阳高县","en":"yanggaoxian"},{"id":"1298","name":"天镇县","en":"tianzhenxian"},{"id":"1299","name":"广灵县","en":"guanglingxian"},{"id":"1300","name":"灵丘县","en":"lingqiuxian"},{"id":"1301","name":"浑源县","en":"hunyuanxian"},{"id":"1302","name":"左云县","en":"zuoyunxian"},{"id":"1303","name":"大同县","en":"datongxian"}]},{"id":"124","name":"阳泉","en":"yangquan","l3":[{"id":"1304","name":"城　区","en":"cheng　qu"},{"id":"1305","name":"矿　区","en":"kuang　qu"},{"id":"1306","name":"郊　区","en":"jiao　qu"},{"id":"1307","name":"平定县","en":"pingdingxian"},{"id":"1308","name":"盂　县","en":"yu　xian"}]},{"id":"125","name":"长治","en":"changzhi","l3":[{"id":"1309","name":"城　区","en":"cheng　qu"},{"id":"1310","name":"郊　区","en":"jiao　qu"},{"id":"1311","name":"长治县","en":"changzhixian"},{"id":"1312","name":"襄垣县","en":"xiangyuanxian"},{"id":"1313","name":"屯留县","en":"tunliuxian"},{"id":"1314","name":"平顺县","en":"pingshunxian"},{"id":"1315","name":"黎城县","en":"lichengxian"},{"id":"1316","name":"壶关县","en":"huguanxian"},{"id":"1317","name":"长子县","en":"changzixian"},{"id":"1318","name":"武乡县","en":"wuxiangxian"},{"id":"1319","name":"沁　县","en":"qin　xian"},{"id":"1320","name":"沁源县","en":"qinyuanxian"},{"id":"1321","name":"潞城","en":"luchengshi"}]},{"id":"126","name":"晋城","en":"jincheng","l3":[{"id":"1322","name":"城　区","en":"cheng　qu"},{"id":"1323","name":"沁水县","en":"qinshuixian"},{"id":"1324","name":"阳城县","en":"yangchengxian"},{"id":"1325","name":"陵川县","en":"lingchuanxian"},{"id":"1326","name":"泽州县","en":"zezhouxian"},{"id":"1327","name":"高平","en":"gaopingshi"}]},{"id":"127","name":"朔州","en":"shuozhou","l3":[{"id":"1328","name":"朔城区","en":"shuochengqu"},{"id":"1329","name":"平鲁区","en":"pingluqu"},{"id":"1330","name":"山阴县","en":"shanyinxian"},{"id":"1331","name":"应　县","en":"ying　xian"},{"id":"1332","name":"右玉县","en":"youyuxian"},{"id":"1333","name":"怀仁县","en":"huairenxian"}]},{"id":"128","name":"晋中","en":"jinzhong","l3":[{"id":"1334","name":"榆次区","en":"yuciqu"},{"id":"1335","name":"榆社县","en":"yushexian"},{"id":"1336","name":"左权县","en":"zuoquanxian"},{"id":"1337","name":"和顺县","en":"heshunxian"},{"id":"1338","name":"昔阳县","en":"xiyangxian"},{"id":"1339","name":"寿阳县","en":"shouyangxian"},{"id":"1340","name":"太谷县","en":"taiguxian"},{"id":"1341","name":"祁　县","en":"qi　xian"},{"id":"1342","name":"平遥县","en":"pingyaoxian"},{"id":"1343","name":"灵石县","en":"lingshixian"},{"id":"1344","name":"介休","en":"jiexiushi"}]},{"id":"129","name":"运城","en":"yuncheng","l3":[{"id":"1345","name":"盐湖区","en":"yanhuqu"},{"id":"1346","name":"临猗县","en":"linyixian"},{"id":"1347","name":"万荣县","en":"wanrongxian"},{"id":"1348","name":"闻喜县","en":"wenxixian"},{"id":"1349","name":"稷山县","en":"jishanxian"},{"id":"1350","name":"新绛县","en":"xinjiangxian"},{"id":"1351","name":"绛　县","en":"jiang　xian"},{"id":"1352","name":"垣曲县","en":"yuanquxian"},{"id":"1353","name":"夏　县","en":"xia　xian"},{"id":"1354","name":"平陆县","en":"pingluxian"},{"id":"1355","name":"芮城县","en":"ruichengxian"},{"id":"1356","name":"永济","en":"yongjishi"},{"id":"1357","name":"河津","en":"hejinshi"}]},{"id":"130","name":"忻州","en":"xinzhou","l3":[{"id":"1358","name":"忻府区","en":"xinfuqu"},{"id":"1359","name":"定襄县","en":"dingxiangxian"},{"id":"1360","name":"五台县","en":"wutaixian"},{"id":"1361","name":"代　县","en":"dai　xian"},{"id":"1362","name":"繁峙县","en":"fanzhixian"},{"id":"1363","name":"宁武县","en":"ningwuxian"},{"id":"1364","name":"静乐县","en":"jinglexian"},{"id":"1365","name":"神池县","en":"shenchixian"},{"id":"1366","name":"五寨县","en":"wuzhaixian"},{"id":"1367","name":"岢岚县","en":"kelanxian"},{"id":"1368","name":"河曲县","en":"hequxian"},{"id":"1369","name":"保德县","en":"baodexian"},{"id":"1370","name":"偏关县","en":"pianguanxian"},{"id":"1371","name":"原平","en":"yuanpingshi"}]},{"id":"131","name":"临汾","en":"linfen","l3":[{"id":"1372","name":"尧都区","en":"yaodouqu"},{"id":"1373","name":"曲沃县","en":"quwoxian"},{"id":"1374","name":"翼城县","en":"yichengxian"},{"id":"1375","name":"襄汾县","en":"xiangfenxian"},{"id":"1376","name":"洪洞县","en":"hongdongxian"},{"id":"1377","name":"古　县","en":"gu　xian"},{"id":"1378","name":"安泽县","en":"anzexian"},{"id":"1379","name":"浮山县","en":"fushanxian"},{"id":"1380","name":"吉　县","en":"ji　xian"},{"id":"1381","name":"乡宁县","en":"xiangningxian"},{"id":"1382","name":"大宁县","en":"daningxian"},{"id":"1383","name":"隰　县","en":"xi　xian"},{"id":"1384","name":"永和县","en":"yonghexian"},{"id":"1385","name":"蒲　县","en":"pu　xian"},{"id":"1386","name":"汾西县","en":"fenxixian"},{"id":"1387","name":"侯马","en":"houmashi"},{"id":"1388","name":"霍州","en":"huozhoushi"}]},{"id":"132","name":"吕梁","en":"lvliang","l3":[{"id":"1389","name":"离石区","en":"lishiqu"},{"id":"1390","name":"文水县","en":"wenshuixian"},{"id":"1391","name":"交城县","en":"jiaochengxian"},{"id":"1392","name":"兴　县","en":"xing　xian"},{"id":"1393","name":"临　县","en":"lin　xian"},{"id":"1394","name":"柳林县","en":"liulinxian"},{"id":"1395","name":"石楼县","en":"shilouxian"},{"id":"1396","name":"岚　县","en":"lan　xian"},{"id":"1397","name":"方山县","en":"fangshanxian"},{"id":"1398","name":"中阳县","en":"zhongyangxian"},{"id":"1399","name":"交口县","en":"jiaokouxian"},{"id":"1400","name":"孝义","en":"xiaoyishi"},{"id":"1401","name":"汾阳","en":"fenyangshi"}]}]},{"id":"36","name":"上海","mark":"S","en":"shanghai","l2":[{"id":"400","name":"上海","en":"shanghai","l3":[{"id":"3581","name":"黄浦区","en":"huangpuqu"},{"id":"3582","name":"卢湾区","en":"luwanqu"},{"id":"3583","name":"徐汇区","en":"xuhuiqu"},{"id":"3584","name":"长宁区","en":"changningqu"},{"id":"3585","name":"静安区","en":"jinganqu"},{"id":"3586","name":"普陀区","en":"putuoqu"},{"id":"3587","name":"闸北区","en":"zhabeiqu"},{"id":"3588","name":"虹口区","en":"hongkouqu"},{"id":"3589","name":"杨浦区","en":"yangpuqu"},{"id":"3590","name":"宝山区","en":"baoshanqu"},{"id":"3591","name":"闵行区","en":"minxingqu"},{"id":"3592","name":"嘉定区","en":"jiadingqu"},{"id":"3593","name":"浦东新区","en":"pudongxinqu"},{"id":"3594","name":"金山区","en":"jinshanqu"},{"id":"3595","name":"松江区","en":"songjiangqu"},{"id":"3596","name":"青浦区","en":"qingpuqu"},{"id":"3597","name":"南汇区","en":"nanhuiqu"},{"id":"3598","name":"奉贤区","en":"fengxianqu"},{"id":"3599","name":"崇明县","en":"chongmingxian"}]}]},{"id":"27","name":"四川","mark":"S","en":"sichuan","l2":[{"id":"312","name":"成都","en":"chengdu","l3":[{"id":"2841","name":"锦江","en":"jinjiang"},{"id":"2842","name":"青羊","en":"qingyang"},{"id":"2843","name":"金牛","en":"jinniu"},{"id":"2844","name":"武侯","en":"wuhou"},{"id":"2845","name":"成华","en":"chenghua"},{"id":"2846","name":"龙泉驿","en":"longquanyi"},{"id":"2847","name":"青白江","en":"qingbaijiang"},{"id":"2848","name":"新都","en":"xindou"},{"id":"2849","name":"温江区","en":"wenjiangqu"},{"id":"2850","name":"都江堰","en":"doujiangyan"},{"id":"2851","name":"彭州","en":"pengzhou"},{"id":"2852","name":"邛崃","en":"qionglai"},{"id":"2853","name":"崇州","en":"chongzhoushi"},{"id":"2854","name":"金堂","en":"jintang"},{"id":"2855","name":"双流","en":"shuangliu"},{"id":"2856","name":"郫县","en":"pixian"},{"id":"2857","name":"大邑","en":"dayi"},{"id":"2858","name":"蒲江","en":"pujiang"},{"id":"2859","name":"新津县","en":"xinjinxian"},{"id":"4130","name":"高新区","en":"gaoxinqu"}]},{"id":"313","name":"自贡","en":"zigong","l3":[{"id":"2860","name":"自流井","en":"ziliujing"},{"id":"2861","name":"贡井区","en":"gongjingqu"},{"id":"2862","name":"大安区","en":"daanqu"},{"id":"2863","name":"沿滩区","en":"yantanqu"},{"id":"2864","name":"荣　县","en":"rong　xian"},{"id":"2865","name":"富顺县","en":"fushunxian"}]},{"id":"314","name":"攀枝花","en":"panzhihua","l3":[{"id":"2866","name":"东　区","en":"dong　qu"},{"id":"2867","name":"西　区","en":"xi　qu"},{"id":"2868","name":"仁和区","en":"renhequ"},{"id":"2869","name":"米易县","en":"miyixian"},{"id":"2870","name":"盐边县","en":"yanbianxian"}]},{"id":"315","name":"泸州","en":"luzhou","l3":[{"id":"2871","name":"江阳区","en":"jiangyangqu"},{"id":"2872","name":"纳溪区","en":"naxiqu"},{"id":"2873","name":"龙马潭","en":"longmatan"},{"id":"2874","name":"泸　县","en":"lu　xian"},{"id":"2875","name":"合江县","en":"hejiangxian"},{"id":"2876","name":"叙永县","en":"xuyongxian"},{"id":"2877","name":"古蔺县","en":"gulinxian"}]},{"id":"316","name":"德阳","en":"deyang","l3":[{"id":"2878","name":"旌阳区","en":"jingyangqu"},{"id":"2879","name":"广汉","en":"guanghanshi"},{"id":"2880","name":"什邡","en":"shenfangshi"},{"id":"2881","name":"绵竹","en":"mianzhushi"},{"id":"2882","name":"罗江县","en":"luojiangxian"},{"id":"2883","name":"中江县","en":"zhongjiangxian"}]},{"id":"317","name":"绵阳","en":"mianyang","l3":[{"id":"2884","name":"涪城区","en":"fuchengqu"},{"id":"2885","name":"游仙区","en":"youxianqu"},{"id":"2886","name":"江油","en":"jiangyoushi"},{"id":"2887","name":"三台县","en":"santaixian"},{"id":"2888","name":"盐亭县","en":"yantingxian"},{"id":"2889","name":"安　县","en":"an　xian"},{"id":"2890","name":"梓潼县","en":"zitongxian"},{"id":"2891","name":"平武县","en":"pingwuxian"},{"id":"2892","name":"北川羌族自治县","en":"beichuanqiangzuzizhixian"}]},{"id":"318","name":"广元","en":"guangyuan","l3":[{"id":"2893","name":"利州区","en":"lizhouqu"},{"id":"2894","name":"元坝区","en":"yuanbaqu"},{"id":"2895","name":"朝天区","en":"chaotianqu"},{"id":"2896","name":"旺苍县","en":"wangcangxian"},{"id":"2897","name":"青川县","en":"qingchuanxian"},{"id":"2898","name":"剑阁县","en":"jiangexian"},{"id":"2899","name":"苍溪县","en":"cangxixian"}]},{"id":"319","name":"遂宁","en":"suining","l3":[{"id":"2900","name":"船山区","en":"chuanshanqu"},{"id":"2901","name":"安居区","en":"anjuqu"},{"id":"2902","name":"蓬溪县","en":"pengxixian"},{"id":"2903","name":"射洪县","en":"shehongxian"},{"id":"2904","name":"大英县","en":"dayingxian"}]},{"id":"320","name":"内江","en":"neijiang","l3":[{"id":"2905","name":"中区","en":"shizhongqu"},{"id":"2906","name":"东兴区","en":"dongxingqu"},{"id":"2907","name":"威远县","en":"weiyuanxian"},{"id":"2908","name":"资中县","en":"zizhongxian"},{"id":"2909","name":"隆昌县","en":"longchangxian"}]},{"id":"321","name":"乐山","en":"leshan","l3":[{"id":"2910","name":"中区","en":"shizhongqu"},{"id":"2911","name":"沙湾区","en":"shawanqu"},{"id":"2912","name":"五通桥","en":"wutongqiao"},{"id":"2913","name":"金口河","en":"jinkouhe"},{"id":"2914","name":"峨眉山","en":"emeishan"},{"id":"2915","name":"犍为县","en":"jianweixian"},{"id":"2916","name":"井研县","en":"jingyanxian"},{"id":"2917","name":"夹江县","en":"jiajiangxian"},{"id":"2918","name":"沐川县","en":"muchuanxian"},{"id":"2919","name":"峨边彝族自治县","en":"ebianyizuzizhixian"},{"id":"2920","name":"马边彝族自治县","en":"mabianyizuzizhixian"}]},{"id":"322","name":"南充","en":"nanchong","l3":[{"id":"2921","name":"顺庆区","en":"shunqingqu"},{"id":"2922","name":"高坪区","en":"gaopingqu"},{"id":"2923","name":"嘉陵区","en":"jialingqu"},{"id":"2924","name":"阆中","en":"langzhongshi"},{"id":"2925","name":"南部县","en":"nanbuxian"},{"id":"2926","name":"营山县","en":"yingshanxian"},{"id":"2927","name":"蓬安县","en":"penganxian"},{"id":"2928","name":"仪陇县","en":"yilongxian"},{"id":"2929","name":"西充县","en":"xichongxian"}]},{"id":"323","name":"宜宾","en":"yibin","l3":[{"id":"2930","name":"翠屏区","en":"cuipingqu"},{"id":"2931","name":"宜宾县","en":"yibinxian"},{"id":"2932","name":"南溪县","en":"nanxixian"},{"id":"2933","name":"江安县","en":"jianganxian"},{"id":"2934","name":"长宁县","en":"changningxian"},{"id":"2935","name":"高　县","en":"gao　xian"},{"id":"2936","name":"珙　县","en":"gong　xian"},{"id":"2937","name":"筠连县","en":"yunlianxian"},{"id":"2938","name":"兴文县","en":"xingwenxian"},{"id":"2939","name":"屏山县","en":"pingshanxian"}]},{"id":"324","name":"广安","en":"guangan","l3":[{"id":"2940","name":"广安区","en":"guanganqu"},{"id":"2941","name":"华蓥","en":"huayingshi"},{"id":"2942","name":"岳池县","en":"yuechixian"},{"id":"2943","name":"武胜县","en":"wushengxian"},{"id":"2944","name":"邻水县","en":"linshuixian"}]},{"id":"325","name":"达州","en":"dazhou","l3":[{"id":"2945","name":"通川区","en":"tongchuanqu"},{"id":"2946","name":"万源","en":"wanyuanshi"},{"id":"2947","name":"达　县","en":"da　xian"},{"id":"2948","name":"宣汉县","en":"xuanhanxian"},{"id":"2949","name":"开江县","en":"kaijiangxian"},{"id":"2950","name":"大竹县","en":"dazhuxian"},{"id":"2951","name":"渠　县","en":"qu　xian"}]},{"id":"326","name":"眉山","en":"meishan","l3":[{"id":"2952","name":"东坡区","en":"dongpoqu"},{"id":"2953","name":"仁寿县","en":"renshouxian"},{"id":"2954","name":"彭山县","en":"pengshanxian"},{"id":"2955","name":"洪雅县","en":"hongyaxian"},{"id":"2956","name":"丹棱县","en":"danlengxian"},{"id":"2957","name":"青神县","en":"qingshenxian"}]},{"id":"327","name":"雅安","en":"yaan","l3":[{"id":"2958","name":"雨城区","en":"yuchengqu"},{"id":"2959","name":"名山县","en":"mingshanxian"},{"id":"2960","name":"荥经县","en":"xingjingxian"},{"id":"2961","name":"汉源县","en":"hanyuanxian"},{"id":"2962","name":"石棉县","en":"shimianxian"},{"id":"2963","name":"天全县","en":"tianquanxian"},{"id":"2964","name":"芦山县","en":"lushanxian"},{"id":"2965","name":"宝兴县","en":"baoxingxian"}]},{"id":"328","name":"巴中","en":"bazhong","l3":[{"id":"2966","name":"巴州区","en":"bazhouqu"},{"id":"2967","name":"通江县","en":"tongjiangxian"},{"id":"2968","name":"南江县","en":"nanjiangxian"},{"id":"2969","name":"平昌县","en":"pingchangxian"}]},{"id":"329","name":"资阳","en":"ziyang","l3":[{"id":"2970","name":"雁江区","en":"yanjiangqu"},{"id":"2971","name":"简阳","en":"jianyangshi"},{"id":"2972","name":"安岳县","en":"anyuexian"},{"id":"2973","name":"乐至县","en":"lezhixian"}]},{"id":"330","name":"阿坝州","en":"abazhou","l3":[{"id":"2974","name":"马尔康","en":"maerkang"},{"id":"2975","name":"汶川县","en":"wenchuanxian"},{"id":"2976","name":"理　县","en":"li　xian"},{"id":"2977","name":"茂　县","en":"mao　xian"},{"id":"2978","name":"松潘县","en":"songpanxian"},{"id":"2979","name":"九寨沟县","en":"jiuzhaigouxian"},{"id":"2980","name":"金川县","en":"jinchuanxian"},{"id":"2981","name":"小金县","en":"xiaojinxian"},{"id":"2982","name":"黑水县","en":"heishuixian"},{"id":"2983","name":"壤塘县","en":"rangtangxian"},{"id":"2984","name":"阿坝县","en":"abaxian"},{"id":"2985","name":"若尔盖县","en":"ruoergaixian"},{"id":"2986","name":"红原县","en":"hongyuanxian"}]},{"id":"331","name":"甘孜州","en":"ganzizhou","l3":[{"id":"2987","name":"康定县","en":"kangdingxian"},{"id":"2988","name":"泸定县","en":"ludingxian"},{"id":"2989","name":"丹巴","en":"danba"},{"id":"2990","name":"九龙","en":"jiulong"},{"id":"2991","name":"雅江","en":"yajiang"},{"id":"2992","name":"道孚","en":"daofu"},{"id":"2993","name":"炉霍","en":"luhuo"},{"id":"2994","name":"甘孜","en":"ganzi"},{"id":"2995","name":"新龙","en":"xinlong"},{"id":"2996","name":"德格","en":"dege"},{"id":"2997","name":"白玉","en":"baiyu"},{"id":"2998","name":"石渠","en":"shiqu"},{"id":"2999","name":"色达","en":"seda"},{"id":"3000","name":"理塘","en":"litang"},{"id":"3001","name":"巴塘","en":"batang"},{"id":"3002","name":"乡城","en":"xiangcheng"},{"id":"3003","name":"稻城","en":"daocheng"},{"id":"3004","name":"得荣","en":"derong"}]},{"id":"332","name":"凉山州","en":"liangshanzhou","l3":[{"id":"3005","name":"西昌","en":"xichangshi"},{"id":"3006","name":"盐源县","en":"yanyuanxian"},{"id":"3007","name":"德昌县","en":"dechangxian"},{"id":"3008","name":"会理县","en":"huilixian"},{"id":"3009","name":"会东","en":"huidong"},{"id":"3010","name":"宁南","en":"ningnan"},{"id":"3011","name":"普格","en":"puge"},{"id":"3012","name":"布拖","en":"butuo"},{"id":"3013","name":"金阳","en":"jinyang"},{"id":"3014","name":"昭觉","en":"zhaojue"},{"id":"3015","name":"喜德","en":"xide"},{"id":"3016","name":"冕宁","en":"mianning"},{"id":"3017","name":"越西","en":"yuexi"},{"id":"3018","name":"甘洛","en":"ganluo"},{"id":"3019","name":"美姑","en":"meigu"},{"id":"3020","name":"雷波","en":"leibo"},{"id":"3021","name":"木里自治县","en":"mulizizhixian"}]}]},{"id":"33","name":"台湾","mark":"T","en":"taiwan","l2":[{"id":"390","name":"台北","en":"taibei","l3":[{"id":"3480","name":"中正区","en":"zhongzhengqu"},{"id":"3481","name":"大同区","en":"datongqu"},{"id":"3482","name":"中山区","en":"zhongshanqu"},{"id":"3483","name":"松山区","en":"songshanqu"},{"id":"3484","name":"大安区","en":"daanqu"},{"id":"3485","name":"万华区","en":"wanghuaqu"},{"id":"3486","name":"信义区","en":"xinyiqu"},{"id":"3487","name":"士林区","en":"shilinqu"},{"id":"3488","name":"北投区","en":"beitouqu"},{"id":"3489","name":"内湖区","en":"neihuqu"},{"id":"3490","name":"南港区","en":"nangangqu"},{"id":"3491","name":"文山区","en":"wenshanqu"}]},{"id":"391","name":"高雄","en":"gaoxiong","l3":[{"id":"3492","name":"新兴区","en":"xinxingqu"},{"id":"3493","name":"前金区","en":"qianjingqu"},{"id":"3494","name":"芩雅区","en":"qinyaqu"},{"id":"3495","name":"盐埕区","en":"yanchengqu"},{"id":"3496","name":"鼓山区","en":"gushanqu"},{"id":"3497","name":"旗津区","en":"qijinqu"},{"id":"3498","name":"前镇区","en":"qianzhenqu"},{"id":"3499","name":"三民区","en":"sanminqu"},{"id":"3500","name":"左营区","en":"zuoyingqu"},{"id":"3501","name":"楠梓区","en":"nanziqu"},{"id":"3502","name":"小港区","en":"xiaogangqu"}]},{"id":"392","name":"基隆","en":"jilong","l3":[{"id":"3503","name":"仁爱区","en":"renaiqu"},{"id":"3504","name":"信义区","en":"xinyiqu"},{"id":"3505","name":"中正区","en":"zhongzhengqu"},{"id":"3506","name":"中山区","en":"zhongshanqu"},{"id":"3507","name":"安乐区","en":"anlequ"},{"id":"3508","name":"暖暖区","en":"nuannuanqu"},{"id":"3509","name":"七堵区","en":"qiduqu"}]},{"id":"393","name":"台中","en":"taizhong","l3":[{"id":"3510","name":"中　区","en":"zhong qu"},{"id":"3511","name":"东　区","en":"dong qu"},{"id":"3512","name":"南　区","en":"nan qu"},{"id":"3513","name":"西　区","en":"xi qu"},{"id":"3514","name":"北　区","en":"bei qu"},{"id":"3515","name":"北屯区","en":"beitunqu"},{"id":"3516","name":"西屯区","en":"xitunqu"},{"id":"3517","name":"南屯区","en":"nantunqu"}]},{"id":"394","name":"台南","en":"tainan","l3":[{"id":"3518","name":"中西区","en":"zhongxiqu"},{"id":"3519","name":"东　区","en":"dong qu"},{"id":"3520","name":"南　区","en":"nan qu"},{"id":"3521","name":"北　区","en":"bei qu"},{"id":"3522","name":"安平区","en":"anpingqu"},{"id":"3523","name":"安南区","en":"annanqu"}]},{"id":"395","name":"新竹","en":"xinzhu","l3":[{"id":"3524","name":"东　区","en":"dong qu"},{"id":"3525","name":"北　区","en":"bei qu"},{"id":"3526","name":"香山区","en":"xiangshanqu"}]},{"id":"396","name":"嘉义","en":"jiayi","l3":[{"id":"3527","name":"东　区","en":"dong qu"},{"id":"3528","name":"西　区","en":"xi qu"}]},{"id":"397","name":"县","en":"xian","l3":[{"id":"3529","name":"台北县(板桥市)","en":"taibeixian(banqiaoshi)"},{"id":"3530","name":"宜兰县(宜兰市)","en":"yilanxian(yilanshi)"},{"id":"3531","name":"新竹县(竹北市)","en":"xinzhuxian(zhubeishi)"},{"id":"3532","name":"桃园县(桃园市)","en":"taoyuanxian(taoyuanshi)"},{"id":"3533","name":"苗栗县(苗栗市)","en":"miaolixian(miaolishi)"},{"id":"3534","name":"台中县(丰原市)","en":"taizhongxian(fengyuanshi)"},{"id":"3535","name":"彰化县(彰化市)","en":"zhanghuaxian(zhanghuashi)"},{"id":"3536","name":"南投县(南投市)","en":"nantouxian(nantoushi)"},{"id":"3537","name":"嘉义县(太保市)","en":"jiayixian(taibaoshi)"},{"id":"3538","name":"云林县(斗六市)","en":"yunlinxian(douliushi)"},{"id":"3539","name":"台南县(新营市)","en":"tainanxian(xinyingshi)"},{"id":"3540","name":"高雄县(凤山市)","en":"gaoxiongxian(fengshanshi)"},{"id":"3541","name":"屏东县(屏东市)","en":"pingdongxian(pingdongshi)"},{"id":"3542","name":"台东县(台东市)","en":"taidongxian(taidongshi)"},{"id":"3543","name":"花莲县(花莲市)","en":"hualianxian(hualianshi)"},{"id":"3544","name":"澎湖县(马公市)","en":"penghuxian(magongshi)"}]}]},{"id":"35","name":"天津","mark":"T","en":"tianjin","l2":[{"id":"399","name":"天津","en":"tianjin","l3":[{"id":"3563","name":"和平区","en":"hepingqu"},{"id":"3564","name":"河东区","en":"hedongqu"},{"id":"3565","name":"河西区","en":"hexiqu"},{"id":"3566","name":"南开区","en":"nankaiqu"},{"id":"3567","name":"河北区","en":"hebeiqu"},{"id":"3568","name":"红桥区","en":"hongqiaoqu"},{"id":"3572","name":"东丽区","en":"dongliqu"},{"id":"3573","name":"西青区","en":"xiqingqu"},{"id":"3574","name":"津南区","en":"jinnanqu"},{"id":"3575","name":"北辰区","en":"beichenqu"},{"id":"3576","name":"武清区","en":"wuqingqu"},{"id":"3577","name":"宝坻区","en":"baodiqu"},{"id":"3578","name":"宁河县","en":"ninghexian"},{"id":"3579","name":"静海县","en":"jinghaixian"},{"id":"3580","name":"蓟　县","en":"ji　xian"},{"id":"4129","name":"滨海新区","en":"binhaixinqu"},{"id":"4162","name":"汉沽区","en":"hanguqu"}]}]},{"id":"40","name":"西藏自治区","mark":"X","en":"xicangzizhiqu","l2":[{"id":"428","name":"拉萨","en":"lasa","l3":[{"id":"3850","name":"城关区","en":"chengguanqu"},{"id":"3851","name":"林周县","en":"linzhouxian"},{"id":"3852","name":"当雄县","en":"dangxiongxian"},{"id":"3853","name":"尼木县","en":"nimuxian"},{"id":"3854","name":"曲水县","en":"qushuixian"},{"id":"3855","name":"堆龙德庆县","en":"duilongdeqingxian"},{"id":"3856","name":"达孜县","en":"dazixian"},{"id":"3857","name":"墨竹工卡县","en":"mozhugongkaxian"}]},{"id":"429","name":"昌都地区","en":"changdudiqu","l3":[{"id":"3858","name":"昌都县","en":"changdouxian"},{"id":"3859","name":"江达县","en":"jiangdaxian"},{"id":"3860","name":"贡觉县","en":"gongjuexian"},{"id":"3861","name":"类乌齐县","en":"leiwuqixian"},{"id":"3862","name":"丁青县","en":"dingqingxian"},{"id":"3863","name":"察雅县","en":"chayaxian"},{"id":"3864","name":"八宿县","en":"basuxian"},{"id":"3865","name":"左贡县","en":"zuogongxian"},{"id":"3866","name":"芒康县","en":"mangkangxian"},{"id":"3867","name":"洛隆县","en":"luolongxian"},{"id":"3868","name":"边坝县","en":"bianbaxian"}]},{"id":"430","name":"山南地区","en":"shannandiqu","l3":[{"id":"3869","name":"乃东县","en":"naidongxian"},{"id":"3870","name":"扎囊县","en":"zanangxian"},{"id":"3871","name":"贡嘎县","en":"gonggaxian"},{"id":"3872","name":"桑日县","en":"sangrixian"},{"id":"3873","name":"琼结县","en":"qiongjiexian"},{"id":"3874","name":"曲松县","en":"qusongxian"},{"id":"3875","name":"措美县","en":"cuomeixian"},{"id":"3876","name":"洛扎县","en":"luozaxian"},{"id":"3877","name":"加查县","en":"jiachaxian"},{"id":"3878","name":"隆子县","en":"longzixian"},{"id":"3879","name":"错那县","en":"cuonaxian"},{"id":"3880","name":"浪卡子县","en":"langqiazixian"}]},{"id":"431","name":"日喀则地区","en":"rikazediqu","l3":[{"id":"3881","name":"日喀则","en":"rikazeshi"},{"id":"3882","name":"南木林县","en":"nanmulinxian"},{"id":"3883","name":"江孜县","en":"jiangzixian"},{"id":"3884","name":"定日县","en":"dingrixian"},{"id":"3885","name":"萨迦县","en":"sajiaxian"},{"id":"3886","name":"拉孜县","en":"lazixian"},{"id":"3887","name":"昂仁县","en":"angrenxian"},{"id":"3888","name":"谢通门县","en":"xietongmenxian"},{"id":"3889","name":"白朗县","en":"bailangxian"},{"id":"3890","name":"仁布县","en":"renbuxian"},{"id":"3891","name":"康马县","en":"kangmaxian"},{"id":"3892","name":"定结县","en":"dingjiexian"},{"id":"3893","name":"仲巴县","en":"zhongbaxian"},{"id":"3894","name":"亚东县","en":"yadongxian"},{"id":"3895","name":"吉隆县","en":"jilongxian"},{"id":"3896","name":"聂拉木县","en":"nielamuxian"},{"id":"3897","name":"萨嘎县","en":"sagaxian"},{"id":"3898","name":"岗巴县","en":"gangbaxian"}]},{"id":"432","name":"那曲地区","en":"naqudiqu","l3":[{"id":"3899","name":"那曲县","en":"naquxian"},{"id":"3900","name":"嘉黎县","en":"jialixian"},{"id":"3901","name":"比如县","en":"biruxian"},{"id":"3902","name":"聂荣县","en":"nierongxian"},{"id":"3903","name":"安多县","en":"anduoxian"},{"id":"3904","name":"申扎县","en":"shenzaxian"},{"id":"3905","name":"索　县","en":"suo　xian"},{"id":"3906","name":"班戈县","en":"bangexian"},{"id":"3907","name":"巴青县","en":"baqingxian"},{"id":"3908","name":"尼玛县","en":"nimaxian"},{"id":"3909","name":"双湖特别区","en":"shuanghutebiequ"}]},{"id":"433","name":"阿里地区","en":"alidiqu","l3":[{"id":"3910","name":"噶尔县","en":"gaerxian"},{"id":"3911","name":"普兰县","en":"pulanxian"},{"id":"3912","name":"札达县","en":"zhadaxian"},{"id":"3913","name":"日土县","en":"rituxian"},{"id":"3914","name":"革吉县","en":"gejixian"},{"id":"3915","name":"改则县","en":"gaizexian"},{"id":"3916","name":"措勤县","en":"cuoqinxian"}]},{"id":"434","name":"林芝地区","en":"linzhidiqu","l3":[{"id":"3917","name":"林芝县","en":"linzhixian"},{"id":"3918","name":"工布江达县","en":"gongbujiangdaxian"},{"id":"3919","name":"米林县","en":"milinxian"},{"id":"3920","name":"墨脱县","en":"motuoxian"},{"id":"3921","name":"波密县","en":"bomixian"},{"id":"3922","name":"察隅县","en":"chayuxian"},{"id":"3923","name":"朗　县","en":"lang　xian"}]}]},{"id":"43","name":"香港特别行政区","mark":"X","en":"xianggang","l2":[{"id":"454","name":"香港","en":"xianggang","l3":[{"id":"4039","name":"中西区","en":"zhongxiqu"},{"id":"4040","name":"东区","en":"dongqu"},{"id":"4041","name":"九龙城区","en":"jiulongchengqu"},{"id":"4042","name":"观塘区","en":"guantangqu"},{"id":"4043","name":"南区","en":"nanqu"},{"id":"4044","name":"深水埗区","en":"shenshuibuqu"},{"id":"4045","name":"黄大仙区","en":"huangdaxianqu"},{"id":"4046","name":"湾仔区","en":"wanziqu"},{"id":"4047","name":"油尖旺区","en":"youjianwangqu"},{"id":"4048","name":"离岛区","en":"lidaoqu"},{"id":"4049","name":"葵青区","en":"kuiqingqu"},{"id":"4050","name":"北区","en":"beiqu"},{"id":"4051","name":"西贡区","en":"xigongqu"},{"id":"4052","name":"沙田区","en":"shatianqu"},{"id":"4053","name":"屯门区","en":"tunmenqu"},{"id":"4054","name":"大埔区","en":"dabuqu"},{"id":"4055","name":"荃湾区","en":"quanwanqu"},{"id":"4056","name":"元朗区","en":"yuanlangqu"}]}]},{"id":"42","name":"新疆维吾尔自治区","mark":"X","en":"xinjiangweiwuerzizhiqu","l2":[{"id":"440","name":"乌鲁木齐","en":"wulumuqi","l3":[{"id":"3945","name":"天山区","en":"tianshanqu"},{"id":"3946","name":"沙依巴克区","en":"shayibakequ"},{"id":"3947","name":"新市区","en":"xinshiqu"},{"id":"3948","name":"水磨沟区","en":"shuimogouqu"},{"id":"3949","name":"头屯河区","en":"toutunhequ"},{"id":"3950","name":"达坂城区","en":"dabanchengqu"},{"id":"3951","name":"米东区","en":"midongqu"},{"id":"3952","name":"乌鲁木齐县","en":"wulumuqixian"}]},{"id":"441","name":"克拉玛依","en":"kelamayi","l3":[{"id":"3953","name":"克拉玛依区","en":"kelamayiqu"},{"id":"3954","name":"独山子区","en":"dushanziqu"},{"id":"3955","name":"白碱滩区","en":"baijiantanqu"},{"id":"3956","name":"乌尔禾区","en":"wuerhequ"}]},{"id":"442","name":"吐鲁番地区","en":"tulufandiqu","l3":[{"id":"3957","name":"吐鲁番","en":"tulufanshi"},{"id":"3958","name":"鄯善县","en":"shanshanxian"},{"id":"3959","name":"托克逊县","en":"tuokexunxian"}]},{"id":"443","name":"哈密地区","en":"hamidiqu","l3":[{"id":"3960","name":"哈密","en":"hamishi"},{"id":"3961","name":"伊吾县","en":"yiwuxian"},{"id":"3962","name":"巴里坤哈萨克自治县","en":"balikunhasakezizhixian"}]},{"id":"444","name":"和田地区","en":"hetiandequ","l3":[{"id":"3963","name":"和田","en":"hetianshi"},{"id":"3964","name":"和田县","en":"hetianxian"},{"id":"3965","name":"墨玉县","en":"moyuxian"},{"id":"3966","name":"皮山县","en":"pishanxian"},{"id":"3967","name":"洛浦县","en":"luopuxian"},{"id":"3968","name":"策勒县","en":"celexian"},{"id":"3969","name":"于田县","en":"yutianxian"},{"id":"3970","name":"民丰县","en":"minfengxian"}]},{"id":"445","name":"阿克苏地区","en":"akesudiqu","l3":[{"id":"3971","name":"阿克苏","en":"akesushi"},{"id":"3972","name":"温宿县","en":"wensuxian"},{"id":"3973","name":"库车县","en":"kuchexian"},{"id":"3974","name":"沙雅县","en":"shayaxian"},{"id":"3975","name":"新和县","en":"xinhexian"},{"id":"3976","name":"拜城县","en":"baichengxian"},{"id":"3977","name":"乌什县","en":"wushenxian"},{"id":"3978","name":"阿瓦提县","en":"awatixian"},{"id":"3979","name":"柯坪县","en":"kepingxian"}]},{"id":"446","name":"喀什地区","en":"kashidiqu","l3":[{"id":"3980","name":"喀什","en":"kashishi"},{"id":"3981","name":"疏附县","en":"shufuxian"},{"id":"3982","name":"疏勒县","en":"shulexian"},{"id":"3983","name":"英吉沙县","en":"yingjishaxian"},{"id":"3984","name":"泽普","en":"zepu"},{"id":"3985","name":"莎车","en":"suoche"},{"id":"3986","name":"叶城","en":"yecheng"},{"id":"3987","name":"麦盖提","en":"maigaiti"},{"id":"3988","name":"岳普湖","en":"yuepuhu"},{"id":"3989","name":"伽师","en":"jiashi"},{"id":"3990","name":"巴楚","en":"bachu"},{"id":"3991","name":"塔什库尔干塔吉克自治","en":"tashenkuergantajikezizhi"}]},{"id":"447","name":"克孜勒苏柯尔克孜自治州","en":"kezilesukeerkezizizhi","l3":[{"id":"3992","name":"阿图什","en":"atushenshi"},{"id":"3993","name":"阿克陶县","en":"aketaoxian"},{"id":"3994","name":"阿合奇县","en":"aheqixian"},{"id":"3995","name":"乌恰县","en":"wuqiaxian"}]},{"id":"448","name":"巴音郭楞蒙古自治州","en":"bayinguolengmengguzizhizhou","l3":[{"id":"3996","name":"库尔勒","en":"kuerleshi"},{"id":"3997","name":"轮台县","en":"luntaixian"},{"id":"3998","name":"尉犁县","en":"yulixian"},{"id":"3999","name":"若羌县","en":"ruoqiangxian"},{"id":"4000","name":"且末县","en":"qiemoxian"},{"id":"4001","name":"焉耆回族自治县","en":"yanqihuizuzizhixian"},{"id":"4002","name":"和静县","en":"hejingxian"},{"id":"4003","name":"和硕县","en":"heshuoxian"},{"id":"4004","name":"博湖县","en":"bohuxian"}]},{"id":"449","name":"昌吉回族自治州","en":"changjihuizuzizhizhou","l3":[{"id":"4005","name":"昌吉","en":"changjishi"},{"id":"4006","name":"阜康","en":"fukangshi"},{"id":"4007","name":"呼图壁县","en":"hutubixian"},{"id":"4008","name":"玛纳斯县","en":"manasixian"},{"id":"4009","name":"奇台县","en":"qitaixian"},{"id":"4010","name":"吉木萨尔县","en":"jimusaerxian"},{"id":"4011","name":"木垒哈萨克自治县","en":"muleihasakezizhixian"}]},{"id":"450","name":"博尔塔拉蒙古自治州","en":"boertalamengguzizhizhou","l3":[{"id":"4012","name":"博乐","en":"boleshi"},{"id":"4013","name":"精河县","en":"jinghexian"},{"id":"4014","name":"温泉县","en":"wenquanxian"}]}]},{"id":"29","name":"云南","mark":"Y","en":"yunnan","l2":[{"id":"342","name":"昆明","en":"kunming","l3":[{"id":"3110","name":"五华区","en":"wuhuaqu"},{"id":"3111","name":"盘龙区","en":"panlongqu"},{"id":"3112","name":"官渡区","en":"guanduqu"},{"id":"3113","name":"西山区","en":"xishanqu"},{"id":"3114","name":"东川区","en":"dongchuanqu"},{"id":"3115","name":"安宁","en":"anningshi"},{"id":"3116","name":"呈贡县","en":"chenggongxian"},{"id":"3117","name":"晋宁县","en":"jinningxian"},{"id":"3118","name":"富民县","en":"fuminxian"},{"id":"3119","name":"宜良县","en":"yiliangxian"},{"id":"3120","name":"嵩明县","en":"songmingxian"},{"id":"3121","name":"石林县","en":"shilinxian"},{"id":"3122","name":"禄劝县","en":"luquanxian"},{"id":"3123","name":"寻甸县","en":"xundianxian"}]},{"id":"343","name":"曲靖","en":"qujing","l3":[{"id":"3124","name":"麒麟区","en":"qilinqu"},{"id":"3125","name":"宣威","en":"xuanweishi"},{"id":"3126","name":"马龙县","en":"malongxian"},{"id":"3127","name":"陆良县","en":"luliangxian"},{"id":"3128","name":"师宗县","en":"shizongxian"},{"id":"3129","name":"罗平县","en":"luopingxian"},{"id":"3130","name":"富源县","en":"fuyuanxian"},{"id":"3131","name":"会泽县","en":"huizexian"},{"id":"3132","name":"沾益县","en":"zhanyixian"}]},{"id":"344","name":"玉溪","en":"yuxi","l3":[{"id":"3133","name":"红塔区","en":"hongtaqu"},{"id":"3134","name":"江川县","en":"jiangchuanxian"},{"id":"3135","name":"澄江县","en":"chengjiangxian"},{"id":"3136","name":"通海县","en":"tonghaixian"},{"id":"3137","name":"华宁县","en":"huaningxian"},{"id":"3138","name":"易门县","en":"yimenxian"},{"id":"3139","name":"峨山县","en":"eshanxian"},{"id":"3140","name":"新平县","en":"xinpingxian"},{"id":"3141","name":"元江县","en":"yuanjiangxian"}]},{"id":"345","name":"保山","en":"baoshan","l3":[{"id":"3142","name":"隆阳区","en":"longyangqu"},{"id":"3143","name":"施甸县","en":"shidianxian"},{"id":"3144","name":"腾冲县","en":"tengchongxian"},{"id":"3145","name":"龙陵县","en":"longlingxian"},{"id":"3146","name":"昌宁县","en":"changningxian"}]},{"id":"346","name":"昭通","en":"zhaotong","l3":[{"id":"3147","name":"昭阳区","en":"zhaoyangqu"},{"id":"3148","name":"鲁甸县","en":"ludianxian"},{"id":"3149","name":"巧家县","en":"qiaojiaxian"},{"id":"3150","name":"盐津县","en":"yanjinxian"},{"id":"3151","name":"大关县","en":"daguanxian"},{"id":"3152","name":"永善县","en":"yongshanxian"},{"id":"3153","name":"绥江县","en":"suijiangxian"},{"id":"3154","name":"镇雄县","en":"zhenxiongxian"},{"id":"3155","name":"彝良县","en":"yiliangxian"},{"id":"3156","name":"威信县","en":"weixinxian"},{"id":"3157","name":"水富县","en":"shuifuxian"}]},{"id":"347","name":"丽江","en":"lijiang","l3":[{"id":"3158","name":"古城区","en":"guchengqu"},{"id":"3159","name":"永胜县","en":"yongshengxian"},{"id":"3160","name":"华坪县","en":"huapingxian"},{"id":"3161","name":"玉龙县","en":"yulongxian"},{"id":"3162","name":"宁蒗县","en":"ninglangxian"}]},{"id":"348","name":"普洱","en":"puer","l3":[{"id":"3163","name":"思茅区","en":"simaoqu"},{"id":"3164","name":"宁洱县","en":"ningerxian"},{"id":"3165","name":"墨江县","en":"mojiangxian"},{"id":"3166","name":"景东县","en":"jingdongxian"},{"id":"3167","name":"景谷县","en":"jingguxian"},{"id":"3168","name":"镇沅县","en":"zhenyuanxian"},{"id":"3169","name":"江城县","en":"jiangchengxian"},{"id":"3170","name":"孟连县","en":"menglianxian"},{"id":"3171","name":"澜沧县","en":"lancangxian"},{"id":"3172","name":"西盟县","en":"ximengxian"}]},{"id":"349","name":"临沧","en":"lincang","l3":[{"id":"3173","name":"临翔区","en":"linxiangqu"},{"id":"3174","name":"凤庆县","en":"fengqingxian"},{"id":"3175","name":"云　县","en":"yun　xian"},{"id":"3176","name":"永德县","en":"yongdexian"},{"id":"3177","name":"镇康县","en":"zhenkangxian"},{"id":"3178","name":"双江县","en":"shuangjiangxian"},{"id":"3179","name":"耿马县","en":"gengmaxian"},{"id":"3180","name":"沧源县","en":"cangyuanxian"}]},{"id":"350","name":"文山州","en":"wenshanzhou","l3":[{"id":"3181","name":"文山县","en":"wenshanxian"},{"id":"3182","name":"砚山县","en":"yanshanxian"},{"id":"3183","name":"西畴县","en":"xichouxian"},{"id":"3184","name":"麻栗坡","en":"malipo"},{"id":"3185","name":"马关县","en":"maguanxian"},{"id":"3186","name":"丘北县","en":"qiubeixian"},{"id":"3187","name":"广南县","en":"guangnanxian"},{"id":"3188","name":"富宁县","en":"funingxian"}]},{"id":"351","name":"红河州","en":"honghezhou","l3":[{"id":"3189","name":"蒙自县","en":"mengzixian"},{"id":"3190","name":"个旧","en":"gejiushi"},{"id":"3191","name":"开远","en":"kaiyuanshi"},{"id":"3192","name":"绿春县","en":"lvchunxian"},{"id":"3193","name":"建水县","en":"jianshuixian"},{"id":"3194","name":"石屏县","en":"shipingxian"},{"id":"3195","name":"弥勒县","en":"milexian"},{"id":"3196","name":"泸西县","en":"luxixian"},{"id":"3197","name":"元阳县","en":"yuanyangxian"},{"id":"3198","name":"红河县","en":"honghexian"},{"id":"3199","name":"金平县","en":"jinpingxian"},{"id":"3200","name":"河口县","en":"hekouxian"},{"id":"3201","name":"屏边县","en":"pingbianxian"}]},{"id":"352","name":"西双版纳州","en":"xishuangbannazhou","l3":[{"id":"3202","name":"景洪","en":"jinghongshi"},{"id":"3203","name":"勐海县","en":"menghaixian"},{"id":"3204","name":"勐腊县","en":"menglaxian"}]},{"id":"353","name":"楚雄州","en":"chuxiongzhou","l3":[{"id":"3205","name":"楚雄","en":"chuxiongshi"},{"id":"3206","name":"双柏县","en":"shuangbaixian"},{"id":"3207","name":"牟定县","en":"moudingxian"},{"id":"3208","name":"南华县","en":"nanhuaxian"},{"id":"3209","name":"姚安县","en":"yaoanxian"},{"id":"3210","name":"大姚县","en":"dayaoxian"},{"id":"3211","name":"永仁县","en":"yongrenxian"},{"id":"3212","name":"元谋县","en":"yuanmouxian"},{"id":"3213","name":"武定县","en":"wudingxian"},{"id":"3214","name":"禄丰县","en":"lufengxian"}]},{"id":"354","name":"大理州","en":"dali","l3":[{"id":"3215","name":"大理","en":"dalishi"},{"id":"3216","name":"祥云县","en":"xiangyunxian"},{"id":"3217","name":"宾川县","en":"binchuanxian"},{"id":"3218","name":"弥渡县","en":"miduxian"},{"id":"3219","name":"永平县","en":"yongpingxian"},{"id":"3220","name":"云龙县","en":"yunlongxian"},{"id":"3221","name":"洱源县","en":"eryuanxian"},{"id":"3222","name":"剑川县","en":"jianchuanxian"},{"id":"3223","name":"鹤庆县","en":"heqingxian"},{"id":"3224","name":"漾濞县","en":"yangbixian"},{"id":"3225","name":"南涧县","en":"nanjianxian"},{"id":"3226","name":"巍山县","en":"weishanxian"}]},{"id":"355","name":"德宏州","en":"dehongzhou","l3":[{"id":"3227","name":"潞西","en":"luxishi"},{"id":"3228","name":"瑞丽","en":"ruilishi"},{"id":"3229","name":"梁河县","en":"lianghexian"},{"id":"3230","name":"盈江县","en":"yingjiangxian"},{"id":"3231","name":"陇川县","en":"longchuanxian"}]},{"id":"356","name":"怒江州","en":"nujiangzhou","l3":[{"id":"3232","name":"泸水县","en":"lushuixian"},{"id":"3233","name":"福贡县","en":"fugongxian"},{"id":"3234","name":"贡山县","en":"gongshanxian"},{"id":"3235","name":"兰坪县","en":"lanpingxian"}]},{"id":"357","name":"迪庆州","en":"diqingzhou","l3":[{"id":"3236","name":"香格里拉县","en":"xianggelilaxian"},{"id":"3237","name":"德钦县","en":"deqinxian"},{"id":"3238","name":"维西县","en":"weixixian"}]}]},{"id":"17","name":"浙江","mark":"Z","en":"zhejiang","l2":[{"id":"182","name":"杭州","en":"hangzhou","l3":[{"id":"1801","name":"拱墅区","en":"gongshuqu"},{"id":"1802","name":"上城区","en":"shangchengqu"},{"id":"1803","name":"下城区","en":"xiachengqu"},{"id":"1804","name":"江干区","en":"jiangganqu"},{"id":"1805","name":"西湖区","en":"xihuqu"},{"id":"1806","name":"滨江区","en":"binjiangqu"},{"id":"1807","name":"萧山区","en":"xiaoshanqu"},{"id":"1808","name":"余杭区","en":"yuhangqu"},{"id":"1809","name":"建德","en":"jiandeshi"},{"id":"1810","name":"富阳","en":"fuyangshi"},{"id":"1811","name":"临安","en":"linanshi"},{"id":"1812","name":"桐庐县","en":"tongluxian"},{"id":"1813","name":"淳安县","en":"chunanxian"}]},{"id":"183","name":"宁波","en":"ningbo","l3":[{"id":"1814","name":"海曙区","en":"haishuqu"},{"id":"1815","name":"江东区","en":"jiangdongqu"},{"id":"1816","name":"江北区","en":"jiangbeiqu"},{"id":"1817","name":"北仑区","en":"beilunqu"},{"id":"1818","name":"镇海区","en":"zhenhaiqu"},{"id":"1819","name":"鄞州区","en":"yinzhouqu"},{"id":"1820","name":"余姚","en":"yuyaoshi"},{"id":"1821","name":"慈溪","en":"cixishi"},{"id":"1822","name":"奉化","en":"fenghuashi"},{"id":"1823","name":"象山县","en":"xiangshanxian"},{"id":"1824","name":"宁海县","en":"ninghaixian"}]},{"id":"184","name":"温州","en":"wenzhou","l3":[{"id":"1825","name":"鹿城区","en":"luchengqu"},{"id":"1826","name":"龙湾区","en":"longwanqu"},{"id":"1827","name":"瓯海区","en":"ouhaiqu"},{"id":"1828","name":"瑞安","en":"ruianshi"},{"id":"1829","name":"乐清","en":"leqingshi"},{"id":"1830","name":"洞头县","en":"dongtouxian"},{"id":"1831","name":"永嘉县","en":"yongjiaxian"},{"id":"1832","name":"平阳县","en":"pingyangxian"},{"id":"1833","name":"苍南县","en":"cangnanxian"},{"id":"1834","name":"文成县","en":"wenchengxian"},{"id":"1835","name":"泰顺县","en":"taishunxian"}]},{"id":"185","name":"嘉兴","en":"jiaxing","l3":[{"id":"1836","name":"南湖区","en":"nanhuqu"},{"id":"1837","name":"秀洲区","en":"xiuzhouqu"},{"id":"1838","name":"海宁","en":"hainingshi"},{"id":"1839","name":"平湖","en":"pinghushi"},{"id":"1840","name":"桐乡","en":"tongxiangshi"},{"id":"1841","name":"嘉善县","en":"jiashanxian"},{"id":"1842","name":"海盐县","en":"haiyanxian"}]},{"id":"186","name":"湖州","en":"huzhou","l3":[{"id":"1843","name":"吴兴区","en":"wuxingqu"},{"id":"1844","name":"南浔区","en":"nanxunqu"},{"id":"1845","name":"德清县","en":"deqingxian"},{"id":"1846","name":"长兴县","en":"changxingxian"},{"id":"1847","name":"安吉县","en":"anjixian"}]},{"id":"187","name":"绍兴","en":"shaoxing","l3":[{"id":"1848","name":"越城区","en":"yuechengqu"},{"id":"1849","name":"诸暨","en":"zhujishi"},{"id":"1850","name":"上虞","en":"shangyushi"},{"id":"1851","name":"嵊州","en":"shengzhoushi"},{"id":"1852","name":"绍兴县","en":"shaoxingxian"},{"id":"1853","name":"新昌县","en":"xinchangxian"}]},{"id":"188","name":"金华","en":"jinhua","l3":[{"id":"1854","name":"婺城区","en":"wuchengqu"},{"id":"1855","name":"金东区","en":"jindongqu"},{"id":"1856","name":"兰溪","en":"lanxishi"},{"id":"1857","name":"义乌","en":"yiwushi"},{"id":"1858","name":"东阳","en":"dongyangshi"},{"id":"1859","name":"永康","en":"yongkangshi"},{"id":"1860","name":"武义县","en":"wuyixian"},{"id":"1861","name":"浦江县","en":"pujiangxian"},{"id":"1862","name":"磐安县","en":"pananxian"}]},{"id":"189","name":"衢州","en":"quzhou","l3":[{"id":"1863","name":"柯城区","en":"kechengqu"},{"id":"1864","name":"衢江区","en":"qujiangqu"},{"id":"1865","name":"江山","en":"jiangshanshi"},{"id":"1866","name":"常山县","en":"changshanxian"},{"id":"1867","name":"开化县","en":"kaihuaxian"},{"id":"1868","name":"龙游县","en":"longyouxian"}]},{"id":"190","name":"舟山","en":"zhoushan","l3":[{"id":"1869","name":"定海区","en":"dinghaiqu"},{"id":"1870","name":"普陀区","en":"putuoqu"},{"id":"1871","name":"岱山县","en":"daishanxian"},{"id":"1872","name":"嵊泗县","en":"shengsixian"}]},{"id":"191","name":"台州","en":"tz","l3":[{"id":"1873","name":"椒江区","en":"jiaojiangqu"},{"id":"1874","name":"黄岩区","en":"huangyanqu"},{"id":"1875","name":"路桥区","en":"luqiaoqu"},{"id":"1876","name":"温岭","en":"wenlingshi"},{"id":"1877","name":"临海","en":"linhaishi"},{"id":"1878","name":"玉环县","en":"yuhuanxian"},{"id":"1879","name":"三门县","en":"sanmenxian"},{"id":"1880","name":"天台县","en":"tiantaixian"},{"id":"1881","name":"仙居县","en":"xianjuxian"}]},{"id":"192","name":"丽水","en":"lishui","l3":[{"id":"1882","name":"莲都区","en":"liandouqu"},{"id":"1883","name":"龙泉","en":"longquanshi"},{"id":"1884","name":"青田县","en":"qingtianxian"},{"id":"1885","name":"缙云县","en":"jinyunxian"},{"id":"1886","name":"遂昌县","en":"suichangxian"},{"id":"1887","name":"松阳县","en":"songyangxian"},{"id":"1888","name":"云和县","en":"yunhexian"},{"id":"1889","name":"庆元县","en":"qingyuanxian"},{"id":"1890","name":"景宁畲族自治县","en":"jingningshezuzizhixian"}]}]}]
    '''
    job_save_zhyc=[]
    page_number = 1
    judge = 0
    total = 0
    dict_city={'巴彦淖尔': '39,423', '兴安盟': '39,425', '清远': '25,306', '濮阳': '22,255', '邵阳': '24,281', '厦门': '19,211', '张掖': '31,374', '北海': '38,406', '黄南州': '32,385', '嘉兴': '17,185', '包头': '39,417', '南充': '27,322', '香港': '43,454', '台州': '17,191', '连云港': '16,175', '泰州': '16,180', '宜春': '20,227', '泰安': '21,239', '定西': '31,378', '县': '33,397', '酒泉': '31,376', '白城': '14,154', '乐山': '27,321', '海南州': '32,386', '泉州': '19,214', '洛阳': '22,249', '宝鸡': '30,360', '阿拉善盟': '39,427', '阿克苏地区': '42,445', '柳州': '38,403', '锦州': '13,139', '秦皇岛': '11,113', '丽江': '29,347', '景德镇': '20,220', '周口': '22,262', '澳门': '44,455', '珠海': '25,293', '唐山': '11,112', '北京': '34,398', '双鸭山': '15,160', '安康': '30,366', '昌都地区': '40,429', '保定': '11,116', '鹰潭': '20,224', '毕节地区': '28,338', '广州': '25,291', '湘西州': '24,290', '兰州': '31,368', '朝阳': '13,145', '衡水': '11,121', '海东地区': '32,383', '金昌': '31,370', '遵义': '28,335', '商洛': '30,367', '赣州': '20,225', '东莞': '25,307', '盐城': '16,177', '鄂州': '23,271', '辽源': '14,150', '漳州': '19,215', '晋城': '12,126', '汉中': '30,364', '南平': '19,216', '嘉义': '33,396', '池州': '18,208', '廊坊': '11,120', '驻马店': '22,263', '六安': '18,206', '银川': '41,435', '舟山': '17,190', '十堰': '23,267', '烟台': '21,235', '萍乡': '20,221', '拉萨': '40,428', '阿里地区': '40,433', '芜湖': '18,194', '宜昌': '23,269', '沈阳': '13,133', '徐州': '16,171', '西宁': '32,382', '渭南': '30,362', '淮北': '18,198', '桂林': '38,404', '襄阳': '23,266', '黄石': '23,265', '本溪': '13,137', '齐齐哈尔': '15,157', '黄冈': '23,273', '吉安': '20,226', '凉山州': '27,332', '许昌': '22,256', '湘潭': '24,279', '德阳': '27,316', '南昌': '20,219', '呼伦贝尔': '39,422', '潍坊': '21,236', '果洛州': '32,387', '绥化': '15,167', '邢台': '11,115', '那曲地区': '40,432', '黔西南州': '28,339', '永州': '24,287', '上海': '36,400', '通辽': '39,420', '宣城': '18,209', '惠州': '25,301', '阜阳': '18,203', '南京': '16,169', '武威': '31,373', '荆州': '23,268', '宁波': '17,183', '宜宾': '27,323', '扬州': '16,178', '广元': '27,318', '石家庄': '11,111', '延边朝鲜族自治州': '14,155', '东营': '21,234', '抚顺': '13,136', '德宏州': '29,355', '哈密地区': '42,443', '贺州': '38,412', '湖州': '17,186', '台北': '33,390', '张家界': '24,284', '青岛': '21,231', '陇南': '31,379', '益阳': '24,285', '海外': '45,465', '汕尾': '25,303', '宿迁': '16,181', '乌鲁木齐': '42,440', '大兴安岭地区': '15,168', '乌海': '39,418', '镇江': '16,179', '怀化': '24,288', '深圳': '25,292', '克拉玛依': '42,441', '鹤壁': '22,252', '天津': '35,399', '枣庄': '21,233', '梅州': '25,302', '普洱': '29,348', '恩施州': '23,276', '马鞍山': '18,197', '西安': '30,358', '吐鲁番地区': '42,442', '石嘴山': '41,436', '白山': '14,152', '资阳': '27,329', '营口': '13,140', '迪庆州': '29,357', '忻州': '12,130', '台南': '33,394', '新竹': '33,395', '承德': '11,118', '巴音郭楞蒙古自治州': '42,448', '贵港': '38,409', '福州': '19,210', '鞍山': '13,135', '张家口': '11,117', '铜陵': '18,199', '淮安': '16,176', '喀什地区': '42,446', '伊春': '15,162', '南通': '16,174', '通化': '14,151', '安庆': '18,200', '攀枝花': '27,314', '临沂': '21,242', '邯郸': '11,114', '淮南': '18,196', '临汾': '12,131', '湛江': '25,298', '鄂尔多斯': '39,421', '大理州': '29,354', '百色': '38,411', '博尔塔拉蒙古自治州': '42,450', '楚雄州': '29,353', '三明': '19,213', '广安': '27,324', '阜新': '13,141', '临夏州': '31,380', '文山州': '29,350', '鹤岗': '15,159', '保山': '29,345', '曲靖': '29,343', '武汉': '23,264', '七台河': '15,164', '雅安': '27,327', '泸州': '27,315', '黔东南州': '28,340', '威海': '21,237', '佛山': '25,296', '阳泉': '12,124', '延安': '30,363', '常德': '24,283', '辽阳': '13,142', '铜仁地区': '28,337', '牡丹江': '15,165', '咸阳': '30,361', '晋中': '12,128', '大连': '13,134', '九江': '20,222', '克孜勒苏柯尔克孜自治州': '42,447', '无锡': '16,170', '菏泽': '21,246', '株洲': '24,278', '黑河': '15,166', '揭阳': '25,457', '临沧': '29,349', '南阳': '22,259', '常州': '16,172', '茂名': '25,299', '哈尔滨': '15,156', '宁德': '19,218', '济宁': '21,238', '丽水': '17,192', '天水': '31,372', '沧州': '11,119', '日照': '21,240', '莆田': '19,212', '吴忠': '41,437', '阳江': '25,305', '甘孜州': '27,331', '济南': '21,230', '内江': '27,320', '和田地区': '42,444', '金华': '17,188', '遂宁': '27,319', '乌兰察布': '39,424', '日喀则地区': '40,431', '杭州': '17,182', '铜川': '30,359', '肇庆': '25,300', '大同': '12,123', '郴州': '24,286', '庆阳': '31,377', '苏州': '16,173', '安阳': '22,254', '盘锦': '13,143', '佳木斯': '15,163', '大庆': '15,161', '朔州': '12,127', '崇左': '38,415', '滁州': '18,202', '成都': '27,312', '随州': '23,275', '海西州': '32,389', '郑州': '22,247', '白银': '31,371', '巴中': '27,328', '防城港': '38,407', '自贡': '27,313', '抚州': '20,228', '安顺': '28,336', '衡阳': '24,280', '基隆': '33,392', '黄山': '18,201', '德州': '21,243', '汕头': '25,294', '玉溪': '29,344', '漯河': '22,257', '新乡': '22,253', '亳州': '18,207', '重庆': '37,401', '嘉峪关': '31,369', '合肥': '18,193', '云浮': '25,458', '长春': '14,147', '平顶山': '22,250', '龙岩': '19,217', '平凉': '31,375', '怒江州': '29,356', '丹东': '13,138', '六盘水': '28,334', '运城': '12,129', '高雄': '33,391', '巢湖': '18,205', '新余': '20,223', '河源': '25,304', '台中': '33,393', '中卫': '41,439', '娄底': '24,289', '林芝地区': '40,434', '莱芜': '21,241', '梧州': '38,405', '阿坝州': '27,330', '吕梁': '12,132', '温州': '17,184', '衢州': '17,189', '宿州': '18,204', '岳阳': '24,282', '淄博': '21,232', '榆林': '30,365', '来宾': '38,414', '商丘': '22,260', '绍兴': '17,187', '呼和浩特': '39,416', '南宁': '38,402', '信阳': '22,261', '三门峡': '22,258', '荆门': '23,270', '昌吉回族自治州': '42,449', '长沙': '24,277', '韶关': '25,295', '四平': '14,149', '上饶': '20,229', '眉山': '27,326', '三亚': '26,310', '吉林': '14,148', '西双版纳州': '29,352', '铁岭': '13,144', '昭通': '29,346', '开封': '22,248', '锡林郭勒盟': '39,426', '滨州': '21,245', '海北州': '32,384', '玉林': '38,410', '孝感': '23,272', '赤峰': '39,419', '咸宁': '23,274', '长治': '12,125', '贵阳': '28,333', '潮州': '25,456', '海口': '26,309', '中山': '25,308', '昆明': '29,342', '山南地区': '40,430', '钦州': '38,408', '江门': '25,297', '玉树州': '32,388', '固原': '41,438', '太原': '12,122', '蚌埠': '18,195', '鸡西': '15,158', '焦作': '22,251', '甘南州': '31,381', '绵阳': '27,317', '聊城': '21,244', '葫芦岛': '13,146', '河池': '38,413', '红河州': '29,351', '达州': '27,325', '黔南州': '28,341'}
    flag_next = True
    while flag_next:
        try:
            jobs_url_li=[]
            try:
                time.sleep(3)
                d_pos = {"kw": compName}
                comp_name = parse.urlencode(d_pos).encode('utf-8')
                comp_name = str(comp_name).split('kw=')[1][:-1]
                city_number=str(dict_city[cityName])
                city_number=city_number.split(',')[0]+'%2C'+city_number.split(',')[1]
            except:
                judge=1
                flag_next = False
                traceback.print_exc()
                break
            url_zhyc_zwss ="http://www.chinahr.com/sou/?"+"keyword="+comp_name+"&city="+city_number+"&page="+str(page_number)
            # url_zhyc_zwss='http://search.chinahr.com/hz/job/?key=%E6%9D%AD%E5%B7%9E%E5%88%9B%E8%B7%83%E5%95%86%E5%8A%A1%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8'
            print("zhyc----",url_zhyc_zwss)
            try:
                html_li_text=xh_pd_req(pos_url=url_zhyc_zwss,data='',headers=head_reqst())
            except:
                flag_next = False
                break
            # request_zw=request.Request(url_zhyc_zwss,headers=head_reqst())
            # html_li_text = request.urlopen(request_zw).read().decode('utf-8', errors='ignore')
            # print(html_li_text)
            if "中华英才" in html_li_text:
                sel = Selector(text=html_li_text)
                job_zhyc_li = sel.xpath('//div[@class="resultList"]/div')
                for job_zhyc in job_zhyc_li:
                    job_zhyc_name = job_zhyc.xpath('string(ul/li[@class="l1"]/span[@class="e3 cutWord"]/a)').extract()[0].strip()
                    # print(job_zhyc_name)
                    if job_zhyc_name == compName:
                        job_zhyc_url = job_zhyc.xpath('string(ul/li[@class="l1"]/span[@class="e1"]/a/@href)').extract()[0].strip()
                        if 'http' not in job_zhyc_url:
                            job_zhyc_url = "http://www.chinahr.com" + job_zhyc_url
                        #print(job_zhyc_url)
                        jobs_url_li.append(job_zhyc_url)
                try:
                    if len(sel.xpath('//div[@class="resultList"]/div')) < 20:
                        flag_next = False
                    else:
                        #print("开始爬取第%s页"%page_number)
                        page_number = page_number + 1
                        if page_number > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                            print("爬取页数超过30页，强制退出")
                            flag_next = False
                except:
                    flag_next = False
                    pass
                for job_url_1 in jobs_url_li[0:]:
                    time.sleep(random.uniform(0.3, 0.6))
                    try:
                        job_zhyc_text = xh_pd_req(pos_url=job_url_1, data='', headers=head_reqst())
                        # request_jx = request.Request(url=job_url_1, headers=head_reqst())
                        # job_zhyc_text = request.urlopen(request_jx, timeout=4).read().decode('utf-8', errors='ignore')
                        zw_data_zhyc = zwjx_zhyc_0(text=job_zhyc_text, compName=compName)
                        zw_data_zhyc['type'] = 'job'
                        zw_data_zhyc['channel'] = channelid
                        zw_data_zhyc['companyName'] = compName
                        zw_data_zhyc['province'] = provName
                        zw_data_zhyc['city'] = cityName_0
                        zw_data_zhyc['county'] = countyName
                        print("zhyc---------", zw_data_zhyc)
                        job_save_zhyc.append(zw_data_zhyc)
                    except:
                        traceback.print_exc()
                        logging.exception("Exception Logged")
                        pass
                    if len(job_save_zhyc) == 3:
                        total = total+3
                        data = json.dumps(job_save_zhyc)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('zhyc_jobl----3')
                        job_save_zhyc = []
                if len(job_save_zhyc) == 3 or len(job_save_zhyc) == 0:
                    pass
                else:
                    total = total + len(job_save_zhyc)
                    data = json.dumps(job_save_zhyc)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('zhyc_jobl----yfs')

            elif "" == html_li_text:
                flag_next = False
        except:
            traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_zhyczw(compName, provName, cityName, countyName,cityName_0, channelid=6):
    job_save_zhyc=[]
    page_number = 1
    type_zhyc='new'
    judge = 0
    total = 0
    url_num = 0
    dict_city={'樟树': {'sublist': {'城区': 'zhangshucq', '其他': 'zhangshuqt'}, 'code': 'zhangshu|5713'}, '海宁': {'sublist': {'海宁周边': 'hainzb', '盐官古城': 'yanggc', '钱塘江北岸': 'qiantjba', '海宁潮': 'hainc', '西山公园': 'xsgy'}, 'code': 'haining|500'}, '祁阳': {'sublist': {'城区': 'qiyangcq', '其他': 'qiyangqt'}, 'code': 'qiyang|8532'}, '慈利': {'sublist': {'城区': 'cilixiancq', '其他': 'cilixianqt'}, 'code': 'cilixian|6791'}, '晋城': {'sublist': {'沁水': 'qinshui', '其他': 'jinchengshi', '阳城': 'yangcheng', '城区': 'chengqu', '高平': 'gaopingjc', '泽州': 'zezhoujc', '开发区': 'kaifa', '陵川': 'lingchuan'}, 'code': 'jincheng|3350'}, '忻州': {'sublist': {'定襄': 'dingxiang', '原平': 'yuanping', '代县': 'daixian', '静乐': 'jingle', '繁峙': 'fanzhi', '其他': 'xinzhouqita', '五台': 'wutaixian', '忻府': 'xinfu', '宁武': 'ningwu'}, 'code': 'xinzhou|3453'}, '韶关': {'sublist': {'曲江': 'qujiang', '北江': 'beijiang', '浈江': 'zhenjiang', '仁化': 'renhua', '新丰': 'xinfeng', '武江': 'wujiangqu', '南雄': 'nanxiong', '翁源县': 'sgwyx', '始兴': 'shixing', '乐昌': 'lechang', '乳源': 'ruyuan', '其它': 'shaoguan'}, 'code': 'sg|2192'}, '南通': {'sublist': {'如东': 'rudongqu', '通州': 'tongzhou', '启东': 'qidongqu', '南通周边': 'nantong', '如皋': 'rugaoqu', '崇川': 'chongchuan', '开发区': 'kfaqu', '海安': 'haianqu', '港闸': 'gangzha', '海门': 'haimenqu'}, 'code': 'nt|394'}, '东营': {'sublist': {'垦利县': 'kenli', '广饶': 'dongyingguangrao', '河口': 'hekou', '利津': 'lijindy', '其他': 'dongyingshi', '东营区': 'dongying'}, 'code': 'dy|623'}, '巴彦淖尔': {'sublist': {'乌拉特中旗': 'wulatezhongqi', '巴彦周边': 'bayanzhoubian', '乌拉特后旗': 'wulatehouqi', '五原': 'wuyuan', '乌拉特前旗': 'wulateqianqi', '临河': 'linheq', '杭锦后旗': 'hangjinhouqi', '磴口': 'dengkou'}, 'code': 'bycem|10070'}, '成都': {'sublist': {'成都周边': 'chengdu', '邛崃市': 'cdqls', '蒲江': 'cdpujiang', '崇州': 'cdchongzhou', '天府新区': 'cdtfxq', '高新西区': 'gaoxinxiqu', '锦江': 'jinjiang', '成华': 'chenghua', '都江堰': 'dujiangyanshi', '青羊': 'qingyangqu', '高新区': 'cdgaoxin', '新都': 'xindu', '温江': 'wenjiang', '郫县': 'pixian', '金堂': 'jintang', '简阳': 'jianyangcd', '武侯': 'wuhou', '双流': 'shuangliu', '金牛': 'jinniu', '龙泉驿': 'longquanyi', '青白江': 'qingbaijiang', '大邑': 'cddayi', '新津': 'xinjin'}, 'code': 'cd|102'}, '桂阳': {'sublist': {'城区': 'czguiyangcq', '其他': 'czguiyangqt'}, 'code': 'czguiyang|5699'}, '黑河': {'sublist': {'嫩江': 'nenjiang', '黑河周边': 'heihezb', '北安': 'beian', '爱辉': 'aihui', '孙吴': 'sunwu', '逊克': 'xunke', '五大连池': 'wudalianchi'}, 'code': 'heihe|9862'}, '马鞍山': {'sublist': {'金家庄': 'jinjiazhuang', '花山': 'huashanqu', '含山': 'hanshanx', '和县': 'hexians', '博望区': 'masbwq', '雨山': 'yushan', '当涂': 'dangtu', '其它': 'maanshan'}, 'code': 'mas|2039'}, '天津': {'sublist': {'津南': 'jinnantj', '大港': 'dagang', '东丽': 'donglitj', '静海': 'jinghaiqu', '汉沽': 'hangu', '南开': 'nankai', '河北': 'hebeiqu', '北辰': 'beichentj', '河东': 'hedong', '西青': 'xiqingtj', '塘沽': 'tanggu', '红桥': 'hongqiaotj', '天津周边': 'tianjin', '宁河': 'ninghexian', '开发区': 'tjkaifaqu', '和平': 'heping', '宝坻': 'baodi', '河西': 'hexi', '武清': 'wuqing', '蓟县': 'jianxiantj'}, 'code': 'tj|18'}, '山南': {'sublist': {'乃东': 'naidongxian', '桑日': 'sangrixian', '贡嘎': 'gonggaxian', '山南周边': 'shannanzhoubian', '琼结': 'qiongjiexian', '扎囊': 'zhanangxian'}, 'code': 'sn|9576'}, '瓦房店': {'sublist': {'得利寺镇': 'delisi', '其他': 'wafangdianqita', '老虎屯镇': 'laohutun', '瓦房店': 'wafangdianshi', '长兴岛': 'changxingdao', '东岗镇': 'donggangzhen', '太阳街道': 'taiyangjie', '复州城镇': 'fuzhoucheng'}, 'code': 'wfd|3279'}, '阳江': {'sublist': {'高新区': 'gaoxinquw', '江城': 'jiangchengqu', '岗侨': 'gangqiaoqu', '阳东': 'yangdongxian', '海陵': 'hailingqu', '阳春': 'yangchunshi', '阳西': 'yangxixian'}, 'code': 'yj|2284'}, '资阳': {'sublist': {'安岳县': 'ziyanganyue', '乐至': 'lezhixian', '简阳市': 'luoyangjianyang', '雁江': 'yanjiangqu'}, 'code': 'zy|6803'}, '高安': {'sublist': {'城区': 'gaoancq', '其他': 'gaoanqt'}, 'code': 'gaoan|5712'}, '宁波': {'sublist': {'高新区': 'nbgxq', '象山': 'xiangshanqunew', '慈溪': 'cixiqu', '江东': 'jiangdong', '奉化': 'fenghua', '海曙': 'haishu', '余姚': 'yuyaoqu', '北仑': 'beilun', '宁海': 'ninghaixian', '镇海': 'zhenhai', '江北': 'jiangbeiqu', '鄞州': 'yinzhou', '宁波周边': 'ningbo'}, 'code': 'nb|135'}, '三门峡': {'sublist': {'义马': 'yimashi', '湖滨': 'hubinqu', '灵宝': 'smxlingbao', '陕县': 'shanxiansmx', '渑池': 'mianchixiansmx', '开发区': 'kaifaqu', '卢氏': 'lushixian'}, 'code': 'smx|9317'}, '柳州': {'sublist': {'城中': 'chengzhongqu', '柳江': 'liujiangxian', '三江': 'sanjiangxian', '融安': 'ronganxian', '融水': 'rongshuixian', '鱼峰': 'yufengqu', '柳北': 'liubeiqu', '柳南': 'liunanqu', '鹿寨': 'luzhaixian', '柳城': 'liuchengxian'}, 'code': 'liuzhou|7133'}, '武穴': {'sublist': {}, 'code': 'wuxueshi|7362'}, '济南': {'sublist': {'市中': 'jnshizhong', '长清': 'changqingqv', '历城': 'licheng', '平阴': 'pingyin', '历下': 'lixia', '章丘': 'zhangqiushi', '天桥': 'tianqiao', '商河': 'shanghe', '济南周边': 'jinanzhoubian', '高新': 'gaoxinqujn', '济阳': 'jiyang', '槐荫': 'huaiyinqu'}, 'code': 'jn|265'}, '睢县': {'sublist': {'城区': 'suixiancq', '其他': 'suixianqt'}, 'code': 'suixian|1038'}, '苍南': {'sublist': {}, 'code': 'cangnanxian|7579'}, '迁西': {'sublist': {'城区': 'qianxixiancq', '其他': 'qianxixianqt'}, 'code': 'qianxixian|7061'}, '张北': {'sublist': {'公会': 'gonghui', '馒头营': 'mantouying', '大囫囵': 'dahulun', '台路沟': 'tailugou', '大河': 'dahe', '油篓沟': 'youlougou', '张北': 'zhangbeizhen', '两面井': 'liangmianjing', '二泉井': 'erquanjing', '二台': 'ertai', '张北周边': 'zhangbeizb', '海流图': 'hailiutu', '单晶河': 'danjinghe'}, 'code': 'zhangbei|11201'}, '昌邑': {'sublist': {'城区': 'changyishicq', '其他': 'changyishiqt'}, 'code': 'changyishi|372'}, '澧县': {'sublist': {'城区': 'lixiancq', '其他': 'lixianqt'}, 'code': 'lixian|876'}, '海西': {'sublist': {'格尔木': 'geermushihx', '海西周边': 'haixizhoubian', '天峻': 'tianjun', '都兰': 'dulan', '德令哈': 'delinghashi', '乌兰': 'wulan'}, 'code': 'hx|9902'}, '新余': {'sublist': {'仙女湖': 'xiannvhu', '分宜': 'fenyixy', '渝水': 'yushui', '新余周边': 'xinyuzhoubian'}, 'code': 'xinyu|10115'}, '来宾': {'sublist': {'武宣': 'wuxuanxian', '兴宾': 'xingbingqu', '合山': 'heshanshi', '象州': 'xiangzhouxian', '忻城': 'qichengxian', '来宾周边': 'laibinzhoubian', '金秀': 'jinxiuxian'}, 'code': 'lb|10552'}, '汝州': {'sublist': {'汝南街道': 'runanjiedao', '煤山街道': 'meishanjiedao', '其他': 'ruzhoushiqita', '临汝镇': 'linruzhen'}, 'code': 'ruzhou|1010'}, '常宁': {'sublist': {'城区': 'changningshicq', '其他': 'changningshiqt'}, 'code': 'changningshi|921'}, '大同': {'sublist': {'浑源': 'hunyuanxian', '矿区': 'kuangqu', '大同': 'datongqu', '阳高': 'yanggaoxian', '左云': 'zuoyunxian', '城区': 'chengquxian', '广灵': 'guanglingxian', '南郊': 'nanjiaoqu', '天镇': 'tianzhenxian', '灵丘': 'lingqiuxian', '新荣': 'xinrongqu'}, 'code': 'dt|6964'}, '利津': {'sublist': {'城区': 'lijincq', '其他': 'lijinqt'}, 'code': 'lijin|628'}, '包头': {'sublist': {'东河': 'donghe', '白云矿区': 'baiyunkuang', '昆都仑区': 'kundoulun', '青山': 'qingshanqu', '滨河新区': 'btbhx', '固阳': 'guy', '稀土高新区': 'xitgxq', '土默特右旗': 'tmtyq', '达尔罕茂明安联合旗': 'daerhanqi', '九原': 'jiuyuan', '包头周边': 'baotou', '石拐': 'shiguai'}, 'code': 'bt|801'}, '眉山': {'sublist': {'青神': 'qingshenxian', '眉山周边': 'meishanzhoubian', '洪雅': 'hongyaxian', '丹棱': 'danlingxian', '彭山': 'pengshanxian', '东坡': 'dongpoqu', '仁寿县': 'meishanrenshou'}, 'code': 'ms|9704'}, '武安': {'sublist': {'城区': 'wuanchengqu', '其他': 'wuanshiqita'}, 'code': 'wuan|577'}, '濮阳': {'sublist': {'高新区': 'gaoxinquyu', '华龙': 'hualongqu', '清丰': 'qingfengxian', '范县': 'fanxianpy', '其他': 'puyangqita', '南乐': 'nanlexian', '台前': 'taiqianxian', '濮阳县': 'puyangxian'}, 'code': 'puyang|2346'}, '三沙': {'sublist': {'西沙群岛': 'xsqd', '南沙群岛': 'nsqd', '中沙群岛': 'zsqd'}, 'code': 'sansha|13722'}, '潍坊': {'sublist': {}, 'code': 'wf|362'}, '肇东': {'sublist': {}, 'code': 'shzhaodong|6721'}, '伊春': {'sublist': {'翠峦': 'cuiluanqu', '伊春': 'yichunqu', '伊春周边': 'yichunzb', '新青': 'xinqingqu', '南岔': 'nanchaqu', '西林': 'xilinqu', '友好': 'youhaoqu'}, 'code': 'yich|9773'}, '随州': {'sublist': {}, 'code': 'suizhou|9656'}, '漳州': {'sublist': {'长泰县': 'zzctx', '平和': 'pinghe', '云霄县': 'zzyxx', '角美': 'zzlckfq', '其他': 'zhangzhoushi', '龙文': 'longwen', '诏安': 'zhaoan', '南靖县': 'zznjx', '华安县': 'zzhax', '漳浦': 'zhangpuzz', '东山': 'dongshanxian', '龙海市': 'zhangzhoulonghai', '芗城': 'xiangchengqu'}, 'code': 'zhangzhou|710'}, '宣城': {'sublist': {'宁国': 'ningguoqu', '郎溪': 'langxi', '旌德': 'jingde', '绩溪': 'jixixian', '泾县': 'hzjingxian', '广德': 'guangde', '宣州': 'xuanzhou', '其它': 'xuanchengshi'}, 'code': 'xuancheng|5633'}, '安丘': {'sublist': {'城区': 'anqiucq', '其他': 'anqiuqt'}, 'code': 'anqiu|370'}, '东台': {'sublist': {'东台市区': 'dongtaishiqu', '其它': 'dongtaiqita'}, 'code': 'dongtai|615'}, '肇州': {'sublist': {'城区': 'zhaozhouchengqu', '其他': 'zhaozhouqita'}, 'code': 'zhaozhou|382'}, '周口': {'sublist': {'川汇': 'chuanhui', '太康': 'taikangzk', '西华': 'xihua', '郸城': 'dancheng', '鹿邑': 'luyizk', '淮阳': 'huaiyang', '其他': 'zhoukou', '商水': 'shangshuizk', '沈丘': 'shenqiuzk', '项城市': 'zhoukouxiangcheng', '扶沟': 'fugou'}, 'code': 'zk|933'}, '射洪': {'sublist': {'城区': 'shehongxiancq', '其他': 'shehongxianqt'}, 'code': 'shehongxian|9694'}, '通辽': {'sublist': {'扎鲁特旗': 'zaluteqi', '科尔沁左翼中旗': 'keerqinyouyizhongq', '通辽周边': 'tongliaozhoubian', '奈曼旗': 'naimanqi', '科尔沁': 'keerqinqu', '开鲁': 'kailu', '库伦旗': 'kulunqi', '霍林郭勒': 'huolinguole', '科尔沁左翼后旗': 'keerqinyouyihouqi'}, 'code': 'tongliao|10015'}, '绍兴': {'sublist': {'新昌': 'xinchangsx', '袍江': 'paojiang', '上虞': 'shangyu', '越城': 'yuecheng', '其他': 'shaoxing', '镜湖': 'sxjh', '诸暨': 'chujiqu', '嵊州': 'shengzhousx', '滨海': 'bhai', '柯桥': 'keqiao'}, 'code': 'sx|355'}, '单县': {'sublist': {'东城街道': 'dongchengjiedao', '南城街道': 'sxnanchengjiedao', '园艺街道': 'yuanyijiedao', '其他': 'danxianqita', '北城街道': 'sxbeichengjiedao'}, 'code': 'shanxian|5636'}, '淇县': {'sublist': {'城区': 'qixianqcq', '其他': 'qixianqqt'}, 'code': 'qixianq|9186'}, '澄迈': {'sublist': {}, 'code': 'cm|10331'}, '长岭': {'sublist': {'城区': 'changlingxiancq', '其他': 'changlingxianqt'}, 'code': 'changlingxian|9084'}, '上杭': {'sublist': {'城区': 'shanghangxiancq', '其他': 'shanghangxianqt'}, 'code': 'shanghangxian|6757'}, '九江': {'sublist': {'永修': 'yongxiuxian', '星子': 'xingzixian', '修水': 'xiushuixian', '九瑞大道': 'jjjrdd', '开发区': 'jjkaifaqu', '瑞昌': 'ruichang', '共青城': 'gongqing', '九江市区': 'jiujiangshiqu', '九江县': 'jiujiangxian', '德安': 'dean', '湖口': 'hukouxian', '彭泽': 'pengzexian', '浔阳区': 'xunyang', '庐山': 'lushan', '都昌': 'duchangxian', '九江周边': 'jiujiangshi', '武宁': 'wuningxian'}, 'code': 'jj|2247'}, '改则': {'sublist': {'改则县卫生局': 'gaizexianweishengju', '改则县政府': 'gaizexianzhengfu'}, 'code': 'gaizexian|9684'}, '石狮': {'sublist': {'石狮服装城': 'shishifzc', '石狮周边': 'shishizb'}, 'code': 'shishi|296'}, '垦利': {'sublist': {'兴隆街': 'xinglongjie', '垦利周边': 'kenlizhoubian', '垦利街': 'kenlijie', '黄河口': 'huanghekou', '郝家': 'haojia', '胜坨': 'shengtuo', '董集': 'dongjixiang', '永安': 'yongankl'}, 'code': 'kl|11313'}, '盘锦': {'sublist': {}, 'code': 'pj|2041'}, '上海': {'sublist': {'卢湾': 'luwan', '奉贤': 'fengxiansh', '南汇': 'nanhui', '宝山': 'baoshan', '长宁': 'changning', '青浦': 'qingpu', '上海周边': 'shanghaizhoubian', '闵行': 'minxing', '崇明': 'chongming', '徐汇': 'xuhui', '嘉定': 'jiading', '浦东': 'pudongxinqu', '金山': 'jinshan', '虹口': 'hongkou', '静安': 'jingan', '杨浦': 'yangpu', '黄浦': 'huangpu', '闸北': 'zhabei', '松江': 'songjiang', '普陀': 'putuo'}, 'code': 'sh|2'}, '凤城': {'sublist': {'城区': 'fengchengcq', '其他': 'fengchengqt'}, 'code': 'fengcheng|3450'}, '南阳': {'sublist': {'方城': 'fangchengxian', '淅川': 'xichuanxian', '内乡': 'neixiangxian', '油田': 'youtianqu', '新野': 'xinyeny', '唐河': 'tanghe', '南召': 'nanzhaoxian', '卧龙': 'wolong', '宛城': 'wancheng', '邓州': 'dengzhouny', '社旗': 'sheqixian', '其他': 'nanyang', '镇平': 'zhenpingxian', '西峡': 'xixiax', '桐柏': 'tongbaixian'}, 'code': 'ny|592'}, '慈溪': {'sublist': {'慈溪市区': 'cixishiqu', '其它': 'cixiqita'}, 'code': 'cixi|5334'}, '上饶': {'sublist': {'信州': 'xinzhouq', '玉山': 'yushanx', '德兴': 'dexing', '上饶周边': 'shangraozhoubian', '上饶县': 'shangraox', '余干': 'yugan', '广丰': 'guangfeng', '鄱阳': 'poyang'}, 'code': 'sr|10120'}, '重庆': {'sublist': {'渝北': 'yubei', '大渡口': 'dadukou', '万州': 'wanzhou', '南岸': 'nanan', '渝中': 'yuzhong', '两江新区': 'liangjiangxinqu', '北碚': 'beibei', '九龙坡': 'jiulongpo', '石柱': 'cqshizhu', '巴南': 'banan', '永川': 'yongchuan', '重庆周边': 'chongqing', '璧山': 'bishanxian', '长寿': 'changshou', '江北': 'jiangbei', '合川': 'hechuan', '涪陵': 'fuling', '沙坪坝': 'shapingba'}, 'code': 'cq|37'}, '本溪': {'sublist': {'本溪县': 'bxbenxi', '明山': 'mingshan', '溪湖': 'bxxihu', '桓仁': 'huanren', '南芬': 'nanfen', '平山': 'pingshanqu', '其它': 'benxishi'}, 'code': 'benxi|5845'}, '临沂': {'sublist': {'兰山': 'lanshanqu', '临沭': 'linshu', '莒南': 'junan', '费县': 'feixian', '沂南': 'yinanxianly', '郯城': 'tanchengly', '沂水': 'yishui', '罗庄': 'luozhuang', '高新区': 'lygaoxinqu', '河东': 'hedongqu', '平邑': 'pingyily', '兰陵': 'cangshanxian', '蒙阴': 'mengyinxian', '开发区': 'lykaifaqu', '北城新区': 'lybcxqu', '临沂周边': 'linyishi'}, 'code': 'linyi|505'}, '乐平': {'sublist': {'塔山街道': 'tashanjiedao', '洎阳街道': 'lpjiyangjiedao', '其他': 'lepingshiqita'}, 'code': 'lepingshi|9048'}, '辽阳': {'sublist': {'文圣': 'wensheng', '辽阳县': 'liaoyangxian', '弓长岭': 'gongchangling', '灯塔': 'dengtaly', '白塔': 'baita', '宏伟': 'hongwei', '太子河': 'taizihe', '其它': 'liaoyangshi'}, 'code': 'liaoyang|2038'}, '铁岭': {'sublist': {'西丰': 'xifengxian', '银州': 'yinzq', '清河': 'qinghequ', '铁岭县': 'tielingxian', '开原': 'kaiyuantl', '调兵山': 'diaobingshan', '昌图': 'changtuxian'}, 'code': 'tl|6729'}, '锦州': {'sublist': {'古塔': 'gutaqu', '黑山': 'heishanshi', '凌河': 'linghequ', '太和': 'taihequ', '凌海': 'linghaishi', '义县': 'yixian', '松山新区': 'songshanxinqu', '北镇': 'beizhenshi', '经济开发区': 'jingjikaifaq'}, 'code': 'jinzhou|2354'}, '淮南': {'sublist': {}, 'code': 'hn|2319'}, '广州': {'sublist': {'增城': 'zengcheng', '黄埔': 'huangpugz', '广州周边': 'guangzhouzhoubian', '花都': 'huadugz', '海珠': 'haizhu', '南沙周边': 'nanshazhoubian', '东莞': 'dongguanqu', '天河': 'tianhe', '白云': 'baiyun', '佛山': 'foshanqu', '横沥': 'hengligz', '荔湾': 'liwan', '萝岗': 'luoganggz', '番禺': 'panyu', '越秀': 'yuexiu', '南沙': 'nanshagz', '从化': 'conghua', '从化周边': 'conghuazhoubian', '经济开发区': 'jingjikaifaqu'}, 'code': 'gz|3'}, '迪庆': {'sublist': {'德钦': 'deqinxian', '香格里拉': 'xianggelilaxian', '维西傈': 'weixilixian', '迪庆周边': 'diqingzhoubian'}, 'code': 'diqing|9432'}, '澳门': {'sublist': {'路氹城': 'ludangcheng', '圣方济各堂': 'shengfanggetangqu', '望德堂': 'wangdetangqu', '圣安多尼堂区': 'shenganduonitangqu', '花地玛堂': 'huadimatangqu', '澳门周边': 'aomenzhoubian', '大堂': 'datangqu', '嘉模堂': 'jiamotangqu', '风顺堂': 'fengshuntangqu'}, 'code': 'am|9399'}, '娄底': {'sublist': {'新化': 'xinhuaxian', '双峰': 'shuangfengxianld', '冷水江': 'lengshuijiangshild', '娄星': 'louxingqu', '涟源': 'lianyuanshild', '娄底周边': 'loudizb'}, 'code': 'ld|9481'}, '祁东': {'sublist': {'城区': 'qidongxiancq', '其他': 'qidongxianqt'}, 'code': 'qidongxian|5690'}, '枣庄': {'sublist': {'台儿庄': 'taierzhuang', '山亭': 'shanting', '滕州': 'zaozhuangtengzhou', '其他': 'zaozhuangshi', '峄城': 'zzyicheng', '市中区': 'shizhongqu', '薛城': 'xuecheng'}, 'code': 'zaozhuang|961'}, '赣州': {'sublist': {'瑞金': 'ruijin', '信丰': 'xinfengq', '寻乌': 'xunwu', '会昌': 'huichang', '赣县': 'ganxianq', '开发区': 'ganzkfq', '健康路': 'gzjkl', '章江新区': 'ganzzjxq', '安远': 'anyuanq', '南康': 'nankang', '定南': 'dingnan', '石城': 'shicheng', '大余': 'dayuq', '宁都': 'ningdu', '崇义': 'chongyi', '站北区': 'ganzzbq', '兴国': 'xingguo', '上犹': 'shangyou', '于都': 'yudu', '全南': 'quannan', '龙南': 'longnan', '章贡': 'zhanggong'}, 'code': 'ganzhou|2363'}, '舟山': {'sublist': {'嵊泗': 'shengsixian', '岱山': 'daishanxian', '普陀': 'putuoqu', '定海': 'dinghaiqu'}, 'code': 'zhoushan|8481'}, '资兴': {'sublist': {'城区': 'zixingcq', '其他': 'zixingqt'}, 'code': 'zixing|5698'}, '甘孜': {'sublist': {'甘孜周边': 'ganzizhoubian', '丹巴': 'danbaxian', '泸定': 'ludingxian', '康定': 'kangdingxian', '甘孜县': 'ganzixian', '德格': 'degexian'}, 'code': 'ganzi|9764'}, '西双版纳': {'sublist': {'景洪': 'jinggongshi', '勐腊': 'menglaxian', '西双版纳周边': 'xishuangbannazhoubian', '勐海': 'menghaixian'}, 'code': 'bn|2397'}, '湘西': {'sublist': {'龙山': 'longshanx', '吉首': 'jishou', '永顺': 'yongshunx', '古丈': 'guzhang', '泸溪': 'luxix', '凤凰': 'fenghuang', '花垣': 'huayuanx', '保靖': 'baojing', '湘西周边': 'xiangxizhoubian'}, 'code': 'xiangxi|10219'}, '秦皇岛': {'sublist': {'海港': 'haigang', '南戴河': 'ndh', '山海关': 'shanhaiguan', '抚宁': 'funing', '其他': 'qinhuangdao', '北戴河': 'beidaihe', '青龙': 'qinglong', '开发区': 'kfq', '昌黎': 'changli', '卢龙': 'lulong'}, 'code': 'qhd|1078'}, '扬中': {'sublist': {'扬中市区': 'yangzhongshiqu', '其它': 'yangzhongqita'}, 'code': 'yangzhong|649'}, '博兴': {'sublist': {'城区': 'boxingcq', '其他': 'boxingqt'}, 'code': 'boxing|949'}, '佛山': {'sublist': {'禅城': 'chancheng', '南海': 'nanhai', '佛山周边': 'foshan', '顺德': 'shundeshiqu', '三水': 'sanshui', '高明': 'gaoming'}, 'code': 'fs|222'}, '晋江': {'sublist': {'体育中心': 'qztyzx', 'SM广场': 'smguangchang', '阳光广场': 'yangguanggc', '晋江周边': 'jinjiangzb'}, 'code': 'jinjiangshi|297'}, '巴中': {'sublist': {'恩阳': 'enyang', '南江': 'nanjiangxian', '巴中周边': 'bazhongzhoubian', '巴州': 'bazhouqu', '平昌': 'pingchangxian', '经开区': 'jingkaiqubz', '通江': 'tongjiangxian'}, 'code': 'bazhong|9811'}, '敦煌': {'sublist': {'城区': 'dunhuangchengqu', '其他': 'dunhuangqita'}, 'code': 'dunhuang|10390'}, '郴州': {'sublist': {'桂阳': 'czguiyangcz', '北湖': 'beihuqu', '宜章': 'yizhang', '嘉禾': 'jiahe', '资兴': 'zixingcz', '永兴': 'yongxingcz', '苏仙': 'suxian', '临武': 'linwu', '其它': 'chenzhoushi'}, 'code': 'chenzhou|5695'}, '商丘': {'sublist': {'睢县': 'suixiansq', '永城': 'yongchengsq', '柘城': 'zhecheng', '民权': 'minquan', '其他': 'shangqiu', '虞城': 'yucheng', '睢阳': 'suiyang', '宁陵': 'ningling', '夏邑': 'xiayi', '梁园': 'liangyuan'}, 'code': 'sq|1029'}, '新昌': {'sublist': {'城区': 'xinchangcq', '其他': 'xinchangqt'}, 'code': 'xinchang|361'}, '随县': {'sublist': {'城区': 'suixiacq', '其他': 'suixiaqt'}, 'code': 'suixia|9660'}, '当阳': {'sublist': {'城区': 'dangyangcq', '其他': 'dangyangqt'}, 'code': 'dangyang|865'}, '昌乐': {'sublist': {'城区': 'changlecq', '其他': 'changleqt'}, 'code': 'changle|373'}, '无棣': {'sublist': {'城区': 'wudicq', '其他': 'wudiqt'}, 'code': 'wudi|951'}, '邹城': {'sublist': {'凫山街道': 'fushanjiedao', '千泉街道': 'qianquanjiedao', '其他': 'zouchengshiqita', '钢山街道': 'gangshanjiedao'}, 'code': 'zoucheng|455'}, '偃师': {'sublist': {'商城街道': 'shangchengjiedao', '顾县镇': 'guxianzhen', '翟镇镇': 'dizhenzhen', '岳滩镇': 'yuetanzhen', '其他': 'yanshiqita'}, 'code': 'yanshiqu|7121'}, '喀什': {'sublist': {'英吉沙': 'yingjishaxian', '塔什库尔干': 'tashikuergan', '喀什周边': 'kashizhoubian', '喀什': 'kashishi', '莎车': 'shachexian', '麦盖提': 'maigaitixian', '疏附': 'shufuxian', '叶城': 'yechengxian', '泽普': 'zepuxian', '疏勒': 'shulexian', '伽师': 'jiashixian', '岳普湖': 'yuepuhuxian', '巴楚': 'bachuxian'}, 'code': 'ks|9326'}, '长沙': {'sublist': {'岳麓': 'yuelu', '开福': 'kaifu', '天心': 'tianxinqu', '芙蓉': 'furong', '长沙周边': 'changsha', '雨花': 'csyuhua', '望城': 'cswc', '星沙': 'xingsha'}, 'code': 'cs|414'}, '天长': {'sublist': {'天长市区': 'tianchangshiqu', '其它': 'tianchangqita'}, 'code': 'tianchang|10273'}, '武夷山': {'sublist': {'新丰': 'xinfengjie', '五夫镇': 'wufuzhen', '崇安': 'chonganjie', '星村镇': 'xingcunzhen', '武夷': 'wuyijie', '武夷山周边': 'wuyishanzhoubian', '兴田镇': 'xingtianzhen'}, 'code': 'wuyishan|10761'}, '通化': {'sublist': {'通化': 'tonghuax', '集安': 'jian', '通化周边': 'tonghuazhoubian', '东昌': 'dongchang', '辉南': 'huinanx', '梅河口': 'meihekouth', '柳河': 'liuhe', '二道江': 'erdaojiang'}, 'code': 'th|10159'}, '沁阳': {'sublist': {'城区': 'qinyangcq', '其他': 'qinyangqt'}, 'code': 'qinyang|3268'}, '孝感': {'sublist': {'汉川市': 'xiaoganhanchuan', '其他': 'xiaoganqita', '大悟': 'dawuxg', '应城': 'yingcheng', '孝昌': 'xiaochangxg', '云梦': 'yunmengxg', '孝南': 'xiaonan', '安陆': 'anluxg'}, 'code': 'xiaogan|3434'}, '莆田': {'sublist': {'黄瓜岛': 'huangguadao', '南日岛': 'nanridao', '秀屿': 'xiuyuqu', '仙游': 'xianyouxian', '涵江': 'hanjiangqu', '湄洲岛': 'meizhoudao', '城厢': 'chengxiangqu', '荔城': 'lichengqu'}, 'code': 'pt|2429'}, '锡林郭勒': {'sublist': {'西乌珠穆沁旗': 'xwzmqq', '东县': 'dongxian', '苏尼特右旗': 'suniteyouqi', '锡林浩特': 'xilinhaoteshi', '多伦': 'duolunxian', '东乌珠穆沁旗': 'dwzmqq', '阿巴嘎旗': 'abagaqi', '太仆寺旗': 'taipusiqi', '苏尼特左旗': 'sunitezuoqi', '正镶白旗': 'zhengxiangbaiqi', '镶黄旗': 'xianghuangqi', '二连浩特': 'erlianhaoteshi', '正蓝旗': 'zhenglanqi'}, 'code': 'xl|2408'}, '塔城': {'sublist': {'塔城市': 'tacs', '托里': 'tactl', '裕民': 'tacym', '沙湾': 'tacsw', '乌苏市': 'tacwss', '和布克赛尔': 'tachbkse'}, 'code': 'tac|18845'}, '汕头': {'sublist': {'金平': 'jinping', '潮南': 'chaonan', '南澳': 'nanao', '潮阳': 'stchaoyang', '龙湖': 'longhu', '其他': 'shantou', '澄海': 'chenghai', '濠江': 'haojiang'}, 'code': 'st|783'}, '阜阳': {'sublist': {'颍东': 'yingdongqu', '颍泉': 'yingquanqu', '临泉': 'linquanxian', '太和': 'taihex', '颍州': 'yingzhouqu', '阜南': 'funanxian', '界首': 'jieshoushi', '颍上': 'yingshangxian', '经济开发区': 'jingjiq'}, 'code': 'fy|2325'}, '保定': {'sublist': {'新市': 'xinshiqu', '北市': 'beishi', '白沟': 'bdbg', '安国': 'anguo', '高碑店': 'gaobeidian', '南市': 'nanshiqu', '涿州市': 'daodingzhuozhou', '高开': 'gaokaiqu', '定州': 'dingzhoushi', '保定周边': 'baoding'}, 'code': 'bd|424'}, '清徐': {'sublist': {'盂封镇': 'yufengzhen', '西谷乡': 'xiguxiang', '东于镇': 'dongyuzhen', '徐沟镇': 'xugouzhen', '马峪乡': 'mayuxiang', '王答乡': 'wangdaxiang', '柳杜乡': 'liuduxiang', '杨房乡': 'yangfangxiang', '清徐周边': 'qingxuzb', '集义乡': 'jiyixiang', '清源镇': 'qingyuanzhen', '高花乡': 'gaohuaxiang'}, 'code': 'qingxu|10908'}, '范县': {'sublist': {'城区': 'fanxiancq', '其他': 'fanxianqt'}, 'code': 'fanxian|7285'}, '南宁': {'sublist': {'青秀': 'qingxiu', '南宁周边': 'nanning', '邕宁': 'yongning', '兴宁': 'xingning', '江南': 'jiangnan', '良庆': 'liangqing', '西乡塘': 'xixiangtang'}, 'code': 'nn|845'}, '安宁': {'sublist': {'安宁新区': 'anxinqu', '安宁市区': 'anshiqu', '安宁周边': 'anningzb', '昆钢': 'kungang', '太平新城': 'taipingxincheng', '温泉': 'kmwenquan'}, 'code': 'anningshi|547'}, '定州': {'sublist': {'北城': 'beichengqu', '西城': 'xichengqu', '南城': 'nanchengqu', '其他': 'dingzhouqita'}, 'code': 'dingzhou|8398'}, '杭州': {'sublist': {'下城': 'xiacheng', '滨江': 'binjiang', '富阳': 'fuyangshi', '杭州周边': 'hangzhou', '桐庐': 'tonglu', '江干': 'jianggan', '余杭': 'yuhang', '萧山': 'xiaoshan', '淳安': 'chunan', '拱墅': 'gongshu', '建德': 'jiandeshi', '上城': 'hzshangcheng', '西湖': 'xihuqu', '临安': 'linanshi'}, 'code': 'hz|79'}, '西宁': {'sublist': {'城中': 'chengzhong', '城东': 'chengdong', '大通': 'datongxian', '城北': 'chengbeiqu', '城西': 'chengxi', '湟源': 'huangyuan', '湟中': 'huangzhong', '其它': 'xining'}, 'code': 'xn|2052'}, '大竹': {'sublist': {'城区': 'dazucq', '其他': 'dazuqt'}, 'code': 'dazu|9806'}, '昭通': {'sublist': {'昭阳': 'zhaoyangqu', '大关': 'daguanxian', '昭通周边': 'zhaotongzhoubian', '巧家': 'qiaojiaxian', '永善': 'yongshanxian', '彝良': 'yiliangxian', '鲁甸': 'ludianxian'}, 'code': 'zt|9409'}, '平阳': {'sublist': {'昆阳': 'kunyangzhen', '萧江': 'xiaojiangzhen', '宋桥': 'songqiaozhen', '南雁': 'nanyanzhen', '麻步': 'mabuzhen', '榆垟': 'yuyangzhen', '凤卧': 'fengwozhen', '郑楼': 'zhenglouzhen', '顺溪': 'shunxizhen', '水头': 'shuitouzhen', '南麂': 'nanluzhen', '宋埠': 'songbuzhen', '山门': 'shanmenzhen', '平阳周边': 'pingyanzhoubian', '鳌江': 'aojiangzhen', '腾蛟': 'tengjiaozhen', '鹤溪': 'hexizhen', '钱仓': 'qiancangzhen'}, 'code': 'pingyangxian|7575'}, '文昌': {'sublist': {'潭牛镇': 'tanniu', '蓬莱镇': 'penglaiz', '文昌周边': 'wenchangzb', '会文镇': 'huiwen', '重兴镇': 'chongxing', '东路镇': 'donglu', '文城镇': 'wencheng'}, 'code': 'wenchang|9984'}, '石河子': {'sublist': {}, 'code': 'shz|9551'}, '河池': {'sublist': {'河池学院': 'hechixueyuan', '都安': 'duanxian', '东兰': 'donglanxian', '天峨': 'tianexian', '罗城': 'luochengxian', '宜州': 'yizhoushi', '凤山': 'fengshanxian', '环江': 'huanjiangxian', '大化': 'dahuaxian', '金城江': 'jinchengjianqu', '南丹': 'nandanxian', '巴马': 'bamaxian'}, 'code': 'hc|2340'}, '福鼎': {'sublist': {'城区': 'fudingshicq', '其他': 'fudingshiqt'}, 'code': 'fudingshi|7970'}, '福安': {'sublist': {'城区': 'fuanshicq', '其他': 'fuanshiqt'}, 'code': 'fuanshi|7969'}, '贺州': {'sublist': {'昭平': 'zhaoping', '钟山': 'zhongshanx', '八步': 'babu', '平桂': 'pinggui', '富川': 'fuchuan', '贺州周边': 'hezhouzhoubian'}, 'code': 'hezhou|10549'}, '长宁': {'sublist': {'城区': 'changningxcq', '其他': 'changningxqt'}, 'code': 'changningx|7148'}, '云梦': {'sublist': {'城区': 'yunmengcq', '其他': 'yunmengqt'}, 'code': 'yunmeng|3438'}, '阿勒泰': {'sublist': {'福海': 'altfh', '阿勒泰市区': 'altsq', '青河': 'altqh', '富蕴': 'altfy', '布尔津': 'altbej', '吉木乃': 'altjmn', '哈巴河': 'althbh'}, 'code': 'alt|18837'}, '庄河': {'sublist': {}, 'code': 'pld|3306'}, '万宁': {'sublist': {'山根镇': 'snageng', '龙滚镇': 'longgun', '万城镇': 'wangchengz', '和乐镇': 'hele', '大茂镇': 'damao', '后安镇': 'houan', '万宁周边': 'wanningzb'}, 'code': 'wanning|10022'}, '北流': {'sublist': {}, 'code': 'beiliushi|9168'}, '克拉玛依': {'sublist': {'白碱滩': 'baijiantan', '乌尔禾': 'wuerhe', '其它': 'kelamayi', '克拉玛依区': 'kelamayiqu', '独山子': 'dushanzi'}, 'code': 'klmy|2042'}, '大理': {'sublist': {'巍山': 'weishanzizhi', '南涧': 'nanjianzizhi', '漾濞': 'yangxianzizhi', '大理市': 'dalishi', '洱源': 'eryuanxian', '宾川': 'binchuanxian', '弥渡': 'miduxian', '鹤庆': 'heqingxian', '云龙': 'yunlongxian', '剑川': 'jianchuanxian', '祥云': 'xiangyunxian', '永平': 'yongpingxian'}, 'code': 'dali|2398'}, '南昌': {'sublist': {'青云谱': 'qingyunpu', '湾里': 'wailiqu', '南昌县': 'nanchangxian', '小蓝经济开发区': 'ncxl', '高新开发区': 'gaoxinkfq', '西湖': 'xihu', '昌北经济开发区': 'nccbjjkfq', '红谷滩新区': 'honggutanxin', '青山湖': 'qingshanhuqu', '东湖': 'donghu', '新建区': 'xinjian', '南昌周边': 'nanchang', '象湖': 'ncxianghu'}, 'code': 'nc|669'}, '郓城': {'sublist': {'城区': 'hzyccq', '其他': 'hzycqt'}, 'code': 'hzyc|5637'}, '新安': {'sublist': {'城区': 'lyxinancq', '其他': 'lyxinanqt'}, 'code': 'lyxinan|11217'}, '宿迁': {'sublist': {'沭阳': 'sqshuyang', '泗阳县': 'suqiansiyang', '泗洪县': 'suqiansihong', '宿豫/宿城': 'sucheng'}, 'code': 'suqian|2350'}, '安阳': {'sublist': {'北关': 'beiguan', '龙安': 'longan', '其他': 'anyangqita', '殷都': 'yindou', '安阳': 'anyangxian', '文峰': 'wenfeng', '林州': 'linzhouay'}, 'code': 'ay|1096'}, '齐齐哈尔': {'sublist': {'泰来': 'tailai', '龙沙': 'longsha', '铁锋': 'tiefeng', '富拉尔基': 'fulaerji', '碾子山': 'nianzishan', '建华': 'jianhua', '梅里斯': 'meilisi', '讷河': 'nehe', '昂昂溪': 'angangxi', '其它': 'qqhe'}, 'code': 'qqhr|5853'}, '巨野': {'sublist': {'城区': 'juyecq', '其他': 'juyeqt'}, 'code': 'juye|5640'}, '佳木斯': {'sublist': {'永红': 'yonghongqu', '汤原': 'tangyuanxian', '桦南': 'huananxian', '郊区': 'jiaoqu', '同江': 'tongjiangshi', '东风': 'dongfengqu', '富锦': 'fujinshi', '抚远': 'fuyuanxian', '向阳': 'xiangyq', '前进': 'qianjinqu', '桦川': 'huachuanxian'}, 'code': 'jms|6776'}, '青岛': {'sublist': {'城阳': 'chengyang', '即墨': 'jimo', '胶南': 'jiaonan', '李沧': 'licang', '平度': 'pingdu', '市南': 'shinan', '市北': 'shibei', '莱西': 'laixi', '黄岛': 'huangdao', '胶州': 'jiaozhou', '崂山': 'laoshan', '四方': 'sifang', '青岛周边': 'qingdao'}, 'code': 'qd|122'}, '神农架': {'sublist': {'红坪镇': 'hongpingzhen', '阳日镇': 'yangrizhen', '松柏镇': 'songbozhen', '木鱼镇': 'muyuzhen', '神农架周边': 'shennongjiazb'}, 'code': 'snj|9605'}, '长治': {'sublist': {'郊区': 'jiaoqushi', '壶关': 'huguanxian', '城区': 'chengqushi', '襄垣': 'xiangyuanxiancz', '长子': 'zhangzixian', '沁县': 'qinxian', '长治县': 'changzhixian', '武乡': 'wuxiangxian', '平顺': 'pingshunxian', '潞城': 'luchengshi', '沁源': 'qinyuanxian', '屯留': 'tunliuxian', '黎城': 'lichengxian'}, 'code': 'changzhi|6921'}, '阳谷': {'sublist': {'博济桥街道': 'lcbjqjd', '侨润街道': 'lcqrjd', '狮子楼街道': 'lcszljd'}, 'code': 'yanggu|886'}, '珠海': {'sublist': {'坦洲': 'zhtanzhou', '香洲': 'xiangzhou', '横琴': 'zhhq', '珠海周边': 'zhuhai', '高新区': 'zhgxq', '斗门': 'doumen', '金湾': 'jinwan'}, 'code': 'zh|910'}, '巢湖': {'sublist': {'巢湖周边': 'chaohuzhoubian', '居巢': 'juchao', '庐江': 'lujiang'}, 'code': 'ch|10229'}, '仁怀': {'sublist': {'鲁班街道': 'lubanjiedao', '盐津街道': 'yanjinjiedao', '其他': 'renhuaishiqita', '中枢街道': 'zhongshujiedao', '坛厂街道': 'tanchangjiedao', '苍龙街道': 'canglongjiedao'}, 'code': 'renhuaishi|7628'}, '鄂尔多斯': {'sublist': {'准格尔旗': 'zhungeerqi', '鄂托克前旗': 'etuokeqianqi', '达拉特旗': 'dalateqi', '东胜': 'dongshengqu', '鄂托克旗': 'etuokeqi', '康巴什区': 'kangbsq', '其它': 'eerduosi', '乌审旗': 'wushenqi', '杭锦旗': 'hangjinqi', '伊金霍洛旗': 'yijinhuoluoqi'}, 'code': 'erds|2037'}, '莒县': {'sublist': {'城区': 'lvxianchengqu', '其他': 'lvxianqita'}, 'code': 'juxian|3180'}, '梅河口': {'sublist': {}, 'code': 'meihekou|10162'}, '聊城': {'sublist': {'莘县': 'shenxianlc', '阳谷': 'yanggulc', '其他': 'liaocheng', '冠县': 'guanxianlc', '东昌府': 'dongchangfu', '高唐': 'gaotanglc', '茌平县': 'liaochengchiping', '开发区': 'lckfq', '东阿': 'donga', '临清县': 'liaochenglinqing'}, 'code': 'lc|882'}, '句容': {'sublist': {'城区': 'jurongchengqu', '其他': 'jurongqita'}, 'code': 'jurong|650'}, '公主岭': {'sublist': {'秦家屯': 'qinjiatun', '大榆树镇': 'dayushuzhen', '公主岭': 'gongzhulingshiqu', '怀德镇': 'huaidezhen', '范家屯': 'gzlfanjiatun', '其他': 'gongzhulingshiqita', '双城堡': 'shuangchengbao'}, 'code': 'gongzhuling|10171'}, '宜城': {'sublist': {'城区': 'yichengshicq', '其他': 'yichengshiqt'}, 'code': 'yichengshi|897'}, '常州': {'sublist': {'戚墅堰': 'qishuyan', '武进': 'wujin', '新北': 'xinbei', '金坛': 'changzhoujintan', '常州周边': 'changzhou', '天宁': 'tianning', '溧阳': 'liyangqu', '钟楼': 'zhonglou'}, 'code': 'cz|463'}, '鸡西': {'sublist': {'麻山': 'mashanquxian', '鸡冠': 'jiguanqu', '恒山': 'hengshanqu', '梨树': 'lishuqu', '密山': 'mishanshi', '滴道': 'didaoqu', '虎林': 'hulinshi', '鸡东': 'jidongxian', '城子河': 'chengzihequ'}, 'code': 'jixi|7289'}, '漯河': {'sublist': {'高新区': 'gaoxinqu', '舞阳': 'wuyangxian', '临颍': 'linyingxian', '源汇': 'yuanhuiqu', '郾城': 'yanchengqu', '召陵': 'zhaolingqu'}, 'code': 'luohe|2347'}, '巴音郭楞': {'sublist': {'且末': 'bygljm', '若羌': 'byglrq', '轮台': 'luntx', '尉犁': 'weilx', '库尔勒': 'kuerleshi', '焉耆': 'yanqx', '博湖': 'byglbh', '和硕': 'byglhs', '和静': 'hejx', '巴州周边': 'bazhouzhoubian'}, 'code': 'bygl|9530'}, '浮梁': {'sublist': {'城区': 'fuliangxiancq', '其他': 'fuliangxianqt'}, 'code': 'fuliangxian|9071'}, '东阳': {'sublist': {'卢宅': 'jhdylz', '东阳周边': 'jhdyzb', '横店': 'jhdyhd', '城东': 'jhdycd', '江北': 'jhdyjb', '东阳市区': 'jhdysq'}, 'code': 'dongyang|536'}, '永城': {'sublist': {'城区': 'yongchengcq', '其他': 'yongchengqt'}, 'code': 'yongcheng|1032'}, '天门': {'sublist': {'岳口街道': 'yuekoujiedao', '杨林街道': 'yanglinjiedao', '竟陵街道': 'jinglingjiedao', '候口街道': 'houkoujiedao', '天门周边': 'tianmenzb'}, 'code': 'tm|9517'}, '常德': {'sublist': {'武陵': 'wuling', '津市': 'jinshi', '汉寿': 'hanshou', '鼎城': 'dingcheng', '临澧': 'linli', '德山': 'deshancd', '澧县': 'lixiancd', '石门': 'shimen', '其他': 'changdeshi', '安乡': 'anxiang', '桃源': 'taoyuan'}, 'code': 'changde|872'}, '杞县': {'sublist': {'城关镇': 'chengguanzhen', '泥沟乡': 'nigouxiang', '五里河镇': 'wulihezhen', '其他': 'qixianqita'}, 'code': 'qixianqu|7389'}, '七台河': {'sublist': {'新兴': 'xinxing', '勃利': 'boli', '七台河周边': 'qitaihezb', '桃山': 'taoshan', '茄子河': 'qiezihe'}, 'code': 'qth|9848'}, '防城港': {'sublist': {'上思': 'shangshi', '防城港周边': 'fangchenggangzhoubian', '港口': 'gangkou', '东兴': 'dongxings', '防城': 'fangcheng'}, 'code': 'fcg|10539'}, '迁安': {'sublist': {}, 'code': 'qianan|284'}, '龙岩': {'sublist': {'长汀': 'changtingxian', '永定': 'yongdingxian', '武平': 'wupingxian', '漳平': 'zhangpingshi', '上杭': 'shanghangxianly', '新罗': 'xinluoqu', '连城': 'lianchengxian'}, 'code': 'ly|6752'}, '白沙': {'sublist': {'打安镇': 'daanzh', '白沙周边': 'baishazb', '牙叉镇': 'yacha', '邦溪镇': 'bangxi', '七坊镇': 'qifang'}, 'code': 'baish|10380'}, '酒泉': {'sublist': {'酒泉': 'jiuquan', '阿克塞': 'akesai', '玉门': 'yumen', '酒泉周边': 'jiuquanzhoubian', '金塔': 'jinta', '肃北': 'subei', '安西': 'anxi', '敦煌': 'jqdunhuang'}, 'code': 'jq|10387'}, '阳春': {'sublist': {'陂面镇': 'pomianzhen', '八甲镇': 'bajiazhen', '河口镇': 'hekouzhen', '石望镇': 'shiwangzhen', '圭岗镇': 'guigangzhen', '岗美镇': 'gangmeizhen', '双窖镇': 'shuangjiaozhen', '三甲镇': 'sanjiazhen', '永宁镇': 'yongningzhen', '马水镇': 'mashuizhen', '春城镇': 'chuncheng', '合水镇': 'heshuizhen', '春湾镇': 'chunwanzhen', '河塱镇': 'helangzhen', '潭水镇': 'tanshuizhen', '松柏镇': 'songbaizhen'}, 'code': 'yangchun|8566'}, '苏州': {'sublist': {'高新区': 'sugaoxinqu', '吴中': 'wuzhongqu', '沧浪': 'canglang', '平江': 'pingjiangqu', '工业园': 'gongyeyuan', '昆山': 'suzhoukunshan', '相城': 'xiangchengqua', '太仓': 'taicangshi', '常熟': 'changshushi', '苏州周边': 'suzhouqita', '吴江': 'wujiangshi', '金阊': 'jinchangquyu', '张家港': 'zhangjiagangshi'}, 'code': 'su|5'}, '吉林': {'sublist': {'磐石': 'panshijl', '吉林周边': 'jljilin', '桦甸': 'huadianjl', '船营': 'chuanying', '龙潭': 'longtan', '昌邑': 'changyi', '蛟河': 'jiaohe', '舒兰': 'shulan', '丰满': 'fengman', '永吉': 'yongj'}, 'code': 'jl|700'}, '邳州': {'sublist': {'邳州市区': 'pizhoushiqu', '其它': 'pizhouqita'}, 'code': 'pizhou|477'}, '孟津': {'sublist': {'城区': 'mengjinqucq', '其他': 'mengjinquqt'}, 'code': 'mengjinqu|7122'}, '沧县': {'sublist': {'城区': 'cangxiancq', '其他': 'cangxianqt'}, 'code': 'cangxian|659'}, '鄂州': {'sublist': {'鄂州周边': 'erzhouzb', '梁子湖': 'liangzihuqu', '华容': 'huarongqu', '鄂城区': 'erchengqu'}, 'code': 'ez|9709'}, '辽源': {'sublist': {'龙山': 'longshan', '西安区': 'liaoyuanxaq', '东辽': 'dongliao', '东丰': 'dongfengxian', '其它': 'liaoyuanqita'}, 'code': 'liaoyuan|2501'}, '东莞': {'sublist': {'凤岗': 'fenggang', '寮步': 'liaobu', '望牛墩': 'wangniud', '谢岗': 'xiegang', '樟木头': 'zhangmutou', '麻涌': 'macong', '高埗': 'gaobus', '松山湖': 'songsh', '道滘': 'daojiao', '企石': 'qishis', '大朗': 'dalang', '清溪': 'qingxi', '石龙': 'shilongs', '洪梅': 'hongmei', '横沥': 'hengl', '东莞周边': 'dongguan', '桥头': 'qiaotouz', '其它': 'dongguanshi', '中堂': 'zhongt', '厚街': 'houjie', '长安': 'changanqv', '沙田': 'shatianz', '南城': 'nancheng', '东城': 'dongchengqv', '塘厦': 'tangsha', '万江': 'wanjiang', '虎门': 'humen', '东坑': 'dongk', '莞城': 'guanchengshi', '石排': 'ship', '石碣': 'shijie', '常平': 'changpingshi', '茶山': 'chashans', '黄江': 'huangjiang', '大岭山': 'dalingshan'}, 'code': 'dg|413'}, '沂源': {'sublist': {'城区': 'yiyuanxiancq', '其他': 'yiyuanxianqt'}, 'code': 'yiyuanxian|7334'}, '雅安': {'sublist': {'宝兴': 'baoxingxian', '汉源': 'hanyuanxian', '雨城': 'yuchengqu', '名山': 'mingshanxian', '雅安周边': 'yaanzhoubian', '芦山': 'lusx', '石棉': 'shimianxian', '天全': 'tianquanxian', '荥经': 'xingjingxian'}, 'code': 'ya|9687'}, '玉溪': {'sublist': {'元江': 'yuanjiang', '新平': 'xinpingxian', '易门': 'yimen', '红塔': 'hongta', '澄江': 'chengjiang', '华宁': 'huaning', '通海': 'tonghai', '江川': 'jiangchuan', '峨山': 'eshanxian', '其它': 'yuxi'}, 'code': 'yx|2040'}, '信阳': {'sublist': {'息县': 'xixianqu', '浉河': 'shihequ', '信阳市区': 'xinyangshi', '淮滨': 'huaibinxianxy', '潢川': 'huangchuanxian', '罗山': 'luoshanxian', '平桥': 'pingqiaoqu', '新县': 'xinxian', '商城': 'shangchengquq', '固始': 'gushixiangs', '羊山新区': 'yangshanxinqu', '光山': 'guangshanxian'}, 'code': 'xy|8694'}, '芜湖': {'sublist': {'南陵': 'nanling', '无为': 'whwuwei', '其他': 'wuhuqita', '鸠江': 'jiujiangqu', '弋江': 'yijiang', '镜湖': 'jinghu', '芜湖县': 'wuhuxian', '三山': 'sanshan', '繁昌': 'fanchang'}, 'code': 'wuhu|2045'}, '新沂': {'sublist': {'新沂市区': 'xinyishiqu', '其它': 'xinyiqita'}, 'code': 'xinyishi|478'}, '永康': {'sublist': {'永康市区': 'jhyksq', '西城街道': 'xichengjiedao', '永康周边': 'jhykzb', '其他': 'yongkangshiqita', '芝英街道': 'zhiyingjiedao', '东城街道': 'ykdongchengjiedao', '江南街道': 'ykjiangnanjiedao'}, 'code': 'yongkang|537'}, '玉树': {'sublist': {'杂多': 'zaduo', '玉树周边': 'yushuzhoubian', '囊谦': 'nangqian', '治多': 'zhiduo', '称多': 'chengduo', '玉树': 'yushux', '曲麻莱': 'qumalai'}, 'code': 'ys|9888'}, '涟源': {'sublist': {'城区': 'lianyuanshicq', '其他': 'lianyuanshiqt'}, 'code': 'lianyuanshi|9471'}, '正定': {'sublist': {'正定镇': 'zhengding', '诸福屯镇': 'zhufutun', '南楼乡': 'nanlou', '其他': 'zhengdingshi', '新安镇': 'xinan', '曲阳桥乡': 'quyangqiao', '南牛乡': 'nanniu', '北早现乡': 'beizaoxian', '新城铺镇': 'xinchengpu'}, 'code': 'zd|3198'}, '南平': {'sublist': {'顺昌': 'shunchang', '延平': 'yanping', '建瓯': 'jianou', '武夷山': 'wuyishanshi', '南平周边': 'nanpingzhoubian', '邵武': 'shaowu', '建阳': 'jianyangs'}, 'code': 'np|10291'}, '临夏': {'sublist': {'积石': 'jishixian', '永靖': 'yongjingxian', '东乡': 'dongxiangxian', '康乐': 'kanglexian', '广河': 'guanghexian', '和政': 'hezhengxian', '临夏': 'linxiaxian', '临夏市': 'linxialxs'}, 'code': 'linxia|7112'}, '龙口': {'sublist': {'东海': 'ytdh', '西城区': 'ytxcq', '南山': 'ytns', '新区': 'ytxq', '东城区': 'ytdcq'}, 'code': 'longkou|233'}, '清远': {'sublist': {'连山': 'lianshanxian', '佛冈': 'fogangxian', '清新': 'qingxinxian', '连州': 'lianzhoushi', '英德': 'yingdeshi', '连南': 'liannanxian', '清城': 'qingchengqu', '阳山': 'yangshanxian'}, 'code': 'qingyuan|7303'}, '庆阳': {'sublist': {'合水': 'heshui', '正宁': 'zhengning', '镇原': 'zheny', '宁县': 'ningx', '西峰': 'xifengq', '环县': 'huanx', '庆阳周边': 'qingyangzhoubian', '华池': 'huachi', '庆城': 'qingcheng'}, 'code': 'qingyang|10475'}, '三河': {'sublist': {'李旗庄镇': 'liqizhuangzhen', '齐心庄镇': 'qixinzhuangzhen', '高楼镇': 'gaolouzhen', '其他': 'sanheshiqita', '泃阳镇': 'juyangzhen'}, 'code': 'sanhe|776'}, '临朐': {'sublist': {'城区': 'linqucq', '其他': 'linquqt'}, 'code': 'linqu|374'}, '黄南': {'sublist': {'尖扎': 'jianzha', '泽库': 'zeku', '河南县': 'henanx', '同仁': 'tongren', '黄南周边': 'huangnanzhoubian'}, 'code': 'huangnan|9896'}, '绥化': {'sublist': {'望奎': 'shwangkui', '肇东': 'shzhaodongxian', '兰西': 'shlanxi', '安达': 'shandaxian', '庆安': 'shqingan', '绥棱': 'shsuileng', '青冈': 'shqinggang', '海伦': 'shhailun', '明水': 'shmingshui', '北林': 'shbeilin'}, 'code': 'suihua|6718'}, '营口': {'sublist': {'盖州': 'gaizhou', '站前': 'zhanqianqu', '大石桥': 'dashiqiao', '西市': 'xishi', '熊岳镇': 'xiongyuezhen', '老边': 'laobian', '鲅鱼圈': 'bayuquan', '其它': 'yingkou'}, 'code': 'yk|5898'}, '桐乡': {'sublist': {'桐乡周边': 'tongxzb', '濮院': 'jxpy', '东栅': 'dongsh', '博物馆': 'bowwg', '乌镇': 'wuzh', '桐乡市区': 'tongxsq', '西栅': 'xish'}, 'code': 'tongxiang|502'}, '扶余': {'sublist': {'城区': 'fuyuxiancq', '其他': 'fuyuxianqt'}, 'code': 'fuyuxian|9085'}, '黔东南': {'sublist': {'黎平': 'liping', '三穗': 'sansui', '天柱': 'tianzhux', '剑河': 'jianhe', '榕江': 'rongjiang', '黔东南周边': 'qdnzhoubian', '凯里': 'kaili', '黄平': 'huangping', '镇远': 'zhenyuan', '雷山': 'leishan', '麻江': 'majiang', '台江': 'taijiangx', '丹寨': 'danzhai', '施秉': 'shibing', '岑巩': 'cengong', '从江': 'congjiang', '锦屏': 'jinpingx'}, 'code': 'qdn|9363'}, '潮州': {'sublist': {'潮州周边': 'chaozhouzhoubian', '饶平': 'raoping', '潮安': 'chaoan', '湘桥': 'xiangqiao', '枫溪': 'fengxi'}, 'code': 'chaozhou|10461'}, '渠县': {'sublist': {'城区': 'quxcq', '其他': 'quxqt'}, 'code': 'qux|9807'}, '邯郸': {'sublist': {'复兴': 'fuxing', '邯郸县': 'handanxian', '成安县': 'cax', '永年县': 'yongnian', '邯山': 'hanshan', '高开区': 'gkq', '峰峰矿区': 'fengfengkuang', '邯郸周边': 'handan', '魏县': 'weix', '武安市': 'handanwuan', '肥乡县': 'feixx', '磁县': 'cixianhd', '丛台': 'congtai', '临漳县': 'linzhang', '涉县': 'shexianhd', '大名县': 'dmx'}, 'code': 'hd|572'}, '嘉善': {'sublist': {'天壬镇': 'tianrenzhen', '惠民街道': 'huiminjiedao', '大云镇': 'dayunzhen', '梅花庵': 'meihuannew', '西塘': 'xitangnew', '大云温泉': 'dywqnew', '陶庄镇': 'taozhuangz', '丁栅湿地': 'dssd', '魏塘街道': 'weitangjiedao', '干窑镇': 'ganyaozhen', '姚庄镇': 'yaozhuangz', '罗星街道': 'luoxingjiedao'}, 'code': 'jiashanx|14357'}, '临沧': {'sublist': {'镇康': 'zhentang', '临翔': 'linx', '沧源': 'cangyuan', '凤庆': 'fengqing', '临沧周边': 'lincangzhoubian', '耿马': 'gengma', '永德': 'yongde', '云县': 'yunx', '双江': 'shuanjiang'}, 'code': 'lincang|9422'}, '梁山': {'sublist': {'城区': 'liangshanxcq', '其他': 'liangshanxqt'}, 'code': 'liangshanx|462'}, '张家口': {'sublist': {'高新区': 'zjkgaoxin', '张北县': 'zhangbeixian', '蔚县': 'weixian', '桥东': 'zjkqiaodong', '宣化区': 'xuanhua', '宣化县': 'xuanhuaxian', '其他': 'zhangjiakou', '怀来': 'huailai', '桥西': 'zjkqiaoxi', '万全': 'wanquanxian'}, 'code': 'zjk|3328'}, '屯昌': {'sublist': {'屯城镇': 'tuncheng', '新兴镇': 'xinxingzh', '枫木镇': 'fengmu', '屯昌周边': 'tunchangzb', '乌坡镇': 'wupo', '坡心镇': 'poxin', '南吕镇': 'nanlv', '南坤镇': 'nankun', '西昌镇': 'xichang'}, 'code': 'tunchang|10044'}, '日土': {'sublist': {}, 'code': 'rituxian|9682'}, '海丰': {'sublist': {}, 'code': 'haifengxian|9444'}, '陇南': {'sublist': {'武都': 'wudu', '两当': 'liangdang', '陇南周边': 'longnanzhoubian', '宕昌': 'dangchang', '徽县': 'huix', '文县': 'wenx', '成县': 'chengx'}, 'code': 'ln|10415'}, '广安': {'sublist': {'邻水': 'linshuixian', '武胜': 'wushengxian', '广安城南': 'guanganchengnan', '广安城北': 'guanganchengbei', '广安': 'guangan', '华蓥': 'huayingshi', '岳池': 'yuechixian', '其他': 'qitaq'}, 'code': 'ga|2381'}, '钦州': {'sublist': {'浦北': 'pubeixian', '钦南': 'qinnanqu', '灵山': 'lingshanxian', '钦北': 'qinbeiqu', '市区': 'qzshiqu'}, 'code': 'qinzhou|2335'}, '德清': {'sublist': {'德清市区': 'deqingshiqu', '其它': 'deqingqita'}, 'code': 'deqing|835'}, '岑溪': {'sublist': {'城区': 'cenxicq', '其他': 'cenxiqt'}, 'code': 'cenxi|2119'}, '牡丹江': {'sublist': {'西安': 'muxian', '穆棱': 'muling', '海林': 'hailin', '爱民': 'aimin', '其他': 'mudanjiang', '宁安': 'ninganshi', '东宁县': 'mdjdnx', '绥芬河': 'suifenhe', '林口县': 'mdjlkx', '阳明': 'yangming', '东安': 'dongan'}, 'code': 'mdj|3489'}, '嵊州': {'sublist': {'城区': 'shengzhoucq', '其他': 'shengzhouqt'}, 'code': 'shengzhou|359'}, '馆陶': {'sublist': {'房寨镇': 'fangzhaizhen', '南徐村乡': 'nanxucun', '馆陶镇': 'guantaozhen', '寿山寺乡': 'shoushansi', '王桥乡': 'wangqiaoxiang', '柴堡镇': 'chaibuzhen', '馆陶': 'guantaoxian', '路桥乡': 'luqiaoxiang', '魏僧寨镇': 'weizengzhai'}, 'code': 'gt|8706'}, '泰兴': {'sublist': {'泰兴市区': 'taixinshiqu', '其它': 'taixinqita'}, 'code': 'taixing|696'}, '固原': {'sublist': {'固原': 'guyuanshi', '彭阳': 'pengyangxian', '原州': 'yuanzhouqu', '海原': 'haiyuanxian', '泾源': 'jingyuanxian', '西吉': 'xijixian', '隆德': 'longdexian', '经济开发区': 'jingjikaifa'}, 'code': 'guyuan|2421'}, '洛阳': {'sublist': {'西工': 'xigongqu', '洛阳周边': 'luoyangshi', '吉利': 'jiliqu', '宜阳': 'lyyiyangly', '涧西': 'jianxi', '洛龙': 'luolong', '汝阳': 'ruyang', '偃师市': 'luoyangyanshi', '伊川': 'yichuanly', '伊滨': 'yibin', '瀍河': 'chanhehuizu', '老城': 'laocheng'}, 'code': 'luoyang|556'}, '荆州': {'sublist': {'荆州': 'jingjingzhou', '沙市': 'shashiqu', '其他': 'jingzhouqita', '石首': 'shishou', '江陵': 'jiangling', '公安': 'gongan', '松滋': 'songzijz', '监利': 'jianli', '洪湖': 'honghu'}, 'code': 'jingzhou|3479'}, '玉田': {'sublist': {'城区': 'yutianxiancq', '其他': 'yutianxianqt'}, 'code': 'yutianxian|7060'}, '诸城': {'sublist': {'百尺河镇': 'baichihe', '石桥子镇': 'shiqiaozi', '舜王街道': 'shunwangj', '龙都街道': 'longduj', '贾悦镇': 'jiayuez', '皇华镇': 'huanghuaz', '辛兴镇': 'xinxingz', '昌城镇': 'changchengz', '密州街道': 'mizhouj', '桃林乡': 'taolinx', '枳沟镇': 'zhigou', '程戈庄镇': 'chenggezhuang', '相州镇': 'xiangzhouz'}, 'code': 'zc|9146'}, '鞍山': {'sublist': {'岫岩': 'xiuyan', '千山': 'qianshan', '铁西': 'tiexi', '海城': 'haicheng', '铁东': 'tiedong', '鞍山周边': 'anshan', '台安': 'taianxian', '立山': 'lishan'}, 'code': 'as|523'}, '丹东': {'sublist': {'振安': 'zhenan', '凤城': 'fengchengdd', '元宝': 'yuanbao', '振兴': 'zhenxing', '其他': 'dandongqita', '宽甸': 'kuandian', '东港': 'donggang'}, 'code': 'dandong|3445'}, '定安': {'sublist': {'龙湖镇': 'longhuz', '黄竹镇': 'huangzhu', '龙门镇': 'longmenz', '定安周边': 'dinganzb', '雷鸣镇': 'leiming', '定城镇': 'dingchengz', '新竹镇': 'xinzhuz'}, 'code': 'da|10303'}, '河源': {'sublist': {'东源': 'dongyuanx', '河源周边': 'heyuanzhoubian', '紫金': 'zijin', '龙川': 'longchuan', '和平县': 'hepingx', '连平': 'lianping', '源城': 'yuancheng'}, 'code': 'heyuan|10467'}, '朝阳': {'sublist': {'建平': 'jiangping', '北票': 'beipiaocy', '龙城': 'longcheng', '双塔': 'shuangtaq', '喀喇沁': 'kalaqin', '朝阳县': 'chaoyangx', '凌源': 'lingyuan', '朝阳周边': 'chaoyangzhoub'}, 'code': 'cy|10106'}, '宜都': {'sublist': {'宜都市区': 'yidoushiqu', '其它': 'yidouqita'}, 'code': 'yidou|864'}, '松滋': {'sublist': {'城区': 'songzicq', '其他': 'songziqt'}, 'code': 'songzi|3484'}, '平顶山': {'sublist': {'平顶山周边': 'pingdingshan', '石龙': 'shilong', '舞钢': 'wugangpds', '湛河': 'zhanhe', '新华': 'xinhuaqu', '汝州市': 'pingdingshanruzhou', '卫东': 'weidong'}, 'code': 'pds|1005'}, '咸阳': {'sublist': {'武功': 'wugongxian', '淳化': 'chunhuaxian', '礼泉': 'liquanxian', '长武': 'changwuxian', '旬邑': 'xunyixian', '泾阳': 'jingyangxian', '兴平': 'sanpingshi', '三原': 'sanyuanxian', '秦都': 'qinduqu', '渭城': 'weichengquyu', '永寿': 'yongshouxian', '彬县': 'xybinxian', '乾县': 'qianxian'}, 'code': 'xianyang|7453'}, '宜春': {'sublist': {'袁州': 'yuanzhou', '上高': 'shanggao', '奉新': 'fengxin', '万载': 'wangzai', '樟树': 'zhangshuyc', '高安': 'gaoanyc', '丰城': 'fengchengshiyc', '宜丰': 'yifeng', '其它': 'yichunshi'}, 'code': 'yichun|5709'}, '桓台': {'sublist': {'少海公园': 'zbshgy', '世纪中学': 'zbsjzx', '索镇街道': 'suozhenjiedao', '东岳路': 'zbdyl', '第二小学': 'zbdexx', '少海街道': 'shaohaijiedao', '少海路': 'zbshl', '喜乐佳': 'zbxlj', '信誉楼': 'zbxyl', '实验中学': 'zbsyzx', '桓台一中': 'zbhengtaiyizhong', '兴桓路': 'zbxhl', '老公园巡警大队': 'zblgyxjdd', '公安街': 'zbgaj', '渔洋街': 'zbyyj', '建校': 'zbjx', '红莲湖': 'zbhlh', '第一小学': 'zbdyxx', '桓台银座': 'zbhtyz', '镇南大街': 'zbzndj', '桓台二中': 'zbhengtaierzhong', '建设街': 'zbjsj', '惠仟佳': 'zbhqj', '车站': 'zbht', '其他': 'zbhtqt', '张北路': 'zbzbl', '中心路': 'zbzxl'}, 'code': 'huantaixian|7335'}, '靖边': {'sublist': {'城区': 'jingbianchengqu', '其他': 'jingbianqita'}, 'code': 'jingbian|5947'}, '宁阳': {'sublist': {'西关': 'taianxg', '南关': 'taiannanguan', '宁阳一中': 'taiannyyz', '北关': 'taianbg', '四中': 'taiansz', '东关': 'taiandg', '宁阳县周边': 'ningyxzb', '文庙街道': 'wenmjd', '县政府': 'taianxzf', '八仙桥街道': 'bxqjd'}, 'code': 'ningyang|691'}, '蚌埠': {'sublist': {}, 'code': 'bengbu|3470'}, '莱州': {'sublist': {'城港路街道': 'chengganglujiedao', '文昌路街道': 'wenchanglujiedao', '其他': 'laizhoushiqita', '文峰路街道': 'wenfenglujiedao', '永安路街道': 'yonganlujiedao', '三山岛街道': 'sanshandaojiedao', '金仓街道': 'jincangjiedao'}, 'code': 'laizhou|235'}, '伊川': {'sublist': {'城区': 'yichuancq', '其他': 'yichuanqt'}, 'code': 'yichuan|11220'}, '济宁': {'sublist': {'市中': 'jnshizhongqu', '汶上': 'wenshangjn', '泗水': 'sishui', '兖州': 'yanzhou', '嘉祥': 'jiaxiang', '邹城': 'jiningzoucheng', '鱼台': 'yutai', '任城': 'rencheng', '济宁周边': 'jiningshi', '北湖新区': 'jiningbhxq', '曲阜': 'qufu', '微山': 'weishanjn', '高新区': 'jininggxq', '金乡': 'jinxiang', '梁山': 'liangshanxjn'}, 'code': 'jining|450'}, '衡水': {'sublist': {'饶阳': 'raoyang', '枣强': 'zaoqiang', '深州': 'hsshenzhou', '其他': 'hengshui', '阜城': 'fucheng', '武邑县': 'hswy', '景县': 'jingxian', '故城': 'guchengxian', '开发区': 'kaifq', '安平': 'anping', '武强': 'wuqiang', '桃城': 'taocheng', '冀州': 'jizhou'}, 'code': 'hs|993'}, '海门': {'sublist': {'海门市区': 'haimenshiqu', '其它': 'haimenqita'}, 'code': 'haimen|399'}, '灌南': {'sublist': {'城区': 'guannanchengqu', '其他': 'guannanxianqita'}, 'code': 'guannan|2150'}, '无为': {'sublist': {'城区': 'wuweichengqu', '其他': 'wuweiqita'}, 'code': 'wuweixian|10232'}, '嘉峪关': {'sublist': {'镜铁山矿区': 'jingtieshan', '前进': 'qianj', '嘉峪关周边': 'jiayuguanzhoubian', '新华': 'xinhua', '五一': 'wuyi', '胜利': 'shengl', '建设': 'jians'}, 'code': 'jyg|10362'}, '格尔木': {'sublist': {'城区': 'geermushicq', '其他': 'geermushiqt'}, 'code': 'geermushi|9904'}, '湛江': {'sublist': {'其他': 'zhanjiangshi', '坡头': 'potou', '遂溪': 'suixixian', '廉江': 'lianjiang', '霞山': 'xiashan', '赤坎': 'chikan', '麻章': 'mazhang', '吴川': 'wuchuanshi', '开发区': 'kaifaq', '雷州': 'leizhou', '徐闻': 'xuwenxian'}, 'code': 'zhanjiang|791'}, '黔南': {'sublist': {'独山': 'dushan', '三都': 'sandushuizu', '罗甸': 'luodian', '龙里': 'longli', '都匀': 'duyun', '平塘': 'pingtang', '福泉': 'fuquan', '黔南周边': 'qiannanzb', '瓮安': 'wengan', '贵定': 'guiding', '长顺': 'changshun', '惠水': 'huishui', '荔波': 'libo'}, 'code': 'qn|10492'}, '无锡': {'sublist': {'惠山': 'huishanq', '宜兴': 'yixingshi', '南长': 'nanchangqu', '崇安': 'chongan', '新区': 'wxxinqu', '无锡周边': 'wuxi', '北塘': 'beitang', '江阴': 'jiangyin', '锡山': 'xishanqu', '滨湖': 'binhu'}, 'code': 'wx|93'}, '武汉': {'sublist': {'沌口开发区': 'whtkfq', '汉南': 'hannan', '青山': 'whqingshanqu', '硚口': 'qiaokou', '江夏': 'jiangxia', '武汉周边': 'wuhan', '蔡甸': 'caidian', '江岸': 'jiangan', '江汉': 'jianghan', '武昌': 'wuchang', '新洲': 'xinzhouqu', '东西湖': 'dongxihu', '洪山': 'hongshan', '汉阳': 'hanyang', '黄陂': 'huangpo'}, 'code': 'wh|158'}, '燕郊': {'sublist': {'潮白河': 'lfcbh', '城区': 'lfcq', '东市区': 'lfdsq', '其他': 'yanjiaoqita', '迎宾路': 'lfybl', '燕郊镇': 'yanjiaozhen', '燕顺路': 'lfysl', '大厂': 'lfdc'}, 'code': 'lfyanjiao|12730'}, '孟州': {'sublist': {'城区': 'mengzhoucq', '其他': 'mengzhouqt'}, 'code': 'mengzhou|3267'}, '合肥': {'sublist': {'经开': 'hfjingkai', '新站': 'hfxinzhan', '北城新区': 'hfbcxq', '包河': 'baohe', '高新': 'hfgaoxin', '蜀山': 'shushanqu', '庐阳': 'luyang', '瑶海': 'yaohai', '合肥周边': 'hefei', '政务': 'hfzhengwu', '滨湖新区': 'hfbinghu'}, 'code': 'hf|837'}, '南安': {'sublist': {'南安市区': 'nananshiqu', '其它': 'nananqita'}, 'code': 'nananshi|293'}, '惠州': {'sublist': {'龙门': 'longmen', '仲恺': 'zkai', '大亚湾': 'dayawan', '惠州周边': 'huizhoushi', '惠东': 'huidongqu', '惠城': 'huicheng', '惠阳': 'huiyang', '博罗': 'boluoqu'}, 'code': 'huizhou|722'}, '射阳': {'sublist': {'城区': 'sheyangcq', '其他': 'sheyangqt'}, 'code': 'sheyang|621'}, '昆山': {'sublist': {'张浦': 'zhangpus', '巴城': 'chengxisu', '周市': 'chengdongsu', '淀山湖': 'szdsh', '周庄': 'szzz', '千灯': 'qiandengs', '陆家': 'lujias', '锦溪': 'szjx', '玉山城西': 'yushancx', '玉山城北': 'chengbeisu', '老城区': 'laochengq', '昆山周边': 'kunshansu', '蓬朗镇': 'szplz', '花桥': 'huaqiaos', '玉山城东': 'yushancd', '玉山城南': 'chengnansu'}, 'code': 'szkunshan|16'}, '东至': {'sublist': {'城区': 'dongzhichengqu', '其他': 'dongzhiqita'}, 'code': 'dongzhi|10262'}, '清镇': {'sublist': {'城区': 'qingzhencq', '其他': 'qingzhenqt'}, 'code': 'qingzhen|12703'}, '阿克苏': {'sublist': {'乌什': 'wushixian', '新和': 'xinhexian', '柯坪': 'kepingxian', '库车': 'kuchexian', '阿克苏周边': 'akeshuzhoubian', '沙雅': 'shayaxian', '阿克苏市': 'aksakss', '阿瓦提': 'awatixian', '温宿': 'wensuxian', '拜城': 'baichengxian'}, 'code': 'aks|9499'}, '德州': {'sublist': {'临邑': 'linyixianqdz', '德城': 'decheng', '陵县': 'lingxian', '宁津': 'ningjindz', '禹城': 'yuchengshidz', '平原': 'pingyuan', '乐陵': 'laolingdz', '庆云': 'qingyun', '其他': 'dezhou', '武城': 'wucheng', '齐河': 'qihedz', '夏津': 'xiajin'}, 'code': 'dz|728'}, '孝义': {'sublist': {'城区': 'xiaoyicq', '其他': 'xiaoyiqt'}, 'code': 'xiaoyi|3227'}, '遵义': {'sublist': {'赤水': 'chishuishi', '桐梓': 'tongzixian', '新浦新区': 'xinpuxinqu', '仁怀市': 'zunyirenhuai', '播州区': 'bozhouqu', '绥阳': 'suiyangxian', '道真': 'daozhenxian', '湄潭': 'meitanxian', '凤冈': 'fenggangxian', '红花岗': 'honghuagangqu', '南白': 'zunyixian', '正安': 'zhenganxian', '汇川': 'huichuanqu', '余庆': 'yuqingxian', '习水': 'xishuix', '务川': 'wuchuanxian'}, 'code': 'zunyi|7620'}, '双鸭山': {'sublist': {'饶河': 'raohe', '双鸭山周边': 'shuangyashanzb', '集贤': 'jixian', '宝山': 'baoshanqu', '尖山': 'jianshan', '岭东': 'lingdong', '宝清': 'baoqing', '四方台': 'sifangtai', '友谊': 'youyix'}, 'code': 'sys|9837'}, '禹城': {'sublist': {'城区': 'yuchengshicq', '其他': 'yuchengshiqt'}, 'code': 'yuchengshi|731'}, '崇左': {'sublist': {'天等': 'tiandeng', '大新': 'daxinx', '江州': 'jiangzhou', '龙州': 'longzhou', '扶绥': 'fusui', '凭祥': 'pingxiangs', '崇左周边': 'chongzuozhoubian', '宁明': 'ningming'}, 'code': 'chongzuo|10524'}, '扬州': {'sublist': {'宝应': 'yangzhoubaoying', '仪征': 'yizheng', '邗江': 'hanjiang', '高邮': 'gaoyou', '广陵': 'guangling', '江都': 'jiangdou', '维扬': 'weiyangqu', '扬州周边': 'yangzhouqita'}, 'code': 'yz|637'}, '内江': {'sublist': {'隆昌': 'longchang', '东兴': 'dongxing', '资中': 'zizhong', '市中区': 'shizhong', '威远': 'weiyuan', '其它': 'neijiangshi'}, 'code': 'scnj|5928'}, '阳泉': {'sublist': {'郊区': 'jiaoquq', '市辖区': 'yqsxq', '城区': 'chengquq', '盂县': 'yuxian', '平定': 'pingdingxian', '矿区': 'kuangquq'}, 'code': 'yq|8760'}, '广水': {'sublist': {'城区': 'guangshuishicq', '其他': 'guangshuishiqt'}, 'code': 'guangshuishi|9657'}, '临邑': {'sublist': {'城区': 'linyixianqcq', '其他': 'linyixianqqt'}, 'code': 'linyixianq|739'}, '福州': {'sublist': {'鼓楼': 'fzgulou', '平潭': 'pingtanxian', '永泰': 'yongtaixian', '长乐': 'changleshi', '福州周边': 'fuzhouzb', '晋安': 'jinanqu', '闽侯': 'minhouxian', '马尾': 'mayi', '闽清': 'minqingxian', '连江': 'lianjiangxian', '仓山': 'cangshan', '台江': 'taijiang', '罗源': 'luoyuanxian', '福清': 'fuqingshi'}, 'code': 'fz|304'}, '台山': {'sublist': {'都斛': 'duhu', '北陡': 'beidou', '端芬': 'duanfen', '四九': 'sijiu', '斗山': 'doushan', '冲蒌': 'chongwei', '三合': 'sanhez', '川岛': 'chuandao', '深井': 'shenjing', '台山周边': 'taishanzb', '白沙': 'baishaz', '大江': 'dajiang', '海宴': 'haiyanz', '广海': 'guanghai', '赤溪': 'chixi'}, 'code': 'taishan|11263'}, '安达': {'sublist': {'城区': 'andachengqu', '其他': 'andaqita'}, 'code': 'shanda|6720'}, '霸州': {'sublist': {'湿地公园': 'shidigogyuan', '火车站': 'huochezhanbz', '市政府': 'shizhengfubz', '霸州一小': 'bazhouyixiao', '孔雀城': 'kongquechengbz', '霸州一中': 'bazhouyizhong', '第五小学': 'diwuxiaoxue', '锦绣华府': 'jinxiuhuafu', '汽车站': 'qichezhanbz', '明珠超市': 'mingzhuchaoshi', '廊坊第四人民医院': 'disirenminyiyuan'}, 'code': 'bazhou|775'}, '四平': {'sublist': {'双辽': 'shuangliao', '伊通县': 'yitong', '公主岭': 'sipinggongzhuling', '梨树县': 'lishusp', '孤家子镇': 'spgjz', '范家屯': 'fanjiatun', '铁东': 'tiedongq', '四平周边': 'sipingzhoubian', '榆树台镇': 'spystz', '铁西': 'tiexiq'}, 'code': 'sp|10171'}, '乳山': {'sublist': {'银滩': 'whyantan', '城区': 'rushanchengqu', '其他': 'rushanshiqita', '市区': 'whsq'}, 'code': 'rushan|520'}, '沧州': {'sublist': {'运河': 'yunhe', '泊头': 'botou', '其他': 'cangzhoushi', '青县': 'qingxian', '新华': 'czxinhua', '孟村': 'mengcun', '沧县': 'cangxiancz', '任丘市': 'cangzhourenqiu', '河间': 'hejiancz', '盐山': 'yanshanxian', '南皮': 'nanpi', '东光': 'dongguang', '海兴': 'haixing', '献县': 'czxianxian', '吴桥': 'wuqiao', '肃宁': 'suning', '黄骅': 'huanghuacz'}, 'code': 'cangzhou|652'}, '哈密': {'sublist': {'巴里坤': 'balilkunzzx', '哈密': 'hamishi', '伊吾': 'yiwuxian'}, 'code': 'hami|7452'}, '黄石': {'sublist': {'西塞山': 'xisaishan', '团城山': 'tuanchengshan', '花湖': 'hshh', '铁山': 'tieshan', '黄石港': 'huangshigang', '大冶': 'daye', '下陆': 'xialu', '阳新': 'hsyangxin', '其它': 'huangshi'}, 'code': 'hshi|1734'}, '吐鲁番': {'sublist': {'大河沿镇': 'daheyanzhen', '老城路': 'laochenglu', '鄯善县': 'tlfssx', '托克逊县': 'tlftkxx', '吐鲁番周边': 'tulufanzhoubian', '高昌路': 'gaochanglu', '七泉湖镇': 'qiquanhuzhen'}, 'code': 'tlf|9475'}, '图木舒克': {'sublist': {'图木休克': 'tumuxiuke', '皮恰克松地': 'piqiakesongdi', '其盖麦旦': 'qigaimaidan', '盖米里克': 'gaimilike', '图木舒克周边': 'tumushukezb', '金墩': 'jindun'}, 'code': 'tmsk|9559'}, '株洲': {'sublist': {'芦淞': 'lusong', '炎陵': 'yanlingxianx', '攸县': 'zzyouxianzz', '其他': 'zhuzhoushi', '醴陵市': 'zhuzhoujiling', '石峰': 'shifeng', '株洲县': 'zhuzhouxian', '荷塘': 'hetang', '天元': 'tianyuan', '茶陵': 'chaling'}, 'code': 'zhuzhou|1086'}, '太原': {'sublist': {'晋源': 'jinyuan', '太原周边': 'taiyuan', '小店': 'xiaodian', '尖草坪': 'jiancaoping', '万柏林': 'wanbolin', '杏花岭': 'xinghualing', '迎泽': 'yingze'}, 'code': 'ty|740'}, '定边': {'sublist': {'城区': 'dingbianchengqu', '其他': 'dingbianqita'}, 'code': 'dingbian|5948'}, '永安': {'sublist': {'城区': 'yongancq', '其他': 'yonganqt'}, 'code': 'yongan|2133'}, '铜仁': {'sublist': {'石阡': 'shiqian', '德江': 'dejiang', '松桃': 'songtao', '沿河': 'yanhe', '万山': 'wangshan', '江口': 'jiangkou', '碧江': 'trbj', '玉屏': 'yuping', '思南': 'sinan', '印江': 'yinjiang', '铜仁周边': 'tongrenzb'}, 'code': 'tr|10417'}, '阿拉尔': {'sublist': {'幸福路': 'xingfulu', '青松路': 'qingsonglu', '团场': 'tuanchang', '阿拉尔周边': 'alaerzhoubian', '南口': 'nankoua', '金银川路': 'jinyinchuanlu'}, 'code': 'ale|9539'}, '海拉尔': {'sublist': {'海拉尔城区': 'hailaercheng', '其他': 'hailaer'}, 'code': 'hlr|2043'}, '平湖': {'sublist': {'东湖景区': 'donghjq', '九龙山海滨浴场': 'jiulshb', '莫氏庄园': 'moszy', '平湖周边': 'pinghuzb'}, 'code': 'pinghushi|501'}, '章丘': {'sublist': {'章丘': 'zhangqiushiqu', '相公庄镇': 'xianggongzhuang', '官庄乡': 'guanzhuangxiang', '其他': 'zhangqiuqita', '辛寨乡': 'xinzhaixiang', '刁镇': 'diaozhen', '水寨镇': 'shuizhaizhen', '普集镇': 'pujizhen', '高官寨镇': 'gaoguanzhai', '绣惠镇': 'xiuhuizhen'}, 'code': 'zhangqiu|8680'}, '阜新': {'sublist': {'海州': 'haizhouq', '阜新县': 'fuxinx', '清河门': 'qinghemen', '阜新周边': 'fuxinzhoubian', '新邱': 'xinqiu', '彰武': 'zhangwu', '太平': 'taipingq', '细河': 'xihe'}, 'code': 'fx|10097'}, '中山': {'sublist': {}, 'code': 'zs|771'}, '岳阳': {'sublist': {'云溪': 'yunxi', '汨罗': 'miluo', '其他': 'yueyang', '岳阳楼': 'yueyanglou', '君山': 'junshan', '临湘': 'linxiang'}, 'code': 'yy|821'}, '攀枝花': {'sublist': {'西区': 'xiq', '仁和': 'renhequ', '东区': 'dongq', '米易': 'miyixian', '盐边': 'yanbianxian'}, 'code': 'panzhihua|2371'}, '乌兰察布': {'sublist': {'集宁': 'jiningq', '乌兰察布周边': 'wulanchabuzhoubian', '商都': 'sangdu', '凉城': 'liangchengx', '卓资': 'zuozhi', '化德': 'huade', '丰镇': 'fengzhen', '兴和': 'xinghe'}, 'code': 'wlcb|9993'}, '泗阳': {'sublist': {'新袁新城': 'xinyuanxincheng', '王集新城': 'wangjixincheng', '众兴镇': 'zhongxingzhen', '其他': 'siyangqita'}, 'code': 'siyang|5959'}, '枣阳': {'sublist': {'南城街道': 'nanchengjiedao', '其他': 'zaoyangshiqita', '北城街道': 'beichengjiedao', '环城街道': 'huanchengjiedao'}, 'code': 'zaoyang|896'}, '阿里': {'sublist': {'措勤': 'cuoqinxian', '阿里周边': 'alizhoubian', '革吉': 'gejixian', '改则': 'aligaize', '普兰': 'pulanxian', '日土区': 'rituqu', '噶尔': 'gaerxian', '札达': 'zhadaxian'}, 'code': 'al|9678'}, '丽水': {'sublist': {'庆元': 'qingyuanquyu', '青田': 'qingtianqu', '遂昌': 'suiyangqu', '松阳': 'songyangqu', '莲都': 'lianduqu', '景宁': 'jingningqu', '龙泉': 'longquanqu', '云和': 'yunhequ', '缙云': 'jinyunqu'}, 'code': 'lishui|7921'}, '禹州': {'sublist': {'顺店镇': 'shundianzhen', '无梁镇': 'wuliangzhen', '其他': 'qitaa', '神后镇': 'shenhouzhen', '文殊镇': 'wenshuzhen', '韩城办': 'hanchengban', '古城镇': 'guchengzhenz', '钧台办': 'diaotaiban', '火龙镇': 'huolongzhen', '鸿畅镇': 'hongchangzhen', '方山镇': 'fangshanzhen', '颍川办': 'yingchuanban', '梁北镇': 'liangbeizhen', '夏都办': 'xiaduban'}, 'code': 'yuzhou|979'}, '朔州': {'sublist': {'朔州周边': 'shuozhouzhoubian', '朔城': 'shuocheng', '怀仁': 'huairen', '右玉': 'youyu', '山阴': 'shanyin', '应县': 'yingx', '平鲁': 'pingluq'}, 'code': 'shuozhou|9871'}, '南漳': {'sublist': {'城区': 'nanzhangcq', '其他': 'nanzhangqt'}, 'code': 'nanzhang|898'}, '汕尾': {'sublist': {'陆河': 'luhexian', '海丰县': 'shanweihaifeng', '陆丰': 'lufengshisw', '汕尾周边': 'shanweizb', '汕尾城区': 'shanweicq'}, 'code': 'sw|9449'}, '天水': {'sublist': {'甘谷': 'ganguxin', '张家川': 'zhangjiachun', '麦积': 'maijiqu', '天水': 'tianshuishi', '秦州': 'qinzhouqu', '清水': 'qingshuixian', '武山': 'wushanxian', '秦安': 'qinanxian'}, 'code': 'tianshui|8601'}, '丹阳': {'sublist': {'丹阳市区': 'danyangshiqu', '其它': 'danyangqita'}, 'code': 'danyang|648'}, '贵港': {'sublist': {'桂平': 'guipingqugg', '平南': 'pingnanxian', '覃塘': 'qintangqu', '港北': 'gangbeiqu', '港南': 'gangnanqu'}, 'code': 'gg|6770'}, '府谷': {'sublist': {'城区': 'fuguchengqu', '其他': 'fuguqita'}, 'code': 'fugu|5945'}, '如皋': {'sublist': {'如皋市区': 'rugaoshiqu', '其它': 'rugaoqita'}, 'code': 'rugao|397'}, '果洛': {'sublist': {'玛多': 'maduo', '班玛': 'banma', '久治': 'jiuzhi', '达日': 'dari', '玛沁': 'maqin', '甘德': 'gande', '果洛周边': 'guoluozhoubian'}, 'code': 'guoluo|9936'}, '新乡': {'sublist': {'长垣县': 'xianxiangchangyuan', '卫辉': 'weihui', '其他': 'xinxiang', '牧野': 'muye', '卫滨': 'weibinqu', '平原示范区': 'pingyuanshifanqu', '新乡县': 'xinxiangxian', '凤泉': 'fengquan', '红旗': 'hongqi', '辉县': 'huixian'}, 'code': 'xx|1016'}, '沈阳': {'sublist': {'皇姑': 'huanggu', '沈北新区': 'xinchengzi', '苏家屯': 'sujiatun', '沈河': 'shenhe', '于洪': 'yuhong', '和平': 'syheping', '大东': 'dadong', '东陵': 'dongling', '浑南新区': 'shenyangshi', '铁西': 'sytiexi', '沈阳周边': 'shenyang'}, 'code': 'sy|188'}, '绵阳': {'sublist': {'游仙': 'youxian', '涪城': 'fuchengqu', '绵阳周边': 'mianyangshi', '高新区': 'mygaoxinqu', '经开区': 'jingkaiqu', '三台县': 'santaixian', '江油': 'jiangyou', '科创园区': 'kechuangyuanqu'}, 'code': 'mianyang|1057'}, '广饶': {'sublist': {'城区': 'guangraochengqu', '其他': 'guangraoxianqita'}, 'code': 'guangrao|627'}, '玉环': {'sublist': {'玉城街道': 'yuchengjiedao', '坎门街道': 'kanmenjiedao', '其他': 'yuhuanxianqita', '大麦屿街道': 'damaiyujiedao'}, 'code': 'yuhuan|409'}, '怒江': {'sublist': {'福贡': 'fugongxian', '泸水': 'lushuixian', '兰坪县': 'nujianglpx', '碧江': 'bijiangxian', '怒江周边': 'nujiangzhoubian', '贡山': 'gongshanxian'}, 'code': 'nujiang|9462'}, '开平': {'sublist': {'新昌': 'xinchangjm', '开平周边': 'kaipingzb', '侨园': 'qiaoyuan', '迳头': 'jingtoujm', '三江': 'sanjiangjm', '新海': 'xinhai', '幸福': 'xingfujm', '水口': 'shuikoujm', '曙光东': 'shuguangdong', '南岛': 'nandao', '曙光西': 'shuguangxi', '祥龙': 'xianglong', '荻海': 'dihai'}, 'code': 'kaipingshi|634'}, '怀化': {'sublist': {'中方': 'zhongfang', '沅陵': 'yuanling', '其它': 'huaihua', '洪江': 'hongjiang', '会同': 'huitong', '溆浦': 'xupuxian', '辰溪': 'chenxi', '鹤城': 'hecheng'}, 'code': 'hh|5756'}, '襄垣': {'sublist': {'城区': 'xiangyuanxiancq', '其他': 'xiangyuanxianqt'}, 'code': 'xiangyuanxian|6928'}, '东明': {'sublist': {'城区': 'dongmingcq', '其他': 'dongmingqt'}, 'code': 'dongming|5641'}, '林州': {'sublist': {'城区': 'linzhoucq', '其他': 'linzhouqt'}, 'code': 'linzhou|1101'}, '琼海': {'sublist': {'博鳌镇': 'boao', '阳江镇': 'yangjiang', '琼海周边': 'qionghaizb', '中原镇': 'zhongyuanz', '万泉镇': 'wangquan', '嘉积镇': 'jiaji', '石壁镇': 'shibi'}, 'code': 'qh|10136'}, '沙洋': {'sublist': {}, 'code': 'shayangxian|9118'}, '金坛': {'sublist': {'尧塘街道': 'yaotangjiedao', '西城街道': 'jtxichengjiedao', '其他': 'jintanqita', '东城街道': 'jtdongchengjiedao'}, 'code': 'jintan|468'}, '襄阳': {'sublist': {'高新区': 'gaoxq', '襄城': 'xiangcheng', '樊城': 'xfxiangcheng', '襄阳周边': 'xiangfan', '鱼梁洲': 'yuliangz', '枣阳市': 'xiangyagnzaoyang', '宜城': 'yichengshixf', '襄州': 'xiangyangqu', '老河口': 'laohekouxf'}, 'code': 'xf|891'}, '那曲': {'sublist': {'那曲镇': 'naquzhen', '古露镇': 'guluzhen', '那曲周边': 'naquzhoubian', '比如县': 'nqbrx', '尼玛县': 'nqnmx', '申扎县': 'nqszx', '班戈县': 'nqbgx', '巴青县': 'nqbqx', '嘉黎县': 'nqjlx', '聂荣县': 'nqnrx', '罗玛镇': 'luomazhen', '安多县': 'nqadx', '索县': 'nqsx'}, 'code': 'nq|9618'}, '南充': {'sublist': {'阆中': 'langzhongshi', '南充周边': 'nanchongzb', '高坪': 'gaopingqu', '营山': 'yingshanxianq', '南部': 'nanbuxian', '蓬安': 'penganxian', '顺庆': 'shunqingqu', '西充': 'xichongxian', '嘉陵': 'jialingqu', '仪陇': 'yilongxian'}, 'code': 'nanchong|2378'}, '茂名': {'sublist': {'茂南': 'maonan', '其他': 'maoming', '化州': 'huazhou', '高州': 'gaozhou', '信宜': 'xinyi', '电白': 'dianbai', '茂港': 'maogang'}, 'code': 'mm|679'}, '吉安': {'sublist': {}, 'code': 'ja|2364'}, '香河': {'sublist': {'新广场物美': 'xinguangchangwumei', '好百年家具城': 'haobainianjiajucheng', '安平镇': 'anpingzhen', '人民公园': 'renmingongyuanxh', '天下第一城': 'tianxiadiyicheng', '鑫亿隆文化广场': 'xinyilongwenhuaguangchang', '华联县医院': 'hualianxianyiyuan', '香河一中': 'xiangheyizhong', '三小二中': 'sanxiaoerzhong', '高速口': 'gaosukou', '938总站': '938zongzhan'}, 'code': 'xianghe|5395'}, '烟台': {'sublist': {'高新区': 'ytgaoxin', '海阳': 'hyang', '烟台周边': 'yantan', '大学城': 'ytdaxue', '莱阳': 'laiyangyt', '开发区': 'ytkaifaqu', '芝罘': 'zhifu', '莱州': 'yantailaizhou', '莱山': 'laishan', '栖霞': 'qixiayt', '蓬莱市': 'yantaipenglai', '牟平': 'mouping', '长岛': 'changdao', '福山': 'fushan', '招远市': 'yantaizhaoyuan', '龙口': 'longkouqu'}, 'code': 'yt|228'}, '安顺': {'sublist': {'镇宁': 'aszhenning', '西秀': 'xixiuqu', '紫云': 'asziyun', '平坝': 'pingbaxian', '安顺周边': 'anshunzhoubian', '普定县': 'pudingxian', '关岭': 'asguanling'}, 'code': 'anshun|7468'}, '尉氏': {'sublist': {'尉氏县': 'wxshixian'}, 'code': 'weishixian|7391'}, '海口': {'sublist': {'美兰': 'meilan', '海口周边': 'haikouqita', '龙华': 'longhuaqu', '秀英': 'xiuying', '琼山': 'qiongshan'}, 'code': 'haikou|2053'}, '滁州': {'sublist': {'来安': 'laian', '明光': 'mingguan', '凤阳': 'fengyangx', '天长': 'tianchangqu', '琅琊': 'langya', '定远': 'dingyuan', '滁州周边': 'chuzhouzhoubian', '全椒': 'quanshu', '南谯': 'nanqiaoq'}, 'code': 'chuzhou|10266'}, '开封': {'sublist': {'尉氏': 'weishixiankf', '杞县': 'kaifengqixian', '禹王台': 'yuwangtai', '通许': 'tongxuxiankf', '开封县': 'kaifengxian', '顺河': 'shunhequ', '兰考': 'lankaoxiankf', '鼓楼': 'gulouquyu', '龙亭': 'longtingqu', '金明': 'jinmingqu'}, 'code': 'kaifeng|2342'}, '瑞安': {'sublist': {'塘下': 'ratangxia', '陶山': 'rataoshan', '飞云': 'rafeiyun', '玉海': 'rayuhai', '湖岭': 'rahuling', '碧山': 'rabishan', '龙湖': 'ralonghu', '安阳': 'raanyang', '瑞安周边': 'raruianzhoubian', '潘岱': 'rapandai', '平阳坑': 'rapingyangkeng', '上望': 'rashangwang', '马屿': 'ramayu', '莘塍': 'raxinsheng', '汀田': 'ratingtian', '东山': 'radongshan', '曹村': 'racaocun', '锦湖': 'rajinhu', '仙降': 'raxianjiang'}, 'code': 'ruiancity|13951'}, '高密': {'sublist': {'醴泉街道': 'liquanjiedao', '密水街道': 'mishuijiedao', '朝阳街道': 'chaoyangjiedao', '其他': 'gaomishiqita', '咸家工业区': 'xianjiagongyequ'}, 'code': 'gaomi|371'}, '海盐': {'sublist': {'城区': 'haiyancq', '其他': 'haiyanqt'}, 'code': 'haiyan|504'}, '贵阳': {'sublist': {'云岩': 'yunyan', '乌当': 'wudang', '小河片': 'xiaohepian', '清镇': 'qingzhengy', '小河': 'xiaohequ', '金阳新区': 'jinyangxinqu', '南明': 'nanming', '白云': 'baiyunqv', '贵阳周边': 'guiyang', '花溪': 'huaxi'}, 'code': 'gy|2015'}, '汉中': {'sublist': {'西乡': 'xixiang', '勉县': 'mianxian', '其他': 'hanzhongshi', '留坝县': 'hanzhonglbx', '南郑': 'nanzheng', '略阳': 'lueyang', '洋县': 'yangxian', '汉台': 'hantai', '宁强县': 'hanzhongnqx', '城固': 'chenggu', '佛坪县': 'hanzhongfpx', '镇巴县': 'hanzhongzbx'}, 'code': 'hanzhong|3163'}, '兴安盟': {'sublist': {'科尔沁右翼中旗': 'keerqinyouyizhongqi', '乌兰浩特': 'wulanhaote', '兴安盟周边': 'xinganmengzhoubian', '突泉': 'tuquan', '科尔沁右翼前旗': 'keerqinyouyiqianqi', '阿尔山': 'aershan', '扎赉特旗': 'zalanteqi'}, 'code': 'xam|9976'}, '郑州': {'sublist': {'航空港': 'zzhkg', '上街': 'shangjiequzz', '中原': 'zhongyuan', '管城区': 'guancheng', '二七': 'eqi', '高新区': 'zzgaoxin', '金水': 'jinshui', '惠济': 'huiji', '郑州周边': 'zhengzhou', '经开区': 'zzjingkaiq', '郑东新区': 'zhengdongxinqu'}, 'code': 'zz|342'}, '溧阳': {'sublist': {'溧阳市区': 'liyangshiqu', '其它': 'liyangqita'}, 'code': 'liyang|469'}, '曹县': {'sublist': {}, 'code': 'caoxian|5638'}, '安庆': {'sublist': {'大观': 'daguanqu', '怀宁': 'huaining', '其他': 'anqingqita', '潜山': 'qianshanxian', '迎江': 'yingjiang', '宜秀': 'yixiu', '桐城': 'tongchengshi', '宿松': 'susong', '岳西': 'yuexi'}, 'code': 'anqing|3251'}, '嘉兴': {'sublist': {'桐乡': 'tongxiangqu', '海宁': 'hainingqu', '南湖': 'nanhu', '秀洲': 'xiuzhou', '嘉善': 'jiashanqu', '嘉兴市区': 'jiaxsq', '海盐': 'haiyanjx', '平湖': 'jxpinghu', '嘉兴周边': 'jiaxing', '经济开发区': 'jingjikfq'}, 'code': 'jx|497'}, '白山': {'sublist': {'八道江': 'badaojiang', '靖宇': 'jingyux', '临江': 'linjiangs', '长白': 'changbaix', '白山周边': 'baishanzhoubian', '抚松': 'fusong', '江源': 'jiangyuan'}, 'code': 'baishan|10179'}, '寿光': {'sublist': {'文家': 'wenjia', '留吕': 'liulv', '台头': 'taitou', '其它': 'shouguangshi'}, 'code': 'shouguang|369'}, '和县': {'sublist': {'沈巷镇': 'shengangzhen', '乌江镇': 'wujiangzhen', '西埠镇': 'xibuzhen', '姥桥镇': 'laoqiaozhen', '香泉镇': 'xiangquanzhen', '历阳镇': 'liyangzhen', '白桥镇': 'baiqiaozhen', '石杨镇': 'shiyangzhens', '善厚镇': 'shanhouzhen', '功桥镇': 'gongqiaozhen'}, 'code': 'hexian|10892'}, '晋中': {'sublist': {'左权': 'zuoquanxian', '平遥': 'pingyaoxian', '祁县': 'qixian', '榆次': 'yuciqu', '太谷': 'taiguxian', '开发区': 'kaifaquq', '介休': 'jiexiushi', '寿阳': 'shouyangxian', '和顺': 'heshunxian', '昔阳': 'xiyangxian', '灵石': 'lingshixian', '榆社': 'yushexian'}, 'code': 'jz|8854'}, '义乌': {'sublist': {'北苑': 'ywbeiyuan', '义乌周边': 'yiwuzhoub', '稠城': 'choucheng', '稠江': 'choujiang', '廿三里': 'ersanli', '城西': 'ywchengxi', '后宅': 'houzhai', '义乌市区': 'yiwsq', '江东': 'ywjiangdong'}, 'code': 'yiwu|12291'}, '台州': {'sublist': {'三门': 'sanmen', '路桥': 'luqiao', '黄岩': 'huangyan', '其他': 'taizhoushi', '温岭': 'wenlingqu', '椒江': 'jiaojiang', '玉环县': 'taizhouyuhuan', '仙居': 'xianju', '天台': 'tiantai', '临海': 'taizhoulinhai'}, 'code': 'tz|403'}, '新泰': {'sublist': {'新汶街道': 'xinwenjd', '客运中心': 'taiankyzx', '体育场': 'taiantiyuchang', '青云街道': 'qingyjd', '平阳河': 'taianpyh', '府前大街': 'taianfqdj', '新泰周边': 'xintzb', '其他': 'xintaishiqita', '杏山路': 'taianxsl', '青云大厦': 'taianqyds', '小协': 'taianxx'}, 'code': 'xintai|689'}, '滑县': {'sublist': {'城区': 'huaxiancq', '其他': 'huaxianqt'}, 'code': 'huaxian|5405'}, '延边': {'sublist': {'和龙': 'helong', '敦化': 'dunhua', '其他': 'yanbianshi', '汪清': 'wangqing', '龙井': 'longjing', '安图': 'antu', '珲春': 'huichun', '延吉': 'yanji', '图们': 'tumen'}, 'code': 'yanbian|3184'}, '灌云': {'sublist': {'城区': 'guanyunchengqu', '侍庄街道': 'shizhuangjiedao', '其他': 'guanyunxianqita'}, 'code': 'guanyun|2148'}, '三明': {'sublist': {'将乐': 'jianglexian', '宁化': 'ninghua', '三明周边': 'sanming', '尤溪': 'youxi', '大田': 'datianxian', '永安': 'yongansm', '清流': 'qingliuxian', '泰宁': 'tainingxian', '三元': 'sanyuan', '建宁': 'jianningxian', '梅列': 'meilie', '沙县': 'shaxian', '明溪': 'mingxi'}, 'code': 'sm|2048'}, '许昌': {'sublist': {'鄢陵': 'yanlingxian', '其他': 'xuchangshi', '长葛': 'changgeshi', '许昌县': 'xuchang', '襄城': 'xiangchengxian', '禹州': 'yuzhoushi', '魏都': 'weidou'}, 'code': 'xc|977'}, '博尔塔拉': {'sublist': {'精河': 'jinghexian', '博州周边': 'bozhouzb', '博乐': 'boleshi', '温泉': 'wenquanxian'}, 'code': 'betl|9529'}, '梨树县': {'sublist': {'城区': 'lishucq', '其他': 'lishuqt'}, 'code': 'lishu|10176'}, '大连': {'sublist': {}, 'code': 'dl|147'}, '威海': {'sublist': {'乳山市': 'weihairushan', '环翠': 'huancui', '其他': 'weihaishi', '高区': 'gaoqu', '经区': 'jingqu', '荣成': 'weihairongcheng', '文登': 'wendeng'}, 'code': 'weihai|518'}, '唐山': {'sublist': {'高新区': 'gxq', '曹妃甸': 'caofeidian', '开平': 'kaiping', '迁西': 'qianxixiants', '迁安': 'tangshanqianan', '遵化': 'zunhuats', '路南': 'lunan', '丰润': 'fengrun', '古冶': 'guye', '丰南': 'fengnan', '路北': 'lubei', '南堡开发区': 'nanbaoqu', '其他': 'tangshan', '海港开发区': 'haigangqu'}, 'code': 'ts|276'}, '金湖': {'sublist': {'城区': 'jinhucq', '其他': 'jinhuqt'}, 'code': 'jinhu|975'}, '衢州': {'sublist': {}, 'code': 'quzhou|6793'}, '沙河': {'sublist': {'城区': 'shaheshicq', '其他': 'shaheshiqt'}, 'code': 'shaheshi|755'}, '大丰': {'sublist': {'白驹': 'baiju', '大桥': 'daqiao', '大中': 'dfdazhong', '南阳': 'nanyangz', '裕华': 'yuhuaz', '刘庄': 'liuzhuang', '草堰': 'caoyan', '西团': 'xituan', '开发区': 'kaifaquz', '小海': 'xiaohai', '方强': 'fangqiang', '大丰周边': 'dafengzb', '新丰': 'xinfengz', '万盈': 'wanying', '三龙': 'sanlong', '大丰港': 'dafenggang'}, 'code': 'dafeng|11279'}, '桂林': {'sublist': {'八里街': 'balijie', '兴安县': 'xanxian', '临桂': 'linguic', '象山': 'xiangshan', '秀峰': 'xiufeng', '七星': 'qixing', '阳朔县': 'yangsx', '桂林周边': 'guilin', '叠彩': 'diecai', '雁山': 'yanshan', '灵川': 'lingchuanc'}, 'code': 'gl|1039'}, '邵东': {'sublist': {'城区': 'shaodongxiancq', '其他': 'shaodongxianqt'}, 'code': 'shaodongxian|6954'}, '宣威': {'sublist': {'城区': 'xuanwushicq', '其他': 'xuanwushiqt'}, 'code': 'xuanwushi|7533'}, '高平': {'sublist': {'城区': 'gaopingcq', '其他': 'gaopingqt'}, 'code': 'gaoping|3354'}, '焦作': {'sublist': {'博爱': 'boaixian', '孟州': 'mengzhoujz', '其他': 'jiaozuoqita', '中站': 'zhongzhan', '解放': 'jiefangqu', '山阳': 'shanyang', '温县': 'wenxianjz', '沁阳': 'qinyangjz', '高新': 'gaoxin', '马村': 'macun', '武陟': 'wuzhixian', '修武': 'xiuwuxian'}, 'code': 'jiaozuo|3266'}, '桐城': {'sublist': {'孔城': 'kongcheng', '青草': 'qingcao', '黄甲': 'huangjia', '桐城周边': 'tongchengzb', '吕亭': 'lvting', '开发区': 'kaifaqutc', '新渡': 'xindutc', '大关': 'daguantc', '唐湾': 'tangwan', '范岗': 'fangang', '嬉子湖': 'xizihu', '文昌': 'wenchangs', '双港': 'shuanggangtc', '金神': 'jinshen', '兴尔旺': 'xingerwang', '龙眠': 'longmian'}, 'code': 'tongcheng|11296'}, '抚州': {'sublist': {'抚州周边': 'fuzhouzhoubian', '崇仁': 'chongren', '东乡': 'dongxiang', '临川': 'linchuan', '乐安': 'lean', '南城': 'nanchengxfz'}, 'code': 'fuzhou|10134'}, '诸暨': {'sublist': {'大唐镇': 'datangzhenzhuji', '街亭镇': 'jietingzhen', '五泄镇': 'wuxiezhen', '枫桥镇': 'fengqiaozhen', '店口镇': 'diankouzhen', '诸暨市区': 'shujishiqu', '其它': 'zhujiqita'}, 'code': 'zhuji|357'}, '吴忠': {'sublist': {'青铜峡': 'qingtongxia', '红寺堡': 'hongsipu', '太阳山': 'taiyangshan', '盐池': 'yanchi', '同心': 'tongxin', '利通': 'litong', '吴忠周边': 'wuzhongzhoubian'}, 'code': 'wuzhong|9962'}, '吕梁': {'sublist': {'方山县': 'lvliangfsx', '其他': 'lvliangshi', '兴县': 'lvliangxx', '临县': 'lvlianglx', '交城': 'jiaocheng', '交口县': 'lvliangjkx', '石楼县': 'lvliangslx', '柳林': 'liulinll', '孝义': 'xiaoyill', '中阳': 'zhongyang', '文水': 'wenshui', '岚县': 'lvlianglanxian', '汾阳': 'fenyang', '离石': 'lishi'}, 'code': 'lvliang|3222'}, '白银': {'sublist': {'靖远': 'jingyuan', '景泰': 'jingtan', '会宁': 'huining', '白银': 'baiyin', '白银周边': 'baiyinzhoubian', '平川': 'pingchuan'}, 'code': 'by|10304'}, '神木': {'sublist': {'神木镇': 'shenmuzhen', '其他': 'shenmuxianqita', '大柳塔镇': 'daliutazhen'}, 'code': 'shenmu|5944'}, '渭南': {'sublist': {}, 'code': 'wn|5733'}, '郯城': {'sublist': {'城区': 'tanchengcq', '其他': 'tanchengqt'}, 'code': 'tancheng|510'}, '海东': {'sublist': {'民和': 'minhe', '互助': 'huzhu', '化隆': 'lualong', '平安': 'pingan', '海东周边': 'haidongzhoubian', '乐都': 'ledu', '循化': 'xunhua'}, 'code': 'haidong|9909'}, '永兴': {'sublist': {'城区': 'yongxingcq', '其他': 'yongxingqt'}, 'code': 'yongxing|5701'}, '玉林': {'sublist': {}, 'code': 'yulin|2337'}, '日照': {'sublist': {'五莲': 'wulian', '岚山': 'lanshan', '莒县': 'rizhaolvxian', '东港': 'donggangqu', '其它': 'rizhaoshi'}, 'code': 'rizhao|3177'}, '伊犁': {'sublist': {'奎屯': 'kuitunshi', '乌苏': 'wusushi', '伊宁': 'yiningshi', '塔城': 'tachengshi', '阿勒泰': 'aletaishi', '伊犁周边': 'yilizhoubian'}, 'code': 'yili|9472'}, '阜宁': {'sublist': {'城区': 'funingxiancq', '其他': 'funingxianqt'}, 'code': 'funingxian|620'}, '北票': {'sublist': {'城区': 'beipiaocq', '其他': 'beipiaoqt'}, 'code': 'beipiao|10109'}, '五指山': {'sublist': {'冲山镇': 'chongshan', '毛阳镇': 'maoyang', '五指山周边': 'wuzhishanzb', '南圣镇': 'nansheng', '番阳镇': 'fanyang'}, 'code': 'wzs|9952'}, '乐陵': {'sublist': {'城区': 'lelingcq', '其他': 'lelingqt'}, 'code': 'leling|730'}, '温县': {'sublist': {'城区': 'wenxiancq', '其他': 'wenxianqt'}, 'code': 'wenxian|7312'}, '漳浦': {'sublist': {'城区': 'zhangpucq', '其他': 'zhangpuqt'}, 'code': 'zhangpu|717'}, '雄安新区': {'sublist': {'雄县': 'xionganxiongxian', '容城': 'xionganrongcheng', '其他': 'xionganxinquqita', '安新': 'anxin'}, 'code': 'xionganxinqu|111234'}, '承德': {'sublist': {'滦平': 'luanpingxian', '承德市': 'chengdeshi', '双滦': 'shuangluan', '围场': 'weichangxian', '双桥': 'cdshuangqiao', '丰宁': 'fengningxian', '开发区': 'cdkaifaqu', '隆化': 'longhuaxian', '营子': 'yingzi', '宽城': 'kuanchengxian', '承德县': 'chengdexian', '承德周边': 'chengdezb', '兴隆': 'xinglongxian', '平泉': 'pingquanxian'}, 'code': 'chengde|6760'}, '咸宁': {'sublist': {'通山': 'tongshanxian', '崇阳': 'chongyangxian', '赤壁': 'chibishixn', '咸安': 'xiananqu', '通城': 'tongchenxian', '嘉鱼': 'jiayuxianxn', '咸宁周边': 'xianningzb'}, 'code': 'xianning|9617'}, '攸县': {'sublist': {'城区': 'zzyouxiancq', '其他': 'zzyouxianqt'}, 'code': 'zzyouxian|1095'}, '白城': {'sublist': {'大安': 'daanshi', '白城': 'baichengshi', '洮北': 'taobei', '镇赉': 'zhenlaixian', '洮南': 'taonan', '通榆': 'tongyuxian', '白城周边': 'bcqita'}, 'code': 'bc|5918'}, '乌鲁木齐': {'sublist': {'沙依巴克': 'shayibake', '新市': 'wlmqxinshi', '乌鲁木齐县': 'wulumuqixian', '天山': 'tianshan', '米东区': 'midongdistrict', '达坂城': 'dabancheng', '乌鲁木齐周边': 'wlmqzb', '开发区': 'kaifaarea', '水磨沟': 'shuitanggou', '头屯河': 'toutunhequ'}, 'code': 'xj|984'}, '谷城': {'sublist': {'城区': 'guchengcq', '其他': 'guchengqt'}, 'code': 'gucheng|899'}, '华容': {'sublist': {'城区': 'huarongcq', '其他': 'huarongqt'}, 'code': 'huarong|830'}, '临汾': {'sublist': {'曲沃': 'quwo', '其它': 'linfenshi', '尧都': 'yaodou', '侯马': 'houma', '洪洞': 'hongdong', '古县': 'lfguxian', '霍州': 'huozhou', '襄汾': 'xiangfen', '翼城': 'lfyicheng'}, 'code': 'linfen|5669'}, '鹰潭': {'sublist': {'贵溪': 'guixi', '其他': 'yingtanqita', '余江': 'yujiangyt', '月湖': 'yuehu', '龙虎山': 'longhushan'}, 'code': 'yingtan|3209'}, '肥城': {'sublist': {'新城街道': 'xincjd', '城区': 'feichengchengqu', '中心区': 'taianzxq', '其他': 'feichengshiqita', '南城区': 'taianncq', '北城区': 'taianbcq', '西城区': 'taianxcq', '肥城周边': 'feiczb', '老城街道': 'laocjd', '东城区': 'taiandcq'}, 'code': 'feicheng|690'}, '顺德': {'sublist': {'勒流': 'leliu', '杏坛': 'xintan', '龙江': 'longjiangz', '北滘': 'beijiao', '伦教': 'lunjiao', '容桂': 'yonggui', '大良': 'daliang', '顺德': 'shunde', '均安': 'junyan', '乐从': 'luochong', '陈村': 'chencun'}, 'code': 'sd|8716'}, '黔西南': {'sublist': {'黔西南周边': 'qianxinanzb', '望谟': 'wangmo', '册亨': 'ceheng', '安龙': 'anlong', '晴隆': 'qinglongx', '普安': 'puan', '兴义': 'xingyi', '兴仁': 'xingren', '贞丰': 'zhenfeng'}, 'code': 'qxn|10434'}, '池州': {'sublist': {'东至': 'czdongzhi', '贵池': 'guichi', '石台': 'shitai', '青阳': 'qingyangx', '池州周边': 'chizhouzhoubian'}, 'code': 'chizhou|10260'}, '泰州': {'sublist': {'靖江': 'jingjiangqu', '高港': 'gaogang', '其他': 'taizhouqita', '姜堰': 'taizhoujiangyan', '兴化': 'xinghuaqu', '海陵': 'hailing', '泰兴': 'taixinqu'}, 'code': 'taizhou|693'}, '丰城': {'sublist': {'城区': 'fengchengshicq', '其他': 'fengchengshiqt'}, 'code': 'fengchengshi|5711'}, '弥勒': {'sublist': {}, 'code': 'milexian|8892'}, '临清': {'sublist': {'先锋路街道': 'lcxfljd', '大辛庄街道': 'lcdxzjd', '青年路街道': 'lcqnljd', '新华路街道': 'lcxhljd'}, 'code': 'linqing|884'}, '莱芜': {'sublist': {'高新区': 'gaoxinquq', '雪野旅游区': 'xueyelvyou', '莱城': 'laichengqu', '钢城': 'gangchengqu'}, 'code': 'lw|2292'}, '鹿邑': {'sublist': {'城区': 'luyicq', '其他': 'luyiqt'}, 'code': 'luyi|939'}, '保亭': {'sublist': {'响水镇': 'xiangshuiz', '什玲镇': 'shenling', '保亭周边': 'baotingzb', '加茂镇': 'jiamao', '保城镇': 'baocheng', '新政镇': 'xinzhengz', '三道镇': 'sandao'}, 'code': 'baoting|10367'}, '邵阳': {'sublist': {'隆回': 'longhuixian', '北塔': 'beitaqu', '武冈': 'wugangshi', '新宁': 'xinningxian', '洞口': 'dongkouxian', '双清': 'shuangqingqu', '邵东': 'shaodongxiansy', '绥宁': 'suiningqu', '大祥': 'daxiangqu', '城步县': 'shaoyangcbx', '新邵': 'xinjunxian', '邵阳县': 'shaoyangxiansy'}, 'code': 'shaoyang|2303'}, '涉县': {'sublist': {'城区': 'shexiancq', '其他': 'shexianqt'}, 'code': 'shexian|14059'}, '宜昌': {'sublist': {'长阳': 'changyang', '宜都': 'yiduqu', '当阳': 'dangyangyc', '猇亭': 'xiaoting', '五峰': 'wufengxian', '夷陵': 'yiling', '枝江': 'zhijiangyc', '宜昌周边': 'yichangqita', '东山': 'dongs', '点军': 'dianjun', '葛洲坝': 'ycgzb', '兴山': 'xingshanxian', '伍家岗': 'wujiagang', '秭归': 'ziguixian', '远安': 'yuananxian', '西陵': 'xiling'}, 'code': 'yc|858'}, '涿州': {'sublist': {}, 'code': 'zhuozhou|428'}, '海南': {'sublist': {'兴海': 'xinghaixian', '贵德': 'guidexian', '共和': 'gonghexian', '同德': 'tongdexian', '海南周边': 'hainanzhoubian', '贵南': 'guinanxian'}, 'code': 'hainan|10574'}, '象山': {'sublist': {'象山市区': 'xiangshanshiqu', '其它': 'xiangshanqita'}, 'code': 'xiangshanxian|6738'}, '临海': {'sublist': {'大洋街道': 'dayangjiedao', '邵家渡街道': 'shaojiadongjiedao', '其他': 'linhaishiqita', '杜桥镇': 'dongqiaozhen', '大田街道': 'datianjiedao', '江南街道': 'jiangnanjiedao', '古城街道': 'guchengjiedao'}, 'code': 'linhai|407'}, '钟祥': {'sublist': {'城区': 'zhongxiangshicq', '其他': 'zhongxiangshiqt'}, 'code': 'zhongxiangshi|9119'}, '邹平': {'sublist': {'黄山街道': 'huangshanjiedao', '其他': 'zoupingxianqita', '西董街道': 'xidongjiedao', '黛溪街道': 'daixijiedao', '好生街道': 'haoshengjiedao', '高新街道': 'gaoxinjiedao'}, 'code': 'zouping|946'}, '连云港': {'sublist': {}, 'code': 'lyg|2049'}, '金昌': {'sublist': {'河西堡': 'hexibao', '金川': 'jinchangshiqu', '永昌': 'yongchangxian'}, 'code': 'jinchang|7428'}, '榆林': {'sublist': {'横山': 'hengshanx', '靖边': 'jingbianxian', '定边': 'dingbianxian', '府谷': 'fuguxian', '米脂': 'mizhi', '榆阳': 'yuyang', '其它': 'yls', '神木': 'yulinshenmu', '佳县': 'sxjx', '绥德': 'suide'}, 'code': 'yl|5942'}, '乌海': {'sublist': {'滨河西区': 'wuhaibhxq', '滨河东区': 'wuhaibhdq', '海南': 'hainanqu', '海勃湾': 'haibowan', '乌达': 'wudaqu'}, 'code': 'wuhai|2404'}, '任丘': {'sublist': {'西环路街道': 'xihuanlujiedao', '新华路街道': 'xinhualujiedao', '永丰路街道': 'yongfenglujiedao', '中华路街道': 'zhonghualujiedao', '其他': 'renqiushiqita'}, 'code': 'renqiu|656'}, '简阳': {'sublist': {'简城街道': 'jianchengjiedao', '杨柳街道': 'yangliujiedao', '射洪坝街道': 'shehongbajiedao', '其他': 'jianyangshiqita', '十里坝街道': 'shilibajiedao'}, 'code': 'jianyangshi|6805'}, '京山': {'sublist': {}, 'code': 'jingshanxian|9117'}, '昆明': {'sublist': {'西山': 'xishan', '盘龙': 'panlong', '官渡': 'guandu', '安宁': 'anningshikm', '五华': 'wuhua', '呈贡': 'chenggong', '昆明周边': 'kunming'}, 'code': 'km|541'}, '琼中': {'sublist': {'中平镇': 'zhongping', '湾岭镇': 'wanling', '长征镇': 'changzhen', '琼中周边': 'qiongzhongzb', '黎母山镇': 'limushan', '和平镇': 'hepingz', '红毛镇': 'hongmao', '营根镇': 'yinggen'}, 'code': 'qiongzhong|10064'}, '兰考': {'sublist': {'兰考县': 'lkaoxian', '空港': 'konggang'}, 'code': 'lankaoxian|7393'}, '冷水江': {'sublist': {'城区': 'lengshuijiangshicq', '其他': 'lengshuijiangshiqt'}, 'code': 'lengshuijiangshi|9470'}, '日喀则': {'sublist': {'日喀则市': 'rkzrkzs', '岗巴': 'gangbaxian', '昂仁': 'angrenxian', '日喀则周边': 'rikezezhoubian', '定日': 'dingrixian', '定结': 'dingjiexian', '白朗': 'bailangxian'}, 'code': 'rkz|9615'}, '台湾': {'sublist': {'基隆': 'jilong', '台南': 'tainan', '台北': 'taibei', '台中': 'taizhong', '高雄': 'gaoxiong', '其它': 'taiwan'}, 'code': 'tw|2051'}, '拉萨': {'sublist': {'墨竹工卡': 'mozhugongka', '当雄': 'dangxiong', '城关': 'chengguan', '林周': 'linzhouxian', '达孜': 'dazi', '曲水': 'qushui', '尼木': 'nimu', '堆龙德庆': 'duilongdeqing', '其它': 'lasaqita'}, 'code': 'lasa|2055'}, '沅江': {'sublist': {'城区': 'yuanjiangscq', '其他': 'yuanjianqt'}, 'code': 'yuanjiangs|10201'}, '项城': {'sublist': {'城区': 'xiangchengchengqu', '其他': 'xiangchengshiqita'}, 'code': 'xiangchengshi|935'}, '汶上': {'sublist': {'城区': 'wenshangcq', '其他': 'wenshangqt'}, 'code': 'wenshang|460'}, '沛县': {'sublist': {'沛县市区': 'peixianshiqu', '其它': 'peixianqita'}, 'code': 'xzpeixian|11349'}, '商水': {'sublist': {'城区': 'shangshuicq', '其他': 'shangshuiqt'}, 'code': 'shangshui|936'}, '红河': {'sublist': {'河口': 'hekouxian', '弥勒': 'milexianhh', '建水': 'jianshuixian', '屏边': 'pingbianxian', '开远': 'kaiyuanshi', '绿春': 'lvchunxian', '元阳': 'yuanyangxian', '个旧': 'gejiushi', '蒙自': 'mengzixian', '金平': 'jinpingxian', '泸西': 'luxixian', '石屏': 'shipingxian', '红河县': 'honghexian'}, 'code': 'honghe|2394'}, '安吉': {'sublist': {'灵峰街道': 'lingfengjiedao', '孝源街道': 'xiaoyuanjiedao', '递铺街道': 'dipujiedao', '其他': 'anjixianqita', '昌硕街道': 'changshuojiedao'}, 'code': 'anji|836'}, '开原': {'sublist': {'城区': 'kaiyuancq', '其他': 'kaiyuanqt'}, 'code': 'kaiyuan|6733'}, '衡阳': {'sublist': {'蒸湘': 'zhengxiang', '华新开发区': 'huaxinkfq', '衡阳周边': 'hengyang', '立新开发区': 'lixinkfq', '石鼓': 'shigu', '雁峰': 'yanfeng', '珠晖': 'zhuhui', '南岳': 'nanyue'}, 'code': 'hy|914'}, '渑池': {'sublist': {'城区': 'yingchixiancq', '其他': 'yingchixianqt'}, 'code': 'yingchixian|9322'}, '恩施': {'sublist': {'咸丰': 'xianfengxian', '鹤峰': 'hefengxian', '巴东': 'badongxian', '来凤': 'laifengxian', '建始': 'jianshixian', '利川': 'lichuanshi', '宣恩': 'xuanenxian', '恩施市': 'enshishi'}, 'code': 'es|2302'}, '阿拉善盟': {'sublist': {'阿拉善右旗': 'alashanyouqi', '阿拉善左旗': 'alashanzuoqi', '阿拉善盟周边': 'alashanmengzhoubian', '额济纳旗': 'ejinaqi'}, 'code': 'alsm|10083'}, '中卫': {'sublist': {'海原': 'haiyuan', '沙坡头': 'shapotou', '中宁': 'zhongning', '中卫周边': 'zhongweizhoubian'}, 'code': 'zw|9951'}, '启东': {'sublist': {'启东市区': 'qidongshiqu', '其它': 'qidongqita'}, 'code': 'qidong|400'}, '高唐': {'sublist': {'人和街道': 'lcrhjd', '汇鑫街道': 'lchxjd', '鱼邱湖街道': 'lcyqhjd'}, 'code': 'gaotang|885'}, '永新': {'sublist': {'北路片乡镇': 'beilupianxz', '西路片乡镇': 'xilupianxz', '南路片乡镇': 'nanlupianxz', '东路片乡镇': 'donglupianxz', '永新县周边': 'yxxzhoubian', '永新县城': 'yxxchengqu'}, 'code': 'yxx|11077'}, '邓州': {'sublist': {'城区': 'dengzhoucq', '其他': 'dengzhouqt'}, 'code': 'dengzhou|595'}, '分宜': {'sublist': {'城区': 'fenyicq', '其他': 'fenyiqt'}, 'code': 'fenyi|10118'}, '江山': {'sublist': {'城区': 'jiangshanshicq', '其他': 'jiangshanshiqt'}, 'code': 'jiangshanshi|6796'}, '自贡': {'sublist': {'大安': 'daanqu', '荣县': 'rongxian', '自流井': 'ziliujing', '富顺': 'fsx', '自贡周边': 'zigongzb', '贡井': 'gongjingqu', '沿滩': 'yantanqu'}, 'code': 'zg|6745'}, '龙海': {'sublist': {'城区': 'longhaichengqu', '其他': 'longhaishiqita'}, 'code': 'longhai|713'}, '儋州': {'sublist': {'兰洋镇': 'lanyang', '雅星镇': 'yaxing', '儋州周边': 'tanzhouzb', '大成镇': 'dachengz', '那大镇': 'nada', '和庆镇': 'heqing', '南丰镇': 'nanfengz'}, 'code': 'danzhou|10394'}, '银川': {'sublist': {'金凤': 'jinfeng', '西夏': 'xixia', '永宁': 'yongningxian', '灵武': 'lingwu', '兴庆': 'xingqing', '贺兰': 'helan', '其它': 'yinchuanqita'}, 'code': 'yinchuan|2054'}, '黄冈': {'sublist': {'黄州': 'huangzhouqu', '英山': 'yingshanxian', '浠水': 'xishuixian', '罗田': 'luotianxian', '武穴': 'wuxueshihg', '麻城': 'machengshi', '红安': 'honganxian', '黄梅': 'huangmeixian', '团风': 'tuanfengxian', '龙感湖': 'longganhuqu', '蕲春': 'qichenxian'}, 'code': 'hg|2299'}, '湘阴': {'sublist': {'城区': 'xiangyincq', '其他': 'xiangyinqt'}, 'code': 'xiangyin|828'}, '北京': {'sublist': {'怀柔': 'huairou', '北京周边': 'beijingzhoubian', '房山': 'fangshan', '崇文': 'chongwen', '石景山': 'shijingshan', '东城': 'dongcheng', '海淀': 'haidian', '丰台': 'fengtai', '燕郊': 'bjyanjiao', '顺义': 'shunyi', '门头沟': 'mentougou', '大兴': 'daxing', '密云': 'miyun', '宣武': 'xuanwu', '西城': 'xicheng', '平谷': 'pinggu', '延庆': 'yanqing', '通州': 'tongzhouqu', '昌平': 'changping', '朝阳': 'chaoyang'}, 'code': 'bj|1'}, '沂南': {'sublist': {'城区': 'yinanxiancq', '其他': 'yinanxianqt'}, 'code': 'yinanxian|7301'}, '老河口': {'sublist': {'城区': 'laohekoucq', '其他': 'laohekouqt'}, 'code': 'laohekou|895'}, '枝江': {'sublist': {'城区': 'zhijiangcq', '其他': 'zhijiangqt'}, 'code': 'zhijiang|866'}, '温州': {'sublist': {'文成': 'wenchengxian', '瑞安': 'ruian', '乐清': 'yueqing', '龙湾': 'longwan', '温州周边': 'wenzhou', '鹿城': 'lucheng', '平阳': 'pingyangxianwz', '永嘉': 'yongjiaxian', '瓯海': 'ouhai', '洞头': 'dongtouxian', '苍南县': 'wenzhoucangnan', '泰顺': 'taishunxian'}, 'code': 'wz|330'}, '博白': {'sublist': {'城区': 'bobaixiancq', '其他': 'bobaixianqt'}, 'code': 'bobaixian|9173'}, '淮北': {'sublist': {'濉溪': 'suixix', '相山': 'xiangshanqu', '杜集': 'dujiqu', '烈山': 'lieshanqu', '淮北周边': 'huaibeizb'}, 'code': 'huaibei|9357'}, '醴陵': {'sublist': {'白兔潭镇': 'baitutanzhen', '国瓷街道': 'guocijiedao', '其他': 'lilingqita', '来龙门街道': 'lailongmenjiedao', '阳三石街道': 'yangsanshijiedao', '仙岳山街道': 'xianyueshanjiedao'}, 'code': 'liling|1091'}, '安岳': {'sublist': {'城区': 'anyuechengqu', '其他': 'anyuexianqita'}, 'code': 'anyuexian|6806'}, '亳州': {'sublist': {'利辛': 'lixinxian', '谯城': 'qiaochengqu', '涡阳': 'woyangxian', '蒙城': 'mengchengxian'}, 'code': 'bozhou|2329'}, '菏泽': {'sublist': {'曹县': 'hezecaoxian', '单县': 'hezeshanxian', '成武': 'chengwu', '东明': 'dongminghz', '郓城': 'hzychz', '牡丹': 'mudanqu', '鄄城': 'juanchenghz', '开发区': 'hzkaifaqu', '定陶': 'dingtao', '巨野': 'juyehz', '其它': 'hezeshi'}, 'code': 'heze|5632'}, '温岭': {'sublist': {'温岭市区': 'wenlingshiqu', '其它': 'wenlingqita'}, 'code': 'wenling|408'}, '通许': {'sublist': {'通许县': 'tongxux'}, 'code': 'tongxuxian|7390'}, '微山': {'sublist': {'城区': 'weishancq', '其他': 'weishanqt'}, 'code': 'weishan|459'}, '余姚': {'sublist': {'余姚市区': 'yuyaoshiqu', '其它': 'yuyaoqita'}, 'code': 'yuyao|5333'}, '长葛': {'sublist': {'长兴路街道': 'changxinglu', '金桥路街道': 'jinqiaolu', '建设路街道': 'jianshelujd', '长社路街道': 'changshelu', '长葛周边': 'changgezb'}, 'code': 'changge|9344'}, '呼伦贝尔': {'sublist': {'根河': 'genhe', '额尔古纳': 'eerguna', '牙克石': 'yakeshi', '扎兰屯': 'zalantun', '满洲里': 'manzhouli', '呼伦贝尔周边': 'hulunbeierzhoubian', '海拉尔': 'hailaerq'}, 'code': 'hlbe|10039'}, '青州': {'sublist': {'云门山街道': 'yunmenshanjiedao', '王府街道': 'wangfujiedao', '黄楼街道': 'huangloujiedao', '其他': 'qingzhoushiqita', '益都街道': 'yidongjiedao'}, 'code': 'qingzhou|367'}, '荣成': {'sublist': {'石岛': 'shidao', '人和镇': 'whrhz', '其他': 'rongchengshiqita', '港湾街道': 'gangwanjiedao', '桃园街道': 'rctaoyuanjiedao', '大疃镇': 'whdtz', '港西': 'gangxi', '虎山镇': 'whhsz', '斥山街道': 'chishanjiedao', '王连街道': 'wanglianjiedao', '宁津街道': 'ningjinjiedao', '东山街道': 'rcdongshanjiedao', '市区': 'whrcsq'}, 'code': 'rongcheng|522'}, '铜陵': {'sublist': {'枞阳': 'zongyang', '狮子山': 'shizishan', '郊区': 'jiaoq', '铜陵县': 'tonglingx', '铜官山': 'tongguanshan', '铜陵周边': 'tonglingzhoubian'}, 'code': 'tongling|10285'}, '湖州': {'sublist': {'长兴': 'changxingqu', '安吉县': 'huzhouanji', '南浔': 'nanxun', '其他': 'huzhoushi', '德清': 'deqingqu', '吴兴': 'wuxing'}, 'code': 'huzhou|831'}, '文山': {'sublist': {'麻栗坡': 'malipo', '富宁': 'funingqu', '丘北': 'qiubeixian', '文山': 'wenshanxian', '广南': 'guangnanxian', '西畴': 'xichouxian', '砚山': 'yanshanqu', '马关': 'maguanxian'}, 'code': 'ws|2395'}, '武义县': {'sublist': {'郭洞景区': 'guodjq', '武义周边': 'jhwyzb', '武义茶城': 'wuycc', '壶山公园': 'hushgy', '寿仙谷': 'shouxg', '城南': 'jhwycn', '牛头山森林公园': 'niutssl', '城东': 'jhwycd', '城郊': 'jhwycj', '城北': 'jhwycb', '清风寨': 'qingfz'}, 'code': 'wuyix|14528'}, '赤壁': {'sublist': {'城区': 'chibishicq', '其他': 'chibishiqt'}, 'code': 'chibishi|9623'}, '安溪': {'sublist': {'城区': 'anxixiancq', '其他': 'anxixianqt'}, 'code': 'anxixian|7100'}, '香港': {'sublist': {'九龙城': 'jiulongcheng', '其它': 'xianggang', '荃湾': 'quanwan', '沙田': 'shatian', '观塘': 'guantang', '离岛': 'lidao', '屯门': 'tunmen', '中西': 'zhongxi', '东区': 'dongqu', '黄大仙': 'huangdaxian', '湾仔': 'wanzai'}, 'code': 'hk|2050'}, '六安': {'sublist': {'舒城': 'shuchengxian', '金寨': 'jinzhaixian', '霍邱县': 'huoqiuxian', '金安': 'jinanquq', '裕安': 'yuanquq', '霍山': 'huoshanxian', '六安市区': 'liuanshiqu'}, 'code': 'la|2328'}, '呼和浩特': {'sublist': {'呼和浩特周边': 'huhehaote', '金山开发区': 'jinshankfq', '武川': 'wc', '赛罕': 'saihan', '金川开发区': 'jinchuan', '土默特左': 'tmtz', '回民': 'huimin', '如意开发区': 'ruyi', '和林格尔': 'hlge', '新城': 'xinchengqu', '清水河': 'qsh', '玉泉': 'yuquan', '托克托': 'tkt', '金桥开发区': 'jinqiaokfq'}, 'code': 'hu|811'}, '曲靖': {'sublist': {'陆良': 'luliangxian', '罗平': 'luopingxian', '师宗': 'shizongxian', '沾益': 'zhanyixian', '富源': 'qjfuyuanxian', '马龙': 'malongxian', '会泽': 'huizexian', '麒麟': 'qilinqu', '宣威': 'xuanwushiqj'}, 'code': 'qj|2389'}, '淮安': {'sublist': {'淮阴': 'huaiyin', '金湖': 'jinhuha', '盱眙': 'xuyiha', '其他': 'huaian', '清浦': 'qingpuqu', '淮安区': 'chuzhouqu', '清河': 'haqinghe', '洪泽': 'hongze', '涟水': 'lianshui', '经济开发区': 'hajjkfq'}, 'code': 'ha|968'}, '廊坊': {'sublist': {}, 'code': 'lf|772'}, '德宏': {'sublist': {}, 'code': 'dh|9437'}, '仙桃': {'sublist': {'郑场': 'zhengchang', '胡场': 'huchang', '仙桃周边': 'xiantaozb', '毛嘴': 'maozui', '长埫口': 'changshangkou', '三伏潭': 'sanfutan', '剅河': 'douhe', '市区': 'xtsq'}, 'code': 'xiantao|9736'}, '潜江': {'sublist': {'潜江周边': 'qianjiangzb', '周矶街道': 'zhoujijiedao', '泽口街道': 'zekoujiedao', '广华街道': 'guanghuajd', '园林街道': 'yuanlinjiedao', '杨市街道': 'yangshijiedao'}, 'code': 'qianjiang|9669'}, '库尔勒': {'sublist': {}, 'code': 'kel|7168'}, '梧州': {'sublist': {'苍梧': 'cangwu', '长洲': 'changzhouqv', '蒙山': 'mengshan', '藤县': 'tengxian', '万秀': 'wanxiu', '岑溪': 'cenxiwz', '蝶山': 'dieshan', '其它': 'wuzhoushi'}, 'code': 'wuzhou|2046'}, '景德镇': {'sublist': {'乐平市': 'jingdezhenleping', '浮梁': 'fuliangxianjdz', '昌江': 'changjiangqu', '珠山': 'zhushanqu'}, 'code': 'jdz|2360'}, '孝昌': {'sublist': {'城区': 'xiaochangcq', '其他': 'xiaochangqt'}, 'code': 'xiaochang|3436'}, '永春': {'sublist': {'城区': 'yongchunxiancq', '其他': 'yongchunxianqt'}, 'code': 'yongchunxian|7101'}, '乐山': {'sublist': {'马边': 'mab', '乐山周边': 'leshan', '井研': 'jingyan', '峨眉山': 'emeishan', '夹江': 'jiaj', '五通桥': 'wutongqiao', '沙湾': 'shawan', '沐川': 'muchuan', '犍为': 'jianwei', '峨边': 'ebian', '市中区': 'lsshizhong'}, 'code': 'ls|3237'}, '遵化': {'sublist': {'城区': 'zunhuacq', '其他': 'zunhuaqt'}, 'code': 'zunhua|283'}, '宝鸡': {'sublist': {'眉县': 'meixian', '渭滨': 'weibin', '凤县': 'fengxian', '金台': 'jintai', '岐山': 'qishanxian', '陈仓': 'chencang', '其它': 'baojishi'}, 'code': 'baoji|2044'}, '金华': {'sublist': {'武义县': 'wuyixjh', '东阳': 'dongyangqu', '磐安': 'panan', '其他': 'jinhua', '兰溪': 'lanxi', '义乌': 'yiwushi', '金华市区': 'wuchengqu', '永康': 'jinhuayongkang', '浦江县': 'pujiang'}, 'code': 'jh|531'}, '鄢陵': {'sublist': {'安陵镇': 'anlingzhen', '马栏镇': 'malanzhen', '望田镇': 'wangtianzhen', '马坊乡': 'mafangxiang', '南坞乡': 'nanwuxiang', '彭店乡': 'pengdianxiang', '陈店乡': 'chendianxiang', '张桥乡': 'zhangqiaoxiang', '大马乡': 'damaxiang', '陶城乡': 'taochengxiang', '只乐乡': 'zhilexiang', '柏梁镇': 'boliangzhen'}, 'code': 'yanling|9123'}, '乐清': {'sublist': {'磐石': 'yqpanshi', '芙蓉': 'yqfurong', '淡溪': 'yqdanxi', '湖雾': 'yqhuwu', '蒲岐': 'yqpuqi', '乐清周边': 'yqyueqingzhoubian', '南塘': 'yqnantang', '大荆': 'yqdajing', '雁荡': 'yqyandang', '仙溪': 'yqxianxi', '翁垟': 'yqwengxiang', '柳市': 'yqliushi', '黄华': 'yqhuanghua', '虹桥': 'yqhongqiao', '石帆': 'yqshifan', '乐成': 'yqlecheng', '象阳': 'yqxiangyang', '七里港': 'yqqiligang', '清江': 'yqqingjiang', '白石': 'yqbaishi', '北白象': 'yqbeibaixiang', '南岳': 'yqnanyue'}, 'code': 'yueqingcity|13950'}, '毕节': {'sublist': {'威宁': 'weining', '织金': 'zhijin', '纳雍': 'nayong', '毕节周边': 'bijiezhoubian', '金沙': 'jinshax', '黔西': 'qianxi', '七星关': 'bjqxg', '大方': 'dafang', '百里杜鹃': 'bjbldj', '赫章': 'hezhang'}, 'code': 'bijie|10564'}, '桂平': {'sublist': {'城区': 'guipingqucq', '其他': 'guipingquqt'}, 'code': 'guipingqu|6774'}, '东方': {'sublist': {'四更镇': 'sigeng', '东方周边': 'dongfangzb', '感城镇': 'gancheng', '三家镇': 'sanjia', '八所镇': 'basuo', '大田镇': 'datian', '板桥镇': 'banqiaoz', '新龙镇': 'xinlong', '东河镇': 'donghez'}, 'code': 'df|10250'}, '大兴安岭': {'sublist': {'呼玛': 'huma', '加格达奇': 'jiagedaqi', '漠河': 'mohe', '松岭': 'songling', '大兴安岭周边': 'daxinganlingzb', '呼中': 'huzhong', '塔河': 'tahe', '新林': 'xinlin'}, 'code': 'dxal|9878'}, '遂宁': {'sublist': {'遂宁周边': 'suiningzb', '安居': 'anjuqu', '大英': 'dayingxian', '蓬溪': 'pengxixian', '射洪': 'shehongxiansn', '船山': 'chuanshanqu'}, 'code': 'suining|9688'}, '淮滨': {'sublist': {'城区': 'huaibinxiancq', '其他': 'huaibinxianqt'}, 'code': 'huaibinxian|8702'}, '定西': {'sublist': {'陇西': 'longxix', '通渭': 'tongwei', '漳县': 'zhangxian', '定西周边': 'dingxizhoubian', '安定': 'anding', '临洮': 'lintao', '渭源': 'weiyuanx', '岷县': 'minxian'}, 'code': 'dx|10322'}, '桦甸': {'sublist': {'城区': 'huadiancq', '其他': 'huadianqt'}, 'code': 'huadian|706'}, '宿州': {'sublist': {'灵璧': 'lingbi', '其他': 'suzhoushi', '砀山': 'dangshan', '萧县': 'xiaoxian', '泗县': 'sixian', '墉桥': 'yongqiao'}, 'code': 'suzhou|3359'}, '余江': {'sublist': {'城区': 'yujiangcq', '其他': 'yujiangqt'}, 'code': 'yujiang|3210'}, '霍邱': {'sublist': {'姚李': 'yaoli', '马店': 'madianz', '霍邱周边': 'huoqiuzb', '河口': 'hekouz', '众兴': 'zongxing', '长集': 'changjiz', '新店': 'xindianz', '周集': 'zhouji', '城关': 'chengguanz', '户胡': 'huhu'}, 'code': 'hq|11226'}, '鹤岗': {'sublist': {'南山': 'nanshanquq', '兴山': 'xingshanqu', '兴安': 'xinganqu', '工农': 'gongnongqu', '东山': 'dongshanqu', '萝北': 'luobeixian', '向阳': 'xiangyangquq', '绥滨': 'suibinxian'}, 'code': 'hegang|9061'}, '三亚': {'sublist': {'凤凰镇': 'fenghuangzhen', '海棠区': 'syhtq', '崖州区': 'syyzq', '天涯区': 'sytyq', '三亚周边': 'syzb', '河西': 'hexiquyu', '吉阳区': 'syjyq'}, 'code': 'sanya|2422'}, '克孜勒苏': {'sublist': {'乌恰': 'wuqiaxian', '阿合奇': 'aheqixian', '阿图什': 'atushishi', '克孜勒苏周边': 'kezileshuzhoubian'}, 'code': 'kzls|9519'}, '博罗': {'sublist': {'罗阳': 'hzluoyang', '博罗周边': 'boluozb', '石湾': 'hzshiwan', '龙溪': 'hzlongxi', '园洲': 'hzyuanzhou'}, 'code': 'boluo|726'}, '莘县': {'sublist': {'莘亭街道': 'lcxtjd', '燕塔街道': 'lcytjd', '东鲁街道': 'lcdljd', '莘州街道': 'lcxzjd'}, 'code': 'shenxian|888'}, '磐石': {'sublist': {'城区': 'panshicq', '其他': 'panshiqt'}, 'code': 'panshi|708'}, '张家界': {'sublist': {'桑植': 'sangzhixian', '永定': 'yongdingqu', '武陵源': 'wulingyuanqu', '慈利': 'cilixianzjj'}, 'code': 'zjj|6788'}, '林芝': {'sublist': {'墨脱': 'motuoxian', '朗县': 'langxian', '米林': 'milinxian', '林芝': 'linzhixian', '林芝周边': 'linzhizb', '八一镇': 'bayizhen', '波密': 'bomixian', '工布江达': 'gongbujiangdax', '察隅': 'chayuxian'}, 'code': 'linzhi|9646'}, '滕州': {'sublist': {'龙泉街道': 'longquanjiedao', '其他': 'tengzhoushiqita', '善南街道': 'shannanjiedao', '荆河街道': 'jinghejiedao', '北辛街道': 'beixinjiedao'}, 'code': 'tengzhou|967'}, '宁德': {'sublist': {'寿宁': 'shouningxian', '蕉城': 'jiaochengqu', '周宁': 'zhouningxian', '福安': 'fuanshind', '霞浦': 'xiapuxian', '柘荣': 'zhenrongxian', '福鼎': 'fudingshind', '屏南': 'pingnanxianq', '古田': 'gutianxian', '东侨区': 'dongqiaoqund'}, 'code': 'nd|7951'}, '进贤': {'sublist': {'城区': 'jinxiancq', '其他': 'jinxianqt'}, 'code': 'jinxian|677'}, '宁津': {'sublist': {'城区': 'ningjincq', '其他': 'ningjinqt'}, 'code': 'ningjin|733'}, '莱阳': {'sublist': {'城区': 'laiyangcq', '其他': 'laiyangqt'}, 'code': 'laiyang|234'}, '益阳': {'sublist': {'沅江': 'yuanjiangsyy', '益阳周边': 'yiyangzhoubian', '安化': 'anhua', '南县': 'nanxianyy', '桃江': 'taojiang', '赫山': 'heshanq', '资阳': 'ziyangq'}, 'code': 'yiyang|10198'}, '厦门': {'sublist': {'集美': 'jimei', '翔安': 'xiangan', '厦门周边': 'xiamenzhoubian', '杏林': 'xmxl', '湖里': 'huli', '同安': 'tongan', '思明': 'siming', '海沧': 'haicang'}, 'code': 'xm|606'}, '浚县': {'sublist': {'城区': 'junxiancq', '其他': 'junxianqt'}, 'code': 'junxian|9185'}, '昌吉': {'sublist': {'吉木萨尔': 'jimusaerxian', '昌吉': 'changjishi', '玛纳斯': 'manasixian', '奇台': 'qitaixian', '阜康': 'fukangshi', '木垒': 'muleixian', '呼图壁': 'hutubishi'}, 'code': 'changji|8582'}, '广汉': {'sublist': {'雒城镇': 'luochengzhen', '其他': 'guanghanshiqita', '中心城区': 'ghzhongxinchengqu'}, 'code': 'guanghanshi|8719'}, '邢台': {'sublist': {'南和': 'nanhe', '沙河': 'shaheshixt', '桥东': 'qiaodongqu', '其他': 'xingtai', '南宫': 'nangong', '清河': 'xtqinghe', '平乡': 'pingxiangxian', '桥西': 'qiaoxiqu', '邢台县': 'xingtaixian'}, 'code': 'xt|751'}, '石嘴山': {'sublist': {'惠农': 'huinong', '石嘴山周边': 'shizuishanzhoubian', '大武口': 'dawukou', '平罗': 'pingluo'}, 'code': 'szs|9971'}, '嘉鱼': {'sublist': {'城区': 'jiayuxiancq', '其他': 'jiayuxianqt'}, 'code': 'jiayuxian|9624'}, '南县': {'sublist': {'城区': 'nanxiancq', '其他': 'nanxianqt'}, 'code': 'nanxian|10202'}, '黄山': {'sublist': {'黟县': 'yix', '黄山周边': 'huangshanzhoubian', '休宁': 'xiuning', '祁门': 'qimen', '屯溪': 'taipq', '黄山风景区': 'huangshanfjq', '歙县': 'shex', '徽州': 'huizhouq', '黄山': 'huangshanq'}, 'code': 'huangshan|2323'}, '西安': {'sublist': {'长安': 'changanlu', '高新区': 'xagx', '沣渭新区': 'fengweixinq', '阎良': 'yanliang', '灞桥': 'baqiao', '新城': 'xaxincheng', '雁塔': 'yanta', '临潼': 'lintong', '碑林': 'beilin', '曲江新区': 'qujiangxinq', '杨凌': 'yangling', '未央': 'weiyang', '莲湖': 'lianhu', '西安周边': 'xianzhoubian'}, 'code': 'xa|483'}, '东平': {'sublist': {'望山街': 'tiaanwsj', '佛山街': 'taianfsj', '龙山大街': 'taianlsdj', '东平街道': 'dongpjd', '东山路': 'taiandsl', '东平县周边': 'dongpxzb', '稻香街': 'taiandxj', '东原路': 'taiandyl'}, 'code': 'dongping|692'}, '建湖': {'sublist': {'建湖市区': 'jianhushiqu', '其它': 'jianghuqita'}, 'code': 'jianhu|618'}, '泰安': {'sublist': {'泰安周边': 'taian', '新泰': 'taianxintai', '东平': 'dongpingta', '泰山区': 'taishanqu', '岱岳区': 'daiyue', '肥城': 'taianfeicheng', '宁阳': 'ningyangta'}, 'code': 'ta|686'}, '冠县': {'sublist': {'清泉街道': 'lcqqjd', '烟庄街道': 'lcyzjd', '崇文街道': 'lccwjd'}, 'code': 'guanxian|890'}, '松原': {'sublist': {'宁江': 'ningjiangxian', '农业高新产业开发区': 'nongyequ', '乾安': 'qiananxian', '长岭': 'changlingxiansy', '扶余': 'fuyuxiansy', '前郭': 'guoerls', '经济技术开发区': 'jingjijs'}, 'code': 'songyuan|2315'}, '丽江': {'sublist': {'永胜': 'yongshengxian', '玉龙': 'yulongxian', '华坪': 'huapingxian', '宁蒗': 'ninglangxian', '古城': 'guchengqu'}, 'code': 'lj|2392'}, '宜阳': {'sublist': {'城区': 'lyyiyangcq', '其他': 'lyyiyangqt'}, 'code': 'lyyiyang|11219'}, '韩城': {'sublist': {'桢州大街': 'zhenzhoudj', '韩城周边': 'hanchengzb', '太史大街': 'taishidajie'}, 'code': 'hancheng|5735'}, '大庆': {'sublist': {'让胡路': 'ranghulu', '萨尔图': 'saertu', '红岗': 'honggang', '龙凤': 'longfeng', '其他': 'daqing', '大同': 'datong'}, 'code': 'dq|375'}, '灯塔': {'sublist': {'城区': 'dengtacq', '其他': 'dengtaqt'}, 'code': 'dengta|2071'}, '江门': {'sublist': {'鹤山': 'heshan', '台山': 'taishanshi', '开平': 'kaipingshijm', '蓬江': 'pengjiang', '南新': 'nanxin', '江门周边': 'jiangmen', '恩平': 'enping', '江海': 'jianghai', '新会': 'xinhui', '北新': 'beixin'}, 'code': 'jm|629'}, '六盘水': {'sublist': {'水城': 'shuicheng', '盘县': 'panx', '六盘水周边': 'liupanshuizb', '六枝特区': 'liuzhi', '钟山': 'zhongshanq'}, 'code': 'lps|10506'}, '衡东': {'sublist': {'城区': 'hengdongcq', '其他': 'hengdongqt'}, 'code': 'hengdong|5693'}, '驻马店': {'sublist': {'西平': 'xiping', '上蔡': 'shangcai', '汝南': 'runan', '泌阳': 'biyang', '平舆': 'pingyu', '正阳': 'zhengyangxian', '其他': 'zhumadian', '遂平': 'suiping', '新蔡': 'xincai', '驿城': 'yichengqu', '确山': 'queshan'}, 'code': 'zmd|1067'}, '陵水': {'sublist': {'光坡镇': 'guangpo', '隆广镇': 'longguang', '文罗镇': 'wenluo', '英州镇': 'yingzhouz', '陵水周边': 'lingshuizb', '椰林镇': 'yelin', '三才镇': 'sancai'}, 'code': 'lingshui|10184'}, '海安': {'sublist': {'其它': 'haianqita', '海安市区': 'haianshiqu'}, 'code': 'haian|401'}, '南京': {'sublist': {'六合': 'liuhequ', '玄武': 'xuanwuqu', '秦淮': 'qinhuai', '白下': 'baixia', '鼓楼': 'gulouqu', '大厂': 'dachangqu', '南京周边': 'nanjing', '浦口': 'pukouqu', '溧水': 'lishuixian', '栖霞': 'qixiaqu', '下关': 'xiaguan', '高淳': 'gaochunxian', '江宁': 'jiangning', '建邺': 'jianye', '雨花台': 'yuhuatai'}, 'code': 'nj|172'}, '泽州': {'sublist': {'城区': 'zezhoucq', '其他': 'zezhouqt'}, 'code': 'zezhou|3353'}, '齐河': {'sublist': {'城区': 'qihecq', '其他': 'qiheqt'}, 'code': 'qihe|734'}, '黄骅': {'sublist': {'城区': 'huanghuacq', '其他': 'huanghuaqt'}, 'code': 'huanghua|657'}, '宝应县': {'sublist': {'城区': 'baoyingchengqu', '宝应县周边': 'baoyingxzb', '其他': 'baoyingxianqita'}, 'code': 'baoyingx|14451'}, '石家庄': {'sublist': {'长安': 'changan', '裕华': 'yuhua', '桥东': 'qiaodong', '新华': 'sjzxinhua', '鹿泉': 'luquan', '桥西': 'qiaoxi', '开发区': 'sjzkaifaqu', '石家庄周边': 'shijiazhuang', '井陉矿区': 'jingjingkuangqu', '栾城': 'luanchengxian', '正定': 'zhengdingxian', '藁城': 'gaocheng'}, 'code': 'sjz|241'}, '和田': {'sublist': {'洛浦': 'luopuxian', '民丰': 'minfengxian', '墨玉': 'moyuxian', '皮山': 'pishanxian', '于田': 'yutx', '和田周边': 'hetianzhoubian', '和田县': 'hetianxian', '策勒': 'celexian'}, 'code': 'ht|9489'}, '铜川': {'sublist': {}, 'code': 'tc|9832'}, '普洱': {'sublist': {'思茅': 'simaoqu', '宁洱': 'ningerxian', '景谷': 'jingguxian', '普洱周边': 'puerzhoubian', '镇沅': 'zhenyuanxian', '景东': 'jingdongxian', '墨江': 'mojiangxian'}, 'code': 'pe|9444'}, '五家渠': {'sublist': {'101团': 'yilingyituan', '人民路': 'renml', '青湖路': 'qinghulu', '103团': 'yilingsantuan', '五家渠周边': 'wujiaquzhoubian', '102团': 'yilingertuan', '军垦路': 'junkenlu'}, 'code': 'wjq|9562'}, '平邑': {'sublist': {'城区': 'pingyicq', '其他': 'pingyiqt'}, 'code': 'pingyi|514'}, '十堰': {'sublist': {'竹山': 'zhushan', '郧西': 'yunxixian', '白浪经济开发区': 'sybljjkfq', '张湾': 'zhangwan', '竹溪': 'zhuxi', '房县': 'fangxian', '丹江口': 'danjiangkou', '郧阳区': 'yunxian', '十堰周边': 'shiyanshi', '武当山': 'sywds', '茅箭': 'maojian'}, 'code': 'shiyan|2032'}, '楚雄': {'sublist': {'南华': 'nanhuaxian', '双柏': 'shuangbaixian', '元谋': 'yuanmouxian', '永仁': 'yongrenxian', '大姚': 'dayaoxian', '姚安': 'yaoanxian', '禄丰': 'lufengxian', '武定': 'wudingxian', '牟定': 'moudingxian', '楚雄': 'chuxiongshi'}, 'code': 'cx|2393'}, '武威': {'sublist': {'武威周边': 'wuweizhoubian', '古浪': 'gulang', '民勤': 'minqin', '天祝': 'tianzx', '凉州': 'liangzhou'}, 'code': 'wuwei|10448'}, '北海': {'sublist': {'合浦': 'hepuxian', '北海周边': 'beihaizhoubian', '铁山港区': 'tieshangangqu', '银海': 'yinhaiqu', '海城': 'haichengqu'}, 'code': 'bh|10536'}, '平凉': {'sublist': {'静宁': 'jingningxian', '泾川': 'jingchuanxian', '灵台': 'lingtaixian', '华亭': 'huatingxian', '庄浪': 'zhuanglangxian', '崆峒': 'kongtongqu', '崇信': 'chongxinxian'}, 'code': 'pl|7154'}, '揭阳': {'sublist': {'惠来': 'huilai', '揭东': 'jiedong', '榕城': 'rongchengqu', '其他': 'jieyang', '普宁': 'puning', '揭西': 'jiexi'}, 'code': 'jy|927'}, '湘潭': {'sublist': {'湘潭县': 'xiangtanxian', '韶山': 'shaoshan', '九华经济开发区': 'jiuhuajingjikfq', '湘潭周边': 'xiangtanqita', '湘乡': 'xiangxiang', '雨湖': 'yuhu', '岳塘': 'yuetang'}, 'code': 'xiangtan|2047'}, '鹤壁': {'sublist': {'淇县': 'qixianqhb', '山城': 'shanchengqu', '浚县': 'xunxianhb', '鹤山': 'heshanqu', '淇滨': 'qibinqu'}, 'code': 'hb|2344'}, '如东': {'sublist': {'如东市区': 'rudongshiqu', '其它': 'rudongqita'}, 'code': 'rudong|402'}, '萍乡': {'sublist': {'芦溪': 'luxi', '湘东': 'xiangdong', '安源': 'anyuan', '上栗': 'shangli', '莲花': 'lianhuaxian', '其它': 'pingxiang'}, 'code': 'px|2248'}, '兰州': {'sublist': {'西固': 'xigu', '城关': 'chengguanqv', '红古': 'honggu', '七里河': 'qilihe', '新区': 'lzxq', '安宁': 'anning', '兰州周边': 'lanzhou'}, 'code': 'lz|952'}, '惠东': {'sublist': {'巽寮': 'xunliao', '黄埠': 'huangbu', '惠东周边': 'huidongzb', '平山': 'hzpingshan', '大岭': 'daling'}, 'code': 'huidong|725'}, '茌平': {'sublist': {'信发街道': 'lcxfjd', '振兴街道': 'lczxjd'}, 'code': 'chiping|887'}, '运城': {'sublist': {'芮城': 'ruicheng', '稷山': 'jishan', '河津': 'hejin', '新绛': 'xinjiangxian', '闻喜': 'wenxi', '临猗': 'yclinyi', '万荣': 'wanrong', '其它': 'yunchengshi', '永济': 'yongji', '盐湖': 'yanhu'}, 'code': 'yuncheng|5653'}, '宁国': {'sublist': {'宁国市区': 'ningguoshiqu', '其它': 'ningguoqita'}, 'code': 'ningguo|5645'}, '阿坝': {'sublist': {'汶川县': 'wenchuanxian', '阿坝周边': 'abazhoubian', '茂县': 'maoxian', '小金': 'xiaojinxian', '马尔康': 'maerkangxian', '九寨沟': 'jiuzhaigouxian', '松潘': 'songpanxian'}, 'code': 'ab|9817'}, '沈丘': {'sublist': {'城区': 'shenqiucq', '其他': 'shenqiuqt'}, 'code': 'shenqiu|942'}, '荆门': {'sublist': {}, 'code': 'jingmen|2296'}, '南城': {'sublist': {'城区': 'nanchengxcq', '其他': 'nanchengxqt'}, 'code': 'nanchengx|10137'}, '泉州': {'sublist': {'德化': 'dehuaxian', '金门县': 'qzjmx', '洛江': 'luojiang', '鲤城': 'qzlicheng', '惠安': 'huianxian', '安溪': 'anxixianqz', '丰泽': 'fengze', '泉港': 'quangang', '台商投资区': 'qztstzq', '泉州周边': 'quanzhouzb', '桥南片区': 'qiaonanpianqu', '晋江': 'jinjiangqunew', '石狮': 'shishiqu', '南安': 'nananqunew', '永春': 'yongchunxianqz'}, 'code': 'qz|291'}, '宜宾': {'sublist': {'翠屏': 'cuipingqu', '珙县': 'gongxian', '高县': 'gaoxian', '长宁': 'changningxyb', '南溪': 'nanxixian', '兴文': 'xingwenxian', '筠连': 'junlianxian', '江安': 'jianganxian', '屏山': 'pingshanxian', '宜宾县': 'yibinxian'}, 'code': 'yb|2380'}, '新野': {'sublist': {'城区': 'xinyecq', '其他': 'xinyeqt'}, 'code': 'xinye|603'}, '海北': {'sublist': {'门源': 'menyuan', '祁连': 'qilian', '刚察': 'gangcha', '海晏': 'haiyanx', '海北周边': 'haibeizhoubian'}, 'code': 'haibei|9917'}, '长垣': {'sublist': {'南蒲街道': 'cynanpujiedao', '蒲东街道': 'pudongjiedao', '其他': 'changyuanxianqita', '蒲北街道': 'pubeijiedao', '魏庄街道': 'weizhuangjiedao', '蒲西街道': 'puxijiedao'}, 'code': 'changyuan|5936'}, '响水': {'sublist': {'城区': 'xiangshuicq', '其他': 'xiangshuiqt'}, 'code': 'xiangshui|619'}, '徐州': {'sublist': {'铜山': 'xztongshan', '睢宁': 'xzsuining', '贾汪': 'jiawang', '徐州周边': 'xuzhou', '邳州': 'pizhouqu', '鼓楼': 'xzgulou', '丰县': 'xzfengx', '沛县': 'peixianqu', '云龙': 'yunlong', '泉山': 'quanshan', '新沂': 'xinyiqu', '金山桥开发区': 'jsqkfq', '新城区': 'xchengqu', '九里': 'jiuli'}, 'code': 'xz|471'}, '柳林': {'sublist': {'城区': 'liulincq', '其他': 'liulinqt'}, 'code': 'liulin|3225'}, '邵阳县': {'sublist': {'城区': 'shaoyangxiancq', '其他': 'shaoyangxianqt'}, 'code': 'shaoyangxian|6955'}, '盐城': {'sublist': {'盐都': 'yandou', '响水': 'xiangshuiyc', '建湖': 'jianhuqu', '其他': 'yanchengshi', '射阳': 'sheyangyc', '东台': 'dongtaiqu', '亭湖': 'tinghu', '大丰': 'dafengshi', '阜宁': 'funingxianyc', '滨海': 'binhai'}, 'code': 'yancheng|613'}, '甘南': {'sublist': {'合作': 'hezuo', '夏河': 'xiahe', '卓尼': 'zuoni', '临潭': 'lintan', '碌曲': 'luqu', '舟曲': 'zhouqu', '甘南周边': 'gannanzhoubian', '玛曲': 'maqu', '迭部': 'diebu'}, 'code': 'gn|10343'}, '济源': {'sublist': {'龙泉街道': 'longquanjd', '天坛街道': 'tiantanjd', '双桥街道': 'shuangqiaojd', '济源周边': 'jiyuanzb', '济水街道': 'jishuijd', '北海街道': 'beihaijd'}, 'code': 'jiyuan|9918'}, '姜堰': {'sublist': {'罗塘街道': 'luotangjiedao', '三水街道': 'sanshuijiedao', '其他': 'jiangyanqita'}, 'code': 'jiangyan|697'}, '长春': {'sublist': {'南关': 'nanguan', '汽车城': 'qichecheng', '双阳': 'shuangyang', '二道': 'erdao', '农安': 'nongan', '德惠': 'dehui', '绿园': 'lvyuan', '经开': 'jingkai', '九台': 'jiutai', '宽城': 'kuancheng', '高新': 'ccgaoxin', '榆树': 'yushu', '朝阳': 'chaoyangqu', '长春周边': 'changchun', '净月': 'jingyue'}, 'code': 'cc|319'}, '云浮': {'sublist': {'新兴': 'xinxingx', '云安': 'yuanan', '罗定': 'luoding', '郁南': 'yunan', '云城': 'yuanchengq', '云浮周边': 'yuanfuzhoubian'}, 'code': 'yf|10485'}, '固始': {'sublist': {'城区': 'gushixiancq', '其他': 'gushixianqt'}, 'code': 'gushixian|8698'}, '百色': {'sublist': {'平果': 'pingguoxian', '右江': 'youjiangqu', '德保': 'debaoxian', '田阳': 'tianyangxian', '百色周边': 'baisezhoubian', '隆林': 'longlinxian', '田东': 'tiandongxian'}, 'code': 'baise|10513'}, '保山': {'sublist': {'隆阳': 'longyangqu', '龙陵': 'longlingxian', '昌宁': 'changningxian', '腾冲': 'tengchongxian', '施甸': 'shidianxian'}, 'code': 'bs|2390'}, '沭阳': {'sublist': {'沭城镇': 'lysczhen'}, 'code': 'shuyang|5772'}, '长兴': {'sublist': {'长兴市区': 'changxingshiqu', '其它': 'chongxingqita'}, 'code': 'changxing|834'}, '靖江': {'sublist': {'靖江市区': 'jingjiangshiqu', '其它': 'jingjiangqita'}, 'code': 'jingjiang|698'}, '舞钢': {'sublist': {'城区': 'wugangcq', '其他': 'wugangqt'}, 'code': 'wugang|1011'}, '固安': {'sublist': {'古玩市场': 'guwanshichangga', '孔雀城': 'kongquechengga', '工业园区': 'gongyeyuanquga', '英才中学': 'yingcaizhongxuega', '四小': 'sixiaogalf', '长途汽车站': 'changtuqichezhanga', '一小城小': 'yixiaochengxiaoga', '县政府': 'xianzhengfuga', '滨河公园': 'binhegognyuan', '牛驼温泉': 'niutuowenquanga', '民政局': 'minzhengjugalf', '二中': 'erhzongga', '县一中': 'xianyizhonggalf', '三小': 'sanxiaoga', '人民医院': 'renminyiyuangalf'}, 'code': 'lfguan|12803'}, '灵宝': {'sublist': {}, 'code': 'lingbaoshi|9307'}, '梅州': {'sublist': {'平远': 'pingyuanxian', '五华': 'wuhuaxian', '梅州周边': 'meizhouzb', '梅江': 'meijiangqu', '梅县': 'meixianm', '大埔': 'dapuxian', '兴宁': 'xingningshi', '蕉岭': 'jiaolingxian', '丰顺': 'fengshunxian'}, 'code': 'mz|9389'}, '临猗': {'sublist': {'孙吉镇': 'sunjizhen', '楚候乡': 'chuhouxiang', '猗氏镇': 'yishizhen', '临晋镇': 'linjinzhen', '北景乡': 'beijingxiang', '角杯乡': 'jiaobeixiang', '北辛乡': 'beixinxiang', '庙上乡': 'miaoshangxiang', '三管镇': 'sanguanzhen', '七级镇': 'qijizhen', '耽子镇': 'danzizhen', '嵋阳镇': 'emeizhen', '东张镇': 'dongzhangzhen'}, 'code': 'linyixian|9193'}, '镇江': {'sublist': {'句容': 'zjjurong', '镇江新区': 'zhenjiangxinqu', '扬中': 'yangzhongsq', '丹阳': 'danyangqu', '其他': 'zhenjiangqita', '京口': 'jingkou', '润州': 'runzhou', '丹徒': 'dantu'}, 'code': 'zj|645'}, '深圳': {'sublist': {'盐田': 'yantian', '深圳周边': 'shenzhenzhoubian', '罗湖': 'luohu', '龙华新区': 'szlhxq', '福田': 'futian', '南山': 'nanshan', '光明新区': 'guangmingxinqu', '宝安': 'baoan', '龙岗区': 'longgang', '坪山新区': 'pingshanxinqu', '大鹏新区': 'dapengxq', '布吉': 'buji'}, 'code': 'sz|4'}, '广元': {'sublist': {'利州': 'lizhouqu', '旺苍': 'wangcangqu', '苍溪': 'cangxixian', '元坝': 'yuanbaqu', '广元周边': 'guangyuanzhoubian', '朝天': 'chaotianqu', '剑阁': 'jiangexian', '青川': 'qingchuanxian'}, 'code': 'guangyuan|9749'}, '仁寿': {'sublist': {'城区': 'renshouchengqu', '其他': 'renshouxianqita'}, 'code': 'renshouxian|9706'}, '泸州': {'sublist': {'龙马潭': 'longmatanqu', '古蔺': 'gulinxian', '合江': 'hejiangxian', '纳溪': 'naxiqu', '叙永': 'xuyongxian', '泸州周边': 'luzhouzb', '泸县': 'luxian', '江阳': 'jiangyangqu'}, 'code': 'luzhou|2372'}, '宣汉': {'sublist': {'城区': 'xuanhancq', '其他': 'xuanhanqt'}, 'code': 'xuanhan|9804'}, '栖霞': {'sublist': {'城区': 'qixiacq', '其他': 'qixiaqt'}, 'code': 'qixia|238'}, '盱眙': {'sublist': {'城区': 'xuyicq', '其他': 'xuyiqt'}, 'code': 'xuyi|976'}, '磁县': {'sublist': {'城区': 'cixiancq', '其他': 'cixianqt'}, 'code': 'cixian|591'}, '鄄城': {'sublist': {'城区': 'juanchengcq', '其他': 'juanchengqt'}, 'code': 'juancheng|5635'}, '延安': {'sublist': {'甘泉': 'ganquanxian', '吴起': 'wuqixian', '黄陵': 'huanglingxian', '富县': 'fuxian', '延川': 'yanchuanxian', '宜川': 'yichuanxian', '子长': 'zichangxian', '洛川': 'luochuanxian', '延长': 'yanchangxian', '黄龙': 'huanglongxian', '安塞': 'anzaixian', '宝塔': 'baotaqu', '志丹': 'zhidanxian'}, 'code': 'yanan|8973'}, '明港': {'sublist': {'甘岸': 'ganan', '查山': 'chashan', '平昌': 'pingchang', '兰店': 'landian', '长台': 'changtaiqu', '明港': 'minggangqu', '肖店': 'xiaodianqu', '王岗': 'wanggang', '刑集': 'xingji'}, 'code': 'mg|8541'}, '双峰': {'sublist': {}, 'code': 'shuangfengxian|9473'}, '德阳': {'sublist': {'德阳周边': 'deyangzb', '什邡': 'shenfangshi', '中江': 'zhongjiangxian', '广汉市': 'deyangguanghan', '罗江': 'luojiangxian', '绵竹': 'mianzhushi', '旌阳': 'jingyangqu'}, 'code': 'deyang|2373'}, '兴化': {'sublist': {'兴化市区': 'xinghuashiqu', '其它': 'xinghuaqita'}, 'code': 'xinghuashi|699'}, '安陆': {'sublist': {'城区': 'anlucq', '其他': 'anluqt'}, 'code': 'anlu|3442'}, '淄博': {'sublist': {'周村': 'zhoucun', '桓台县': 'zibohengtai', '博山': 'boshan', '高青': 'gaoqingxian', '其他': 'zibo', '张店': 'zhangdian', '开发区': 'kaifaquyu', '淄川': 'zichuan', '沂源': 'yiyuanxianzb', '临淄': 'linzi'}, 'code': 'zb|385'}, '永州': {'sublist': {'宁远': 'ningyuan', '江华': 'jianghua', '祁阳': 'qiyangyz', '道县': 'daoxiang', '江永': 'jiangyong', '蓝山': 'langshan', '新田': 'xintian', '零陵': 'linglingqu', '双牌': 'shuangpai', '冷水滩': 'lengshuitangqu', '东安': 'donganxian'}, 'code': 'yongzhou|2307'}, '太康': {'sublist': {'城区': 'taikangcq', '其他': 'taikangqt'}, 'code': 'taikang|938'}, '东海': {'sublist': {'东海市区': 'donghaishiqu', '其它': 'donghaiqita'}, 'code': 'donghai|2147'}, '张掖': {'sublist': {'民乐': 'minle', '肃南': 'sunan', '高台': 'gaotai', '临泽': 'linzhe', '山丹': 'shandan', '张掖周边': 'zhangyezhoubian'}, 'code': 'zhangye|10454'}, '昌都': {'sublist': {}, 'code': 'changdu|9648'}, '商洛': {'sublist': {'商州': 'shangzhou', '丹凤': 'danfeng', '商南': 'sangnan', '洛南': 'luonan', '柞水': 'zuoshui', '镇安': 'zhenanx', '山阳': 'shanyangx', '商洛周边': 'sangluozhoubian'}, 'code': 'sl|9854'}, '葫芦岛': {'sublist': {'连山': 'lianshan', '绥中': 'suizhong', '兴城': 'xingcheng', '葫芦岛周边': 'huludaozhoubian', '北港工业区': 'beiganggongye', '南票': 'nanpiao', '开发区': 'hldkaifaqu', '建昌': 'jianchang', '龙港': 'longgangq'}, 'code': 'hld|10088'}, '赵县': {'sublist': {'王西章乡': 'wangxizhangxiang', '赵州镇': 'zhaozhouzhen', '谢庄乡': 'xiezhuangxiang', '高村乡': 'gaocunxiang', '前大章乡': 'qiandazhangxiang', '南柏舍镇': 'nanbaishezhen', '沙河店镇': 'shahedianzhen', '范庄镇': 'fanzhuangzhen', '新寨店镇': 'xinzhaidianzhen', '韩村镇': 'hancunzhen', '北王里镇': 'beiwanglizhen'}, 'code': 'zx|9048'}, '大悟': {'sublist': {'城区': 'dawucq', '其他': 'dawuqt'}, 'code': 'dawu|3437'}, '安康': {'sublist': {'汉阴县': 'ankanghyx', '镇坪': 'zhenping', '旬阳': 'xunyangxian', '宁陕县': 'ankangnsx', '其他': 'ankangshi', '平利县': 'ankangplx', '白河县': 'ankangbhx', '汉滨': 'hanbin', '石泉县': 'ankangsqx', '紫阳': 'ziyang', '岚皋': 'langao'}, 'code': 'ankang|3157'}, '滨州': {'sublist': {'高新区': 'gaoxinbz', '阳信': 'yangxin', '其他': 'binzhou', '惠民': 'huiminxian', '沾化': 'zhanhua', '滨城': 'bincheng', '邹平': 'binzhouzouping', '无棣': 'wudibz', '博兴': 'boxingbz'}, 'code': 'bz|944'}, '陆丰': {'sublist': {'大安': 'daans', '南塘': 'nantang', '陂洋': 'piyang', '河东': 'hedongs', '湖东': 'hudong', '内湖': 'neihu', '金厢': 'jinxiangs', '潭西': 'tanxi', '上英': 'shangying', '甲子': 'jiazi', '东海': 'xiancheng', '城东': 'chengdongss', '碣石': 'jieshi', '博美': 'swbomei', '八万': 'bawan', '甲东': 'jiadong', '桥冲': 'qiaochong', '西南': 'xinans', '河西': 'hexis', '甲西': 'jiaxi', '陆丰周边': 'qitalf'}, 'code': 'lufengshi|9456'}, '河间': {'sublist': {'城区': 'hejiancq', '其他': 'hejianqt'}, 'code': 'hejian|658'}, '达州': {'sublist': {'开江': 'kaijiang', '达县': 'daxian', '宣汉': 'xuanhandz', '通川': 'tongchuanqu', '达州周边': 'dazhouzhoubian', '万源': 'wanyuanshi', '大竹': 'dazudz', '渠县': 'quxdz'}, 'code': 'dazhou|9799'}, '抚顺': {'sublist': {'高湾新区': 'gaowanxinqu', '其他': 'fushunshi', '开发区': 'fskaifa', '胜利': 'fsshengli', '新宾': 'xinbin', '清原': 'fsqingyuan', '李石开发区': 'lishikaifaqu', '抚顺': 'fushunxian', '望花': 'wanghua', '东洲': 'dongzhou', '顺城': 'shuncheng', '新抚': 'xinfuqu'}, 'code': 'fushun|5722'}, '凉山': {'sublist': {'德昌': 'dechang', '凉山周边': 'liangshanzhoubian', '甘洛': 'ganluo', '布拖': 'butuo', '会理': 'huili', '会东': 'huid', '西昌': 'xichangshi'}, 'code': 'liangshan|9717'}, '泗洪': {'sublist': {'城区': 'sihongchengqu', '其他': 'sihongqita'}, 'code': 'sihong|5958'}, '哈尔滨': {'sublist': {'木兰': 'hebmulan', '哈尔滨周边': 'haerbin', '道里': 'daoli', '宾县': 'hebbinxian', '南岗': 'nangang', '通河': 'hebtonghe', '依兰': 'hebyilan', '开发区': 'hrbkaifaqu', '道外': 'daowai', '方正': 'hebfangz', '香坊': 'xiangfang', '江北': 'hrbjiangbei', '巴彦': 'hebbayan'}, 'code': 'hrb|202'}, '蓬莱': {'sublist': {'登州街道': 'dengzhoujiedao', '其他': 'penglaishiqita', '紫荆山街道': 'zijingshanjiedao', '新港街道': 'xingangjiedao'}, 'code': 'penglai|237'}, '赤峰': {'sublist': {'松山': 'songshan', '红山': 'hshan', '元宝山': 'yuanbaoshan', '其他': 'cfqita', '翁牛特旗': 'wengniuteqi', '新城区': 'cfxinchengqu', '宁城': 'ningchengxian', '敖汉旗': 'aohanqi', '喀喇沁旗': 'keciqinqi', '林西': 'linxi'}, 'code': 'chifeng|6700'}, '滦南': {'sublist': {'城区': 'luannanxiancq', '其他': 'luannanxianqt'}, 'code': 'luannanxian|7066'}, '招远': {'sublist': {'泉山': 'zhaoyuanquanshan', '大秦家': 'daqinjia', '罗峰': 'luofeng', '梦芝': 'mengzhi', '其他': 'zhaoyuanshiqita'}, 'code': 'zhaoyuan|3325'}, '汉川': {'sublist': {}, 'code': 'hanchuan|3439'}, '肇庆': {'sublist': {'德庆': 'deqingxian', '其他': 'zhaoqing', '广宁': 'guangning', '四会': 'sihui', '鼎湖': 'dinghu', '怀集': 'huaiji', '端州': 'duanzhou', '封开': 'fengkai', '高要': 'gaoyao'}, 'code': 'zq|901'}}
    list_url = []
    flag_next = True
    while flag_next:
        try:
            jobs_url_li=[]
            try:
                time.sleep(3)
                d_pos = {"kw": compName}
                comp_name = parse.urlencode(d_pos).encode('utf-8')
                comp_name = str(comp_name).split('kw=')[1][:-1]
                city_str=dict_city[cityName]['code'].split('|')[0]
            except:
                judge=1
                flag_next = False
                traceback.print_exc()
                break
            url_zhyc_zwss ="http://search.chinahr.com/"+city_str+"/job/pn"+str(page_number)+'/?key='+comp_name
            print("zhyc----",url_zhyc_zwss)
            try:
                html_li_text=xh_pd_req(pos_url=url_zhyc_zwss,data='',headers=head_reqst())
            except:
                traceback.print_exc()
                flag_next = False
                break
            # request_zw=request.Request(url_zhyc_zwss,headers=head_reqst())
            # html_li_text = request.urlopen(request_zw).read().decode('utf-8', errors='ignore')
            # print(html_li_text)
            if "中华英才" in html_li_text:
                sel = Selector(text=html_li_text)
                if len(sel.xpath('//div[@class="job-list-box"]/div')) == 0 :
                    type_zhyc = 'old'
                    print('*************新版本未能查询到数据，进行旧版本查询*************')
                    get_zhyczw_0(compName, provName, cityName, countyName, cityName_0, channelid=6)
                    break
                else:
                    job_zhyc_li = sel.xpath('//div[@class="job-list-box"]/div')
                    for job_zhyc in job_zhyc_li:
                        job_zhyc_name = job_zhyc.xpath('string(//li[@class="job-company"])').extract()[0].strip()
                        if job_zhyc_name == compName:
                            job_zhyc_url = job_zhyc.xpath('string(@data-detail)').extract()[0].strip()
                            if 'http' not in job_zhyc_url:
                                job_zhyc_url = "http://www.chinahr.com" + job_zhyc_url
                            #print(job_zhyc_url)
                            if job_zhyc_url not in list_url:
                                list_url.append(job_zhyc_url)
                                jobs_url_li.append(job_zhyc_url)
                    try:
                        if len(sel.xpath('//div[@class="job-list-box"]/div')) < 30:
                            print('最后一页')
                            flag_next = False
                        else:
                            print("开始爬取第%s页"%page_number)
                            page_number = page_number + 1
                            if page_number > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                                print("爬取页数超过30页，强制退出")
                                flag_next = False
                    except:
                        flag_next = False
                        pass
                    #三页全部职位全部重复后结束循环
                    if jobs_url_li ==[]:
                        url_num=url_num+1
                        print('页面重复')
                        if url_num >2:
                            flag_next = False
                    else:
                        for job_url_1 in jobs_url_li[0:]:
                            time.sleep(random.uniform(0.3, 0.6))
                            try:
                                job_zhyc_text = xh_pd_req(pos_url=job_url_1, data='', headers=head_reqst())
                                # request_jx = request.Request(url=job_url_1, headers=head_reqst())
                                # job_zhyc_text = request.urlopen(request_jx, timeout=4).read().decode('utf-8', errors='ignore')
                                zw_data_zhyc = zwjx_zhyc(text=job_zhyc_text, compName=compName)
                                zw_data_zhyc['type'] = 'job'
                                zw_data_zhyc['channel'] = channelid
                                zw_data_zhyc['companyName'] = compName
                                zw_data_zhyc['province'] = provName
                                zw_data_zhyc['city'] = cityName_0
                                zw_data_zhyc['county'] = countyName
                                print("zhyc---------", zw_data_zhyc)
                                job_save_zhyc.append(zw_data_zhyc)
                            except:
                                print('解析错误，{}'.format(job_url_1))
                                traceback.print_exc()
                                logging.exception("Exception Logged")
                                pass
                            if len(job_save_zhyc) == 3:
                                total = total+3
                                data = json.dumps(job_save_zhyc)
                                data = data.encode('utf-8')
                                requests.post(url=job_save_url, data=data)
                                logging.error('zhyc_jobl----3')
                                job_save_zhyc = []
                        if len(job_save_zhyc) == 3 or len(job_save_zhyc) == 0:
                            pass
                        else:
                            total = total + len(job_save_zhyc)
                            data = json.dumps(job_save_zhyc)
                            data = data.encode('utf-8')
                            requests.post(url=job_save_url, data=data)
                            logging.error('zhyc_jobl----yfs')

            elif "" == html_li_text:
                flag_next = False

        except:
            traceback.print_exc()
            pass
    if  type_zhyc == 'new':
        if total > 0:
            scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif total == 0:
            if judge == 0:
                scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
                data = json.dumps(scrapy_state)
                data = data.encode('utf-8')
                requests.post(url=job_save_url, data=data)
            elif judge == 1:
                scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
                data = json.dumps(scrapy_state)
                data = data.encode('utf-8')
                requests.post(url=job_save_url, data=data)
        print('爬取完成')
def get_djzw(compName, provName, cityName, countyName,cityName_0, channelid=7):
    city_dajie={'石河子': '659100', '临沧': '530900', '东莞': '441900', '吐鲁番': '652100', '青岛': '370200', '蒙自': '533700', '大庆': '230600', '日照': '371100', '黄南': '632300', '揭阳': '445200', '昭通': '530600', '贵阳': '520100', '德州': '371400', '抚顺': '210400', '那曲': '542400', '岳阳': '430600', '丹东': '210600', '余姚': '331600', '鄂尔多斯': '150600', '西双版纳': '532800', '太仓': '321800', '涿州': '131400', '驻马店': '411700', '荆州': '421000', '潜江': '423000', '加格达奇': '232900', '喀什': '653100', '聊城': '371500', '江阴': '322100', '赤峰': '150400', '周口': '411600', '儋州': '460500', '娄底': '431300', '汉中': '610700', '河池': '451200', '辽源': '220400', '佛山': '440600', '苏州': '320500', '张家港': '322000', '阿里': '542500', '青州': '371800', '南海': '445700', '甘南': '623000', '新乡': '410700', '襄阳': '420600', '宜春': '360900', '巴彦淖尔': '150800', '文山': '532600', '湖州': '330500', '宜宾': '511500', '赣州': '360700', '泉州': '350500', '玉溪': '530400', '宁国': '341900', '果洛': '632600', '清远': '441800', '咸宁': '421200', '鸡西': '230300', '秦皇岛': '130300', '雅安': '511800', '昆山': '321500', '阿坝': '513200', '毕节': '522400', '本溪': '210500', '阜新': '210900', '黑河': '231100', '东营': '370500', '临夏': '622900', '枣庄': '370400', '威海': '371000', '海西': '632800', '曲靖': '530300', '海宁': '331400', '安阳': '410500', '普洱': '530800', '齐齐哈尔': '230200', '来宾': '451300', '瓦房店': '211500', '景洪': '533500', '大兴安岭': '232700', '安顺': '520400', '鄂州': '420700', '巴中': '511900', '榆林': '610800', '乌鲁木齐': '650100', '朔州': '140600', '桂林': '450300', '渭南': '610500', '常德': '430700', '衢州': '330800', '韶关': '440200', '金昌': '620300', '漯河': '411100', '三亚': '460200', '蚌埠': '340300', '朝阳': '211300', '思茅': '533600', '张家界': '430800', '无锡': '320200', '图木舒克': '659300', '迪庆': '533400', '伊春': '230700', '锦州': '210700', '阿拉尔': '659200', '东方': '469300', '井冈山': '361300', '常州': '320400', '营口': '210800', '海东': '632100', '河源': '441600', '濮阳': '410900', '菏泽': '371700', '莱芜': '371200', '南充': '511300', '锡林郭勒': '152500', '九江': '360400', '邯郸': '130400', '北京': '110000', '重庆': '500000', '运城': '140800', '乐山': '511100', '德阳': '510600', '南宁': '450100', '黔西南': '522300', '昆明': '530100', '西安': '610100', '泰安': '370900', '其他': '141300', '延安': '610600', '阳江': '441700', '马鞍山': '340500', '白城': '220800', '呼和浩特': '150100', '扬州': '321000', '衡水': '131100', '汕头': '440500', '盘锦': '211100', '克孜勒苏': '653000', '开封': '410200', '长沙': '430100', '宝鸡': '610300', '池州': '341700', '呼伦贝尔': '150700', '上饶': '361100', '嘉峪关': '620200', '崇左': '451400', '酒泉': '620900', '晋城': '140500', '淮北': '340600', '双鸭山': '230500', '惠州': '441300', '合肥': '340100', '唐山': '130200', '都匀': '522800', '泰州': '321200', '阜阳': '341200', '梅河口': '222600', '新余': '360500', '石家庄': '130100', '海城': '211600', '宿州': '341300', '恩施': '422800', '信阳': '411500', '宿迁': '321300', '南京': '320100', '金华': '330700', '莆田': '350300', '平顶山': '410400', '丽江': '530700', '新会': '445800', '龙岩': '350800', '辽阳': '211000', '淄博': '370300', '济南': '370100', '克拉玛依': '650200', '吕梁': '141100', '鹰潭': '360600', '铜仁': '522200', '舟山': '330900', '亳州': '341600', '从化': '445500', '贵港': '450800', '博尔塔拉': '652700', '潍坊': '370700', '衡阳': '430400', '泸州': '510500', '张掖': '620700', '港澳台': '800100', '柳州': '450200', '鹤岗': '230400', '鞍山': '210300', '六安': '341500', '邵阳': '430500', '凯里': '523000', '增城': '445900', '钦州': '450700', '长治': '140400', '上海': '310000', '德宏': '533100', '盐城': '320900', '梅州': '441400', '通化': '220500', '廊坊': '131000', '临汾': '141000', '三明': '350400', '中山': '442000', '玉林': '450900', '湘西': '433100', '吴江': '321900', '珠海': '440400', '琼海': '460400', '文昌': '469100', '攀枝花': '510400', '承德': '130800', '庆阳': '621000', '曲阜': '371900', '哈密': '652200', '南平': '350700', '红河': '532500', '遂宁': '510900', '潮州': '445100', '吉首': '433200', '其它': '999999', '厦门': '350200', '广州': '440100', '郴州': '431000', '忻州': '140900', '淮安': '320800', '抚州': '361000', '宜昌': '420500', '吉林市': '220200', '黔南': '522700', '临沂': '371300', '贺州': '451100', '万宁': '469200', '黄石': '420200', '百色': '451000', '葫芦岛': '211400', '肇庆': '441200', '张家口': '130700', '慈溪': '331200', '绍兴': '330600', '包头': '150200', '黔东南': '522600', '滁州': '341100', '洛阳': '410300', '怒江': '533300', '商丘': '411400', '孝感': '420900', '定西': '621100', '甘孜': '513300', '太原': '140100', '和田': '653200', '绵阳': '510700', '仙桃': '422900', '徐州': '320300', '阿拉善': '152900', '随州': '421300', '松原': '220700', '北戴河': '131300', '兰州': '620100', '黄冈': '421100', '黄山': '341000', '台州': '331000', '西宁': '630100', '保定': '130600', '天门': '423100', '遵义': '520300', '商洛': '611000', '许昌': '411000', '宣城': '341800', '吉安': '360800', '延吉': '222500', '固原': '640400', '株洲': '430200', '萧山': '331300', '牡丹江': '231000', '嘉兴': '330400', '林芝': '542600', '中卫': '640500', '海外': '810100', '兴安': '152200', '福州': '350100', '阿克苏': '652900', '昌都': '542100', '伊犁': '654000', '丽水': '331100', '乌兰察布': '150900', '烟台': '370600', '绥宁': '433300', '杭州': '330100', '溧阳': '322400', '白山': '220600', '长春': '220100', '武汉': '420100', '公主岭': '222700', '芜湖': '340200', '萍乡': '360300', '延边': '222400', '连云港': '320700', '山南': '542200', '玉树': '632700', '铜川': '610200', '塔城': '654200', '兴义': '522900', '乌海': '150300', '楚雄': '532300', '神农架': '423200', '榆次': '141200', '十堰': '420300', '防城港': '450600', '邢台': '130500', '荆门': '420800', '阳泉': '140300', '成都': '510100', '巴音郭楞': '652800', '济源': '419000', '大同': '140200', '佳木斯': '230800', '保山': '530500', '广元': '510800', '沧州': '130900', '湘潭': '430300', '咸阳': '610400', '安康': '610900', '宁波': '330200', '沈阳': '210100', '天津': '120000', '阿勒泰': '654300', '七台河': '230900', '绥化': '231200', '海南州': '632500', '北海': '450500', '石狮': '351000', '辛集': '131200', '益阳': '430900', '白银': '620400', '常熟': '321400', '内江': '511000', '安庆': '340800', '天水': '620500', '泰兴': '322300', '昌吉': '652300', '凉山': '513400', '陇南': '621200', '资阳': '512000', '景德镇': '360200', '海北': '632200', '达州': '511700', '银川': '640100', '焦作': '410800', '南阳': '411300', '哈尔滨': '230100', '济宁': '370800', '鹤壁': '410600', '眉山': '511400', '淮阴': '321600', '开平': '445600', '云浮': '445300', '镇江': '321100', '顺德': '445400', '漳州': '350600', '梧州': '450400', '铁岭': '211200', '温州': '330300', '永州': '431100', '自贡': '510300', '晋中': '140700', '平凉': '620800', '拉萨': '540100', '广安': '511600', '巢湖': '341400', '茂名': '440900', '六盘水': '520200', '通辽': '150500', '汕尾': '441500', '深圳': '440300', '湛江': '440800', '大理': '532900', '海口': '460100', '五指山': '460300', '大连': '210200', '丹阳': '322200', '南昌': '360100', '郑州': '410100', '吴忠': '640300', '五家渠': '659400', '三门峡': '411200', '日喀则': '542300', '淮南': '340400', '庐山': '361200', '武威': '620600', '南通': '320600', '滨州': '371600', '宁德': '350900', '铜陵': '340700', '江门': '440700', '怀化': '431200', '义乌': '331500', '石嘴山': '640200', '四平': '220300'}
    page_num = 1
    judge = 0
    total = 0
    job_save_dj = []
    zw_url_id = []
    flag_next = True
    panduan=0
    while flag_next:
        try:
            if panduan>10:
                flag_next = False
            try:
                d_pos = {"kw111": compName, "city": cityName}
                postname = parse.urlencode(d_pos).encode('utf-8')
                com_name = str(postname).split('kw111=')[1][:-1].split('&')[0]
                city_name = str(postname).split('city=')[1][:-1].split('&')[0]
                city_num = city_dajie[cityName]
                url_zy="https://so.dajie.com/job/search?cityId="+ city_num + "&cname=" + city_name +"&from=job&clicktype=blank"
                session = requests.Session()
            except:
                judge=1
                traceback.print_exc()
                flag_next = False
                break
            res = session.get(url=url_zy, headers=head_reqst(),proxies=proxies,allow_redirects=False)
            url_dj_zw = "http://so.dajie.com/job/ajax/search/filter?keyword="+ com_name + "&city="+ city_num +"&page="+str(page_num)
            headers_1 = {
                'accept':'application/json, text/javascript, */*; q=0.01',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'referer':url_zy,
                'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
            }

            time.sleep(random.uniform(1, 1.5))
            html_li_text=session.get(url=url_dj_zw, headers=headers_1,proxies=proxies).text
            print("djw-------",html_li_text)
            dict_li=json.loads(html_li_text)
            totalPage=dict_li["data"]["totalPage"]
            try:
                if page_num < totalPage:
                    page_num=page_num+1
                    if page_num >30:
                        flag_next = False

                elif page_num >= totalPage:
                    flag_next = False
                    pass
            except:
                traceback.print_exc()
                flag_next = False
                pass
            if dict_li["result"]== 0 :
                for dj_data_zw in dict_li["data"]["list"]:
                    if dj_data_zw['compName']== compName:
                        url_zw='http:'+dj_data_zw['jobHref']
                        time.sleep(random.uniform(0.3, 0.6))
                        try:
                            dj_zw_text = xh_pd_req(pos_url=url_zw,data='',headers=head_reqst())
                            zw_data_dj = zwjx_dj(text=dj_data_zw, compName=compName, zw_data=dj_zw_text)
                            zw_data_dj['type'] = 'job'
                            zw_data_dj['channel'] = channelid
                            zw_data_dj['companyName'] = compName
                            zw_data_dj['province'] = provName
                            zw_data_dj['city'] = cityName_0
                            zw_data_dj['county'] = countyName
                        except:
                            pass
                        print('djw-------',zw_data_dj)
                        job_save_dj.append(zw_data_dj)
                        if len(job_save_dj) == 3:
                            total = total + 3
                            data = json.dumps(job_save_dj)
                            data = data.encode('utf-8')
                            requests.post(url=job_save_url, data=data)
                            logging.error('dj_jobl----3')
                            job_save_dj = []
                if len(job_save_dj) == 3 or len(job_save_dj) == 0:
                    pass
                else:
                    total = total + len(job_save_dj)
                    data = json.dumps(job_save_dj)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('dj_jobl----yfs')
        except:
            panduan=panduan+1
            traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_zpzw(compName,provName,cityName, countyName,cityName_0, channelid=8):
    dict_city={'铜仁':'101260400','湖南':'101250000','葫芦岛':'101071400','凉山':'101272000','南充':'101270500','鹤壁':'101181200','梅州':'101280400','赣州':'101240700','黔东南':'101260700','随州':'101201100','芜湖':'101220300','通辽':'101080400','乌鲁木齐':'101130100','石嘴山':'101170200','驻马店':'101181600','丽水':'101210800','信阳':'101180600','阿勒泰':'101131500','佛山':'101280800','昆明':'101290100','福建':'101230000','安阳':'101180200','龙岩':'101230700','天津':'101030100',
               '新余':'101241000','湖北':'101200000','屯昌':'101311100','阳江':'101281800','黑龙江':'101050000','深圳':'101280600','舟山':'101211100','湖州':'101210200','鹰潭':'101241100','喀什':'101131200','黄冈':'101200500','北海':'101301300','银川':'101170100','包头':'101080200','甘孜':'101272100','沈阳':'101070100','邵阳':'101250900','大理':'101291600','兰州':'101160100','南阳':'101180700','临高':'101311300','琼海':'101310600','五家渠':'101131900','克拉玛依':'101130200','临沂':'101120900','山西':'101100000','济南':'101120100','通化':'101060400',
               '扬州':'101190600','秦皇岛':'101091100','恩施':'101201300','琼中':'101311900','绍兴':'101210500','渭南':'101110500','绵阳':'101270400',
               '泉州':'101230500','博尔塔拉':'101130500','铁门关':'101132000','阜新':'101070900','厦门':'101230200','郴州':'101250500','雅安':'101271600','吐鲁番':'101130800','双河市':'101132400','孝感':'101200400','楚雄':'101291700','重庆':'101040100','辽宁':'101070000','黄石':'101200600','莆田':'101230400','廊坊':'101090600','荆州':'101200800','三沙':'101310300',
               '无锡':'101190200','景德镇':'101240800','海北':'101150300','昆玉市':'101132300','保定':'101090200','鹤岗':'101051100','四川':'101270000','西宁':'101150100','晋中':'101100400','果洛':'101150600','河南':'101180000','铜川':'101111000','神农架':'101201700','澳门':'101330100','云浮':'101281400','黔西南':'101260900','白银':'101161000','衡阳':'101250400','福州':'101230100','佳木斯':'101050400','那曲':'101140600','陇南':'101161100','淮南':'101220400','哈密':'101130900','江西':'101240000','迪庆':'101291500','乐东':'101311600',
               '湛江':'101281000','三明':'101230800','怒江':'101291400','台州':'101210600','东营':'101121200','武汉':'101200100','池州':'101221500','抚顺':'101070400','呼和浩特':'101080100','安徽':'101220000','上海':'101020100','海口':'101310100','齐齐哈尔':'101050200','昌吉':'101130300','可克达拉市':'101132200','长沙':'101250100','南京':'101190100','毕节':'101260500','岳阳':'101251000','宁波':'101210400','营口':'101070800','眉山':'101271500','怀化':'101251200','绥化':'101050500','许昌':'101180400','临夏':'101161300','江门':'101281100','衡水':'101090800','常德':'101250600',
               '河池':'101301200','黄南':'101150400','襄阳':'101200200','资阳':'101271300','茂名':'101282000','吉安':'101240600','遵义':'101260200','周口':'101181400','宝鸡':'101110900','阜阳':'101220800','松原':'101060700','杭州':'101210100','固原':'101170400',
               '内蒙古':'101080000','延边':'101060900','潍坊':'101120600','鄂州':'101200300','唐山':'101090500','大同':'101100200','兴安盟':'101081100','三门峡':'101181700','昌都':'101140300','江苏':'101190000','宣城':'101221300','德宏':'101291300','浙江':'101210000','贺州':'101300700','西安':'101110100','鸡西':'101051000','哈尔滨':'101050100','林芝':'101140400','乐山':'101271400','青岛':'101120200','海西':'101150800','本溪':'101070500','河源':'101281200','临沧':'101290800',
               '郑州':'101180100','湘西':'101251400','张家口':'101090300','阿克苏':'101131000','铜陵':'101221200','衢州':'101211000','天水':'101160900','延安':'101110300','呼伦贝尔':'101080700','丹东':'101070600','克孜勒苏柯尔克孜':'101131100','宿迁':'101191300','朝阳':'101071200','巴彦淖尔':'101080800','河北':'101090000','攀枝花':'101270200','抚州':'101240400','阿拉善':'101081200','吉林':'101060000','镇江':'101190300','临汾':'101100700','白沙':'101311400','六盘水':'101260600','徐州':'101190800','桂林':'101300500','菏泽':'101121000',
               '嘉峪关':'101161200','永州':'101251300','邯郸':'101091000','石家庄':'101090100','普洱':'101290500','温州':'101210700','平顶山':'101180500','陵水':'101311700','南通':'101190500','钦州':'101301100','朔州':'101100900','沧州':'101090700','漯河':'101181500','聊城':'101121700','金昌':'101160600','贵阳':'101260100','湘潭':'101250200','成都':'101270100','泰安':'101120800','广西':'101300000','来宾':'101300400','昭通':'101290700','淄博':'101120300','揭阳':'101281900','仙桃':'101201400','百色':'101301000','酒泉':'101160800','枣庄':'101121400','宜昌':'101200900','庆阳':'101160400',
               '忻州':'101101000','肇庆':'101280900','台湾':'101340000','中山':'101281700','甘南':'101161400','西双版纳':'101291000','承德':'101090400','海东':'101150200','九江':'101240200','巴中':'101270900','合肥':'101220100','香港':'101320300','烟台':'101120500','曲靖':'101290200','南昌':'101240100','滁州':'101221000','韶关':'101280200','黔南':'101260800','阿里':'101140700','濮阳':'101181300','宜宾':'101271100','晋城':'101100600','玉林':'101300900','红河':'101291200','济宁':'101120700','德阳':'101271700','开封':'101180800','西藏':'101140000','丽江':'101290900','武威':'101160500','平凉':'101160300',
               '潮州':'101281500','三亚':'101310200','泰州':'101191200','邢台':'101090900','山南':'101140500','定安':'101311000',
               '宁德':'101230300','贵港':'101300800','达州':'101270600','大兴安岭':'101051300','安庆':'101220600','金华':'101210900','常州':'101191100','嘉兴':'101210300','商丘':'101181000','辽阳':'101071000','泸州':'101271000','马鞍山':'101220500','白城':'101060500','宜春':'101240500','盘锦':'101071300','珠海':'101280700','七台河':'101050900','淮北':'101221100','盐城':'101190700','锡林郭勒':'101081000','日照':'101121500','玉树':'101150700','商洛':'101110600','和田':'101131300','鞍山':'101070300','汉中':'101110800','甘肃':'101160000','淮安':'101190900','昌江':'101311500','图木舒克':'101131800','汕尾':'101282100',
               '陕西':'101110000','汕头':'101280500','北屯市':'101132100','黄山':'101221600','伊春':'101050700','威海':'101121300','榆林':'101110400','双鸭山':'101051200','青海':'101150000','广元':'101271800','玉溪':'101290400','亳州':'101220900','崇左':'101300200','乌兰察布':'101080900','宿州':'101220700','澄迈':'101311200','黑河':'101050600','潜江':'101201500','内江':'101271200','吴忠':'101170300','梧州':'101300600','乌海':'101080300','东沙群岛':'101282200','荆门':'101201200','东莞':'101281600','长春':'101060100','锦州':'101070700','张家界':'101251100','滨州':'101121100','贵州':'101260000','萍乡':'101240900',
               '日喀则':'101140200','中卫':'101170500','莱芜':'101121600','运城':'101100800','张掖':'101160700','益阳':'101250700','文昌':'101310700','铁岭':'101071100','济源':'101181800','山东':'101120000','洛阳':'101180900','大庆':'101050800','巴音郭楞':'101130400','东方':'101310900','万宁':'101310800','新乡':'101180300','安顺':'101260300','安康':'101110700','天门':'101201600','辽源':'101060600','焦作':'101181100','咸阳':'101110200','新疆':'101130000','长治':'101100500','牡丹江':'101050300','五指山':'101310500','保山':'101290300','保亭':'101311800','苏州':'101190400','株洲':'101250300','阿拉尔':'101131700',
               '宁夏':'101170000','遂宁':'101270700','拉萨':'101140100','石河子':'101131600','定西':'101160200','自贡':'101270300','鄂尔多斯':'101080600','上饶':'101240300','娄底':'101250800','塔城':'101131400','伊犁':'101130600','云南':'101290000','清远':'101281300','四平':'101060300','广东':'101280000','太原':'101100100','赤峰':'101080500','广州':'101280100','阿坝':'101271900','德州':'101120400','白山':'101060800','阳泉':'101100300','文山':'101291100','大连':'101070200','咸宁':'101200700','惠州':'101280300','南宁':'101300100','防城港':'101301400','海南':'101150500','漳州':'101230600','北京':'101010100','蚌埠':'101220200',
               '儋州':'101310400','广安':'101270800','连云港':'101191000','吕梁':'101101100','十堰':'101201000','六安':'101221400','柳州':'101300300','南平':'101230900'}
    job_save_zp=[]
    page_number = 1
    judge = 0
    total = 0
    flag_next = True
    while flag_next:
        try:
            jobs_url_li=[]
            time.sleep(1)
            d_pos = {"kw": compName}
            postname = parse.urlencode(d_pos).encode('utf-8')
            try:
                city_number=dict_city[cityName]
            except:
                judge = 1
                break
            company_encode = str(postname).split('kw=')[1][:-1]
            url_zp_zwss ="https://www.zhipin.com/c" + city_number +"/h_" + city_number +"/?query=" + company_encode +"&page=" + str(page_number)
            print("zp----",url_zp_zwss)
            try:
                html_li_text=xh_pd_req(pos_url=url_zp_zwss,data="",headers=head_reqst())
            except:
                break
            sel = Selector(text=html_li_text)
            job_zp_li = sel.xpath('//div[@id="main"]/div[@class="job-box"]/div[@class="job-list"]/ul/li')
            for job_zp in job_zp_li[0:]:
                job_zp_name = job_zp.xpath('string(descendant::div[@class="company-text"]/h3/a)').extract()[0]
                if job_zp_name == compName:
                    job_zp_url = job_zp.xpath('string(descendant::div[@class="info-primary"]/h3/a/@href)').extract()[0]
                    if 'http' not in job_zp_url:
                        job_zp_url = "https://www.zhipin.com" + job_zp_url
                    jobs_url_li.append(job_zp_url)
            if len(sel.xpath('//div[@class="job-list"]/ul/li')) < 30:
                flag_next = False
            else:
                page_number = page_number + 1
                if page_number > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                    flag_next = False
            for job_url_1 in jobs_url_li[0:]:
                try:
                    time.sleep(random.uniform(0.3, 0.6))
                    job_zp_text =xh_pd_req(pos_url=job_url_1, data="", headers=head_reqst())
                    zw_data_zp=zwjx_zp(text=job_zp_text,compName=compName)
                    zw_data_zp['type'] = 'job'
                    zw_data_zp['channel'] = channelid
                    zw_data_zp['companyName'] = compName
                    zw_data_zp['province'] = provName
                    zw_data_zp['city'] = cityName_0
                    zw_data_zp['county'] = countyName
                    job_save_zp.append(zw_data_zp)
                    print("zp---------", zw_data_zp)
                except:
                    traceback.print_exc()
                    pass
                if len(job_save_zp) == 3:
                    total = total + 3
                    data = json.dumps(job_save_zp)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('zp_jobl----3')
                    job_save_zp = []
            if len(job_save_zp) == 3 or len(job_save_zp) == 0:
                pass
            else:
                total = total + len(job_save_zp)
                data = json.dumps(job_save_zp)
                data = data.encode('utf-8')
                requests.post(url=job_save_url, data=data)
                logging.error('zp_jobl----yfs')
        except:
            logging.exception("Exception Logged")
            traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print("爬取完成")
def get_ntzw(compName,provName,cityName, countyName,cityName_0, channelid=9):
    page_number = 1
    job_save_nt = []
    judge = 0
    total = 0
    flag_next = True
    while flag_next:
        try:
            jobs_url_li=[]
            time.sleep(1)
            url_nt = "http://www.neitui.me/?name=job&handle=lists&"
            print("nt----", url_nt)
            pageNo = str(page_number)
            fam_data = {
                "page": pageNo,
                "city": cityName,
                "keyword": compName
            }
            try:
                html_li_text=xh_pd_req(pos_url=url_nt,data=fam_data,headers=head_reqst())
            except:
                flag_next = False
                break
            if "内推网" in html_li_text:
                sel = Selector(text=html_li_text)
                job_nt_li = sel.xpath('//ul[@class="list-items"]/li')
                for job_nt in job_nt_li[0:]:
                    job_nt_name = job_nt.xpath('string(div//span/a/@title)').extract()[0]
                    # print(job_nt_name)
                    if job_nt_name == compName:
                        job_nt_id = job_nt.xpath('string(div//a[@class="font16 max300"]/@href)').extract()[0]
                        job_nt_url = "http://www.neitui.me" + job_nt_id
                        jobs_url_li.append(job_nt_url)
                # 判断是否进入下一页
                try:
                    if len(sel.xpath('//ul[@class="list-items"]/li')) < 18:
                        flag_next = False
                    else:
                        # print("开始爬取第%s页"%page_number)
                        page_number = page_number + 1
                        if page_number > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                            # print("爬取页数超过30页，强制退出")
                            flag_next = False
                except:
                    traceback.print_exc()
                    logging.exception("Exception Logged")
                    flag_next = False
                    pass
                for job_url_1 in jobs_url_li[0:]:
                    # print(job_url_1)
                    time.sleep(random.uniform(0.3, 0.6))
                    try:
                        # request_jx = request.Request((job_url_1), headers=head_reqst())
                        # job_nt_text = request.urlopen(request_jx,timeout=4).read().decode('utf-8', errors='ignore')
                        job_nt_text = xh_pd_req(pos_url=job_url_1, data='', headers=head_reqst())
                        zw_data_nt = zwjx_nt(text=job_nt_text, compName=compName)
                        zw_data_nt['type'] = 'job'
                        zw_data_nt['channel'] = channelid
                        zw_data_nt['companyName'] = compName
                        zw_data_nt['province'] = provName
                        zw_data_nt['city'] = cityName_0
                        zw_data_nt['county'] = countyName
                        print("nt---------", zw_data_nt)
                        job_save_nt.append(zw_data_nt)
                    except:
                        traceback.print_exc()
                        logging.exception("Exception Logged")
                        pass
                    if len(job_save_nt) == 3:
                        total = total + 3
                        data = json.dumps(job_save_nt)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('nt_jobl----3')
                        job_save_nt = []
                if len(job_save_nt) == 3 or len(job_save_nt) == 0:
                    pass
                else:
                    total = total + len(job_save_nt)
                    data = json.dumps(job_save_nt)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('nt_jobl----yfs')
            elif "" == html_li_text:
                flag_next = False

        except:
            logging.exception("Exception Logged")
            # traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2, 'total': total, 'type': 'job', 'channel': channelid, 'companyName': compName,
                         'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total, 'message': '未能查询到数据', 'type': 'job', 'channel': channelid,
                             'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [
                {'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type': 'job', 'channel': channelid,
                 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)

    print('爬取完成')
def get_lpzw(compName, provName, cityName, countyName,cityName_0, channelid=10):
    cityList_dic = {'邢台': {'code': '140100', 'sublist': {}}, '三明': {'code': '090070', 'sublist': {}}, '盐城': {'code': '060150', 'sublist': {}}, '开平': {'code': '050240', 'sublist': {}}, '攀枝花': {'code': '280090', 'sublist': {}}, '福安': {'code': '090120', 'sublist': {}}, '运城': {'code': '260050', 'sublist': {}}, '延边': {'code': '190110', 'sublist': {}}, '百色': {'code': '110110', 'sublist': {}}, '河源': {'code': '050210', 'sublist': {}}, '儋州': {'code': '130090', 'sublist': {}}, '黔西南': {'code': '120080', 'sublist': {}}, '绵阳': {'code': '280050', 'sublist': {}}, '宜兴': {'code': '060230', 'sublist': {}}, '益阳': {'code': '180070', 'sublist': {}}, '平凉': {'code': '100120', 'sublist': {}}, '果洛': {'code': '240080', 'sublist': {}}, '四平': {'code': '190040', 'sublist': {}}, '内江': {'code': '280060', 'sublist': {}}, '荆门': {'code': '170070', 'sublist': {}}, '肇庆': {'code': '050120', 'sublist': {}}, '菏泽': {'code': '250170', 'sublist': {}}, '永州': {'code': '180130', 'sublist': {}}, '临夏': {'code': '100140', 'sublist': {}}, '三门峡': {'code': '150130', 'sublist': {}}, '遵义': {'code': '120030', 'sublist': {}}, '武汉': {'code': '170020', 'sublist': {'汉南区': '170020130', '新洲区': '170020110', '汉阳区': '170020040', '武昌区': '170020050', '江夏区': '170020090', '黄陂区': '170020100', '江岸区': '170020010', '江汉区': '170020020', '蔡甸区': '170020080', '硚口区': '170020030', '开发区': '170020140', '青山区': '170020060', '东西湖': '170020120', '洪山区': '170020070'}}, '如皋': {'code': '060260', 'sublist': {}}, '丽江': {'code': '310040', 'sublist': {}}, '古巴': {'code': '360140', 'sublist': {}}, '桐乡': {'code': '070240', 'sublist': {}}, '抚州': {'code': '200080', 'sublist': {}}, '毕节': {'code': '120060', 'sublist': {}}, '潍坊': {'code': '250110', 'sublist': {}}, '文昌': {'code': '130060', 'sublist': {}}, '广州': {'code': '050020', 'sublist': {'天河区': '050020020', '萝岗区': '050020090', '花都区': '050020080', '海珠区': '050020040', '白云区': '050020010', '增城区': '050020120', '番禺区': '050020070', '南沙区': '050020100', '从化区': '050020110', '荔湾区': '050020060', '黄埔区': '050020050', '越秀区': '050020030'}}, '榆林': {'code': '270110', 'sublist': {}}, '潜江': {'code': '170060', 'sublist': {}}, '绥芬河': {'code': '160180', 'sublist': {}}, '西平': {'code': '150200', 'sublist': {}}, '靖江': {'code': '060240', 'sublist': {}}, '香港': {'code': '320', 'sublist': {'中西区': '320010170', '沙田区': '320010010', '湾仔区': '320010120', '荃湾区': '320010160', '屯门区': '320010060', '深水埗': '320010090', '九龙城': '320010050', '油尖旺': '320010130', '北区': '320010140', '观塘区': '320010030', '南区': '320010150', '西贡区': '320010100', '大埔区': '320010110', '离岛区': '320010180', '葵青区': '320010070', '元朗区': '320010080', '黄大仙': '320010040', '东区': '320010020'}}, '太原': {'code': '260020', 'sublist': {'杏花岭': '260020010', '尖草坪': '260020040', '清徐县': '260020100', '万柏林': '260020050', '娄烦县': '260020120', '工业园': '260020090', '古交市': '260020130', '晋源区': '260020060', '迎泽区': '260020030', '开发区': '260020080', '小店区': '260020020', '阳曲县': '260020110', '高新区': '260020070'}}, '美国': {'code': '360030', 'sublist': {'北达科他州': '420340', '田纳西州': '420410', '堪萨斯州': '420160', '纽约州': '420320', '罗得岛州': '420470', '明尼苏达州': '420230', '阿肯色州': '420040', '内华达州': '420280', '康涅狄格州': '420070', '伊利诺伊州': '420130', '爱达荷州': '420120', '夏威夷州': '420110', '密西西比州': '420240', '西佛吉尼亚州': '420480', '印第安那州': '420140', '俄亥俄州': '420350', '新罕布什尔州': '420290', '北卡罗莱纳州': '420330', '科罗拉多州': '420060', '肯塔基州': '420170', '宾夕法尼亚州': '420380', '路易斯安那州': '420180', '佛罗里达州': '420090', '爱荷华州': '420150', '俄勒冈州': '420370', '乔治亚州': '420100', '华盛顿州': '420460', '麻萨诸塞州': '420210', '犹他州': '420430', '怀俄明州': '420500', '马里兰州': '420200', '俄克拉何马州': '420360', '特拉华州': '420080', '亚拉巴马州': '420010', '威斯康星州': '420490', '加利福尼亚州': '420050', '佛蒙特州': '420440', '缅因州': '420190', '蒙大拿州': '420260', '密苏里州': '420250', '南达科他州': '420400', '南卡罗来纳州': '420390', '弗吉尼亚州': '420450', '新泽西州': '420300', '内布拉斯加州': '420270', '德克萨斯州': '420420', '密歇根州': '420220', '新墨西哥州': '420310', '阿拉斯加州': '420020', '亚利桑那州': '420030', '华盛顿哥伦比亚特区': '420510'}}, '宿迁': {'code': '060170', 'sublist': {}}, '加拿大': {'code': '360020', 'sublist': {'曼尼托巴省': '430030', '纽芬兰与拉布拉多省': '430040', '育空地区': '430130', '新不伦瑞克省': '430050', '萨斯喀彻温省': '430100', '西北地区': '430120', '安大略省': '430070', '努纳武特地区': '430110', '新斯科舍省': '430060', '爱德华王子岛省': '430080', '魁北克省': '430090', '不列颠哥伦比亚省': '430020', '阿尔伯塔省': '430010'}}, '崇左': {'code': '110080', 'sublist': {}}, '连云港': {'code': '060060', 'sublist': {}}, '丽水': {'code': '070110', 'sublist': {}}, '乐清': {'code': '070220', 'sublist': {}}, '惠州': {'code': '050060', 'sublist': {}}, '琼海': {'code': '130070', 'sublist': {}}, '昌图': {'code': '210180', 'sublist': {}}, '云浮': {'code': '050230', 'sublist': {}}, '芜湖': {'code': '080050', 'sublist': {}}, '温州': {'code': '070040', 'sublist': {'苍南县': '070040090', '平阳县': '070040080', '龙湾区': '070040020', '永嘉县': '070040070', '乐清市': '070040050', '鹿城区': '070040010', '文成县': '070040100', '泰顺县': '070040110', '瑞安市': '070040040', '洞头县': '070040060', '瓯海区': '070040030'}}, '兖州': {'code': '250250', 'sublist': {}}, '酒泉': {'code': '100040', 'sublist': {}}, '义乌': {'code': '070130', 'sublist': {}}, '延吉': {'code': '190100', 'sublist': {}}, '滁州': {'code': '080110', 'sublist': {}}, '金昌': {'code': '100050', 'sublist': {}}, '仙桃': {'code': '170150', 'sublist': {}}, '满洲里': {'code': '220150', 'sublist': {}}, '南美洲': {'code': '370', 'sublist': {'哥伦比亚': '370020', '法属圭亚那': '370050', '智利': '370110', '秘鲁': '370080', '乌拉圭': '370130', '巴拉圭': '370140', '委内瑞拉': '370030', '巴西': '370100', '厄瓜多尔': '370070', '阿根廷': '370120', '圭亚那': '370040', '玻利维亚': '370090', '苏里南': '370060'}}, '泉港区': {'code': '090110', 'sublist': {}}, '临沧': {'code': '310100', 'sublist': {}}, '新余': {'code': '200110', 'sublist': {}}, '阜新': {'code': '210110', 'sublist': {}}, '锦州': {'code': '210090', 'sublist': {}}, '永康': {'code': '070170', 'sublist': {}}, '平顶山': {'code': '150070', 'sublist': {}}, '简阳': {'code': '280250', 'sublist': {}}, '白银': {'code': '100060', 'sublist': {}}, '晋江': {'code': '090130', 'sublist': {}}, '瑞安': {'code': '070250', 'sublist': {}}, '焦作': {'code': '150090', 'sublist': {}}, '衢州': {'code': '070100', 'sublist': {}}, '十堰': {'code': '170030', 'sublist': {}}, '昌江': {'code': '130190', 'sublist': {}}, '阿勒泰': {'code': '300130', 'sublist': {}}, '琼中': {'code': '130160', 'sublist': {}}, '韶关': {'code': '050170', 'sublist': {}}, '上海': {'code': '020', 'sublist': {'普陀区': '020010040', '虹口区': '020010060', '徐汇区': '020010020', '宝山区': '020010110', '青浦区': '020010160', '黄浦区': '020010080', '奉贤区': '020010180', '浦东新区': '020010010', '松江区': '020010150', '金山区': '020010140', '长宁区': '020010030', '闸北区': '020010050', '闵行区': '020010120', '静安区': '020010100', '杨浦区': '020010070', '嘉定区': '020010130', '崇明县': '020010190'}}, '德州': {'code': '250030', 'sublist': {}}, '贺州': {'code': '110130', 'sublist': {}}, '开曼群岛': {'code': '360360', 'sublist': {}}, '昌都': {'code': '290060', 'sublist': {}}, '安阳': {'code': '150060', 'sublist': {}}, '山南': {'code': '290050', 'sublist': {}}, '上虞': {'code': '070270', 'sublist': {}}, '德阳': {'code': '280100', 'sublist': {}}, '荣成': {'code': '250190', 'sublist': {}}, '双城': {'code': '160160', 'sublist': {}}, '巴哈马': {'code': '360130', 'sublist': {}}, '忻州': {'code': '260110', 'sublist': {}}, '常熟': {'code': '060030', 'sublist': {}}, '凉山': {'code': '280230', 'sublist': {}}, '固安': {'code': '140140', 'sublist': {}}, '永嘉': {'code': '070230', 'sublist': {}}, '佛山': {'code': '050050', 'sublist': {'禅城区': '050050010', '顺德区': '050050030', '三水区': '050050040', '南庄': '050050100', '新城区': '050050060', '黄岐': '050050080', '西樵': '050050090', '南海区': '050050020', '大沥': '050050070', '高明区': '050050050'}}, '汉中': {'code': '270070', 'sublist': {}}, '日喀则': {'code': '290030', 'sublist': {}}, '多米尼克': {'code': '360200', 'sublist': {}}, '鄂尔多斯': {'code': '220050', 'sublist': {}}, '张掖': {'code': '100080', 'sublist': {}}, '林芝': {'code': '290040', 'sublist': {}}, '濮阳': {'code': '150100', 'sublist': {}}, '蚌埠': {'code': '080040', 'sublist': {}}, '德宏': {'code': '310140', 'sublist': {}}, '五指山': {'code': '130110', 'sublist': {}}, '马鞍山': {'code': '080070', 'sublist': {}}, '昌吉': {'code': '300120', 'sublist': {}}, '黔东南': {'code': '120090', 'sublist': {}}, '海北': {'code': '240050', 'sublist': {}}, '保山': {'code': '310070', 'sublist': {}}, '廊坊': {'code': '140060', 'sublist': {}}, '泸州': {'code': '280040', 'sublist': {}}, '胶州': {'code': '250270', 'sublist': {}}, '方家山': {'code': '070330', 'sublist': {}}, '黄南': {'code': '240060', 'sublist': {}}, '商丘': {'code': '150050', 'sublist': {}}, '龙岩': {'code': '090090', 'sublist': {}}, '北海': {'code': '110030', 'sublist': {}}, '海东': {'code': '240030', 'sublist': {}}, '文山': {'code': '310120', 'sublist': {}}, '广德': {'code': '080200', 'sublist': {}}, '朔州': {'code': '260090', 'sublist': {}}, '茂名': {'code': '050180', 'sublist': {}}, '兴平': {'code': '270130', 'sublist': {}}, '大庆': {'code': '160030', 'sublist': {}}, '金华': {'code': '070060', 'sublist': {}}, '公安': {'code': '170190', 'sublist': {}}, '伊犁': {'code': '300050', 'sublist': {}}, '南京': {'code': '060020', 'sublist': {'高淳县': '060020130', '大厂区': '060020140', '白下区': '060020020', '建邺区': '060020040', '六合区': '060020080', '雨花台': '060020100', '江宁区': '060020110', '玄武区': '060020010', '下关区': '060020060', '鼓楼区': '060020050', '浦口区': '060020070', '栖霞区': '060020090', '秦淮区': '060020030', '溧水县': '060020120'}}, '烟台': {'code': '250120', 'sublist': {}}, '黄岛': {'code': '250200', 'sublist': {}}, '龙川': {'code': '050280', 'sublist': {}}, '上饶': {'code': '200070', 'sublist': {}}, '六安': {'code': '080140', 'sublist': {}}, '伯利兹': {'code': '360070', 'sublist': {}}, '郴州': {'code': '180080', 'sublist': {}}, '济源': {'code': '150190', 'sublist': {}}, '营口': {'code': '210100', 'sublist': {}}, '晋中': {'code': '260100', 'sublist': {}}, '铜陵': {'code': '080090', 'sublist': {}}, '淮北': {'code': '080080', 'sublist': {}}, '龙泉': {'code': '070340', 'sublist': {}}, '金湖': {'code': '060320', 'sublist': {}}, '双鸭山': {'code': '160090', 'sublist': {}}, '铜川': {'code': '270050', 'sublist': {}}, '海南': {'code': '240070', 'sublist': {}}, '巴巴多斯': {'code': '360240', 'sublist': {}}, '广元': {'code': '280110', 'sublist': {}}, '咸阳': {'code': '270040', 'sublist': {}}, '陵水': {'code': '130210', 'sublist': {}}, '鹰潭': {'code': '200120', 'sublist': {}}, '临高': {'code': '130150', 'sublist': {}}, '徐州': {'code': '060110', 'sublist': {}}, '阜阳': {'code': '080120', 'sublist': {}}, '齐齐哈尔': {'code': '160060', 'sublist': {}}, '公主岭': {'code': '190120', 'sublist': {}}, '淮安': {'code': '060140', 'sublist': {}}, '清远': {'code': '050070', 'sublist': {}}, '台山': {'code': '050250', 'sublist': {}}, '三门': {'code': '070300', 'sublist': {}}, '玉环县': {'code': '070150', 'sublist': {}}, '武穴': {'code': '170200', 'sublist': {}}, '江阴': {'code': '060190', 'sublist': {}}, '海口': {'code': '130020', 'sublist': {'儋州市': '130020080', '万宁市': '130020060', '昌江县': '130020110', '临高县': '130020130', '屯昌县': '130020090', '东方市': '130020100', '琼海市': '130020140', '府城': '130020150', '龙华区': '130020020', '美兰区': '130020040', '乐东黎': '130020120', '秀英区': '130020010', '澄迈县': '130020050', '琼山区': '130020030', '文昌市': '130020070'}}, '邵阳': {'code': '180100', 'sublist': {}}, '克州': {'code': '300170', 'sublist': {}}, '余姚': {'code': '070200', 'sublist': {}}, '莆田': {'code': '090060', 'sublist': {}}, '玉树': {'code': '240090', 'sublist': {}}, '大连': {'code': '210040', 'sublist': {'中山区': '210040020', '瓦房店': '210040070', '新区': '210040130', '普兰店': '210040080', '长海县': '210040120', '甘井子': '210040040', '开发区': '210040140', '普湾区': '210040100', '旅顺口': '210040050', '西岗区': '210040010', '庄河市': '210040090', '沙河口': '210040030', '金州区': '210040060'}}, '白沙': {'code': '130180', 'sublist': {}}, '鄂州': {'code': '170100', 'sublist': {}}, '乐山': {'code': '280030', 'sublist': {}}, '常德': {'code': '180050', 'sublist': {}}, '塔城': {'code': '300150', 'sublist': {}}, '延安': {'code': '270100', 'sublist': {}}, '拉萨': {'code': '290020', 'sublist': {'林周县': '290020020', '工卡县': '290020080', '曲水县': '290020050', '当雄县': '290020030', '龙德庆': '290020060', '达孜县': '290020070', '尼木县': '290020040', '城关区': '290020010'}}, '泉州': {'code': '090030', 'sublist': {}}, '哈密': {'code': '300070', 'sublist': {}}, '黑河': {'code': '160120', 'sublist': {}}, '珠海': {'code': '050140', 'sublist': {'香洲区': '050140010', '横琴新区': '050140040', '金湾区': '050140030', '斗门区': '050140020'}}, '哈尔滨': {'code': '160020', 'sublist': {'动力区': '160020030', '道外区': '160020070', '木兰县': '160020190', '平房区': '160020040', '依兰县': '160020160', '香坊区': '160020050', '延寿县': '160020200', '道里区': '160020010', '通河县': '160020180', '南岗区': '160020020', '宾县': '160020150', '巴彦县': '160020170', '呼兰区': '160020090', '松北区': '160020100', '太平区': '160020060', '方正县': '160020140', '五常市': '160020130', '阿城市': '160020080', '尚志市': '160020110', '双城市': '160020120'}}, '安达': {'code': '160150', 'sublist': {}}, '潮州': {'code': '050030', 'sublist': {}}, '来宾': {'code': '110090', 'sublist': {}}, '杭州': {'code': '070020', 'sublist': {'上城区': '070020010', '余杭区': '070020080', '下城区': '070020020', '市郊': '070020140', '富阳区': '070020100', '桐庐县': '070020120', '西湖区': '070020040', '萧山区': '070020070', '滨江区': '070020060', '淳安县': '070020130', '临安市': '070020090', '拱墅区': '070020030', '建德市': '070020110', '江干区': '070020050'}}, '南充': {'code': '280130', 'sublist': {}}, '肥城': {'code': '250240', 'sublist': {}}, '嘉峪关': {'code': '100030', 'sublist': {}}, '江门': {'code': '050150', 'sublist': {}}, '博尔塔拉': {'code': '300190', 'sublist': {}}, '沈阳': {'code': '210020', 'sublist': {'法库县': '210020140', '新民市': '210020110', '苏家屯': '210020060', '铁西区': '210020050', '皇姑区': '210020020', '东陵区': '210020070', '浑南区': '210020100', '沈河区': '210020010', '大东区': '210020040', '沈北区': '210020080', '康平县': '210020130', '辽中县': '210020120', '和平区': '210020030', '于洪区': '210020090'}}, '启东': {'code': '060290', 'sublist': {}}, '河池': {'code': '110140', 'sublist': {}}, '宣城': {'code': '080170', 'sublist': {}}, '五家渠': {'code': '300100', 'sublist': {}}, '曲靖': {'code': '310060', 'sublist': {}}, '凤阳': {'code': '080190', 'sublist': {}}, '葫芦岛': {'code': '210050', 'sublist': {}}, '池州': {'code': '080160', 'sublist': {}}, '石河子': {'code': '300080', 'sublist': {}}, '普宁': {'code': '050260', 'sublist': {}}, '安庆': {'code': '080030', 'sublist': {}}, '牙买加': {'code': '360150', 'sublist': {}}, '贵港': {'code': '110150', 'sublist': {}}, '乐东': {'code': '130200', 'sublist': {}}, '湖州': {'code': '070080', 'sublist': {}}, '顺德': {'code': '050100', 'sublist': {}}, '合肥': {'code': '080020', 'sublist': {'新站区': '080020080', '瑶海区': '080020020', '包河区': '080020040', '肥西县': '080020070', '经开区': '080020090', '政务区': '080020130', '蜀山区': '080020030', '长丰县': '080020050', '滨湖区': '080020110', '肥东县': '080020060', '庐阳区': '080020010', '北城区': '080020120', '高新区': '080020100'}}, '兴安盟': {'code': '220110', 'sublist': {}}, '岳阳': {'code': '180090', 'sublist': {}}, '盘锦': {'code': '210130', 'sublist': {}}, '黄冈': {'code': '170110', 'sublist': {}}, '呼和浩特': {'code': '220020', 'sublist': {'武川县': '220020090', '新城区': '220020030', '土左旗': '220020060', '格尔县': '220020080', '清水河': '220020050', '赛罕区': '220020040', '回民区': '220020010', '托克托': '220020070', '玉泉区': '220020020'}}, '遵化': {'code': '140150', 'sublist': {}}, '周口': {'code': '150150', 'sublist': {}}, '峨眉': {'code': '280240', 'sublist': {}}, '昭通': {'code': '310080', 'sublist': {}}, '特克斯': {'code': '360350', 'sublist': {}}, '波多黎各': {'code': '360260', 'sublist': {}}, '盱眙': {'code': '060300', 'sublist': {}}, '东阳': {'code': '070180', 'sublist': {}}, '遂宁': {'code': '280120', 'sublist': {}}, '蒙特塞拉特': {'code': '360300', 'sublist': {}}, '株洲': {'code': '180040', 'sublist': {}}, '泰州': {'code': '060160', 'sublist': {}}, '平湖': {'code': '070160', 'sublist': {}}, '娄底': {'code': '180120', 'sublist': {}}, '乌审旗': {'code': '220140', 'sublist': {}}, '沧州': {'code': '140110', 'sublist': {}}, '乌苏': {'code': '300210', 'sublist': {}}, '白山': {'code': '190070', 'sublist': {}}, '楚雄': {'code': '310150', 'sublist': {}}, '南沙': {'code': '050270', 'sublist': {}}, '慈溪': {'code': '070210', 'sublist': {}}, '和田': {'code': '300160', 'sublist': {}}, '乌海': {'code': '220060', 'sublist': {}}, '圣文森特': {'code': '360220', 'sublist': {}}, '非洲': {'code': '400', 'sublist': {'塞舌尔': '400190', '几内亚比绍': '400340', '乌干达': '400160', '布基纳法索': '400320', '贝宁': '400410', '刚果': '400250', '博茨瓦纳': '400490', '冈比亚': '400300', '科摩罗': '400550', '阿尔及利亚': '400060', '毛里求斯': '400560', '加那利群岛': '400430', '塞内加尔': '400290', '多哥': '400400', '乍得': '400200', '毛里塔尼亚': '400270', '留尼旺': '400570', '尼日尔': '400420', '喀麦隆': '400220', '赤道几内亚': '400230', '纳米比亚': '400500', '南非': '400510', '马达加斯加': '400540', '尼日利亚': '400590', '埃及': '400020', '突尼斯': '400050', '利比里亚': '400370', '几内亚': '400330', '厄立特里亚': '400110', '马拉维': '400470', '加纳': '400390', '埃塞俄比亚': '400100', '加蓬': '400240', '苏丹': '400040', '布隆迪': '400180', '莫桑比克': '400480', '索马里': '400120', '肯尼亚': '400140', '中非': '400210', '马里': '400310', '斯威士兰': '400520', '佛得角': '400350', '西撒哈拉': '400280', '亚速尔群岛': '400080', '马德拉群岛': '400090', '科特迪瓦': '400380', '利比亚': '400030', '安哥拉': '400450', '莱索托': '400530', '坦桑尼亚': '400150', '摩洛哥': '400070', '圣赫勒拿': '400580', '圣普': '400260', '赞比亚': '400440', '吉布提': '400130', '津巴布韦': '400460', '卢旺达': '400170', '塞拉利昂': '400360'}}, '三亚': {'code': '130030', 'sublist': {}}, '保定': {'code': '140030', 'sublist': {}}, '通辽': {'code': '220070', 'sublist': {}}, '铜仁': {'code': '120070', 'sublist': {}}, '诸暨': {'code': '070280', 'sublist': {}}, '南阳': {'code': '150170', 'sublist': {}}, '安的列斯': {'code': '360330', 'sublist': {}}, '中山': {'code': '050130', 'sublist': {}}, '中卫': {'code': '230060', 'sublist': {}}, '阳江': {'code': '050160', 'sublist': {}}, '孝感': {'code': '170120', 'sublist': {}}, '莱西': {'code': '250300', 'sublist': {}}, '三河': {'code': '140170', 'sublist': {}}, '兰州': {'code': '100020', 'sublist': {'七里河': '100020030', '西固区': '100020040', '安宁区': '100020050', '永登县': '100020070', '红古区': '100020060', '皋兰县': '100020010', '榆中县': '100020080', '城关区': '100020020'}}, '太仓': {'code': '060090', 'sublist': {}}, '和顺': {'code': '260140', 'sublist': {}}, '洪都拉斯': {'code': '360090', 'sublist': {}}, '南宁': {'code': '110020', 'sublist': {'马山县': '110020090', '邕宁区': '110020010', '上林县': '110020100', '江南区': '110020060', '隆安县': '110020080', '武鸣县': '110020070', '兴宁区': '110020030', '宾阳县': '110020110', '横县': '110020120', '青秀区': '110020020', '西乡塘': '110020050', '良庆区': '110020040'}}, '襄阳': {'code': '170040', 'sublist': {}}, '梧州': {'code': '110070', 'sublist': {}}, '定安': {'code': '130120', 'sublist': {}}, '漯河': {'code': '150120', 'sublist': {}}, '宁海': {'code': '070290', 'sublist': {}}, '海宁': {'code': '070140', 'sublist': {}}, '吐鲁番': {'code': '300140', 'sublist': {}}, '阿拉尔': {'code': '300090', 'sublist': {}}, '安圭拉': {'code': '360290', 'sublist': {}}, '咸宁': {'code': '170130', 'sublist': {}}, '许昌': {'code': '150110', 'sublist': {}}, '亳州': {'code': '080150', 'sublist': {}}, '格林纳达': {'code': '360230', 'sublist': {}}, '阿拉善盟': {'code': '220130', 'sublist': {}}, '宿松': {'code': '080210', 'sublist': {}}, '开原': {'code': '210190', 'sublist': {}}, '宜城': {'code': '170210', 'sublist': {}}, '固原': {'code': '230050', 'sublist': {}}, '昆明': {'code': '310020', 'sublist': {'东川区': '310020050', '宜良区': '310020100', '五华区': '310020020', '呈贡新': '310020070', '嵩明区': '310020110', '寻甸': '310020140', '富民区': '310020090', '盘龙区': '310020010', '禄劝': '310020130', '官渡区': '310020030', '西山区': '310020040', '安宁市': '310020060', '石林县': '310020120', '晋宁新': '310020080'}}, '汕头': {'code': '050080', 'sublist': {}}, '泰兴': {'code': '060220', 'sublist': {}}, '瓜德罗普': {'code': '360310', 'sublist': {}}, '扬州': {'code': '060120', 'sublist': {}}, '银川': {'code': '230020', 'sublist': {'灵武市': '230020040', '永宁县': '230020050', '贺兰县': '230020060', '青铜峡': '230020100', '西夏区': '230020010', '金凤区': '230020020', '兴庆区': '230020030'}}, '平度': {'code': '250290', 'sublist': {}}, '那曲': {'code': '290070', 'sublist': {}}, '喀什': {'code': '300030', 'sublist': {}}, '鸡西': {'code': '160070', 'sublist': {}}, '赣州': {'code': '200040', 'sublist': {}}, '揭阳': {'code': '050220', 'sublist': {}}, '安康': {'code': '270080', 'sublist': {}}, '鹤山': {'code': '050290', 'sublist': {}}, '海西': {'code': '240040', 'sublist': {}}, '荆州': {'code': '170080', 'sublist': {}}, '通州': {'code': '060310', 'sublist': {}}, '西昌': {'code': '280200', 'sublist': {}}, '燕郊': {'code': '140130', 'sublist': {}}, '长沙': {'code': '180020', 'sublist': {'宁乡县': '180020100', '岳麓区': '180020010', '雨花区': '180020050', '芙蓉区': '180020020', '天心区': '180020030', '开发区': '180020060', '长沙县': '180020080', '望城区': '180020090', '浏阳市': '180020070', '开福区': '180020040'}}, '萨尔瓦多': {'code': '360080', 'sublist': {}}, '本溪': {'code': '210070', 'sublist': {}}, '白城': {'code': '190090', 'sublist': {}}, '常州': {'code': '060040', 'sublist': {'新北区': '060040050', '金坛市': '060040080', '武进区': '060040060', '戚墅堰': '060040030', '郊区': '060040040', '天宁区': '060040010', '溧阳市': '060040070', '钟楼区': '060040020'}}, '达州': {'code': '280160', 'sublist': {}}, '天津': {'code': '030', 'sublist': {'河西区': '030010030', '南开区': '030010040', '津南区': '030010120', '红桥区': '030010060', '汉沽区': '030010080', '武清区': '030010140', '滨海区': '030010210', '塘沽区': '030010070', '西青区': '030010110', '河东区': '030010020', '静海县': '030010170', '宁河县': '030010160', '蓟\u3000县': '030010180', '大港区': '030010090', '东丽区': '030010100', '北辰区': '030010130', '和平区': '030010010', '宝坻区': '030010150', '开发区': '030010200', '河北区': '030010050'}}, '铁岭': {'code': '210140', 'sublist': {}}, '宜宾': {'code': '280070', 'sublist': {}}, '嘉兴': {'code': '070090', 'sublist': {}}, '庆阳': {'code': '100130', 'sublist': {}}, '厦门': {'code': '090040', 'sublist': {'海沧区': '090040020', '集美区': '090040040', '同安区': '090040050', '翔安区': '090040060', '思明区': '090040010', '湖里区': '090040030'}}, '肇东': {'code': '160190', 'sublist': {}}, '绍兴': {'code': '070050', 'sublist': {}}, '阿坝': {'code': '280220', 'sublist': {}}, '万宁': {'code': '130080', 'sublist': {}}, '嘉善': {'code': '070190', 'sublist': {}}, '石家庄': {'code': '140020', 'sublist': {'元氏县': '140020230', '裕华区': '140020050', '井陉县': '140020130', '桥东区': '140020020', '长安区': '140020010', '晋州市': '140020100', '井陉矿': '140020060', '平山县': '140020220', '赵县': '140020240', '桥西区': '140020030', '高邑县': '140020180', '正定县': '140020140', '灵寿县': '140020170', '鹿泉市': '140020120', '深泽县': '140020190', '高新区': '140020070', '栾城县': '140020150', '行唐县': '140020160', '无极县': '140020210', '新华区': '140020040', '辛集市': '140020080', '新乐市': '140020110', '藁城市': '140020090', '赞皇县': '140020200'}}, '大兴安岭': {'code': '160140', 'sublist': {}}, '湛江': {'code': '050110', 'sublist': {}}, '马提尼克': {'code': '360320', 'sublist': {}}, '西双版纳': {'code': '310130', 'sublist': {}}, '多米尼加': {'code': '360170', 'sublist': {}}, '资阳': {'code': '280190', 'sublist': {}}, '尚志': {'code': '160170', 'sublist': {}}, '特立尼达': {'code': '360250', 'sublist': {}}, '亚洲': {'code': '350', 'sublist': {'印度尼西亚': '350150', '印度': '350200', '塞浦路斯': '350480', '乌兹别克': '350270', '阿塞拜疆': '350460', '马来西亚': '350120', '不丹': '350180', '巴勒斯坦': '350360', '也门': '350430', '文莱': '350130', '新加坡': '350140', '巴基斯坦': '350210', '日本': '350050', '尼泊尔': '350170', '马尔代夫': '350230', '缅甸': '350100', '约旦': '350330', '东帝汶': '350160', '哈萨克斯坦': '350240', '巴林': '350380', '格鲁吉亚': '350440', '阿联酋': '350410', '沙特阿拉伯': '350370', '韩国': '350040', '吉尔吉斯': '350250', '伊朗': '350310', '柬埔寨': '350090', '斯里兰卡': '350220', '越南': '350070', '叙利亚': '350320', '卡塔尔': '350390', '黎巴嫩': '350340', '伊拉克': '350300', '孟加拉': '350190', '亚美尼亚': '350450', '老挝': '350080', '塔吉克斯坦': '350260', '土耳其': '350470', '蒙古': '350020', '朝鲜': '350030', '以色列': '350350', '泰国': '350110', '科威特': '350400', '菲律宾': '350060', '阿曼': '350420', '阿富汗': '350290', '土库曼斯坦': '350280'}}, '滨州': {'code': '250150', 'sublist': {}}, '黄山': {'code': '080100', 'sublist': {}}, '怀化': {'code': '180140', 'sublist': {}}, '济宁': {'code': '250050', 'sublist': {}}, '自贡': {'code': '280080', 'sublist': {}}, '九江': {'code': '200030', 'sublist': {}}, '信阳': {'code': '150180', 'sublist': {}}, '雅安': {'code': '280170', 'sublist': {}}, '鹤壁': {'code': '150140', 'sublist': {}}, '神农架': {'code': '170170', 'sublist': {}}, '百慕大': {'code': '360370', 'sublist': {}}, '衡阳': {'code': '180060', 'sublist': {}}, '郑州': {'code': '150020', 'sublist': {'荥阳市': '150020130', '上街区': '150020060', '金水区': '150020010', '巩义市': '150020120', '登封市': '150020160', '新郑市': '150020150', '加工区': '150020110', '惠济区': '150020070', '新密市': '150020140', '管城区': '150020040', '二七区': '150020030', '邙山区': '150020020', '中原区': '150020050', '郑东区': '150020080', '中牟县': '150020170', '高新区': '150020100', '经济区': '150020090'}}, '包头': {'code': '220030', 'sublist': {}}, '福州': {'code': '090020', 'sublist': {'闽清县': '090020110', '晋安区': '090020050', '永泰县': '090020120', '鼓楼区': '090020010', '罗源县': '090020100', '仓山区': '090020030', '福清市': '090020060', '马尾区': '090020040', '台江区': '090020020', '长乐市': '090020070', '连江县': '090020090', '平潭县': '090020130', '闽侯县': '090020080'}}, '克拉玛依': {'code': '300040', 'sublist': {}}, '桂林': {'code': '110040', 'sublist': {}}, '防城港': {'code': '110100', 'sublist': {}}, '长春': {'code': '190020', 'sublist': {'德惠市': '190020110', '绿园区': '190020050', '农安县': '190020140', '经开区': '190020090', '朝阳区': '190020010', '南关区': '190020040', '二道区': '190020030', '双阳区': '190020060', '汽开区': '190020100', '经济区': '190020160', '宽城区': '190020020', '榆树市': '190020130', '九台市': '190020120', '高新区': '190020080', '净月区': '190020070'}}, '阳泉': {'code': '260070', 'sublist': {}}, '松原': {'code': '190080', 'sublist': {}}, '黄石': {'code': '170090', 'sublist': {}}, '宜昌': {'code': '170050', 'sublist': {}}, '渭南': {'code': '270060', 'sublist': {}}, '新乡': {'code': '150080', 'sublist': {}}, '苏州': {'code': '060080', 'sublist': {'周庄镇': '060080210', '沧浪区': '060080020', '工业园': '060080040', '锦溪镇': '060080230', '张家港': '060080080', '昆山市': '060080110', '常熟市': '060080090', '张浦镇': '060080200', '开发区': '060080240', '吴中区': '060080060', '平江区': '060080030', '高新区': '060080050', '陆家镇': '060080170', '太仓市': '060080100', '花桥镇': '060080180', '巴城镇': '060080150', '玉山镇': '060080140', '金阊区': '060080010', '淀山湖': '060080190', '虎丘区': '060080130', '相城区': '060080070', '周市镇': '060080160', '千灯镇': '060080220', '吴江市': '060080120'}}, '通化': {'code': '190060', 'sublist': {}}, '七台河': {'code': '160110', 'sublist': {}}, '陇南': {'code': '100110', 'sublist': {}}, '奎屯': {'code': '300200', 'sublist': {}}, '枣庄': {'code': '250140', 'sublist': {}}, '玉林': {'code': '110060', 'sublist': {}}, '吉林': {'code': '190030', 'sublist': {}}, '乳山': {'code': '250210', 'sublist': {}}, '尼加拉瓜': {'code': '360100', 'sublist': {}}, '青岛': {'code': '250070', 'sublist': {'城阳区': '250070030', '四方区': '250070040', '胶州市': '250070080', '市南区': '250070010', '崂山区': '250070070', '即墨市': '250070090', '黄岛区': '250070060', '市北区': '250070020', '胶南市': '250070110', '平度市': '250070100', '莱西市': '250070120', '李沧区': '250070050'}}, '安提瓜': {'code': '360180', 'sublist': {}}, '衡水': {'code': '140120', 'sublist': {}}, '丹东': {'code': '210080', 'sublist': {}}, '三沙': {'code': '130040', 'sublist': {}}, '临汾': {'code': '260040', 'sublist': {}}, '锡林郭勒盟': {'code': '220120', 'sublist': {}}, '黔南': {'code': '120100', 'sublist': {}}, '辽阳': {'code': '210120', 'sublist': {}}, '美属维尔京': {'code': '360280', 'sublist': {}}, '圣卢西亚': {'code': '360210', 'sublist': {}}, '张家界': {'code': '180110', 'sublist': {}}, '甘南': {'code': '100150', 'sublist': {}}, '开封': {'code': '150030', 'sublist': {}}, '昆山': {'code': '060050', 'sublist': {}}, '漳州': {'code': '090050', 'sublist': {}}, '唐山': {'code': '140080', 'sublist': {}}, '东营': {'code': '250040', 'sublist': {}}, '东方': {'code': '130100', 'sublist': {}}, '普洱': {'code': '310090', 'sublist': {}}, '海阳': {'code': '250260', 'sublist': {}}, '萍乡': {'code': '200100', 'sublist': {}}, '济南': {'code': '250020', 'sublist': {'长清区': '250020060', '平阴县': '250020080', '市中区': '250020010', '商河县': '250020100', '历下区': '250020020', '章丘市': '250020070', '历城区': '250020050', '天桥区': '250020030', '近郊': '250020120', '槐荫区': '250020040', '济阳县': '250020090', '高新区': '250020110'}}, '宁波': {'code': '070030', 'sublist': {'江东区': '070030020', '镇海区': '070030040', '北仑区': '070030050', '象山县': '070030100', '鄞州区': '070030060', '奉化市': '070030090', '慈溪市': '070030080', '海曙区': '070030010', '余姚市': '070030070', '宁海县': '070030110', '江北区': '070030030'}}, '甘孜': {'code': '280210', 'sublist': {}}, '高邮': {'code': '060280', 'sublist': {}}, '象山': {'code': '070320', 'sublist': {}}, '西宁': {'code': '240020', 'sublist': {'城西区': '240020030', '城东区': '240020020', '海湖区': '240020090', '湟源县': '240020060', '城北区': '240020040', '湟中县': '240020050', '大通': '240020070', '城中区': '240020010', '城南区': '240020080'}}, '图木舒克': {'code': '300110', 'sublist': {}}, '保亭': {'code': '130170', 'sublist': {}}, '圣基茨': {'code': '360190', 'sublist': {}}, '临沂': {'code': '250060', 'sublist': {}}, '德清': {'code': '070310', 'sublist': {}}, '湘潭': {'code': '180030', 'sublist': {}}, '巴彦淖尔': {'code': '220090', 'sublist': {}}, '广安': {'code': '280150', 'sublist': {}}, '汕尾': {'code': '050200', 'sublist': {}}, '即墨': {'code': '250230', 'sublist': {}}, '牡丹江': {'code': '160050', 'sublist': {}}, '宁德': {'code': '090100', 'sublist': {}}, '台湾': {'code': '340', 'sublist': {'高雄': '340010020', '基隆': '340010030', '台北': '340010010', '苗栗县': '340010100', '屏东县': '340010140', '花莲县': '340010160', '台南': '340010050', '澎湖县': '340010170', '桃园县': '340010090', '新竹': '340010060', '台东县': '340010150', '南投县': '340010120', '云林县': '340010130', '嘉义': '340010070', '台中': '340010040', '彰化县': '340010110', '宜兰县': '340010080'}}, '鹤岗': {'code': '160080', 'sublist': {}}, '梅州': {'code': '050190', 'sublist': {}}, '湘西': {'code': '180150', 'sublist': {}}, '深圳': {'code': '050090', 'sublist': {'罗湖区': '050090010', '坪山新区': '050090080', '盐田区': '050090060', '南山区': '050090030', '福田区': '050090020', '龙华新区': '050090100', '光明新区': '050090070', '大鹏新区': '050090090', '宝安区': '050090040', '龙岗区': '050090050'}}, '大理': {'code': '310030', 'sublist': {}}, '伊春': {'code': '160100', 'sublist': {}}, '承德': {'code': '140040', 'sublist': {}}, '钦州': {'code': '110120', 'sublist': {}}, '眉山': {'code': '280140', 'sublist': {}}, '长葛': {'code': '150210', 'sublist': {}}, '海地': {'code': '360160', 'sublist': {}}, '宝鸡': {'code': '270030', 'sublist': {}}, '欧洲': {'code': '390', 'sublist': {'摩尔多瓦': '390140', '斯洛伐克': '390450', '列支敦士登': '390210', '挪威': '390040', '瑞士': '390200', '保加利亚': '390300', '俄罗斯': '390120', '波兰': '390150', '冰岛': '390050', '法罗群岛': '390070', '波墨': '390370', '塞尔维亚': '390310', '法国': '390270', '摩纳哥': '390280', '斯洛文尼亚': '390350', '马耳他': '390410', '西班牙': '390420', '立陶宛': '390100', '比利时': '390250', '英国': '390220', '奥地利': '390190', '卢森堡': '390260', '爱沙尼亚': '390080', '拉脱维亚': '390090', '圣马力诺': '390400', '乌克兰': '390130', '罗马尼亚': '390290', '荷兰': '390240', '梵蒂冈': '390390', '丹麦': '390060', '安道尔': '390440', '克罗地亚': '390360', '爱尔兰': '390230', '芬兰': '390020', '马其顿': '390320', '匈牙利': '390170', '意大利': '390380', '白俄罗斯': '390110', '捷克': '390160', '希腊': '390340', '瑞典': '390030', '德国': '390180', '葡萄牙': '390430', '阿尔巴尼亚': '390330'}}, '东莞': {'code': '050040', 'sublist': {'樟木头': '050040180', '东城区': '050040020', '大岭山': '050040150', '石龙镇': '050040050', '横沥镇': '050040260', '石排镇': '050040290', '黄江镇': '050040170', '谢岗镇': '050040210', '道滘镇': '050040080', '石碣镇': '050040090', '茶山镇': '050040130', '常平镇': '050040240', '麻涌镇': '050040070', '望牛墩': '050040110', '南城区': '050040010', '厚街镇': '050040220', '塘厦镇': '050040200', '寮步镇': '050040140', '企石镇': '050040280', '高埗镇': '050040320', '凤岗镇': '050040190', '万江区': '050040030', '虎门镇': '050040060', '沙田镇': '050040100', '松山湖': '050040330', '东坑镇': '050040270', '中堂镇': '050040310', '桥头镇': '050040250', '大朗镇': '050040160', '长安镇': '050040300', '莞城区': '050040040', '清溪镇': '050040230', '洪梅镇': '050040120'}}, '安顺': {'code': '120050', 'sublist': {}}, '澄迈': {'code': '130140', 'sublist': {}}, '成都': {'code': '280020', 'sublist': {'龙泉驿': '280020060', '蒲江县': '280020140', '大邑县': '280020120', '温江区': '280020110', '武侯区': '280020020', '邛崃市': '280020210', '青白江': '280020070', '郫县': '280020100', '新津县': '280020150', '青羊区': '280020030', '彭州市': '280020200', '高新西': '280020180', '崇州市': '280020220', '成华区': '280020010', '金堂县': '280020130', '新都区': '280020080', '都江堰': '280020190', '金牛区': '280020050', '高新区': '280020170', '双流县': '280020090', '锦江区': '280020040'}}, '巴拿马': {'code': '360120', 'sublist': {}}, '海城': {'code': '210170', 'sublist': {}}, '宜春': {'code': '200050', 'sublist': {}}, '乌兰察布': {'code': '220100', 'sublist': {}}, '大同': {'code': '260030', 'sublist': {}}, '恩施': {'code': '170180', 'sublist': {}}, '格陵兰': {'code': '360050', 'sublist': {}}, '温岭': {'code': '070260', 'sublist': {}}, '阿鲁巴': {'code': '360340', 'sublist': {}}, '北京': {'code': '010', 'sublist': {'顺义区': '010010130', '海淀区': '010010050', '东城区': '010010010', '平谷区': '010010140', '密云县': '010010180', '石景山': '010010070', '延庆县': '010010170', '朝阳区': '010010030', '门头沟': '010010080', '昌平区': '010010150', '怀柔区': '010010160', '西城区': '010010020', '丰台区': '010010090', '大兴区': '010010110', '房山区': '010010100', '通州区': '010010120'}}, '胶南': {'code': '250280', 'sublist': {}}, '台州': {'code': '070070', 'sublist': {}}, '张家口': {'code': '140090', 'sublist': {}}, '南昌': {'code': '200020', 'sublist': {'桑海区': '200020130', '东湖区': '200020010', '安义县': '200020110', '西湖区': '200020020', '新建县': '200020100', '进贤县': '200020120', '南昌县': '200020090', '红谷滩': '200020060', '昌北区': '200020070', '青山湖': '200020050', '湾里区': '200020040', '高新区': '200020080', '青云谱': '200020030'}}, '英属维尔京': {'code': '360270', 'sublist': {}}, '乌鲁木齐': {'code': '300020', 'sublist': {'达坂城': '300020060', '昌吉市': '300020090', '巴克区': '300020020', '天山区': '300020010', '乌县': '300020080', '水磨沟': '300020040', '新市区': '300020030', '米东区': '300020070', '阜康市': '300020110', '头屯河': '300020050'}}, '六盘水': {'code': '120040', 'sublist': {}}, '巴音郭楞': {'code': '300180', 'sublist': {}}, '辽源': {'code': '190050', 'sublist': {}}, '石嘴山': {'code': '230030', 'sublist': {}}, '景德镇': {'code': '200090', 'sublist': {}}, '西安': {'code': '270020', 'sublist': {'新城区': '270020020', '碑林区': '270020030', '未央区': '270020060', '灞桥区': '270020050', '临潼区': '270020080', '蓝田县': '270020100', '长安区': '270020090', '高陵县': '270020130', '阎良区': '270020070', '雁塔区': '270020040', '莲湖区': '270020010', '经开区': '270020140', '户县': '270020120', '高新区': '270020150', '周至县': '270020110'}}, '香河': {'code': '140160', 'sublist': {}}, '淄博': {'code': '250130', 'sublist': {}}, '南平': {'code': '090080', 'sublist': {}}, '吴忠': {'code': '230040', 'sublist': {}}, '阿里': {'code': '290080', 'sublist': {}}, '定西': {'code': '100100', 'sublist': {}}, '贵阳': {'code': '120020', 'sublist': {'息烽县': '120020120', '花溪区': '120020030', '开阳县': '120020100', '金阳区': '120020070', '白云区': '120020050', '小河区': '120020060', '修文县': '120020110', '新天园': '120020080', '云岩区': '120020020', '南明区': '120020010', '乌当区': '120020040', '清镇市': '120020090'}}, '吉安': {'code': '200060', 'sublist': {}}, '邯郸': {'code': '140050', 'sublist': {}}, '巢湖': {'code': '080180', 'sublist': {}}, '随州': {'code': '170140', 'sublist': {}}, '吕梁': {'code': '260120', 'sublist': {}}, '无锡': {'code': '060100', 'sublist': {'锡山区': '060100040', '江阴市': '060100090', '南长区': '060100030', '新区': '060100070', '崇安区': '060100010', '宜兴市': '060100080', '惠山区': '060100050', '滨湖区': '060100060', '北塘区': '060100020'}}, '天门': {'code': '170160', 'sublist': {}}, '赤峰': {'code': '220040', 'sublist': {}}, '迪庆': {'code': '310170', 'sublist': {}}, '鞍山': {'code': '210030', 'sublist': {}}, '商洛': {'code': '270090', 'sublist': {}}, '南通': {'code': '060070', 'sublist': {}}, '巴中': {'code': '280180', 'sublist': {}}, '扬中': {'code': '060270', 'sublist': {}}, '威海': {'code': '250100', 'sublist': {}}, '杨凌': {'code': '270120', 'sublist': {}}, '抚顺': {'code': '210060', 'sublist': {}}, '晋城': {'code': '260080', 'sublist': {}}, '泰安': {'code': '250090', 'sublist': {}}, '屯昌': {'code': '130130', 'sublist': {}}, '丹阳': {'code': '060200', 'sublist': {}}, '日照': {'code': '250080', 'sublist': {}}, '柳州': {'code': '110050', 'sublist': {}}, '溧阳': {'code': '060210', 'sublist': {}}, '红河': {'code': '310110', 'sublist': {}}, '莱芜': {'code': '250180', 'sublist': {}}, '武威': {'code': '100090', 'sublist': {}}, '思茅': {'code': '310180', 'sublist': {}}, '城阳': {'code': '250220', 'sublist': {}}, '聊城': {'code': '250160', 'sublist': {}}, '朝阳': {'code': '210150', 'sublist': {}}, '长治': {'code': '260060', 'sublist': {}}, '舟山': {'code': '070120', 'sublist': {}}, '驻马店': {'code': '150160', 'sublist': {}}, '宿州': {'code': '080130', 'sublist': {}}, '重庆': {'code': '040', 'sublist': {'黔江区': '040010190', '綦江区': '040010200', '北碚区': '040010070', '南岸区': '040010030', '奉节县': '040010340', '酉阳县': '040010390', '沙坪坝': '040010040', '铜梁区': '040010220', '江北区': '040010020', '大渡口': '040010060', '丰都县': '040010280', '武隆县': '040010270', '秀山县': '040010420', '南川区': '040010170', '渝中区': '040010010', '永川区': '040010100', '万州区': '040010180', '开县': '040010310', '石柱': '040010370', '巫溪县': '040010320', '云阳县': '040010350', '合川区': '040010120', '垫江县': '040010260', '潼南县': '040010210', '梁平县': '040010300', '巴南区': '040010080', '璧山区': '040010250', '大足区': '040010230', '涪陵区': '040010110', '渝北区': '040010090', '九龙坡': '040010050', '巫山县': '040010330', '彭水县': '040010380', '荣昌县': '040010240', '城口县': '040010290', '忠县': '040010360', '长寿区': '040010140', '江津区': '040010130', '石柱县': '040010410'}}, '危地马拉': {'code': '360060', 'sublist': {}}, '永济': {'code': '260130', 'sublist': {}}, '玉溪': {'code': '310050', 'sublist': {}}, '阿克苏': {'code': '300060', 'sublist': {}}, '句容': {'code': '060250', 'sublist': {}}, '绥化': {'code': '160130', 'sublist': {}}, '墨西哥': {'code': '360040', 'sublist': {}}, '哥斯达黎加': {'code': '360110', 'sublist': {}}, '淮南': {'code': '080060', 'sublist': {}}, '呼伦贝尔': {'code': '220080', 'sublist': {}}, '怒江': {'code': '310160', 'sublist': {}}, '天水': {'code': '100070', 'sublist': {}}, '秦皇岛': {'code': '140070', 'sublist': {}}, '洛阳': {'code': '150040', 'sublist': {}}, '佳木斯': {'code': '160040', 'sublist': {}}, '镇江': {'code': '060130', 'sublist': {}}, '兴城': {'code': '210160', 'sublist': {}}, '大洋洲': {'code': '380', 'sublist': {'密克罗尼西亚': '380070', '美属萨摩亚': '380240', '基里巴斯': '380110', '瓦利斯': '380210', '瓦努阿图': '380060', '波利尼西亚': '380190', '库克群岛': '380160', '澳大利亚': '380020', '马绍尔群岛': '380080', '托克劳': '380230', '萨摩亚': '380130', '纽埃': '380220', '帕劳群岛': '380090', '汤加': '380150', '关岛': '380170', '新喀里多尼亚': '380180', '斐济群岛': '380140', '巴布亚': '380040', '所罗门群岛': '380050', '皮特凯恩岛': '380200', '图瓦卢': '380120', '北马里亚纳': '380250', '新西兰': '380030', '瑙鲁': '380100'}}}
    page_num = 1
    judge = 0
    total = 0
    jobs_url_li = []
    job_save_lp = []
    flag_next = True
    job_linshi = []
    job_linshi_id = []
    fan_ye = 0
    while flag_next:
        try:
            try:
                city_jc = cityList_dic[cityName]['code']
            except:
                judge = 1
                traceback.print_exc()
                break
            d_pos = {"kw111": compName}
            postname = parse.urlencode(d_pos).encode('utf-8')
            com_name = str(postname).split('kw111=')[1][:-1]
            if countyName != '':
                try:
                    county_jc=cityList_dic[cityName]['sublist'][countyName]
                    url_lp_zw = 'https://www.liepin.com/zhaopin/?key=' + com_name + '&fromSearchBtn=2&dqs=' + county_jc + '&curPage=' + str(page_num - 1)
                except:
                    try:
                        county_Name = countyName.replace('区','')
                        county_jc = cityList_dic[cityName]['sublist'][county_Name]
                        url_lp_zw = 'https://www.liepin.com/zhaopin/?key=' + com_name + '&fromSearchBtn=2&dqs=' + county_jc + '&curPage=' + str(page_num - 1)
                    except:
                        url_lp_zw = 'https://www.liepin.com/zhaopin/?key=' + com_name + '&fromSearchBtn=2&dqs=' + city_jc + '&curPage=' + str(page_num - 1)
                        pass
            else:
                url_lp_zw = 'https://www.liepin.com/zhaopin/?key=' + com_name + '&fromSearchBtn=2&dqs=' + city_jc + '&curPage=' + str(page_num - 1)
            print('lp----', url_lp_zw)
            url_lp_zw = 'https://www.liepin.com/zhaopin/?key=' + com_name + '&fromSearchBtn=2&dqs=' + city_jc + '&curPage=' + str(page_num - 1)
            try:
                html_li_text=xh_pd_req(pos_url=url_lp_zw,data='',headers=head_reqst())
            except:
                flag_next = False
                break
            # request_li = request.Request(url=url_lp_zw, headers=head_reqst())
            # reponse_li = request.urlopen(request_li,timeout=3).read()
            # html_li_text = reponse_li.decode('utf-8', errors='ignore')
            # print(html_li_text)
            if "猎聘" in html_li_text:
                sel = Selector(text=html_li_text)
                xpa_lpjob_li = '//ul[@class="sojob-list"]/li'

                for job_lp in sel.xpath(xpa_lpjob_li):
                    joblp_name = job_lp.xpath('string(//p[@class="company-name"]/a)').extract()[0]
                    if joblp_name == compName:
                        joblp_url = job_lp.xpath('div/div[@class="job-info"]/h3/a/@href').extract()[0]
                        joblp_id = joblp_url.split("job/")[1].split(".shtml")[0]
                        if 'http' not in joblp_url:
                            joblp_url = 'http://' + joblp_url

                        # 如果链接为一条新的链接
                        if joblp_id not in job_linshi:
                            fan_ye = 1
                            jobs_url_li.append(joblp_url)
                            job_linshi.append(joblp_id)
                            job_linshi_id.append(joblp_id)
                        else:
                            # print(joblp_id)
                            # print(joblp_url)
                            fan_ye = 0
                            flag_next = False

                # 判断是否进入下一页
                if fan_ye != 0 and job_linshi_id != []:
                    # print("下一页")
                    page_num = page_num + 1
                    if page_num > 50:
                        flag_next = False
                else:
                    flag_next = False
                job_linshi_id = []
        except:
            # traceback.print_exc()
            pass
    try:
        for index, joblp_url1 in enumerate(jobs_url_li):
            try:
                time.sleep(random.uniform(0.3, 0.6))
                try:
                    job_xq_text = xh_pd_req(pos_url=joblp_url1,data='',headers=head_reqst())
                    # request_job_lp = request.Request(url=joblp_url1, headers=head_reqst())
                    # response_job_lp = request.urlopen(request_job_lp, timeout=3).read()
                    # job_xq_text = response_job_lp.decode('utf-8', errors='ignore')
                    zw_data_lp = zwjx_lp(text=job_xq_text, compName=compName)
                    zw_data_lp['type'] = 'job'
                    zw_data_lp['channel'] = channelid
                    zw_data_lp['companyName'] = compName
                    zw_data_lp['province'] = provName
                    zw_data_lp['city'] = cityName_0
                    zw_data_lp['county'] = countyName
                    print('lp-------', zw_data_lp)
                except:
                    traceback.print_exc()
                    pass
                job_save_lp.append(zw_data_lp)
                if len(job_save_lp) == 3:
                    total=total+3
                    data = json.dumps(job_save_lp)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('lp_jobl----3')
                    job_save_lp = []
            except:
                pass
        if len(job_save_lp) == 3 or len(job_save_lp) == 0:
            pass
        else:
            total = total + len(job_save_lp)
            data = json.dumps(job_save_lp)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
            logging.error('lp_jobl----yfs')
    except:
        # traceback.print_exc()
        pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_rcrxzw(compName, provName, cityName, countyName,cityName_0, channelid=12):
    dict_num={'保亭': {'code': '6418'}, '昌吉': {'code': '5705'}, '潮州': {'code': '2040'}, '商洛': {'code': '5310'}, '上饶': {'code': '4305'}, '宿州': {'code': '4111'}, '邵阳': {'code': '4705'}, '玉树': {'code': '5507'}, '佳木斯': {'code': '3804'}, '黔南': {'code': '5009'}, '运城': {'code': '3411'}, '咸宁': {'code': '4611'}, '万宁': {'code': '6408'}, '安顺': {'code': '5004'}, '澄迈': {'code': '6412'}, '咸阳': {'code': '5304'}, '宜昌': {'code': '4604'}, '防城港': {'code': '4806'}, '临高': {'code': '6413'}, '抚顺': {'code': '3604'}, '景德镇': {'code': '4308'}, '秦皇岛': {'code': '3303'}, '伊犁': {'code': '5712'}, '陇南': {'code': '5412'}, '七台河': {'code': '3810'}, '花莲': {'code': '6103'}, '香港': {'sublist': {'香港岛': '6002', '新界': '6003', '九龙': '6001'}, 'code': '60'}, '呼伦贝尔': {'code': '3505'}, '曲靖': {'code': '5102'}, '汕头': {'code': '2014'}, '乐东': {'code': '6416'}, '东营': {'code': '4405'}, '湖州': {'code': '4006'}, '桃园': {'code': '6116'}, '济源': {'code': '4518'}, '大同': {'code': '3402'}, '鹰潭': {'code': '4311'}, '安康': {'code': '5309'}, '苗栗': {'code': '6108'}, '鹤壁': {'code': '4506'}, '承德': {'code': '3308'}, '攀枝花': {'code': '4903'}, '绵阳': {'code': '4906'}, '三沙': {'code': '6403'}, '天门': {'code': '4616'}, '哈密': {'code': '5704'}, '漯河': {'code': '4511'}, '南平': {'code': '4208'}, '营口': {'code': '3608'}, '克拉玛依': {'code': '5702'}, '合肥': {'code': '4101'}, '宜兰': {'code': '6120'}, '黄山': {'code': '4109'}, '焦作': {'code': '4508'}, '淄博': {'code': '4403'}, '上海': {'sublist': {'静安区': '300105', '宝山区': '300110', '闵行区': '300111', '奉贤区': '300118', '松江区': '300114', '浦东新区': '300113', '金山区': '300115', '长宁区': '300104', '青浦区': '300116', '卢湾区': '300102', '崇明县': '300119', '南汇区': '300117', '虹口区': '300108', '嘉定区': '300112', '黄浦区': '300101', '杨浦区': '300109', '普陀区': '300106', '徐汇区': '300103', '闸北区': '300107'}, 'code': '30'}, '龙岩': {'code': '4206'}, '锡林郭勒': {'code': '3508'}, '泸州': {'code': '4904'}, '重庆': {'sublist': {'巫山': '6330', '巴南': '6312', '潼南': '6316', '九龙坡': '6307', '江北': '6305', '荣昌': '6319', '忠县': '6326', '铜梁': '6317', '黔江': '6313', '奉节': '6329', '城口': '6322', '秀山': '6333', '大渡口': '6304', '梁平': '6321', '綦江': '6315', '巫溪': '6331', '武隆': '6325', '彭水': '6335', '垫江': '6324', '合川': '6337', '云阳': '6328', '丰都': '6323', '长寿': '6314', '大足': '6318', '江律': '6336', '永川': '6338', '万州': '6301', '璧山': '6320', '沙坪坝': '6306', '渝北': '6311', '石柱': '6332', '渝中': '6303', '万盛': '6310', '酉阳': '6334', '南川': '6339', '涪陵': '6302', '北碚': '6309', '南岸': '6308', '开县': '6327'}, 'code': '63'}, '蚌埠': {'code': '4103'}, '贺州': {'code': '4811'}, '巴音郭楞': {'code': '5707'}, '克孜勒苏柯尔克孜': {'code': '5709'}, '吕梁': {'code': '3408'}, '泰安': {'code': '4409'}, '玉溪': {'code': '5103'}, '舟山': {'code': '4011'}, '安阳': {'code': '4505'}, '黄南': {'code': '5504'}, '甘孜': {'code': '4920'}, '嘉义': {'code': '6104'}, '眉山': {'code': '4912'}, '许昌': {'code': '4510'}, '宝鸡': {'code': '5303'}, '石家庄': {'code': '3301'}, '平凉': {'code': '5408'}, '阿拉善': {'code': '3512'}, '延安': {'code': '5306'}, '衢州': {'code': '4008'}, '威海': {'code': '4410'}, '北京': {'sublist': {'平谷区': '310116', '顺义区': '310112', '门头沟区': '310109', '房山区': '310110', '朝阳区': '310105', '丰台区': '310107', '昌平区': '310113', '石景山区': '310108', '大兴区': '310114', '西城区': '310102', '崇文区': '310103', '延庆县': '310118', '海淀区': '310106', '宣武区': '310104', '东城区': '310101', '通州区': '310111', '密云县': '310117', '怀柔区': '310115'}, 'code': '31'}, '神农架': {'code': '4617'}, '酒泉': {'code': '5409'}, '广州': {'sublist': {'天河区': '201005', '海珠区': '201004', '芳村区': '201008', '萝岗区': '201014', '越秀区': '201001', '荔湾区': '201003', '从化区': '201011', '黄埔区': '201007', '增城区': '201012', '花都区': '201009', '白云区': '201006', '南沙区': '201013', '番禺区': '201010', '东山区': '201002'}, 'code': '2010'}, '白银': {'code': '5404'}, '石河子': {'code': '5715'}, '邯郸': {'code': '3304'}, '临夏': {'code': '5413'}, '淮北': {'code': '4106'}, '平顶山': {'code': '4504'}, '宁波': {'code': '4002'}, '琼海': {'code': '6405'}, '鹤岗': {'code': '3808'}, '呼和浩特': {'code': '3501'}, '西双版纳': {'code': '5112'}, '辽阳': {'code': '3610'}, '沈阳': {'code': '3601'}, '渭南': {'code': '5305'}, '兴安': {'code': '3506'}, '钦州': {'code': '4807'}, '宜春': {'code': '4303'}, '铜仁': {'code': '5005'}, '郑州': {'code': '4501'}, '通化': {'code': '3705'}, '丽江': {'code': '5106'}, '十堰': {'code': '4603'}, '保定': {'code': '3306'}, '德阳': {'code': '4905'}, '通辽': {'code': '3507'}, '新竹县': {'code': '6119'}, '云浮': {'code': '2044'}, '揭阳': {'code': '2042'}, '烟台': {'code': '4406'}, '新北': {'code': '6117'}, '韶关': {'code': '2022'}, '漳州': {'code': '4205'}, '图木舒克': {'code': '5717'}, '吐鲁番': {'code': '5703'}, '松原': {'code': '3709'}, '楚雄': {'code': '5109'}, '新竹': {'code': '6118'}, '海北': {'code': '5503'}, '遂宁': {'code': '4908'}, '安庆': {'code': '4108'}, '周口': {'code': '4514'}, '阜新': {'code': '3609'}, '江门': {'sublist': {'台山': '201804', '恩平': '201807', '蓬江': '201801', '鹤山': '201806', '新会': '201803', '江海': '201802', '开平': '201805'}, 'code': '2018'}, '金华': {'code': '4004'}, '枣庄': {'code': '4404'}, '白沙': {'code': '6414'}, '厦门': {'code': '4202'}, '澳门': {'sublist': {'离岛': '6202', '澳门半岛': '6201'}, 'code': '62'}, '阿拉尔': {'code': '5716'}, '达州': {'code': '4915'}, '宿迁': {'code': '3913'}, '临沂': {'code': '4415'}, '葫芦岛': {'code': '3614'}, '天水': {'code': '5405'}, '成都': {'code': '4901'}, '武汉': {'code': '4601'}, '白城': {'code': '3707'}, '定西': {'code': '5411'}, '屯昌': {'code': '6411'}, '新乡': {'code': '4507'}, '喀什': {'code': '5710'}, '赣州': {'code': '4302'}, '衡水': {'code': '3311'}, '桂林': {'code': '4803'}, '琼中': {'code': '6419'}, '怀化': {'code': '4712'}, '济南': {'code': '4401'}, '岳阳': {'code': '4706'}, '铜川': {'code': '5302'}, '台南': {'code': '6114'}, '黔东南': {'code': '5008'}, '萍乡': {'code': '4309'}, '常德': {'code': '4707'}, '百色': {'code': '4810'}, '肇庆': {'code': '2036'}, '巴中': {'code': '4917'}, '陵水': {'code': '6417'}, '双鸭山': {'code': '3809'}, '柳州': {'code': '4802'}, '和田': {'code': '5711'}, '张家口': {'code': '3307'}, '洛阳': {'code': '4503'}, '雅安': {'code': '4916'}, '湘西': {'code': '4714'}, '文昌': {'code': '6407'}, '甘南': {'code': '5414'}, '兰州': {'code': '5401'}, '吴忠': {'code': '5603'}, '乌鲁木齐': {'code': '5701'}, '鞍山': {'code': '3603'}, '中山': {'sublist': {'石岐区街道': '201201', '小榄镇': '201203', '东区街道': '201202'}, 'code': '2012'}, '包头': {'code': '3502'}, '潜江': {'code': '4615'}, '贵港': {'code': '4808'}, '徐州': {'code': '3904'}, '无锡': {'code': '3902'}, '深圳': {'sublist': {'大鹏新区': '200809', '宝安区': '200804', '福田区': '200803', '罗湖区': '200802', '盐田区': '200806', '龙岗区': '200805', '龙华新区': '200810', '南山区': '200801', '坪山新区': '200808', '光明新区': '200807'}, 'code': '2008'}, '文山': {'code': '5111'}, '娄底': {'code': '4713'}, '普洱': {'code': '5107'}, '哈尔滨': {'code': '3801'}, '银川': {'code': '5601'}, '淮南': {'code': '4104'}, '清远': {'code': '2038'}, '遵义': {'code': '5003'}, '珠海': {'sublist': {'香洲区': '201301', '金湾区': '201303', '斗门区': '201302'}, 'code': '2013'}, '西宁': {'code': '5501'}, '昆明': {'code': '5101'}, '昌江': {'code': '6415'}, '榆林': {'code': '5308'}, '塔城': {'code': '5713'}, '黄石': {'code': '4602'}, '张掖': {'code': '5407'}, '嘉义县': {'code': '6105'}, '鄂州': {'code': '4606'}, '鸡西': {'code': '3807'}, '太原': {'code': '3401'}, '白山': {'code': '3706'}, '阿里': {'code': '5206'}, '南阳': {'code': '4516'}, '聊城': {'code': '4414'}, '长春': {'code': '3702'}, '广元': {'code': '4907'}, '梧州': {'code': '4804'}, '金昌': {'code': '5403'}, '广安': {'code': '4914'}, '河池': {'code': '4812'}, '宜宾': {'code': '4913'}, '孝感': {'code': '4608'}, '铁岭': {'code': '3612'}, '汕尾': {'code': '2028'}, '常州': {'code': '3905'}, '红河': {'code': '5110'}, '唐山': {'code': '3302'}, '滁州': {'code': '4112'}, '九江': {'code': '4307'}, '南通': {'code': '3906'}, '本溪': {'code': '3605'}, '毕节': {'code': '5007'}, '台州': {'code': '4009'}, '阿勒泰': {'code': '5714'}, '商丘': {'code': '4513'}, '海南藏族': {'code': '5505'}, '凉山': {'code': '4921'}, '淮安': {'code': '3908'}, '福州': {'code': '4201'}, '抚州': {'code': '4306'}, '固原': {'code': '5604'}, '内江': {'code': '4909'}, '茂名': {'code': '2034'}, '大兴安岭': {'code': '3813'}, '定安': {'code': '6410'}, '恩施': {'code': '4613'}, '资阳': {'code': '4918'}, '北海': {'code': '4805'}, '镇江': {'code': '3911'}, '莆田': {'code': '4203'}, '盘锦': {'code': '3611'}, '武威': {'code': '5406'}, '莱芜': {'code': '4417'}, '乌海': {'code': '3503'}, '自贡': {'code': '4902'}, '梅州': {'code': '2026'}, '怒江': {'code': '5115'}, '锦州': {'code': '3607'}, '沧州': {'code': '3309'}, '屏东': {'code': '6111'}, '盐城': {'code': '3909'}, '南充': {'code': '4911'}, '池州': {'code': '4116'}, '齐齐哈尔': {'code': '3802'}, '湛江': {'code': '2032'}, '彰化': {'code': '6122'}, '云林': {'code': '6121'}, '荆门': {'code': '4607'}, '滨州': {'code': '4412'}, '嘉峪关': {'code': '5402'}, '贵阳': {'code': '5001'}, '赤峰': {'code': '3504'}, '南昌': {'code': '4301'}, '丹东': {'code': '3606'}, '三门峡': {'code': '4512'}, '惠州': {'sublist': {'仲恺高新区': '201507', '惠城区': '201502', '惠阳区': '201504', '龙门县': '201505', '大亚湾区': '201506', '惠东县': '201503', '博罗县': '201501'}, 'code': '2015'}, '果洛': {'code': '5506'}, '丽水': {'code': '4010'}, '汉中': {'code': '5307'}, '高雄': {'code': '6102'}, '东方': {'code': '6409'}, '拉萨': {'code': '5201'}, '延边': {'code': '3708'}, '湘潭': {'code': '4703'}, '台中': {'code': '6115'}, '大连': {'code': '3602'}, '中卫': {'code': '5605'}, '阿克苏': {'code': '5708'}, '黄冈': {'code': '4610'}, '林芝': {'code': '5207'}, '朔州': {'code': '3406'}, '日喀则': {'code': '5204'}, '马鞍山': {'code': '4105'}, '昭通': {'code': '5105'}, '临沧': {'code': '5108'}, '金门': {'code': '6107'}, '黔西南': {'code': '5006'}, '东莞': {'sublist': {'麻涌镇': '201108', '东城街道': '201103', '常平镇': '201107', '道滘镇': '201128', '东坑镇': '201120', '高埗镇': '201132', '石龙镇': '201106', '虎门镇': '201110', '沙田镇': '201127', '樟木头镇': '201109', '长安镇': '201112', '石碣镇': '201105', '松山湖管委会': '201133', '寮步镇': '201121', '大朗镇': '201122', '石排镇': '201115', '大岭山镇': '201126', '南城街道': '201102', '塘厦镇': '201113', '桥头镇': '201118', '虎门港管委会': '201134', '厚街镇': '201111', '望牛墩镇': '201130', '谢岗镇': '201119', '黄江镇': '201123', '清溪镇': '201124', '中堂镇': '201131', '茶山镇': '201114', '凤岗镇': '201125', '横沥镇': '201117', '洪梅镇': '201129', '万江街道': '201104', '东莞生态园': '201135', '企石镇': '201116', '莞城街道': '201101'}, 'code': '2011'}, '济宁': {'code': '4408'}, '博尔塔拉': {'code': '5706'}, '佛山': {'sublist': {'高明区': '201950', '禅城区': '201910', '三水区': '201940', '南海区': '201930', '顺德区': '201920'}, 'code': '2019'}, '晋中': {'code': '3409'}, '益阳': {'code': '4709'}, '三明': {'code': '4207'}, '荆州': {'code': '4609'}, '迪庆': {'code': '5116'}, '驻马店': {'code': '4515'}, '廊坊': {'code': '3310'}, '六盘水': {'code': '5002'}, '随州': {'code': '4612'}, '南投': {'code': '6109'}, '信阳': {'code': '4517'}, '河源': {'code': '2024'}, '三亚': {'code': '6402'}, '吉安': {'code': '4304'}, '忻州': {'code': '3407'}, '巢湖': {'code': '4115'}, '伊春': {'code': '3806'}, '昌都': {'code': '5202'}, '南宁': {'code': '4801'}, '山南': {'code': '5203'}, '来宾': {'code': '4813'}, '濮阳': {'code': '4509'}, '四平': {'code': '3703'}, '株洲': {'code': '4702'}, '菏泽': {'code': '4416'}, '巴彦淖尔': {'code': '3511'}, '天津': {'sublist': {'大港区': '3219', '和平': '3201', '宁河': '3214', '西青': '3208', '河东': '3202', '河北': '3205', '蓟县': '3216', '汉沽区': '3218', '塘沽区': '3217', '津南': '3209', '武清': '3211', '南开': '3204', '东丽': '3207', '静海': '3215', '红桥': '3206', '滨海': '3213', '河西': '3203', '宝坻': '3212', '北辰': '3210'}, 'code': '32'}, '海口': {'code': '6401'}, '郴州': {'code': '4710'}, '牡丹江': {'code': '3803'}, '嘉兴': {'code': '4007'}, '邢台': {'code': '3305'}, '长治': {'code': '3404'}, '永州': {'code': '4711'}, '阳江': {'code': '2030'}, '扬州': {'code': '3910'}, '泰州': {'code': '3912'}, '绥化': {'code': '3811'}, '长沙': {'code': '4701'}, '连云港': {'code': '3907'}, '苏州': {'code': '3903'}, '阿坝': {'code': '4919'}, '衡阳': {'code': '4704'}, '临汾': {'code': '3410'}, '杭州': {'code': '4001'}, '五指山': {'code': '6404'}, '基隆': {'code': '6106'}, '那曲': {'code': '5205'}, '黑河': {'code': '3812'}, '阳泉': {'code': '3403'}, '玉林': {'code': '4809'}, '大庆': {'code': '3805'}, '朝阳': {'code': '3613'}, '铜陵': {'code': '4107'}, '宣城': {'code': '4114'}, '泉州': {'code': '4204'}, '乌兰察布': {'code': '3509'}, '张家界': {'code': '4708'}, '辽源': {'code': '3704'}, '澎湖': {'code': '6110'}, '新余': {'code': '4310'}, '海东': {'code': '5502'}, '保山': {'code': '5104'}, '仙桃': {'code': '4614'}, '乐山': {'code': '4910'}, '海西': {'code': '5508'}, '芜湖': {'code': '4102'}, '温州': {'code': '4003'}, '大理': {'code': '5113'}, '台东': {'code': '6113'}, '崇左': {'code': '4814'}, '德州': {'code': '4413'}, '德宏': {'code': '5114'}, '宁德': {'code': '4209'}, '开封': {'code': '4502'}, '西安': {'code': '5301'}, '潍坊': {'code': '4407'}, '鄂尔多斯': {'code': '3510'}, '台北': {'code': '6112'}, '庆阳': {'code': '5410'}, '阜阳': {'code': '4110'}, '六安': {'code': '4113'}, '日照': {'code': '4411'}, '吉林': {'code': '3701'}, '连江': {'code': '6101'}, '青岛': {'code': '4402'}, '晋城': {'code': '3405'}, '儋州': {'code': '6406'}, '襄阳': {'code': '4605'}, '绍兴': {'code': '4005'}, '南京': {'code': '3901'}, '石嘴山': {'code': '5602'}, '五家渠': {'code': '5718'}}
    page_num = 1
    judge = 0
    total = 0
    job_save_rcrx = []
    flag_next = True
    xunhuan=0
    while flag_next:
        try:
            if xunhuan >10:
                flag_next=False
            try:
                Location=dict_num[cityName]['code']
            except:
                traceback.print_exc()
                flag_next = False
                pass
            if countyName != '':
                try:
                    county_jc=dict_city[cityName]['sublist'][countyName]
                    Location=county_jc
                except:
                    try:
                        county_Name = countyName.replace('区','')
                        county_jc = dict_city[cityName]['sublist'][county_Name]
                        Location = county_jc
                    except:
                        pass


            url_rcrx_zw = 'http://s.cjol.com/service/joblistjson.aspx?'
            form_data = {'KeywordType': '3',
                         'KeyWord': compName,
                         'Location': Location,
                         'SearchType': '3',
                         'ListType': '2',
                         'page': page_num}
            html_li_text = requests.post(url=url_rcrx_zw, headers=head_reqst(),data=form_data,proxies=proxies).text
            # print(html_li_text)
            print('rcrx----', html_li_text)
            dict_jl = json.loads(html_li_text)
            html_li = dict_jl['JobListHtml']
            sel = Selector(text=html_li)
            # 页码判断
            try:
                if len(sel.xpath('//body/div/ul')) < 40:
                    flag_next_zl = False
                else:
                    page_num = page_num + 1

                    if page_num > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                        flag_next_zl = False
            except:
                traceback.print_exc()
                break
            if 'JobListHtml' in html_li_text and html_li != "":
                for index, li in enumerate(sel.xpath('//body/div/ul')):
                    comp_name=li.xpath('string(li[3]/a/strong)').extract()[0].strip()
                    if comp_name == compName:
                        zw_rcrx_url=li.xpath('string(li[2]/h3/a/@href)').extract()[0].strip()
                        # print(index,zw_rcrx_url)
                        time.sleep(random.uniform(0.3, 0.6))
                        try:

                            rcrx_zw_text=xh_pd_req(pos_url=zw_rcrx_url,headers=head_reqst(),data='')
                            zw_data_rcrx = zwjx_rcrx(text=rcrx_zw_text, compName=compName)
                            zw_data_rcrx['type'] = 'job'
                            zw_data_rcrx['channel'] = channelid
                            zw_data_rcrx['companyName'] = compName
                            zw_data_rcrx['province'] = provName
                            zw_data_rcrx['city'] = cityName_0
                            zw_data_rcrx['county'] = countyName
                            print('rcrx-------', zw_data_rcrx)
                            job_save_rcrx.append(zw_data_rcrx)
                        except:
                            traceback.print_exc()
                            pass
                            if len(job_save_rcrx) == 3:
                                total = total + 3
                                data = json.dumps(job_save_rcrx)
                                data = data.encode('utf-8')
                                # requests.post(url=job_save_url, data=data)
                                logging.error('rcrx_jobl----3')
                                job_save_rcrx = []
                    if len(job_save_rcrx) == 3 or len(job_save_rcrx) == 0:
                        pass

                    else:
                        total = total + len(job_save_rcrx)
                        data = json.dumps(job_save_rcrx)
                        data = data.encode('utf-8')
                        # requests.post(url=job_save_url, data=data)
                        logging.error('rcrx_jobl----yfs')
            elif html_li == "":
                flag_next = False
        except:
            xunhuan=xunhuan+1
            traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_lgzw(compName, provName, cityName, countyName,cityName_0, channelid=13):
    page_num = 1
    judge = 0
    total = 0
    job_save_lg = []
    zw_url_id=[]
    flag_next = True
    xunhuan=0
    while flag_next:
        try:
            if xunhuan >10:
                flag_next=False
            try:
                d_pos = {"kw111": countyName,"city":cityName,'company':compName}
                postname = parse.urlencode(d_pos).encode('utf-8')
                count_name = str(postname).split('kw111=')[1][:-1].split('&')[0]
                city_name= str(postname).split('city=')[1][:-1].split('&')[0]
                company_name_str = str(postname).split('company=')[1][:-1].split('&')[0]
                # data = parse.urlencode(form_data).encode('utf-8')
            except:
                traceback.print_exc()
                flag_next = False
                pass
            url_sy = 'https://www.lagou.com/jobs/list_' + company_name_str + '?city=' + city_name + '&cl=false&fromSearch=true&labelWords=&suginput='
            url_lg_zw = 'https://www.lagou.com/jobs/positionAjax.json?city=' + city_name + '&district=' + count_name + '&needAddtionalResult=false'
            print('lg----', url_lg_zw)
            form_data = {'first': 'true', 'pn': page_num, 'kd': compName}
            time.sleep(random.uniform(3, 5))
            html_li_text =lg_get_cookie(url_sy,url_lg_zw, form_data)
            # print(html_li_text)
            print('lg----', html_li_text)
            dict_jl = json.loads(html_li_text)
            if page_num != 1 or dict_jl['success'] == True:
                if dict_jl['success'] == True:
                    result = dict_jl['content']['positionResult']['result']
                    for index, job_xq_text in enumerate(result):
                        if job_xq_text["companyShortName"] == compName:
                            pos_id=str(job_xq_text['positionId'])
                            zw_lg_url='http://www.lagou.com/jobs/'+ pos_id +'.html'
                            time.sleep(random.uniform(0.3, 0.6))
                            zw_url_id.append(pos_id)
                            # print(zw_lg_url)
                            try:
                                lg_zw_text=xh_pd_req(pos_url=zw_lg_url,headers=head_reqst(),data='')
                                zw_data_lg = zwjx_lg(text=job_xq_text, compName=compName,zw_data=lg_zw_text)
                                zw_data_lg['type'] = 'job'
                                zw_data_lg['channel'] = channelid
                                zw_data_lg['companyName'] = compName
                                zw_data_lg['province'] = provName
                                zw_data_lg['city'] = cityName_0
                                zw_data_lg['county'] = countyName
                                print('lg-------', zw_data_lg)
                                job_save_lg.append(zw_data_lg)
                            except:
                                traceback.print_exc()
                                pass

                            if len(job_save_lg) == 3:
                                total = total + 3
                                data = json.dumps(job_save_lg)
                                data = data.encode('utf-8')
                                requests.post(url=job_save_url, data=data)
                                logging.error('lg_jobl----3')
                                job_save_lg = []
                    if len(job_save_lg) == 3 or len(job_save_lg) == 0:
                        pass

                    else:
                        total = total + len(job_save_lg)
                        data = json.dumps(job_save_lg)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('lg_jobl----yfs')

                    if zw_url_id == []:
                        flag_next = False

                    if  result != []:
                        page_num = page_num + 1
                        if page_num > 30:
                            flag_next = False
                    else:
                        flag_next = False

                elif dict_jl['success'] == False :
                    flag_next = False

        except:
            xunhuan=xunhuan+1
            traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_qcrczw(compName, provName, cityName, countyName,cityName_0, channelid=15):
    dict_city={'岳阳': 'A1906', '芜湖': 'A1503', '资阳': 'A0919', '天津': 'A0500', '青岛': 'A1203', '柳州': 'A1404', '来宾': 'A1408', '佳木斯': 'A2208', '福州': 'A1102', '日喀则': 'A3003', '铜陵': 'A1508', '盐城': 'A0713', '黄冈': 'A1811', '神农架林区': 'A1817', '遵义': 'A2603', '石家庄': 'A1602', '定西': 'A2711', '酒泉': 'A2708', '石嘴山': 'A2903', '乌兰察布': 'A2810', '齐齐哈尔': 'A2206', '漯河': 'A1712', '抚顺': 'A2306', '东营': 'A1210', '昭通': 'A2512', '牡丹江': 'A2207', '揭阳': 'A0319', '本溪': 'A2310', '武威': 'A2706', '安庆': 'A1504', '贵港': 'A1412', '安康': 'A2010', '哈尔滨': 'A2202', '西宁': 'A3202', '韶关': 'A0309', '昆山': 'A0706', '阳江': 'A0325', '庆阳': 'A2710', '海口': 'A1002', '娄底': 'A1912', '基隆': 'A3503', '黔东南': 'A2609', '黔西南': 'A2608', '雅安': 'A0917', '重庆': 'A0600', '铜川': 'A2005', '荆门': 'A1808', '宣城': 'A1514', '运城': 'A2103', '拉萨': 'A3002', '宿州': 'A1518', '承德': 'A1608', '舟山': 'A0811', '镇江': 'A0710', '陇南': 'A2712', '毕节': 'A2607', '合肥': 'A1502', '鸡西': 'A2211', '玉溪': 'A2504', '防城港': 'A1406', '鄂州': 'A1810', '临夏回族自治州': 'A2713', '信阳': 'A1716', '荆州': 'A1807', '大庆': 'A2205', '桂林': 'A1403', '新余': 'A1312', '吉林': 'A2403', '鞍山': 'A2304', '溧水县': 'A0715', '清远': 'A0316', '河池': 'A1414', '商洛': 'A2011', '七台河 ': 'A2212', '伊春': 'A2203', '威海': 'A1206', '宜昌': 'A1803', '台北': 'A3501', '汕头': 'A0304', '常德': 'A1907', '汕尾': 'A0321', '营口': 'A2305', '玉林': 'A1411', '三亚': 'A1003', '湖北': 'A1800', '泰州': 'A0718', '延边朝鲜族自治州': 'A2410', '无锡': 'A0704', '大兴安岭地区': 'A2214', '渭南': 'A2008', '澳门': 'A3400', '凉山州': 'A0922', '随州': 'A1813', '喀什地区': 'A3104', '临沂': 'A1208', '杭州': 'A0802', '乌海': 'A2805', '红河州': 'A2510', '浙江': 'A0800', '济南': 'A1202', '四平': 'A2406', '南通': 'A0709', '襄阳': 'A1805', '乌鲁木齐': 'A3102', '河源': 'A0318', '吕梁': 'A2112', '怀化': 'A1911', '白山': 'A2407', '衡水': 'A1610', '乐山': 'A0904', '辽源': 'A2404', '吴忠': 'A2904', '宁德': 'A1109', '茂名': 'A0320', '宁夏': 'A2900', '丽水': 'A0810', '烟台': 'A1204', '淄博': 'A1207', '湘潭': 'A1904', '江西': 'A1300', '常熟': 'A0707', '嘉兴': 'A0807', '阿拉善盟': 'A2813', '潍坊': 'A1205', '增城': 'A0313', '梅州': 'A0323', '海北藏族自治州': 'A3204', '铜仁': 'A2606', '宿迁': 'A0719', '榆林': 'A2007', '鹰潭': 'A1308', '普洱': 'A2521', '大理': 'A2505', '滁州': 'A1509', '蒙自': 'A2507', '沧州': 'A1609', '通化': 'A2405', '阳泉': 'A2106', '池州': 'A1515', '银川': 'A2902', '安顺': 'A2605', '澳门特别行政区': 'A3401', '内蒙古': 'A2800', '临汾': 'A2105', '广西': 'A1400', '巢湖': 'A1513', '焦作': 'A1706', '德宏州': 'A2518', '北京': 'A0100', '嘉义': 'A3507', '潮州': 'A0317', '中山': 'A0307', '黑河': 'A2213', '鹤岗': 'A2209', '厦门': 'A1103', '海南': 'A1000', '崇左': 'A1407', '三门峡': 'A1713', '福建': 'A1100', '成都': 'A0902', '延安': 'A2006', '广东': 'A0300', '许昌': 'A1711', '莱芜': 'A1214', '三明': 'A1107', '张家口': 'A1612', '松原': 'A2408', '呼和浩特': 'A2802', '邢台': 'A1611', '高雄': 'A3505', '遂宁': 'A0912', '曲靖': 'A2503', '宜宾': 'A0907', '迪庆州': 'A2520', '湖州': 'A0809', '滨州 ': 'A1220', '新竹': 'A3506', '长治': 'A2107', '亳州': 'A1516', '兴安盟': 'A2812', '攀枝花': 'A0910', '抚州': 'A1311', '辽阳': 'A2311', '临沧': 'A2514', '江门': 'A0310', '湘西州': 'A1915', '青海': 'A3200', '泉州': 'A1104', '长春': 'A2402', '扬州': 'A0708', '西双版纳州': 'A2516', '南阳': 'A1714', '张家界': 'A1914', '西藏': 'A3000', '阜新 ': 'A2314', '吉安': 'A1310', '台州': 'A0808', '南京': 'A0702', '莆田': 'A1106', '九江': 'A1303', '阜阳': 'A1507', '南平': 'A1108', '锡林郭勒盟': 'A2811', '呼伦贝尔': 'A2808', '吴江': 'A0720', '商丘': 'A1715', '昆明': 'A2502', '秦皇岛': 'A1606', '克孜勒苏柯尔克自治州': 'A3105', '赤峰': 'A2803', '楚雄州': 'A2517', '葫芦岛': 'A2309', '甘南藏族自治州': 'A2714', '甘孜州': 'A0921', '鹤壁 ': 'A1707', '嘉峪关': 'A2715', '张家港': 'A0714', '巴中': 'A0918', '眉山': 'A0916', '固原 ': 'A2905', '黔南': 'A2610', '天门': 'A1816', '北海': 'A1405', '仙桃': 'A1815', '自贡': 'A0908', '怒江州': 'A2519', '周口': 'A1717', '鄂尔多斯': 'A2807', '甘肃': 'A2700', '六安': 'A1512', '白城': 'A2409', '宝鸡': 'A2004', '潜江': 'A1814', '衢州': 'A0812', '安阳': 'A1709', '泰安': 'A1211', '德州': 'A1213', '咸阳': 'A2003', '贵州': 'A2600', '阿坝州': 'A0920', '苏州': 'A0703', '朝阳': 'A2315', '张掖': 'A2707', '朔州': 'A2109', '金昌': 'A2703', '保定': 'A1604', '太原': 'A2102', '白银': 'A2704', '香港': 'A3300', '淮北': 'A1517', '通辽': 'A2806', '新乡': 'A1708', '云南': 'A2500', '郴州': 'A1909', '宁波': 'A0803', '丽江': 'A2506', '枣庄': 'A1215', '上饶': 'A1304', '高淳县': 'A0716', '山西': 'A2100', '果洛藏族自治州': 'A3207', '佛山': 'A0306', '文山州': 'A2515', '宜春': 'A1305', '郑州': 'A1702', '安徽': 'A1500', '香港特别行政区': 'A3301', '湘西土家族苗族自治州': 'A1916', '上海': 'A0200', '唐山': 'A1605', '东莞': 'A0308', '绥化': 'A2204', '驻马店': 'A1718', '深圳': 'A0311', '兰州': 'A2702', '孝感': 'A1809', '开封': 'A1704', '德阳': 'A0906', '思茅': 'A2513', '保山': 'A2511', '开远': 'A2508', '永州': 'A1913', '绍兴': 'A0805', '忻州': 'A2111', '湛江': 'A0314', '巴彦淖尔': 'A2809', '聊城': 'A1216', '江苏': 'A0700', '萍乡': 'A1307', '汉中': 'A2009', '日照': 'A1212', '广元': 'A0911', '济源': 'A1719', '咸宁': 'A1812', '中卫': 'A2906', '陕西': 'A2000', '包头': 'A2804', '淮南': 'A1511', '黄山': 'A1510', '温州': 'A0804', '四川': 'A0900', '黑龙江': 'A2200', '国外': 'A3600', '丹东': 'A2308', '钦州': 'A1415', '廊坊': 'A1603', '肇庆': 'A0315', '邯郸': 'A1607', '辽宁': 'A2300', '西安': 'A2002', '河南': 'A1700', '南宁': 'A1402', '杨凌示范区': 'A2012', '武汉': 'A1802', '恩施州': 'A1818', '洛阳': 'A1703', '克拉玛依': 'A3103', '内江': 'A0909', '淮安': 'A0717', '平顶山': 'A1705', '广州': 'A0302', '湖南': 'A1900', '漳州': 'A1105', '云浮': 'A0324', '济宁': 'A1209', '盘锦': 'A2313', '衡阳': 'A1905', '龙岩': 'A1110', '百色': 'A1413', '株洲': 'A1903', '锦州': 'A2307', '河北': 'A1600', '南昌': 'A1302', '马鞍山': 'A1505', '顺德': 'A0322', '铁岭': 'A2312', '金华': 'A0806', '菏泽': 'A1217', '晋城': 'A2108', '南充': 'A0913', '黄石': 'A1804', '山东': 'A1200', '泸州': 'A0905', '赣州': 'A1309', '十堰': 'A1806', '徐州': 'A0711', '台湾': 'A3500', '景德镇': 'A1306', '连云港': 'A0712', '台中': 'A3504', '濮阳': 'A1710', '六盘水': 'A2604', '大同': 'A2104', '达州': 'A0915', '双鸭山': 'A2210', '贵阳': 'A2602', '邵阳': 'A1910', '新疆': 'A3100', '大连': 'A2303', '益阳': 'A1908', '平凉': 'A2709', '个旧': 'A2509', '台南': 'A3502', '常州': 'A0705', '贺州': 'A1410', '晋中': 'A2110', '梧州': 'A1409', '绵阳': 'A0903', '珠海': 'A0305', '蚌埠': 'A1506', '长沙': 'A1902', '沈阳': 'A2302', '天水': 'A2705', '惠州': 'A0303', '广安': 'A0914'}
    flag_next_qcrc = True
    p = 1
    judge=0
    total = 0
    job_save_qcrc = []
    while flag_next_qcrc:
        try:
            jobs_url_li=[]
            try:
                com_num=dict_city[cityName]
            except:
                # traceback.print_exc()
                judge = 1
                break
            url_qcrc_zwss = "http://www.carjob.com.cn/public/"+com_num+"_T2_P"+str(p)+"/?"
            print("qcrc-------",url_qcrc_zwss)
            data_li = {'key_word': compName}
            try:
                html_li_text =xh_pd_req(pos_url=url_qcrc_zwss,data=data_li,headers=head_reqst())
            except:
                traceback.print_exc()
                break
            if '汽车人才网' in html_li_text:
                print("111")
                sel = Selector(text=html_li_text)
                for job_qcrc in sel.xpath('//ul[@class="result_list"]/li'):
                    job_qcrc_name = job_qcrc.xpath('string(div[@class="company"]/span/a)').extract()[0].strip()
                    if job_qcrc_name == compName:
                        job_qcrc_url ="http://www.carjob.com.cn"+job_qcrc.xpath('string(div[@class="position"]/div/span/a/@href)').extract()[0].strip()
                        # print(job_qcrc_url)
                        jobs_url_li.append(job_qcrc_url)

            # 判断是否进入下一页
                try:
                    if len(sel.xpath('//ul[@class="result_list"]/li')) < 30 or sel.xpath('//ul[@class="result_list"]/li')== []:
                        flag_next_qcrc = False
                    else:
                        p = p+1
                        if p > 30:  # 若总页数大于30页，默认进入了死循环，强制退出
                            flag_next_qcrc = False
                except:
                    traceback.print_exc()
                    logging.exception("Exception Logged")
                    flag_next_qcrc = False
                for job_url_1 in jobs_url_li:
                    print(job_url_1)
                    time.sleep(random.uniform(0.3, 0.6))
                    try:
                        job_qcrc_text = xh_pd_req(pos_url=job_url_1, data='', headers=head_reqst())
                        # job_qcrc_text=requests.get(url=job_url_1,headers=head_reqst()).text
                        zw_data_qcrc = zwjx_qcrc(text=job_qcrc_text, compName=compName)
                        zw_data_qcrc['type'] = 'job'
                        zw_data_qcrc['channel'] = channelid
                        zw_data_qcrc['companyName'] = compName
                        zw_data_qcrc['province'] = provName
                        zw_data_qcrc['city'] = cityName_0
                        zw_data_qcrc['county'] = countyName
                        print("qcrc---------", zw_data_qcrc)
                        job_save_qcrc.append(zw_data_qcrc)
                    except:
                        traceback.print_exc()
                        logging.exception("Exception Logged")
                        pass
                    if len(job_save_qcrc) == 3:
                        total = total + 3
                        data = json.dumps(job_save_qcrc)
                        data = data.encode('utf-8')
                        # requests.post(url=job_save_url, data=data)
                        logging.error('qcrc_jobl----3')
                        job_save_qcrc = []
                if len(job_save_qcrc) == 3 or len(job_save_qcrc) == 0:
                    pass
                else:
                    total = total + len(job_save_qcrc)
                    data = json.dumps(job_save_qcrc)
                    data = data.encode('utf-8')
                    # requests.post(url=job_save_url, data=data)
                    logging.error('qcrc_jobl----yfs')
            elif "" == html_li_text:
                flag_next_qcrc = False
        except:
            logging.exception("Exception Logged")
            traceback.print_exc()
            pass

    if total > 0:
        scrapy_state = [{'scrapy_state': 2, 'total': total, 'type': 'job', 'channel': channelid, 'companyName': compName,
                         'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total, 'message': '未能查询到数据', 'type': 'job', 'channel': channelid,
                             'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [
                {'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type': 'job', 'channel': channelid,
                 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_sxszw(compName, provName, cityName, countyName,cityName_0, channelid=16):
    city_sxs={'大庆': '230600', '厦门': '350200', '成都': '510100', '南昌': '360100', '郑州': '410100', '西安': '610100', '丽水': '331100', '无锡': '320200', '韶关': '440200', '湖州': '330500', '杭州': '330100', '南京': '320100', '泉州': '350500', '太原': '140100', '南宁': '450100', '天津': '120100', '宁波': '330200', '珠海': '440400', '沈阳': '210100', '兰州': '620100', '南通': '320600', '石家庄': '130100', '长沙': '430100', '合肥': '340100', '黄山': '341000', '香港': '810000', '贵阳': '520100', '青岛': '370200', '福州': '350100', '苏州': '320500', '丽江': '530700', '深圳': '440300', '长春': '220100', '大理': '532900', '哈尔滨': '230100', '济南': '370100', '大连': '210200', '重庆': '500100', '北京': '110100', '佛山': '440600', '海外': '888888', '温州': '330300', '海口': '460100', '上海': '310100', '广州': '440100', '武汉': '420100',}
    page_num = 1
    fan_ye = 0
    judge = 0
    total = 0
    job_save_sxs = []
    jobs_url_li = []
    job_linshi = []
    job_linshi_id = []
    flag_next = True
    panduan=0
    while flag_next:
        try:
            if panduan >10:
                flag_next = False
            try:
                d_pos = {"kw111": compName, "city": cityName}
                postname = parse.urlencode(d_pos).encode('utf-8')
                com_name = str(postname).split('kw111=')[1][:-1].split('&')[0]
                city_name = str(postname).split('city=')[1][:-1].split('&')[0]
                city_num = city_sxs[cityName]
            except:
                judge = 1
                traceback.print_exc()
                flag_next = False
                break
            url_zw="https://www.shixiseng.com/interns/st-intern_c-"+ city_num + "_?k=" + com_name +"&p="+ str(page_num)
            print('sxs-------',url_zw)
            html_li_text =handl_sxs_font(url_zw)
            # html_li_text=requests.get(url=url_zw, headers=head_reqst(),proxies=proxies).text
            if '实习僧' in html_li_text:
                sel = Selector(text=html_li_text)
                xpa_sxs_li = '//ul[@class="position-list"]/li'
                for job_sxs in sel.xpath(xpa_sxs_li):
                    sxs_name = job_sxs.xpath('div[@class="info1"]/div[@class="company-box"]/a/text()').extract()[0]
                    if sxs_name == compName:
                        sxs_url = job_sxs.xpath('div[@class="info1"]/div[@class="name-box clearfix"]/a/@href').extract()[0]
                        if "http" not in sxs_url:
                            sxs_url='https://www.shixiseng.com'+sxs_url
                            sxs_id = sxs_url.split("inn_")[1].strip()
                            # 如果链接为一条新的链接
                            if sxs_id not in job_linshi:
                                fan_ye = 1
                                jobs_url_li.append(sxs_url)
                                job_linshi.append(sxs_id)
                                job_linshi_id.append(sxs_id)
                            else:
                                fan_ye = 0
                                flag_next = False

                # 判断是否进入下一页
                try:
                    if fan_ye != 0 and job_linshi_id != []:
                        page_num = page_num + 1
                        if page_num > 50:
                            flag_next = False
                    else:
                        flag_next = False
                    job_linshi_id = []
                except:
                    flag_next = False
                    pass
        except:
            panduan= panduan+1
            logging.exception("Exception Logged")
            traceback.print_exc()
            pass
        try:
            for index, sxs_url1 in enumerate(jobs_url_li):
                # print(index)
                time.sleep(random.uniform(0.3, 0.6))
                try:
                    # request_job_xq = request.Request(url=sxs_url1, headers=head_reqst())
                    # response_job_xq = request.urlopen(request_job_xq).read()
                    # job_xq_text = response_job_xq.decode('utf-8', errors='ignore')
                    # com=Selector(text=job_xq_text)
                    # com_name=com.xpath('string(//div[@class="job_com_name"])').extract()[0].strip()
                    # if com_name == compName:
                    try:
                        job_xq_text = handl_sxs_font(sxs_url1)
                        zw_data_sxs = zwjx_sxs(text=job_xq_text, compName=compName)
                        zw_data_sxs['type'] = 'job'
                        zw_data_sxs['channel'] = channelid
                        zw_data_sxs['companyName'] = compName
                        zw_data_sxs['province'] = provName
                        zw_data_sxs['city'] = cityName_0
                        zw_data_sxs['county'] = countyName
                        print('sxs-------', zw_data_sxs)
                        job_save_sxs.append(zw_data_sxs)
                    except:
                        logging.exception("Exception Logged")
                        sj_str = str(int(time.time() * 1000))
                        logging.error('sxs_job_jx_fail----' + sj_str)
                    if len(job_save_sxs) == 3:
                        total=total+3
                        data = json.dumps(job_save_sxs)
                        data = data.encode('utf-8')
                        requests.post(url=job_save_url, data=data)
                        logging.error('sxs_jobl----3')
                        job_save_sxs = []
                except:
                    traceback.print_exc()
                    logging.exception("Exception Logged")
                    pass
            if len(job_save_sxs) == 3 or len(job_save_sxs) == 0:
                pass
            else:
                total = total + len(job_save_sxs)
                data = json.dumps(job_save_sxs)
                data = data.encode('utf-8')
                requests.post(url=job_save_url, data=data)
                logging.error('sxs_jobl----yfs')
            jobs_url_li = []

        except:
            logging.exception("Exception Logged")
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
    print('爬取完成')
def get_mmzw(compName, provName, cityName, countyName,cityName_0, channelid=17):
    job_save_mm=[]
    pn = 0
    judge = 0
    total = 0
    flag_next = True
    while flag_next:
        try:
            time.sleep(1)
            query="脉脉+"+compName
            url_mm_zwss = "http://zhaopin.baidu.com/api/qzasync?"
            fam_data = {"query":query,"city": cityName,"pn": str(pn),"rn": '10',"pcmod": '1',}
            try:
                html_li_text=xh_pd_req(pos_url=url_mm_zwss,data=fam_data,headers=head_reqst())
                dict_jl = json.loads(html_li_text)
                print("mm-------",html_li_text)
            except:
                # traceback.print_exc()
                flag_next = False
                break
            if  dict_jl['status'] == 0:
                result = dict_jl['data']['disp_data']
                for index, job_xq_text in enumerate(result):
                    if job_xq_text["company"].strip() == compName:
                        wapurl = str(job_xq_text['wapurl'])
                        zw_mm_url = 'http://zhaopin.baidu.com/szzw?'
                        data_f={'id':wapurl}
                        time.sleep(random.uniform(0.3, 0.6))
                        # print(zw_mm_url)
                        try:
                            mm_zw_text = xh_pd_req(pos_url=zw_mm_url, headers=head_reqst(), data=data_f)
                            zw_data_mm = zwjx_mm(text=job_xq_text, compName=compName, zw_data=mm_zw_text)
                            zw_data_mm['type'] = 'job'
                            zw_data_mm['channel'] = channelid
                            zw_data_mm['companyName'] = compName
                            zw_data_mm['province'] = provName
                            zw_data_mm['city'] = cityName_0
                            zw_data_mm['county'] = countyName
                            print('mm-------', zw_data_mm)
                            job_save_mm.append(zw_data_mm)
                        except:
                            traceback.print_exc()
                            pass
                        if len(job_save_mm) == 3:
                            total = total + 3
                            data = json.dumps(job_save_mm)
                            data = data.encode('utf-8')
                            requests.post(url=job_save_url, data=data)
                            logging.error('mm_jobl----3')
                            job_save_mm = []
                if len(job_save_mm) == 3 or len(job_save_mm) == 0:
                    pass

                else:
                    total = total + len(job_save_mm)
                    data = json.dumps(job_save_mm)
                    data = data.encode('utf-8')
                    requests.post(url=job_save_url, data=data)
                    logging.error('mm_jobl----yfs')

            elif dict_jl['status'] != 0:
                flag_next = False
            #判断是否进入下一页
            try:
                if len(result) < 10:
                    flag_next = False
                else:
                    # print("开始爬取第%s页"%page_number)
                    pn = pn + 10
                    if pn > 300:  # 若总页数大于30页，默认进入了死循环，强制退出
                        flag_next = False
            except:
                traceback.print_exc()
                logging.exception("Exception Logged")
                flag_next = False

        except:
            logging.exception("Exception Logged")
            traceback.print_exc()
            pass
    if total > 0:
        scrapy_state = [{'scrapy_state': 2,'total': total, 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
        data = json.dumps(scrapy_state)
        data = data.encode('utf-8')
        requests.post(url=job_save_url, data=data)
    elif total == 0:
        if judge == 0:
            scrapy_state = [{'scrapy_state': 3, 'total': total,'message':'未能查询到数据', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif judge == 1:
            scrapy_state = [{'scrapy_state': 4, 'total': total, 'message': '该渠道不支持此城市的职位查询', 'type':'job','channel': channelid, 'companyName': compName, 'province': provName, 'county': countyName, 'city': cityName_0}]
            data = json.dumps(scrapy_state)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)

    print('爬取完成')

def run(page):
    get_data_dic=page
    if get_data_dic['type'] == 'job':
        compName = get_data_dic['companyName'].strip()
        provName = get_data_dic['province'].strip()
        countyName = get_data_dic['county'].strip()
        cityName = get_data_dic['city'].replace("市", '').strip()
        cityName_0 = get_data_dic['city'].strip()
        if int(get_data_dic['channel']) == 1:
            get_zlzw(compName, provName, cityName, countyName,cityName_0, channelid=1)
        elif int(get_data_dic['channel']) == 2:
            get_qczw(compName, provName, cityName, countyName,cityName_0, channelid=2)
        elif int(get_data_dic['channel']) == 3:
            get_58zw(compName, provName, cityName, countyName,cityName_0, channelid=3)
        elif int(get_data_dic['channel']) == 4:
            get_gjzw(compName, provName, cityName, countyName,cityName_0, channelid=4)
        elif int(get_data_dic['channel']) == 5:
            get_hzrczw(compName, provName, cityName, countyName,cityName_0, channelid=5)
        elif int(get_data_dic['channel']) == 6:
            get_zhyczw(compName, provName, cityName, countyName,cityName_0, channelid=6)
        elif int(get_data_dic['channel']) == 7:
            get_djzw(compName, provName, cityName, countyName,cityName_0, channelid=7)
        elif int(get_data_dic['channel']) == 8:
            get_zpzw(compName, provName, cityName, countyName,cityName_0, channelid=8)
        elif int(get_data_dic['channel']) == 10:
            get_lpzw(compName, provName, cityName, countyName,cityName_0, channelid=10)
        elif int(get_data_dic['channel']) == 12:
            get_rcrxzw(compName, provName, cityName, countyName,cityName_0, channelid=12)
        elif int(get_data_dic['channel']) == 13:
            get_lgzw(compName, provName, cityName, countyName,cityName_0, channelid=13)
        elif int(get_data_dic['channel']) == 15:
            get_qcrczw(compName, provName, cityName, countyName,cityName_0, channelid=15)
        elif int(get_data_dic['channel']) == 16:
            get_sxszw(compName, provName, cityName, countyName,cityName_0, channelid=16)
        elif int(get_data_dic['channel']) == 17:
            get_mmzw(compName, provName, cityName, countyName,cityName_0, channelid=17)


# get_mmzw('阿里巴巴','','杭州','','')
# get_rcrxzw('深圳市中联华成数字技术有限公司','','深圳','','')
# get_qcrczw('深圳市顺和盈汽车贸易有限公司','','深圳','','')
# get_ntzw('搜狐','','北京','','')

"""
服务器端
"""


host_name = socket.gethostname()
print("hostname:%s" % host_name)
print("IP address: %s" % socket.gethostbyname(host_name))
sock = socket.socket()  # 生成socket对象
sock.bind(('192.168.1.191', 8001))  # 绑定主机ip和端口号
# sock.bind(('172.16.53.108', 8001))  # 绑定主机ip和端口号
# sock.bind(('localhost', 8001))                          # 绑定localhost可以
sock.listen(5000)
data_fi={"state":1}
data = json.dumps(data_fi)
data = data.encode('utf-8')

while True:
    time.sleep(1)
    connection, addr = sock.accept()  # 接受客户端的连接
    try:
        connection.settimeout(1)
        get_1 = connection.recv(2048)
        print(111, get_1)
        try:
            get_1 = base64.b64decode(get_1)
            print(222, get_1)
        except:
            traceback.print_exc()
            pass
        try:
            get_1 = get_1.decode('utf-8', errors='ignore')
            print(333, get_1)
        except:
            traceback.print_exc()
            pass
        try:
            get_data = json.loads(get_1)
            print(444, get_data)
        except:
            traceback.print_exc()
            pass
        logging.error('接收请求:{}'.format(get_data))
        connection.send(data)  # 向客户端发送一个字符串信息
        connection.close()
        # 原来的
        # get_1 = connection.recv(1024).decode('utf-8', errors='ignore')
        # get_data = json.loads(get_1)
        # connection.send(data)  # 向客户端发送一个字符串信息
        # connection.close()
        print('发送完成')

        myqueue = queue.Queue()
        myqueue.put(get_data)

        while not myqueue.empty():
            if threading.activeCount() < 6:
                th_1 = threading.Thread(target=run, args=(myqueue.get(),))
                th_1.start()
                print(threading.activeCount())

    # except socket.timeout:                             # 如果出现超时
    #     print('time out')
    except:
        traceback.print_exc()
        # connection.close()







