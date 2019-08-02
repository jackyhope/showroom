#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy import Selector
import traceback
import urllib.request
from fontTools.ttLib import TTFont
import shutil
import requests
from lxml import etree
import json
import datetime
import re
import time
import logging
import urllib.request
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

wu_jl_url = RESUME_DOWNLOAD_URL
wu_jlxw_url = SEARCH_STATUS_URL


def jx_58(text_58, job_id='', org_id='111', lx=0, channel_id='', dt=''):
    # driver.get(url_58)
    sel = Selector(text=text_58)
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    data_58_ss_sjx = {}
    data_58_ss_sjx['info'] = {}
    xpath_name = '//span[@id="name"]/text()'
    xpath_sex = '//span[@class="sex stonefont"]/text()'
    xpath_aage = '//span[@class="age stonefont"]/text()'
    xpath_degree = '//span[@class="edu stonefont"]/text()'
    xpath_work_year = '//div[@class="base-detail"]/span[@class="stonefont"]/text()'
    xpath_salary = '//span[@class="title" and contains(text(),"期望薪资：")]/parent::p[@class="stonefont"]/text()'
    try:
        re_phone = r'"phoneProtect":.*?"number":"(\d{11})"'
        patt_phone = re.compile(re_phone)
        phone_li = patt_phone.findall(text_58)
        data_58_ss_sjx['info']['mobilephone'] = phone_li[0]
    except:
        pass


    data_58_ss_sjx['info']['name'] = sel.xpath(xpath_name).extract()[0].strip()
    data_58_ss_sjx['info']['sex'] = sel.xpath(xpath_sex).extract()[0].strip()
    birth_str = sel.xpath(xpath_aage).extract()[0].strip()
    data_58_ss_sjx['info']['birth_year'] = int(now_year) - int(birth_str.split('岁')[0])
    data_58_ss_sjx['info']['degree'] = sel.xpath(xpath_degree).extract()[0].strip()
    wy_str = sel.xpath(xpath_work_year).extract()[0].strip()
    if '-' in wy_str:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year) - int(wy_str.split('年')[0].split('-')[1])
    # 一年以下工作经验
    elif '以下' in wy_str:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year) - 1
    # 10年以上
    elif '以上' in wy_str:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year) - 10
    # 无经验、应届生
    else:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year)
    salary_str = sel.xpath(xpath_salary).extract()[0].strip()
    if '-' in salary_str:
        data_58_ss_sjx['objective']['expected_salary_lower'] = wy_str.split('元')[0].split('-')[0]
        data_58_ss_sjx['objective']['expected_salary_upper'] = wy_str.split('元')[0].split('-')[1]
    elif '面议' in salary_str:
        data_58_ss_sjx['objective']['expected_salary_lower'] = 0
        data_58_ss_sjx['objective']['expected_salary_upper'] = 0
    else:
        # 1000以下
        if '以下' in salary_str:
            data_58_ss_sjx['objective']['expected_salary_lower'] = 1000
            data_58_ss_sjx['objective']['expected_salary_upper'] = 1000
        #  25000以上
        elif '以上' in salary_str:
            data_58_ss_sjx['objective']['expected_salary_lower'] = 25000
            data_58_ss_sjx['objective']['expected_salary_upper'] = 25000

    data_58_ss_sjx['objective'] = {}

    re_jlid = r'"bizId":(\d+)'
    patt_jlid = re.compile(re_jlid)
    jlid_li = patt_jlid.findall(text_58)
    if jlid_li[0] != '0':
        data_58_ss_sjx['info']['channel_resume_id'] = jlid_li[0]
    else:
        if channel_id:
            data_58_ss_sjx['info']['channel_resume_id'] = channel_id

    # data_58_ss_sjx['info']['channel_resume_id'] = driver.current_url.split('https://jianli.58.com/resumedetail/singles/')[1].split('?')[0]
    # print(1111111, data_58_ss_sjx['info']['channel_resume_id'])
    data_58_ss_sjx['info']['photo_url'] = sel.xpath('//div[@class="basicInfo"]/div[@class="headFigure"]/img/@src').extract()[0]

    if dt:
        data_58_ss_sjx['info']['channel_update_time'] = dt
    data_58_ss_sjx['info']['channel'] = 3
    # 户籍
    if sel.xpath('//div[@class="base-detail"]/span[9]'):
        if '现居' in sel.xpath('//div[@class="base-detail"]/span[9]/text()').extract()[0]:
            data_58_ss_sjx['info']['current_address'] = \
            sel.xpath('//div[@class="base-detail"]/span[9]/text()').extract()[0].replace('现居', '')
        else:
            data_58_ss_sjx['info']['residence_address'] = \
            sel.xpath('//div[@class="base-detail"]/span[9]/text()').extract()[0].replace('人', '')
            # print(data_58_ss_sjx['info']['residence_address'])
    # 现在居住地
    if sel.xpath('//div[@class="base-detail"]/span[11]'):
        data_58_ss_sjx['info']['current_address'] = sel.xpath('//div[@class="base-detail"]/span[11]/text()').extract()[
            0].replace('现居', '')
        # print(data_58_ss_sjx['info']['current_address'])
    # 高亮最上方标签
    if sel.xpath('//ul[@class="highLights"]/li'):
        data_58_ss_sjx['objective']['individual_label'] = []
        for bq in sel.xpath('//ul[@class="highLights"]/li'):
            data_58_ss_sjx['objective']['individual_label'].append(bq.xpath('text()').extract()[0])
        # print(data_58_ss_sjx['objective']['individual_label'])
    # 工作状态
    data_58_ss_sjx['objective']['work_status'] = sel.xpath('//div[@id="Job-status"]/text()').extract()[0].strip()
    # print(data_58_ss_sjx['objective']['work_status'])
    # 求职名称
    data_58_ss_sjx['objective']['expected_job_title'] = sel.xpath('//div[@id="expectJob"]/text()').extract()[0].split('、（')[0].strip().split('、')
    # 期望工作地点
    data_58_ss_sjx['objective']['expected_address'] = sel.xpath('//div[@id="expectLocation"]/text()').extract()[0].split('、（')[0].strip().split('、')

    # 工作经历
    data_58_ss_sjx['jobs'] = []

    if sel.xpath('//div[@class="work experience"]/div[@class="experience-detail"]'):
        for work in sel.xpath('//div[@class="work experience"]/div[@class="experience-detail"]'):
            job = {}
            job['company'] = work.xpath('div[@class="itemName"]/text()').extract()[0]
            text_wk = work.xpath('string(div[@class="project-content"])').extract()[0].strip()
            if '工作时间' in text_wk:
                gzsj = text_wk.split('工作时间：')[1].split('薪资水平：')[0].split('在职职位：')[0].split('工作职责：')[0].strip()
                if '至今' not in gzsj:
                    job['during_start'] = gzsj.split('-')[0].replace('年', '-').replace('月', '-') + '01'
                    job['during_end'] = gzsj.split('-')[1].split('（')[0].replace('年', '-').replace('月', '-') + '01'
                else:
                    job['during_start'] = gzsj.split('-')[0].replace('年', '-').replace('月', '-') + '01'
                    job['during_end'] = '9999-01-01'
            if '薪资水平' in text_wk:
                job_xz = text_wk.split('薪资水平：')[1].split('工作时间：')[0].split('在职职位：')[0].split('工作职责：')[0].strip()
                if '以下' in job_xz:
                    job['monthly_salary_lower'] = 1000
                    job['monthly_salary_upper'] = 1000
                elif '以上' in job_xz:
                    job['monthly_salary_lower'] = 25000
                    job['monthly_salary_upper'] = 25000
                elif '-' in job_xz:
                    job['monthly_salary_lower'] = int(job_xz.split('-')[0])
                    job['monthly_salary_upper'] = int(job_xz.split('-')[1])
                else:
                    pass
                    # job['monthly_salary_lower'] = 0
                    # job['monthly_salary_upper'] = 0
            if '在职职位' in text_wk:
                job['job_title'] = text_wk.split('在职职位：')[1].split('工作时间：')[0].split('薪资水平：')[0].split('工作职责：')[
                    0].strip()
            if '工作职责' in text_wk:
                job['job_content'] = text_wk.split('工作职责：')[1].split('在职职位：')[0].split('工作时间：')[0].split('薪资水平：')[
                    0].strip()
            data_58_ss_sjx['jobs'].append(job)
        # print(data_58_ss_sjx['jobs'])

    # 教育经历
    data_58_ss_sjx['educations'] = []

    if sel.xpath('//div[@class="education experience"]'):
        for jy in sel.xpath('//div[@class="education experience"]/div[@class="edu-detail"]'):
            edu = {}
            edu['school'] = jy.xpath('div/span[1]/text()').extract()[0].strip()
            if '月毕业' in jy.xpath('div/span[3]/text()').extract()[0]:
                edu['during_end'] = jy.xpath('div/span[3]/text()').extract()[0].strip().split('月毕业')[0].replace('年',
                                                                                                                '-') + '-01'
            else:
                edu['during_end'] = '9999-01-01'
            edu['major'] = jy.xpath('div[@class="item-content"]/span[@class="professional"]/text()').extract()[
                0].strip()
            data_58_ss_sjx['educations'].append(edu)
        # print(data_58_ss_sjx['educations'])

    # 技能语言
    data_58_ss_sjx['languages'] = []
    # 语言
    if sel.xpath('//div[@class="language experience"]'):
        for la in sel.xpath('//div[@class="language experience"]/div[@class="edu-detail"]'):
            lang = {}
            all_text = la.xpath('string(div[@class="item-content"])').extract()[0].strip()
            lang['language'] = all_text.split('： ')[0]
            lang_text1 = all_text.split('： ')[1].split('| ')[0]
            lang_text2 = all_text.split('： ')[1].split('| ')[1]
            lang_len = len(all_text.split('： ')[1].split('| '))
            if lang_len == 3:
                lang['level'] = all_text.split('： ')[1].split('| ')[2]
            if '听' in lang_text1:
                lang['speaking'] = lang_text1.replace('听说', '')
                lang['writing'] = lang_text2.replace('读写', '')
            else:
                lang['speaking'] = lang_text2.replace('听说', '')
                lang['writing'] = lang_text1.replace('读写', '')
            data_58_ss_sjx['languages'].append(lang)
    # 技能
    if sel.xpath('//div[@class="skillList experience"]'):
        for jn in sel.xpath('//div[@class="skillList experience"]/div[@class="certificate-item"]'):
            skill = {}
            skill['skill'] = jn.xpath('span[1]/text()').extract()[0]
            skill['duration'] = jn.xpath('span[3]/text()').extract()[0].split('（')[1].split('）')[0].strip()
            skill['level'] = jn.xpath('span[3]/text()').extract()[0].split('（')[0].strip()
            data_58_ss_sjx['languages'].append(skill)
        # print(data_58_ss_sjx['languages'])
    # 自我评价
    if sel.xpath('//div[@class="aboutMe experience"]'):
        text_me = sel.xpath('string(//div[@class="aboutMe experience"]/div[@class="edu-detail"])').extract()[0].strip()
        data_58_ss_sjx['objective']['self_evaluation'] = text_me
        # print(data_58_ss_sjx['objective']['self_evaluation'])

    # 项目经验
    data_58_ss_sjx['projects'] = []

    if sel.xpath('//div[@class="project experience"]'):
        for pro in sel.xpath('//div[@class="project experience"]/div[@class="experience-detail"]'):
            pro_dic = {}
            pro_dic['title'] = pro.xpath('div[@class="itemName"]/text()').extract()[0]
            pro_text = pro.xpath('string(div[@class="project-content"])').extract()[0].strip()
            xmsj = pro_text.split('项目时间：')[1].split('项目简介：')[0].split('项目业绩：')[0]
            if '至今' not in xmsj:
                pro_dic['during_start'] = xmsj.split('-')[0].strip().replace('年', '-').replace('月', '-') + '01'
                pro_dic['during_end'] = xmsj.split('-')[1].strip().replace('年', '-').replace('月', '-') + '01'
            else:
                pro_dic['during_start'] = xmsj.split('-')[0].strip().replace('年', '-').replace('月', '-') + '01'
                pro_dic['during_end'] = '9999-01-01'
            pro_dic['description'] = pro_text.split('项目简介：')[1].split('项目时间：')[0].split('项目业绩：')[0].strip()
            pro_dic['duty'] = pro_text.split('项目业绩：')[1].split('项目时间：')[0].split('项目简介：')[0].strip()
            data_58_ss_sjx['projects'].append(pro_dic)
        # print(data_58_ss_sjx['projects'])

    # 证书
    data_58_ss_sjx['credentials'] = []

    if sel.xpath('//div[@class="medal experience"]'):
        for zs in sel.xpath('//div[@class="medal experience"]/div[@class="certificate-item"]'):
            zs_dic = {}
            zs_dic['title'] = zs.xpath('span[@class="certificate-name auto_hidden"]/text()').extract()[0].strip()
            zs_dic['get_date'] = zs.xpath('span[@class="certificate-time"]/text()').extract()[0].strip().replace('年',
                                                                                                                 '-').replace(
                '月', '-') + '01'
            data_58_ss_sjx['credentials'].append(zs_dic)
        # print(data_58_ss_sjx['credentials'])

    # 在校情况
    data_58_ss_sjx['at_schools'] = []
    if sel.xpath('//div[@class="school experience"]'):
        for sch in sel.xpath('//div[@class="school experience"]/div[@class="experience-detail"]'):
            sch_dic = {}
            for sch_con in sch.xpath('div[@class="project-content"]/div[@class="title-content"]'):
                if '获奖学金' in sch_con.xpath('div[@class="item-title"]/text()').extract()[0].strip():
                    sch_dic['scholarship'] = sch_con.xpath('string(div[@class="item-content"])').extract()[0].strip()
                if '活动奖项' in sch_con.xpath('div[@class="item-title"]/text()').extract()[0].strip():
                    sch_dic['prize'] = \
                    sch_con.xpath('string(div[@class="item-content"]/p[@class="award-name"])').extract()[0].strip()
                if '校内职务' in sch_con.xpath('div[@class="item-title"]/text()').extract()[0].strip():
                    sch_dic['campus_post'] = \
                    sch_con.xpath('string(div[@class="item-content"]/p[@class="job"])').extract()[0].strip()
            data_58_ss_sjx['at_schools'].append(sch_dic)
        # print(data_58_ss_sjx['at_schools'])
    # 培训经历----没找到
    data_58_ss_sjx['trainings'] = []
    data_58_ss_sjx['org'] = {}
    try:
        if sel.xpath('//div[@id="divHead"]/table/tbody/tr[1]/td[1]/span[3]/text()').extract()[0]:
            data_58_ss_sjx['org']['receive_time'] = \
            sel.xpath('//div[@id="divHead"]/table/tbody/tr[1]/td[1]/span[3]/text()').extract()[0]
    except:
        pass


    data_58_ss_sjx['org']['org_id'] = org_id
    data_58_ss_sjx['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 插件
    if lx == 3:
        data_58_ss_sjx['org']['resume_type'] = 3
    # 收件箱
    elif lx == 1:
        data_58_ss_sjx['org']['resume_type'] = 1
    # 搜索/推荐
    elif lx == 2:
        data_58_ss_sjx['org']['resume_type'] = 2
    if job_id:
        data_58_ss_sjx['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    try:
        if data_58_ss_sjx['info']['mobilephone']:
            data_58_ss_sjx['org']['download_status'] = 1
    except:
        data_58_ss_sjx['org']['download_status'] = 0
    if dt:
        data_58_ss_sjx['org']['delivery_time'] = dt
    # print(data_58_ss_sjx)
    return data_58_ss_sjx


class Module_58(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_58, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'User-Agent': get_useragent(),
        }
        self.driver_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'phantomjs.exe'

    def parse_font_xml_58(self, font_xml_file):
        xml = etree.parse(font_xml_file)
        root = xml.getroot()
        font_dict = {}
        all_data = root.xpath('//glyf/TTGlyph')
        for index, data in enumerate(all_data):
            font_key = data.attrib.get('name')[3:].lower()
            contour_list = []
            if index == 0:
                continue
            for contour in data:
                for pt in contour:
                    contour_list.append(dict(pt.attrib))
            font_dict[font_key] = json.dumps(contour_list, sort_keys=True)
        return font_dict

    def handl_58_font(self, url):
        xz_font_file = True
        retry_t = 0
        while xz_font_file:
            r = self.session.get(url)
            r.encoding = 'utf-8'
            text = r.text
            # print(r.text)
            fontfile = str(time.time()*10000).split('.')[0]
            file_path = os.getcwd() + os.sep + 'Mod_pyth' + os.sep + fontfile
            # print(file_path)
            if not os.path.exists(file_path):
                # print('文件夹', file_path, '不存在，重新建立')
                # os.mkdir(file_path)
                os.makedirs(file_path)
            else:
                shutil.rmtree(file_path)
                os.makedirs(file_path)
            sel = Selector(text=text)
            # print(text)
            stonefont_url = sel.xpath('//style[not(@*)]').extract()[0]
            # print(999, stonefont_url)
            file_name = file_path + os.sep + 'all.txt'
            # 把字体文件的下载链接保存在本地
            try:
                with open(file_name, 'a+') as f:
                    if '.eot' in stonefont_url:
                        continue
                    elif 'data:application/font-woff' in stonefont_url:
                        stonefont_url = stonefont_url.split('font-family:"customfont"; src:url(')[1].split(')')[0]
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
                    font_dic = self.parse_font_xml_58(fontxml_name)
                    # print(font_dic)
                    # print(len(font_dic))
                    final_font_dic = {}
                    for font_dic_k, font_dic_v in font_dic.items():
                        # print(font_dic_k)
                        font_dic_v_li = json.loads(font_dic_v)
                        # print(font_dic_v_li)
                        # print(type(font_dic_v_li))
                        font_diff_num = 0
                        for pos_x_y_on in font_dic_v_li[:-1]:
                            pos_x = int(pos_x_y_on['x'])
                            pos_y = int(pos_x_y_on['y'])
                            pos_on = int(pos_x_y_on['on'])
                            font_diff_num = font_diff_num + (pos_x + pos_y) * pos_on
                        final_font_dic[font_dic_k] = font_diff_num

                    font_dic_58 = {16094: '5', 17040: '2', 49364: '生', 27549: '士', 79010: '硕', 70232: '高', 50789: '应',
                                   77541: '验', 16100: 'E', 72807: '杨', 143069: '博', 20662: '6', 75136: '赵', 23315: '3',
                                   25190: '下', 11305: '8', 37669: 'M', 36126: '女', 49804: '吴', 54816: '刘', 18005: '9',
                                   69688: '男', 18441: '4', 19321: 'A', 8799: '7', 88359: '校', 67790: '张', 107409: '黄',
                                   27285: '大', 83428: '技', 9985: '1', 66538: '经', 53319: '专', 86743: '陈', 68703: '周',
                                   24532: 'B', 65992: '李', 37621: '以', 73616: '科', 41369: '中', 34485: '王', 44164: '本',
                                   47827: '无', 67933: '届', 10966: '0'}
                    re_font = r"&#x([0-9a-f]+?);"
                    pattern_font = re.compile(re_font)
                    font_code_set = set(pattern_font.findall(text))
                    for font_code in font_code_set:
                        sub_before = "&#x" + font_code + ";"
                        text = text.replace(sub_before, font_dic_58[final_font_dic[font_code]])
                    # print(text)
                    return text
            except:
                shutil.rmtree(file_path)
                traceback.print_exc()
                time.sleep(random.uniform(3, 5))
                retry_t = retry_t + 1
                if retry_t >= 10:
                    xz_font_file = False
    # 登录状态判断
    def login_judge_58(self):
        home_url = 'https://employer.58.com/index/resourcechart'
        response_zy = self.session.get(url=home_url, headers=self.headers)
        response_zy = response_zy.text
        try:
            resp_dic = {}
            re_jpzwd = r'"jingpin":.+?"openVipReamin":"(\d+?)"'
            patt_jpzwd = re.compile(re_jpzwd)
            jpzwd_li = patt_jpzwd.findall(response_zy)
            resp_dic['jpzwd'] = jpzwd_li[0]

            re_jld = r'"resume":.+?"localResumeReamin":"(\d+?)"'
            patt_jld = re.compile(re_jld)
            jld_li = patt_jld.findall(response_zy)
            resp_dic['bdjld'] = jld_li[0]

            re_jld = r'"resume":.+?"normalResumeReamin":"(\d+?)"'
            patt_jld = re.compile(re_jld)
            jld_li = patt_jld.findall(response_zy)
            resp_dic['qgjld'] = jld_li[0]

            re_gjsxd = r'"newshuaxin":.+?"remainCount":"(\d+?)"'
            patt_gjsxd = re.compile(re_gjsxd)
            gjsxd_li = patt_gjsxd.findall(response_zy)
            resp_dic['gjsxd'] = gjsxd_li[0]
            # print(response_zy)
            # print(resp_dic)
            return resp_dic
        except:
            return None
    # 职位刷新-----仅支持精品职位刷新
    def refresh_job_58(self, JobID):
        get_useid_url = 'https://employer.58.com/operatelog/accountselect'
        resp_useid = self.session.get(url=get_useid_url)
        re_userid = r'"userID":"(\d+?)"'
        patt_userid = re.compile(re_userid)
        useid_58 = patt_userid.findall(resp_useid.text)
        # print(useid_58[0])
        refresh_url = 'https://zprefresh.vip.58.com/jingpinrefresh/dorefresh?infoIds=' + JobID + '&source=3&userId=' + useid_58[0]
        rf_result = self.session.get(url=refresh_url)
        rf_result_dic = json.loads(rf_result.text)
        # rf_result_dic = json.loads('{"resultMsg":{"errorCode":1002,"errorFlag":true,"msg":"通过规则校验！"},"refreshEntityList":[{"count":0,"days":0,"errorCode":1000,"errorMsg":"设置精品刷新成功！","infoId":29680500544427,"refreshTime":"2018-07-27 11:01:40","title":"技术支持"}],"refreshcount":1,"gaojiresource":1952}')
        # print(rf_result_dic)
        # print(type(rf_result_dic))
        if '成功' in rf_result_dic['refreshEntityList'][0]['errorMsg']:
            return 1
        else:
            return 0
    # 保存原始简历
    def save_jl_picture(self, url, driver, org_id, bucket):
        text = self.handl_58_font(url)
        # print(text)
        html = etree.HTML(text)
        head = html.xpath('//head')[0]
        head = etree.tostring(head, method='html').replace(b'"//', b'"https://')

        content = html.xpath('//div[@class="vipResContent resume_preview"]')[0]
        content = etree.tostring(content, method='html')
        try:
            phone = re.search(r'"number":"(\d*?)"', text, re.M|re.S).group(1)
            if phone:
                # phone = phone[:11]
                number = html.xpath('//div[@class="telephone telephone-no-border"]')[0]
                number = etree.tostring(number, method='html')
                replace_div = '<div class="telephone"><p class="phoneNum"><span class="icon-mobile"></span><span class="real-mobile stonefont">{number}</span></p><div class="resume-action"><div id="interview_send" class="interview-btn btn">发送面试邀请</div><div class="interview-result"><div id="bizState-1" class="result-item"><span class="icon-noSelected"></span><span class="invitation-result">可面试</span></div><div id="bizState-2" class="result-item"><span class="icon-noSelected"></span><span class="invitation-result">待定</span></div><div id="bizState-3" class="result-item"><span class="icon-noSelected"></span><span class="invitation-result">不合适</span></div><div id="bizState-5" class="result-item"><span class="icon-noSelected"></span><span class="invitation-result">暂未接通</span></div></div></div></div>'.format(
                    number=phone)
                content = content.replace(number, replace_div.encode('utf-8'))
        except:
            pass
        full_html = (head + content).decode('utf-8')

        file_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '58_picture' + os.sep + 'temp_58.html'
        filedir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '58_picture'
        picture_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + '58_picture' + os.sep + '58cj.png'
        if not os.path.exists(filedir):
            # print('文件夹', new_tj, '不存在，重新建立')
            # os.mkdir(file_path)
            os.makedirs(filedir)
        else:
            shutil.rmtree(filedir)
            os.makedirs(filedir)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        driver.get('file:///' + file_path)
        # print(browser.page_source)
        time.sleep(1)
        driver.save_screenshot(picture_path)
        with open(picture_path, 'rb') as f_58:
            shotname = str(int(time.time() * 1000)) + '_' + picture_path.split(os.sep)[-1]
            filename = 'channel_resume/' + org_id + '/' + str(shotname)
            resp_save = bucket.put_object(filename, f_58)
            save_url = resp_save.resp.response.url
        shutil.rmtree(filedir)
        return save_url
    # 58同城简历搜索并下载
    def search_58(self, orgid, jlid, paytype):
        pre_dl_url = 'https://jianli.58.com/resumedown/{jlid}/single/'.format(jlid=jlid)
        headers1 = {
            'Referer': 'https://jianli.58.com/resumedetail/singles/{jlid}'.format(jlid=jlid),
            'User-Agent': get_useragent()
        }
        res = self.session.get(url=pre_dl_url, headers=headers1)
        js = json.loads(res.text)
        if js.get('result') == 'success':
            # followparam = js['data']['followparam']
            resumeUpdateTime = js['data']['resumeUpdateTime']
            download_url = 'https://jianli.58.com/resumedown/ajax/{jlid}/single/?resumeUpdateTime={resumeUpdateTime}&selectPayType={Paytype}'.format(
                jlid=jlid, resumeUpdateTime=resumeUpdateTime, Paytype=paytype)
            headers2 = {
                'Referer': 'https://jianli.58.com/resumedown/{jlid}/single/'.format(jlid=jlid),
                'User-Agent': get_useragent()
            }
            res = self.session.get(url=download_url, headers=headers2)
            if '成功' in res.text:
                # re_58_tel = r'"mobile":"(\d+?)"'
                # patt_58_tel = re.compile(re_58_tel)
                # tel_58_li = patt_58_tel.findall(res.text)
                try:
                    xz_58_url = 'https://jianli.58.com/resumedetail/singles/' + jlid
                    xz_text = self.handl_58_font(xz_58_url)
                    xz_58_data = jx_58(xz_text, org_id=orgid, lx=2, channel_id=jlid)
                    return 1, xz_58_data
                except:
                    return 0, '简历解析出错，请联系管理员'
            else:
                return 0, '下载失败'
        else:
            return 0, js['msg']

    # 杭州人才查看前询问
    @staticmethod
    def ask_before_read(jls, orgid, jobid):
        flag = True
        today1 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        resp_li_all = []

        now_num = len(jls)
        # print(now_num)
        if now_num == 0:
            flag = False
        # 余数
        ys = now_num % 10
        if ys != 0:
            cs = int(now_num / 10) + 1
        else:
            cs = int(now_num / 10)
        # print(cs)
        # 每个页面，询问次数
        for i in range(1, cs + 1):
            if i == 1 and flag:
                pos = []
                Towu_jl = []
                jl_d = 1
                if now_num >= 10:
                    li_en = jls[0:i * 10]
                else:
                    li_en = jls
                for jl in li_en:
                    try:
                        info_ele = jl.xpath('./td[@class="Common_list_table-id-text"]/span/@id')[0]
                        chanl_id = info_ele.split('spanB')[1]
                        td_date = jl.xpath('./td[9]/text()')[0].strip()

                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid   # 企业id
                            content['jobId'] = jobid
                            content['channel'] = 2
                            content['channelUpdateTime'] = td_date
                            content['channelResumeId'] = chanl_id
                            content['downloadStatus'] = 0
                            content['resumeType'] = 2
                            Towu_jl.append(content)
                        else:
                            flag = False
                    except:
                        pos.append(len(Towu_jl))
                        content = {}
                        content['orgId'] = orgid
                        content['jobId'] = '000'
                        content['channel'] = 2
                        content['channelUpdateTime'] = '2018-01-01'
                        content['channelResumeId'] = '111111'
                        content['downloadStatus'] = 1
                        content['resumeType'] = 1
                        Towu_jl.append(content)
                # print(Towu_jl)
                # 将dict类型的数据转成str
                data = json.dumps(Towu_jl)
                data = data.encode('utf-8')
                resp_page = requests.post(url=wu_jlxw_url, data=data)
            elif 1 < i < cs and flag:
                pos = []
                jl_d = i
                Towu_jl = []
                for jl in jls[(i - 1) * 10:i * 10]:
                    try:
                        info_ele = jl.xpath('./td[@class="Common_list_table-id-text"]/span/@id')[0]
                        chanl_id = info_ele.split('spanB')[1]
                        td_date = jl.xpath('./td[9]/text()')[0]

                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid
                            content['jobId'] = jobid
                            content['channel'] = 2
                            content['channelUpdateTime'] = td_date
                            content['channelResumeId'] = chanl_id
                            content['downloadStatus'] = 0
                            content['resumeType'] = 2
                            Towu_jl.append(content)
                        else:
                            flag = False
                    except:
                        pos.append(len(Towu_jl))
                        content = {}
                        content['orgId'] = orgid
                        content['jobId'] = '000'
                        content['channel'] = 2
                        content['channelUpdateTime'] = '2018-01-01'
                        content['channelResumeId'] = '111111'
                        content['downloadStatus'] = 1
                        content['resumeType'] = 1
                        Towu_jl.append(content)
                    # print(Towu_jl)
                    # 将dict类型的数据转成str
                data = json.dumps(Towu_jl)
                data = data.encode('utf-8')
                resp_page = requests.post(url=wu_jlxw_url, data=data)
            elif i == cs and flag:
                pos = []
                jl_d = i
                Towu_jl = []
                for jl in jls[(i - 1) * 10:]:
                    try:
                        info_ele = jl.xpath('./td[@class="Common_list_table-id-text"]/span/@id')[0]
                        chanl_id = info_ele.split('spanB')[1]
                        td_date = jl.xpath('./td[9]/text()')[0]

                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid
                            content['jobId'] = jobid
                            content['channel'] = 2
                            content['channelUpdateTime'] = td_date
                            content['channelResumeId'] = chanl_id
                            content['downloadStatus'] = 0
                            content['resumeType'] = 2
                            Towu_jl.append(content)
                        else:
                            flag = False
                    except:
                        pos.append(len(Towu_jl))
                        content = {}
                        content['orgId'] = orgid
                        content['jobId'] = '000'
                        content['channel'] = 2
                        content['channelUpdateTime'] = '2018-01-01'
                        content['channelResumeId'] = '111111'
                        content['downloadStatus'] = 1
                        content['resumeType'] = 1
                        Towu_jl.append(content)
                    # print(Towu_jl)
                    # 将dict类型的数据转成str
                data = json.dumps(Towu_jl)
                data = data.encode('utf-8')
                resp_page = requests.post(url=wu_jlxw_url, data=data)
            # resp_page = [1]
            xd = resp_page.text
            # print(xd)
            # print(Towu_jl)
            xxx = xd.replace(', ', '-').replace(' ', '').replace('[', '').replace(']', '')
            resp_li = xxx.split('-')
            resp_li_all.extend(resp_li)
            # resp_li = ['1', '1', '1']
        return resp_li_all

    # 杭州人才简历搜索
    @staticmethod
    def search_resume_hzrc(data):
        def infunc(a):
            Ass = re.findall(r"code: '(.*?)', value: '(.*?)'",
                             re.search(r'var {a} = (.*?);'.format(a=a), text).group(1))
            return {i[1]: i[0] for i in Ass}
        js_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'pyth' + os.sep + 'xc_dir' + os.sep + 'DictTable.js'
        with open(js_path, encoding='utf-8') as f:
            text = f.read()

        ctJobareaAss = infunc('ctJobareaAss')
        ctIndTypeAss = infunc('ctIndTypeAss')
        ctFunTypeAss = infunc('ctFunTypeAss')
        # ctMajorAss = infunc('ctMajorAss')

        ctFL = {i.split('^')[0]: '22' + i.split('^')[1] for i in
                re.search(r'var ctFL = "(.*?)";', text).group(1).split('|')}

        workyear = {'': '不限', '0': '不限', '1': '无工作经验', '2': '一年', '3': '二年', '4': '三年', '5': '四年', '6': '五年', '7': '七年',
                    '8': '八年', '9': '九年', '10': '十年'}
        workyearfrom = {'不限': '0', '无工作经验': '1', '一年': '3', '二年': '4', '三年': '5', '五年': '6', '八年': '7', '十年': '8'}
        workyearto = {'不限': '99', '无工作经验': '1', '一年': '3', '二年': '4', '四年': '5', '七年': '6', '九年': '7'}

        degree = {'': '不限', '0': '不限', '1': '初中及以下', '2': '高中/中技/中专', '3': '大专', '4': '本科', '5': '硕士', '6': 'MBA',
                  '7': '博士'}
        degreefrom = {'不限': '0', '初中及以下': '1', '高中/中技/中专': '2', '大专': '5', '本科': '6', '硕士': '7', 'MBA': '10', '博士': '8'}
        degreeto = {'不限': '99', '初中及以下': '1', '高中/中技/中专': '4', '大专': '5', '本科': '6', '硕士': '7', '博士': '8'}

        expectsalary = {'': '不限', '0': '不限', '1': '1.5k', '2': '2k', '3': '3k', '4': '4.5k', '5': '6k', '6': '8k',
                        '7': '10k',
                        '8': '15k', '9': '20k', '10': '25k', '11': '30k', '12': '40k', '13': '50k', '14': '70k',
                        '15': '100k'}
        expectsalaryfrom = {'不限': '01', '1.5k': '02', '2k': '03', '3k': '04', '4.5k': '05', '6k': '06', '8k': '07',
                            '10k': '08',
                            '15k': '09', '20k': '13', '25k': '10', '30k': '14', '40k': '11', '50k': '12', '70k': '15',
                            '100k': '16'}
        expectsalaryto = {'不限': '99', '1.5k': '01', '2k': '02', '3k': '03', '4.5k': '04', '6k': '05', '8k': '06',
                          '10k': '07', '15k': '08', '20k': '09', '25k': '13', '30k': '10', '40k': '14', '50k': '11',
                          '70k': '12', '100k': '15'}

        # cursalaryfrom = {'不限': '01', '1.5k': '02', '2k': '03', '3k': '04', '4.5k': '05', '6k': '06', '8k': '07', '10k': '08',
        #                     '15k': '13', '20k': '09', '25k': '14', '30k': '10', '40k': '15', '50k': '11', '70k': '16', '100k': '12'}
        # cursalaryto = {'不限': '99', '及以上': '99', '1.5k': '01', '2k': '02', '3k': '03', '4.5k': '04', '6k': '05', '8k': '06',
        #                     '10k': '07', '15k': '08', '20k': '13', '25k': '09', '30k': '14', '40k': '10', '50k': '15',
        #                     '70k': '11', '100k': '16'}
        # englishlevel = {'不限': '99', '英语四级以上': '0116', '英语六级以上': '0117', '专业四级以上': '0132', '专业八级': '0133'}

        dd_flevel = {'一般': '2', '良好': '3', '熟练': '1', '精通': '0'}
        rsmupdate = {'近1周': '1', '近2周': '2', '近1个月': '3', '近2个月': '4', '近6个月': '5', '近1年': '6', '1年及以上': '7'}
        jobstatus = {'不限': '99', '目前正在找工作': '0', '其他': '1'}

        keyWord = str(data['keyWord'])
        place = '$'.join([ctJobareaAss.get(i.split('#', 1)[1].replace('#', '-').strip(),
                                           '') if '#' in i else ctJobareaAss.get(i.strip(), '') for i in data['place']])
        expectPlaceRule = str(data['expectPlaceRule'])
        job = '$'.join(
            [ctFunTypeAss.get(i.split('#', 1)[1].strip(), '') if '#' in i else ctFunTypeAss.get(i.strip(), '') for i in
             data['job']])
        industry = '$'.join(
            [ctIndTypeAss.get(i.split('#', 1)[1].strip(), '') if '#' in i else ctIndTypeAss.get(i.strip(), '') for i in
             data['industry']])
        workLimitfrom = workyearfrom.get(workyear[data['workLimit'][0].strip() if data['workLimit'] else ''], '')
        workLimitto = workyearto.get(workyear[data['workLimit'][1].strip() if data['workLimit'] else ''], '')
        educationfrom = degreefrom.get(degree[data['education'][0].strip() if data['education'] else ''], '')
        educationto = degreeto.get(degree[data['education'][1].strip() if data['education'] else ''], '')
        agefrom = data['age'][0].strip() if data['age'] else ''
        ageto = data['age'][1].strip() if data['age'] else ''
        nearCompany = data['nearCompany'].strip()
        if data['sex'].strip() == '男':
            sex = '0'
        elif data['sex'].strip() == '女':
            sex = '1'
        else:
            sex = '99'
        expectPayfrom = expectsalaryfrom.get(expectsalary[data['expectPay'][0]].strip() if data['expectPay'] else '',
                                             '')
        expectPayto = expectsalaryto.get(expectsalary[data['expectPay'][1]].strip() if data['expectPay'] else '', '')

        cursalaryfrom = ''
        cursalaryto = ''
        search_major_txt = ''
        search_hukou_txt = ''
        language = ctFL.get(data['language'].strip(), '')
        proficiency = dd_flevel.get(data['proficiency'].strip(), '')
        englishlevel = ''
        dateUpdated = rsmupdate.get(data['dateUpdated'].strip(), '')
        applyStatus = jobstatus.get(data['applyStatus'].strip(), '')
        no_name = '1'
        keyWordRule = str(data['keyWordRule'])
        ckbox = ' '.join(['985' if data['jbw'] == 1 else '', '211' if data['eyy'] == 1 else '',
                          '全日制' if data['fullTime'] == 1 else '', '海外留学' if data['overseasStudy'] == 1 else ''])
        expectPlace = '$'.join(
            [ctJobareaAss.get(i.split('#', 1)[1].strip(), '') if '#' in i else ctJobareaAss.get(i.strip(), '') for i in
             data['expectPlace']])
        overseas = str(data['overseas'])
        latelyJob = str(data['latelyJob'])
        latelyIndustry = str(data['latelyIndustry'])

        searchValueHid = '#'.join(
            [keyWord, place, expectPlaceRule, job, industry, workLimitfrom, workLimitto, educationfrom,
             educationto, agefrom, ageto, nearCompany, sex, expectPayfrom, expectPayto, cursalaryfrom,
             cursalaryto, search_major_txt, search_hukou_txt, language, proficiency, englishlevel, dateUpdated,
             applyStatus, no_name, keyWordRule, ckbox, expectPlace, overseas, latelyJob, latelyIndustry])
        return searchValueHid

    # 杭州人才查看简历
    def read_resume_hzrc(self, searchValueHid, orgid, jobid, max_num):
        url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
        response = self.session.post(url=url, headers=self.headers, data={'searchValueHid': searchValueHid})

        data_wu_51 = []
        ss_num = 0

        def paging(response_page):
            nonlocal data_wu_51, ss_num

            if '抱歉，没有搜到您想找的简历！' in response_page.text:
                if len(data_wu_51) > 0:
                    data = json.dumps(data_wu_51)
                    data = data.encode('utf-8')
                    res = requests.post(url=wu_jl_url, data=data)
                    print(res.text)
                    data_wu_51 = []
                return

            VIEWSTATE = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', response_page.text).group(1)
            hidCheckUserIds = re.search(r'<input name="hidCheckUserIds" type="hidden" id="hidCheckUserIds" value="(.*?)" />', response_page.text).group(1)
            hidCheckKey = re.search(r'<input name="hidCheckKey" type="hidden" id="hidCheckKey" value="(.*?)" />', response_page.text).group(1)

            print(hidCheckUserIds)
            html = etree.HTML(response_page.text)
            lis = html.xpath('//div[@class="Common_list-table"]/table/tbody/tr')
            lis1 = [value for key, value in enumerate(lis) if key % 2 == 0]
            ask_result = self.ask_before_read(lis1, orgid, jobid)

            for key, value in enumerate(lis1):
                try:
                    ask_status = ask_result[key]
                except:
                    if len(data_wu_51) > 0:
                        data = json.dumps(data_wu_51)
                        data = data.encode('utf-8')
                        res = requests.post(url=wu_jl_url, data=data)
                        print(res.text)
                        data_wu_51 = []
                    return
                if ask_status == '1':
                    try:
                        details_url = 'https://ehire.51job.com' + value.xpath('./td[2]/span[1]/a/@href')[0]
                        details_response = self.session.get(url=details_url, headers=self.headers)
                        try:
                            final_data = jx_51_ss(text=details_response.text, ds=0, org_id=orgid, job_id=jobid, lx=1)
                        except Exception as e:
                            final_data = jx_51_sjx(text=details_response.text, ds=0, org_id=orgid, job_id=jobid, lx=1)

                        data_wu_51.append(final_data)
                        ss_num = ss_num + 1

                    except:
                        logging.exception("Exception Logged")
                        continue

                    if ss_num >= max_num:
                        data = json.dumps(data_wu_51)
                        data = data.encode('utf-8')
                        res = requests.post(url=wu_jl_url, data=data)
                        print(res.text)
                        data_wu_51 = []
                        return

                    if len(data_wu_51) == 3:
                        data = json.dumps(data_wu_51)
                        data = data.encode('utf-8')
                        res = requests.post(url=wu_jl_url, data=data)
                        print(res.text)
                        data_wu_51 = []

                    time.sleep(random.uniform(1.5, 3))

            data = {
                '__EVENTTARGET': 'pagerBottomNew$nextButton',
                '__VIEWSTATE': VIEWSTATE,
                'hidCheckUserIds': hidCheckUserIds,
                'hidCheckKey': hidCheckKey,
                'ctrlSerach$hidSearchValue': searchValueHid
            }
            response_page = self.session.post(url=url, headers=self.headers, data=data)
            paging(response_page)

        paging(response)
        return ss_num
