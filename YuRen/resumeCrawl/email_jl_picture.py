# -*- coding: utf-8 -*-


import os
import imgkit
import shutil
import uuid
import time
import random
from PIL import Image
import traceback
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

wkhtmltoimage = os.getcwd() + os.sep + 'wkhtmltoimage.exe'
exe_path = os.getcwd() + os.sep + 'phantomjs.exe'
import oss2
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。
# 强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
yourAccessKeyId = '*******'
yourAccessKeySecret = '*******'
yourBucketName = 'rsmfiletest'
auth = oss2.Auth(yourAccessKeyId, yourAccessKeySecret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', yourBucketName)
# 设置存储空间为私有读写权限。
# bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
# 公共读权限
bucket.create_bucket(oss2.OBJECT_ACL_PUBLIC_READ)
oss2.ObjectIterator(bucket, delimiter='/')
def email_jl_picture(from_path, to_path, exe_path=wkhtmltoimage,from_url=''):
    config = imgkit.config(wkhtmltoimage=exe_path)
    options_file = {
        # 'format': 'png',
        # 'encoding': "UTF-8",
        # 'cookie': cookies_str,
        # 'cookie-jar': ck_jar,
        # 'custom-header': [('User-Agent',user_agent),('Cookie',cookies_str)],
        'quality': 50,
        'width': 600,
        # 'height': 1024,
        # 'disable-javascript': True,
        # 'javascript-delay': 5000
    }
    options_url = {
        # 'format': 'png',
        # 'encoding': "UTF-8",
        # 'cookie': cookies_str,
        # 'cookie-jar': ck_jar,
        # 'custom-header': [('User-Agent',user_agent),('Cookie',cookies_str)],
        'quality': 100,
        # 'width': 600,
        'height': 1024,
        # 'disable-javascript': True,
        # 'javascript-delay': 5000
    }
    if from_url:
        try:
            imgkit.from_url(url=from_url, output_path=to_path, options=options_url, config=config)
        except:
            pass
    else:
        try:
            imgkit.from_file(filename=from_path, output_path=to_path, options=options_file, config=config)
        except:
            pass
def crop_ele_pic(driver_exe_path, ele_path, out_path, url, headers=''):
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            # 'Cookie': cookies_str,
            # 'Referer': 'https://rd5.zhaopin.com/resume/download',
            # 'Referer': 'https://easy.lagou.com/can/index.htm',
            # 'Host': 'rd5.zhaopin.com'
        }
    cap = DesiredCapabilities.PHANTOMJS.copy()  # 使用copy()防止修改原代码定义dict
    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS(desired_capabilities=cap, executable_path=driver_exe_path)
    driver.get(url)
    time.sleep(2)
    base_salary = driver.find_element_by_xpath(ele_path)
    location = base_salary.location
    size = base_salary.size
    # print(location)
    # print(size)
    driver.get_screenshot_as_file(out_path)
    # print(driver.page_source)
    rangle = (int(location['x']+10), int(location['y']+10), int(location['x'] + size['width']-10), int(location['y'] + size['height']-15))
    img = Image.open(out_path)
    fina_img = img.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    fina_img.save(out_path)
def save_to_oss(html_str,org_id, from_url='', ele_path=''):
    dirname = str(uuid.uuid1())
    file_path = os.getcwd() + os.sep + dirname
    # print(file_path)
    if not os.path.exists(file_path):
        # print('文件夹', file_path, '不存在，重新建立')
        # os.mkdir(file_path)
        os.makedirs(file_path)
    else:
        shutil.rmtree(file_path)
        os.makedirs(file_path)
    from_path = file_path + os.sep +'temp.html'
    to_path = file_path + os.sep + 'temp.png'
    if from_url:
        crop_ele_pic(exe_path, ele_path, to_path, from_url)
    else:
        with open(from_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
            f.write(html_str)
        email_jl_picture(from_path, to_path)
    with open(to_path, 'rb') as f1:
        shotname = str(int(time.time() * 1000)) + '_' + to_path.split(os.sep)[-1]
        filename = 'channel_resume/' + org_id + '/' + str(shotname)
        resp_save = bucket.put_object(filename, f1)
        save_url = resp_save.resp.response.url
    try:
        shutil.rmtree(file_path)
    except:
        pass
        # traceback.print_exc()
    return save_url




