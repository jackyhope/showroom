# -*- coding: utf-8 -*- 
# @Author : Zhy

'''获取所有类目，保存在meta.json文件中'''

import json
import requests
import time
import random

def PROXIES():
    # 代理隧道验证信息

    from urllib import request
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # proxyUser = "H889BT3GSSBG3U6D"         #ok
    # proxyPass = "C4E4EA69296C97B8"
    #
    proxyUser = "H8X8141CM4JDB0VD"
    proxyPass = "14CE3A81B9E49EB5"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxy_handler = request.ProxyHandler({
        "http": proxyMeta,
        "https": proxyMeta,
    })
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    opener = request.build_opener(proxy_handler)
    request.install_opener(opener)

    return proxies
def XH_REQ(url,data,headers,):
    num=0
    flag = True
    while flag:
        try:
            if num<3:

                if data == '':
                    job_xq_text = requests.get(url=url,headers=headers,timeout=4,proxies=proxies)
                else:
                    job_xq_text = requests.get(url=url,params=data,headers=headers,timeout=4,proxies=proxies)

                if job_xq_text.status_code  == 200:

                    return job_xq_text.text
                else:
                    num = num + 1
                    time.sleep(random.uniform(1,1.5))
                    continue
            else:
                flag = False
        except:
            time.sleep(random.uniform(1, 1.5))
            pass
def XH_REQ_1(url,data,headers,):
    num=0
    flag = True
    while flag:
        try:
            if num<3:

                if data == '':
                    job_xq_text = requests.get(url=url,headers=headers,timeout=4,)
                else:
                    job_xq_text = requests.get(url=url,params=data,headers=headers,timeout=4,)

                if job_xq_text.status_code  == 200:

                    return job_xq_text.text
                else:
                    num = num + 1
                    time.sleep(random.uniform(3,5))
                    continue
            else:
                flag = False
        except:
            time.sleep(random.uniform(3, 5))
            pass
def get_dict(file):
    with open(file, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict
LIST_COOKIE=[
'UM_distinctid=16bde7f0d27464-07681ef0f58d2f-404b032d-100200-16bde7f0d283bd; ali_ab=112.17.103.39.1562805999058.2; lid=tb982084477; cna=5h+rFcL01ycCAXARZydz2tPK; h_keys="%u5973%u88c5#sa#%u62b9%u80f8"; ali_beacon_id=112.17.103.39.1562809422469.797925.0; hng=CN%7Czh-CN%7CCNY%7C156; ali_apache_track=c_mid=b2b-3870117476bc050|c_lid=tb982084477|c_ms=1; cookie2=1837abbe695d59b5bfab16f7903e4a08; t=83a25c1d6a3a6b30bd76f8e945e193d9; _tb_token_=3463636eeeba; __cn_logon__=true; __cn_logon_id__=tb982084477; ali_apache_tracktmp=c_w_signed=Y; last_mid=b2b-3870117476bc050; alicnweb=homeIdttS%3D95741725498328762873660274152480767830%7ChomeIdttSAction%3Dtrue%7Ctouch_tb_at%3D1565688608725%7Chp_newbuyerguide%3Dtrue%7Clastlogonid%3Dtb982084477; cookie1=VFR0QZj%2BGpICLiKOgsNJU5EbsITHRPYOeM%2BjLhWOxus%3D; cookie17=UNiDQ9MBYYQC5A%3D%3D; sg=761; csg=d8b69116; unb=3870117476; uc4=nk4=0%40FY4HVFvfBFVJMLGaQOkqffB3xPPBmw%3D%3D&id4=0%40Ug%2Bcisa1oGrqxsBCuqzsiFNOqa79; _nk_=tb982084477; _csrf_token=1565689980290; _is_show_loginId_change_block_=b2b-3870117476bc050_false; _show_force_unbind_div_=b2b-3870117476bc050_false; _show_sys_unbind_div_=b2b-3870117476bc050_false; _show_user_unbind_div_=b2b-3870117476bc050_false; __rn_alert__=false; ad_prefer="2019/08/13 17:53:16"; isg=BM7Ole5lH2tcDqs5GWuKNK-xH6RQ55PHkt76NvgXIFGHW261YNynWcgJkceS2Iph; l=cBrirwBnqxrGM-19BOCanurza77OSIRYYuPzaNbMi_5pK6T_x47Ok-JZiF96VjWd9_YB45fyK2p9-etkZv7viWdNIfiC.',
]

proxies = PROXIES()



if __name__ == '__main__':
    DICT_CITY = get_dict(r'spiders\table\aliCity.json')
    DICT_SEARCH = get_dict(r'spiders\table\aliSearch.json')

    # list_re=['北京','上海','天津','重庆','海外']

    # list_city=[]
    #
    # for name,value in DICT_CITY.items():
    #     if name in list_re:
    #         list_city.append({'city': '', 'province': name+','+value['id']})
    #     else:
    #         for dict_children in value['children']:
    #             dict_1 = {}
    #             dict_1['province'] = name+','+value['id']
    #             dict_1['city']=dict_children['name']+','+dict_children['id']
    #             list_city.append(dict_1)
    #     print(list_city)
    #
    # print(len(list_city))
    #
    # f = open(r"spiders\table\listCity.json", "w")
    # json.dump(list_city, f, ensure_ascii=False)
    # f.close()

    # list_city = get_dict(r'spiders\table\listCity.json')
    #
    # list_meta=[]
    #
    # for dict_city in list_city:
    #
    #     for FirstCate,value in DICT_SEARCH.items():
    #
    #         for dict_cate in value['children']:
    #             SecondCate=dict_cate['name']
    #             for dict_3 in dict_cate['children']:
    #                 meta={}
    #                 meta['province']=dict_city['province']
    #                 meta['city']=dict_city['city']
    #                 meta['FirstCate'] = FirstCate
    #                 meta['SecondCate']=SecondCate
    #                 meta['ThirdCate']=dict_3['name']
    #                 print(meta)
    #                 list_meta.append(meta)
    #
    # print(len(list_meta))
    # f = open(r"spiders\table\meta.json", "w")
    # json.dump(list_meta, f, ensure_ascii=False)
    # f.close()





