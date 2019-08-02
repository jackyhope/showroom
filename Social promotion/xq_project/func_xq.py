# -*- coding: utf-8 -*- 
# @Author : Zhy

import requests
import time
import json
import logging
import traceback
import random
import pymysql
from scrapy import Selector
from setting import *
from xq_project.Logger import Log
from reset_num import update_crawelNum,select_crawelNum
import string
import os
import base64

log = Log('comment')
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
url_gener=URL_GENTER       #内网,询问指定文章是否已评论过
url_result=URL_RESULT      #内网,提交评论结果
url_channel=URL_CHANNEL    #内网,提交账号状态
url_login=URL_LOGIN        #内网，http_login请求地址
def xh_pd_req(pos_url,data,headers):
    num=0
    flag = True
    while flag:
        try:
            if num<3:

                if data == '':
                    job_xq_text = requests.get(url=pos_url,headers=headers,timeout=3,proxies=proxies)
                else:
                    job_xq_text = requests.get(url=pos_url,params=data,headers=headers,timeout=3,proxies=proxies)

                if job_xq_text.status_code  == 200:

                    return job_xq_text.text
                else:
                    num = num + 1
                    time.sleep(random.uniform(1,1.5))
                    continue

            else:
                flag = False
        except:
            pass
def xh_session(s_type,session,pos_url,data,headers):
    num = 0
    flag = True
    while flag:
        try:
            if num < 3:
                if s_type=='get':

                    if data == '':
                        job_xq_text = session.get(url=pos_url, headers=headers, timeout=3, proxies=proxies)
                    else:
                        job_xq_text = session.get(url=pos_url, params=data, headers=headers, timeout=3, proxies=proxies)
                elif s_type == 'post':

                    if data == '':
                        job_xq_text = session.post(url=pos_url, headers=headers, timeout=3, proxies=proxies)
                    else:
                        job_xq_text = session.post(url=pos_url, data=data, headers=headers, timeout=3,proxies=proxies)

                if job_xq_text.status_code == 200:

                    return job_xq_text.text
                else:
                    num = num + 1
                    time.sleep(random.uniform(1, 1.5))
                    continue

            else:
                flag = False
        except:

            pass
def get_random_str():
    list = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in
                                                                                 range(10)]  # 大写字母+小写字母+数字
    FH = ('!', '@', '#', '$', '%', '&', '_')  # 特殊字符
    for f in FH:
        list.append(f)
    num = random.sample(list, 2)
    str_1 = ''
    value = str_1.join(num)  # 将取出的十个随机数进行重新合并
    if not value[0].isdigit():
        return value
def qx_test_cookie(cookie,data_acc):
    '''判断cookie是否有效，失效则给http_login服务端发送重新登录请求'''

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'xueqiu.com',
        'Referer': 'https://xueqiu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
    }

    url_sy = 'https://xueqiu.com/'
    re_num=1
    while True:
        if re_num >3:
            break
        try:
            sy_text = requests.get(url=url_sy, headers=headers,proxies=proxies,)
            if sy_text.status_code  == 200 or sy_text.status_code  == 403:
                break
            else:
                re_num=re_num+1
                time.sleep(random.uniform(2, 3))
        except:
            re_num = re_num + 1
            time.sleep(random.uniform(2,3))
            pass
    # sy_text = xh_pd_req(pos_url=url_sy,data='',headers=headers)

    if '没有账号？立即注册' in sy_text.text:
        return '该账号登录状态失效'
    else:
        return '该账号登录状态有效'

def random_operation(cookie,article_id,):
    num=random.randint(1,3)

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'xueqiu.com',
        'Referer': 'https://xueqiu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
    }

    if num == 1:
        try:
            url_like='https://xueqiu.com/statuses/like.json'
            a=requests.post(url=url_like,headers=headers,data={'id':article_id}).text
            # print(a)
        except:
            pass
    elif num == 2:
        try:
            url_favor='https://xueqiu.com/favorites/create.json?id={}'.format(article_id)
            a=requests.post(url=url_favor,headers=headers).text
            # print(a)
        except:
            pass
    elif num ==3:
        try:
            url_sy='https://xueqiu.com/'
            a=requests.get(url=url_sy,headers=headers).text
        except:
            pass
def sleep_time(task_id,cookie,article_id):
    state = qx_test_cookie(cookie,'')
    if '该账号登录状态失效' in state or '未能查询到账号' in state:
        return 2
    try:
        random_operation(cookie,article_id)
    except:
        pass
    num=0
    while True:

        time.sleep(random.uniform(120, 240))

        state = r.hmget('thread:pid', task_id)
        try:
            if int(state[0]) == 0:
                log.logger.info('退出任务：{}成功'.format(task_id))
                print('退出任务：{}成功'.format(task_id))
                return 1
            else:
                num=num+1
            if num >=5:
                return 0

        except:
            log.logger.info('该任务：{}被异常终止'.format(task_id))
            return 1

def submit_unusual(data,task,state):
    '''提交账号异常'''

    try:
        data_1 = json.dumps({'accinfo':task,'act':'cookie_notuse',})
        data_1 = data_1.encode('utf-8')
        a = requests.post(url=url_login, data=data_1).text
    except:
        pass

    try:
        data_acc_xq = {'id': task['accountId'],
                       'orgId': data['orgId'],
                       'headUrl': '',  # 账号头像
                       'focusNum': '',  # 关注人数
                       'status': 1,  # 账号状态，0正常，1异常
                       'nickname': '',
                       'errorDescription': state  # 异常信息
                       }
        data_acc_xq = json.dumps(data_acc_xq)
        data_acc_xq = data_acc_xq.encode('utf-8')
        state_acc_xq = requests.post(url=url_channel, data=data_acc_xq,
                                     headers={'Content-type': 'application/json'}).text
        print('提交账号失效异常：{}'.format(state_acc_xq))
    except:
        pass

def get_cookie(task):
    '''从数据库中查询到对应账号的cookie'''

    while True:
        try:

            conn = pymysql.connect(host=MYSQL_HOST, port=PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD,
                                   db=MYSQL_DB,
                                   charset='utf8')
            cursor = conn.cursor()
            break
        except:
            # traceback.print_exc()
            time.sleep(3)

    try:
        sql_select_cookie = 'select cookie from cookie_pool where username={} and channelType={}'.format(task['taskAcc'],task['channelType'])
        conn.ping(reconnect=True)
        cur_cookie = cursor.execute(sql_select_cookie)
        cur_cookie = cursor.fetchall()
        cookie=cur_cookie[0][0]
        data_acc={'channelAcc':task['taskAcc'],'type':task['channelType'],'act':'cookie_notuse','ownerAcc':task['ownerAcc']}

        state=qx_test_cookie(cookie,data_acc)

        if state== '该账号登录状态有效':
            return cookie
        else:
            return '该账号登录状态失效'

    except:
        return '未能查询到账号'
def get_art_id(user_id,headers):
    '''获取指定博主最近一条发布的文章id'''

    url_user = 'https://xueqiu.com/u/{}'.format(user_id)
    # html_user = requests.get(url=url_user, headers=headers,proxies=proxies).text
    html_user = xh_pd_req(pos_url=url_user,data='',headers=headers)

    sel_1=Selector(text=html_user)
    u_id=sel_1.xpath('string(//div[@class="container profiles__main__container"]/input/@value)').extract()[0].strip()
    url_id = 'https://xueqiu.com/v4/statuses/user_timeline.json?page=1&user_id={}&type=0'.format(u_id)
    # request_art = requests.get(url=url_id, headers=headers,proxies=proxies).text
    request_art = xh_pd_req(pos_url=url_id,data='',headers=headers)

    json_art = json.loads(request_art)
    art_id = json_art['statuses'][0]['id']
    return art_id
def Comment(article_id,task,cookie):
    '''通过文章id按要求实现评论'''

    '''
    :param article_id: 文章id
    :param type: 评论的类别，纯文本：text，文本+图片：photo
    :return: 评论结果，无权限评论、评论成功、评论失败
    '''

    '''判断该文章是否有权限评论'''

    text_1='''那些光线。那些日出。那些晨雾。一样都会准时而来。无限漫长时光里的温柔。无限温柔里的漫长时光。一直都在。疼痛。是疼还是痛。有区别吗。心疼和心痛。有区别吗。不安全。不安分。不安稳。不安静。不安宁。不安心。那些光线。那些日出。那些晨雾。一样都会准时而来。无限漫长时光里的温柔。无限温柔里的漫长时光。一直都在。疼痛。是疼还是痛。有区别吗。心疼和心痛。有区别吗。不安全。不安分。不安稳。不安静。不安宁。不安心。'''

    list_text=text_1.split('。')

    if task['imageUrl'] == '':
        comment_type='text'
    else:
        comment_type='photo'

    time_1=str(time.time()*1000)[:13]

    url_1='https://xueqiu.com/statuses/allow_reply.json?status_id={}&_={}'.format(article_id,time_1)
    session=requests.session()
    headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie': cookie,
        'Host':'xueqiu.com',
        'Referer':'https://xueqiu.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
    }
    # state=session.get(url=url_1,headers=headers,proxies=proxies).text
    state=xh_session(s_type='get',session=session,pos_url=url_1,data='',headers=headers)
    dict_state=json.loads(state)
    try:
        if dict_state['success']:

            '''获取session_token'''
            time_2 = str(time.time() * 1000)[:13]
            url_2='https://xueqiu.com/provider/session/token.json?api_path=%2Fstatuses%2Freply.json&_={}'.format(time_2)
            # request_token=session.get(url=url_2,headers=headers,proxies=proxies).text
            request_token=xh_session(s_type='get',session=session,pos_url=url_2,data='',headers=headers)

            dict_token=json.loads(request_token)
            session_token=dict_token['session_token']


            if comment_type == 'text':
                '''纯文字评论'''

                # comment=task['text'] +'---' + get_random_str()
                comment=task['text'] +'---' + random.choice(list_text)

                comment_text='<p>{}</p>'.format(comment)

            elif comment_type == 'photo':

                '''文本+图片评论'''
                url_photo = task['imageUrl']
                time_photo = str(time.time() * 1000)[:13]
                while True:
                    try:
                        r = requests.get(url_photo)
                        if r.status_code == 200:
                            break
                        else:
                            time.sleep(random.uniform(2,3))
                    except:
                        time.sleep(random.uniform(2,3))

                with open('{}.png'.format(time_photo), 'wb') as f:
                    f.write(r.content)
                f.close()
                comment=task['text']  +'---'+ random.choice(list_text)
                photo_path='{}.png'.format(time_photo)
                url_upload='https://xueqiu.com/photo/upload.json'
                headers_1 = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    'Cookie': cookie,
                    'Host': 'xueqiu.com',
                    'Referer': 'https://xueqiu.com/u/{}'.format(article_id),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
                }
                fo=open(photo_path, 'rb')
                files = {'file': (photo_path, fo, 'image/png')}
                num=1

                # while True:
                #     if num<5:
                #         try:
                #             request_photo=requests.post(url=url_upload,files=files,headers=headers_1,proxies=proxies).text
                #             print(request_photo)
                #             break
                #         except:
                #             num=num+1
                #             pass

                while True:
                    if num<5:
                        try:
                            request_photo=requests.post(url=url_upload,files=files,headers=headers_1,proxies=proxies)
                            print(request_photo.text)
                            if request_photo.status_code == 200:
                                break
                            else:
                                time.sleep(random.uniform(1, 3))
                        except:
                            time.sleep(random.uniform(1,3))
                            num=num+1
                            traceback.print_exc()
                            pass
                    else:
                        break

                dict_photo=json.loads(request_photo.text)
                new_photo_path=dict_photo['filename']
                comment_text='<p>{}</p><img src="//xqimg.imedao.com/{}" class="co-img-link">'.format(comment,new_photo_path)

                fo.close()

                try:
                    time.sleep(5)
                    print('本地', photo_path)
                    os.remove(photo_path)
                except:
                    traceback.print_exc()
                    pass

            url_3 = 'https://xueqiu.com/statuses/reply.json'
            data = {'comment': comment_text,
                    'forward': '0',
                    'id': article_id,
                    'session_token': session_token}
            request_text = session.post(url=url_3, headers=headers, data=data,proxies=proxies)
            # request_text = xh_session(s_type='post',session=session,pos_url=url_3,data=data,headers=headers)
            print(request_text.text)

            if request_text.status_code == 200:
                return '评论成功'

            elif request_text.status_code == 400:
                log.logger.info('评论限制：{}'.format(request_text))
                return '爬取限制'

        else:
            return '无权限评论'
    except:
        traceback.print_exc()
        pass

def xq_classify(data,task):
    '''
    :param data:任务模块数据 
    :param task:单任务 
    '''
    log.logger.info('接收雪球分类评论任务:{}'.format(task['id']))
    state=get_cookie(task)
    if '该账号登录状态失效' in state or '未能查询到账号' in state:
        submit_unusual(data,task,'登录失效')
        log.logger.info('该任务账号：{}cookie失效'.format(task['taskAcc']))
    else:
        '''账号状态正常'''
        cookie=state
        article_num=200
        list_key=[]

        if ',' in task['groupClass']:
            list_key = task['groupClass'].split(',')
        else:
            list_key.append(task['groupClass'])
        try:
            odd_num = select_crawelNum(task['taskAcc'], 3)
            artic_num = int((200 - odd_num) / len(list_key))
            print(artic_num)
            log.logger.info('当前账号已评论：{}次,当前分类将各爬取:{}次'.format(odd_num, artic_num))
        except:
            traceback.print_exc()
            pass

        for article_key in list_key:
            print(article_key)
            try:
                article_key=article_key.strip()

                try:
                    crawel_num = select_crawelNum(task['taskAcc'], 3)
                    if crawel_num >= 200:
                        log.logger.info('账号{}当天已满200条'.format(task['taskAcc']))
                        return
                except:
                    traceback.print_exc()
                    pass

                headers = {
                           'Cookie': cookie,
                           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
                           'Host':'xueqiu.com',
                           'Connection':'keep-alive'
                           }
                dict_art_type = {'3051': {'name': '互联网', 'value': '1'},
                                 '3052': {'name': '节能环保', 'value': '118'}, '3053': {'name': '成长股', 'value': '67'},
                                 '3054': {'name': '稀土有色', 'value': '113'},
                                 '3055': {'name': '服装家纺', 'value': '32'},
                                 '3056': {'name': '量化投资', 'value': '71'},
                                 '3057': {'name': '农林牧渔', 'value': '39'},
                                 '3058': {'name': '人工智能', 'value': '129'},
                                 '3063': {'name': '基金达人', 'value': '85'},
                                 '3001': {'name': '军工国防', 'value': '77'},
                                 '3002': {'name': '人气用户', 'value': '100'},
                                 '3003': {'name': '文体传媒', 'value': '63'},
                                 '3004': {'name': '公司高管', 'value': '131'},
                                 '3005': {'name': '旅游餐饮', 'value': '16'},
                                 '3006': {'name': '新金融', 'value': '126'},
                                 '3007': {'name': '保险产品', 'value': '89'},
                                 '3008': {'name': '医药业', 'value': '19'},
                                 '3009': {'name': '基金经理', 'value': ''},
                                 '3010': {'name': '财经媒体', 'value': ''},
                                 '3011': {'name': '区块链', 'value': '125'},
                                 '3012': {'name': '期货对冲', 'value': '52'},
                                 '3013': {'name': '专家学者', 'value': '101'},
                                 '3014': {'name': '煤炭', 'value': '112'},
                                 '3015': {'name': '房地产', 'value': '20'},
                                 '3016': {'name': '航空运输', 'value': '115'},
                                 '3017': {'name': '机械制造', 'value': '116'},
                                 '3018': {'name': '活跃财经媒体', 'value': '74'},
                                 '3019': {'name': '自媒体', 'value': '132'},
                                 '3020': {'name': '活跃分析师', 'value': '29'},
                                 '3021': {'name': '公用事业', 'value': '114'},
                                 '3022': {'name': '美股达人', 'value': '59'},
                                 '3023': {'name': '半导体', 'value': '120'},
                                 '3024': {'name': '钢铁', 'value': '111'},
                                 '3025': {'name': '组合达人', 'value': '106'},
                                 '3026': {'name': '平台账号', 'value': '86'},
                                 '3027': {'name': '电力', 'value': '110'},
                                 '3028': {'name': 'AR/VR', 'value': '91'},
                                 '3029': {'name': '电子', 'value': '38'},
                                 '3030': {'name': '教育', 'value': '122'},
                                 '3031': {'name': '食品饮料', 'value': '31'},
                                 '3032': {'name': '活跃基金经理', 'value': '7'},
                                 '3033': {'name': '债券', 'value': '109'},
                                 '3034': {'name': '家电家居', 'value': '35'},
                                 '3035': {'name': '技术趋势', 'value': '64'},
                                 '3036': {'name': '新能源', 'value': '57'},
                                 '3037': {'name': '银行', 'value': '87'},
                                 '3038': {'name': '汽车行业', 'value': '119'},
                                 '3039': {'name': '上市公司', 'value': '130'},
                                 '3040': {'name': '化工', 'value': '30'},
                                 '3041': {'name': '金融机构', 'value': '49'},

                                 '3042': {'name': '建筑建材', 'value': '36'},
                                 '3043': {'name': '证券', 'value': '107'},
                                 '3044': {'name': '港股达人', 'value': '60'},
                                 '3045': {'name': '财务分析', 'value': '13'},
                                 '3046': {'name': 'A股投资', 'value': '47'},
                                 '3047': {'name': '保险', 'value': '108'},
                                 '3048': {'name': '通信通讯', 'value': '6'},
                                 '1001': {'name': '美股', 'value': '101'},
                                 '1002': {'name': '房产', 'value': '111'},
                                 '1003': {'name': '头条', 'value': '-1'},
                                 '1004': {'name': '基金', 'value': '104'},
                                 '1005': {'name': '沪深', 'value': '105'},
                                 '1006': {'name': '汽车', 'value': '114'},
                                 '1007': {'name': '港股', 'value': '102'},
                                 '1008': {'name': '保险', 'value': '110'},
                                 '1009': {'name': '私募', 'value': '113'},
                                 '1010': {'name': '科创板', 'value': '115'},
                                 '3059': {'name': '可转债', 'value': '73'},
                                 '3060': {'name': '新材料', 'value': '37'},
                                 '3061': {'name': '交运运输', 'value': '22'},
                                 '3062': {'name': '策略宏观', 'value': '15'},
                                 '3049': {'name': '分析师', 'value': ''},
                                 '3064': {'name': '贵金属', 'value': '127'},
                                 '3065': {'name': '造纸', 'value': '128'},
                                 '3050': {'name': '电商零售', 'value': '33'}}

                list_art_id = []
                if str(article_key).startswith('10'):

                    count='10'
                    max_id='-1'
                    category=dict_art_type[article_key]['value']

                    logging.info('{}--'.format(dict_art_type[article_key]['name']))
                    while True:
                        try:
                            url_art_type='https://xueqiu.com/v4/statuses/public_timeline_by_category.json'
                            params={'since_id':'-1',
                                    'max_id':max_id,
                                    'count':count,
                                    'category':category}
                            # request_id=requests.get(url=url_art_type,headers=headers,params=params,proxies=proxies).text
                            request_id =xh_pd_req(pos_url=url_art_type, data=params, headers=headers)

                            dict_request_id=json.loads(request_id)
                            for art_id in dict_request_id['list']:
                                data_id=art_id['data'].split('\"id\":')[1].split(',\"title\"')[0].strip()
                                list_art_id.append(data_id)

                            if len(list_art_id) < article_num:
                                max_id=dict_request_id['next_max_id']
                                count=15
                            else:
                                break
                        except:
                            log.logger.exception("Exception Logged")
                            pass
                elif str(article_key) == '3009' or str(article_key) == '3010' or str(article_key) == '3049':
                    article_name=dict_art_type[article_key]['name']
                    logging.info('{}--'.format(article_name))
                    list_userid=[]
                    url_people='https://xueqiu.com/people'
                    # html_people=requests.get(url=url_people,headers=headers,proxies=proxies).text
                    html_people=xh_pd_req(pos_url=url_people, data='', headers=headers)
                    sel=Selector(text=html_people)

                    for influence in sel.xpath('//div[@class="bd topInfluence"]/div'):
                        try:
                            name=influence.xpath('string(h3/span[@class="title"])').extract()[0].strip()
                            if name == article_name:
                                for ul in influence.xpath('ul/li/div'):
                                    user_id=ul.xpath('string(div/a/@href)').extract()[0].strip()
                                    list_userid.append(user_id.split('/')[1])
                        except:
                            log.logger.exception("Exception Logged")
                            pass

                    for user_id in list_userid:
                        try:
                            time.sleep(random.uniform(1,1.5))
                            art_id=get_art_id(user_id,headers)
                            list_art_id.append(art_id)
                        except:
                            log.logger.exception("Exception Logged")
                            pass
                elif str(article_key).startswith('30'):

                    time_2 = str(time.time() * 1000)[:13]
                    id=dict_art_type[article_key]['value']
                    logging.info('{}--'.format(dict_art_type[article_key]['name']))
                    url='https://xueqiu.com/recommend/user/industry.json?id={}&_={}'.format(id,time_2)
                    # request_json=requests.get(url=url,headers=headers,proxies=proxies).text
                    request_json=xh_pd_req(pos_url=url, data='', headers=headers)
                    dict_art=json.loads(request_json)
                    for user in dict_art['industries'][0]['users']:
                        try:
                            time.sleep(random.uniform(1,3.5))
                            art_id=get_art_id(user['id'],headers)
                            list_art_id.append(art_id)
                            if len(list_art_id) >= artic_num:
                                break
                        except:
                            pass
                art_num=0
                log.logger.info('list_art_id:{}'.format(list_art_id))
                for art_id in list_art_id:
                    try:
                        '''查询任务是否需要停止'''
                        while True:
                            try:
                                state = r.hmget('thread:pid', task['id'])
                                break
                            except:
                                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
                                time.sleep(3)
                                pass

                        try:
                            print(state)
                            if int(state[0]) == 0:
                                log.logger.info('退出：{}成功'.format(task['id']))
                                print('退出：{}成功'.format(task['id']))
                                return
                        except:
                            log.logger.info('该任务：{}被异常终止'.format(task['id']))
                            return

                        '''查询是否已评论过'''

                        data_ask_xq = {'orgId': data['orgId'],
                                       'ownerAcc': task['ownerAcc'],
                                       'taskAcc': task['taskAcc'],  # 任务所选账号
                                       'digest': art_id  # 所评论文章的id
                                       }
                        data_ask_xq = json.dumps(data_ask_xq)
                        data_ask_xq = data_ask_xq.encode('utf-8')
                        try:
                            state_ask_xq = requests.post(url=url_gener, data=data_ask_xq,
                                                         headers={'Content-type': 'application/json'}).text
                            dict_ask_xq = json.loads(state_ask_xq)
                        except:
                            log.logger.error('查询是否已评论失败')
                            pass
                        if dict_ask_xq['status']:
                            '''在询问的结果为ture的情况下评论指定内容，并提交评论结果'''

                            sleep_state =sleep_time(task['id'],cookie,art_id)

                            if sleep_state == 0:
                                conclusion=Comment(art_id,task,cookie)
                                if '评论成功' in conclusion:
                                    art_num=art_num+1
                                    log.logger.info('评论成功：{}+{}'.format(task['taskAcc'],art_id))
                                    dict_submit_xq = {'orgId': data['orgId'],
                                                   'ownerAcc': task['ownerAcc'],
                                                   'taskAcc': task['taskAcc'],  # 任务所选账号
                                                   'taskId':task['id'],
                                                   'digest': art_id  # 所评论文章的id
                                                   }
                                    try:
                                        dict_submit_xq = json.dumps(dict_submit_xq)
                                        dict_submit_xq = dict_submit_xq.encode('utf-8')
                                        state_submit_xq = requests.post(url=url_result, data=dict_submit_xq,
                                                                        headers={'Content-type': 'application/json'}).text
                                        # print('提交：',state_submit_xq)
                                        # dict_return_xq = json.loads(state_submit_xq)
                                        try:
                                            crawel_num=update_crawelNum(task['taskAcc'],3)
                                            if crawel_num >= 200:
                                                log.logger.info('账号{}当天已满200条'.format(task['taskAcc']))
                                                return
                                        except:
                                            pass
                                        try:
                                            if art_num >= artic_num:
                                                log.logger.info('账号：{}已将分类：{}评论完毕'.format(task['taskAcc'],article_key))
                                                break
                                        except:
                                            pass
                                    except:
                                        log.logger.error('提交评论结果失败')
                                    pass
                                elif '无权限评论' in conclusion:
                                    log.logger.info('无权限评论：{}+{}'.format(task['taskAcc'],art_id))
                                elif '爬取限制' in conclusion:
                                    log.logger.info('评论限制：{}+{}'.format(task['taskAcc'],art_id))
                                    submit_unusual(data, task, '评论被限制')
                                    return
                                else:
                                    log.logger.info('评论失败：{}+{}'.format(task['taskAcc'],art_id))
                            elif sleep_state == 1:
                                return
                            elif sleep_state == 2:
                                submit_unusual(data, task,'登录失效')
                                log.logger.info('该任务账号：{}cookie失效'.format(task['taskAcc']))
                                return

                        elif not dict_ask_xq['status']:
                            if dict_ask_xq['msg'] == '已评论过':
                                log.logger.info('已评论过:{}+{}'.format(task['taskAcc'], art_id))

                    except:
                        log.logger.exception("Exception Logged")
                        log.logger.info('评论失败：{}+{}'.format(task['taskAcc'], art_id))
                        pass
            except:
                log.logger.info('当前分类出错：{}'.format(article_key))
                log.logger.exception("Exception Logged")
                pass

def xq_attention(data,task):
    log.logger.info('接收雪球分类评论任务:{}'.format(task['id']))
    state = get_cookie(task)
    if '该账号登录状态失效' in state or '未能查询到账号' in state:
        submit_unusual(data, task,'登录失效')
        log.logger.info('该任务账号:{}cookie失效'.format(task['taskAcc']))
    else:
        '''账号状态正常'''
        cookie=state
        headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
            'Host': 'xueqiu.com',
            'Connection': 'keep-alive'
        }
        time_1 = str(time.time() * 1000)[:13]
        user_id=cookie.split('u=')[1].split(';')[0]
        page_num=1
        flag=True
        list_art_id=[]
        while flag:
            try:
                time.sleep(random.uniform(0.5,1.5))
                url_att='https://xueqiu.com/friendships/groups/members.json?uid={}&page={}&gid=0&_={}'.format(user_id,str(page_num),time_1)
                text_att = xh_pd_req(pos_url=url_att, data='', headers=headers)

                dict_att=json.loads(text_att)
                max_page=dict_att['maxPage']

                for uesr in dict_att['users']:
                    try:
                        time.sleep(random.uniform(1,3))
                        art_id=get_art_id(uesr['id'], headers)
                        list_art_id.append(art_id)
                    except:
                        log.logger.exception("Exception Logged")
                        pass

                if page_num < max_page:
                    page_num=page_num+1
                else:
                    flag=False
            except:
                pass

        for article_id in list_art_id:
            '''查询是否已评论过'''
            try:
                while True:
                    try:
                        state = r.hmget('thread:pid', task['id'])
                        break
                    except:
                        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
                        time.sleep(3)
                        pass
                try:
                    log.logger.info(state)
                    if int(state[0]) == 0:
                        log.logger.info('退出：{}成功'.format(task['id']))
                        print('退出：{}成功'.format(task['id']))
                        return
                except:
                    log.logger.info('该任务：{}被异常终止'.format(task['id']))
                    return
                data_ask_xq = {'orgId': data['orgId'],
                               'ownerAcc': task['ownerAcc'],
                               'taskAcc': task['taskAcc'],  # 任务所选账号
                               'digest': article_id  # 所评论文章的id
                               }
                data_ask_xq = json.dumps(data_ask_xq)
                data_ask_xq = data_ask_xq.encode('utf-8')
                try:
                    state_ask_xq = requests.post(url=url_gener, data=data_ask_xq,
                                                 headers={'Content-type': 'application/json'}).text
                    state_ask_xq = json.loads(state_ask_xq)

                except:
                    traceback.print_exc()
                    log.logger.error('查询是否已评论失败')
                    log.logger.exception("Exception Logged")

                if state_ask_xq['status']:
                    '''在询问的结果为ture的情况下评论指定内容，并提交评论结果'''
                    sleep_state=sleep_time(task['id'],cookie,article_id)

                    if sleep_state == 0:
                        conclusion=Comment(article_id,task,cookie)
                        if '评论成功' in conclusion:
                            dict_submit_xq = {'orgId': data['orgId'],
                                           'ownerAcc': task['ownerAcc'],
                                           'taskAcc': task['taskAcc'],  # 任务所选账号
                                           'taskId':task['id'],
                                           'digest': article_id  # 所评论文章的id
                                           }
                            log.logger.info('评论成功:{}+{}'.format(task['taskAcc'], article_id))
                            try:
                                dict_submit_xq = json.dumps(dict_submit_xq)
                                dict_submit_xq = dict_submit_xq.encode('utf-8')
                                state_submit_xq = requests.post(url=url_result, data=dict_submit_xq,
                                                                headers={'Content-type': 'application/json'}).text
                                dict_return_xq = json.loads(state_submit_xq)
                            except:
                                traceback.print_exc()
                                log.logger.error('提交评论结果失败')
                                log.logger.exception("Exception Logged")
                            try:
                                crawel_num=update_crawelNum(task['taskAcc'],3)
                                if crawel_num==200:
                                    log.logger.info('账号{}当天已满200条'.format(task['taskAcc']))
                                    return
                            except:
                                traceback.print_exc()
                                pass
                        elif '无权限评论' in conclusion:
                            log.logger.info('无权限评论：{}+{}'.format(task['taskAcc'], art_id))
                        elif '爬取限制' in conclusion:
                            log.logger.info('评论限制：{}+{}'.format(task['taskAcc'], art_id))
                            submit_unusual(data, task, '评论被限制')
                            return
                        else:
                            log.logger.error('评论失败：{}+{}'.format(task['taskAcc'], article_id))
                            pass
                    elif sleep_state == 1:
                        return
                    elif sleep_state == 2:
                        submit_unusual(data, task,'登录失效')
                        log.logger.info('该任务账号：{}cookie失效'.format(task['taskAcc']))
                        return

                elif not state_ask_xq['status']:
                    if state_ask_xq['msg'] == '已评论过':
                        log.logger.info('已评论过:{}+{}'.format(task['taskAcc'], article_id))

            except:
                traceback.print_exc()
                log.logger.error('评论失败：{}+{}'.format(task['taskAcc'],article_id))
def xq_login(cookie):

    u_id=cookie.split('u=')[1].split(';')[0]
    dict_1={}

    url_xq='https://xueqiu.com/u/{}'.format(u_id)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'xueqiu.com',
        'Referer': 'https://xueqiu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
    }

    # html_1=requests.get(url=url_xq,headers=headers,proxies=proxies).text
    html_1=xh_pd_req(pos_url=url_xq,data='',headers=headers)

    sel_xq=Selector(text=html_1)
    focusNum=sel_xq.xpath('string(//ul[@class="friendship-number"]/li[1])').extract()[0].strip()
    focusNum=int(focusNum.split('关注')[0].strip())
    nickname=sel_xq.xpath('string(//div[@class="profiles__hd__info"]/h2)').extract()[0].strip()
    headUrl=sel_xq.xpath('string(//div[@class="profiles__hd__avatar"]/img/@src)').extract()[0].strip()
    headUrl='https:'+headUrl
    dict_1['focusNum']=focusNum
    dict_1['headUrl']=headUrl
    dict_1['nickname']=nickname

    print(dict_1)
    return dict_1


if __name__ == '__main__':
    pass
    # task={'startDate': '', 'channelType': 3, 'accountId': 'e384f5c6304d4f59b61113ef8e9468a4', 'updateAcc': '', 'imageUrl': 'http://ylhslytest.oss-cn-hangzhou.aliyuncs.com/20190424/9990c11eed3341e0989149e33c6be1b8', 'focusNum': 0, 'endDate': '', 'password': 'qf123456', 'contentId': '409f6d39645b4fdb8bf5265e77bc8717', 'id': 'dceadc8b5d804764b0f870140275465a', 'orgId': 'rdkj', 'todayCount': 0, 'ownerAcc': 'rdkj001', 'groupClass': '1009,1002', 'isDel': 0, 'headUrl': '', 'inputAcc': 'rdkj001', 'text': '哦~', 'limitKey': '', 'updateTime': None, 'nickname': '', 'taskAcc': '13018956681', 'inputTime': {'time': 1556094292000, 'minutes': 24, 'seconds': 52, 'hours': 16, 'month': 3, 'year': 119, 'timezoneOffset': -480, 'day': 3, 'date': 24}, 'isOpen': 0, 'groupKey': '', 'orderKey': '', 'generalizeType': 0}
    # # # print(get_cookie(task))
    # # # cookie=get_cookie(task)
    # #
    # cookie='HMACCOUNT=6CAAFFC5F3AC9144;GeeTestUser=34ddb4dfbd773eded917a054070c6b34;GeeTestAjaxUser=a6cc2f595ef521d14207ee0d2edbdd57;u=4979192105;Hm_lvt_1db88642e346389874251b5a1eded6e3=1557198031,1557198247,1557277802,1557278172;device_id=869f08f715a22f7a85944b305de8b466;s=fe117qixou;aliyungf_tc=AQAAAMt9Jl0keQgAJ2cRcEDBFnj7OKrm;xq_a_token=c23271298213e76e1e889f535fc4df6b225c1418;xq_a_token.sig=E_oWkIRXLzY9jShEop_cL1Cho-4;xq_r_token=2d88c6037c95cc8046a450775f0eb1da90b4eeab;xq_r_token.sig=pWkiZQ7anInrwuRDKG7nXTznEb8;Hm_lpvt_1db88642e346389874251b5a1eded6e3=1557278205;Hm_ck_1557278171820=is-cookie-enabled;Hm_ck_1557278186656=is-cookie-enabled;xqat=c23271298213e76e1e889f535fc4df6b225c1418;xq_is_login=1;Hm_ck_1557278205374=is-cookie-enabled;'
    #
    # # print(Comment('112985826',task,cookie))
    # print(qx_test_cookie(cookie,''))

