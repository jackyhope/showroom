import getpass
import sqlite3
import platform
from al_qf import *
from lxml import etree
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.utils import parsedate, parsedate_to_datetime
from datetime import datetime
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Thread
from func_58 import *

from urllib import parse
now_osuser = getpass.getuser()
os_platform = platform.platform()
if 'Windows-XP' in os_platform:
    cookfile = r'C:\Documents and Settings\Administrator\Local Settings\Application Data\Google\Chrome\User Data\Default\Cookies'
else:
    cookfile = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Cookies'
# if now_osuser != 'Administrator':
#     cookfile = cookfile.replace('Administrator', now_osuser)
USER_AGENTS = [
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
cookies_basis_58 = '58home=hz; id58=c5/njVrkAq4CHw7fCy2pAg==; city=hz; 58tj_uuid=1f516501-df3b-4ebd-9c53-ecc7b1d9b885; als=0; commontopbar_myfeet_tooltip=end; xxzl_deviceid=Hb6BJKfGNnpCtcAZW5scSlpeq0arRmILCxjIJuH%2Bv2dVGVZgAb3wEV4Ca0Ot5vXV; xxzl_smartid=5df4462181a0e9a59ad660693e06180b; showOrder=1; showPTTip=1; ljrzfc=1; wmda_uuid=3bbb65d735f4aca3baf11990491e042a; wmda_new_uuid=1; wmda_visited_projects=%3B1731916484865; getKey=1; new_uv=18; utm_source=; spm=; init_refer=; new_session=0; ppStore_fingerprint=1E29E49F92B622558C0F49B1EEC5C6D071A46AB80C1100D2%EF%BC%BF1526605436746; PPU="UID=34650726585862&UN=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&TT=5a6401ac9086214f9d16ca3b1086d9e7&PBODY=Z8JmnhEeK5SxeIcyEEsZuf89rEIg-vcNBo40_0H-zkIWAdUIHCbzrQ5Q4XFC48aQrJWcGAMR7B-SUAL7zPYcbl4lIn9oaKBoEvC0g6rIRITDcj5qOOuP3efm-Koeua7KdCyiddcL-DbXX0teXQaq0ynbEV-OeY4OeQK-4vz5MIw&VER=1"; 58cooper="userid=34650726585862&username=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&cooperkey=e27167b5b83925fb7d570f5ce95666ab"; www58com="AutoLogin=true&UserID=34650726585862&UserName=%E4%BC%81%E8%9C%82%E9%80%9A%E4%BF%A1%E6%9D%AD%E5%B7%9E%E5%88%86%E5%85%AC%E5%8F%B8&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=887EB60F8846773DB0F871F4A103A2056CDD83AE89F6452A0&Phone=&WltUrl=&UserLoginVer=08CDD29DF3C97588732B3336A726CC43F&LT=1526605454806"; vip=vipusertype%3D0%26vipuserpline%3D0%26v%3D1%26vipkey%3D782bcfd78f29e63156ec0afa9efbfc25%26masteruserid%3D34650726585862; wmda_session_id_1731916484865=1526605965138-4d558735-cb44-1cac'
cookies_basis_hzrc = 'UM_distinctid=163de889caed3-028b380ab63eff-44410a2e-100200-163de889caf41c; _ubm_id.d2cc513d10e26176994c26da25947ea2=1096e84c977a2486; longinUser=wb; Hm_lvt_46b0265c3ac55b35a0fc9e4683094a94=1528508654,1528685759; JSESSIONID=fFwgwAdo1QFX1mrVudLvHNpTntWrDysZgTlsfgj8A1c9cFn9Q-Cw!-196033929; CNZZDATA2145298=cnzz_eid%3D868844613-1528441555-null%26ntime%3D1529560309; _ubm_ses.d2cc513d10e26176994c26da25947ea2=*; Hm_lpvt_46b0265c3ac55b35a0fc9e4683094a94=1529563918'
cookies_basis_zl = "JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976"
cookies_basis_gj = 'ganji_xuuid=c7dc72ef-60db-4264-aced-0a6a701c2cd3.1528708751959; ganji_uuid=7150266604199787963746; xxzl_deviceid=hNmWYgYm3yVBw3yuNYA%2BLPpzVYJGhHRfC9VGkavtS3QxEfmxbyvsUW%2F%2FIgzp8FIi; lg=1; NTKF_T2D_CLIENTID=guestA8ABE4E8-9FE5-DEC9-A48B-EE251D637B74; cityDomain=bj; citydomain=bj; 58tj_uuid=def2acb6-3e85-430a-8c40-c72caf90a077; als=0; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A31561918616%7D; use_https=1; new_uv=3; __utmc=32156897; __utmz=32156897.1529023568.3.3.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; nTalk_CACHE_DATA={uid:kf_10111_ISME9754_557709909}; username_login_n=15669087700; GanjiLoginType=0; __utma=32156897.1024205804.1528708769.1529023568.1529029837.4; GANJISESSID=shdb8t2vgn99tnkn0ofdcgrihf; sscode=9HsRkf041lVH%2BQf39HWsQh54; GanjiUserName=szfl666; GanjiUserInfo=%7B%22user_id%22%3A557709909%2C%22email%22%3A%22%22%2C%22username%22%3A%22szfl666%22%2C%22user_name%22%3A%22szfl666%22%2C%22nickname%22%3A%22%5Cu5e73%5Cu5b89%5Cu6768%5Cu9752%5Cu9752%22%7D; bizs=%5B3%5D; supercookie=AGH3AmN5BGN5WQtlMTMuAmRkMwNlLmOvLGp0ZTMzLzMyMJWvAJZ0BGH0LmpjMwSuMGR%3D; xxzl_smartid=46229e619fb608c62d39dc189295baf9; last_name=szfl666; ganji_login_act=1529044045164'
cookies_basis_lp = 'abtest=0; _fecdn_=1; __uuid=1530527233544.45; __tlog=1530527233545.26%7C00000000%7C00000000%7Cs_00_pz0%7Cs_00_pz0; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1530527234; _mscid=s_00_pz0; _uuid=5A88398AFFA848187736D9B9BF2D2CD8; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1530527255; user_name=%E9%83%AD%E5%AD%90%E6%A1%A2; lt_auth=6L5bbCcFxl76tnGKiGpet69N3dOtU27O9H9Y0RFV1oe%2BD%2F3i4PrlQwOErLIDxBIhlkt3JsULNLP%2B%0D%0AMOr5y3VD6UMTwGmnlYCxuuW70XweTedcdvmi0a72kMzZQslxnXEHyHBg8H9Okx31sUAhN9TvnF7I%0D%0Ap6HH7ral8vvE%0D%0A; UniqueKey=d4d47f8153c841621a667e00ad0d9493; user_kind=1; _l_o_L_=e3c9b446218c5b2bd4d47f8153c841621a667e00ad0d9493; login_temp=islogin; _e_ld_auth_=ac23e04875d8628e; b-beta2-config=%7B%22d%22%3A365%2C%22e%22%3A9612079%2C%22ejm%22%3A%221%22%2C%22n%22%3A%22%25E9%2583%25AD%25E5%25AD%2590%25E6%25A1%25A2%22%2C%22audit%22%3A%221%22%2C%22ecomp_id%22%3A9612079%2C%22photo%22%3A%22%2F%2Fimage0.lietou-static.com%2Fimg%2F5afa5b868e50d906233368cf04a.png%22%2C%22version%22%3A%222%22%2C%22hasPhoneNum%22%3A%221%22%2C%22v%22%3A%222%22%2C%22ecreate_time%22%3A%2220180702%22%2C%22p%22%3A%222%22%2C%22entry%22%3A%221%22%2C%22jz%22%3A%220%22%7D; imClientId=3a3ef6be625ffffc4462f629076d8d2a; imId=3a3ef6be625ffffc5da7d3574f2ad402; fe_lpt_jipinByOneGiveTwo=true; fe_lpt_resumeLib=true; fe_lpt_sevenAnniversaryBegin=true; fe_lpt_realname=true; JSESSIONID=24835A675443F7EA7CF7131A3639013B; __session_seq=34; __uv_seq=34'
cookies_basis_boss = 't=iGi5GHct1hJtEcXs; wt=iGi5GHct1hJtEcXs; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1531788978,1531874497; __c=1531874497; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCwtxAKnPLdPYamZHCAx0xu2z7FldlGtRqlEqZHkU2JxwW_10IbmDQVPG88TAoDGb%26wd%3D%26eqid%3D84749153000331aa000000045b4e8cbb; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1531874825; __a=6342634.1531788976.1531789284.1531874497.18.3.7.18'
cookies_basis_lg = 'user_trace_token=20180608172121-4e7272f2-6afd-11e8-942d-5254005c3644; LGUID=20180608172121-4e7276ee-6afd-11e8-942d-5254005c3644; LG_LOGIN_USER_ID=a037173e83dd072da9f3ddf0141401b1847ae1274a49cb8706d0dfe51c362b0d; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAAADAAAEE67B0B4E271A1563F641CA62320D4E337; mds_login_authToken="QTx9OrCX/HyIgwfYM2PRnijqFX36RAo18aBeXYE48Wi2da+ZKoRIjp+IZlsukDxy4+m88GXbjD2EAMQfN1MFDY68/jOyusIWUGuoQa36kskg3cIHTmOK7y/+tnfTQ/gOub3owMsyEpypBuHsbXOeLs+D9K/A18Cs6cflM2D5cmZ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=13656711074; mds_u_ci=405490; mds_u_cn=%5Cu5b81%5Cu6ce2%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1%5Cu6280%5Cu672f%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu4f01%5Cu8702%5Cu901a%5Cu4fe1; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresult.htm%3Fkeyword%3D%25E7%2588%25AC%25E8%2599%25AB; PRE_LAND=https%3A%2F%2Feasy.lagou.com%2Fsearch%2Fresume%2FfetchResume.htm%3FresumeFetchKey%3DnfvspaeP6NuOwyqzBx9oU2egDzfETa11ITJjcp5AhNuvtQvtxYgYBFs4vNIHLCMbzuDNiOeNFj_ohOizRgxioQ%3D%3D%26outerPositionId%3D; gate_login_token=f1ba0d394e31ca9d1431cb1d8cc19a0a0d0d8663274eec62c194275bea0d51f7; _gat=1; _putrc=F3EC4483D6493723123F89F2B170EADC; login=true; unick=%E9%92%9F%E7%BA%A2%E4%B9%89; _ga=GA1.2.1078549279.1528449670; _gid=GA1.2.1608387311.1531095960; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530752513,1530776510,1530789547,1531095960; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531096043; Hm_lvt_bfa5351db2249abae67476f1ec317000=1530791548,1530838877,1531095947,1531095969; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1531096422; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2211181887%22%2C%22%24device_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22first_id%22%3A%2216464b1e240337-01b39e9c159c71-71292b6e-1049088-16464b1e241286%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.3.1078549279.1528449670; Hm_lvt_b53988385ecf648a7a8254b14163814d=1530697743,1530750651,1531096057; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1531096424; X_HTTP_TOKEN=5a6e08c0ea501f3ab938664c167ae639; LGSID=20180709082602-a9273bcc-830e-11e8-81dc-525400f775ce; LGRID=20180709083345-bcec605f-830f-11e8-81dc-525400f775ce; gray=resume'
cookies_basis_zhyc = 'als=0; chrId=3da5b6992c494b81a648beaec3a9d766; uniq=141aeef3c6744a369ecf180be790ae47; loginTime=1531726094; _blong=1; _buname=qifengtongxin; wmda_uuid=462c2b6e6b98a2ad6faad624283db65d; wmda_new_uuid=1; wmda_visited_projects=%3B1730494577921; show_skmap_intro=1; gtid=8f61bbe493524a4cadf25a9babc65348; skill-map-hint=1; gr_session_id_927337b436c67ce1=0a81ddcb-6035-4a0d-a9aa-c88430ab4878; gr_session_id_927337b436c67ce1_0a81ddcb-6035-4a0d-a9aa-c88430ab4878=true; RecentVisitCity=182_hangzhou; RecentVisitCityFullpathPc="17,182"; bps="buid=36575385187329&bst=1531738322443&bstSign=cae839f3dc893cecb62&blt=1531738322443&bltSign=8ddebfcb37bb2977bf1&lg=1531734320884&tk=36575385187329&source=1&lo=1"; gr_user_id=a1a3173d-c5a6-413e-8c27-2ad432ce4b08; wmda_session_id_1730494577921=1531734321039-6c63fc77-3698-8910; 58tj_uuid=0cfb7f75-68f2-4e93-9589-721afb398afd; channel=social; new_session=0; new_uv=8; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DQ-B4FQLb_uSXvK6PQPZfDrIKx67sc7OqlvEG9OteI0UAP0AWzHE-4NXKAWa150zV%2526wd%253D%2526eqid%253Da717ef2d0002d72b000000045b4c718e'
cookies_basis_sxs = '__jsluid=b479516d6fb68b555bdf3b04d4d95aee; sxs_usr="2|1:0|10:1531880807|7:sxs_usr|24:dXNyX3lnbG92OGlhdnh5cg==|2a088019793e0f5181ca05d9c09de6b6511c9b0c35e8f00e1375e684b3f84a67"; userflag=company; SXS_XSESSION_ID="2|1:0|10:1531880807|15:SXS_XSESSION_ID|48:ZjAyNzI0NTYtYTJhYi00YjRlLWFkMGYtZTU1OGU4NzE2OThh|87ab5a1f8555f7dbbbacae30c510c055e7bfc75842456a8f43c4c5befad00ac7"; affefdgx=usr_yglov8iavxyr; SXS_XSESSION_ID_EXP="2|1:0|10:1531880807|19:SXS_XSESSION_ID_EXP|16:MTUzNDQ3MjgwNw==|5f37d54f26f71115fadb8462a3f777c2ea7e600f266699a0f4859f703d2abf75"; MEIQIA_EXTRA_TRACK_ID=17JF0z0rxLHrzun3hmKojCV9fxz; gr_cs1_57cc3437-e85d-4913-9e20-797e6c09a06e=user_id%3Anull; gr_session_id_96145fbb44e87b47_57cc3437-e85d-4913-9e20-797e6c09a06e=true; gr_session_id_96145fbb44e87b47=5d9cca33-8fd2-44e3-808e-792a4ab834e2; Hm_lvt_59802bedd38a5af834100b04592579e2=1531880789,1531905358; Hm_lpvt_59802bedd38a5af834100b04592579e2=1531905358; gr_session_id_96145fbb44e87b47_5d9cca33-8fd2-44e3-808e-792a4ab834e2=true; MEIQIA_VISIT_ID=17YDuEFXd92jqzS7Jak0VQMi5T8; SXS_VISIT_XSESSION_ID_V3.0="2|1:0|10:1531905511|26:SXS_VISIT_XSESSION_ID_V3.0|48:ZjAyNzI0NTYtYTJhYi00YjRlLWFkMGYtZTU1OGU4NzE2OThh|0d4f552f74fe5296028dc0e38f05db60fc3dee6640440954f2a4455ebcc15612"; SXS_VISIT_XSESSION_ID_V3.0_EXP="2|1:0|10:1531905511|30:SXS_VISIT_XSESSION_ID_V3.0_EXP|16:MTUzNDQ5NzUxMQ==|e158607ee0e678f5c72eaf35f30ed79d66771f180643b9133604feab50ca0054"'
cookies_basis_djw = 'DJ_UVID=MTUyODM1OTczNTM4ODcwNjI5; dj_auth_v3=MQB2cB5OeLIdYUJFVSSaeziCdgizDgH8c7LQzBzzsM1a5B7e31P_HpiFsBJTBH4*; dj_auth_v4=ed0ce108c489e4c896c429cb5ddbb0e8_pc; uchome_loginuser=39782118; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0hbE0YNkcedjYI8zbT0DtuObwx0TAkjLOeiKYoFFzTq%26wd%3D%26eqid%3Db0c41e2900033cf1000000045b528709; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; _ssytip=1532135170424; USER_ACTION=request^AProfessional^AAUTO^A-^A-; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1531960239,1531972412,1532058071,1532135169; Hm_lpvt_6822a51ffa95d58bbe562e877f743b4f=1532135172; login_email=3001261262%40qq.com; _ga=GA1.2.1190465485.1531960330; _gid=GA1.2.205178732.1531960330'
cookies_basis_51 = 'guid=15126185243667940069; EhireGuid=57343d4ab9144eeaaac53570c55c6bd5; RememberLoginInfo=member_name=790EDF22D15A367144E78236FFD81B69&user_name=3F6D7EB2B10CC033; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0VmkU00uiAs0aQA-p00000aaJBdb00000X8ZxsW.THLZ_Q5n1VeHksK85ydEUhkGUhNxndqbusK15y7-uj-BP1fdnj0snvnzrjn0IHY4fW0knHI7wWRsrj-KwD7KwRDYnbfdn1n3rDwaP1Naw0K95gTqFhdWpyfqn10LP1T4PWbLPiusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqPHnzPWb%2526tpl%253Dtpl_10085_16624_12226%2526l%253D1502325280%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m4b66f41d%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D233%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dmonline_3_dg%2526inputT%253D4274%26%7C%26adsnum%3D789233; LangType=Lang=&Flag=1; 51job=cuid%3D52237061%26%7C%26cusername%3D13598213097%26%7C%26cpassword%3D%26%7C%26cname%3D%25D1%25EE%25D2%25F8%25B2%25A8%26%7C%26cemail%3D455471846%2540qq.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0g4r6HYlhTBg%26%7C%26cconfirmkey%3D4555sQmuzH7DE%26%7C%26cresumeids%3D.0Sy8EEE7wagc%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D45usYTv%252FFNEs.%26%7C%26to%3DXmMBaANjCz5cOlo2UTJRYwxzBjYANVU1AT5dNwE5BTQNNlA7D2QLOlF8XTALa1ViBT9UZQM0AWRdYlQ%252BATI%253D%26%7C%26; ps=us%3DXGUCawBgVn4CYVg2B2dXegIzBjVWYwZ9VWIBag0zBXkLMgBuUzALOgJnXzRRMAA7Vm0BOQA2UDJdY1Z4D0QANFxhAjEAFw%253D%253D%26%7C%26needv%3D0; _ujz=NTIyMzcwNjEw; AccessKey=d45a0618ef944d1; partner=baidupz; slife=lastlogindate%3D20180209%26%7C%26; ASP.NET_SessionId=tnj5cjfsmtf5h2nf3avtcvrc; HRUSERINFO=CtmID=2424128&DBID=2&MType=02&HRUID=2788355&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=hzjl340&IsStandard=0&LoginTime=02%2f09%2f2018+09%3a01%3a32&ExpireTime=02%2f09%2f2018+09%3a11%3a32&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=bf9abebe61bef674; KWD=SEARCH='


def get_cook_str(cookfile, hostKey, cook_yb):
    cookieFile = cookfile

    LocalFree = windll.kernel32.LocalFree
    memcpy = cdll.msvcrt.memcpy
    CryptProtectData = windll.crypt32.CryptProtectData
    CryptUnprotectData = windll.crypt32.CryptUnprotectData
    CRYPTPROTECT_UI_FORBIDDEN = 0x01

    class DATA_BLOB(Structure):
        _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

    def getData(blobOut):
        cbData = int(blobOut.cbData)
        pbData = blobOut.pbData
        buffer = c_buffer(cbData)
        memcpy(buffer, pbData, cbData)
        LocalFree(pbData)
        return buffer.raw

    def encrypt(plainText):
        bufferIn = c_buffer(plainText, len(plainText))
        blobIn = DATA_BLOB(len(plainText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptProtectData(byref(blobIn), u"python_data", None,
                            None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to encrypt data")

    def decrypt(cipherText):
        bufferIn = c_buffer(cipherText, len(cipherText))
        blobIn = DATA_BLOB(len(cipherText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to decrypt data")

    # 获取cookies，此处cookies需要保存在本地
    conn = sqlite3.connect(cookieFile)
    c = conn.cursor()
    sql = "select host_key, name, value, path,encrypted_value from cookies where host_key like \'%" + hostKey + "%\'"
    c.execute(sql)
    cookies = c.fetchall()
    # print(cookies)
    # print(len(cookies))
    c.close()
    # 加工cookies成字符串
    cookies_list = []
    cookies_all_list = []
    cookies_name_list = []
    cookies_str_zl = cook_yb
    cookies_list0 = cookies_str_zl.split(';')

    for cookie in cookies_list0:
        cookies_name = cookie.split('=')[0].strip()
        cookies_name_list.append(cookies_name)

    cookies_str_list = []
    for row in cookies:
        dc = decrypt(row[4])
        cookie_one2 = str(row[1]) + '=' + str(dc, encoding='utf-8')
        cookies_all_list.append(cookie_one2)
        if str(row[1]) in cookies_name_list:
            cookies_dict = {}
            cookies_dict['domain'] = str(row[0])
            cookies_dict['name'] = str(row[1])
            cookies_dict['value'] = str(dc, encoding='utf-8')
            cookies_dict['path'] = '/'
            cookies_dict['httpOnly'] = False
            cookies_dict['HostOnly'] = False
            cookies_dict['Secure'] = False
            str_cook = str(row[1]) + '=' + str(dc, encoding='utf-8')
            cookies_str_list.append(str_cook)
    cookies_str = ';'.join(cookies_str_list)
    return cookies_str
def parse_font_xml_58(font_xml_file):
    xml = etree.parse(font_xml_file)
    root = xml.getroot()
    font_dict = {}
    all_data = root.xpath('//glyf/TTGlyph')
    for index, data in enumerate(all_data):
        font_key = data.attrib.get('name')[3:].lower()
        contour_list = []
        if index == 0:
            continue
        for contour in data:
            for pt in contour:
                contour_list.append(dict(pt.attrib))
        font_dict[font_key] = json.dumps(contour_list, sort_keys=True)
    return font_dict
def handl_58_font(sess, url):
    xz_font_file = True
    retry_t = 0
    while xz_font_file:
        # user_agent = random.choice(USER_AGENTS)
        # cookies_str = get_cook_str(cookfile, hostKey='.58.com', cook_yb=cookies_basis_58)
        # headers = {'User-Agent': user_agent,
        #            "Cookie": cookies_str,
        #            'Accept-Encoding': 'gzip, deflate',
        #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        #            'Connection': 'keep-alive',
        #            'Cache-Control	': 'max-age=0',
        #            # 'Content-Length': '14',
        #            # 'Origin': 'https://rdsearch.zhaopin.com',
        #            # 'Content-Type': 'application/x-www-form-urlencoded',
        #            # 'Referer': 'https://rdsearch.zhaopin.com/home/RedirectToRd/qzUBjcckExs7P1ZJLKxLJQ_1_1?searchresume=1',
        #            # 'Upgrade-Insecure-Requests': '1',
        #            'Host': 'jianli.58.com',
        #            }
        r = sess.get(url)
        r.encoding = 'utf-8'
        text = r.text
        # print(r.text)
        file_path = os.getcwd() + os.sep + 'font1'
        # print(file_path)
        if not os.path.exists(file_path):
            print('文件夹', file_path, '不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(file_path)
        else:
            shutil.rmtree(file_path)
            os.makedirs(file_path)
        sel = Selector(text=text)
        stonefont_url = sel.xpath('//style[not(@*)]').extract()[0]  # 报错：<h1>您好，此求职者暂不对外公开简历！<br>请您查看其他简历</h1>
        # print(999, stonefont_url)
        file_name = file_path + os.sep + 'all.txt'
        # 把字体文件的下载链接保存在本地
        try:
            with open(file_name, 'a+') as f:
                if '.eot' in stonefont_url:
                    continue
                elif 'data:application/font-woff' in stonefont_url:
                    stonefont_url = stonefont_url.split('font-family:"customfont"; src:url(')[1].split(')')[0]
                    f.write(stonefont_url + '\n')
                else:
                    print(stonefont_url)
                    print('请注意，出现新字体。。。')
            xz_font_file = False
            if stonefont_url:
                fontwoff_name = file_path + os.sep + '1.woff'
                fontxml_name = file_path + os.sep + '1_1.xml'
                urllib.request.urlretrieve(stonefont_url, fontwoff_name)
                # 整个if下部分为解析字体文件
                font = TTFont(fontwoff_name)
                # print('font对象：', font)
                font.saveXML(fontxml_name)
                # fontxml_name = '1532069096795_1.xml'
                font_dic = parse_font_xml_58(fontxml_name)
                # print(font_dic)
                # print(len(font_dic))
                final_font_dic = {}
                for font_dic_k, font_dic_v in font_dic.items():
                    # print(font_dic_k)
                    font_dic_v_li = json.loads(font_dic_v)
                    # print(font_dic_v_li)
                    # print(type(font_dic_v_li))
                    font_diff_num = 0
                    for pos_x_y_on in font_dic_v_li[:-1]:
                        pos_x = int(pos_x_y_on['x'])
                        pos_y = int(pos_x_y_on['y'])
                        pos_on = int(pos_x_y_on['on'])
                        font_diff_num = font_diff_num + (pos_x + pos_y) * pos_on
                    final_font_dic[font_dic_k] = font_diff_num
                    # print('***'*100)
                # print(final_font_dic)
                re_font = r"&#x([0-9a-f]+?);"
                pattern_font = re.compile(re_font)
                font_code_set = set(pattern_font.findall(text))
                font_dic_58 = {25854: 'B', 17310: 'E', 108282: '黄', 44164: '本', 66521: '经', 79735: '硕', 88359: '校',
                               70005: '张', 72807: '杨', 42824: '中', 27285: '大', 69694: '周', 10749: '1', 49259: '生',
                               11443: '7', 18005: '9', 34404: '王', 39469: 'M', 18441: '4', 83428: '技', 20662: '6',
                               77766: '验', 10966: '0', 18042: '5', 86743: '陈', 27620: '士', 69296: '届', 73616: '科',
                               20376: 'A', 36126: '女', 22483: '8', 50789: '应', 75136: '赵', 52577: '吴', 48986: '无',
                               17040: '2', 56307: '刘', 26615: '下', 23514: '3', 53960: '专', 146442: '博', 67457: '李',
                               71089: '高', 39944: '以', 72974: '男'}
                for font_code in font_code_set:
                    sub_before = "&#x" + font_code + ";"
                    text = text.replace(sub_before, font_dic_58[final_font_dic[font_code]])
                # print(text)
                return text
        except:
            traceback.print_exc()
            time.sleep(random.uniform(3, 5))
            retry_t = retry_t + 1
            if retry_t >= 10:
                xz_font_file = False
def jx_58(text_58, job_id='', org_id='111', lx=0, channel_id='',dt=''):
    # print(text_58)
    # driver.get(url_58)
    sel = Selector(text=text_58)
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    data_58_ss_sjx = {}
    data_58_ss_sjx['info'] = {}
    data_58_ss_sjx['objective'] = {}
    xpath_name = '//span[@id="name"]/text()'
    xpath_sex = '//span[@class="sex stonefont"]/text()'
    xpath_aage = '//span[@class="age stonefont"]/text()'
    xpath_degree = '//span[@class="edu stonefont"]/text()'
    xpath_work_year = '//div[@class="base-detail"]/span[@class="stonefont"]/text()'
    xpath_salary = '//span[@class="title" and text()="期望薪资："]/parent::p[@class="stonefont"]/text()'
    try:
        re_phone = r'"phoneProtect":.*?"number":"(\d{11})"'
        patt_phone = re.compile(re_phone)
        phone_li = patt_phone.findall(text_58)
        data_58_ss_sjx['info']['mobilephone'] = phone_li[0]
    except:
        pass


    data_58_ss_sjx['info']['name'] = sel.xpath(xpath_name).extract()[0].strip()
    data_58_ss_sjx['info']['sex'] = sel.xpath(xpath_sex).extract()[0].strip()
    birth_str = sel.xpath(xpath_aage).extract()[0].strip()
    data_58_ss_sjx['info']['birth_year'] = int(now_year) - int(birth_str.split('岁')[0])
    data_58_ss_sjx['info']['degree'] = sel.xpath(xpath_degree).extract()[0].strip()
    wy_str = sel.xpath(xpath_work_year).extract()[0].strip()
    if '-' in wy_str:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year) - int(wy_str.split('年')[0].split('-')[1])
    # 一年以下工作经验
    elif '以下' in wy_str:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year) - 1
    # 10年以上
    elif '以上' in wy_str:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year) - 10
    # 无经验、应届生
    else:
        data_58_ss_sjx['info']['start_working_year'] = int(now_year)
    if len(sel.xpath(xpath_salary)) == 2:
        try:
            salary_str = sel.xpath(xpath_salary).extract()[1].strip()
            # print(12121212, sel.xpath(xpath_salary).extract()[1].strip())
        except:
            traceback.print_exc()
    else:
        salary_str = sel.xpath(xpath_salary).extract()[0].strip()
    # print(12121212, sel.xpath(xpath_salary))
    if '-' in salary_str:
        data_58_ss_sjx['objective']['expected_salary_lower'] = salary_str.split('-')[0]
        data_58_ss_sjx['objective']['expected_salary_upper'] = salary_str.split('-')[1]
    elif '面议' in salary_str:
        pass
        # data_58_ss_sjx['objective']['expected_salary_lower'] = 0
        # data_58_ss_sjx['objective']['expected_salary_upper'] = 0
    else:
        # 1000以下
        if '以下' in salary_str:
            data_58_ss_sjx['objective']['expected_salary_lower'] = 1000
            data_58_ss_sjx['objective']['expected_salary_upper'] = 1000
        #  25000以上
        elif '以上' in salary_str:
            data_58_ss_sjx['objective']['expected_salary_lower'] = 25000
            data_58_ss_sjx['objective']['expected_salary_upper'] = 25000

    re_jlid = r'"bizId":(\d+)'
    patt_jlid = re.compile(re_jlid)
    jlid_li = patt_jlid.findall(text_58)
    if jlid_li[0] != '0':
        data_58_ss_sjx['info']['channel_resume_id'] = jlid_li[0]
    else:
        if channel_id:
            data_58_ss_sjx['info']['channel_resume_id'] = channel_id

    # data_58_ss_sjx['info']['channel_resume_id'] = driver.current_url.split('https://jianli.58.com/resumedetail/singles/')[1].split('?')[0]
    # print(1111111, data_58_ss_sjx['info']['channel_resume_id'])
    data_58_ss_sjx['info']['photo_url'] = sel.xpath('//div[@class="basicInfo"]/div[@class="headFigure"]/img/@src').extract()[0]

    if dt:
        data_58_ss_sjx['info']['channel_update_time'] = dt
    data_58_ss_sjx['info']['channel'] = 3
    # 户籍
    if sel.xpath('//div[@class="base-detail"]/span[9]'):
        if '现居' in sel.xpath('//div[@class="base-detail"]/span[9]/text()').extract()[0]:
            data_58_ss_sjx['info']['current_address'] = \
            sel.xpath('//div[@class="base-detail"]/span[9]/text()').extract()[0].replace('现居', '')
        else:
            data_58_ss_sjx['info']['residence_address'] = \
            sel.xpath('//div[@class="base-detail"]/span[9]/text()').extract()[0].replace('人', '')
            # print(data_58_ss_sjx['info']['residence_address'])
    # 现在居住地
    if sel.xpath('//div[@class="base-detail"]/span[11]'):
        data_58_ss_sjx['info']['current_address'] = sel.xpath('//div[@class="base-detail"]/span[11]/text()').extract()[
            0].replace('现居', '')
        # print(data_58_ss_sjx['info']['current_address'])
    # 高亮最上方标签
    if sel.xpath('//ul[@class="highLights"]/li'):
        data_58_ss_sjx['objective']['individual_label'] = []
        for bq in sel.xpath('//ul[@class="highLights"]/li'):
            data_58_ss_sjx['objective']['individual_label'].append(bq.xpath('text()').extract()[0])
        # print(data_58_ss_sjx['objective']['individual_label'])
    # 工作状态
    data_58_ss_sjx['objective']['work_status'] = sel.xpath('//div[@id="Job-status"]/text()').extract()[0].strip()
    # print(data_58_ss_sjx['objective']['work_status'])
    # 求职名称
    data_58_ss_sjx['objective']['expected_job_title'] = sel.xpath('//div[@id="expectJob"]/text()').extract()[0].split('、（')[0].strip().split('、')
    # 期望工作地点
    data_58_ss_sjx['objective']['expected_address'] = sel.xpath('//div[@id="expectLocation"]/text()').extract()[0].split('、（')[0].strip().split('、')

    # 工作经历
    data_58_ss_sjx['jobs'] = []

    if sel.xpath('//div[@class="work experience"]/div[@class="experience-detail"]'):
        for work in sel.xpath('//div[@class="work experience"]/div[@class="experience-detail"]'):
            job = {}
            job['company'] = work.xpath('div[@class="itemName"]/text()').extract()[0]
            text_wk = work.xpath('string(div[@class="project-content"])').extract()[0].strip()
            if '工作时间' in text_wk:
                gzsj = text_wk.split('工作时间：')[1].split('薪资水平：')[0].split('在职职位：')[0].split('工作职责：')[0].strip()
                if '至今' not in gzsj:
                    job['during_start'] = gzsj.split('-')[0].replace('年', '-').replace('月', '-') + '01'
                    job['during_end'] = gzsj.split('-')[1].split('（')[0].replace('年', '-').replace('月', '-') + '01'
                else:
                    job['during_start'] = gzsj.split('-')[0].replace('年', '-').replace('月', '-') + '01'
                    job['during_end'] = '9999-01-01'
            if '薪资水平' in text_wk:
                job_xz = text_wk.split('薪资水平：')[1].split('工作时间：')[0].split('在职职位：')[0].split('工作职责：')[0].strip()
                if '以下' in job_xz:
                    job['monthly_salary_lower'] = 1000
                    job['monthly_salary_upper'] = 1000
                elif '以上' in job_xz:
                    job['monthly_salary_lower'] = 25000
                    job['monthly_salary_upper'] = 25000
                elif '-' in job_xz:
                    job['monthly_salary_lower'] = int(job_xz.split('-')[0])
                    job['monthly_salary_upper'] = int(job_xz.split('-')[1])
                else:
                    pass
                    # job['monthly_salary_lower'] = 0
                    # job['monthly_salary_upper'] = 0
            if '在职职位' in text_wk:
                job['job_title'] = text_wk.split('在职职位：')[1].split('工作时间：')[0].split('薪资水平：')[0].split('工作职责：')[
                    0].strip()
            if '工作职责' in text_wk:
                job['job_content'] = text_wk.split('工作职责：')[1].split('在职职位：')[0].split('工作时间：')[0].split('薪资水平：')[
                    0].strip()
            data_58_ss_sjx['jobs'].append(job)
        # print(data_58_ss_sjx['jobs'])

    # 教育经历
    data_58_ss_sjx['educations'] = []

    if sel.xpath('//div[@class="education experience"]'):
        for jy in sel.xpath('//div[@class="education experience"]/div[@class="edu-detail"]'):
            edu = {}
            edu['school'] = jy.xpath('div/span[1]/text()').extract()[0].strip()
            if '月毕业' in jy.xpath('div/span[3]/text()').extract()[0]:
                edu['during_end'] = jy.xpath('div/span[3]/text()').extract()[0].strip().split('月毕业')[0].replace('年',
                                                                                                                '-') + '-01'
            else:
                edu['during_end'] = '9999-01-01'
            edu['major'] = jy.xpath('div[@class="item-content"]/span[@class="professional"]/text()').extract()[
                0].strip()
            data_58_ss_sjx['educations'].append(edu)
        # print(data_58_ss_sjx['educations'])

    # 技能语言
    data_58_ss_sjx['languages'] = []
    # 语言
    if sel.xpath('//div[@class="language experience"]'):
        for la in sel.xpath('//div[@class="language experience"]/div[@class="edu-detail"]'):
            lang = {}
            all_text = la.xpath('string(div[@class="item-content"])').extract()[0].strip()
            lang['language'] = all_text.split('： ')[0]
            lang_text1 = all_text.split('： ')[1].split('| ')[0]
            lang_text2 = all_text.split('： ')[1].split('| ')[1]
            lang_len = len(all_text.split('： ')[1].split('| '))
            if lang_len == 3:
                lang['level'] = all_text.split('： ')[1].split('| ')[2]
            if '听' in lang_text1:
                lang['speaking'] = lang_text1.replace('听说', '')
                lang['writing'] = lang_text2.replace('读写', '')
            else:
                lang['speaking'] = lang_text2.replace('听说', '')
                lang['writing'] = lang_text1.replace('读写', '')
            data_58_ss_sjx['languages'].append(lang)
    # 技能
    if sel.xpath('//div[@class="skillList experience"]'):
        for jn in sel.xpath('//div[@class="skillList experience"]/div[@class="certificate-item"]'):
            skill = {}
            skill['skill'] = jn.xpath('span[1]/text()').extract()[0]
            skill['duration'] = jn.xpath('span[3]/text()').extract()[0].split('（')[1].split('）')[0].strip()
            skill['level'] = jn.xpath('span[3]/text()').extract()[0].split('（')[0].strip()
            data_58_ss_sjx['languages'].append(skill)
        # print(data_58_ss_sjx['languages'])
    # 自我评价
    if sel.xpath('//div[@class="aboutMe experience"]'):
        text_me = sel.xpath('string(//div[@class="aboutMe experience"]/div[@class="edu-detail"])').extract()[0].strip()
        data_58_ss_sjx['objective']['self_evaluation'] = text_me
        # print(data_58_ss_sjx['objective']['self_evaluation'])

    # 项目经验
    data_58_ss_sjx['projects'] = []

    if sel.xpath('//div[@class="project experience"]'):
        for pro in sel.xpath('//div[@class="project experience"]/div[@class="experience-detail"]'):
            pro_dic = {}
            pro_dic['title'] = pro.xpath('div[@class="itemName"]/text()').extract()[0]
            pro_text = pro.xpath('string(div[@class="project-content"])').extract()[0].strip()
            xmsj = pro_text.split('项目时间：')[1].split('项目简介：')[0].split('项目业绩：')[0]
            if '至今' not in xmsj:
                pro_dic['during_start'] = xmsj.split('-')[0].strip().replace('年', '-').replace('月', '-') + '01'
                pro_dic['during_end'] = xmsj.split('-')[1].strip().replace('年', '-').replace('月', '-') + '01'
            else:
                pro_dic['during_start'] = xmsj.split('-')[0].strip().replace('年', '-').replace('月', '-') + '01'
                pro_dic['during_end'] = '9999-01-01'
            pro_dic['description'] = pro_text.split('项目简介：')[1].split('项目时间：')[0].split('项目业绩：')[0].strip()
            pro_dic['duty'] = pro_text.split('项目业绩：')[1].split('项目时间：')[0].split('项目简介：')[0].strip()
            data_58_ss_sjx['projects'].append(pro_dic)
        # print(data_58_ss_sjx['projects'])

    # 证书
    data_58_ss_sjx['credentials'] = []

    if sel.xpath('//div[@class="medal experience"]'):
        for zs in sel.xpath('//div[@class="medal experience"]/div[@class="certificate-item"]'):
            zs_dic = {}
            zs_dic['title'] = zs.xpath('span[@class="certificate-name auto_hidden"]/text()').extract()[0].strip()
            zs_dic['get_date'] = zs.xpath('span[@class="certificate-time"]/text()').extract()[0].strip().replace('年',
                                                                                                                 '-').replace(
                '月', '-') + '01'
            data_58_ss_sjx['credentials'].append(zs_dic)
        # print(data_58_ss_sjx['credentials'])

    # 在校情况
    data_58_ss_sjx['at_schools'] = []
    if sel.xpath('//div[@class="school experience"]'):
        for sch in sel.xpath('//div[@class="school experience"]/div[@class="experience-detail"]'):
            sch_dic = {}
            for sch_con in sch.xpath('div[@class="project-content"]/div[@class="title-content"]'):
                if '获奖学金' in sch_con.xpath('div[@class="item-title"]/text()').extract()[0].strip():
                    sch_dic['scholarship'] = sch_con.xpath('string(div[@class="item-content"])').extract()[0].strip()
                if '活动奖项' in sch_con.xpath('div[@class="item-title"]/text()').extract()[0].strip():
                    sch_dic['prize'] = \
                    sch_con.xpath('string(div[@class="item-content"]/p[@class="award-name"])').extract()[0].strip()
                if '校内职务' in sch_con.xpath('div[@class="item-title"]/text()').extract()[0].strip():
                    sch_dic['campus_post'] = \
                    sch_con.xpath('string(div[@class="item-content"]/p[@class="job"])').extract()[0].strip()
            data_58_ss_sjx['at_schools'].append(sch_dic)
        # print(data_58_ss_sjx['at_schools'])
    # 培训经历----没找到
    data_58_ss_sjx['trainings'] = []
    data_58_ss_sjx['org'] = {}
    try:
        if sel.xpath('//div[@id="divHead"]/table/tbody/tr[1]/td[1]/span[3]/text()').extract()[0]:
            data_58_ss_sjx['org']['receive_time'] = \
            sel.xpath('//div[@id="divHead"]/table/tbody/tr[1]/td[1]/span[3]/text()').extract()[0]
    except:
        pass


    data_58_ss_sjx['org']['org_id'] = org_id
    data_58_ss_sjx['org']['receive_time'] = str(datetime.datetime.now())[0:10]
    # 插件
    if lx == 3:
        data_58_ss_sjx['org']['resume_type'] = 3
    # 搜索/推荐
    elif lx == 1:
        data_58_ss_sjx['org']['resume_type'] = 1
    # 收件箱
    elif lx == 2:
        data_58_ss_sjx['org']['resume_type'] = 2
    if job_id:
        data_58_ss_sjx['org']['job_id'] = job_id
    # 插件无职业，搜索职业为遇仁，收件箱职业是渠道
    try:
        if data_58_ss_sjx['info']['mobilephone']:
            data_58_ss_sjx['org']['download_status'] = 1
    except:
        data_58_ss_sjx['org']['download_status'] = 0
    if dt:
        data_58_ss_sjx['org']['delivery_time'] = dt
    # print(data_58_ss_sjx)
    return data_58_ss_sjx
def push_58(dic, cookies, get_num):
    t = time.time()
    resume_url_li = []
    resume_id_li = []
    # def first_get(dic, cookies):
    page_url = 'https://employer.58.com/resumesearch'
    with requests.session() as sess:
        sess.headers = {'User-Agent': get_useragent(), 'x-requested-with': 'XMLHttpRequest',
                        'referer': 'https://employer.58.com/resumesearch?'}
        sess.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None,
                                                          overwrite=True)
        xx = sess.get(page_url)
        fontkey = re.findall('fontKey: "(.+)"', xx.text)
        # print(fontkey[0])
        dic['fontKey'] = fontkey[0]
        # dic['fontKey'] = 'jQuery180032332760681241046_1541668708763'
        dic['callback'] = 'jQuery18005397851186043843_' + str(int(time.time() * 1000))
        time.sleep(5)
        dic['_'] = str(int(time.time() * 100))
        dic['pageindex'] = 1
        search_url = 'https://employer.58.com/resume/searchresume?' + parse.urlencode(dic)
        # print(search_url)
        yy = sess.get(search_url)
        # print(yy.text)
        yy_data_str = yy.text.split('(', 1)[1][:-1]
        yy_data_dic = json.loads(yy_data_str)
        all_num = int(yy_data_dic['data']['count'])
        all_resume = yy_data_dic['data']['resumeList']
        every_page_num = len(all_resume)
        today_str = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        print(today_str)
        ys = all_num % every_page_num
        if ys != 0:
            cs = int(all_num / every_page_num) + 1
        else:
            cs = int(all_num / every_page_num)
        # print(666)
        for i in range(1, cs + 1):
            print('第{}页'.format(i))
            dic['pageindex'] = i
            dic['callback'] = 'jQuery18005397851186043843_' + str(int(time.time() * 1000))
            time.sleep(5)
            dic['_'] = str(int(time.time() * 100))
            search_url = 'https://employer.58.com/resume/searchresume?' + parse.urlencode(dic)
            yy = sess.get(search_url)
            yy_data_str = yy.text.split('(', 1)[1][:-1]
            yy_data_dic = json.loads(yy_data_str)
            # print(yy_data_dic)
            all_resume = yy_data_dic['data']['resumeList']
            for resume_1 in all_resume:
                # print(resume_1['updateDate'])
                if resume_1['updateDate'] == today_str and len(resume_url_li) < get_num:
                    resume_id = resume_1['resumeID']
                    # print(resume_id)
                    resume_url = resume_1['url']
                    resume_url_li.append(resume_url)
                    resume_id_li.append(resume_id)
                    # break
                elif len(resume_url_li) >= get_num:
                    break
            if len(resume_url_li) >= get_num:
                break
        for index_i, i in enumerate(resume_url_li):
            time.sleep(6)
            print(index_i)
            if not i.startswith('https:'):
                i = 'https:' + i
            # resume_cont = self.session.get(i)
            try:
                text_58 = handl_58_font(sess, i)
                resume_58 = jx_58(text_58)
            except:
                pass
            # print(resume_58)
        print(time.time() - t)
        # print()
dic = {}
# dic['dsid'] = 13139
# dic['cateid'] = 13352
# dic['exper'] = 1
dic['workabove'] = 0
# dic['education'] = 4
dic['eduabove'] = 0
# dic['age'] = 3
# dic['sex'] = -1
# dic['salary'] = 5
dic['cid'] = 1
dic['aid'] = -1
dic['nid'] = -1
dic['update'] = 1
dic['update24Hours'] = 1
# dic['pageindex'] = 1
dic['pc'] = 0
dic['mc'] = 0
dic['keyword'] = '销售'
dic['resumeSort'] = 'intelligent'
cookies_str_58 = get_cook_str(cookfile, '.58.com', cookies_basis_58)
push_58(dic, cookies_str_58, 300)

