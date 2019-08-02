# -*- coding: utf-8 -*- 
# @Author : Zhy

import pythoncom
import requests
from win32api import GetSystemMetrics
import glob
import fitz
import socket
import json
import time
import base64
import traceback
from PIL import Image
import queue
import threading
from urllib import request
import urllib
import os
from win32com import client as wc
import oss2
import shutil

job_save_url = 'http://*********/crawler/resume/uploadSourceUrl'
# job_save_url = 'http://*********/resume/uploadSourceUrl'


"""
服务器端
"""
host_name = socket.gethostname()
print("hostname:%s" % host_name)
print("IP address: %s" % socket.gethostbyname(host_name))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # 生成socket对象
sock.bind(('*********', 8000))  # 绑定主机ip和端口号
# sock.bind(('localhost', 8001))                               # 绑定localhost可以
sock.listen(5000)
data_fi={"state":1}
data = json.dumps(data_fi)
data = data.encode('utf-8')

yourAccessKeyId = '*********'
yourAccessKeySecret = '*********'
yourBucketName = '*********'
auth = oss2.Auth(yourAccessKeyId, yourAccessKeySecret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', yourBucketName)
# 设置存储空间为私有读写权限。
# bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
# 公共读权限
bucket.create_bucket(oss2.OBJECT_ACL_PUBLIC_READ)
oss2.ObjectIterator(bucket, delimiter='/')

#图片转webp
def image2webp(inputFile, outputFile,saveq,get_data_1):
    try:
        try:
            try:
                resume_url = get_data_1['send_to']
                # print(resume_url)
                resume_type = 1
            except:
                resume_type = 0
                # traceback.print_exc()
                pass
            image = Image.open(inputFile)
            if image.mode != 'RGBA' and image.mode != 'RGB':
                image = image.convert('RGBA')
            ori_w, ori_h = image.size
            print(int(ori_w*saveq),int(ori_h*saveq))
            newimage=image.resize((int(ori_w*saveq),int(ori_h*saveq)))
            newimage.save(outputFile, 'WEBP')
            print(inputFile + ' has converted to ' + outputFile)
        except Exception as e:
            traceback.print_exc()
            print('Error: ' + inputFile + ' converte failed to ' + outputFile)
        with open(outputFile, 'rb') as f1:
            shotname = outputFile.split(os.sep)[-1]
            # file_oss = 'channel_resume/' + '123' + '/' + str(shotname)
            # print(file_oss)
            resp_save = bucket.put_object(shotname, f1)
            spec_oss_url = resp_save.resp.response.url
            print(spec_oss_url)
        if resume_type == 0:
            get_data_1['fileUrl']=spec_oss_url
            print(get_data_1)
            data = json.dumps(get_data_1)
            data = data.encode('utf-8')
            requests.post(url=job_save_url, data=data)
        elif resume_type == 1:
            get_data_1['resume']['info']['source_url'] = spec_oss_url
            list_1 = []
            list_1.append(get_data_1['resume'])
            print('保存简历',list_1)
            data = json.dumps(list_1)
            data = data.encode('utf-8')
            a=requests.post(url=resume_url, data=data)
            print(a.text)

        shutil.rmtree(str(now_time))
    except:
        traceback.print_exc()
        shutil.rmtree(str(now_time))
        print('解析错误')
#word转pdf
def word2pdf(source_path, target_path):
    try:
        pythoncom.CoInitialize()
        word = wc.DispatchEx('Word.Application')
    except:
        pythoncom.CoInitialize()
        word = wc.DispatchEx('kwps.Application')
    try:
        word.Documents.Close()
        word.Documents.Close(word.wdDoNotSaveChanges)
        word.Quit()
    except:
        pass
    word.Visible = 0
    word.DisplayAlerts = 0
    doc = word.Documents.Open(source_path)
    doc.SaveAs(target_path, 17, False, "", True, "", False, False, False, False)
    doc.Close()
    word.Quit()
#pdf转图片
def pdf2img(source_path, target_path):
    pdffile = glob.glob(source_path)[0]
    doc = fitz.open(pdffile)
    totaling = doc.pageCount
    for pg in range(totaling):
        page = doc[pg]
        zoom = int(100)
        rotate = int(0)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(os.path.join(target_path, '%s.jpg' % str(pg + 1)))
    return totaling
def pdftowebp(inputFile, outputFile,get_data_1):
    pdf2img(inputFile, outputFile)
    imagefile = []
    new_height = 0
    new_width = 0
    page_height = 0
    for root, dirs, files in os.walk(outputFile):
        for f in files:
            temp_1_name, temp_1_ext = os.path.splitext(f)
            if temp_1_ext in ['.jpg', '.png', '.jpeg']:
                print('处理', f)
                img_temp_1 = Image.open(outputFile + '/' + f)
                new_height = new_height + img_temp_1.size[1]
                new_width = img_temp_1.size[0]
                page_height = img_temp_1.size[1]
                imagefile.append(img_temp_1)
    target = Image.new('RGB', (new_width, new_height))  # 最终拼接的图像的大小为(229*3) * (229*6)
    left = 0
    right = page_height
    for image in imagefile:
        target.paste(image, (0, left, new_width, right))
        left += page_height  # 从上往下拼接，左上角的纵坐标递增
        right += page_height  # 左下角的纵坐标也递增　
        quality_value = 100
        target.save(outputFile + '/result.jpg', quality=quality_value)
    webp_from = outputFile + '/result.jpg'
    webp_to = outputFile + '/result.webp'
    image2webp(webp_from, webp_to, 1,get_data_1)
def wordtowebp(inputFile, outputFile,get_data_1):
    
    word2pdf(inputFile, outputFile)
    outfile = str(now_time)
    pdftowebp(outputFile, outfile,get_data_1)

while True:
    time.sleep(1)
    connection, addr = sock.accept()  # 接受客户端的连接
    try:
        connection.settimeout(2000)
        get_1 = connection.recv(2048000)
        print(111, get_1)
        try:
            get_1 = base64.b64decode(get_1)
            print(222, get_1)
        except:
            traceback.print_exc()
            pass
        try:
            get_1 = get_1.decode('utf-8', errors='ignore')
            print(333, get_1)
        except:
            traceback.print_exc()
            pass
        try:
            get_data = json.loads(get_1)
            print(444, get_data)
        except:
            traceback.print_exc()
            pass

        # print('23333',get_1)
        # try:
        #     get_1 = base64.b64decode(get_1)
        #     print('222',get_1)
        #     get_1 = get_1.decode('utf-8', errors='ignore')
        #     get_data = json.loads(get_1)
        #     now_time=int(time.time())
        #     os.mkdir(str(now_time))
        #     print(111, get_data)
        #     url_1=get_data['fileUrl']
        # except:
        #     traceback.print_exc()
        #     pass
        url_1 = get_data['fileUrl']

        now_time = int(time.time())
        connection.send(data)  # 向客户端发送一个字符串信息
        connection.close()
        os.mkdir(str(now_time))
        inputfile=str(now_time)+'/'+str(now_time)+'.'+url_1.split('.')[-1]
        outfile=str(now_time)+'/'+str(now_time)+'.webp'
        with urllib.request.urlopen(url_1, timeout=30) as response, open(inputfile, 'wb') as f_save:
            f_save.write(response.read())
            f_save.flush()
            f_save.close()
        myqueue = queue.Queue()
        myqueue.put(inputfile)
        # while not myqueue.empty():
        if threading.activeCount() < 3:
            input_file=myqueue.get()
            if '.pdf' in input_file:
                outfile=str(now_time)
                th_1 = threading.Thread(target=pdftowebp, args=(input_file,outfile,get_data))
                th_1.start()
            elif '.doc' in input_file or  '.docx' in input_file:
                path_1=os.getcwd()
                th_1 = threading.Thread(target=wordtowebp, args=(path_1+'\\' + str(now_time)+'\\'+str(now_time)+'.'+input_file.split('.')[-1], path_1+'\\'+str(now_time)+'\\'+str(now_time)+'.pdf',get_data))
                th_1.start()
            else:
                th_2 = threading.Thread(target=image2webp, args=(input_file,outfile, 1,get_data))
                th_2.start()
            print(threading.activeCount())

    except:
        traceback.print_exc()

