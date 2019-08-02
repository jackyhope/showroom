import json
import re
import requests
import datetime
import time
from lxml import etree
from scrapy import Selector
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

def first_show(s, list_1):
    list2 = []
    for ss1 in list_1:
        if ss1 in s:
            ss1_inx = s.index(ss1)
            list2.append(ss1_inx)
        else:
            pass
    return min(list2)
# 源码解析---时间相关
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

def dl_51(sjx_51_text):
    sel = Selector(text=sjx_51_text)
    data_51 = {}
    data_51['info'] = {}
    data_51['info']['channel'] = 2
    phone_xpa = '//img[contains(@src,"image/resumedetails/y2.png")]/parent::td/text()'
    email_xpa = '//a[contains(@href,"mailto:")]/text()'
    try:
        data_51['info']['name'] = sel.xpath('//td[@class="name"]/text()').extract()[0].strip()
    except:
        data_51['info']['name'] = ''
    try:
        data_51['info']['phone'] = sel.xpath(phone_xpa).extract()[0].strip()
    except:
        data_51['info']['phone'] = ''
    try:
        data_51['info']['email'] = sel.xpath(email_xpa).extract()[0].strip()
    except:
        data_51['info']['email'] = ''
    return data_51
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

# (sjx_51_text=qc_text, lx=0, org_id=org_id, ds=0)


class Module_51(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_51, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    # 51登录判断
    def login_judge_51(self):
        home_url = 'https://ehire.51job.com/Navigate.aspx'
        response = self.session.get(url=home_url, headers=self.headers)

        strKey = re.search(r'var strKey = "(.*?)";', response.text).group(1)
        url = 'https://ehire.51job.com/ajax/Navi/GlobalGlightNaviAjax.ashx'
        data = {
            'doType': 'getresourcesnumber',
            'resName': 'top,job,sms,rsmtodwn,resume',
            'Key': strKey
        }
        response = self.session.post(url=url, headers=self.headers, data=data)
        res = json.loads(response.text)
        return {'resume_num': int(res['resume_num'] if res['resume_num'] != '' else 0),
                'job_num': int(res['job_num'] if res['job_num'] != '' else 0), 'sms_num': int(res['sms_num'] if res['sms_num'] != '' else 0)}

    # 51职位刷新
    def refresh_job_51(self, JobID):
        refresh_url = 'https://ehire.51job.com/ajax/jobs/GlobalJobsAjax.ashx'
        data = {
            'doType': 'Refresh',
            'JobID': JobID,
            'Flag': '1',
        }
        response = self.session.post(url=refresh_url, headers=self.headers, data=data)
        if '<succrefreshedCount><![CDATA[1]]></succrefreshedCount>' in response.text:
            return True

    # 51简历搜索下载
    def search_51(self, userid):
        search_url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
        data = {
            'searchValueHid': '{userid}##0##########99############1#0###0#0#0'.format(userid=userid)
        }
        search_response = self.session.post(url=search_url, headers=self.headers, data=data)
        if '抱歉，没有搜到您想找的简历！' not in search_response.text:
            download_url = 'https://ehire.51job.com/Ajax/Resume/GlobalDownload.aspx'
            data = {
                'userid': userid,
                'doType': 'SearchToCompanyHr',
                'pageCode': '3',
            }
            download_response = self.session.post(url=download_url, headers=self.headers, data=data)

            html = etree.HTML(search_response.text)
            details_url = 'https://ehire.51job.com' + html.xpath('//div[@class="Common_list-table"]/table/tbody/tr[1]/td[@class="Common_list_table-id-text"]/span/a/@href')[0]
            details_response = self.session.get(url=details_url, headers=self.headers)

            return download_response, details_response
        else:
            return None, None

    # 51查看前询问
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

    # 51简历搜索
    @staticmethod
    def search_resume_51(data):
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
        if agefrom != '':
            if int(agefrom) < 18:
                agefrom = '18'
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
                          '全日制' if data['fullTime'] == 1 else '', '海外留学' if data['overseasStudy'] == 1 else '']).strip()
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

    # 51查看简历
    def read_resume_51(self, searchValueHid, orgid, jobid, max_num):
        def paging(response_page):
            nonlocal data_wu_51, ss_num, scpy_again

            time.sleep(random.uniform(5, 8))
            if '<input name="hidShowCode" type="hidden" id="hidShowCode" value="1" />' in response_page.text:
                logging.error('对不起,由于您的操作过于频繁,请输入验证码!')
                time.sleep(60*10)
                scpy_again = True
                return

            if '抱歉，没有搜到您想找的简历！' in response_page.text:
                return

            VIEWSTATE = re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', response_page.text).group(1)
            hidCheckUserIds = re.search(r'<input name="hidCheckUserIds" type="hidden" id="hidCheckUserIds" value="(.*?)" />', response_page.text).group(1)
            hidCheckKey = re.search(r'<input name="hidCheckKey" type="hidden" id="hidCheckKey" value="(.*?)" />', response_page.text).group(1)
            logging.error('now page jl list: ', hidCheckUserIds)

            html = etree.HTML(response_page.text)
            lis = html.xpath('//div[@class="Common_list-table"]/table/tbody/tr')
            lis1 = [value for key, value in enumerate(lis) if key % 2 == 0]
            ask_result = self.ask_before_read(lis1, orgid, jobid)

            for key, value in enumerate(lis1):
                try:
                    ask_status = ask_result[key]
                except:
                    logging.error('date is not new，stop scrapy...')
                    return

                if ask_status == '1':
                    try:
                        details_url = 'https://ehire.51job.com' + value.xpath('./td[2]/span[1]/a/@href')[0]
                        details_response = self.session.get(url=details_url, headers=get_useragent(), data={'hidShowCode': '0'})
                        while 1:
                            if '<input name="hidShowCode" type="hidden" id="hidShowCode" value="1" />' in details_response.text:
                                logging.error('对不起,由于您的操作过于频繁,请输入验证码!')
                                time.sleep(60*10)
                                details_response = self.session.get(url=details_url, headers=get_useragent())
                            else:
                                break
                        try:
                            final_data = jx_51_ss(text=details_response.text, ds=0, org_id=orgid, job_id=jobid, lx=2)
                        except:
                            final_data = jx_51_sjx(text=details_response.text, ds=0, org_id=orgid, job_id=jobid, lx=2)

                        data_wu_51.append(final_data)
                        ss_num = ss_num + 1

                    except:
                        logging.error("this jl parse wrong...")
                        continue

                    if ss_num >= max_num:
                        return

                    if len(data_wu_51) == 3:
                        data = json.dumps(data_wu_51)
                        data = data.encode('utf-8')
                        requests.post(url=wu_jl_url, data=data)
                        data_wu_51 = []

                    time.sleep(random.uniform(5, 8))

            post_data = {
                '__EVENTTARGET': 'pagerBottomNew$nextButton',
                'hidShowCode': '0',
                '__VIEWSTATE': VIEWSTATE,
                'hidCheckUserIds': hidCheckUserIds,
                'hidCheckKey': hidCheckKey,
                'ctrlSerach$hidSearchValue': searchValueHid
            }
            response_page = self.session.post(url=url, headers=get_useragent(), data=post_data)
            paging(response_page)

        data_wu_51 = []
        ss_num = 0

        url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
        while 1:
            scpy_again = False
            response = self.session.post(url=url, headers=get_useragent(), data={'hidShowCode': '0', 'searchValueHid': searchValueHid})
            paging(response)
            if not scpy_again:
                break

        if len(data_wu_51) > 0:
            data = json.dumps(data_wu_51)
            data = data.encode('utf-8')
            requests.post(url=wu_jl_url, data=data)
            data_wu_51 = []

        return ss_num
