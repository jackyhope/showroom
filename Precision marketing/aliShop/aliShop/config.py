# -*- coding: utf-8 -*- 
# @Author : Zhy

'''获取所有类目，保存在meta.json文件中'''

import json
import requests
import time
import random

def PROXIES():
    # 阿布云代理隧道验证信息

    from urllib import request
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    proxyUser = "user"       #账号
    proxyPass = "password"   #密码

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
            time.sleep(random.uniform(1, 1.5))
            pass
def get_dict(file):
    with open(file, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict

proxies = PROXIES()



if __name__ == '__main__':
    DICT_CITY = get_dict(r'spiders\table\aliCity.json')
    DICT_SEARCH = get_dict(r'spiders\table\aliSearch.json')

    list_re=['北京','上海','天津','重庆','海外']
    list_hot=[{'city': '', 'province': '重庆'}, {'city': '', 'province': '天津'}, {'city': '', 'province': '北京'}, {'city': '', 'province': '上海'},{'city': '', 'province': '海外'},]

    list_meta=[]
    #
    # for name,value in DICT_CITY.items():
    #     if name not in list_re:
    #         for dict_children in value['children']:
    #             dict_1 = {}
    #             dict_1['province'] = name
    #             dict_1['city']=dict_children['name']
    #             list_city.append(dict_1)
    #
    #     print(list_city)
    #
    # print(len(list_city))
    # print(list_city)
    #
    # f = open(r"spiders\table\listCity.json", "w")
    # json.dump(list_meta, f, ensure_ascii=False)
    # f.close()

    list_city=[{'province': '重庆', 'city': ''}, {'province': '天津', 'city': ''}, {'province': '北京', 'city': ''}, {'province': '上海', 'city': ''}, {'province': '海外', 'city': ''}, {'province': '福建', 'city': '福州'}, {'province': '福建', 'city': '厦门'}, {'province': '福建', 'city': '泉州'}, {'province': '福建', 'city': '漳州'}, {'province': '福建', 'city': '龙岩'}, {'province': '福建', 'city': '南平'}, {'province': '福建', 'city': '宁德'}, {'province': '福建', 'city': '莆田'}, {'province': '福建', 'city': '三明'}, {'province': '海南', 'city': '海口'}, {'province': '海南', 'city': '三亚'}, {'province': '海南', 'city': '琼海'}, {'province': '海南', 'city': '东方'}, {'province': '海南', 'city': '儋州'}, {'province': '海南', 'city': '万宁'}, {'province': '海南', 'city': '文昌'}, {'province': '海南', 'city': '定安县'}, {'province': '海南', 'city': '五指山'}, {'province': '海南', 'city': '屯昌县'}, {'province': '海南', 'city': '澄迈县'}, {'province': '海南', 'city': '临高县'}, {'province': '海南', 'city': '白沙黎族自'}, {'province': '海南', 'city': '昌江黎族自'}, {'province': '海南', 'city': '乐东黎族自'}, {'province': '海南', 'city': '陵水黎族自'}, {'province': '海南', 'city': '琼中黎族苗'}, {'province': '海南', 'city': '保亭黎族苗'}, {'province': '甘肃', 'city': '兰州'}, {'province': '甘肃', 'city': '白银'}, {'province': '甘肃', 'city': '酒泉'}, {'province': '甘肃', 'city': '定西'}, {'province': '甘肃', 'city': '嘉峪关'}, {'province': '甘肃', 'city': '金昌'}, {'province': '甘肃', 'city': '庆阳'}, {'province': '甘肃', 'city': '陇南'}, {'province': '甘肃', 'city': '平凉'}, {'province': '甘肃', 'city': '天水'}, {'province': '甘肃', 'city': '武威'}, {'province': '甘肃', 'city': '张掖'}, {'province': '甘肃', 'city': '甘南藏族自'}, {'province': '甘肃', 'city': '临夏回族自'}, {'province': '陕西', 'city': '西安'}, {'province': '陕西', 'city': '咸阳'}, {'province': '陕西', 'city': '汉中'}, {'province': '陕西', 'city': '安康'}, {'province': '陕西', 'city': '宝鸡'}, {'province': '陕西', 'city': '商洛'}, {'province': '陕西', 'city': '铜川'}, {'province': '陕西', 'city': '渭南'}, {'province': '陕西', 'city': '延安'}, {'province': '陕西', 'city': '榆林'}, {'province': '内蒙古', 'city': '呼和浩特'}, {'province': '内蒙古', 'city': '包头'}, {'province': '内蒙古', 'city': '赤峰'}, {'province': '内蒙古', 'city': '鄂尔多斯'}, {'province': '内蒙古', 'city': '呼伦贝尔'}, {'province': '内蒙古', 'city': '阿拉善盟'}, {'province': '内蒙古', 'city': '通辽'}, {'province': '内蒙古', 'city': '乌海'}, {'province': '内蒙古', 'city': '兴安盟'}, {'province': '内蒙古', 'city': '巴彦淖尔'}, {'province': '内蒙古', 'city': '乌兰察布盟'}, {'province': '内蒙古', 'city': '锡林郭勒盟'}, {'province': '江苏', 'city': '南京'}, {'province': '江苏', 'city': '苏州'}, {'province': '江苏', 'city': '无锡'}, {'province': '江苏', 'city': '常州'}, {'province': '江苏', 'city': '淮安'}, {'province': '江苏', 'city': '镇江'}, {'province': '江苏', 'city': '扬州'}, {'province': '江苏', 'city': '徐州'}, {'province': '江苏', 'city': '连云港'}, {'province': '江苏', 'city': '南通'}, {'province': '江苏', 'city': '宿迁'}, {'province': '江苏', 'city': '泰州'}, {'province': '江苏', 'city': '盐城'}, {'province': '黑龙江', 'city': '哈尔滨'}, {'province': '黑龙江', 'city': '大庆'}, {'province': '黑龙江', 'city': '佳木斯'}, {'province': '黑龙江', 'city': '鹤岗'}, {'province': '黑龙江', 'city': '牡丹江'}, {'province': '黑龙江', 'city': '黑河'}, {'province': '黑龙江', 'city': '鸡西'}, {'province': '黑龙江', 'city': '七台河'}, {'province': '黑龙江', 'city': '齐齐哈尔'}, {'province': '黑龙江', 'city': '双鸭山'}, {'province': '黑龙江', 'city': '绥化'}, {'province': '黑龙江', 'city': '伊春'}, {'province': '黑龙江', 'city': '大兴安岭'}, {'province': '澳门', 'city': '澳门半岛'}, {'province': '澳门', 'city': '澳门离岛'}, {'province': '贵州', 'city': '贵阳'}, {'province': '贵州', 'city': '安顺'}, {'province': '贵州', 'city': '毕节'}, {'province': '贵州', 'city': '铜仁'}, {'province': '贵州', 'city': '遵义'}, {'province': '贵州', 'city': '六盘水'}, {'province': '贵州', 'city': '黔东南苗族'}, {'province': '贵州', 'city': '黔南布依族'}, {'province': '贵州', 'city': '黔西南布依'}, {'province': '河南', 'city': '郑州'}, {'province': '河南', 'city': '洛阳'}, {'province': '河南', 'city': '开封'}, {'province': '河南', 'city': '焦作'}, {'province': '河南', 'city': '安阳'}, {'province': '河南', 'city': '南阳'}, {'province': '河南', 'city': '周口'}, {'province': '河南', 'city': '商丘'}, {'province': '河南', 'city': '新乡'}, {'province': '河南', 'city': '鹤壁'}, {'province': '河南', 'city': '平顶山'}, {'province': '河南', 'city': '三门峡'}, {'province': '河南', 'city': '信阳'}, {'province': '河南', 'city': '许昌'}, {'province': '河南', 'city': '驻马店'}, {'province': '河南', 'city': '漯河'}, {'province': '河南', 'city': '濮阳'}, {'province': '四川', 'city': '成都'}, {'province': '四川', 'city': '宜宾'}, {'province': '四川', 'city': '绵阳'}, {'province': '四川', 'city': '巴中'}, {'province': '四川', 'city': '攀枝花'}, {'province': '四川', 'city': '达州'}, {'province': '四川', 'city': '德阳'}, {'province': '四川', 'city': '遂宁'}, {'province': '四川', 'city': '广安'}, {'province': '四川', 'city': '广元'}, {'province': '四川', 'city': '乐山'}, {'province': '四川', 'city': '泸州'}, {'province': '四川', 'city': '眉山'}, {'province': '四川', 'city': '南充'}, {'province': '四川', 'city': '内江'}, {'province': '四川', 'city': '雅安'}, {'province': '四川', 'city': '资阳'}, {'province': '四川', 'city': '自贡'}, {'province': '四川', 'city': '甘孜藏族自'}, {'province': '四川', 'city': '凉山彝族自'}, {'province': '四川', 'city': '阿坝藏族羌'}, {'province': '湖南', 'city': '长沙'}, {'province': '湖南', 'city': '常德'}, {'province': '湖南', 'city': '株洲'}, {'province': '湖南', 'city': '岳阳'}, {'province': '湖南', 'city': '郴州'}, {'province': '湖南', 'city': '怀化'}, {'province': '湖南', 'city': '湘潭'}, {'province': '湖南', 'city': '张家界'}, {'province': '湖南', 'city': '衡阳'}, {'province': '湖南', 'city': '娄底'}, {'province': '湖南', 'city': '邵阳'}, {'province': '湖南', 'city': '益阳'}, {'province': '湖南', 'city': '永州'}, {'province': '湖南', 'city': '湘西土家族'}, {'province': '吉林', 'city': '长春'}, {'province': '吉林', 'city': '吉林'}, {'province': '吉林', 'city': '四平'}, {'province': '吉林', 'city': '通化'}, {'province': '吉林', 'city': '白城'}, {'province': '吉林', 'city': '白山'}, {'province': '吉林', 'city': '辽源'}, {'province': '吉林', 'city': '松原'}, {'province': '吉林', 'city': '延边朝鲜族'}, {'province': '山西', 'city': '太原'}, {'province': '山西', 'city': '大同'}, {'province': '山西', 'city': '晋城'}, {'province': '山西', 'city': '晋中'}, {'province': '山西', 'city': '临汾'}, {'province': '山西', 'city': '吕梁'}, {'province': '山西', 'city': '朔州'}, {'province': '山西', 'city': '长治'}, {'province': '山西', 'city': '忻州'}, {'province': '山西', 'city': '阳泉'}, {'province': '山西', 'city': '运城'}, {'province': '安徽', 'city': '合肥'}, {'province': '安徽', 'city': '芜湖'}, {'province': '安徽', 'city': '马鞍山'}, {'province': '安徽', 'city': '淮南'}, {'province': '安徽', 'city': '蚌埠'}, {'province': '安徽', 'city': '黄山'}, {'province': '安徽', 'city': '阜阳'}, {'province': '安徽', 'city': '淮北'}, {'province': '安徽', 'city': '铜陵'}, {'province': '安徽', 'city': '亳州'}, {'province': '安徽', 'city': '宣城'}, {'province': '安徽', 'city': '安庆'}, {'province': '安徽', 'city': '巢湖'}, {'province': '安徽', 'city': '池州'}, {'province': '安徽', 'city': '六安'}, {'province': '安徽', 'city': '滁州'}, {'province': '安徽', 'city': '宿州'}, {'province': '宁夏', 'city': '银川'}, {'province': '宁夏', 'city': '固原'}, {'province': '宁夏', 'city': '石嘴山'}, {'province': '宁夏', 'city': '吴忠'}, {'province': '宁夏', 'city': '中卫'}, {'province': '山东', 'city': '济南'}, {'province': '山东', 'city': '青岛'}, {'province': '山东', 'city': '烟台'}, {'province': '山东', 'city': '济宁'}, {'province': '山东', 'city': '滨州'}, {'province': '山东', 'city': '莱芜'}, {'province': '山东', 'city': '日照'}, {'province': '山东', 'city': '潍坊'}, {'province': '山东', 'city': '淄博'}, {'province': '山东', 'city': '德州'}, {'province': '山东', 'city': '威海'}, {'province': '山东', 'city': '东营'}, {'province': '山东', 'city': '菏泽'}, {'province': '山东', 'city': '聊城'}, {'province': '山东', 'city': '临沂'}, {'province': '山东', 'city': '泰安'}, {'province': '山东', 'city': '枣庄'}, {'province': '浙江', 'city': '杭州'}, {'province': '浙江', 'city': '宁波'}, {'province': '浙江', 'city': '温州'}, {'province': '浙江', 'city': '绍兴'}, {'province': '浙江', 'city': '台州'}, {'province': '浙江', 'city': '嘉兴'}, {'province': '浙江', 'city': '金华'}, {'province': '浙江', 'city': '丽水'}, {'province': '浙江', 'city': '湖州'}, {'province': '浙江', 'city': '衢州'}, {'province': '浙江', 'city': '舟山'}, {'province': '江西', 'city': '南昌'}, {'province': '江西', 'city': '上饶'}, {'province': '江西', 'city': '抚州'}, {'province': '江西', 'city': '赣州'}, {'province': '江西', 'city': '九江'}, {'province': '江西', 'city': '鹰潭'}, {'province': '江西', 'city': '吉安'}, {'province': '江西', 'city': '景德镇'}, {'province': '江西', 'city': '萍乡'}, {'province': '江西', 'city': '新余'}, {'province': '江西', 'city': '宜春'}, {'province': '云南', 'city': '昆明'}, {'province': '云南', 'city': '保山'}, {'province': '云南', 'city': '丽江'}, {'province': '云南', 'city': '玉溪'}, {'province': '云南', 'city': '昭通'}, {'province': '云南', 'city': '临沧'}, {'province': '云南', 'city': '曲靖'}, {'province': '云南', 'city': '普洱'}, {'province': '云南', 'city': '楚雄彝族自'}, {'province': '云南', 'city': '大理白族自'}, {'province': '云南', 'city': '迪庆藏族自'}, {'province': '云南', 'city': '怒江傈傈族'}, {'province': '云南', 'city': '文山壮族苗'}, {'province': '云南', 'city': '西双版纳傣'}, {'province': '云南', 'city': '德宏傣族景'}, {'province': '云南', 'city': '红河哈尼族'}, {'province': '辽宁', 'city': '沈阳'}, {'province': '辽宁', 'city': '大连'}, {'province': '辽宁', 'city': '鞍山'}, {'province': '辽宁', 'city': '丹东'}, {'province': '辽宁', 'city': '抚顺'}, {'province': '辽宁', 'city': '本溪'}, {'province': '辽宁', 'city': '朝阳'}, {'province': '辽宁', 'city': '铁岭'}, {'province': '辽宁', 'city': '锦州'}, {'province': '辽宁', 'city': '辽阳'}, {'province': '辽宁', 'city': '阜新'}, {'province': '辽宁', 'city': '葫芦岛'}, {'province': '辽宁', 'city': '盘锦'}, {'province': '辽宁', 'city': '营口'}, {'province': '香港', 'city': '香港岛'}, {'province': '香港', 'city': '九龙'}, {'province': '香港', 'city': '新界'}, {'province': '西藏', 'city': '拉萨'}, {'province': '西藏', 'city': '阿里'}, {'province': '西藏', 'city': '昌都'}, {'province': '西藏', 'city': '林芝'}, {'province': '西藏', 'city': '那曲'}, {'province': '西藏', 'city': '日喀则'}, {'province': '西藏', 'city': '山南'}, {'province': '台湾', 'city': '台北县'}, {'province': '台湾', 'city': '宜兰县'}, {'province': '台湾', 'city': '桃园县'}, {'province': '台湾', 'city': '新竹县'}, {'province': '台湾', 'city': '苗栗县'}, {'province': '台湾', 'city': '台中县'}, {'province': '台湾', 'city': '彰化县'}, {'province': '台湾', 'city': '南投县'}, {'province': '台湾', 'city': '云林县'}, {'province': '台湾', 'city': '嘉义县'}, {'province': '台湾', 'city': '台南县'}, {'province': '台湾', 'city': '高雄县'}, {'province': '台湾', 'city': '屏东县'}, {'province': '台湾', 'city': '台东县'}, {'province': '台湾', 'city': '花莲县'}, {'province': '台湾', 'city': '澎湖县'}, {'province': '台湾', 'city': '基隆市'}, {'province': '台湾', 'city': '新竹市'}, {'province': '台湾', 'city': '台中市'}, {'province': '台湾', 'city': '嘉义市'}, {'province': '台湾', 'city': '台南市'}, {'province': '台湾', 'city': '台北市'}, {'province': '台湾', 'city': '高雄市'}, {'province': '台湾', 'city': '金门县'}, {'province': '台湾', 'city': '连江县'}, {'province': '湖北', 'city': '武汉'}, {'province': '湖北', 'city': '黄冈'}, {'province': '湖北', 'city': '黄石'}, {'province': '湖北', 'city': '荆门'}, {'province': '湖北', 'city': '荆州'}, {'province': '湖北', 'city': '潜江'}, {'province': '湖北', 'city': '宜昌'}, {'province': '湖北', 'city': '鄂州'}, {'province': '湖北', 'city': '十堰'}, {'province': '湖北', 'city': '随州'}, {'province': '湖北', 'city': '天门'}, {'province': '湖北', 'city': '仙桃'}, {'province': '湖北', 'city': '咸宁'}, {'province': '湖北', 'city': '襄樊'}, {'province': '湖北', 'city': '孝感'}, {'province': '湖北', 'city': '神农架林区'}, {'province': '湖北', 'city': '恩施土家族'}, {'province': '新疆', 'city': '乌鲁木齐'}, {'province': '新疆', 'city': '哈密'}, {'province': '新疆', 'city': '和田'}, {'province': '新疆', 'city': '喀什'}, {'province': '新疆', 'city': '吐鲁番'}, {'province': '新疆', 'city': '阿克苏'}, {'province': '新疆', 'city': '阿拉尔'}, {'province': '新疆', 'city': '石河子'}, {'province': '新疆', 'city': '五家渠'}, {'province': '新疆', 'city': '克拉玛依'}, {'province': '新疆', 'city': '图木舒克'}, {'province': '新疆', 'city': '昌吉回族自'}, {'province': '新疆', 'city': '伊犁哈萨克'}, {'province': '新疆', 'city': '巴音郭楞蒙'}, {'province': '新疆', 'city': '博尔塔拉蒙'}, {'province': '新疆', 'city': '克孜勒苏柯'}, {'province': '新疆', 'city': '塔城地区'}, {'province': '新疆', 'city': '阿勒泰地区'}, {'province': '广西', 'city': '南宁'}, {'province': '广西', 'city': '桂林'}, {'province': '广西', 'city': '北海'}, {'province': '广西', 'city': '柳州'}, {'province': '广西', 'city': '梧州'}, {'province': '广西', 'city': '玉林'}, {'province': '广西', 'city': '百色'}, {'province': '广西', 'city': '崇左'}, {'province': '广西', 'city': '贵港'}, {'province': '广西', 'city': '河池'}, {'province': '广西', 'city': '贺州'}, {'province': '广西', 'city': '来宾'}, {'province': '广西', 'city': '防城港'}, {'province': '广西', 'city': '钦州'}, {'province': '青海', 'city': '西宁'}, {'province': '青海', 'city': '海东'}, {'province': '青海', 'city': '果洛藏族自'}, {'province': '青海', 'city': '海北藏族自'}, {'province': '青海', 'city': '海南藏族自'}, {'province': '青海', 'city': '黄南藏族自'}, {'province': '青海', 'city': '玉树藏族自'}, {'province': '青海', 'city': '海西蒙古族'}, {'province': '广东', 'city': '广州'}, {'province': '广东', 'city': '深圳'}, {'province': '广东', 'city': '珠海'}, {'province': '广东', 'city': '潮州'}, {'province': '广东', 'city': '中山'}, {'province': '广东', 'city': '东莞'}, {'province': '广东', 'city': '佛山'}, {'province': '广东', 'city': '惠州'}, {'province': '广东', 'city': '汕头'}, {'province': '广东', 'city': '汕尾'}, {'province': '广东', 'city': '韶关'}, {'province': '广东', 'city': '湛江'}, {'province': '广东', 'city': '肇庆'}, {'province': '广东', 'city': '河源'}, {'province': '广东', 'city': '江门'}, {'province': '广东', 'city': '揭阳'}, {'province': '广东', 'city': '茂名'}, {'province': '广东', 'city': '梅州'}, {'province': '广东', 'city': '清远'}, {'province': '广东', 'city': '阳江'}, {'province': '广东', 'city': '云浮'}, {'province': '河北', 'city': '石家庄'}, {'province': '河北', 'city': '保定'}, {'province': '河北', 'city': '沧州'}, {'province': '河北', 'city': '秦皇岛'}, {'province': '河北', 'city': '承德'}, {'province': '河北', 'city': '邯郸'}, {'province': '河北', 'city': '唐山'}, {'province': '河北', 'city': '邢台'}, {'province': '河北', 'city': '廊坊'}, {'province': '河北', 'city': '衡水'}, {'province': '河北', 'city': '张家口'}]


    for dict_city in list_city:

        for FirstCate,value in DICT_SEARCH.items():

            for dict_cate in value['children']:
                SecondCate=dict_cate['name']
                for dict_3 in dict_cate['children']:
                    meta={}
                    meta['province']=dict_city['province']
                    meta['city']=dict_city['city']
                    meta['FirstCate'] = FirstCate
                    meta['SecondCate']=SecondCate
                    meta['ThirdCate']=dict_3['name']
                    list_meta.append(meta)

    print(len(list_meta))
    f = open(r"spiders\table\meta.json", "w")
    json.dump(list_meta, f, ensure_ascii=False)
    f.close()





