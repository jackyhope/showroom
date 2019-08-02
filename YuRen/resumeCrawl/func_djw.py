# -*- coding: utf-8 -*-：

import traceback
import json
from scrapy.selector import Selector
import re
import time
import requests,datetime
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

def handle_salary(text):
    if 'RMB/月' in text:
        text = text.replace('RMB/月', '')
    # pattern = re.compile(r'([0-9]{0,10}[万]?[元]?[-]?)?([0-9]{0,10}[万]?[元]?)?')--------------可以用，下面的为改进版
    pattern = re.compile(r'([0-9]{0,10}[.]?[0-9]{0,6}?.*?[-至到/]?[0-9]{0,10}[.]?[0-9]{0,6}?)')
    date_result = pattern.findall(text)
    salary_str = ''.join(date_result)
    salary_dic = {}
    pattern_sub = re.compile(r'([至到/])')
    salary_str = pattern_sub.sub('-', salary_str)
    # print(salary_str)
    mult_li = []
    if '-' in salary_str:
        salary_str_0 = salary_str.split('-')[0]
        salary_str_1 = salary_str.split('-')[1]
        if '.' in salary_str_0:
            salary_str_0_len = len(salary_str_0.split('.')[1])
            salary_str_0_mult = int('1' + '0'*int(salary_str_0_len))
        else:
            salary_str_0_mult = 1
        if '.' in salary_str_1:
            salary_str_1_len = len(salary_str_1.split('.')[1])
            salary_str_1_mult = int('1' + '0'*int(salary_str_1_len))
        else:
            salary_str_1_mult = 1
        mult_li.append(salary_str_1_mult)
        mult_li.append(salary_str_0_mult)
        mult_value = max(mult_li)
        mult_len = len(str(mult_value))-1
        # print(mult_value)
        if float(salary_str_0) < 1000:
            salary_str_0 = float(salary_str_0)*10000
        else:
            salary_str_0 = float(salary_str_0)
        if float(salary_str_1) < 1000:
            salary_str_1 = float(salary_str_1)*10000
        else:
            salary_str_1 = float(salary_str_1)
        salary_dic['lower'] = int(str(salary_str_0).split('.')[0])
        salary_dic['upper'] = int(str(salary_str_1).split('.')[0])
    else:
        salary_str_0 = salary_str.split('-')[0]
        if '.' in salary_str_0:
            salary_str_0_len = len(salary_str_0.split('.')[1])
            mult_value = int('1' + '0'*int(salary_str_0_len))
            mult_len = len(str(mult_value)) - 1
        else:
            mult_value = 1
            mult_len = 0
        if float(salary_str_0) < 1000:
            salary_str_0 = float(salary_str_0)*10000
        else:
            salary_str_0 = float(salary_str_0)
        salary_dic['lower'] = int(str(salary_str_0).split('.')[0])
        salary_dic['upper'] = int(str(salary_str_0).split('.')[0])
    return salary_dic
def riqizhaunhuan(xx):
    xx_li = xx.split('-')
    for index,value in enumerate(xx_li):
        if int(value) <= 9 and len(str(value)) == 1:
            xx_li_temp = '0' + str(value)
            xx_li[index] = xx_li_temp
    return '-'.join(xx_li)
def handle_time(text):
    # 下面那个感觉更好但是却匹配到不想要的结果
    if '毕业' in text:
        text = text.split('毕业')[0]
    if '至今' in text:
        text = text.split('至今')[0]
    if '至' in text:
        text = text.replace('至', '#')
    # print(text)
    pattern = re.compile(r'([0-9零一二三四五六七八九十]{2,4}[年./\-]+?)?([0-9零一二三四五六七八九十]{1,2}[月./\-]*?)?([0-9零一二三四五六七八九十]+[日号\-]*?)?')
    # pattern = re.compile(r'([0-9零一二三四五六七八九十]{2,4}[年./-至])?([0-9零一二三四五六七八九十]{1,2}[月./-至])?([0-9零一二三四五六七八九十]{1,2}[日号至]?)?')
    date_result = pattern.findall(text)
    now_year = datetime.datetime.now().year
    time_data = []
    # print(date_result)
    for date_tuple in date_result:
        tj_1 = date_tuple[0] and date_tuple[1]
        tj_2 = date_tuple[2] and date_tuple[1]
        tj_3 = date_tuple[2] and date_tuple[1] and date_tuple[0]
        pattern_sub = re.compile(r'([月年./\-至])')
        pattern_sub_1 = re.compile(r'([日号\-至])')
        if tj_3:
            time_str = '-'.join(list(date_tuple))
            time_str = pattern_sub.sub('-', time_str)
            print(time_str)
            time_str = pattern_sub_1.sub('', time_str)
            print(time_str)
            time_str = time_str.replace('--', '-')
            time_str = riqizhaunhuan(time_str)
            time_data.append(time_str)
        elif tj_2:
            time_str = '-'.join(list(date_tuple[1:]))
            time_str = str(now_year) + '-' + pattern_sub.sub(time_str, '-')
            time_str = pattern_sub.sub('-', time_str)
            time_str = pattern_sub_1.sub('', time_str)
            time_str = time_str.replace('--', '-')
            time_str = riqizhaunhuan(time_str)
            time_data.append(time_str)
        elif tj_1:
            time_str = '-'.join(list(date_tuple[:-1]))
            time_str = pattern_sub.sub('-', time_str) + '-01'
            time_str = time_str.replace('--', '-')
            time_str = riqizhaunhuan(time_str)
            time_data.append(time_str)
    if len(time_data) == 1:
        time_data.append('9999-01-01')
    return time_data
def get_date(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)

#职位刷新次数
def zw_shua_xi(cookie):
    num = 0
    return num
#职位刷新
def zw_sx(cookie,job_id):
    pass

#判断ID是否存在
def jl_idcx(cookie,jl_id):
    headers = {
        'User-Agent': get_useragent(),
        'Cookie': cookie,
    }
    url_zy = 'https://job.dajie.com/search/talent/ajax/getresumes?resumeIds={}'.format(jl_id)
    response_html = requests.post(url=url_zy, headers=headers).text
    dict_response=json.loads(response_html)
    totalPage=dict_response['data']['totalPage']
    if totalPage == 0:
        jl_id_num=0
        return jl_id_num
    elif  totalPage == 1:
        jl_id_num=1
        return jl_id_num

#特权点数，下载、刷新劵数
def jl_ds(cookie):
    headers = {
            'User-Agent': get_useragent(),
            'Cookie': cookie,
        }
    url_ds = "https://job.dajie.com/recruit/index"
    response_html = requests.get(url=url_ds, headers=headers).text
    # print(response_html)
    sel=Selector(text=response_html)
    tqds= sel.xpath('string(//div[@class="integralBoxRightC"]/p[1]/span[@class="num"])').extract()[0].strip()
    tq_ds=tqds.replace('点',"")
    print(type(tq_ds))

    url_juan="https://job.dajie.com/recruit/point/ticket?from=index"
    juan_html = requests.get(url=url_juan, headers=headers).text
    # print(juan_html)
    sel_1 = Selector(text=juan_html)
    xzjuan = sel_1.xpath('string(//div[@class="unusedBox"]/div/ul/li[@data-desc="简历下载1份券"]//span[@class="num"])').extract()[0].strip()
    xz_juan=xzjuan.replace('张',"")
    # print(xz_juan)
    sxjuan= sel_1.xpath('string(//div[@class="unusedBox"]/div/ul/li[@data-desc="职位刷新1次券"]//span[@class="num"])').extract()[0].strip()
    sx_juan = sxjuan.replace('张', "")
    # print(sx_juan)
    if sx_juan == '':
        sx_juan = '0'
    if xz_juan == '':
        xz_juan = '0'
    return tq_ds,xz_juan,sx_juan

def login_judge_djw(cookie):
    headers={
    'User-Agent':get_useragent(),
    'Cookie':cookie,
    }
    url_zy="https://job.dajie.com/recruit/index"
    response_html = requests.get(url=url_zy, headers=headers).text
    sel=Selector(text=response_html)
    xz_sl=sel.xpath('string(//div[@class="integralBoxRightC"]/p/a/span[@class="numZ"])').extract()[0]
    # print('6666666', xz_sl, '999999999999999999999')
    if xz_sl:
        return xz_sl
    else:
        raise Exception('djw not login')
def jl_xiazai(cookie,jl_id,pay_way):
    headers = {
        'User-Agent': get_useragent(),
        'Cookie': cookie,
    }
    url_zy = 'https://job.dajie.com/search/talent/ajax/getresumes?resumeIds={}'.format(jl_id)
    response_html = requests.post(url=url_zy, headers=headers).text
    dict_response = json.loads(response_html)
    encryptedId=dict_response['data']['list'][0]['encryptedId']

    pageType="search"
    pay_way= pay_way
    url_xz="https://job.dajie.com/recruit/apply/ajax/paycontact?pageType=" +pageType
    data = {
        'ajax':'1',
        'encryptedId': encryptedId,
        'payWay': pay_way
    }
    header_xz={
        'Host': 'job.dajie.com',
        'Connection': 'keep-alive',
        'Content-Length': '60',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://job.dajie.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Referer':url_ref ,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': get_useragent(),
        'Cookie': cookie,
    }
    response_xz = requests.post(url=url_xz, data=data, headers=header_xz).text

    if json.loads(response_xz)['message'] == "sorry, 精英或智能推荐邀约人才不能使用特权券!":
        return "sorry, 精英或智能推荐邀约人才不能使用特权券!"
    elif json.loads(response_xz)['message'] == "sorry，您的人才券不足":
        return "sorry，您的人才券不足！"
    elif json.loads(response_xz)['message'] == "sorry，您的点数不足！":
        return "sorry，您的点数不足！"
    else:
        time.sleep(1.5)
        html_1 = requests.post(url=url_zy, headers=headers).text
        dict_1 = json.loads(html_1)
        email = dict_1['data']['list'][0]['email']
        mobile = dict_1['data']['list'][0]['mobile']
        name=dict_1['data']['list'][0]['name']
        djw_jl={}
        djw_jl['email']=email
        djw_jl['mobile']=mobile
        djw_jl['name'] = name
        return djw_jl

def jljx_djw(text, jl_id='',ds=0, org_id='', job_id='',lx=0, dt=0):
    jl_djw_data = {}
    sel = Selector(text=text)
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_today = datetime.datetime.now().strftime('%Y-%m-%d')
    jl_djw_data['info'] = {}
    jl_djw_data['objective'] = {}
    jl_djw_data['jobs'] = []
    jl_djw_data['educations'] = []
    jl_djw_data['at_schools'] = []
    jl_djw_data['credentials'] = []
    jl_djw_data['languages'] = []
    jl_djw_data['trainings'] = []
    jl_djw_data['projects'] = []
    jl_djw_data['projects'] = []
    jl_djw_data['info']['channel'] = 7
    jl_djw_data['org'] = {}
    jl_djw_data['org']['resume_type'] = 3
    try:
        job_title_str = sel.xpath('string(//div[@class="r_l_top"])').extract()[0]
        jl_djw_data['org']['job_title'] = job_title_str.split('应聘：')[1].split('投递时间')[0].split('简历更新时间')[0].strip()
        jl_djw_data['info']['channel_update_time'] = job_title_str.split('简历更新时间：')[1].split('应聘：')[0].split('投递时间')[0].strip()
    except:
        # traceback.print_exc()
        pass
    jl_djw_data['info']['channel_resume_id'] = sel.xpath('//span[@class="idT"]/text()').extract()[0].split('ID: ')[1].strip()
    xpa_bk_li = '//div[@class="profile-in"]/div[@class="main-wrap"]/dl[@class="pre-item"]'
    xpa_bk_name = 'string(//div[@class="basic-information"]/div[@class="informationLeft"]/h5)'
    xpa_bk_jbxx = '//div[@class="basic-information"]/div[@class="informationLeft"]/ul/li'
    xpa_bk_qzyx = '//div[@class="profile-in"]/div[@class="main-wrap"]/dl[@class="pre-item jobWanted"]/descendant::tr[@class="padding-no"]'
    djw_name_str = sel.xpath(xpa_bk_name).extract()[0]
    jl_djw_data['info']['name'] = djw_name_str.split('（')[0].strip()
    if '，' in djw_name_str.split('（')[1]:
        jl_djw_data['info']['sex'] = djw_name_str.split('（')[1].split('，')[0].strip()
    #     djw_age = djw_name_str.split('（')[1].split('，')[1].split('）')[0].strip()
    #     jl_djw_data['info']['birth_year'] = int(now_year) - int(djw_age)
    else:
        if '男' in djw_name_str.split('（')[1]:
            jl_djw_data['info']['sex'] = '男'
        elif '女' in djw_name_str.split('（')[1]:
            jl_djw_data['info']['sex'] = '女'
    for djw_jbxx in sel.xpath(xpa_bk_jbxx):
        djw_jbxx_str = djw_jbxx.xpath('string(.)').extract()[0].replace("\r", "").replace("\n","").replace("\t","").replace(" ","").replace("　","")
        # print(djw_jbxx_str)
        if '工作经验：' in djw_jbxx_str:
            try:
                jl_djw_data['info']['start_working_year'] = int(now_year) - int(djw_jbxx_str.split('工作经验：')[1].split('年')[0].strip())
            except:
                pass
        elif '学  历：' in djw_jbxx_str:
            jl_djw_data['info']['degree'] = djw_jbxx_str.split('学  历：')[1].strip()
        elif '出生日期：' in djw_jbxx_str:
            birth_str = int(djw_jbxx_str.split('出生日期：')[1].strip().split('-')[0])
            if birth_str:
                jl_djw_data['info']['birth_year'] = int(birth_str)
        elif '所在城市：' in djw_jbxx_str:
            jl_djw_data['info']['current_address'] = djw_jbxx_str.split('所在城市：')[1].strip()
        elif '政治面貌：' in djw_jbxx_str:
            jl_djw_data['info']['politics_status'] = djw_jbxx_str.split('政治面貌：')[1].strip()
        elif '户  口：' in djw_jbxx_str:
            jl_djw_data['info']['residence_address'] = djw_jbxx_str.split('户  口：')[1].strip()
        elif '手  机：' in djw_jbxx_str:
            tel_str = djw_jbxx_str.split('手  机：')[1].strip()
            if '*' not in tel_str:
                jl_djw_data['info']['mobilephone'] = tel_str
        elif '邮  箱：' in djw_jbxx_str:
            email_str = djw_jbxx_str.split('邮  箱：')[1].strip()
            if '*' not in email_str:
                jl_djw_data['info']['email'] = email_str
    for djw_qzyx in sel.xpath(xpa_bk_qzyx):
        djw_qzyx_th = djw_qzyx.xpath('string(th)').extract()[0].strip()
        djw_qzyx_td = djw_qzyx.xpath('string(td)').extract()[0].replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("　", "").strip()
        if '目前状态' in djw_qzyx_th:
            jl_djw_data['info']['work_status'] = djw_qzyx_td
        elif '求职类型' in djw_qzyx_th:
            jl_djw_data['objective']['job_nature'] = djw_qzyx_td.split('、')
        elif '期望职业' in djw_qzyx_th:
            jl_djw_data['objective']['expected_job_title'] = djw_qzyx_td.split('、')
        elif '期望行业' in djw_qzyx_th:
            jl_djw_data['objective']['trade'] = djw_qzyx_td.split('、')
        elif '期望城市' in djw_qzyx_th:
            jl_djw_data['objective']['expected_address'] = djw_qzyx_td.split('、')
        elif '期望月薪' in djw_qzyx_th:
            try:
                if '不限' not in djw_qzyx_td:
                    djw_salary_dic = handle_salary(djw_qzyx_td)
                    jl_djw_data['objective']['expected_salary_lower'] = djw_salary_dic['lower']
                    jl_djw_data['objective']['expected_salary_upper'] = djw_salary_dic['upper']
                else:
                    jl_djw_data['objective']['expected_salary_lower'] = 0
                    jl_djw_data['objective']['expected_salary_upper'] = 0
            except:
                pass
    for djw_bk_1 in sel.xpath(xpa_bk_li):
        djw_bk_1_th = djw_bk_1.xpath('string(dt)').extract()[0].strip()
        if '自我介绍' in djw_bk_1_th:
            djw_bk_1_dd = djw_bk_1.xpath('string(dd)').extract()[0].replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("　", "").strip()
            jl_djw_data['objective']['self_evaluation'] = djw_bk_1_dd
        elif '工作经历' in djw_bk_1_th:
            xpa_djw_job_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_job_tr):
                xpa_djw_job_tr = 'dd/table/tbody/tr'
            for djw_job_1 in djw_bk_1.xpath(xpa_djw_job_tr):
                djw_job_dic = {}
                try:
                    th_source_code = djw_job_1.xpath('th').extract()[0].replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("　", "").strip()
                    # print(th_source_code)
                    re_djw_job_time = r"(?<=<th>).+?(?=<br>)"
                    pattern_djw_job_time = re.compile(re_djw_job_time)
                    th_str = pattern_djw_job_time.findall(th_source_code)
                    # print(th_str[0])
                    djw_job_time_li = handle_time(th_str[0])
                    djw_job_dic['during_start'] = djw_job_time_li[0]
                    djw_job_dic['during_end'] = djw_job_time_li[1]
                    djw_job_title_str = djw_job_1.xpath('td/p[@class="item-tit highlight-filter"]/text()').extract()[0].strip()
                    # print(djw_job_title_str)
                    djw_job_dic['job_title'] = djw_job_title_str
                    djw_job_comp_str = djw_job_1.xpath('td/p[@class="item-tit highlight-filter"]/span/text()').extract()[0].strip()
                    # print(djw_job_comp_str)
                    re_djw_job_comp_trade = r"(?<=（)([^（]+)?(?=）)"
                    pattern_djw_job_time = re.compile(re_djw_job_comp_trade)
                    thrade_str = pattern_djw_job_time.findall(djw_job_comp_str)
                    if len(thrade_str) == 0:
                        djw_job_dic['company'] = djw_job_comp_str
                    elif len(thrade_str) >= 1:
                        trade_str_all = '（' + thrade_str[-1] + '）'
                        djw_job_dic['company'] = djw_job_comp_str.replace(trade_str_all, '').strip()
                        djw_job_dic['trade'] = thrade_str[-1].strip()
                    try:
                        djw_job_detail_str = djw_job_1.xpath('string(td/p[@class="highlight-filter"])').extract()[0].replace("\r", "").replace("\n", "").replace("\t","").replace(" ", "").replace("　", "").strip()
                        # print(djw_job_detail_str)
                        try:
                            djw_job_dic['company_nature'] = djw_job_detail_str.split('公司性质：')[1].split('公司规模：')[0].split('所在部门：')[0].split('汇报对象：')[0].split('薪水：')[0].strip()
                        except:
                            pass
                        try:
                            djw_job_dic['company_scale'] = djw_job_detail_str.split('公司规模：')[1].split('公司性质：')[0].split('所在部门：')[0].split('汇报对象：')[0].split('薪水：')[0].strip()
                        except:
                            pass
                        try:
                            djw_job_dic['department'] = djw_job_detail_str.split('所在部门：')[1].split('公司规模：')[0].split('公司性质：')[0].split('汇报对象：')[0].split('薪水：')[0].strip()
                        except:
                            pass
                        try:
                            djw_job_dic['boss'] = djw_job_detail_str.split('汇报对象：')[1].split('公司规模：')[0].split('所在部门：')[0].split('公司性质：')[0].split('薪水：')[0].strip()
                        except:
                            pass
                        try:
                            djw_job_salary_str = djw_job_detail_str.split('薪水：')[1].split('公司规模：')[0].split('所在部门：')[0].split('汇报对象：')[0].split('公司性质：')[0].strip()
                            djw_job_salary_dic = handle_salary(djw_job_salary_str)
                            djw_job_dic['monthly_salary_lower'] = djw_job_salary_dic['lower']
                            djw_job_dic['monthly_salary_upper'] = djw_job_salary_dic['upper']
                        except:
                            pass
                    except:
                        traceback.print_exc()
                        pass
                    try:
                        djw_job_detail_str_2 = djw_job_1.xpath('string(td/p[@class="highlight-filter "])').extract()[
                            0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("　",
                                                                       "").strip()
                        if djw_job_detail_str_2:
                            djw_job_dic['job_content'] = djw_job_detail_str_2
                    except:
                        pass
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['jobs'].append(djw_job_dic)
                # print(th_str)
        elif '项目经验' in djw_bk_1_th:
            xpa_djw_pro_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_pro_tr):
                xpa_djw_pro_tr = 'dd/table/tbody/tr'
            for djw_pro_1 in djw_bk_1.xpath(xpa_djw_pro_tr):
                djw_pro_dic = {}
                try:
                    th_source_code = djw_pro_1.xpath('th').extract()[0].replace("\r", "").replace("\n", "").replace(
                        "\t", "").replace(" ", "").replace("　", "").strip()
                    # print(th_source_code)
                    re_djw_pro_time = r"(?<=<th>).+?(?=</th>)"
                    pattern_djw_pro_time = re.compile(re_djw_pro_time)
                    th_str = pattern_djw_pro_time.findall(th_source_code)
                    # print(th_str[0])
                    djw_pro_time_li = handle_time(th_str[0])
                    djw_pro_dic['during_start'] = djw_pro_time_li[0]
                    djw_pro_dic['during_end'] = djw_pro_time_li[1]
                    djw_pro_title_str = djw_pro_1.xpath('td/p[@class="item-tit highlight-filter"]/text()').extract()[
                        0].strip()
                    # print(djw_pro_title_str)
                    djw_pro_dic['title'] = djw_pro_title_str
                    djw_pro_comp_str = djw_pro_1.xpath('td/p[@class="item-tit highlight-filter"]/span/text()').extract()[0].strip()
                    djw_pro_dic['company'] = djw_pro_comp_str
                    try:
                        djw_pro_detail_str_2 = djw_pro_1.xpath('string(td/p[@class="indent-wrap highlight-filter"][1])').extract()[
                            0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("　",
                                                                                                              "").strip()
                        # print(888, djw_pro_detail_str_2)
                        djw_pro_dic['description'] = djw_pro_detail_str_2.split('简介：')[1]
                    except:
                        pass
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['projects'].append(djw_pro_dic)
        elif '教育经历' in djw_bk_1_th:
            xpa_djw_edu_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_edu_tr):
                xpa_djw_edu_tr = 'dd/table/tbody/tr'
            for djw_edu_1 in djw_bk_1.xpath(xpa_djw_edu_tr):
                djw_edu_dic = {}
                try:
                    th_source_code = djw_edu_1.xpath('th').extract()[0].replace("\r", "").replace("\n", "").replace(
                        "\t", "").replace(" ", "").replace("　", "").strip()
                    # print(th_source_code)
                    re_djw_edu_time = r"(?<=<th>).+?(?=</th>)"
                    pattern_djw_edu_time = re.compile(re_djw_edu_time)
                    th_str = pattern_djw_edu_time.findall(th_source_code)
                    # print(th_str[0])
                    djw_edu_time_li = handle_time(th_str[0])
                    djw_edu_dic['during_start'] = djw_edu_time_li[0]
                    djw_edu_dic['during_end'] = djw_edu_time_li[1]
                    djw_edu_title_str = djw_edu_1.xpath('td/p[@class="item-tit highlight-filter"]/text()').extract()[
                        0].strip()
                    # print(djw_edu_title_str)
                    djw_edu_title_li = djw_edu_title_str.split(' ')
                    try:
                        djw_edu_dic['degree'] = djw_edu_title_li[0].strip()
                    except:
                        pass
                    try:
                        djw_edu_dic['major'] = djw_edu_title_li[1].strip()
                    except:
                        pass
                    djw_edu_comp_str = \
                    djw_edu_1.xpath('td/p[@class="item-tit highlight-filter"]/span/text()').extract()[0].strip()
                    djw_edu_dic['school'] = djw_edu_comp_str
                    try:
                        djw_edu_detail_str_2 = \
                        djw_edu_1.xpath('string(td/p[@class="item-des highlight-filter])').extract()[
                            0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("　",
                                                                                                              "").strip()
                        # print(888, djw_edu_detail_str_2)
                        djw_edu_dic['major_description'] = djw_edu_detail_str_2.split('简介：')[1]
                    except:
                        pass
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['educations'].append(djw_edu_dic)
        elif 'IT技能' in djw_bk_1_th:
            xpa_djw_ski_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_ski_tr):
                xpa_djw_ski_tr = 'dd/table/tbody/tr'
            for djw_ski_1 in djw_bk_1.xpath(xpa_djw_ski_tr):
                try:
                    djw_ski_title_str = djw_ski_1.xpath('td/p[@class="item-tit"]/text()').extract()[0].strip()
                    # print(djw_ski_title_str)
                    if '良好' in djw_ski_title_str:
                        djw_ski_level = '良好'
                    elif '精通' in djw_ski_title_str:
                        djw_ski_level = '精通'
                    elif '熟悉' in djw_ski_title_str:
                        djw_ski_level = '熟悉'
                    else:
                        continue

                    for djw_skill_1 in djw_ski_1.xpath('td/p[@class="list highlight-filter"]/span'):
                        djw_ski_dic = {}
                        djw_ski_name = djw_skill_1.xpath('string(.)').extract()[0].strip()
                        djw_ski_dic[djw_ski_name] = djw_ski_level
                        jl_djw_data['languages'].append(djw_ski_dic)
                except:
                    traceback.print_exc()
                    pass
        elif '语言能力' in djw_bk_1_th:
            xpa_djw_lang_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_lang_tr):
                xpa_djw_lang_tr = 'dd/table/tbody/tr'
            for djw_lang_1 in djw_bk_1.xpath(xpa_djw_lang_tr):
                djw_lang_dic = {}
                try:
                    djw_lang_title_str = djw_lang_1.xpath('td/p[@class="item-tit"]/text()').extract()[0].strip()
                    # print(djw_lang_title_str)
                    djw_lang_dic['language'] = djw_lang_title_str
                    for djw_skill_1 in djw_lang_1.xpath('td/p/span[@class="item-list highlight-filter"]'):
                        djw_lang_level = djw_skill_1.xpath('string(.)').extract()[0].strip()
                        if '读写：' in djw_lang_level:
                            djw_lang_dic['writing'] = djw_lang_level.split('读写：')[1].strip()
                        elif '听说：' in djw_lang_level:
                            djw_lang_dic['speaking'] = djw_lang_level.split('听说：')[1].strip()
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['languages'].append(djw_lang_dic)
        elif '培训经历' in djw_bk_1_th:
            xpa_djw_train_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_train_tr):
                xpa_djw_train_tr = 'dd/table/tbody/tr'
            for djw_train_1 in djw_bk_1.xpath(xpa_djw_train_tr):
                djw_train_dic = {}
                try:
                    th_source_code = djw_train_1.xpath('th').extract()[0].replace("\r", "").replace("\n", "").replace(
                        "\t", "").replace(" ", "").replace("　", "").strip()
                    # print(th_source_code)
                    re_djw_train_time = r"(?<=<th>).+?(?=</th>)"
                    pattern_djw_train_time = re.compile(re_djw_train_time)
                    th_str = pattern_djw_train_time.findall(th_source_code)
                    # print(th_str[0])
                    djw_train_time_li = handle_time(th_str[0])
                    djw_train_dic['during_start'] = djw_train_time_li[0]
                    djw_train_dic['during_end'] = djw_train_time_li[1]
                    djw_train_title_str = \
                    djw_train_1.xpath('td/p[@class="item-tit highlight-filter"]/text()').extract()[
                        0].strip()
                    # print(djw_train_title_str)
                    try:
                        djw_train_dic['training_course'] = djw_train_title_str
                    except:
                        pass

                    djw_train_comp_str = \
                        djw_train_1.xpath('td/p[@class="item-tit highlight-filter"]/span/text()').extract()[0].strip()
                    djw_train_dic['training_agency'] = djw_train_comp_str
                    try:
                        djw_train_detail_str_2 = \
                            djw_train_1.xpath('string(td/p[@class="highlight-filter"])').extract()[
                                0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("　",
                                                                                                                  "").strip()
                        # print(888, djw_train_detail_str_2)
                        djw_train_dic['description'] = djw_train_detail_str_2
                    except:
                        pass
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['trainings'].append(djw_train_dic)
        elif '证书' in djw_bk_1_th:
            xpa_djw_zs_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_zs_tr):
                xpa_djw_zs_tr = 'dd/table/tbody/tr'
            for djw_zs_1 in djw_bk_1.xpath(xpa_djw_zs_tr):
                try:
                    for djw_zs_1 in djw_zs_1.xpath('td/p[@class="list highlight-filter"]/span'):
                        djw_zs_dic = {}
                        djw_zs_level = djw_zs_1.xpath('string(.)').extract()[0].strip()
                        djw_zs_dic['title'] = djw_zs_level
                        jl_djw_data['credentials'].append(djw_zs_dic)
                except:
                    # traceback.print_exc()
                    pass
        elif '校内职务' in djw_bk_1_th:
            xpa_djw_campus_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_campus_tr):
                xpa_djw_campus_tr = 'dd/table/tbody/tr'
            for djw_campus_1 in djw_bk_1.xpath(xpa_djw_campus_tr):
                djw_campus_dic = {}
                try:
                    th_source_code = djw_campus_1.xpath('th').extract()[0].replace("\r", "").replace("\n", "").replace(
                        "\t", "").replace(" ", "").replace("　", "").strip()
                    # print(th_source_code)
                    re_djw_campus_time = r"(?<=<th>).+?(?=</th>)"
                    pattern_djw_campus_time = re.compile(re_djw_campus_time)
                    th_str = pattern_djw_campus_time.findall(th_source_code)
                    # print(th_str[0])
                    djw_campus_time_li = handle_time(th_str[0])
                    djw_campus_dic['during_start'] = djw_campus_time_li[0]
                    djw_campus_dic['during_end'] = djw_campus_time_li[1]
                    djw_campus_title_str = \
                    djw_campus_1.xpath('td/p[@class="item-tit highlight-filter"]/text()').extract()[
                        0].strip()
                    # print(djw_campus_title_str)
                    djw_campus_dic['campus_post'] = djw_campus_title_str
                    try:
                        djw_campus_detail_str_2 = \
                        djw_campus_1.xpath('string(td/p[@class="highlight-filter"])').extract()[
                            0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("　",
                                                                                                              "").strip()
                        # print(888, djw_campus_detail_str_2)
                        djw_campus_dic['description'] = djw_campus_detail_str_2
                    except:
                        pass
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['at_schools'].append(djw_campus_dic)
        elif '校内奖励' in djw_bk_1_th:
            xpa_djw_campus_tr = 'dd/table/tr'
            if not djw_bk_1.xpath(xpa_djw_campus_tr):
                xpa_djw_campus_tr = 'dd/table/tbody/tr'
            for djw_campus_1 in djw_bk_1.xpath(xpa_djw_campus_tr):
                djw_campus_dic = {}
                try:
                    th_source_code = djw_campus_1.xpath('th').extract()[0].replace("\r", "").replace("\n", "").replace(
                        "\t", "").replace(" ", "").replace("　", "").strip()
                    # print(th_source_code)
                    re_djw_campus_time = r"(?<=<th>).+?(?=</th>)"
                    pattern_djw_campus_time = re.compile(re_djw_campus_time)
                    th_str = pattern_djw_campus_time.findall(th_source_code)
                    # print(th_str[0])
                    djw_campus_time_li = handle_time(th_str[0])
                    djw_campus_dic['get_time'] = djw_campus_time_li[0]
                    djw_campus_title_str = \
                    djw_campus_1.xpath('td/p[@class="item-tit highlight-filter"]/text()').extract()[
                        0].strip()
                    # print(djw_campus_title_str)
                    djw_campus_dic['prize'] = djw_campus_title_str
                    try:
                        djw_campus_detail_str_2 = \
                        djw_campus_1.xpath('string(td/p[@class="highlight-filter"])').extract()[
                            0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "").replace("　",
                                                                                                              "").strip()
                        # print(888, djw_campus_detail_str_2)
                        djw_campus_dic['description'] = djw_campus_detail_str_2
                    except:
                        pass
                except:
                    traceback.print_exc()
                    pass
                jl_djw_data['at_schools'].append(djw_campus_dic)
    # org
    jl_djw_data['org']['org_id'] = org_id
    try:
        if jl_djw_data['info']['mobilephone']:
            jl_djw_data['org']['download_status'] = 1
    except:
        jl_djw_data['org']['download_status'] = 0
    # 插件
    jl_djw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 搜索/推荐----------遇仁职位ID
    if job_id:
        jl_djw_data['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    if dt:
        jl_djw_data['org']['delivery_time'] = dt
    return jl_djw_data




# def jl_djw(text, ds=0, org_id='', job_id='', lx=0, dt=0):
#     # text = text.replace('#→start→#', '').replace('#←end←#', '')
#     jl_djw_data = {}
#     sel = Selector(text=text)
#     now_year = datetime.datetime.now().year
#     now_month = datetime.datetime.now().month
#     now_today = datetime.datetime.now().strftime('%Y-%m-%d')
#     jl_djw_data['info'] = {}
#     jl_djw_data['objective'] = {}
#     jl_djw_data['jobs'] = []
#     jl_djw_data['educations'] = []
#     jl_djw_data['at_schools'] = []
#     jl_djw_data['credentials'] = []
#     jl_djw_data['languages'] = []
#     jl_djw_data['trainings'] = []
#     jl_djw_data['projects'] = []
#     jl_djw_data['info']['channel'] = 7
#     # 更新时间
#     try:
#         channel_update_time = sel.xpath('string(//div[@class="lightspot-box"]/p)').extract()[0]
#         if '今天' in channel_update_time or '刚' in channel_update_time:
#             jl_djw_data['info']['channel_update_time'] = now_today
#         elif '昨天' in channel_update_time:
#             yestoday_li = str(get_date(1))[:10]
#             jl_djw_data['info']['channel_update_time'] = yestoday_li
#         else:
#             jl_djw_data['info']['channel_update_time'] = channel_update_time.split("简历更新时间：")[1].strip()
#     except:
#         pass
#     # 简历ID
#     try:
#         channel_resume_id = sel.xpath('string(//input[@id="encryptedId"]/@value)').extract()[0].strip()
#         jl_djw_data['info']['channel_resume_id'] = channel_resume_id
#     except:
#         pass
#     # 照片地址
#     if sel.xpath('//div[@class="pre-photo"]/img/@src'):
#         try:
#             pho_url = sel.xpath('string(//div[@class="pre-photo"]/img/@src)').extract()[0]
#             if 'http' not in pho_url:
#                 pho_url = 'http:' + pho_url
#             jl_djw_data['info']['photo_url'] = pho_url
#         except:
#             pass
#     # 姓名、性别、出生年份
#     try:
#         info= sel.xpath('string(//div[@class="informationLeft"]/h5)').extract()[0].strip()
#         jl_djw_data['info']['name'] = info.split("（")[0].strip()
#         try:
#             jl_djw_data['info']['sex'] = info.split("（")[1].split("，")[0].strip()
#         except:
#             pass
#         try:
#             jl_djw_data['info']['birth_year'] = int(now_year) - int(info.split('，')[1].split("）")[0].strip())
#         except:
#             pass
#     except:
#         pass
#     # 、学历、参加工作年份、政治面貌、户籍、现居住地
#     if sel.xpath('//div[@class="informationLeft"]/ul'):
#         age_or_hk = sel.xpath('//div[@class="informationLeft"]/ul/li')
#         for a_or_h in age_or_hk:
#             a_h_v = a_or_h.xpath('text()').extract()[0].strip()
#             if '学  历' in a_h_v:
#                 try:
#                     jl_djw_data['info']['degree'] = a_h_v.split('学  历：')[1].strip()
#                 except:
#                     pass
#             elif '工作经验' in a_h_v:
#                 try:
#                     if "暂无" in a_h_v:
#                         jl_djw_data['info']['start_working_year'] = int(now_year)
#                     elif "以下" in a_h_v:
#                         jl_djw_data['info']['start_working_year'] = int(now_year) - 1
#                     else:
#                         jl_djw_data['info']['start_working_year'] = int(now_year) - int(
#                             a_h_v.split('工作经验：')[1].split('年')[0].strip())
#                 except:
#                     pass
#             elif "手  机" in a_h_v  and  "*" not in a_h_v:
#                 try:
#                     jl_djw_data['info']['mobilephone'] = a_h_v.split('手  机：')[1].strip()
#                 except:
#                     pass
#             elif "邮  箱" in a_h_v and "*" not in a_h_v:
#                 try:
#                     jl_djw_data['info']['email'] = a_h_v.split('邮  箱：')[1].strip()
#                 except:
#                     pass
#             elif "政治面貌" in a_h_v :
#                 try:
#                     jl_djw_data['info']['politics_status'] = a_h_v.split('政治面貌：')[1].strip()
#                 except:
#                     pass
#             elif "户  口" in a_h_v:
#                 try:
#                     jl_djw_data['info']['residence_address'] = a_h_v.split('户  口：')[1].strip()
#                 except:
#                     pass
#             elif "所在城市：" in a_h_v:
#                 try:
#                     jl_djw_data['info']['current_address'] = a_h_v.split('所在城市：')[1].strip()
#                 except:
#                     pass
#
#
# # 各模块内容
#     if sel.xpath('//dl[@class="pre-item jobWanted"]'):
#             section= sel.xpath('//dl[@class="pre-item jobWanted"]')
#             section_name = sel.xpath('string(//dl[@class="pre-item jobWanted"]/dt/span)').extract()[0].strip()
#             if "求职意愿" in section_name:
#                 for row in sel.xpath('//dl[@class="pre-item jobWanted"]/dd/table/tr'):
#                     row_name = row.xpath('string(th)').extract()[0]
#                     if "期望职业" in row_name:
#                         jl_djw_data['objective']['expected_job_title'] = []
#                         expected_job_title = row.xpath('string(td/p)').extract()[0]
#                         for job_title in expected_job_title.split("、"):
#                             jl_djw_data['objective']['expected_job_title'].append(job_title.strip())
#                     elif "期望行业" in row_name:
#                         jl_djw_data['objective']['trade'] = []
#                         trade = row.xpath('string(span)').extract()[0]
#                         for trade_title in trade.split("|"):
#                             jl_djw_data['objective']['trade'].append(trade_title.strip())
#                 #     # elif "求职性质" in row_name:
#     #                     jl_djw_data['objective']['job_nature'] = []
#     #                     job_nature = row.xpath('string(span)').extract()[0]
#     #                     jl_djw_data['objective']['job_nature'].append(job_nature.strip())
#     #                 elif "工作状态" in row_name:
#     #                     jl_djw_data['objective']['work_status'] = row.xpath('string(span)').extract()[0]
#     #                 elif "期望地点" in row_name:
#     #                     jl_djw_data['objective']['expected_address'] = []
#     #                     expected_address = row.xpath('string(span)').extract()[0]
#     #                     for address in expected_address.split("|"):
#     #                         jl_djw_data['objective']['expected_address'].append(address.strip())
#     #                 elif "期望薪水" in row_name:
#     #                     salary = row.xpath('string(span)').extract()[0]
#     #                     jl_djw_data['objective']['expected_salary_lower'] = int(salary.replace(".0", ""))
#     #                     jl_djw_data['objective']['expected_salary_upper'] = int(salary.replace(".0", ""))
#     #         if "个人评价" in section_name:
#     #             jl_djw_data['objective']['self_evaluation'] = \
#     #             section.xpath('string(div[@class="des"]/p)').extract()[0].replace("\r", "").replace("\n",
#     #                                                                                                 "").replace(
#     #                 "\t", "").replace(" ", "")
#     #
#     #         # 工作经历
#     #         elif "工作经历" in section_name:
#     #             for project in section.xpath('div[@class="project"]'):
#     #                 job_exp = {}
#     #                 company = project.xpath('string(div[@class="row item-title"])').extract()[0]
#     #                 job_exp['company'] = company.split("(")[0]
#     #                 job_exp['job_title'] = project.xpath('string(div[@class="row sub-title"])').extract()[0]
#     #                 # 起止时间
#     #                 during_time = project.xpath('string(div/em)').extract()[0]
#     #                 during_start = during_time.replace("(", "").replace(")", "").split("-")[0].replace(".",
#     #                                                                                                    "-").strip()
#     #                 job_exp['during_start'] = during_start + "-01"
#     #                 during_end = during_time.replace("(", "").replace(")", "").split("-")[1].replace(".",
#     #                                                                                                  "-").strip()
#     #                 if "至今" in during_end:
#     #                     job_exp['during_end'] = '2099-01-01'
#     #                 else:
#     #                     job_exp['during_end'] = during_end + "-01"
#     #                 # 所属行业、公司性质、公司规模、部门、职位类别、工作内容描述
#     #                 for row in project.xpath('div[@class="row"]'):
#     #                     if "所属行业" in row.xpath('string(label)').extract()[0]:
#     #                         job_exp['trade'] = row.xpath('string(span)').extract()[0].strip()
#     #                     elif "公司性质" in row.xpath('string(label)').extract()[0]:
#     #                         company_xz = row.xpath('string(span)').extract()[0].strip()
#     #                         job_exp['company_nature'] = company_xz.split("|")[0].strip()
#     #                         job_exp['company_scale'] = company_xz.split("|")[1].strip()
#     #                     elif "所属部门" in row.xpath('string(label)').extract()[0]:
#     #                         job_exp['department'] = row.xpath('string(span)').extract()[0].strip()
#     #                     elif "工作内容" in row.xpath('string(label)').extract()[0]:
#     #                         job_exp['job_content'] = row.xpath('string(span)').extract()[0].replace("\r",
#     #                                                                                                 "").replace(
#     #                             "\n", "").replace("\t", "").replace(" ", "")
#     #
#     #                 jl_djw_data['jobs'].append(job_exp)
#     #
#     #                 pass
#     #
#     #                 # row_name = row.xpath('string(label)').extract()[0]
#     #                 #
#     #                 # elif "期望薪水" in row_name:
#     #                 #     salary = row.xpath('string(span)').extract()[0]
#     #                 #     jl_djw_data['objective']['expected_salary_lower'] = int(salary.replace(".0", ""))
#     #                 #     jl_djw_data['objective']['expected_salary_upper'] = int(salary.replace(".0", ""))
#     #
#     #         # 项目经历
#     #         elif "项目经历" in section_name:
#     #             for project in section.xpath('div[@class="project"]'):
#     #                 project_exp = {}
#     #                 title = project.xpath('string(div[@class="row item-title"])').extract()[0]
#     #                 project_exp['title'] = title.split("（")[0].strip()
#     #                 # 起止时间
#     #                 during_time = project.xpath('string(div/em)').extract()[0]
#     #                 during_start = during_time.replace("（", "").replace("）", "").split("-")[0].replace(".",
#     #                                                                                                    "-").strip()
#     #                 project_exp['during_start'] = during_start + "-01"
#     #                 during_end = during_time.replace("（", "").replace("）", "").split("-")[1].replace(".",
#     #                                                                                                  "-").strip()
#     #                 if "至今" in during_end:
#     #                     project_exp['during_end'] = '2099-01-01'
#     #                 else:
#     #                     project_exp['during_end'] = during_end + "-01"
#     #                 # 职位描述、项目描述
#     #                 for row in project.xpath('div[@class="row"]'):
#     #                     if "职责描述" in row.xpath('string(label)').extract()[0]:
#     #                         project_exp['duty'] = row.xpath('string(span)').extract()[0].replace("\r", "").replace(
#     #                             "\n", "").replace("\t", "").replace(" ", "")
#     #                     elif "项目描述" in row.xpath('string(label)').extract()[0]:
#     #                         project_exp['description'] = row.xpath('string(span)').extract()[0].replace("\r",
#     #                                                                                                     "").replace(
#     #                             "\n", "").replace("\t", "").replace(" ", "")
#     #
#     #                 jl_djw_data['projects'].append(project_exp)
#     #
#     #                 pass
#     #
#     #                 # row_name = row.xpath('string(label)').extract()[0]
#     #                 #
#     #                 # elif "期望薪水" in row_name:
#     #                 #     salary = row.xpath('string(span)').extract()[0]
#     #                 #     jl_djw_data['objective']['expected_salary_lower'] = int(salary.replace(".0", ""))
#     #                 #     jl_djw_data['objective']['expected_salary_upper'] = int(salary.replace(".0", ""))
#     #
#     #         # 教育经历
#     #         elif "教育经历" in section_name:
#     #             for project in section.xpath('div[@class="project"]'):
#     #                 edu_exp = {}
#     #                 school = project.xpath('string(div[@class="row item-title"])').extract()[0]
#     #                 edu_exp['school'] = school.split("（")[0].split("(")[0].strip()
#     #                 # 起止时间
#     #                 during_time = project.xpath('string(div/em)').extract()[0]
#     #                 during_start = \
#     #                 during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[
#     #                     0].replace(".", "-").strip()
#     #                 edu_exp['during_start'] = during_start + "-01"
#     #                 during_end = \
#     #                 during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[
#     #                     1].replace(".", "-").strip()
#     #                 if "至今" in during_end:
#     #                     edu_exp['during_end'] = '2099-01-01'
#     #                 else:
#     #                     edu_exp['during_end'] = during_end + "-01"
#     #                 # 学历、专业
#     #                 xue_zhuan = project.xpath('string(div[@class="row sub-title"])').extract()[0]
#     #                 edu_exp['degree'] = xue_zhuan.split("|")[0].strip()
#     #                 edu_exp['major'] = xue_zhuan.split("|")[1].strip()
#     #                 jl_djw_data['educations'].append(edu_exp)
#     #
#     #         # 培训经历
#     #         elif "培训经历" in section_name:
#     #             for project in section.xpath('div[@class="project"]'):
#     #                 trainings_exp = {}
#     #                 training_course = project.xpath('string(div[@class="row item-title"])').extract()[0]
#     #                 trainings_exp['training_course'] = training_course.split("（")[0].strip()
#     #                 # 起止时间
#     #                 during_time = project.xpath('string(div/em)').extract()[0]
#     #                 during_start = \
#     #                     during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[
#     #                         0].replace(".", "-").strip()
#     #                 trainings_exp['during_start'] = during_start + "-01"
#     #                 during_end = \
#     #                     during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("-")[
#     #                         1].replace(".", "-").strip()
#     #                 if "至今" in during_end:
#     #                     trainings_exp['during_end'] = '2099-01-01'
#     #                 else:
#     #                     trainings_exp['during_end'] = during_end + "-01"
#     #                 # 培训描述、培训机构
#     #                 for row in project.xpath('div[@class="row"]'):
#     #                     if "培训机构" in row.xpath('string(label)').extract()[0]:
#     #                         trainings_exp['training_agency'] = row.xpath('string(span)').extract()[0].replace("\r",
#     #                                                                                                           "").replace(
#     #                             "\n", "").replace("\t", "").replace(" ", "")
#     #                     elif "培训描述" in row.xpath('string(label)').extract()[0]:
#     #                         trainings_exp['description'] = row.xpath('string(span)').extract()[0].replace("\r",
#     #                                                                                                       "").replace(
#     #                             "\n", "").replace("\t", "").replace(" ", "")
#     #
#     #                 jl_djw_data['trainings'].append(trainings_exp)
#     #
#     #                 pass
#     #
#     #                 # row_name = row.xpath('string(label)').extract()[0]
#     #                 #
#     #                 # elif "期望薪水" in row_name:
#     #                 #     salary = row.xpath('string(span)').extract()[0]
#     #                 #     jl_djw_data['objective']['expected_salary_lower'] = int(salary.replace(".0", ""))
#     #                 #     jl_djw_data['objective']['expected_salary_upper'] = int(salary.replace(".0", ""))
#     #
#     #         # 证书
#     #         elif "证书" in section_name:
#     #             for project in section.xpath('div[@class="project"]'):
#     #                 credentials = {}
#     #                 title = project.xpath('string(div[@class="row item-title"])').extract()[0]
#     #                 credentials['title'] = title.split("（")[0].strip()
#     #                 # 起止时间
#     #                 during_time = project.xpath('string(div/em)').extract()[0]
#     #                 during_start = \
#     #                     during_time.replace("（", "").replace("）", "").replace("(", "").replace(")", "").split("获得")[
#     #                         0].replace(".", "-").strip()
#     #                 credentials['get_date'] = during_start + "-01"
#     #                 jl_djw_data['credentials'].append(credentials)
#     #
#     #         # 技能、语言
#     #         elif "技能" in section_name:
#     #             for project in section.xpath('div[@class="skill"]/ul/li'):
#     #                 ji_neng = {}
#     #                 ji_ne = project.xpath('string()').extract()[0]
#     #                 ji_neng['skill'] = ji_ne.split("|")[0].strip()
#     #                 ji_neng['level'] = ji_ne.split("|")[1].strip()
#     #                 jl_djw_data['languages'].append(ji_neng)
#
#     # # jl_djw_data['org'] = {}
#     # # jl_djw_data['org']['resume_type'] = 6
#     # # jl_djw_data['org']['org_id'] = org_id
#     # # try:
#     # #     if jl_djw_data['info']['mobilephone']:
#     # #         jl_djw_data['org']['download_status'] = 1
#     # # except:
#     # #     jl_djw_data['org']['download_status'] = 0
#     # # # 插件
#     # # jl_djw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
#     # # # 搜索/推荐----------遇仁职位ID
#     # # if lx == 2:
#     # #     jl_djw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
#     # #     if job_id:
#     # #         jl_djw_data['org']['job_id'] = job_id
#     # # # 收件箱--------------渠道职位ID
#     # # elif lx == 1:
#     # #     jl_djw_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]
#     # #     if job_id:
#     # #         jl_djw_data['org']['job_id'] = job_id
#     # # # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
#     # # if dt:
#     # #     jl_djw_data['org']['delivery_time'] = dt
#
#     print(jl_djw_data)
#     return jl_djw_data
