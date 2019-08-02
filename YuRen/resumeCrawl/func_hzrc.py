import json
import re
import requests
import datetime
import time
from lxml import etree
import logging
from scrapy import Selector
import shutil
from settings import *
from al_qf import *
from PIL import Image
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


def jx_hzrc(text, ds=0, job_id='', org_id='111', lx=0, dt=''):
        hzrc_data = {}
        sel = Selector(text=text)
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        # 简历主表
        hzrc_data['info'] = {}
        hzrc_data['info']['channel'] = 5
        resume_id_str = sel.xpath('//input[@id="acb2ge"]/parent::div/div[@class="nine1"]/@onclick').extract()[0].strip()
        hzrc_data['info']['channel_resume_id'] = resume_id_str.split("dodownload('")[1].split("',this")[0]

        if not sel.xpath('//div[@id="read" and @class="nine3"]'):
            try:
                hzrc_data['info']['mobilephone'] = sel.xpath('//td[@id="persionbae017"]/text()').extract()[0]
            except:
                pass
            try:
                hzrc_data['info']['email'] = sel.xpath('//td[@id="persionaae159"]/text()').extract()[0]
            except:
                pass

        hzrc_data['info']['name'] = sel.xpath('//span[@id="nameAac003"]/text()').extract()[0]
        if '*' in hzrc_data['info']['name']:
            hzrc_data['info']['name'] = hzrc_data['info']['name'].replace('*', 'X')
        # 应聘者照片
        try:
            pho_url = sel.xpath('//div[@style="float:right"]/div/img/@src').extract()[0]
            hzrc_data['info']['photo_url'] = pho_url
            if 'http:' not in pho_url:
                hzrc_data['info']['photo_url'] = 'http://www.hzrc.com' + pho_url
        except:
            pass
        for rc_in in sel.xpath('//table[@class="bg6-table"]//tr'):
            rc_intr = rc_in.xpath('string()').extract()[0].strip()
            # 出生日期、性别
            if "出生日期" in rc_intr:
                birth_year = rc_intr.split("出生日期：")[1].strip().split(" ")[0].split("-")[0]
                hzrc_data['info']['birth_year'] = birth_year
                if "性别" in rc_intr:
                    sex = rc_intr.split("性别：")[1].strip()
                    hzrc_data['info']['sex'] = sex
            # 政治面貌、参加工作时间
            elif "政治面貌" in rc_intr:
                birth_year = rc_intr.split("政治面貌：")[1].strip().split(" ")[0].strip()
                hzrc_data['info']['politics_status'] = birth_year
                if "工作时间" in rc_intr:
                    sex = rc_intr.split("工作时间：")[1].strip().split("-")[0]
                    hzrc_data['info']['start_working_year'] = sex
            # 学历
            elif "学历" in rc_intr:
                degree = rc_intr.split("最高学历：")[1].strip().split(" ")[0].replace("大学", "").strip()
                hzrc_data['info']['degree'] = degree
            # 婚姻状况
            elif "婚姻状况" in rc_intr:
                marital_status = rc_intr.split("婚姻状况：")[1].strip().split(" ")[0].strip()
                hzrc_data['info']['marital_status'] = marital_status
            # 户口所在地
            elif "户口所在地" in rc_intr:
                residence_address = rc_intr.split("户口所在地：")[1].strip()
                hzrc_data['info']['residence_address'] = residence_address
            # 现居住地
            elif "居 住 地" in rc_intr:
                current_address = rc_intr.split("居 住 地：")[1].strip()
                hzrc_data['info']['current_address'] = current_address
        # 渠道更新时间
        try:
            channel_update_time = sel.xpath('string(//span[@class="bg5-span04"])').extract()[0]
            hzrc_data['info']['channel_update_time'] = channel_update_time.split(" ")[0].strip()
        except:
            pass
        # 求职意向
        hzrc_data['objective'] = {}
        hzrc_data['credentials'] = []
        hzrc_data['jobs'] = []
        hzrc_data['trainings'] = []
        hzrc_data['educations'] = []
        hzrc_data['languages'] = []
        for objective in sel.xpath('//table[@class="bg9-table"]//tr'):
            objective_qz = objective.xpath('string()').extract()[0].strip()
            # 期望月薪
            if "期望月薪" in objective_qz:
                if '保密' not in objective_qz and '以' not in objective_qz:
                    try:
                        hzrc_data['objective']['expected_salary_lower'] = int(
                            objective_qz.replace("期望月薪：", "").split('-')[0].strip())
                        hzrc_data['objective']['expected_salary_upper'] = int(
                            objective_qz.split('-')[1].replace("元", "").strip())
                    except:
                        pass
                elif '保密' not in objective_qz and '以' in objective_qz:
                    try:
                        hzrc_data['objective']['expected_salary_lower'] = int(
                            objective_qz.replace("期望月薪：", "").replace("元", "").split('以')[0].strip())
                        hzrc_data['objective']['expected_salary_upper'] = int(
                            objective_qz.replace("期望月薪：", "").replace("元", "").split('以')[0].strip())
                    except:
                        pass
                else:
                    try:
                        hzrc_data['objective']['expected_salary_lower'] = 0
                        hzrc_data['objective']['expected_salary_upper'] = 0
                    except:
                        pass
            # 期望工作地点
            elif "工作地点" in objective_qz:
                hzrc_data['objective']['expected_address'] = []
                for trade in (objective_qz.replace("工作地点：", "").strip().split(",")[0:]):
                    try:
                        hzrc_data['objective']['expected_address'].append(trade)
                    except:
                        pass
            # 期望职位
            elif "期望职位" in objective_qz:
                hzrc_data['objective']['expected_job_title'] = []
                try:
                    for expected_job_title in (
                    objective_qz.replace("期望职位：", "").replace("\n", "").replace("\t", "").replace(" ",
                                                                                                  "").strip().split(
                            ",")[0:]):
                        hzrc_data['objective']['expected_job_title'].append(expected_job_title)
                except:
                    pass
            # 行业
            elif "期望行业" in objective_qz:
                hzrc_data['objective']['trade'] = []
                try:
                    for trade in (objective_qz.replace("期望行业：", "").strip().split(",")[0:]):
                        hzrc_data['objective']['trade'].append(trade)
                except:
                    pass
            # 工作性质
            elif "工作性质" in objective_qz:
                hzrc_data['objective']['job_nature'] = []
                try:
                    if '全' in objective_qz and '兼' in objective_qz:
                        hzrc_data['objective']['job_nature'] = ['全职', '兼职']
                    elif '全职' in objective_qz:
                        hzrc_data['objective']['job_nature'].append('全职')
                    elif '兼职' in objective_qz:
                        hzrc_data['objective']['job_nature'].append('兼职')
                except:
                    pass
            # 自我评价
            hzrc_data['objective']['self_evaluation'] = sel.xpath('string(//span[@class="bg10-sp5"])').extract()[
                0].replace("\r", "").replace("\n", "").replace("\t", "").strip()
        dk_ele_len = len(sel.xpath('//div[@class="right-div-down"]/div[@class="bg-title"]'))
        for index, dk_ele in enumerate(sel.xpath('//div[@class="right-div-down"]/div[@class="bg-title"]')):
            try:
                # 工作经验
                if '工作实践经验' in dk_ele.xpath('string(.)').extract()[0].strip():
                    now_index = int(index) + 1
                    if now_index != dk_ele_len:
                        xpa_now_0 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index) + ']'
                        xpa_now_1 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index + 1) + ']'
                        # print(xpa_now)
                        source_code_0 = sel.xpath(xpa_now_0).extract()[0]
                        source_code_1 = sel.xpath(xpa_now_1).extract()[0]
                        source_code_final = text.split(source_code_0)[1].split(source_code_1)[0]
                        # print(source_code_final)
                        sel_job = Selector(text=source_code_final)
                        # 工作时间、单位、职位、内容
                        for train_1 in sel_job.xpath('//div[@class="bg-10"]'):
                            # print(sel_job.xpath('string(//div[@class="bg-10"])').extract()[0])
                            train_dic = {}
                            job_content = train_1.xpath('string(div[@class="bg10-div2"])').extract()[0]
                            # print(job_content)
                            # 工作内容
                            train_dic['job_content'] = job_content.split("主要工作内容：", 1)[1].replace("\r", "").replace(
                                "\n", "").replace("\t", "").strip()
                            for train_ele in train_1.xpath('div[@class="bg10-div1"]'):
                                for yy_ele in train_ele.xpath('span'):
                                    try:
                                        if "工作单位" in yy_ele.xpath('string()').extract()[0]:
                                            company = yy_ele.xpath('string()').extract()[0]
                                            train_dic['company'] = company.split("工作单位：")[1]
                                        elif "所在职位" in yy_ele.xpath('string()').extract()[0]:
                                            job_title = yy_ele.xpath('string()').extract()[0]
                                            train_dic['job_title'] = job_title.split("所在职位：")[1]
                                        elif "工作时间" in yy_ele.xpath('string()').extract()[0]:
                                            during=yy_ele.xpath('string()').extract()[0]
                                            if '未知' not in during:
                                                if "至今" in during:
                                                    train_dic['during_start'] = during.split("工作时间：")[1].split("至")[0].strip()
                                                    train_dic['during_end'] = "9999-01-01"
                                                else:
                                                    train_dic['during_start']=during.split("工作时间：")[1].split("至")[0].strip()
                                                    train_dic['during_end']=during.split("至")[1].strip()
                                            else:
                                                during = during.replace('未知', '').replace('至', '')
                                                train_dic['during_start'] = during.split("工作时间：")[1].strip()
                                    except:
                                        pass
                            hzrc_data['jobs'].append(train_dic)
                # 培训经历
                elif '培训经历' in dk_ele.xpath('string(.)').extract()[0].strip():
                    now_index = int(index) + 1
                    if now_index != dk_ele_len:
                        xpa_now_0 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index) + ']'
                        xpa_now_1 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index + 1) + ']'
                        # print(xpa_now)
                        source_code_0 = sel.xpath(xpa_now_0).extract()[0]
                        source_code_1 = sel.xpath(xpa_now_1).extract()[0]
                        source_code_final = text.split(source_code_0)[1].split(source_code_1)[0]
                        # print(source_code_final)
                        sel2 = Selector(text=source_code_final)
                        # 培训时间、地点、课程、内容
                        for train_1 in sel2.xpath('//div[@class="bg-10"]'):
                            train_dic = {}
                            description = train_1.xpath('string(div[@class="bg10-div4"])').extract()[0]
                            # 培训内容（详情）
                            train_dic['training_course'] = description.split("培训内容：")[1].replace("\r", "").replace("\n",
                                                                                                                   "").replace(
                                "\t", "").strip()
                            for train_ele in train_1.xpath('div[@class="bg10-div3"]'):
                                for yy_ele in train_ele.xpath('span'):
                                    try:
                                        if "培训机构" in yy_ele.xpath('string()').extract()[0]:
                                            training_agency = yy_ele.xpath('string()').extract()[0]
                                            train_dic['training_agency'] = training_agency.split("培训机构：")[1]
                                        elif "培训课程" in yy_ele.xpath('string()').extract()[0]:
                                            training_course = yy_ele.xpath('string()').extract()[0]
                                            train_dic['training_course'] = training_course.split("培训课程：")[1].replace(
                                                "\r", "").replace("\n", "").replace("\t", "").strip()
                                        elif "培训时间" in yy_ele.xpath('string()').extract()[0]:
                                            during = yy_ele.xpath('string()').extract()[0]
                                            if "至今" in during:
                                                train_dic['during_start'] = during.split("培训时间：")[1].split("至")[
                                                    0].strip()
                                                train_dic['during_end'] = "9999-01-01"
                                            else:
                                                train_dic['during_start'] = during.split("培训时间：")[1].split("至")[
                                                    0].strip()
                                                train_dic['during_end'] = during.split("至")[1].strip()
                                    except:
                                        pass
                            hzrc_data['trainings'].append(train_dic)
                # 证书
                elif '所获证书' in dk_ele.xpath('string(.)').extract()[0].strip():
                    now_index = int(index) + 1
                    if now_index != dk_ele_len:
                        xpa_now_0 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index) + ']'
                        xpa_now_1 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index + 1) + ']'
                        # print(xpa_now)
                        source_code_0 = sel.xpath(xpa_now_0).extract()[0]
                        source_code_1 = sel.xpath(xpa_now_1).extract()[0]
                        source_code_final = text.split(source_code_0)[1].split(source_code_1)[0]
                        # print(source_code_final)
                        sel_zs = Selector(text=source_code_final)
                        for train_1 in sel_zs.xpath('//div[@class="bg-10"]'):
                            train_dic = {}
                            # 详细描述（成绩）、名称、时间
                            score = train_1.xpath('string(div[@class="bg10-div4"])').extract()[0]
                            train_dic['score'] = score.split("详细描述：")[1].replace("\r", "").replace("\n", "").replace(
                                "\t", "").strip()
                            for train_ele in train_1.xpath('div[@class="bg10-div3"]'):
                                for yy_ele in train_ele.xpath('span'):
                                    try:
                                        if "证书名称" in yy_ele.xpath('string()').extract()[0]:
                                            training_agency = yy_ele.xpath('string()').extract()[0]
                                            train_dic['training_agency'] = training_agency.split("证书名称：")[1]
                                        elif "获取时间" in yy_ele.xpath('string()').extract()[0]:
                                            training_course = yy_ele.xpath('string()').extract()[0]
                                            train_dic['training_course'] = training_course.split("获取时间：")[1]
                                    except:
                                        pass
                            hzrc_data['credentials'].append(train_dic)
                # 教育经历
                elif '教育经历' in dk_ele.xpath('string(.)').extract()[0].strip():
                    now_index = int(index) + 1
                    if now_index != dk_ele_len:
                        xpa_now_0 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index) + ']'
                        xpa_now_1 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index + 1) + ']'
                        # print(xpa_now)
                        source_code_0 = sel.xpath(xpa_now_0).extract()[0]
                        source_code_1 = sel.xpath(xpa_now_1).extract()[0]
                        source_code_final = text.split(source_code_0)[1].split(source_code_1)[0]
                        # print(source_code_final)
                        sel_zs = Selector(text=source_code_final)
                        for train_1 in sel_zs.xpath('//div[@class="bg-10"]'):
                            train_dic = {}
                            # 时间、毕业院校、专业、学历
                            for train_ele in train_1.xpath('div[@class="bg10-div3"]'):
                                for yy_ele in train_ele.xpath('span'):
                                    try:
                                        if "毕业院校" in yy_ele.xpath('string()').extract()[0]:
                                            school = yy_ele.xpath('string()').extract()[0]
                                            train_dic['school'] = school.split("毕业院校：")[1]
                                        elif "所学专业" in yy_ele.xpath('string()').extract()[0]:
                                            major = yy_ele.xpath('string()').extract()[0]
                                            train_dic['major'] = major.split("所学专业：")[1]
                                        elif "学历" in yy_ele.xpath('string()').extract()[0]:
                                            degree = yy_ele.xpath('string()').extract()[0]
                                            train_dic['degree'] = degree.split("学历：")[1]
                                        elif "教育时间" in yy_ele.xpath('string()').extract()[0]:
                                            during = yy_ele.xpath('string()').extract()[0]
                                            if '未知' in during:
                                                if "至今" in during:
                                                    train_dic['during_end'] = "9999-01-01"
                                            else:
                                                if "至今" in during:
                                                    train_dic['during_start'] = during.split("教育时间：")[1].split("至")[0].strip()
                                                    train_dic['during_end'] = "9999-01-01"
                                                else:
                                                    train_dic['during_start'] = during.split("教育时间：")[1].split("至")[0].strip()
                                                    train_dic['during_end'] = during.split("至")[1].strip()
                                    except:
                                        pass
                            hzrc_data['educations'].append(train_dic)
                # 专业技能
                elif '专业技能' in dk_ele.xpath('string(.)').extract()[0].strip():
                    now_index = int(index) + 1
                    if now_index != dk_ele_len:
                        xpa_now_0 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index) + ']'
                        xpa_now_1 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index + 1) + ']'
                        # print(xpa_now)
                        source_code_0 = sel.xpath(xpa_now_0).extract()[0]
                        source_code_1 = sel.xpath(xpa_now_1).extract()[0]
                        source_code_final = text.split(source_code_0)[1].split(source_code_1)[0]
                        # print(source_code_final)
                        sel_languages = Selector(text=source_code_final)
                        # 获取时间、技能、等级、说明
                        for train_1 in sel_languages.xpath('//div[@class="bg-10"]'):
                            train_dic = {}
                            for train_ele in train_1.xpath('div[@class="bg10-div3"]'):
                                for yy_ele in train_ele.xpath('span'):
                                    try:
                                        if "技能" in yy_ele.xpath('string()').extract()[0]:
                                            skill = yy_ele.xpath('string()').extract()[0]
                                            train_dic['skill'] = skill.split("技能：")[1]
                                        elif "等级" in yy_ele.xpath('string()').extract()[0]:
                                            level = yy_ele.xpath('string()').extract()[0]
                                            train_dic['level'] = level.split("等级：")[1]
                                        elif "获取时间" in yy_ele.xpath('string()').extract()[0]:
                                            duration = yy_ele.xpath('string()').extract()[0]
                                            train_dic['duration'] = 2018 - int(
                                                duration.split("获取时间：")[1].split("-")[0].strip())
                                    except:
                                        pass
                            hzrc_data['languages'].append(train_dic)
                # 获奖情况
                elif '获奖情况' in dk_ele.xpath('string(.)').extract()[0].strip():
                    now_index = int(index) + 1
                    if now_index != dk_ele_len:
                        xpa_now_0 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index) + ']'
                        xpa_now_1 = '//div[@class="right-div-down"]/div[@class="bg-title"][' + str(now_index + 1) + ']'
                        # print(xpa_now)
                        source_code_0 = sel.xpath(xpa_now_0).extract()[0]
                        source_code_1 = sel.xpath(xpa_now_1).extract()[0]
                        source_code_final = text.split(source_code_0)[1].split(source_code_1)[0]
                        # print(source_code_final)
                        sel_hj = Selector(text=source_code_final)
                        for train_1 in sel_hj.xpath('//div[@class="bg-10"]'):
                            train_dic = {}
                            # 证书名称、成果名称、时间、成果说明
                            score = train_1.xpath('string(div[@class="bg10-div4"])').extract()[0]
                            # 成果说明
                            train_dic['score'] = score.split("成果说明：")[1].replace("\r", "").replace("\n", "").replace(
                                "\t", "").strip()
                            for train_ele in train_1.xpath('div[@class="bg10-div3"]'):
                                for yy_ele in train_ele.xpath('span'):
                                    try:
                                        if "证书名称" in yy_ele.xpath('string()').extract()[0]:
                                            training_agency = yy_ele.xpath('string()').extract()[0]
                                            train_dic['training_agency'] = training_agency.split("证书名称：")[1]
                                        elif "获取时间" in yy_ele.xpath('string()').extract()[0]:
                                            training_course = yy_ele.xpath('string()').extract()[0]
                                            train_dic['training_course'] = training_course.split("获取时间：")[1]
                                    except:
                                        pass
                            hzrc_data['credentials'].append(train_dic)
            except:
                pass
        hzrc_data['org'] = {}

        hzrc_data['org']['org_id'] = org_id
        try:
            if hzrc_data['info']['mobilephone']:
                hzrc_data['org']['download_status'] = 1
        except:
            hzrc_data['org']['download_status'] = 0
        # 插件
        hzrc_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        # 收件箱--------------渠道职位ID
        if lx == 1:
            hzrc_data['org']['resume_type'] = 1
            hzrc_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
            if job_id:
                hzrc_data['org']['job_id'] = job_id
        # 搜索/推荐----------遇仁职位ID
        elif lx == 2:
            hzrc_data['org']['resume_type'] = 2
            hzrc_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
            if job_id:
                hzrc_data['org']['job_id'] = job_id
        # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
        if dt:
            hzrc_data['org']['delivery_time'] = dt
        # print(hzrc_data)
        return hzrc_data


class Module_hzrc(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_hzrc, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'User-Agent': get_useragent(),
        }


    # 邮箱下载附件
    def email_dl(self, dl_url):
        hzrc_xz_dir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc' + os.sep + 'download'
        # print(new_tj)
        # time.sleep(1000)
        if not os.path.exists(hzrc_xz_dir):
            # print('文件夹', new_tj, '不存在，重新建立')
            # os.mkdir(file_path)
            os.makedirs(hzrc_xz_dir)
        else:
            shutil.rmtree(hzrc_xz_dir)
            os.makedirs(hzrc_xz_dir)
        id_str = dl_url.split('acc210=')[1]
        dl_file = self.session.get(url=dl_url, headers=self.headers)
        if ',' in id_str:
            with open("Mod_Pyth/hzrc/download/hzrc.zip", "wb") as code:
                code.write(dl_file.content)
            return 'zip'
        else:
            with open("Mod_Pyth/hzrc/download/hzrc.doc", "wb") as code:
                code.write(dl_file.content)
            return 'doc'

    # 杭州人才登录判断
    def login_judge_hzrc(self):
        home_url = 'http://www.hzrc.com/wb/a/a/wbaa_cont.html'
        response_zy = self.session.get(url=home_url, headers=self.headers)
        response_zy = response_zy.text
        # print(response_zy)
        sel = Selector(text=response_zy)
        # xzs_hzrc = 0
        xpa_bk_li = '//div[@class="left-3"]/div[@class="left-3-div1"]'
        for bk in sel.xpath(xpa_bk_li):
            bk_name = bk.xpath('a[@class="left-3-div1-span1"]/text()').extract()[0].strip()
            if '网络招聘' in bk_name:
                xzs_hzrc_li = bk.xpath('span[@class="left-3-div1-span2"]')
                for bk_child_1 in xzs_hzrc_li:
                    bk_child_str = bk_child_1.xpath('string()').extract()[0].strip()
                    # print(bk_child_str)
                    if '可下载简历数：' in bk_child_str:
                        xzs_hzrc = bk_child_str.split('可下载简历数：')[1].replace('个', '').strip()
                        # print(xzs_hzrc)
        return xzs_hzrc
    # 杭州人才职位刷新
    def refresh_job_hzrc(self, JobID):
        refresh_sjc = str(int(time.time()*1000))
        refresh_url = 'http://www.hzrc.com/wb/d/b/wbdb_refresh_job.html?acb210=' + JobID + '&_=' + refresh_sjc
        rf_result = self.session.get(url=refresh_url, headers=self.headers)
        rf_result_dic = json.loads(rf_result.text)
        rf_time = rf_result_dic['aae396']
        # print(rf_time)
        return rf_time

    def save_jl_picture(self, url, driver, org_id, bucket):
        filedir = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc_picture'
        picture_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'hzrc_picture' + os.sep + 'hzrccj.png'
        if not os.path.exists(filedir):
            # print('文件夹', new_tj, '不存在，重新建立')
            # os.mkdir(file_path)
            os.makedirs(filedir)
        else:
            shutil.rmtree(filedir)
            os.makedirs(filedir)

        driver.get(url)
        # print(browser.page_source)
        time.sleep(2)
        driver.save_screenshot(picture_path)
        try:
            source_xpa_comman = '//div[@class="match-vita"]'
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
        with open(picture_path, 'rb') as f_58:
            shotname = str(int(time.time() * 1000)) + '_' + picture_path.split(os.sep)[-1]
            filename = 'channel_resume/' + org_id + '/' + str(shotname)
            resp_save = bucket.put_object(filename, f_58)
            save_url = resp_save.resp.response.url
        shutil.rmtree(filedir)
        return save_url
    # 杭州人才简历搜索下载
    def search_hzrc(self, orgid, acc200, acc210):
        time_str = str(int(time.time() * 1000))
        search_url_1 = 'http://www.hzrc.com/wb/b/a/wbba_checktc.html?acc200=' + acc200 + '&acc210=' + acc210 + '&_' + time_str
        search_url_0 = 'http://www.hzrc.com/wb/b/a/wbba_viewcc21.html?acc200=' + acc200 + '&acc210=' + acc210 + '&keyword='

        search_response_0 = self.session.get(url=search_url_0, headers=self.headers)
        source_text = search_response_0.text
        resume_cont = jx_hzrc(text=source_text, ds=0, job_id='', org_id=orgid, lx=2, dt='')
        search_response_1 = self.session.get(url=search_url_1, headers=self.headers)
        # print(search_response_1.text)
        # print(type(search_response_1.text))
        search_response_dict = json.loads(search_response_1.text)
        try:
            resume_cont['info']['name'] = search_response_dict['cc22']['aac003']
        except:
            pass
        try:
            resume_cont['info']['email'] = search_response_dict['cc22']['aae159']
        except:
            pass
        try:
            resume_cont['info']['mobilephone'] = search_response_dict['cc22']['bae017']
        except:
            pass
        return resume_cont

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
