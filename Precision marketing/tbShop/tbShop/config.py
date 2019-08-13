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

# LIST_COOKIE=[
#     'miid=1121841226593907354; t=3ed5547c5b7b8fe91c8047c36160054b; thw=cn; cna=Bc20FE+2kWsCAXARZyfv+agB; hng=CN%7Czh-CN%7CCNY%7C156; birthday_displayed=1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _uab_collina=156074362538868539402582; cookie2=1d7a77a862a5728e497832b34b86abb4; _tb_token_=eb1e135be57fa; _cc_=W5iHLLyFfA%3D%3D; tg=5; enc=gREZkEd4fLIp%2BMvg8FOMu%2B4RKGc3aQQfjJlrvI7rZ6xlRRplMjsSm3KeEoDJucvqF61xr7MLP9Q6Y07yZU0gtQ%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; whl=-1%260%260%261561426894411; swfstore=213616; mt=ci=0_0; v=0; uc1=cookie14=UoTaGdntv6UN%2BA%3D%3D; JSESSIONID=B2D7D1D61FA0970B8D11CF1C1BEA4EBC; isg=BKengBfdtq8QTTI0io3NpSqKNtuxhHqYbV4t_XkUSjZdaMQqif74XqgqiijTgFOG; l=bBQBJ0HRqjA0lDyLBOfaZuI8LU_TiIRbzsPzw4OgFICPO7fk5XVPWZHXwELDC3GVZ1WeP3R5I36YBXLOjyIV.',
#     'miid=1121841226593907354; t=3ed5547c5b7b8fe91c8047c36160054b; thw=cn; cna=Bc20FE+2kWsCAXARZyfv+agB; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; tg=0; _cc_=UIHiLt3xSw%3D%3D; enc=LgsmO9hdXJ1tDqa1yn66nDdJILF6MW%2FdmgdeIsktL2vr%2FuOOpEm98lgPPLfkGYilX2AO8OQDmbSH84pgl14sHA%3D%3D; cookie2=19fff2ce319e10fdc7ae2fb13e91a358; _tb_token_=f55104b6a534f; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zZPEr%2FCrvCMS%2BG3sTRRWrQ%2BVVTl09ME1KrXEpvrFZEmTiBjfMoJaU7sfxNSkdCPwLDmiVgnylOzpvhZXezVdvCcJ0hVZjyTO4CADFatt5Y675Vc6bMsMQSP%2FKZ%2BSEH%2BIODva8rHw5%2FQnGPj%2F5iMMFl%2B7R4VPtPZl%2FR3Lh8dpSuTt3bmG78UePZvT3e3s9SW6wvWab%2B0Gwm6HpNnOka9hFIagyS94ezBIawBmWMX1YGMy5EUMimEhpalCU1Vmt6Tk%2BhuKUaTfP4iIVdCTpbFwgES2Lu1eioRjFoFgUDxUb2xtzM%2BZ6DEjyy2nfqv4Ae%2Fw%3D%3D; _m_h5_tk=03b4f973feaad27eb80509dade60482f_1561608138688; _m_h5_tk_enc=741d053c0541c76120a29f22b8422333; swfstore=118256; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=90F218C6F52D8F4B5877B4CB84B94F60; mt=ci=0_0; v=0; l=bBP-APxgqT83bF5DBOfwNuI8LU_OqIRf1sPzw4OgFICPOK195jTdWZH-WTTpC3GVZ1qX83R5I36YB-TGOyCV.; isg=BCQkn_rCJYOWyVHIzsyo6vYU9SLWFUmxsr8OFD5FT--y6cezZc42tzELrUFxMYB_',
#     'miid=1121841226593907354; t=3ed5547c5b7b8fe91c8047c36160054b; thw=cn; cna=Bc20FE+2kWsCAXARZyfv+agB; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; tg=0; enc=LgsmO9hdXJ1tDqa1yn66nDdJILF6MW%2FdmgdeIsktL2vr%2FuOOpEm98lgPPLfkGYilX2AO8OQDmbSH84pgl14sHA%3D%3D; _m_h5_tk=e5e9f599c598da4234027c845d3878a3_1561624107128; _m_h5_tk_enc=bb4d2139cca9460834cc9d2b1b34e891; _cc_=WqG3DMC9EA%3D%3D; cookie2=12703d520a32122268ca802bf9b8b14f; _tb_token_=ea5877e5e7377; mt=ci=0_0; v=0; isg=BMrKrTg_oxDBRy-6pIpuOEy6G7CsE0-D-GEQxlQCXJ2oB2nBOkueJRAhE3Pb98at; l=bBP-APxgqT83b5wvBOfaquI8LU_9rIRbzsPzw4OgFICPOefM51oFWZH52uTHC3GVw1feS3R5I36YBeYBqtf..',
#     ]
LIST_COOKIE=[
'cna=wreTE5+5pRsCAXARfXGOIRCu; enc=7DBlORmYTyj%2B6YPASNY6E9L%2BT0ZoiOLQcbAIwziWxau2FWq61Vtbs%2FNUhT626%2BR8Sfohh%2BzkeifM%2FQPtgjOfcA%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=171595862063787402; uc3=vt3=F8dBy32uPXTUlOCPsaE%3D&id2=UoH4HFNPF9kkww%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D&nk2=F5RMGLcxQ5EfSL1W; lgc=tb9113796_99; t=cc5c3369a597fe072ef2a9a24ae07243; uc4=nk4=0%40FY4HXZ50AdmJ50Phr5MDZXNcXWagcbA%3D&id4=0%40UOnnGcrCg0L%2F9FBZLExMpgCjJyRy; tracknick=tb9113796_99; _cc_=UIHiLt3xSw%3D%3D; tg=0; mt=ci=24_1; cookie2=50d596e0af251f1b7f6941be8a94b2f2; v=0; _tb_token_=f63483737a39e; uc1=cookie14=UoTaHYuj2WbADw%3D%3D; _uab_collina=156559573861556782699252; x5sec=7b2274616f62616f2d73686f707365617263683b32223a22326633623966626231313064646463633337366439353430653931646136393043497535784f6f4645496e663976624e3170694873514561444445774e7a6b324e546b334d6a67374d673d3d227d; JSESSIONID=82DAE6AC5B776B72073C934E6E913521; isg=BIqKYWKk45Qs-2lljfHpyNIPz3Ds0w9qsos8yBTDNl1oxyqB_Ate5dA103O-LIZt; l=cBIgUtTqvPSbp5ytBOCanurza77OSLRYYuPzaNbMi_5p96T_WN7Ok-NICF96VjWd_EYB4BbMhIJ9-etkZ8IN5C8U-dWG.',
    ]





if __name__ == '__main__':
    DICT_CITY = get_dict(r'spiders\table\tbCity.json')
    DICT_SEARCH = get_dict(r'spiders\table\tbSearch.json')

    # print(DICT_CITY)
    # list_city=[]
    # for province,value in DICT_CITY.items():
    #     print(province,value)
    #     if value['children']==[]:
    #         list_city.append({'province':province+','+value['id'],'city':''})
    #     else:
    #         for dict_city in value['children']:
    #             dict_1={}
    #             dict_1['province']=province+','+value['id']
    #             dict_1['city']=dict_city['name']+','+dict_city['id']
    #             list_city.append(dict_1)
    #     print(list_city)
    #
    # print(len(list_city))
    # f = open(r"spiders\table\list_city.json", "w")
    # json.dump(list_city, f, ensure_ascii=False)
    # f.close()

    #
    # list_city = get_dict(r'spiders\table\list_city.json')
    #
    # list_meta=[]
    #
    # for dict_city in list_city:
    #     print(dict_city)
    #
    #     for FirstCate,value in DICT_SEARCH.items():
    #         print(FirstCate,value)
    #
    #         for dict_cate in value['children']:
    #             meta={}
    #             meta['province']=dict_city['province']
    #             meta['city']=dict_city['city']
    #             meta['FirstCate'] = FirstCate
    #             meta['SecondCate']=dict_cate['name']
    #             print(meta)
    #             list_meta.append(meta)
    #
    #
    # print(len(list_meta))
    # f = open(r"spiders\table\meta.json", "w")
    # json.dump(list_meta, f, ensure_ascii=False)
    # f.close()

