# -*- coding: utf-8 -*- 
# @Author : Zhy

'''获取所有类目，保存在meta.json文件中'''

import json
import requests
import time
import random


def XH_REQ(url,data,headers):
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
                    time.sleep(random.uniform(1,1.5))
                    continue
            else:
                flag = False
        except:
            pass
def get_dict(file):
    with open(file, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict

LIST_COOKIE=[
    'miid=1121841226593907354; t=3ed5547c5b7b8fe91c8047c36160054b; thw=cn; cna=Bc20FE+2kWsCAXARZyfv+agB; hng=CN%7Czh-CN%7CCNY%7C156; birthday_displayed=1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _uab_collina=156074362538868539402582; cookie2=1d7a77a862a5728e497832b34b86abb4; _tb_token_=eb1e135be57fa; _cc_=W5iHLLyFfA%3D%3D; tg=5; enc=gREZkEd4fLIp%2BMvg8FOMu%2B4RKGc3aQQfjJlrvI7rZ6xlRRplMjsSm3KeEoDJucvqF61xr7MLP9Q6Y07yZU0gtQ%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; whl=-1%260%260%261561426894411; swfstore=213616; mt=ci=0_0; v=0; uc1=cookie14=UoTaGdntv6UN%2BA%3D%3D; JSESSIONID=B2D7D1D61FA0970B8D11CF1C1BEA4EBC; isg=BKengBfdtq8QTTI0io3NpSqKNtuxhHqYbV4t_XkUSjZdaMQqif74XqgqiijTgFOG; l=bBQBJ0HRqjA0lDyLBOfaZuI8LU_TiIRbzsPzw4OgFICPO7fk5XVPWZHXwELDC3GVZ1WeP3R5I36YBXLOjyIV.',
    'miid=1121841226593907354; t=3ed5547c5b7b8fe91c8047c36160054b; thw=cn; cna=Bc20FE+2kWsCAXARZyfv+agB; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; tg=0; _cc_=UIHiLt3xSw%3D%3D; enc=LgsmO9hdXJ1tDqa1yn66nDdJILF6MW%2FdmgdeIsktL2vr%2FuOOpEm98lgPPLfkGYilX2AO8OQDmbSH84pgl14sHA%3D%3D; cookie2=19fff2ce319e10fdc7ae2fb13e91a358; _tb_token_=f55104b6a534f; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zZPEr%2FCrvCMS%2BG3sTRRWrQ%2BVVTl09ME1KrXEpvrFZEmTiBjfMoJaU7sfxNSkdCPwLDmiVgnylOzpvhZXezVdvCcJ0hVZjyTO4CADFatt5Y675Vc6bMsMQSP%2FKZ%2BSEH%2BIODva8rHw5%2FQnGPj%2F5iMMFl%2B7R4VPtPZl%2FR3Lh8dpSuTt3bmG78UePZvT3e3s9SW6wvWab%2B0Gwm6HpNnOka9hFIagyS94ezBIawBmWMX1YGMy5EUMimEhpalCU1Vmt6Tk%2BhuKUaTfP4iIVdCTpbFwgES2Lu1eioRjFoFgUDxUb2xtzM%2BZ6DEjyy2nfqv4Ae%2Fw%3D%3D; _m_h5_tk=03b4f973feaad27eb80509dade60482f_1561608138688; _m_h5_tk_enc=741d053c0541c76120a29f22b8422333; swfstore=118256; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=90F218C6F52D8F4B5877B4CB84B94F60; mt=ci=0_0; v=0; l=bBP-APxgqT83bF5DBOfwNuI8LU_OqIRf1sPzw4OgFICPOK195jTdWZH-WTTpC3GVZ1qX83R5I36YB-TGOyCV.; isg=BCQkn_rCJYOWyVHIzsyo6vYU9SLWFUmxsr8OFD5FT--y6cezZc42tzELrUFxMYB_',
    'miid=1121841226593907354; t=3ed5547c5b7b8fe91c8047c36160054b; thw=cn; cna=Bc20FE+2kWsCAXARZyfv+agB; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; tg=0; enc=LgsmO9hdXJ1tDqa1yn66nDdJILF6MW%2FdmgdeIsktL2vr%2FuOOpEm98lgPPLfkGYilX2AO8OQDmbSH84pgl14sHA%3D%3D; _m_h5_tk=e5e9f599c598da4234027c845d3878a3_1561624107128; _m_h5_tk_enc=bb4d2139cca9460834cc9d2b1b34e891; _cc_=WqG3DMC9EA%3D%3D; cookie2=12703d520a32122268ca802bf9b8b14f; _tb_token_=ea5877e5e7377; mt=ci=0_0; v=0; isg=BMrKrTg_oxDBRy-6pIpuOEy6G7CsE0-D-GEQxlQCXJ2oB2nBOkueJRAhE3Pb98at; l=bBP-APxgqT83b5wvBOfaquI8LU_9rIRbzsPzw4OgFICPOefM51oFWZH52uTHC3GVw1feS3R5I36YBeYBqtf..'
    ]





if __name__ == '__main__':
    DICT_CITY = get_dict(r'spiders\table\tbCity.json')
    DICT_SEARCH = get_dict(r'spiders\table\tbSearch.json')

    list_city=[{'province': '广东', 'city': '深圳'}, {'province': '广东', 'city': '广州'}, {'province': '广东', 'city': '中山'}, {'province': '广东', 'city': '佛山'}, {'province': '广东', 'city': '东莞'}, {'province': '广东', 'city': '全部'}, {'province': '湖南', 'city': '长沙'}, {'province': '湖南', 'city': '全部'}, {'province': '内蒙古', 'city': '全部'}, {'province': '北京', 'city': '北京'}, {'province': '海南', 'city': '全部'}, {'province': '重庆', 'city': '重庆'}, {'province': '吉林', 'city': '长春'}, {'province': '吉林', 'city': '全部'}, {'province': '安徽', 'city': '合肥'}, {'province': '安徽', 'city': '全部'}, {'province': '江苏', 'city': '无锡'}, {'province': '江苏', 'city': '苏州'}, {'province': '江苏', 'city': '南京'}, {'province': '江苏', 'city': '全部'}, {'province': '台湾', 'city': '全部'}, {'province': '广西', 'city': '全部'}, {'province': '黑龙江', 'city': '哈尔滨'}, {'province': '黑龙江', 'city': '全部'}, {'province': '山东', 'city': '青岛'}, {'province': '山东', 'city': '济南'}, {'province': '山东', 'city': '全部'}, {'province': '上海', 'city': '上海'}, {'province': '西藏', 'city': '全部'}, {'province': '辽宁', 'city': '沈阳'}, {'province': '辽宁', 'city': '大连'}, {'province': '辽宁', 'city': '全部'}, {'province': '湖北', 'city': '武汉'}, {'province': '湖北', 'city': '全部'}, {'province': '四川', 'city': '成都'}, {'province': '四川', 'city': '全部'}, {'province': '青海', 'city': '全部'}, {'province': '云南', 'city': '昆明'}, {'province': '云南', 'city': '全部'}, {'province': '浙江', 'city': '杭州'}, {'province': '浙江', 'city': '温州'}, {'province': '浙江', 'city': '宁波'}, {'province': '浙江', 'city': '金华'}, {'province': '浙江', 'city': '嘉兴'}, {'province': '浙江', 'city': '全部'}, {'province': '澳门', 'city': '澳门'}, {'province': '甘肃', 'city': '全部'}, {'province': '陕西', 'city': '西安'}, {'province': '陕西', 'city': '全部'}, {'province': '河南', 'city': '郑州'}, {'province': '河南', 'city': '全部'}, {'province': '贵州', 'city': '贵阳'}, {'province': '贵州', 'city': '全部'}, {'province': '山西', 'city': '全部'}, {'province': '河北', 'city': '石家庄'}, {'province': '河北', 'city': '全部'}, {'province': '香港', 'city': '全部'}, {'province': '天津', 'city': '天津'}, {'province': '新疆', 'city': '全部'}, {'province': '宁夏', 'city': '全部'}, {'province': '福建', 'city': '福州'}, {'province': '福建', 'city': '厦门'}, {'province': '福建', 'city': '泉州'}, {'province': '福建', 'city': '全部'}, {'province': '江西', 'city': '南昌'}, {'province': '江西', 'city': '全部'}, {'province': '海外', 'city': '海外'}]


    list_meta=[]

    for dict_city in list_city:

        for FirstCate,value in DICT_SEARCH.items():

            for dict_cate in value:
                meta={}
                meta['province']=dict_city['province']
                meta['city']=dict_city['city']
                meta['FirstCate'] = FirstCate

                meta['SecondCate']=dict_cate['name']
                list_meta.append(meta)

    print(len(list_meta))

    f = open(r"spiders\table\meta.json", "w")
    json.dump(list_meta, f, ensure_ascii=False)
    f.close()

