# -*- coding: utf-8 -*-：

from scrapy.selector import Selector
import requests
import datetime
import json
from settings import *
from al_qf import *
import logging

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


def get_date(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)

def login_judge_zhyc(cookie):
    headers={
    'User-Agent':get_useragent(),
    'Cookie':cookie,
    }
    url_zy="http://qy.chinahr.com/resource/isChrCoinUser"
    response_zy = requests.post(url=url_zy, headers=headers).text
    dict_re=json.loads(response_zy)
    coin_num= dict_re['entity']
    # print(coin_num)
    return coin_num

def zw_shua_xi(cookie,job_id):
    url_sx="http://qy.chinahr.com/bjobmanager/online/refreshSel/"
    headers={
        'User-Agent': get_useragent(),
        'Cookie': cookie,
    }
    data={'jobId':job_id}
    reponse_sx=requests.post(url=url_sx,headers=headers,data=data).text
    # print(reponse_sx)
    return reponse_sx


def jl_xiazai(cookie,jl_id,org_id):
    cvid= jl_id.split("cvid=")[1].split("&")[0]
    data_from = jl_id.split("from=")[1].split("&")[0]
    sign= jl_id.split("sign=")[1].split("&")[0]

    url_xz="http://qy.chinahr.com/cv/downresume"
    data = {
        'cvid': cvid,
        'from': data_from,
        'sign': sign
    }
    header_xz={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': get_useragent(),
        'Cookie': cookie,
    }
    response_xz = requests.post(url=url_xz, data=data, headers=header_xz).text
    print(response_xz)
    try:
        mobile = response_xz.replace('"', '').split("mobile:")[1].split(",")[0].strip()
        email = response_xz.replace('"', '').split("email:")[1].split("}")[0].strip()
    except:
        pass

    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent':get_useragent(),
        'Cookie': cookie,
    }
    url_jl="http://qy.chinahr.com/cvm/preview?"
    response_jl = requests.post(url=url_jl,data=data, headers=headers).text
    zhyc_data=jl_zhyc(text=response_jl,mobile=mobile,email=email,jl_id=jl_id,org_id=org_id,resume_type=2)
    return(mobile, email,zhyc_data)

def jl_zhyc(text,resume_type,mobile='',email='', jl_id='',ds=0, org_id='', job_id='',lx=0, dt=0,):
    # text = text.replace('#→start→#', '').replace('#←end←#', '')
    jl_zhyc_data = {}
    sel = Selector(text=text)
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_today = datetime.datetime.now().strftime('%Y-%m-%d')
    jl_zhyc_data['info'] = {}
    jl_zhyc_data['objective'] = {}
    jl_zhyc_data['jobs'] = []
    jl_zhyc_data['educations'] = []
    jl_zhyc_data['at_schools'] = []
    jl_zhyc_data['credentials'] = []
    jl_zhyc_data['languages'] = []
    jl_zhyc_data['trainings'] = []
    jl_zhyc_data['projects'] = []
    jl_zhyc_data['info']['channel'] = 6

    #电话号码,email
    if mobile != "":
        try:
            jl_zhyc_data['info']['mobilephone'] = mobile
        except:
            pass
    if email != "":
        try:
            jl_zhyc_data['info']['email'] = email
        except:
            # traceback.print_exc()
            pass
    # 更新时间
    try:
        channel_update_time=sel.xpath('string(//div[@class="rm-body"]/div/div[@class="num"]/p[1])').extract()[0]
        if '今天' in channel_update_time or '刚' in channel_update_time:
            jl_zhyc_data['info']['channel_update_time'] = now_today
        elif '昨天' in channel_update_time:
            yestoday_li = str(get_date(1))[:10]
            jl_zhyc_data['info']['channel_update_time'] = yestoday_li
        else:
            jl_zhyc_data['info']['channel_update_time'] = channel_update_time.split("更新时间：")[1].strip()
    except:
        pass
    # 简历ID
    try:
        if jl_id != "":
            jl_zhyc_data['info']['channel_resume_id'] = jl_id
    except:
        pass
    # 照片地址
    if sel.xpath('//div[@class="user-info"]/div[@class="photo"]/img/@src'):
        try:
            pho_url = sel.xpath('string(//div[@class="user-info"]/div[@class="photo"]/img/@src)').extract()[0]
            if 'http' not in pho_url:
                pho_url = 'http:' + pho_url
            jl_zhyc_data['info']['photo_url'] = pho_url
        except:
            pass
    #姓名
    try:
        jl_zhyc_data['info']['name'] = sel.xpath('//div[@class="per-info"]/div[@class="name"]/span/text()').extract()[0].strip()
    except:
        pass
    # 性别、出生年份、学历、参加工作年份、婚姻状况
    list_degree = ['其他', '初中', '中技', '中职', '中专', '职高', '高中', '高职', '大专', '本科', '硕士', 'MBA', 'EMBA', '博士', ]
    if sel.xpath('//div[@class="per-info"]/div[@class="age"]'):
        age_or_hk = sel.xpath('//div[@class="per-info"]/div[@class="age"]/em')
        for a_or_h in age_or_hk:
            a_h_v = a_or_h.xpath('text()').extract()[0].strip()
            if '男' in a_h_v or '女' in a_h_v:
                try:
                    jl_zhyc_data['info']['sex'] = a_h_v.strip()
                except:
                    pass
            elif '岁' in a_h_v:
                try:
                    jl_zhyc_data['info']['birth_year'] = int(now_year) - int(a_h_v.replace('岁', '').strip())
                except:
                    pass
            elif a_h_v in list_degree:
                try:
                    jl_zhyc_data['info']['degree'] = a_h_v.strip()
                except:
                    pass
            elif '工作经验' in a_h_v:
                try:
                    if "暂无" in a_h_v:
                        jl_zhyc_data['info']['start_working_year'] = int(now_year)
                    elif "以下" in a_h_v:
                        jl_zhyc_data['info']['start_working_year'] = int(now_year)-1
                    else:
                        jl_zhyc_data['info']['start_working_year'] = int(now_year) - int(a_h_v.replace('年工作经验', '').strip())
                except:
                    pass
            elif "未婚"in a_h_v or "已婚" in a_h_v:
                try:
                    jl_zhyc_data['info']['marital_status'] = a_h_v.strip()
                except:
                    pass
    #户籍、现居住地、海外经验
    if sel.xpath('//ul[@class="loc-info"]/li'):
        for loc_info in sel.xpath('//ul[@class="loc-info"]/li'):
            if loc_info.xpath('label/text()').extract()[0].strip() == "目前所在地：":
                try:
                    jl_zhyc_data['info']['current_address'] = loc_info.xpath('span/text()').extract()[0].strip()
                except:
                    pass
            elif loc_info.xpath('label/text()').extract()[0].strip() == "户口所在地：":
                try:
                    jl_zhyc_data['info']['residence_address'] = loc_info.xpath('span/text()').extract()[0].strip()
                except:
                    pass
            elif "海外"in  loc_info.xpath('label/text()').extract()[0].strip():
                jl_zhyc_data['info']['oversea_experience'] = 1

#各模块内容
    if sel.xpath('//div[@class="rm-detail"]'):
        for section in sel.xpath('//div[@class="rm-detail"]/div'):
            #求职意向
            section_name= section.xpath('string(h2)').extract()[0].strip()
            if "求职意向"in section_name:
                try:
                    for row in section.xpath('//div[@class="project"]/div'):
                        row_name=row.xpath('string(label)').extract()[0]
                        if "期望工作" in row_name:
                            try:
                                jl_zhyc_data['objective']['expected_job_title'] = []
                                expected_job_title=row.xpath('string(span)').extract()[0]
                            except:
                                pass
                            try:
                                for job_title in expected_job_title.split("|"):
                                    jl_zhyc_data['objective']['expected_job_title'].append(job_title.strip())
                            except:
                                pass
                        elif "期望行业" in row_name:
                            try:
                                jl_zhyc_data['objective']['trade'] = []
                                trade = row.xpath('string(span)').extract()[0]
                                for trade_title in trade.split("|"):
                                    jl_zhyc_data['objective']['trade'].append(trade_title.strip())
                            except:
                                pass
                        elif "求职性质" in row_name:
                            try:
                                jl_zhyc_data['objective']['job_nature'] = []
                                job_nature = row.xpath('string(span)').extract()[0]
                                jl_zhyc_data['objective']['job_nature'].append(job_nature.strip())
                            except:
                                pass
                        elif "工作状态" in row_name:
                            try:
                                jl_zhyc_data['objective']['work_status']=row.xpath('string(span)').extract()[0]
                            except:
                                pass
                        elif "期望地点" in row_name:
                            try:
                                jl_zhyc_data['objective']['expected_address'] = []
                                expected_address = row.xpath('string(span)').extract()[0]
                                for address in expected_address.split("|"):
                                    jl_zhyc_data['objective']['expected_address'].append(address.strip())
                            except:
                                pass
                        elif "期望薪水" in row_name:
                            try:
                                salary = row.xpath('string(span)').extract()[0]
                                jl_zhyc_data['objective']['expected_salary_lower'] = int(salary.replace(".0",""))
                                jl_zhyc_data['objective']['expected_salary_upper'] = int(salary.replace(".0",""))
                            except:
                                pass
                except:
                    pass
            if "个人评价" in section_name:
                try:
                    jl_zhyc_data['objective']['self_evaluation'] = section.xpath('string(div[@class="des"]/p)').extract()[0].replace("\r", "").replace("\n","").replace("\t","").replace(" ","")
                except:
                    pass

            #工作经历
            elif "工作经历" in section_name:
                try:
                    for project in section.xpath('div[@class="project"]'):
                        try:
                            job_exp = {}
                            company=project.xpath('string(div[@class="row item-title"])').extract()[0]
                            job_exp['company']= company.split("(")[0]
                            job_title= project.xpath('string(div[@class="row sub-title"])').extract()[0]
                            job_exp['job_title']= job_title.split("|")[0]
                            try:
                                monthly_salary = project.xpath('string(div[@class="row sub-title"]/em[@class="sub-des"])').extract()[0]
                                print(monthly_salary)
                                if "至" in monthly_salary:
                                    job_exp['monthly_salary_lower'] = int(monthly_salary.split("至")[0])
                                    job_exp['monthly_salary_upper'] = int(monthly_salary.split("至")[1].split("/月")[0])
                            except:
                                pass
                        except:
                            pass
                        #起止时间
                        try:
                            during_time=project.xpath('string(div/em)').extract()[0]
                            during_start=during_time.replace("(","").replace(")","").split("-")[0].replace(".","-").strip()
                            job_exp['during_start'] =during_start + "-01"
                            during_end= during_time.replace("(","").replace(")","").split("-")[1].replace(".","-").strip()
                            if "至今" in during_end:
                                job_exp['during_end'] ='9999-01-01'
                            else:
                                job_exp['during_end'] = during_end + "-01"
                        except:
                            pass
                        #所属行业、公司性质、公司规模、部门、职位类别、工作内容描述
                        try:
                            for row in project.xpath('div[@class="row"]'):
                                if "所属行业" in row.xpath('string(label)').extract()[0]:
                                    job_exp['trade']= row.xpath('string(span)').extract()[0].strip()
                                elif "公司性质" in row.xpath('string(label)').extract()[0]:
                                    company_xz=row.xpath('string(span)').extract()[0].strip()
                                    job_exp['company_nature']=company_xz.split("|")[0].strip()
                                    job_exp['company_scale'] = company_xz.split("|")[1].strip()
                                elif "所属部门" in row.xpath('string(label)').extract()[0]:
                                    job_exp['department']= row.xpath('string(span)').extract()[0].strip()
                                elif "工作内容" in row.xpath('string(label)').extract()[0]:
                                    job_exp['job_content']= row.xpath('string(span)').extract()[0].replace("\r", "").replace("\n","").replace("\t","").replace(" ","")
                        except:
                            pass
                        jl_zhyc_data['jobs'].append(job_exp)
                except:
                    pass

            #项目经历
            elif "项目经历" in section_name:
                try:
                    for project in section.xpath('div[@class="project"]'):
                        try:
                            project_exp = {}
                            title=project.xpath('string(div[@class="row item-title"])').extract()[0]
                            project_exp['title']= title.split("（")[0].strip()
                        except:
                            pass
                            #起止时间
                        try:
                            during_time=project.xpath('string(div/em)').extract()[0]
                            during_start=during_time.replace("（","").replace("）","").split("-")[0].replace(".","-").strip()
                            project_exp['during_start'] =during_start + "-01"
                            during_end= during_time.replace("（","").replace("）","").split("-")[1].replace(".","-").strip()
                            if "至今" in during_end:
                                project_exp['during_end'] ='9999-01-01'
                            else:
                                project_exp['during_end'] = during_end + "-01"
                        except:
                            pass
                        #职位描述、项目描述
                        try:
                            for row in project.xpath('div[@class="row"]'):
                                if "职责描述" in row.xpath('string(label)').extract()[0]:
                                    project_exp['duty']= row.xpath('string(span)').extract()[0].replace("\r", "").replace("\n","").replace("\t","").replace(" ","")
                                elif "项目描述" in row.xpath('string(label)').extract()[0]:
                                    project_exp['description']= row.xpath('string(span)').extract()[0].replace("\r", "").replace("\n","").replace("\t","").replace(" ","")
                        except:
                            pass
                        jl_zhyc_data['projects'].append(project_exp)

                except:
                    pass

            # 教育经历
            elif "教育经历" in section_name:
                try:
                    for project in section.xpath('div[@class="project"]'):
                        try:
                            edu_exp = {}
                            school = project.xpath('string(div[@class="row item-title"])').extract()[0]
                            edu_exp['school'] = school.split("（")[0].split("(")[0].strip()
                        except:
                            pass
                        # 起止时间
                        try:
                            during_time = project.xpath('string(div/em)').extract()[0]
                            during_start = during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[0].replace(".","-").strip()
                            edu_exp['during_start'] = during_start + "-01"
                            during_end = during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[1].replace(".","-").strip()
                            if "至今" in during_end:
                                edu_exp['during_end'] = '9999-01-01'
                            else:
                                edu_exp['during_end'] = during_end + "-01"
                        except:
                            pass
                        #学历、专业
                        try:
                            xue_zhuan = project.xpath('string(div[@class="row sub-title"])').extract()[0]
                            edu_exp['degree']=xue_zhuan.split("|")[0].strip()
                            edu_exp['major'] = xue_zhuan.split("|")[1].strip()
                            jl_zhyc_data['educations'].append(edu_exp)
                        except:
                            pass
                except:
                    pass

            # 培训经历
            elif "培训经历" in section_name:
                try:
                    for project in section.xpath('div[@class="project"]'):
                        try:
                            trainings_exp = {}
                            training_course = project.xpath('string(div[@class="row item-title"])').extract()[0]
                            trainings_exp['training_course'] = training_course.split("（")[0].strip()
                        except:
                            pass
                        # 起止时间
                        try:
                            during_time = project.xpath('string(div/em)').extract()[0]
                            during_start = \
                            during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[
                                0].replace(".", "-").strip()
                            trainings_exp['during_start'] = during_start + "-01"
                            during_end = \
                            during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[
                                1].replace(".", "-").strip()
                            if "至今" in during_end:
                                trainings_exp['during_end'] = '9999-01-01'
                            else:
                                trainings_exp['during_end'] = during_end + "-01"
                        except:
                            pass
                        #培训描述、培训机构
                        try:
                            for row in project.xpath('div[@class="row"]'):
                                if "培训机构" in row.xpath('string(label)').extract()[0]:
                                    trainings_exp['training_agency'] = row.xpath('string(span)').extract()[0].replace("\r", "").replace(
                                        "\n", "").replace("\t", "").replace(" ", "")
                                elif "培训描述" in row.xpath('string(label)').extract()[0]:
                                    trainings_exp['description'] = row.xpath('string(span)').extract()[0].replace("\r",
                                                                                                                "").replace(
                                        "\n", "").replace("\t", "").replace(" ", "")
                        except:
                            pass
                        jl_zhyc_data['trainings'].append(trainings_exp)
                except:
                    pass


            # 证书
            elif "证书" in section_name:
                try:
                    for project in section.xpath('div[@class="project"]'):
                        try:
                            credentials = {}
                            title = project.xpath('string(div[@class="row item-title"])').extract()[0]
                            credentials['title'] = title.split("（")[0].strip()
                        except:
                            pass
                        # 起止时间
                        try:
                            during_time = project.xpath('string(div/em)').extract()[0]
                            during_start = \
                                during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("获得")[
                                    0].replace(".", "-").strip()
                            credentials['get_date'] = during_start + "-01"
                        except:
                            pass
                        jl_zhyc_data['credentials'].append(credentials)
                except:
                    pass

            # 技能、语言
            elif "技能" in section_name:
                try:
                    for project in section.xpath('div[@class="skill"]/ul/li'):
                        ji_neng = {}
                        ji_ne = project.xpath('string()').extract()[0]
                        ji_neng['skill'] = ji_ne.split("|")[0].strip()
                        ji_neng['level'] = ji_ne.split("|")[1].strip()
                        jl_zhyc_data['languages'].append(ji_neng)
                except:
                    pass

    # org
    jl_zhyc_data['org'] = {}
    jl_zhyc_data['org']['resume_type'] = resume_type
    jl_zhyc_data['org']['org_id'] = org_id
    try:
        if jl_zhyc_data['info']['mobilephone']:
            jl_zhyc_data['org']['download_status'] = 1
    except:
        jl_zhyc_data['org']['download_status'] = 0

    # 工作ID
    try:
        if job_id != "":
            jl_zhyc_data['org']['job_id'] = job_id
    except:
        pass

    # # # 插件
    # # jl_zhyc_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # # # 搜索/推荐----------遇仁职位ID
    # # if lx == 2:
    # #     jl_zhyc_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # #     if job_id:
    # #         jl_zhyc_data['org']['job_id'] = job_id
    # # # 收件箱--------------渠道职位ID
    # # elif lx == 1:
    # #     jl_zhyc_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # #     if job_id:
    # #         jl_zhyc_data['org']['job_id'] = job_id
    # # # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    # # if dt:
    # #     jl_zhyc_data['org']['delivery_time'] = dt
    # print(jl_zhyc_data)
    return jl_zhyc_data
