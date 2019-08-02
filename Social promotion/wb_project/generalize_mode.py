import re
import time
import json
import hashlib
import random
import redis
from lxml import etree
import requests
from urllib.parse import quote
from requests.cookies import RequestsCookieJar
from wb_project.request import Request
from wb_project.tools import Log, PostData
from reset_num import update_crawelNum, select_crawelNum
from setting import *

log = Log('crawler')


class RedisClient:
    redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, max_connections=100, retry_on_timeout=True, decode_responses=True)

    @classmethod
    def quit_judge(cls, taskId):
        redis_conn = redis.Redis(connection_pool=cls.redis_pool)
        state = redis_conn.hmget('thread:pid', taskId)[0]
        if state and int(state) == 0:
            return True

class Generalize:
    factor = ['那些光线。', '那些日出。', '那些晨雾。', '一样都会准时而来。', '无限漫长时光里的温柔。', '无限温柔里的漫长时光。', '一直都在。', '疼痛。', '是疼还是痛。', '有区别吗。',
              '心疼和心痛。', '有区别吗。', '不安全。', '不安分。', '不安稳。', '不安静。', '不安宁。', '不安心。', '那些光线。',
              '那些日出。', '那些晨雾。', '一样都会准时而来。', '无限漫长时光里的温柔。', '无限温柔里的漫长时光。', '一直都在。',
              '疼痛。', '是疼还是痛。', '有区别吗。', '心疼和心痛。', '有区别吗。', '不安全。', '不安分。', '不安稳。', '不安静。', '不安宁。', '不安心。']

    def __init__(self, cookies: RequestsCookieJar, uid: str, orgId, ownerAcc, taskAcc, taskId, content, task):
        self.req = Request(cookies, log)
        self.uid = uid
        self.orgId = orgId
        self.ownerAcc = ownerAcc
        self.taskAcc = taskAcc
        self.taskId = taskId
        self.content = content
        self.task = task

    def run(self, *args, **kwargs):
        pass

    def account_except(self):
        data = {
            'id': self.task['accountId'],
            'orgId': self.orgId,
            'status': 1,
            'errorDescription': '登录状态失效'
        }
        PostData.channel_info(data)
        log.logger.warning('登录状态失效: {}'.format(self.taskAcc))

        data_1 = json.dumps({'accinfo': self.task, 'act': 'cookie_notuse'}, ensure_ascii=False).encode('utf-8')
        requests.post(url=URL_LOGIN, data=data_1)

    def comment(self, mid, location, page_id, referer):
        """评论"""
        time.sleep(random.randint(30, 60))
        string = str(self.taskAcc) + '+' + str(mid)
        try:
            try:
                if random.choice(list(range(1, 9))) == 1:
                    url = 'https://weibo.com/aj/fav/mblog/add?ajwvr=6'
                    data = {
                        'mid': mid,
                        'location': 'v6_content_home',
                        'group_source': 'group_all',
                    }
                    headers = {
                        'Host': 'weibo.com',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Referer': referer,
                    }
                    self.req.post(url=url, headers=headers, data=data)
                    time.sleep(random.randint(3, 5))

                if random.choice(list(range(1, 9))) == 2:
                    url = 'https://weibo.com/aj/v6/like/add?ajwvr=6'
                    data = {
                        'location': 'v6_content_home',
                        'group_source': 'group_all',
                        'version': 'mini',
                        'qid': 'heart',
                        'mid': mid,
                        'like_src': '1',
                        'cuslike': '1',
                        'hide_multi_attitude': '1',
                        'liked': '0',
                        'floating': '0',
                        '_t': '0',
                    }
                    headers = {
                        'Host': 'weibo.com',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Referer': referer,
                    }
                    self.req.post(url=url, headers=headers, data=data)
                    time.sleep(random.randint(3, 5))
            except:
                pass

            md = hashlib.md5()
            md.update(string.encode('utf-8'))
            digest = md.hexdigest()

            ask_data = {
                'orgId': self.orgId,
                'ownerAcc': self.ownerAcc,
                'taskAcc': self.taskAcc,
                'digest': digest,
            }
            if PostData.ask(ask_data):
                url = 'https://weibo.com/aj/v6/comment/add?ajwvr=6'
                data = {
                    'act': 'post',
                    'mid': mid,  # 4350109595195955，某条动态的id
                    'uid': self.uid,  # 5685522058，当前登录用户的id
                    'forward': '0',
                    'isroot': '0',
                    'content': self.content + ' ' + random.choice(self.factor),
                    'location': location,  # page_100505_home
                    'module': 'scommlist',
                    'group_source': '',
                    'tranandcomm': '1',
                    'pdetail': page_id,  # 1005055331040243，博主的id
                    '_t': '0',
                }
                headers = {
                    'Host': 'weibo.com',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': referer,
                }
                response = self.req.post(url=url, headers=headers, data=data)
                result = json.loads(response.text)
                if result['code'] == '100000':
                    submit_data = {
                        'orgId': self.orgId,
                        'ownerAcc': self.ownerAcc,
                        'taskAcc': self.taskAcc,
                        'digest': digest,
                        'taskId': self.taskId,
                    }
                    PostData.submit(submit_data)
                    log.logger.info('评论完成：{}'.format(string))
                    return True
                else:
                    log.logger.info('评论失败：{}|{}'.format(string, str(result)))
            else:
                log.logger.info('评论过了：{}'.format(string))
        except:
            log.logger.exception('评论异常：{}'.format(string))

class RecommendedContentGeneralize(Generalize):
    def run(self, numbers):
        current_num = select_crawelNum(self.taskAcc, 2)
        total_count = 0
        for number in numbers:
            if number == '0':
                try:
                    category_id = self.special_category()
                except:
                    log.logger.exception('获取定位分类失败: {}'.format(self.taskAcc))
                    continue
            else:
                category_id = '102803_ctg1_{number}_-_ctg1_{number}'.format(number=number)

            log.logger.info('开始爬取热门分类（{}）下的微博：{}'.format(category_id, self.taskAcc))

            location = 'page_' + category_id + '_home'
            url = 'https://d.weibo.com/{category_id}?from=faxian_hot&mod=fenlei'.format(category_id=category_id)

            count = 0
            for mid in self.hot_details(category_id):
                try:
                    if RedisClient.quit_judge(self.taskId):
                        log.logger.info('线程退出：{}'.format(self.taskId))
                        return
                    result = self.comment(mid, location, category_id, url)
                    if result:
                        count += 1
                        if update_crawelNum(self.taskAcc, 2) >= 200:
                            return
                        if count > (200 - current_num) // len(numbers):
                            break
                    total_count += 1
                    if total_count > random.randint(20, 25):
                        total_count = 0
                        log.logger.info('暂停：{}'.format(self.taskAcc))
                        time.sleep(random.randint(8000, 10000))
                except:
                    log.logger.exception("Exception Logged")

    def special_category(self):
        """获取定位分类的id"""
        time.sleep(random.randint(1, 3))
        url = 'https://d.weibo.com/'
        headers = {
            'Host': 'd.weibo.com',
            'Referer': 'https://weibo.com/u/{}/home?topnav=1&wvr=6'.format(self.uid),
        }
        response = self.req.get(url=url, headers=headers)
        match = re.search(r'<script>FM\.view\(({.*?"domid":"Pl_Discover_TextList__4".*})\)</script>', response.text).group(1)
        html = json.loads(match)['html']
        element = etree.HTML(html)
        href = element.xpath('//ul[@class="ul_text clearfix"]/li[1]/a[1]/@href')[0]
        return quote(re.match(r'/(.*?oid.*?)\?', href).group(1))

    def hot_details(self, category_id):
        """获取当前分类下的每一页每一条动态的mid"""
        url = 'https://d.weibo.com/p/aj/v6/mblog/mbloglist'
        page = -1
        while page < 19:
            time.sleep(random.randint(1, 3))
            try:
                params = {
                    'ajwvr': '6',
                    'domain': category_id,
                    'from': 'faxian_hot',
                    'mod': 'fenlei',
                    'tab': 'home',
                    'pagebar': str(page),
                    'pre_page': '1',
                    'pl_name': 'Pl_Core_NewMixFeed__3',
                    'id': category_id,
                    'feed_type': '1',
                    'domain_op': category_id,
                }
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'd.weibo.com',
                    'Referer': 'https://d.weibo.com/{}?from=faxian_hot&mod=fenlei'.format(category_id),
                    'X-Requested-With': 'XMLHttpRequest',
                }
                response = self.req.get(url=url, headers=headers, params=params)
                html = json.loads(response.text)['data']
                element = etree.HTML(html)
                mid_list = element.xpath('//div/@mid')
                if mid_list:
                    for mid in mid_list:
                        yield mid
                else:
                    raise Exception
            except GeneratorExit:
                pass
            except:
                log.logger.exception('热门分类页面访问失败：{}'.format({'page': page, 'category_id': category_id, 'username': self.taskAcc}))
                self.account_except()
                break
            page += 1

class RecommendedBloggerGeneralize(Generalize):
    def run(self, numbers):
        current_num = select_crawelNum(self.taskAcc, 2)
        total_count = 0
        for number in numbers:
            category_id = '1087030002_' + number
            log.logger.info('开始爬取博主分类（{}）下的微博：{}'.format(category_id, self.taskAcc))

            count = 0
            for blogger_url, referer in self.get_blogger(category_id):
                try:
                    if RedisClient.quit_judge(self.taskId):
                        log.logger.info('线程退出：{}'.format(self.taskId))
                        return

                    log.logger.info('爬取博主（{}）'.format(blogger_url))
                    try:
                        mid, location, page_id = self.blogger_details(blogger_url, referer)
                    except:
                        log.logger.exception('博主主页访问失败：{}'.format(blogger_url))
                        continue
                    result = self.comment(mid, location, page_id, blogger_url)
                    if result:
                        count += 1
                        if update_crawelNum(self.taskAcc, 2) >= 200:
                            return
                        if count > (200 - current_num) // len(numbers):
                            break
                    total_count += 1
                    if total_count > random.randint(20, 25):
                        total_count = 0
                        log.logger.info('暂停：{}'.format(self.taskAcc))
                        time.sleep(random.randint(8000, 10000))
                except:
                    log.logger.exception("Exception Logged")

    def get_blogger(self, category_id):
        """获取当前分类下的博主的主页链接"""
        page = 1
        while page <= 20:
            time.sleep(random.randint(1, 3))
            try:
                url = 'https://d.weibo.com/{}'.format(category_id)
                params = {
                    'pids': 'Pl_Core_F4RightUserList__4',
                    'page': page,
                    'ajaxpagelet': '1',
                    '__ref': '/{}'.format(category_id)
                }
                headers = {
                    'Host': 'd.weibo.com',
                    'Referer': 'https://d.weibo.com/{}?pids=Pl_Core_F4RightUserList__4&page={}'.format(category_id, page),
                }
                response = self.req.get(url=url, headers=headers, params=params)
                match = re.search(r'parent\.FM\.view\((.*)\)', response.text).group(1)
                html = json.loads(match)['html']
                element = etree.HTML(html)
                a_tags = element.xpath('//ul[@class="follow_list"]/li/dl[1]/dt[1]/a[1]')
                if a_tags:
                    for cell in a_tags:
                        href = 'https:' + cell.xpath('./@href')[0]
                        referer = 'https://d.weibo.com/{}?page={}'.format(category_id, page)
                        yield href, referer
                else:
                    break
            except GeneratorExit:
                pass
            except:
                log.logger.exception('博主分类页面访问失败：{}'.format({'page': page, 'category_id': category_id, 'username': self.taskAcc}))
                self.account_except()
                break
            page += 1

    def blogger_details(self, url, referer):
        """获取当前博主的最新一条动态的mid"""
        time.sleep(random.randint(1, 3))
        headers = {
            'Host': 'weibo.com',
            'Referer': referer,
        }
        response = self.req.get(url=url, headers=headers)
        oid = re.search("\$CONFIG\['oid'\]='(.*?)';", response.text).group(1)
        page_id = re.search("\$CONFIG\['page_id'\]='(.*?)';", response.text).group(1)
        location = re.search("\$CONFIG\['location'\]='(.*?)';", response.text).group(1)
        match = re.search(r'<script>FM\.view\(({.*?"domid":"Pl_Official_MyProfileFeed.*})\)</script>', response.text).group(1)
        html = json.loads(match)['html']
        element = etree.HTML(html)
        mid = element.xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[contains(@tbinfo, "ouid={ouid}") and not(@feedtype="top")]/@mid'.format(ouid=oid))[0]
        return mid, location, page_id

class FollowersGeneralize(Generalize):
    def run(self):
        log.logger.info('开始爬取关注博主的微博：{}'.format(self.taskAcc))
        total_count = 0
        for blogger_url, referer in self.get_followers():
            try:
                if RedisClient.quit_judge(self.taskId):
                    log.logger.info('线程退出：{}'.format(self.taskId))
                    return
                log.logger.info('爬取关注博主（{}）'.format(blogger_url))
                try:
                    mid, location, page_id = self.follower_details(blogger_url, referer)
                except:
                    log.logger.exception('关注博主主页访问失败：{}'.format(blogger_url))
                    continue
                result = self.comment(mid, location, page_id, blogger_url)
                if result:
                    if update_crawelNum(self.taskAcc, 2) >= 200:
                        return
                total_count += 1
                if total_count > random.randint(20, 25):
                    total_count = 0
                    log.logger.info('暂停：{}'.format(self.taskAcc))
                    time.sleep(random.randint(8000, 10000))
            except:
                log.logger.exception("Exception Logged")

    def get_followers(self):
        """获取各个关注的博主的主页链接"""
        page = 1
        while page < 50:
            time.sleep(random.randint(1, 3))
            try:
                url = 'https://weibo.com/p/100505{}/myfollow'.format(self.uid)
                params = {
                    't': '1',
                    'pids': 'Pl_Official_RelationMyfollow__95',
                    'cfs': '',
                    'Pl_Official_RelationMyfollow__95_page': page,
                    'ajaxpagelet': '1',
                    'ajaxpagelet_v6': '1',
                    '__ref': '/p/100505{}/home?from=page_100505&mod=TAB#place'.format(self.uid)
                }
                headers = {
                    'Host': 'weibo.com',
                    'Referer': 'https://weibo.com/p/100505{}/home?from=page_100505&mod=TAB'.format(self.uid),
                }
                response = self.req.get(url=url, headers=headers, params=params)
                match = re.search(r'parent\.FM\.view\((.*)\)', response.text).group(1)
                html = json.loads(match)['html']
                element = etree.HTML(html)
                a_tags = element.xpath('//ul[@class="member_ul clearfix"]/li/div[1]/div[@class="mod_info"]/div[1]/a[1]')
                if a_tags:
                    for cell in a_tags:
                        href = 'https://weibo.com' + cell.xpath('./@href')[0]
                        referer = 'https://weibo.com/p/100505{}/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__95_page={}'.format(self.uid, page)
                        yield href, referer
                else:
                    break
            except GeneratorExit:
                pass
            except:
                log.logger.exception('关注列表页面访问失败：{}'.format({'page': page, 'username': self.taskAcc}))
                self.account_except()
                break
            page += 1

    def follower_details(self, url, referer):
        """获取当前博主的最新一条动态的mid"""
        time.sleep(random.randint(1, 3))
        headers = {
            'Host': 'weibo.com',
            'Referer': referer,
        }
        response = self.req.get(url=url, headers=headers)
        oid = re.search("\$CONFIG\['oid'\]='(.*?)';", response.text).group(1)
        page_id = re.search("\$CONFIG\['page_id'\]='(.*?)';", response.text).group(1)
        location = re.search("\$CONFIG\['location'\]='(.*?)';", response.text).group(1)
        match = re.search(r'<script>FM\.view\(({.*?"domid":"Pl_Official_MyProfileFeed.*})\)</script>', response.text).group(1)
        html = json.loads(match)['html']
        element = etree.HTML(html)
        mid = element.xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[contains(@tbinfo, "ouid={ouid}") and not(@feedtype="top")]/@mid'.format(ouid=oid))[0]
        return mid, location, page_id
