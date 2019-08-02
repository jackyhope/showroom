import json
import re
import traceback
import requests
import datetime
import time
from scrapy.selector import Selector
import logging
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
    return {'User-Agent': user_agent}


def jx_lp_ss(text, ds=0, org_id='111', job_id='', lx=0):
    sel = Selector(text=text)

    today1 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month

    jljx_lp_data = {}
    jljx_lp_data['info'] = {}
    jljx_lp_data['objective'] = {}
    jljx_lp_data['jobs'] = []
    jljx_lp_data['educations'] = []
    jljx_lp_data['at_schools'] = []
    jljx_lp_data['credentials'] = []
    jljx_lp_data['languages'] = []
    jljx_lp_data['trainings'] = []
    jljx_lp_data['projects'] = []
    jljx_lp_data['info']['channel'] = 10

    try:
        jljx_lp_data['info']['channel_resume_id'] = \
            sel.xpath('//section[@class="title-info"]/div[@class="clearfix"]/h6[1]/small[2]/text()').extract()[
                0].strip()
        jljx_lp_data['info']['channel_update_time'] = \
            sel.xpath('//section[@class="title-info"]/div[@class="clearfix"]/h6[2]/small[1]/text()').extract()[
                0].replace(
                '更新', '').strip()
    except:
        print(traceback.format_exc())

    try:
        jljx_lp_data['info']['photo_url'] = 'https:' + sel.xpath(
            '//div[@class="individual-img relative float-left"]/img/@src').extract()[0]
    except:
        print(traceback.format_exc())

    # 个人信息
    info = sel.xpath('//div[@class="individual-info float-left"]/ul[1]')
    if bool(info):
        info = info[0]
        try:
            ul_li1 = ''.join(info.xpath('./li[1]/span[2]//text()').extract()).strip().split('·')
            ul_li1 = [i.strip() for i in ul_li1]
            jljx_lp_data['info']['name'] = ul_li1[0] if ul_li1[0] not in ['******', '不公开'] else jljx_lp_data['info'][
                'channel_resume_id']
            for i in ul_li1[1:]:
                if i in ['男', '女']:
                    jljx_lp_data['info']['sex'] = i
                elif '岁' in i:
                    jljx_lp_data['info']['birth_year'] = int(now_year) - int(i.replace('岁', '').strip())
                elif i in ['已婚', '未婚']:
                    jljx_lp_data['info']['marital_status'] = i
                elif '籍贯' in i:
                    jljx_lp_data['info']['residence_address'] = i.replace('（籍贯）', '').strip()
        except:
            print(traceback.format_exc())

        try:
            ul_li2 = info.xpath('./li[2]/span[2]/text()').extract()[0].strip().split('·')
            jljx_lp_data['info']['company'] = ul_li2[0].strip()
            work_year = ul_li2[2].strip().replace('经验', '').strip()
            if work_year == '小于1年':
                work_year = '0'
            jljx_lp_data['info']['start_working_year'] = int(now_year) - int(work_year.replace('年', '').strip())
            jljx_lp_data['objective']['work_status'] = info.xpath('./li[2]/label[1]/span/text()').extract()[0].strip()
        except:
            print(traceback.format_exc())

        try:
            ul_li3 = info.xpath('./li[3]/span[2]/text()').extract()[0].strip().split('·')
            jljx_lp_data['info']['degree'] = ul_li3[2].strip()
        except:
            print(traceback.format_exc())

        try:
            ul_li4 = info.xpath('./li[4]/span[2]/em/text()').extract()
            mobilephone = ul_li4[0].strip()
            if mobilephone not in ['******', '不公开']:
                jljx_lp_data['info']['mobilephone'] = mobilephone
            email = ul_li4[1].strip()
            if email not in ['******', '不公开']:
                jljx_lp_data['info']['email'] = email
        except:
            print(traceback.format_exc())

    # 职业概况
    objective = sel.xpath('//section[@class="occupation-survey content-wrap"]/div[@class="sub-wrap"]/table/tbody')
    if bool(objective):
        objective = objective[0]
        try:
            jljx_lp_data['info']['current_address'] = \
                objective.xpath('.//span[contains(text(), "目前地点")]/following-sibling::span[1]/text()').extract()[
                    0].strip()
        except:
            print(traceback.format_exc())

        try:
            annual_salary = \
                objective.xpath('.//span[contains(text(), "目前年薪")]/following-sibling::span[1]/text()').extract()[
                    0].strip()
            if annual_salary not in ['保密', '未填']:
                jljx_lp_data['info']['annual_salary'] = round(float(annual_salary.split('万')[0]) * 10000, 1)
        except:
            print(traceback.format_exc())

        try:
            expected_salary = \
                objective.xpath('.//span[contains(text(), "期望年薪")]/following-sibling::span[1]/text()').extract()[
                    0].strip()
            if expected_salary not in ['面议', '保密', '未填']:
                jljx_lp_data['objective']['expected_salary_lower'] = jljx_lp_data['objective'][
                    'expected_salary_upper'] = round(float(expected_salary.split('万')[0]) * 10000, 1)
        except:
            print(traceback.format_exc())

        try:
            jljx_lp_data['objective']['trade'] = \
                objective.xpath('.//span[contains(text(), "期望行业")]/following-sibling::span[1]/text()').extract()[
                    0].strip().split(';')
        except:
            print(traceback.format_exc())

        try:
            jljx_lp_data['objective']['expected_address'] = \
                objective.xpath('.//span[contains(text(), "期望地点")]/following-sibling::span[1]/text()').extract()[
                    0].strip().split(';')

        except:
            print(traceback.format_exc())

        try:
            jljx_lp_data['objective']['expected_job_title'] = \
                objective.xpath('.//span[contains(text(), "期望职位")]/following-sibling::span[1]/text()').extract()[
                    0].strip().split(';')
        except:
            print(traceback.format_exc())

    # 项目经验
    projects = sel.xpath('//section[@class="project-experience content-wrap"]/div[@class="sub-wrap"]')
    if bool(projects):
        projects = projects[0].xpath('./div[@class="project-cont"]')
        for cell in projects:
            try:
                project_1 = {}
                try:
                    project_time = cell.xpath('./p[1]/span[2]/text()').extract()[0].replace(' ', '').split('(')[
                        0].split('-')
                    project_1['during_start'] = project_time[0].replace('/', '-') + '-01'
                    project_1['during_end'] = '9999-01-01' if '至今' in project_time[1] else project_time[1].replace('/',
                                                                                                                   '-') + '-01'
                except:
                    print(traceback.format_exc())
                try:
                    project_1['title'] = cell.xpath('./p[1]/span[1]/text()').extract()[0].strip()
                except:
                    print(traceback.format_exc())

                company = cell.xpath('.//span[contains(text(), "所在公司")]/following-sibling::*[1]/text()').extract()
                if company:
                    project_1['company'] = company[0].strip()

                description = cell.xpath('.//span[contains(text(), "项目简介")]/following-sibling::*[1]/text()').extract()
                if bool(description):
                    project_1['description'] = ''.join([i.strip() for i in description]).strip()

                duty = cell.xpath('.//span[contains(text(), "项目职责")]/following-sibling::*[1]//text()').extract()
                if bool(duty):
                    project_1['duty'] = ''.join([i.strip() for i in duty]).strip()

                jljx_lp_data['projects'].append(project_1)

            except:
                print(traceback.format_exc())

    # 教育经历
    educations = sel.xpath(
        '//section[@class="education-experience content-wrap"]/div[@class="sub-wrap"]/ul[@class="education-cont"]')
    if bool(educations):
        educations = educations[0].xpath('./li[@class="clearfix"]/dl[1]/dd[1]/p[1]')

        for cell in educations:
            try:
                education_1 = dict()

                person_edu = cell.xpath('./span[1]/text()').extract()[0].strip().split('·')
                education_1['school'] = person_edu[0].strip()
                education_1['major'] = person_edu[1].strip()
                education_1['degree'] = person_edu[2].strip()

                education_time = cell.xpath('./time/text()').extract()[0].replace(' ', '').split('-')
                education_1['during_start'] = education_time[0].replace('/', '-') + '-01'
                education_1['during_end'] = '9999-01-01' if '至今' in education_time[1] else education_time[1].replace(
                    '/', '-') + '-01'

                jljx_lp_data['educations'].append(education_1)

            except:
                print(traceback.format_exc())

    def split_up(wordList):
        lis = []
        for jj in wordList:
            if '(' in jj and ')' in jj:
                g = re.match(r'(.*?)\((.*?)\)', jj).groups()
                if '、' in g[1]:
                    level = g[1].split('、')[1].strip()
                else:
                    level = g[1].strip()
                if level in ['简单沟通', '读写精通', '商务洽谈', '同声翻译']:
                    lis.append((g[0].strip(), level))
                else:
                    lis.append((g[0].strip(),))
            else:
                lis.append((jj.strip(),))

        return lis

    # 语言能力
    languages = sel.xpath('//section[@class="language-experience content-wrap"]/div[@class="sub-wrap"]')
    if bool(languages):
        try:
            language = languages[0].xpath(
                './ul/li/label[@class="labels labels-blue float-left language"]/span/text()').extract()
            result = split_up(language)
            for cell_1 in result:
                language_1 = dict()
                language_1['language'] = cell_1[0]
                if len(cell_1) == 2:
                    language_1['writing'] = language_1['speaking'] = cell_1[1]
                jljx_lp_data['languages'].append(language_1)

            skill = languages[0].xpath('./ul/li/label[@class="labels labels-blue float-left"]/span/text()').extract()
            for cell_1 in skill:
                skill_1 = dict()
                skill_1['skill'] = cell_1
                jljx_lp_data['languages'].append(skill_1)

        except:
            print(traceback.format_exc())

    # 自我评价
    evaluation = sel.xpath('//section[@class="attach-info content-wrap"]/div[@class="sub-wrap"]')
    if bool(evaluation):
        try:
            self_evaluation = evaluation[0].xpath(
                './/p[contains(text(), "自我评价")]/following-sibling::p[1]/text()').extract()
            if bool(self_evaluation):
                jljx_lp_data['objective']['self_evaluation'] = ''.join([i.strip() for i in self_evaluation]).strip()
        except:
            print(traceback.format_exc())

    # 工作经验
    jobs = sel.xpath('//section[@class="work-experience content-wrap"]/div[@class="sub-wrap"]')
    if bool(jobs):
        jobs = jobs[0].xpath('./div[@class="work-cont"]')
        for cell in jobs:
            job_1 = {}
            work_cont_company = cell.xpath('./div[@class="work-cont-company"]')
            if work_cont_company:
                work_cont_company = work_cont_company[0]
                try:
                    job_time = work_cont_company.xpath('./div[1]/p[2]/text()').extract()[0].replace(' ', '').split('(')[
                        0].split('-')
                    job_1['during_start'] = job_time[0].replace('/', '-') + '-01'
                    job_1['during_end'] = '9999-01-01' if '至今' in job_time[1] else job_time[1].replace('/', '-') + '-01'
                except:
                    print(traceback.format_exc())
                try:
                    job_1['company'] = work_cont_company.xpath('./div[1]/p[1]/span[1]/text()').extract()[0].strip()
                except:
                    print(traceback.format_exc())
                try:
                    job_group = re.search(r'公司行业(.*?)公司地点(.*?)公司规模(.*?)公司性质(.*?)</div>', work_cont_company.extract(),
                                          re.S).groups()
                    if '<span>' in job_group[0]:
                        job_1['trade'] = re.search(r'<span>(.*?)</span>', job_group[0]).group(1)
                    if '<span>' in job_group[2]:
                        job_1['company_scale'] = re.search(r'<span>(.*?)</span>', job_group[2]).group(1)
                    if '<span>' in job_group[3]:
                        job_1['company_nature'] = re.search(r'<span>(.*?)</span>', job_group[3]).group(1)
                except:
                    print(traceback.format_exc())

                try:
                    job_1['job_title'] = work_cont_company.xpath('./div[3]/p[1]/text()').extract()[0].strip()
                except:
                    print(traceback.format_exc())

            work_cont_other = cell.xpath('./div[@class="work-cont-other"]')
            if work_cont_other:
                work_cont_other = work_cont_other[0]
                try:
                    department = work_cont_other.xpath(
                        './/span[contains(text(), "所在部门")]/following-sibling::span[1]/text()').extract()
                    if department:
                        job_1['department'] = department[0].strip()

                    boss = work_cont_other.xpath(
                        './/span[contains(text(), "汇报对象")]/following-sibling::span[1]/text()').extract()
                    if boss:
                        job_1['boss'] = boss[0].strip()

                    subordinates = work_cont_other.xpath(
                        './/span[contains(text(), "下属人数")]/following-sibling::span[1]/text()').extract()
                    if subordinates:
                        job_1['subordinates'] = subordinates[0].strip()

                    monthly_salary = work_cont_other.xpath(
                        './/span[contains(text(), "薪酬情况")]/following-sibling::span[1]/text()').extract()
                    if monthly_salary:
                        monthly_salary = monthly_salary[0].strip()
                        if monthly_salary not in ['保密', '未填']:
                            job_1['monthly_salary_lower'] = job_1['monthly_salary_upper'] = round(
                                float(monthly_salary) * 12, 1)
                except:
                    print(traceback.format_exc())

            work_cont_list = cell.xpath('./div[@class="work-cont-list"]')
            if work_cont_list:
                work_cont_list = work_cont_list[0]
                try:
                    achievements = work_cont_list.xpath(
                        './/dt[contains(text(), "职责业绩")]/following-sibling::dd[1]/span/text()').extract()
                    if achievements:
                        job_1['achievements'] = ''.join([i.strip() for i in achievements]).strip()
                except:
                    print(traceback.format_exc())

            jljx_lp_data['jobs'].append(job_1)

    jljx_lp_data['org'] = {}
    jljx_lp_data['org']['org_id'] = org_id
    try:
        if jljx_lp_data['info']['email']:
            jljx_lp_data['org']['download_status'] = 1
    except:
        jljx_lp_data['org']['download_status'] = 0

    # 插件
    if lx == 3:
        # jljx_lp_data['org']['update_time'] = str(datetime.datetime.now())[0:10]
        jljx_lp_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        jljx_lp_data['org']['resume_type'] = 3
    # 搜索/推荐
    elif lx == 2:
        jljx_lp_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        if job_id:
            jljx_lp_data['org']['job_id'] = job_id
            jljx_lp_data['org']['resume_type'] = 2
    # 收件箱
    elif lx == 1:
        jljx_lp_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        jljx_lp_data['org']['resume_type'] = 1
        if job_id:
            jljx_lp_data['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    return jljx_lp_data


class Module_lp(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_lp, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    # 猎聘登录判断
    def login_judge_lp(self):
        home_url = 'https://lpt.liepin.com/privilege/getwillexpireresource.json'
        response = self.session.post(url=home_url, headers=self.headers)
        res = json.loads(response.text)
        return {'L_COIN': int(res['data']['L_COIN']['leftResourceCount']), 'CV_DOWNLOAD': int(res['data']['CV_DOWNLOAD']['leftResourceCount'])}

    # 猎聘职位刷新
    def refresh_job_lp(self, JobID):
        refresh_url = 'https://lpt.liepin.com/ejob/refreshejobs.json'
        data = {
            'ejob_ids': JobID
        }
        headers = get_useragent()
        headers['X-Requested-With'] = 'XMLHttpRequest'
        response = self.session.post(url=refresh_url, headers=headers, data=data)
        flag = json.loads(response.text)['flag']
        return flag

    # 猎聘简历搜索下载
    def search_lp(self, userid, download_way):
        search_url = 'https://lpt.liepin.com/resume/showresumedetail/?res_id_encode={userid}'.format(userid=userid)
        search_response = self.session.get(url=search_url, headers=self.headers)
        if '抱歉，简历信息不存在或已被删除！' not in search_response.text:
            headers = get_useragent()
            headers['X-Requested-With'] = 'XMLHttpRequest'
            download_url = 'https://lpt.liepin.com/resume/downloadresume.json'
            resource_type = '22' if download_way == 1 else '20'
            data = {
                'res_id_encode': userid,
                'resource_type': resource_type
            }
            download_response = self.session.post(url=download_url, headers=headers, data=data)

            details_url = 'https://lpt.liepin.com/resume/showresumedetail/?res_id_encode={userid}'.format(userid=userid)
            details_response = self.session.get(url=details_url, headers=self.headers)

            # headers_job = get_useragent()
            # headers_job['X-Requested-With'] = 'XMLHttpRequest'
            # get_job_url = 'https://lpt.liepin.com/resume/getworkexps'
            # data_job = {
            #     'res_id_encode': userid,
            #     'language': '0',
            #     'v': '1.4',
            # }
            # job_response = self.session.post(url=get_job_url, headers=headers_job, data=data_job)

            return download_response, details_response
        else:
            return None, None

    # 询问
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
                        chanl_id = jl['resIdEncode']
                        td_date = jl['resModifytime']
                        if td_date == '':
                            td_date = today1
                        # print(chanl_id, td_date)
                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid  # 企业id
                            content['jobId'] = jobid
                            content['channel'] = 10
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
                        content['channel'] = 10
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
                        chanl_id = jl['resIdEncode']
                        td_date = jl['resModifytime']
                        if td_date == '':
                            td_date = today1
                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid
                            content['jobId'] = jobid
                            content['channel'] = 10
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
                        content['channel'] = 10
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
                        chanl_id = jl['resIdEncode']
                        td_date = jl['resModifytime']
                        if td_date == '':
                            td_date = today1
                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid
                            content['jobId'] = jobid
                            content['channel'] = 10
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
                        content['channel'] = 10
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

    # 猎聘简历搜索
    @staticmethod
    def search_resume_lp(data):
        searchValueHid = {
            'suggestKey': '',
            'searchRefer': '1',
            'cvSearchForm': '0',
            'searchKey': '',
            'filterKey': '',
            'degrade': '',
            'csCreateTimeFlag': '',
            'csCreateTime': '',
            'csId': '',
            'curPage': '0',
            'keys': '',
            'searchLevel': '',
            'dqs': '',
            'contains_wantdq': '1',
            'workyears': '',
            'edulevel': '',
            'industrys': '',
            'jobtitles': '',
            'updateDate': '01',
            'userStatus': '',
            'sex': '',
            'age': '',
            'yearSalarylow': '',
            'earSalaryhigh': '',
            'wantYearSalaryLow': '',
            'wantYearSalaryHigh': '',
            'sortflag': '',
            'filterDownload': '1',
        }
        return searchValueHid

    # 猎聘搜索简历
    def read_resume_lp(self, searchValueHid, orgid='111', jobid='', max_num=50):
        def paging(response_page):
            nonlocal data_wu_lp, ss_num, scpy_again, page

            time.sleep(random.uniform(5, 8))
            js = json.loads(response_page.text)

            # if '<input name="hidShowCode" type="hidden" id="hidShowCode" value="1" />' in response_page.text:
            #     logging.error('对不起,由于您的操作过于频繁,请输入验证码!')
            #     time.sleep(60*10)
            #     scpy_again = True
            #     return

            lis = js['data']['cvSearchResultForm']['cvSearchListFormList']
            if not lis:
                return

            ask_result = self.ask_before_read(lis, orgid, jobid)
            # ask_result = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
            for key, value in enumerate(lis):
                try:
                    ask_status = ask_result[key]
                except:
                    logging.error('date is not new，stop scrapy...')
                    return

                if ask_status == '1':
                    try:
                        details_url = 'https://lpt.liepin.com' + value.get('resumeUrl')
                        details_response = self.session.get(url=details_url, headers=get_useragent())

                        headers_job = get_useragent()
                        headers_job['X-Requested-With'] = 'XMLHttpRequest'
                        get_job_url = 'https://lpt.liepin.com/resume/getworkexps'
                        data_job = {
                            'res_id_encode': value.get('resIdEncode'),
                            'language': '0',
                            'v': '1.4',
                        }
                        job_response = self.session.post(url=get_job_url, headers=headers_job, data=data_job)

                        # while 1:
                        #     if '<input name="hidShowCode" type="hidden" id="hidShowCode" value="1" />' in details_response.text:
                        #         logging.error('对不起,由于您的操作过于频繁,请输入验证码!')
                        #         time.sleep(60*10)
                        #         details_response = self.session.get(url=details_url, headers=get_useragent(), data={'hidShowCode': '0'})
                        #     else:
                        #         break

                        final_data = jx_lp_ss(text=details_response.text, job_text=job_response.text, ds=0, org_id=orgid, job_id=jobid, lx=2)
                        print(final_data)
                        print('\n')
                        data_wu_lp.append(final_data)
                        ss_num = ss_num + 1

                    except:
                        logging.exception("Exception Logged")
                        logging.error("this jl parse wrong...")
                        continue

                    if ss_num >= max_num:
                        return

                    if len(data_wu_lp) == 3:
                        data = json.dumps(data_wu_lp)
                        data = data.encode('utf-8')
                        requests.post(url=wu_jl_url, data=data)
                        data_wu_lp = []

                    time.sleep(random.uniform(5, 8))

            page += 1
            searchValueHid['curPage'] = str(page)
            headers = get_useragent()
            headers['X-Requested-With'] = 'XMLHttpRequest'
            response_page = self.session.post(url=url, headers=headers, data=searchValueHid)
            paging(response_page)

        data_wu_lp = []
        ss_num = 0
        page = 0

        url = 'https://lpt.liepin.com/cvsearch/search.json'
        while 1:
            scpy_again = False
            headers = get_useragent()
            headers['X-Requested-With'] = 'XMLHttpRequest'
            response = self.session.post(url=url, headers=headers, data=searchValueHid)
            paging(response)
            if not scpy_again:
                break

        if len(data_wu_lp) > 0:
            data = json.dumps(data_wu_lp)
            data = data.encode('utf-8')
            requests.post(url=wu_jl_url, data=data)
            data_wu_lp = []

        return ss_num
