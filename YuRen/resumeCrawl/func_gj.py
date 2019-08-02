import requests
import json
from lxml.html import etree
import datetime
import time
import re
import logging
from scrapy.selector import Selector
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

def get_date(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)


def riqizhaunhuan(xx):
    xx_li = xx.split('-')
    for index,value in enumerate(xx_li):
        if int(value) <= 9 and len(str(value)) == 1:
            xx_li_temp = '0' + str(value)
            xx_li[index] = xx_li_temp
    return '-'.join(xx_li)


def jljx_gjw(text, ds=0, org_id='111', job_id='',lx=0, dt=0):
    # text = text.replace('#→start→#', '').replace('#←end←#', '')
    jljx_gjw_data = {}
    sel = Selector(text=text)
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_today = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(now_today)
    # print(now_year)
    # print(now_month)
    jljx_gjw_data['info'] = {}
    jljx_gjw_data['objective'] = {}
    jljx_gjw_data['jobs'] = []
    jljx_gjw_data['educations'] = []
    jljx_gjw_data['at_schools'] = []
    jljx_gjw_data['credentials'] = []
    jljx_gjw_data['languages'] = []
    jljx_gjw_data['trainings'] = []
    jljx_gjw_data['projects'] = []
    jljx_gjw_data['info']['channel'] = 4
    # 电话号码
    if sel.xpath('//ul[@id="js_contact_container"]/li/span[@class="orange"]'):
        try:
            jljx_gjw_data['info']['mobilephone'] = sel.xpath('//ul[@id="js_contact_container"]/li/span[@class="orange"]/@data-phone').extract()[0].strip()
        except:
            pass
        try:
            jljx_gjw_data['info']['email'] = sel.xpath('//ul[@id="js_contact_container"]/li[@data-role="viewEmail"]/span[@class="orange"]/text()').extract()[0].strip()
            # print(jljx_gjw_data['info']['email'])
        except:
            # traceback.print_exc()
            pass

    # 更新时间
    if sel.xpath('//span[text()="更新时间："]/parent::div/strong'):
        try:
            jljx_gjw_data['info']['channel_update_time'] = sel.xpath('//span[text()="更新时间："]/parent::div/strong/text()').extract()[0]
            if '今天' in jljx_gjw_data['info']['channel_update_time'] or '刚' in jljx_gjw_data['info']['channel_update_time']:
                jljx_gjw_data['info']['channel_update_time'] = now_today
            elif '昨天' in jljx_gjw_data['info']['channel_update_time']:
                yestoday_li = str(get_date(1))[:10]
                jljx_gjw_data['info']['channel_update_time'] = yestoday_li
        except:
            pass
    # 简历ID
    puid = sel.xpath('//span[@id="deliverAndDownload"]/@data-puid').extract()[0].strip()
    # data_hash = sel.xpath('//span[@id="deliverAndDownload"]/@data-hash').extract()[0].strip()
    jljx_gjw_data['info']['channel_resume_id'] = puid
    # 照片地址
    if sel.xpath('//div[@class="resume-avatar"]/img/@src'):
        try:
            pho_url = sel.xpath('//div[@class="resume-avatar"]/img/@src').extract()[0]
            if 'http:' not in pho_url:
                pho_url = 'http:' + pho_url
            jljx_gjw_data['info']['photo_url'] = pho_url
        except:
            pass
    # 年龄、户口
    # if sel.xpath('//div[@class="resume-lines"]/div[@class="name-line"]'):
    jljx_gjw_data['info']['name'] = sel.xpath('//div[@class="resume-lines"]/div[@class="name-line"]/strong/text()').extract()[0].strip()
    jljx_gjw_data['info']['sex'] = sel.xpath('//div[@class="resume-lines"]/div[@class="name-line"]/span[not(@class)]/text()').extract()[0].strip()
    age_or_hk = sel.xpath('//div[@class="resume-lines"]/div[@class="name-line"]/span[@class="left-border"]')
    for a_or_h in age_or_hk:
        a_h_v = a_or_h.xpath('text()').extract()[0].strip()
        if '人' in a_h_v:
            try:
                jljx_gjw_data['info']['residence_address'] = a_h_v.split('人')[0].strip()
            except:
                pass
        elif '岁' in a_h_v:
            try:
                jljx_gjw_data['info']['birth_year'] = int(now_year) - int(a_h_v.replace('岁', '').strip())
            except:
                pass
    # print(jljx_gjw_data)
    # 工作年限
    if sel.xpath('//div[@class="resume-lines"]/div[@class="college-line clearfix"]'):
        try:
            wy_str = sel.xpath('//div[@class="resume-lines"]/div[@class="college-line clearfix"]/div[@class="right-box"]/b/text()').extract()[0]
            try:
                info_xl_str = sel.xpath('//div[@class="resume-lines"]/div[@class="college-line clearfix"]/div[@class="left-box"]/b/text()').extract()[0]
                jljx_gjw_data['info']['degree'] = info_xl_str
            except:
                pass
            if '无' in wy_str or '在读' in wy_str or '应届' in wy_str:
                jljx_gjw_data['info']['start_working_year'] = int(now_year)
            elif '以内' in wy_str:
                jljx_gjw_data['info']['start_working_year'] = int(now_year) - 1
            elif '以上' in wy_str:
                jljx_gjw_data['info']['start_working_year'] = int(now_year) - 10
            else:
                try:
                    jljx_gjw_data['info']['start_working_year'] = int(now_year) - int(wy_str.replace('年', '').split('-')[1])
                except:
                    pass
        except:
            pass

    # 个人标签
    if sel.xpath('//div[@class="tags-line clearfix"]/ul/li'):
        jljx_gjw_data['objective']['individual_label'] = []
        indi_li = sel.xpath('//div[@class="tags-line clearfix"]/ul/li')
        for indi in indi_li:
            try:
                indi_str = indi.xpath('text()').extract()[0]
                jljx_gjw_data['objective']['individual_label'].append(indi_str)
            except:
                pass
        # print(jljx_gjw_data['objective']['individual_label'])
    # 期望薪资已见分类：面议--5000-8000元---200元/天--8000-12000元--100元/天--3000-5000元--20000元以上--12000-20000元--150元/天--2000-3000元--130元/天--10000元/天--77元/天
    # 期望薪资
    if sel.xpath('//div[@class="resume-lines"]/div[@class="salary-line clearfix"]'):
        try:
            jljx_gjw_data['objective']['expected_address'] = []
            salary_str = sel.xpath('//div[@class="resume-lines"]/div[@class="salary-line clearfix"]/div[@class="left-box"]/b/text()').extract()[0]
            try:
                gzdd_str = sel.xpath('//div[@class="resume-lines"]/div[@class="salary-line clearfix"]/div[@class="right-box"]/b/text()').extract()[0]
                gzdd_str = gzdd_str.split('-')[0].strip()
                jljx_gjw_data['objective']['expected_address'].append(gzdd_str)
                # print(qz_text)
            except:
                pass
            if '元/天' in salary_str:
                sala_obj = int(salary_str.split('元/天')[0].strip())*22.5
                jljx_gjw_data['objective']['expected_salary_lower'] = int(sala_obj)
                jljx_gjw_data['objective']['expected_salary_upper'] = int(sala_obj)
            elif '面议' in salary_str:
                jljx_gjw_data['objective']['expected_salary_lower'] = 0
                jljx_gjw_data['objective']['expected_salary_upper'] = 0
            elif '以上' in salary_str or '以下' in salary_str:
                sala_obj = salary_str.split('元')[0].strip()
                jljx_gjw_data['objective']['expected_salary_lower'] = int(sala_obj)
                jljx_gjw_data['objective']['expected_salary_upper'] = int(sala_obj)
            else:
                sala_obj_li = salary_str.split('元')[0].strip().split('-')
                jljx_gjw_data['objective']['expected_salary_lower'] = int(sala_obj_li[0])
                jljx_gjw_data['objective']['expected_salary_upper'] = int(sala_obj_li[1])
        except:
            pass
    # 期望job
    if sel.xpath('//div[@class="resume-lines"]/div[@class="tend-line clearfix"]'):
            jljx_gjw_data['objective']['expected_job_title'] = []
            zwzn_list = sel.xpath('//div[@class="resume-lines"]/div[@class="tend-line clearfix"]/b/a')
            for zwzn in zwzn_list:
                try:
                    zwzn_str = zwzn.xpath('text()').extract()[0]
                    jljx_gjw_data['objective']['expected_job_title'].append(zwzn_str)
                except:
                    pass
    # 自我评价
    if sel.xpath('//div[@class="detail-info"]/div[@class="self-block"]'):
        try:
            self_str = sel.xpath('string(//div[@class="detail-info"]/div[@class="self-block"]/div)').extract()[0]
            jljx_gjw_data['objective']['self_evaluation'] = self_str.replace(' ', '').replace('\n', '；').replace('\r', '；').replace('\r\n', '；')
        except:
            pass
    # 工作经历
    if sel.xpath('//div[@class="detail-info"]/div[@class="experience-block"]'):
        job_list = sel.xpath('//div[@class="detail-info"]/div[@class="experience-block"]/b')
        job_sumnum = len(job_list)
        for job_num in range(1, job_sumnum+1):
            xpa_job_cont = '//div[@class="detail-info"]/div[@class="experience-block"]/ul[' + str(job_num) + ']/li'
            xpa_job_comp = '//div[@class="detail-info"]/div[@class="experience-block"]/b[' + str(job_num) + ']/text()'
            job_1 = {}
            job_1['company'] = sel.xpath(xpa_job_comp).extract()[0].strip()
            # print(jobs_51['company'])
            cont_li = sel.xpath(xpa_job_cont)
            for cont in cont_li:
                cont_title = cont.xpath('span/text()').extract()[0]
                # print(cont_title)
                if '时间' in cont_title:
                    try:
                        cont_sj = cont.xpath('p/text()').extract()[0]
                        job_start_str = cont_sj.split('至')[0].replace('年', '-').replace('月', '').strip()
                        if len(job_start_str.split('-')[1]) == 1:
                            job_1['during_start'] = job_start_str.split('-')[0] + '-0' + job_start_str.split('-')[1] + '-01'
                        else:
                            job_1['during_start'] = job_start_str + '-01'
                        job_end_str = cont_sj.split('至')[1]
                        if '今' in job_end_str:
                            job_1['during_end'] = '9999-01-01'
                        else:
                            try:
                                job_end_str = job_end_str.replace('年', '-').replace('月', '').strip()
                                if len(job_end_str.split('-')[1]) == 1:
                                    job_1['during_end'] = job_end_str.split('-')[0] + '-0' + job_end_str.split('-')[1] + '-01'
                                else:
                                    job_1['during_end'] = job_end_str + '-01'
                            except:
                                pass
                    except:
                        pass
                elif '职位' in cont_title:
                    try:
                        cont_zw = cont.xpath('p/text()').extract()[0]
                        job_1['job_title'] = cont_zw.strip()
                    except:
                        pass
                elif '内容' in cont_title:
                    try:
                        desc_cont = cont.xpath('string(p)').extract()[0]
                        job_1['job_content'] = desc_cont.replace(' ', '').replace('\n', '；').replace('\r', '；').replace('\r\n', '；').replace('<br />','').replace('<br/>','')
                    except:
                        pass
            jljx_gjw_data['jobs'].append(job_1)
    # 语言能力
    if sel.xpath('//div[@class="detail-info"]/div[@class="project-block lang-block clearfix"]/p'):
        ski_li = sel.xpath('//div[@class="detail-info"]/div[@class="project-block lang-block clearfix"]/p')
        for ski in ski_li:
            try:
                skill_dict = {}
                skill_dict['language'] = ski.xpath('text()').extract()[0].split('：')[0].strip()
                skill_dict['writing'] = ski.xpath('text()').extract()[0].split('：')[1].strip()
                skill_dict['speaking'] = ski.xpath('text()').extract()[0].split('：')[1].strip()
                jljx_gjw_data['languages'].append(skill_dict)
            except:
                pass
    # 教育经历
    if sel.xpath('//div[@class="detail-info"]/div[@class="education-block"]/table'):
        edu_li = sel.xpath('//div[@class="detail-info"]/div[@class="education-block"]/table/descendant::tr')
        for edu in edu_li:
            try:
                jyjl_dic = {}
                jyjl_end_str = edu.xpath('td[1]/text()').extract()[0].split('毕业')[0].replace('年', '-').replace('月', '')
                if len(jyjl_end_str.split('-')[1]) == 1:
                    jyjl_dic['during_end'] = jyjl_end_str.split('-')[0] + '-0' + jyjl_end_str.split('-')[1] + '-01'
                else:
                    jyjl_dic['during_end'] = jyjl_end_str + '-01'
                jyjl_dic['major'] = edu.xpath('td[3]/text()').extract()[0].strip()
                jyjl_dic['school'] = edu.xpath('td[2]/text()').extract()[0].strip()
                jljx_gjw_data['educations'].append(jyjl_dic)
            except:
                pass
    # 源码类似板块
    xpa_leisi = '//div[@class="detail-info"]/div[@class="project-block"]'
    for lsbk in sel.xpath(xpa_leisi):
        # print(lsbk.xpath('string(h3)').extract()[0].strip())
        if '专业技能' in lsbk.xpath('string(h3)').extract()[0].strip():
            xpa_zyjn_li = 'table/descendant::tr'
            for zyjn in lsbk.xpath(xpa_zyjn_li):
                ski_dic = {}
                try:
                    ski_dic['skill'] = zyjn.xpath('td[not(@title)]/text()').extract()[0].split('：')[0].strip()
                except:
                    pass
                try:
                    ski_dic['level'] = zyjn.xpath('td[not(@title)]/text()').extract()[0].split('：')[1].strip()
                except:
                    pass
                try:
                    ski_dic['duration'] = zyjn.xpath('td[@title]/text()').extract()[0].split('：')[1].strip()
                except:
                    pass
                jljx_gjw_data['languages'].append(ski_dic)
        elif '项目/培训经验' in lsbk.xpath('string(h3)').extract()[0]:
            pxjl_li = lsbk.xpath('ul/li')
            for pxjl in pxjl_li:
                try:
                    px_dict = {}
                    # 此处p标签内容按正常死活解析不出来，但是当作和h4同级标签就可以解出

                    px_dict['certificate'] = pxjl.xpath('string(p)').extract()[0].strip()
                    px_sj = pxjl.xpath('h4/span/text()').extract()[0].strip()
                    px_sj_start = px_sj.split('-')[0].replace('年', '-').replace('月', '').strip()
                    if len(px_sj_start.split('-')[1]) == 1:
                        px_dict['during_start'] = px_sj_start.split('-')[0] + '-0' + px_sj_start.split('-')[1] + '-01'
                    else:
                        px_dict['during_start'] = px_sj_start + '-01'
                    px_sj_end = px_sj.split('-')[1]
                    if '今' in px_sj_end:
                        px_dict['during_end'] = '9999-01-01'
                    else:
                        px_sj_end = px_sj_end.replace('年', '-').replace('月', '').strip()
                        if len(px_sj_end.split('-')[1]) == 1:
                            px_dict['during_end'] = px_sj_end.split('-')[0] + '-0' + px_sj_end.split('-')[1] + '-01'
                        else:
                            px_dict['during_end'] = px_sj_end + '-01'
                    pxjl_cont_li = pxjl.xpath('div')
                    for pxjl_cont in pxjl_cont_li:
                        pxjl_cont_title = pxjl_cont.xpath('span/text()').extract()[0]
                        if '机构' in pxjl_cont_title:
                            try:
                                px_dict['training_agency'] = pxjl_cont.xpath('p/text()').extract()[0].strip()
                            except:
                                pass
                        elif '内容' in pxjl_cont_title:
                            try:
                                px_dict['description'] = pxjl_cont.xpath('p/text()').extract()[0].strip()
                            except:
                                pass
                    jljx_gjw_data['trainings'].append(px_dict)
                except:
                    pass
        elif '证书奖项' in lsbk.xpath('string(h3)').extract()[0]:
            zs_li = lsbk.xpath('table/descendant::tr')
            for zs in zs_li:
                zs_dict = {}
                if zs.xpath('td[@class="cert-name"]'):
                    try:
                        zs_dict['title'] = zs.xpath('td[@class="cert-name"]/text()').extract()[0].strip().split('：')[
                            1].strip()
                    except:
                        pass
                if zs.xpath('td[not(@class)]'):
                    try:
                        getdate_str = zs.xpath('td[not(@class)]/text()').extract()[0].split('：')[1].strip()
                        zs_dict['get_date'] = getdate_str.replace('年', '-').replace('月', '') + '-01'
                    except:
                        pass
                jljx_gjw_data['credentials'].append(zs_dict)

    jljx_gjw_data['org'] = {}

    jljx_gjw_data['org']['org_id'] = org_id
    try:
        if jljx_gjw_data['info']['mobilephone']:
            jljx_gjw_data['org']['download_status'] = 1
    except:
        jljx_gjw_data['org']['download_status'] = 0
    # 插件
    jljx_gjw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 收件箱--------------渠道职位ID
    if lx == 1:
        jljx_gjw_data['org']['resume_type'] = 1
        jljx_gjw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        if job_id:
            jljx_gjw_data['org']['job_id'] = job_id
    # 搜索/推荐----------遇仁职位ID
    elif lx == 2:
        jljx_gjw_data['org']['resume_type'] = 2
        jljx_gjw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        if job_id:
            jljx_gjw_data['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    if dt:
        jljx_gjw_data['org']['delivery_time'] = dt
    # print(jljx_gjw_data)
    return jljx_gjw_data

def jljx_gjw_jz(text, ds=0, org_id='111', job_id='',lx=0, dt=0):
    # text = text.replace('#→start→#', '').replace('#←end←#', '')
    jljx_gjw_data = {}
    sel = Selector(text=text)
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_today = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(now_today)
    # print(now_year)
    # print(now_month)
    jljx_gjw_data['info'] = {}
    jljx_gjw_data['objective'] = {}
    jljx_gjw_data['jobs'] = []
    jljx_gjw_data['educations'] = []
    jljx_gjw_data['at_schools'] = []
    jljx_gjw_data['credentials'] = []
    jljx_gjw_data['languages'] = []
    jljx_gjw_data['trainings'] = []
    jljx_gjw_data['projects'] = []
    jljx_gjw_data['info']['channel'] = 4
    xpa_name = '//span[@class="offer_name"]/text()'
    xpa_age_sex = '//span[@class="offer_age"]/text()'

    jljx_gjw_data['info']['name'] = sel.xpath(xpa_name).extract()[0]
    sex_age_str = sel.xpath(xpa_age_sex).extract()[0]
    if '女' in sex_age_str:
        jljx_gjw_data['info']['sex'] = '女'
    else:
        jljx_gjw_data['info']['sex'] = '男'
    jljx_gjw_data['info']['birth_year'] = int(now_year) - int(sex_age_str.split('，')[1].split('岁')[0])

    if sel.xpath('//span[@class="offer_name"]/parent::div/p/span[not(@id)]'):
        try:
            update_str = sel.xpath('//span[@class="offer_name"]/parent::div/p/span[not(@id)]/text()').extract()[0].strip()
            # print(update_str)
            if '今天' in update_str or '刚' in update_str:
                jljx_gjw_data['info']['channel_update_time'] = now_today
            elif '昨天' in update_str:
                yestoday_li = str(get_date(1))[:10]
                jljx_gjw_data['info']['channel_update_time'] = yestoday_li
            else:
                jljx_gjw_data['info']['channel_update_time'] = update_str
            jljx_gjw_data['info']['channel_update_time'] = riqizhaunhuan(jljx_gjw_data['info']['channel_update_time'])
        except:
            pass
    if sel.xpath('//div[@class="resume-avatar"]/img/@src'):
        try:
            pho_url = sel.xpath('//div[@class="resume-avatar"]/img/@src').extract()[0]
            if 'http:' not in pho_url:
                pho_url = 'http:' + pho_url
            jljx_gjw_data['info']['photo_url'] = pho_url
        except:
            pass
    puid = sel.xpath('//span[@id="deliverAndDownload"]/@data-puid').extract()[0].strip()
    # data_hash = sel.xpath('//span[@id="deliverAndDownload"]/@data-hash').extract()[0].strip()
    jljx_gjw_data['info']['channel_resume_id'] = puid
    xpa_li = '//ul[@id="js_contact_container"]/li'
    for ele_1 in sel.xpath(xpa_li):
        ele_str = ele_1.xpath('string()').extract()[0]
        if '最高学历：' in ele_str:
            jljx_gjw_data['info']['degree'] = ele_str.split('最高学历：')[1].strip()
        elif '期望日薪：' in ele_str:
            salary_str = ele_str.split('期望日薪：')[1].split('元')[0].strip()
            try:
                sala_obj = int(salary_str) * 22.5
                jljx_gjw_data['objective']['expected_salary_lower'] = int(sala_obj)
                jljx_gjw_data['objective']['expected_salary_upper'] = int(sala_obj)
            except:
                pass
        elif '期望地区：' in ele_str:
            jljx_gjw_data['objective']['expected_address'] = []
            try:
                gzdd_str = ele_str.split('期望地区：')[1].strip()
                jljx_gjw_data['objective']['expected_address'].append(gzdd_str)
            except:
                pass
        elif '工作年限：' in ele_str:
            try:
                wy_str = ele_str.split('工作年限：')[1].strip()
                if '无' in wy_str or '在读' in wy_str or '应届' in wy_str:
                    jljx_gjw_data['info']['start_working_year'] = int(now_year)
                elif '以内' in wy_str:
                    jljx_gjw_data['info']['start_working_year'] = int(now_year) - 1
                elif '以上' in wy_str:
                    jljx_gjw_data['info']['start_working_year'] = int(now_year) - 10
                else:
                    try:
                        jljx_gjw_data['info']['start_working_year'] = int(now_year) - int(wy_str.replace('年', '').split('-')[1])
                    except:
                        pass
            except:
                pass
        elif '期望职位：' in ele_str:
            jljx_gjw_data['objective']['expected_job_title'] = []
            zwzn_str = ele_str.split('期望职位：')[1].strip()
            jljx_gjw_data['objective']['expected_job_title'].append(zwzn_str)
        elif '籍　　贯：' in ele_str:
            hjjg_str = ele_str.split('籍　　贯：')[1].strip()
            jljx_gjw_data['objective']['residence_address'] = hjjg_str
    xpa_self = '//div[@class="nrcon lht24"]'
    if sel.xpath(xpa_self):
        self_str = sel.xpath('string(//div[@class="nrcon lht24"])').extract()[0]
        jljx_gjw_data['objective']['self_evaluation'] = self_str.replace(' ', '').replace('\n', '').replace('\r', '').replace( '\r\n', '')
    # print(jljx_gjw_data)
    jljx_gjw_data['org'] = {}

    jljx_gjw_data['org']['org_id'] = org_id
    try:
        if jljx_gjw_data['info']['mobilephone']:
            jljx_gjw_data['org']['download_status'] = 1
    except:
        jljx_gjw_data['org']['download_status'] = 0
    # 插件
    jljx_gjw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 收件箱--------------渠道职位ID
    if lx == 1:
        jljx_gjw_data['org']['resume_type'] = 1
        jljx_gjw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        if job_id:
            jljx_gjw_data['org']['job_id'] = job_id
    # 搜索/推荐----------遇仁职位ID
    elif lx == 2:
        jljx_gjw_data['org']['resume_type'] = 2
        jljx_gjw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
        if job_id:
            jljx_gjw_data['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    if dt:
        jljx_gjw_data['org']['delivery_time'] = dt
    return jljx_gjw_data


class Module_gj(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_gj, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    # 赶集登录判断
    def login_judge_gj(self):
        home_url = 'http://hrvip.ganji.com/home/all_point_ajax'
        response = self.session.get(url=home_url, headers=self.headers)
        res = json.loads(response.text)
        # print(res)
        return {'resume_num': float(res['resumeDownloadCount'])}

    # 赶集职位刷新------------
    def refresh_job_gj(self, JobID):
        joblist_url = 'http://hrvip.ganji.com/wanted_post/all_post?tab=normal'
        resp_text = self.session.get(url=joblist_url, headers=self.headers).text
        # print(resp_text)
        userid = re.search(r"/weizhaopin/(.*?)/", resp_text).group(1)
        sourcecode = re.search(r'sourcecode=(.*?)"', resp_text).group(1)
        if '&' in sourcecode:
            sourcecode = sourcecode.split('&')[0]
        revolutType_1 = 'normal'
        revolutType_2 = 'senior'
        refresh_url = 'http://refresh.ganji.com/pcajax/dorefresh?userid={userid}&infoid={JobID}&sourcecode={sourcecode}&revolutType={revolutType_1}'.format(userid=userid,revolutType_1=revolutType_1, JobID=JobID, sourcecode=sourcecode)
        # print(refresh_url)
        resp_text = self.session.get(url=refresh_url, headers=self.headers)
        # print(resp_text.text)
        resp_dic = json.loads(resp_text.text)
        # print(resp_dic)
        return resp_dic['code']

    # 赶集职位刷新点数获得------------------好像不对
    def refresh_point_gj(self):
        refresh_url = 'http://hrvip.ganji.com/wanted_post/all_post?tab=normal'
        resp_text = self.session.get(url=refresh_url, headers=self.headers).text
        sel = Selector(text=resp_text)
        rf_point_0 = sel.xpath('//em[@title="帮帮帖刷新次数"]/text()').extract()[0]
        rf_point_1 = sel.xpath('//em[@title="已购刷新点数"]/text()').extract()[0]
        return rf_point_0, rf_point_1

    # 赶集简历搜索下载
    def search_gj(self, userid):
        if '---' in userid:
            url_head = 'http://' + userid.split('---')[1]
            resume_id = userid.split('---')[0]
            search_url = 'http://www.ganji.com/jianli/{resume_id}x.htm'.format(resume_id=resume_id)
            download_response = self.session.get(url=search_url, headers=self.headers)
            # print(download_response.text)
            if '对不起，该简历已停止找工作了' not in download_response.text:
                hash_value = re.search(r"indow.PAGE_CONFIG.__hash__ = '(.*?)';", download_response.text).group(1)
                acusr = re.search(r"&acusr=(.*?)&", download_response.text).group(1)
                data = {
                    '__hash__': hash_value
                }
                download_url = '{url_head}/findjob/download_resume.php?downloadBy=POINT&version=1&action=download&findjob_puid={resume_id}&acusr={acusr}'.format(resume_id=resume_id, acusr=acusr, url_head=url_head)
                details_response = self.session.post(url=download_url, headers=self.headers, data=data)
                return download_response.text, details_response.text
            else:
                return None, None


    # 询问（新增）
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
                        html = etree.HTML(jl[0].text)
                        info_ele = html.xpath('//div[@class="resume-report clearfix"]/a[1]/span/@data-ref')[0]
                        chanl_id = json.loads(info_ele).get('postId')
                        td_date = jl[1].xpath('./dl[1]/dd[7]/text()')[0].strip()

                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid   # 企业id
                            content['jobId'] = jobid
                            content['channel'] = 4
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
                        content['channel'] = 4
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
                        html = etree.HTML(jl[0].text)
                        info_ele = html.xpath('//div[@class="resume-report clearfix"]/a[1]/span/@data-ref')[0]
                        chanl_id = json.loads(info_ele).get('postId')
                        td_date = jl[1].xpath('./dl[1]/dd[7]/text()')[0].strip()

                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid
                            content['jobId'] = jobid
                            content['channel'] = 4
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
                        content['channel'] = 4
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
                        html = etree.HTML(jl[0].text)
                        info_ele = html.xpath('//div[@class="resume-report clearfix"]/a[1]/span/@data-ref')[0]
                        chanl_id = json.loads(info_ele).get('postId')
                        td_date = jl[1].xpath('./dl[1]/dd[7]/text()')[0].strip()

                        if td_date == today1:
                            content = {}
                            content['orgId'] = orgid
                            content['jobId'] = jobid
                            content['channel'] = 4
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
                        content['channel'] = 4
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

    @staticmethod
    def search_resume_gj(data):
        searchValueHid = {
            'category': '-1',
            'major': '',
            'tag': '',
            'city_id': '26',
            'district_id': '-1',
            'street_id': '-1',
            'sex': '-1',
            'degree': '-1',
            'date': '-1',
            'age': '-1',
            'age_start': '',
            'age_end': '',
            'period': '-1',
            'period_more': 'on',
            'price': '-1',
            'parttime_price': '-1',
            'salary_less': 'on',
            'key': '',
            'related': '0',
        }
        return searchValueHid

    # 赶集查看简历
    def read_resume_gj(self, params, orgid, jobid, max_num):
        page = 1
        url = 'http://hrvip.ganji.com/resume_library/search_resume'

        params['page'] = str(page)
        response = self.session.get(url=url, headers=get_useragent(), params=params)

        data_wu_gj = []
        ss_num = 0

        def paging(response_page, page):
            nonlocal data_wu_gj, ss_num

            html = etree.HTML(response_page.text)
            lis = html.xpath('//div[@data-modify-class="frm-search"]/div')

            if not lis:
                return

            res_lis = []
            for cell in lis:
                details_url = cell.xpath('./dl[1]/dt[1]/a[1]/@href')[0]
                details_response = self.session.get(url=details_url, headers=get_useragent())
                res_lis.append((details_response, cell))

            ask_result = self.ask_before_read(res_lis, orgid, jobid)

            for key, value in enumerate(res_lis):
                try:
                    ask_status = ask_result[key]
                except:
                    logging.error('date is not new，stop scrapy...')
                    return

                if ask_status == '1':
                    try:
                        try:
                            final_data = jljx_gjw(text=value[0].text, ds=0, org_id=orgid, job_id=jobid, lx=2)
                        except:
                            final_data = jljx_gjw_jz(text=value[0].text, ds=0, org_id=orgid, job_id=jobid, lx=2)

                        data_wu_gj.append(final_data)
                        ss_num = ss_num + 1

                    except:
                        logging.error("this jl parse wrong...")
                        continue

                    if ss_num >= max_num:
                        return

                    if len(data_wu_gj) == 3:
                        data = json.dumps(data_wu_gj)
                        data = data.encode('utf-8')
                        requests.post(url=wu_jl_url, data=data)
                        data_wu_gj = []

                    time.sleep(random.uniform(3, 5))

            page += 1
            params['page'] = str(page)
            response_page = self.session.get(url=url, headers=get_useragent(), params=params)
            paging(response_page, page)

        paging(response, page)

        if len(data_wu_gj) > 0:
            data = json.dumps(data_wu_gj)
            data = data.encode('utf-8')
            requests.post(url=wu_jl_url, data=data)
            data_wu_gj = []

        return ss_num
