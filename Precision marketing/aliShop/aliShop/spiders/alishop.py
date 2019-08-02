# -*- coding: utf-8 -*-
import scrapy
from aliShop.config import get_dict,XH_REQ
import logging
from urllib import parse
from urllib.request import quote
from aliShop.settings import DEFAULT_REQUEST_HEADERS
from aliShop.items import AlishopItem
from scrapy import Selector


class AlishopSpider(scrapy.Spider):
    name = 'alishop'
    allowed_domains = ['1688.com']
    start_urls = ['http://1688.com/']
    list_meta = get_dict(r'table\meta.json')

    def parse(self, response):
        '''按城市、类别分别创建url'''

        for index, dict_meta in enumerate(self.list_meta[100:500]):
            logging.info('{}:{}'.format(index, dict_meta))
            keywords=quote((dict_meta['SecondCate']+' '+dict_meta['ThirdCate']).encode('gbk'))
            province=quote((dict_meta['province']).encode('gbk'))
            city=quote((dict_meta['city']).encode('gbk'))
            params_search = {
                'filt':'y',
                'n': 'y',
                'netType': '1,11',
                'pageSize': '30',
                'offset': '3',
            }
            url_basic='https://s.1688.com/company/company_search.htm?keywords={}&province={}&city={}&'.format(keywords,province,city)
            url_search=url_basic+parse.urlencode(params_search)
            try:
                totalPage = self.totalPage(url=url_search, dict_meta=dict_meta)
                logging.info('【{}】共：{}页'.format(url_search,totalPage))
                for page in range(1,totalPage+1):
                    url_referer=url_search+'&beginPage={}'.format(str(page))
                    dict_meta['urlReferer'] = url_referer
                    print(url_referer)
                    yield scrapy.Request(url=url_referer,meta=dict_meta,callback=self.parse_search,priority=10)
            except:
                continue

    def parse_search(self,response):
        meta=response.meta
        sel = Selector(text=response.text)
        for company_item in sel.xpath('//li[@class="company-list-item"]'):
            dict_shop=self.jixi(company_item)
            dict_shop['FirstCate']=meta['FirstCate']
            dict_shop['SecondCate']=meta['SecondCate']
            dict_shop['ThirdCate']=meta['ThirdCate']
            dict_shop['province']=meta['province']
            dict_shop['city']=meta['city']
            dict_shop['urlReferer']=meta['urlReferer']
            logging.info(dict_shop['shopLink'])
            item = AlishopItem()
            item=self.shop_info(item,dict_shop)
            yield item

    def shop_info(self,item,meta):

        item['_id']=meta['_id']
        item['province']=meta['province']
        item['city']=meta['city']
        item['FirstCate']=meta['FirstCate']
        item['SecondCate']=meta['SecondCate']
        item['ThirdCate']=meta['ThirdCate']
        item['companyName']=meta['companyName']
        item['shopName']=meta['shopName']
        item['shopLink']=meta['shopLink']
        item['locArea']=meta['locArea']
        item['itemId']=meta['itemId']
        item['honestyMember']=meta['honestyMember']
        item['honestyYear']=meta['honestyYear']
        item['tipTitle']=meta['tipTitle']
        item['mainProduct']=meta['mainProduct']
        item['processingMethods']=meta['processingMethods']
        item['companyNumber']=meta['companyNumber']
        item['factoryArea']=meta['factoryArea']
        item['certificate']=meta['certificate']
        item['factoryReport']=meta['factoryReport']
        item['hotProduct']=meta['hotProduct']
        item['businessModel']=meta['businessModel']
        item['urlReferer']=meta['urlReferer']
        
        return item

    def jixi(self,company_item):

        dict_shop = {}
        dict_shop['shopLink'] = \
        company_item.xpath('string(div/div/div[@class="list-item-title"]/a/@href)').extract()[0].strip()
        dict_shop['_id']=dict_shop['shopLink'].split('//')[1].split('.1688.com')[0].strip()
        dict_shop['companyName'] = \
        company_item.xpath('string(div/div/div[@class="list-item-title"]/a/@title)').extract()[0].strip()
        dict_shop['shopName'] = company_item.xpath('string(div/div/div[@class="list-item-icons"]/span)').extract()[
            0].replace('｜', '').strip()
        dict_shop['itemId'] = company_item.xpath('string(@itemid)').extract()[0].strip()  # 旺旺id

        if '阿里巴巴建议您优先选择诚信通会员' in company_item.extract():
            dict_shop['honestyMember'] = '1'  # 诚信通会员
        else:
            dict_shop['honestyMember'] = '0'
        dict_shop['tipTitle'] = []
        dict_shop['honestyYear'] = '0'
        for title in company_item.xpath('div/div/div[@class="list-item-icons"]/a'):
            tip_title = title.xpath('string(@title)').extract()[0].strip()
            if '诚信通会员' in tip_title:
                dict_shop['honestyYear'] = title.xpath('string(em)').extract()[0].strip()
                continue
            if '先行赔付' in tip_title:
                tip_title = '先行赔付'
            elif '实力商家' in tip_title:
                tip_title = '实力商家'
            dict_shop['tipTitle'].append(tip_title)

        try:
            mainProduct = \
            company_item.xpath('string(div/div/div[@class="list-item-detail"]/div/div[1]/a)').extract()[0].strip()
            dict_shop['mainProduct'] = mainProduct.replace('\n', '').replace(' ', '')
        except:
            dict_shop['mainProduct'] = ''

        try:
            dict_shop['locArea'] = \
            company_item.xpath('string(div/div/div[@class="list-item-detail"]/div/div[2]/a/@title)').extract()[
                0].strip()
        except:
            dict_shop['locArea'] = ''
        try:
            dict_shop['companyNumber'] = \
            company_item.xpath('string(div/div/div[@class="list-item-detail"]/div/div[3]/a)').extract()[0].replace(
                ' ', '')
        except:
            dict_shop['companyNumber'] = ''
        try:
            dict_shop['certificate'] = company_item.xpath(
                'string(div/div/div[@class="list-item-detail"]/div/div[4]/a[@offer-stat="certificate"]/@href)').extract()[
                0].strip()
        except:
            dict_shop['certificate'] = ''
        try:
            dict_shop['factoryReport'] = company_item.xpath(
                'string(div/div/div[@class="list-item-detail"]/div/div[4]/a[@offer-stat="factory"]/@href)').extract()[
                0].strip()
        except:
            dict_shop['factoryReport'] = ''

        try:
            dict_shop['processingMethods'] = ''
            dict_shop['factoryArea'] = ''
            for detail_right in company_item.xpath(
                    'div/div/div[@class="list-item-detail"]/div[@class="detail-right"]/div'):
                title = detail_right.xpath('string(span)').extract()[0].strip()
                if '经营模式' in title:
                    try:
                        dict_shop['businessModel'] = detail_right.xpath('string(b)').extract()[0].strip()
                    except:
                        dict_shop['businessModel'] = ''
                elif '加工方式' in title:
                    try:
                        dict_shop['processingMethods'] = detail_right.xpath('string(a)').extract()[0].strip()
                    except:
                        dict_shop['processingMethods'] = ''
                elif '厂房面积' in title:
                    try:
                        dict_shop['factoryArea'] = detail_right.xpath('string(a)').extract()[0].strip()
                    except:
                        dict_shop['factoryArea'] = ''
        except:
            pass

        try:
            dict_shop['hotProduct'] = []
            for li in company_item.xpath(
                    'div[@class="list-item-right"]/div/div[@class="list-item-itemsWrap"]/ul/li'):
                try:
                    dict_hot = {}
                    try:
                        if 'data-lazyload-src' in li.extract():
                            dict_hot['picture'] = li.xpath('string(a/img/@data-lazyload-src)').extract()[0].strip()
                        else:
                            dict_hot['picture'] = li.xpath('string(a/img/@src)').extract()[0].strip()
                    except:
                        pass
                    dict_hot['title'] = li.xpath('string(a/img/@alt)').extract()[0].strip()
                    dict_hot['price'] = li.xpath('string(div/span[@class="price"]/@title)').extract()[0].strip()
                    dict_hot['volume'] = li.xpath('string(div/span[@class="volume"]/@title)').extract()[0].strip()
                    dict_shop['hotProduct'].append(dict_hot)
                except:
                    pass
        except:
            pass

        return dict_shop

    def totalPage(self,url,dict_meta):
        try:
            html=XH_REQ(url=url,headers=DEFAULT_REQUEST_HEADERS,data='')
            sel=Selector(text=html)
            if '缩短或修改您的搜索词，重新搜索'in html:
                totalPage=0
            elif '下一页' in html:
                totalPage = sel.xpath('string(//div[@class="page-op"]/span[@class="total-page"])').extract()[0].strip()
                totalPage = int(totalPage.replace('共', '').replace('页', ''))
            else:
                totalPage=1
            return totalPage
        except:
            logging.error('词条获取失败：{}'.format(dict_meta))
            pass


if __name__ == '__main__':
    ttt='''
    
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="GBK">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=GBK" />
<meta http-equiv="Cache-Control" content="no-siteapp" />

<link rel="canonical" href="https://s.1688.com/company/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html"/>
<title>广告服务 广告策划公司_重庆_公司黄页 - 阿里巴巴</title>
<meta name="keywords" content="广告服务 广告策划，广告服务 广告策划公司，广告服务 广告策划工厂，广告服务 广告策划企业，广告服务 广告策划供应商"/>
<meta name="description" content="共找到3条符合广告服务 广告策划的查询结果。您可以在阿里巴巴公司黄页搜索到关于广告服务 广告策划生产商的工商注册年份、员工人数、年营业额、信用记录、相关广告服务 广告策划产品的供求信息、交易记录等企业详情。"/>
<meta name="robots" content="noindex,follow">
<meta name="data-spm" content="b26110380">

<link rel="shortcut icon" href="https://www.1688.com/favicon.ico" />













 <link rel="stylesheet" href="//astyle.alicdn.com/fdevlib/css/lofty/alicn/alitalk/1.0/alitalk.css?_v=ee36a3ae6cb008a8cadbffc330a5cf1f.css" />
  <script type="text/javascript">
 var iSearchPV = {
 'iSubject':[]
 };
 </script>

<script type="text/javascript">
var asyncResource={"searchweb":{"css":[],"js":["//astyle.alicdn.com/??app/search/js/list/cml/appbase/base.min.js,app/search/js/main/common/base/utility-amd.js,app/search/js/list/cml/global/default/pageconfig-amd.js,fdevlib/js/lofty/lang/observer.js,app/search/js/list/cml/global/default/config-amd.js,app/search/js/list/cml/pv/default/pv-amd.js,app/search/js/list/cml/global/default/checkscreensize-amd.js,app/search/js/list/cml/global/default/global-amd.merge.js,app/search/js/list/cml/searchbar/default/searchbar.min.js,app/opensearch/cml/famousshop/pkg-a/js/famousshop.js,app/search/js/list/cml/navigatebar/default/navigatebar.min.js,app/search/js/list/plugins/company/filtbar/default/filtbar.min.js,fdevlib/js/lofty/lang/attribute.js,fdevlib/js/lofty/lang/pluginhost.js,fdevlib/js/lofty/lang/base.js,fdevlib/js/lofty/util/exposure/1.0/exposure.js,fdevlib/js/lofty/util/webp/1.0/webp.js,fdevlib/js/lofty/util/datalazyload/2.0/datalazyload.js,fdevlib/js/lofty/alicn/alitalk/1.0/alitalk.js?_v=9ff0149547c5df6005e2c0ae18e1e0f0.js","//astyle.alicdn.com/??fdevlib/js/lofty/util/misc/2.0/misc.js,app/search/js/list/cml/widget/alitalk-amd.js,fdevlib/js/lofty/util/template/2.0/template.js,app/search/js/list/plugins/company/offerresult/multishop.js,sys/js/searchweb/open/base64util.js,sys/js/searchweb/open/service-v1.js,sys/js/searchweb/twins.js,app/search/js/list/plugins/company/offerresult/offerresult.js,app/search/js/list/plugins/company/offerresult/offerresult.min.js,app/searchweb/common/widget/js/zqx.js,app/search/js/list/plugins/company/bottomp4p/previewcompanydismap.js,fdevlib/js/lofty/util/cookie/1.0/cookie.js,fdevlib/js/lofty/util/template/2.0/runtime.js,app/search/js/list/plugins/company/bottomp4p/views/bottomp4p.art.js,sys/js/searchweb/gemini.js,app/search/js/list/plugins/company/bottomp4p/bottomp4p.js?_v=c9dcc46831afc798bd98d1506572d719.js"]}};
</script>

<link rel="stylesheet" href="//astyle.alicdn.com/??app/search/css/list/cml/appbase/base.min.css,app/search/css/list/plugins/company/common/common.css,app/search/css/list/cml/layout/rightgold/layout.css,app/search/css/list/cml/searchbar/default/rwd.searchbar.min.css,app/search/css/list/cml/breadCrumb/default/breadCrumb.min.css,app/search/css/list/plugins/company/sn/default.css,app/search/css/list/plugins/company/recommendwords/default/recommendwords.min.css,app/search/css/list/plugins/company/filtbar/default/filtbar.min.css,app/search/css/list/plugins/company/offerresult/img/screens/default.min.css,app/search/css/list/plugins/company/bottomp4p/default/bottomp4p.min.css,app/search/css/list/cml/relativewords/default/relativewords.min.css,app/search/css/list/cml/bottomsearch/default/bottomsearch.min.css,app/search/css/list/cml/credit/default/credit.min.css,fdevlib/css/lofty/ui/sidebar/2.0/front/sidebar-min.css?_v=8c7b9f1bdae6f9ecdf1e20dbf111d7b9.css" /></head>

<body data-spm="2178313"><script>
var dmtrack_c='{ali%5fresin%5ftrace%3dc%5fsemi%3d0%7cc%5fnitvtcnt%3d3%7cc%5fsrescnt%3d3%7cc%5fset%3d4%7cc%5fsek%3d%25B9%25E3%25B8%25E6%25B7%25FE%25CE%25F1%2b%25B9%25E3%25B8%25E6%25B2%25DF%25BB%25AE%7cc%5fsep%3d1%7cc%5fsefilter%3d1%7cc%5fsepro%3d%25D6%25D8%25C7%25EC%7cc%5fsecid%3d69%7cc%5fp4pid%3d1564715663335103039155%7cc%5fexp%3dxt%3acompany%5frenqi%2cceg%3afxb%2cpolicyId%3a2000%7cc%5fbid%3d202611%5f1}';
with(document)with(body)with(insertBefore(createElement("script"),firstChild))setAttribute("exparams","category=&userid=&aplus&asid=AQAAAACPqkNdUcxbHwAAAAB+i0+DMbun+A==&aat=&abb=&ret=ali%5fresin%5ftrace%3dc%5fsemi%3d0%7cc%5fnitvtcnt%3d3%7cc%5fsrescnt%3d3%7cc%5fset%3d4%7cc%5fsek%3d%25B9%25E3%25B8%25E6%25B7%25FE%25CE%25F1%2b%25B9%25E3%25B8%25E6%25B2%25DF%25BB%25AE%7cc%5fsep%3d1%7cc%5fsefilter%3d1%7cc%5fsepro%3d%25D6%25D8%25C7%25EC%7cc%5fsecid%3d69%7cc%5fp4pid%3d1564715663335103039155%7cc%5fexp%3dxt%3acompany%5frenqi%2cceg%3afxb%2cpolicyId%3a2000%7cc%5fbid%3d202611%5f1&c_signed=false&hn=search%2dweb2011250157065%2ecenter%2eeu13&at_bu=cbu",id="beacon-aplus",src="//g.alicdn.com/alilog/??/aplus_plugin_b2bfront/index.js,mlog/aplus_v2.js")
</script>
<script type="text/javascript">
function initResponse(){var d,b,a=window.innerWidth||document.documentElement.clientWidth,g=navigator.userAgent.toLowerCase(),h=/(msie) ([\w.]+)/,f=h.exec(g),c;if(f!==null&&f[1]==="msie"){c=f[2];if(c==="8.0"||c==="7.0"||c==="6.0"){a=a+21}}document.body.style.width="";var e=(document.body.className&&document.body.className.indexOf("sw-list-")!=-1);if(a>=1400){d=2}else{if(a>=1280||e){d=1}else{d=0}}switch(d){case 2:b="s-layout-1390";break;case 1:b="s-layout-1190";break;case 0:b="s-layout-990";break;default:b="s-layout-990";break}b=document.body.className+" "+b;document.body.className=b}initResponse();
</script>
<script src="//g.alicdn.com/secdev/pointman/js/index.js" app="1688-default"></script>

		    
	<div id="alibar" class="fd-clr">
	  <div id="alibar-v4">
	    <div class="alibar-container adapt-201486">
	      <div class="mobile">
	        <a href="//3g.1688.com/?tracelog=wireless_alibar">手机版</a>
	      </div>
	      <span class="sayHello">您好，</span>
	      <div class="account-sign-status">
	        <ul>
	          <li class="account-welcome vipInfoBox">
	            <div class="nav-title">
	              <span class="account-id">
	                欢迎来到阿里巴巴
	              </span>
	            </div>
	            <div class="nav-content"></div>
	          </li>
	          <li class="account-msg fd-hide">
	            <a rel="nofollow" href="//work.1688.com/app/messageCenter.htm" title="查看你的消息" target="_blank">消息</a>
	          </li>
	          <li class="account-signin">
	            <a rel="nofollow" href="https://login.1688.com/member/signin.htm?Done=https://my.1688.com/" title="请登录" data-trace="cn_alibar_login" target="_self">请登录</a>
	          </li>
	          <li class="account-signup">
	            <a rel="nofollow" href="//member.1688.com/member/join/enterprise_join.htm" title="免费注册" data-trace="cn_alibar_reg" target="_blank">免费注册</a>
	          </li>
	        </ul>
	      </div>
	      <div class="topnav">
	        <ul>
	          <li class="list-first">
	            <div class="nav-title">
	              <a href="//www.1688.com/" title="阿里巴巴首页" data-trace="cn_alibar_home" target="_blank">1688首页</a>
	            </div>
	          </li>
	          <li class="topnav-myali extra">
	            <div class="nav-title">
	              <a rel="nofollow" class="nav-arrow" href="//work.1688.com/" title="我的阿里" data-trace="cn_alibar_myali" target="_blank">我的阿里</a>
	            </div>
	            <div class="nav-content" style="width:380px">
	              <dl>
	                <dt>
	                  <a rel="nofollow" href="//work.1688.com/#nav/wholesale/wholesale" title="批发进货" data-trace="cn_alibar_myali_pfjh">批发进货</a>
	                </dt>
	                <dd>
	                  <a rel="nofollow" href="//work.1688.com/app/buyList.htm" title="已买到货品" data-trace="cn_alibar_myali_bought">已买到货品</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="https://marketing.1688.com/coupon/buyer_coupon_list.htm" title="优惠券" data-trace="cn_alibar_myali_yhq">优惠券</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//i.crm.1688.com/" title="店铺动态" data-trace="cn_alibar_myali_dpdt">店铺动态</a>
	                </dd>
	              </dl>
	              <dl>
	                <dt>
	                  <a rel="nofollow" href="https://work.1688.com/#nav/purchase/purchase" title="生产采购" data-trace="cn_alibar_myali_sccg">生产采购</a>
	                </dt>
	                <dd>
	                  <a rel="nofollow" href="https://caigou.1688.com/" title="去采购商城" data-trace="cn_alibar_myali_qcgsc">去采购商城</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="https://go.1688.com/buyoffer/post_buy_offer.htm" title="发布询价单" data-trace="cn_alibar_myali_fbxjd">发布询价单</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="https://go.1688.com/bidding/post/post_bidding_invitation.htm" title="发布招标单" data-trace="cn_alibar_myali_fbzbd">发布招标单</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//go.1688.com/product/product_list.htm" title="管理产品目录" data-trace="cn_alibar_myali_glcpml">管理产品目录</a>
	                </dd>
	              </dl>
	              <dl>
	                <dt>
	                  <a rel="nofollow" href="//work.1688.com/home/newIndex.html#nav/sale/sale" title="销售" data-trace="cn_alibar_myali_xs">销售</a>
	                </dt>
	                <dd>
	                  <a rel="nofollow" href="//work.1688.com/app/saleList.htm" title="已卖出货品" data-trace="cn_alibar_myali_sold">已卖出货品</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//work.1688.com/app/orderPost.htm" title="发布供应产品" data-trace="cn_alibar_myali_offer_post">发布供应产品</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="https://work.1688.com/app/orderManage.htm" title="管理供应产品" data-trace="cn_alibar_myali_offer_manage">管理供应产品</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//apps.1688.com/page/freewinportopen.htm" title="管理旺铺" data-trace="cn_alibar_myali_winport">管理旺铺</a>
	                </dd>
	              </dl>
	              <dl>
	                <dt>
	                  <a rel="nofollow" href="//work.1688.com/home/newIndex.html#nav/app" title="应用" data-trace="cn_alibar_myali_yy">应用</a>
	                </dt>
	                <dd>
	                  <a rel="nofollow" href="//view.1688.com/cms/itbu/app/index.html" title="应用市场" data-trace="cn_alibar_myali_yysc">应用市场</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//yy.1688.com/" title="运营服务" data-trace="yyfw_from_syma">运营服务</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//56.1688.com/" title="物流服务" data-trace="cn_alibar_myali_wlfw">物流服务</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//hezuo.1688.com/" title="站点服务" data-trace="cn_alibar_myali_zdfw">站点服务</a>
	                </dd>
	              </dl>
	            </div>
	          </li>
	          <li class="topnav-purchaselist extra topnav-purchaselist-empty">
	            <div class="nav-title">
	              <a rel="nofollow" class="nav-arrow" href="//cart.1688.com/cart.htm" title="进货单" data-trace="cn_alibar_cart" target="_blank"><span>&nbsp;</span>进货单(<em>0</em>)</a>
	            </div>
	            <div class="nav-content">
	              <div class="product-list fd-clr">
	                <p>
	                  进货单中暂未添加任何货品
	                </p>
	              </div>
	              <div class="purchase-info fd-clr">
	                <a class="btn-y" title="查看进货单" href="//cart.1688.com/cart.htm" target="_blank" data-trace="cn_alibar_purchaselist_list">查看进货单</a>
	              </div>
	            </div>
	          </li>
	          <li class="topnav-favorite extra">
	            <div class="nav-title">
	              <a class="nav-arrow" href="//purchase.1688.com/favorites/favorite_shop.htm?tracelog=alibar_2_favorite_shop" title="收藏夹" data-trace="cn_alibar_myali_fav" target="_blank"><span>&nbsp;</span>收藏夹</a>
	            </div>
	            <div class="nav-content">
	              <dl>
	                <dd>
	                  <a rel="nofollow" class="favorite-offer" href="//purchase.1688.com/favorites/favorite_offer.htm?tracelog=alibar_2_favorite_offer" title="收藏的货品">收藏的货品</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" class="favorite-seller" href="//purchase.1688.com/favorites/favorite_shop.htm?tracelog=alibar_2_favorite_shop" title="收藏的供应商">收藏的供应商</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" class="dealed-seller" href="//purchase.1688.com/favorites/trade_shop.htm?tracelog=alibar_2_trade_shop" title="交易过的供应商">交易过的供应商</a>
	                </dd>
	              </dl>
	            </div>
	          </li>
	          <li class="topnav-tp extra">
	            <div class="nav-title">
	              <a rel="nofollow" class="nav-arrow" href="//cxt.1688.com/" title="诚信通服务" data-trace="cn_alibar_cxt" target="_blank">诚信通服务</a>
	            </div>
	            <div class="nav-content">
	              <dl>
	                <dd>
	                  <a rel="nofollow" class="contact-us-new" href="//view.1688.com/cms/promotion/ppcall6188.html"
	                  title="免费联系我们" data-trace="top_alibar_cxt_contact" target="_blank">免费联系我们</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" class="privilege-experience" href="//cxt.1688.com/vip.html" title="特权体验馆" data-trace="top_alibar_cxt_vipexe" target="_blank">特权体验馆</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" class="newmember-application" href="//cxt.1688.com/register.html"
	                  title="新会员申请" data-trace="top_alibar_cxt_newmeber" target="_blank">新会员申请</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" class="oldmember-xufei" href="//cxt.1688.com/xufei.html"
	                  title="老会员续费" data-trace="top_alibar_cxt_oldmember" target="_blank">老会员续费</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" class="special-offer" href="//cxt.1688.com/pro.html"
	                  title="优惠活动" data-trace="top_alibar_cxt_coupon" target="_blank">优惠活动</a>
	                </dd>
	              </dl>
	            </div>
	          </li>
	          <li class="topnav-wsgys extra">
	            <div class="nav-title">
	              <a class="nav-arrow" href="//gys.1688.com" title="我是供应商" data-trace="cn_alibar_supplier" target="_blank">我是供应商</a>
	            </div>
	            <div class="nav-content" style="width:86px">
	              <dl>
	                <dd>
	                  <a rel="nofollow" href="//gys.1688.com/skill.html" title="交易技巧" target="_blank">交易技巧</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//gys.1688.com/story.html" title="成功经验" target="_blank">成功经验</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//gys.1688.com/pro.html" title="热门活动" target="_blank">热门活动</a>
	                </dd>
	              </dl>
	            </div>
	          </li>
	          <li class="topnav-kf extra">
	            <div class="nav-title">
	              <a class="nav-arrow" rel="nofollow" href="//114.1688.com/kf/index.html?tracelog=kf_2012_budian_shouyetongyi" title="客服中心" target="_blank">客服中心</a>
	            </div>
	            <div class="nav-content">
	              <dl>
	                <dd>
	                  <a rel="nofollow" href="//114.1688.com/newbie/index.htm?tracelog=kf_2012_budian_shouyetongyi1" title="新手入门" target="_blank">新手入门</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//114.1688.com/kf/question/mjbz.html?tracelog=kf_2012_budian_shouyetongyi2" title="买家帮助" target="_blank">买家帮助</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//114.1688.com/kf/aliwall.html?kf_2012_budian_shouyetongyi3" title="卖家帮助" target="_blank">卖家帮助</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//page.1688.com/html/help_pop.html" title="在线咨询" target="_blank">在线咨询</a>
	                </dd>
	                <dd>
	                  <a rel="nofollow" href="//114.1688.com/kf/contact.html" title="联系客服" target="_blank">联系客服</a>
	                </dd>
	              </dl>
	            </div>
	          </li>
	          <li class="topnav-sitemap extra new-sitemap">
	            <div class="nav-title">
	              <a class="nav-arrow" href="//114.1688.com/sitemap.html" title="网站导航" data-trace="cn_alibar_allservice" target="_blank">网站导航</a>
	            </div>
	            <style>
	              #alibar #alibar-v4 .topnav-sitemap .zone .spacing {
	              margin: 0 12px !important;
	              }
	              #alibar #alibar-v4 .topnav-sitemap .zone .detail {
	              width: 352px !important;
	              }
	            </style>
	            <div class="nav-content" style="width:450px;">
	              <div class="hangye-category">
	                <dl class="zone fd-clr">
	                  <dt class="name">行业市场</dt>
	                  <dd class="detail">
	                    <span><a rel="nofollow" href="//fuzhuang.1688.com/" title="服装内衣">服装内衣</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//fushi.1688.com/" title="鞋包配饰">鞋包配饰</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//sport.1688.com/" title="运动户外">运动户外</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//muying.1688.com/" title="童装母婴">童装母婴</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//home.1688.com/" title="日用百货">日用百货</a></span>
	                    
	                    <span><a rel="nofollow" href="//auto.1688.com/" title="汽车用品">汽车用品</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//enjoy.1688.com/" title="工艺品及宠物">工艺品及宠物</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//food.1688.com/" title="食品">食品</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//jia.1688.com/" title="家纺家饰">家纺家饰</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//jiazhuang.1688.com/" title="家装建材">家装建材</a></span>
	                    <span><a rel="nofollow" href="//mei.1688.com/" title="美妆日化">美妆日化</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//3c.1688.com/" title="数码家电">数码家电</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//industry.1688.com/diangong" title="电工电气">电工电气</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//industry.1688.com/anfang" title="安全防护">安全防护</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//page.1688.com/channel/industry/zhaoming.html" title="照明电子">照明电子</a></span>
	                    
	                    <span><a rel="nofollow" href="//jd.1688.com/" title="机械汽摩">机械汽摩</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//wjgj.1688.com/" title="五金工具">五金工具</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//yqyb.1688.com/" title="仪器仪表">仪器仪表</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//chem.1688.com/" title="化工原料">化工原料</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//jingxi.1688.com/" title="精细化学">精细化学</a></span>
	                    <span><a rel="nofollow" href="//yejin.1688.com/" title="冶金矿产">冶金矿产</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//steel.1688.com/" title="钢材">钢材</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//plas.1688.com/" title="橡塑">橡塑</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//bz.1688.com/" title="包装">包装</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//fangzhi.1688.com/" title="纺织皮革">纺织皮革</a></span>
	                    
	                  </dd>
	                </dl>
	                <dl class="dashedline"></dl>
	                <dl class="zone fd-clr">
	                  <dt class="name">特色市场</dt>
	                  <dd class="detail">
	                    <span><a rel="nofollow" href="//ye.1688.com/" title="产业带">产业带</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="https://huopin.1688.com/" title="伙拼">伙拼</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//ding.1688.com/" title="新品快订">新品快订</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//tgc.1688.com/" title="淘工厂">淘工厂</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//daili.1688.com/" title="代理加盟">代理加盟</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//ls.1688.com/" title="零售通">零售通</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//yang.1688.com/" title="免费拿样">免费拿样</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//tao.1688.com/" title="淘货源">淘货源</a></span>
	                  </dd>
	                </dl>
	                <dl class="dashedline"></dl>
	                <dl class="zone fd-clr">
	                  <dt class="name">采购平台</dt>
	                  <dd class="detail">
	                    <span><a rel="nofollow" href="//caigou.1688.com/" title="采购商城">采购商城</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//mingqi.1688.com/" title="大企业采购">大企业采购</a></span>
	                  </dd>
	                </dl>
	                <dl class="dashedline"></dl>
	                <dl class="zone fd-clr">
	                  <dt class="name">以商会友</dt>
	                  <dd class="detail">
	                    <span><a rel="nofollow" href="//club.1688.com/" title="商友圈">商友圈</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//baike.1688.com/" title="生意经">生意经</a></span>
	                  </dd>
	                </dl>
	                <dl class="dashedline"></dl>
	                <dl class="zone fd-clr">
	                  <dt class="name">常用工具</dt>
	                  <dd class="detail">
	                    <span><a rel="nofollow" href="//wangwang.1688.com" data-trace="cn_alibar_allservice_alitalk" title="阿里旺旺">阿里旺旺</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//3g.1688.com/?tracelog=wireless_alibar" title="手机阿里">手机阿里</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//dk.aliloan.com/b2bapply/credit/apply.htm?lable=bmb_cn" title="阿里贷款">阿里贷款</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//56.1688.com/" title="阿里物流" data-trace="cn_alibar_allservice_56">阿里物流</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//view.1688.com/cms/shangji/sjzl.html" title="商机助理" >商机助理</a></span>
	                  </dd>
	                </dl>
	                <dl class="dashedline"></dl>
	                <dl class="zone fd-clr">
	                  <dt class="name">安全交易</dt>
	                  <dd class="detail">
	                    <span><a rel="nofollow" href="//page.1688.com/buyerprotection/buyer.html" data-trace="cn_alibar_allservice_ buyerprotection" title="买家保障">买家保障</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//page.1688.com/trust/rztx.html" data-trace="cn_alibar_allservice_rztx" title="商家认证">商家认证</a></span>
	                    <span class="spacing"></span>
	                    <span><a rel="nofollow" href="//view.1688.com/cms/safe/xyzf/zwz/alipay/zfbyxy.html" data-trace="cn_alibar_allservice_alipay" title="支付宝">支付宝</a></span>
	                    <span class="spacing"></span> 
	                    <span><a rel="nofollow" href="//rule.1688.com/? tracelog=aliguize_wzdh01" data-trace="cn_alibar_allservice_flag" title="阿里网规" data-spm-anchor-id="a260k.635.794253809.70">阿里网规</a></span>
	                    <span class="spacing"></span> 
	                    <span><a rel="nofollow" href="//levit.1688.com/complain/cmtPost/selectPage.htm" data-trace="cn_alibar_allservice_flag" title="投诉举报">投诉举报</a></span>
	                    
	                  </dd>
	                </dl>
	              </div>
	              <div class="more">
	                <a rel="nofollow" class="moreBtn" href="//114.1688.com/sitemap.html">更多内容</a>
	              </div>
	            </div>
	          </li>
	        </ul>
	      </div>
	    </div>
	    <div class="alibar-tips fd-hide">
	      <div class="tips-content">
	        <div class="tip-logo"></div>
	        <div class="tip-text">阿里巴巴中国站和淘宝网会员帐号体系、《阿里巴巴服务条款》升级，完成登录后两边同时登录成功。<a href="//page.1688.com/2012/notice.html" target="_blank" class="fd-right detail-link">查看详情&gt;&gt;</a></div>
	        <div class="tips-close"></div>
	      </div>
	      <div class="tips-top"></div>
	    </div>
	  </div>
	</div>
<div id="header" class="sw-mod-header">

<div class="s-layout-box">
 <div class="s-layout-block">
<div class="sm-side" trace="list_logo">
 <h1 class="sw-logo">
 <a href="https://www.1688.com/" title="全球最大的采购批发市场" trace="list_logo" target="_self" hidefocus=""></a>
 </h1>
 </div>
 <div class="search-wrapper">

 <form target="_self" method="get" action="https://s.1688.com/company/company_search.htm" name="search" id="s_search_form" class="search-form">
<fieldset>
<legend>阿里巴巴搜索</legend>
<div class="searchtab-mod" trace="searchbar">
<ul class="searchtab-list" id="s_searchtabList">
 <li data-type="selloffer" class=" first" ctype="tabs" cvalue="selloffer">
<em class="sm-widget-split"></em>
<a action="https://s.1688.com/selloffer/offer_search.htm" href="https://s.1688.com/selloffer/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html" target="_self" >产品</a>
</li>
 <li data-type="company" class="selected" ctype="tabs" cvalue="company">
<em class="sm-widget-split"></em>
<a action="https://s.1688.com/company/company_search.htm" href="https://s.1688.com/company/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html" target="_self" >供应商</a>
</li>
<li data-type="newbuyoffer" class="" ctype="tabs" cvalue="newbuyoffer">
<em class="sm-widget-split"></em>
<a action="https://s.1688.com/newbuyoffer/buyoffer_search.htm" href="https://s.1688.com/newbuyoffer/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html" target="_self" >求购</a>
</li>
<li data-type="wiki" class="" ctype="tabs" cvalue="wiki">
<em class="sm-widget-split"></em>
<a action="https://s.1688.com/wiki/wiki_search.htm" href="https://s.1688.com/wiki/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html" target="_self" >生意经</a>
</li>
 </ul>
</div>
<div class="search-pannel">
<div class="search-pannel-wrap">
<div class="search-i">
  <div class="search-i-wrap">
 <input type="text" value="广告服务 广告策划"  autocomplete="off" id="q" name="keywords" class="q" maxlength="50" linkurl="" />
 </div>

<div class="search-i-action" trace="topbutton">
 <button type="submit" value="搜索">搜索</button>
</div>

</div>
 </div>
  <div class="search-history" trace="recentwords">
   
     <a cType="industryKeywords" cText="国际快递" href="https://s.1688.com/company/-B9FABCCABFECB5DD.html">国际快递</a>
   <a cType="industryKeywords" cText="商标注册" href="https://s.1688.com/company/-C9CCB1EAD7A2B2E1.html">商标注册</a>
   <a cType="industryKeywords" cText="代运营" href="https://s.1688.com/company/-B4FAD4CBD3AA.html">代运营</a>
   <a cType="industryKeywords" cText="国际物流" href="https://s.1688.com/company/-B9FABCCACEEFC1F7.html">国际物流</a>
   <a cType="industryKeywords" cText="公司注册" href="https://s.1688.com/company/-B9ABCBBED7A2B2E1.html">公司注册</a>
   <a cType="industryKeywords" cText="国际货运" href="https://s.1688.com/company/-B9FABCCABBF5D4CB.html">国际货运</a>
   <a cType="industryKeywords" cText="店铺装修" href="https://s.1688.com/company/-B5EAC6CCD7B0D0DE.html">店铺装修</a>
         <a id="sw_mod_top_word" class="sw-mod-topWord-trigger" href="#">更多></a>
  </div>
 </div>
<input type="hidden" id="sale_topSearchButton" name="button_click" value="top" />
<input type="hidden" id="category_direct" name="earseDirect" value="false" />
<input type="hidden" value="y" name="n"/>
<input type="hidden" value="1,11" name="netType" />
 </fieldset>
 </form>
 </div>
       <div class="sw-mod-topWord">
 <div class="sw-mod-topWord-layer" trace="searchbar"> 
 <div class="sw-mod-topWord-content">
 <div class="sw-mod-topWord-arrow"></div>
 <ul>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="国际快递到美国" title="国际快递到美国" href="https://s.1688.com/company/-B9FABCCABFECB5DDB5BDC3C0B9FA.html">国际快递到美国</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="台湾集运" title="台湾集运" href="https://s.1688.com/company/-CCA8CDE5BCAFD4CB.html">台湾集运</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="国际空运" title="国际空运" href="https://s.1688.com/company/-B9FABCCABFD5D4CB.html">国际空运</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="台湾专线" title="台湾专线" href="https://s.1688.com/company/-CCA8CDE5D7A8CFDF.html">台湾专线</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="代理记账" title="代理记账" href="https://s.1688.com/company/-B4FAC0EDBCC7D5CB.html">代理记账</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="兰蔻粉水" title="兰蔻粉水" href="https://s.1688.com/company/-C0BCDEA2B7DBCBAE.html">兰蔻粉水</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="物流" title="物流" href="https://s.1688.com/company/-CEEFC1F7.html">物流</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="货代" title="货代" href="https://s.1688.com/company/-BBF5B4FA.html">货代</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="别墅图纸" title="别墅图纸" href="https://s.1688.com/company/-B1F0CAFBCDBCD6BD.html">别墅图纸</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="兼职" title="兼职" href="https://s.1688.com/company/-BCE6D6B0.html">兼职</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="e邮宝" title="e邮宝" href="https://s.1688.com/company/-65D3CAB1A6.html">e邮宝</a></li>
   <li><a class="moreKeywords" cType="industryKeywords" cValue="食品经营许可证" title="食品经营许可证" href="https://s.1688.com/company/-CAB3C6B7BEADD3AAD0EDBFC9D6A4.html">食品经营许可证</a></li>
   </ul> 
 </div>
 </div>
 </div>
 </div>
</div>
</div>

 
<div id="doc" class="sw-layout-doc" data-doc-config='{"uid":"", "categoryId":"0","keywords":"广告服务 广告策划","keywordsGbk":"%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE","categoryNameGbk":"","searchType":"company","showStyle":"img","buttonClick":"","version":0.2, "prodid":"61", "beginPage":"1", 

"originalKeyword":"广告服务 广告策划", "isDangerWords":"",
"buttonClickTrace":"","isZeroResult":"false","filt":"y","videoURL":"http://service.s.1688.com/search/json_viewer.htm",
"aliToolTrace":"","trackCookie":"", "entrance":"", "cleanCookie":"false", "p4pid":"1564715663335103039155", "results":"1",
"feature":"", "province":"%D6%D8%C7%EC", "city":"", "biztype":"", "categorypath":"", "paSenderUrl":"https://s.1688.com/iprofile/track?", "viewKeywordsGbk":"%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE","searchwebUrlGbk":"http%3A%2F%2Fs.1688.com%2Fcompany%2Fcompany_search.htm%3Fkeywords%3D%25B9%25E3%25B8%25E6%25B7%25FE%25CE%25F1%2520%25B9%25E3%25B8%25E6%25B2%25DF%25BB%25AE%26province%3D%25D6%25D8%25C7%25EC%26city%3D%26filt%3Dy%26offset%3D3%26netType%3D1%252C11%26pageSize%3D30%26n%3Dy%26beginPage%3D1", "clientIp":"112.17.103.39",
"keywordsHashid":"%B9%E3%B8%E6%B7%FE%CE%F1%B9%E3%B8%E6%B2%DF%BB%AE","stat":1,

"isWideScreen":"true",
"end":0}'> 
 
  <div id="content" class="sw-layout-content">
 <div id="sm_famousShop" style="position: relative; margin: 0 auto;"></div>

 
 <div class="sw-mod-navigatebar fd-clr" id="sw_mod_navigatebar" trace="breadcrumb">


<ul class="sm-navigatebar-items" value="">
    <li class="sm-navigatebar-wholeCat sm-navigatebar-item" >
 所有类目
  </li>
  <li id="sm-folded-SN">
<div class="sm-folded-SN">
 <a href="#" class="sm-foldedSN-btnLink sm-foldedSN-display" id="sm-foldedSN-btnLink"></a>
</div>
 </li>
<li id="breadCrumbText" class="sm-navigatebar-result sm-navigatebar-item">
共找到<em class="sm-navigatebar-count">3</em>条公司信息</li>
  </ul>

<div class="sm-navigatebar-splitLine"></div>
</div>  <div id="sw_mod_sn" class="sw-mod-sn sw-layout-mod fd-hide">
 <div id="sw_mod_sn" class="sw-mod-sn ">






</div>
   <script>
 if(typeof(iSearchPV)!='undefined'){
 iSearchPV.iSubject.push("asxg_show");
 }
 </script>
<div id="sw_mod_related" class="sw-mod-related" trace="recwords">

 您是不是在找:  <a href="https://s.1688.com/company/-B9E3B8E6B2DFBBAEB9ABCBBE.html?rs=1" cvalue="广告策划公司">广告策划公司</a>
  <a href="https://s.1688.com/company/-B1A6B0B2C7F820B9E3B8E6B2DFBBAE.html?rs=1" cvalue="宝安区 广告策划">宝安区 广告策划</a>
  <a href="https://s.1688.com/company/-B9E3B8E6C9E8BCC6B2DFBBAE.html?rs=1" cvalue="广告设计策划">广告设计策划</a>
  <a href="https://s.1688.com/company/-B9E3B8E6B9ABCBBE.html?rs=1" cvalue="广告公司">广告公司</a>
  <a href="https://s.1688.com/company/-B9E3D6DDCAD0B9E3B8E6B2DFBBAEB9ABCBBE.html?rs=1" cvalue="广州市广告策划公司">广州市广告策划公司</a>
  <a href="https://s.1688.com/company/-B9E3B8E6D6C6D7F7.html?rs=1" cvalue="广告制作">广告制作</a>
  <a href="https://s.1688.com/company/-D3AACFFAB2DFBBAE.html?rs=1" cvalue="营销策划">营销策划</a>
  <a href="https://s.1688.com/company/-C6B7C5C6B2DFBBAE.html?rs=1" cvalue="品牌策划">品牌策划</a>
  <a href="https://s.1688.com/company/-BBEEB6AFB2DFBBAE.html?rs=1" cvalue="活动策划">活动策划</a>
  <a href="https://s.1688.com/company/-B2DFBBAEB9ABCBBE.html?rs=1" cvalue="策划公司">策划公司</a>
 </div>

 </div>
 <div id="sw_mod_filter" class="sw-mod-filter">

<div class="filter-bottom-wrap">
 <div class="sm-filtbar-bottom" id="filter_bottom" trace="filtbar">
 <ul id="filter-bar" class="sm-filter-bar fd-clr">

   <li class="sw-ui-select sm-filtbar-area  Selected-now " id="sw_mod_filter_area" currentprovince="" default="" industrydistricts="">
 <span class="sw-ui-selectValue sm-filter-Area-Selected">重庆</span>
 <div class="wgt-areabox" style="display: none;"><div class="wgt-areabg"></div></div>
 </li>
 
 
   <li id="filter_biztype" class="sw-ui-select sm-filtbar-biztype " biztype="biztype" >
 <span class="sw-ui-selectValue">
  经营模式   </span>
 <ul _frmfield="biztype" class="sw-ui-selectItems" style="display: none;">
 <li >
 <a val="1" href="#" clickval="生产加工" trace="biztype">生产加工</a>
 </li>
 <li >
 <a val="2" href="#" clickval="经销批发" trace="biztype">经销批发</a>
 </li>
 <li >
 <a val="4" href="#" clickval="招商代理" trace="biztype">招商代理</a>
 </li>
 <li >
 <a val="8" href="#" clickval="商业服务" trace="biztype">商业服务</a>
 </li>
 <li class="sw-ui-selectItem">
 <a val="0" href="#" clickval="经营模式" trace="biztype">经营模式</a>
 </li>
 </ul>
 </li>


   <li class="sw-ui-select sm-filtbar-employeesCount" id="filter_employeesCount">
 <span class="sw-ui-selectValue">员工人数</span>
 <ul class="sw-ui-selectItems" _frmfield="employeesCount">
   <li  >
 <a val="1" href="#" clickval="5人以下" trace="employeesCount" rel="nofollow" >5人以下</a>
 </li> 
   <li  >
 <a val="2,3" href="#" clickval="5人-50人" trace="employeesCount" rel="nofollow" >5人-50人</a>
 </li> 
   <li  >
 <a val="4" href="#" clickval="51人-100人" trace="employeesCount" rel="nofollow" >51人-100人</a>
 </li> 
   <li  >
 <a val="8,5,9" href="#" clickval="101人-500人" trace="employeesCount" rel="nofollow" >101人-500人</a>
 </li> 
   <li  >
 <a val="6" href="#" clickval="501人-1000人" trace="employeesCount" rel="nofollow" >501人-1000人</a>
 </li> 
   <li  >
 <a val="7" href="#" clickval="1000人以上" trace="employeesCount" rel="nofollow" >1000人以上</a>
 </li> 
 <li><a val="" href="#" rel="nofollow"  class="sw-ui-selectItem"  >员工人数</a></li>
 </ul>
 </li>
 

   <li class="sw-ui-select sm-filtbar-annualRevenue" id="filter_annualRevenue">
 <span class="sw-ui-selectValue">年营业额</span>
 <ul class="sw-ui-selectItems" _frmfield="annualRevenue"> 
  <li >
<a val="8,1" href="#" trace="annualRevenue" clickval="10万以下" rel="nofollow" >10万以下</a>
</li>
  <li >
<a val="9,10,1" href="#" trace="annualRevenue" clickval="10万-50万" rel="nofollow" >10万-50万</a>
</li>
  <li >
<a val="11,1" href="#" trace="annualRevenue" clickval="51万-100万" rel="nofollow" >51万-100万</a>
</li>
  <li >
<a val="2,12,3" href="#" trace="annualRevenue" clickval="101万-500万" rel="nofollow" >101万-500万</a>
</li>
  <li >
<a val="14" href="#" trace="annualRevenue" clickval="501万-1000万" rel="nofollow" >501万-1000万</a>
</li>
  <li >
<a val="5,15,16,17,6,7" href="#" trace="annualRevenue" clickval="1000万以上" rel="nofollow" >1000万以上</a>
</li>
<li><a val="" href="#" rel="nofollow" trace="annualRevenue" clickval="年营业额"  class="sw-ui-selectItem"  >年营业额</a></li>
 </ul>
 </li>


 
   <li class="sm-filtbar-line"></li>
 <li class="sm-filtbar-sort">
 <a class="sm-filtbar-popSort  sm-filtbar-popSorted  " id="filter_popSort" _frmfield="sortType" val="pop" disval="notpop"  checked="checked" clickval="pop" trace="sortType" href="#" title="人气从高到低排序" target="_self" >人气</a>
<a class="sm-filtbar-cxtSort  " id="filter_cxtSort" _frmfield="sortType" val="pmSort" disval=""  clickval=""  trace="sortType" href="#" title="诚信通年份从高到低排序" target="_self" ><span class="sw-ui-icon-cxt16x16">年份</span></a>
</li>
<li class="sm-filtbar-line"></li>
<li class="sm-filter-bottom-item sm-filter-distanceSelet"><span class="fd-left">采购距离&nbsp;</span>
 <div ctype="distance" trace="distance" initialclass="" class="sw-mod-distanceSelect " id="distanceSelect" location="">
<a index="1" dis="50" clickval="50" class="sw-mod-distanceSelect-link sw-mod-distanceSelect-dis1" href="#"></a>
<a index="2" dis="100" clickval="100" class="sw-mod-distanceSelect-link sw-mod-distanceSelect-dis2" href="#"></a>
<a index="3" dis="200" clickval="200" class="sw-mod-distanceSelect-link sw-mod-distanceSelect-dis3" href="#"></a>
<a index="4" dis="300" clickval="300" class="sw-mod-distanceSelect-link sw-mod-distanceSelect-dis4" href="#"></a>
<a index="5" dis="unlimited" clickval="unlimited" class="sw-mod-distanceSelect-link sw-mod-distanceSelect-dis5" href="#"></a>
 </div>
 </li>
           
   <li class="sm-filtbar-rzReport"> 
 <input id="filter_ckbrzReport" _frmfield="rzReport" val="true" type="checkbox" trace="rzReport"  clickval="false">
 <label for="filter_ckbrzReport"><span>有认证报告</span></label>
 </li>
 
   <li class="sm-filtbar-payGuarantee" >
 <input id="filter_ckbSurence" _frmfield="isCreditFlag" val="true" type="checkbox" trace="creditFlag"  clickval="false" >
 <label for="filter_ckbSurence"><span>买家保障</span></label>
 </li>

  <li class="sm-filtbar-shili" >
 <input id="filter_ckbShili" _frmfield="memberTags" val="205057" type="checkbox" trace="shili"  clickval="false" >
 <label for="filter_ckbShili"><span>实力商家</span></label>
 </li>



 </ul>

 </div>
</div>

</div>



 <div id="sw_mod_mainblock" class="sw-mod-mainblock sw-layout-mod">
 <div id="sw_mod_searchlist" class="sw-layout-doc sw-layout-mod">

<ul class="sm-company-list fd-clr" data-p4p-info='{"p4pSessionId":"430f1a8aafb7c96194cbe9d187af058f"}' data-spm="result">
<li id="offer1" class="company-list-item" itemid="36651404" companyid="b2b-33881859280605a"  trace="companyTemplate" memberId="b2b-33881859280605a" nowCount="1" offerState="m0c0000" >
<div class="list-item-left">
<div class="bg"></div>
<div class="wrap">
 <div class="list-item-title">
      <a class="list-item-title-text" offer-id="offer1"  rel="nofollow" offerId="" offer-stat="com" title="重庆琪洋会展服务有限公司" target="_blank" href="https://shop1412n70r41354.1688.com" gotodetail="2" >重庆琪洋会展服务有限公司</a>
 <a class="alitalk alitalk-on" title="点此可直接与对方在线咨询产品、交流洽谈。还支持语音视频和多方商务洽谈" offer-id="offer1" rel="nofollow"  offerId="" offer-stat="alitalk" alitalk="{'infoId':'','id':'qiyangzhanye123','type':'company','categoryId':'0'}" href="#"></a>
<a class="sw-ui-icon-callme" style="display:none;" offerId="" offer-id="offer1" rel="nofollow"  offer-stat="mfhj" target="_self" href="#" data-callme-id="b2b-33881859280605a" ></a>
</div>
<div class="list-item-icons">

     <a target="_blank" offer-id="offer1"  offer-stat="tp" offerId="" title="阿里巴巴建议您优先选择诚信通会员" href="https://shop1412n70r41354.1688.com/page/creditdetail.htm" class="icons-identification sw-ui-icon-cxt16x16" rel="nofollow">
 <i></i>
  <em>2</em>年 | 
   </a>


        <a class="icons-guarantee sw-ui-icon-payGuarantee" target="_blank" offer-stat="7day" offerId="" href="https://page.1688.com/buyerprotection/buyer.html" title="该卖家支持先行赔付，保障买家交易安全" rel="nofollow"></a>
     
</div>
 <div class="list-item-detail">
   
 <div class="detail-left">
<div class="detail-float-items">
 <span class="detail-field-name">主营产品:</span>
 <a target="_blank" offer-stat="mainProduct" offerId="" offer-id="offer1"  href="https://shop1412n70r41354.1688.com/page/offerlist.htm" rel="nofollow">
   <span>广告礼品定做;</span>
   <span>印刷宣传片定;</span>
   <span>广告用;</span>
   </a>
</div>
<div>
<span class="detail-field-name">所在地:</span>
<a class="sm-offerResult-areaaddress" title=" 重庆市九龙坡区 陈家坪帝豪名都1905" offer-id="offer1" offerId=""  offer-stat="local" target="_blank" href="https://shop1412n70r41354.1688.com/page/contactinfo.htm?appfrom=searchweb" rel="nofollow"> 重庆市九龙坡区 陈家坪帝豪名...</a>
 </div>
<div>
<span class="detail-field-name">员工人数:</span>
<a href="https://shop1412n70r41354.1688.com/page/creditdetail.htm" offerId="" title="51 - 100 人" offer-id="offer1"  offer-stat="employee" target="_blank" rel="nofollow">51 - 100 人</a>
</div>
 <div>
<a href="https://cx.1688.com/certificate/image/certificateImageView.htm?memberId=b2b-33881859280605a" offerId="" offer-id="offer1"  offer-stat="certificate" target="_blank" rel="nofollow">资质证书&gt;</a>
 <a href="https://shop1412n70r41354.1688.com/page/creditdetail.htm" offerId="" offer-id="offer1"  offer-stat="morecompany" target="_blank" rel="nofollow">更多公司信息&gt;</a>
</div>
 </div>
<div class="detail-right">
 <div><span class="detail-field-name">经营模式:</span><b>生产加工</b></div>
  <div title="服装印花">
 <span class="detail-field-name">工艺类型:</span>
 <a href="https://shop1412n70r41354.1688.com/page/creditdetail.htm" target="_blank" offer-id="offer1" offerId=""  offer-stat="detail" rel="nofollow">服装印花</a>
 </div>
  <div title="来图加工,来样加工">
 <span class="detail-field-name">加工方式:</span>
 <a href="https://shop1412n70r41354.1688.com/page/creditdetail.htm" target="_blank" offer-id="offer1" offerId=""  offer-stat="detail" rel="nofollow">来图加工,来样加工</a>
 </div>
  <div title="1000平方米">
 <span class="detail-field-name">厂房面积:</span>
 <a href="https://shop1412n70r41354.1688.com/page/creditdetail.htm" target="_blank" offer-id="offer1" offerId=""  offer-stat="detail" rel="nofollow">1000平方米</a>
 </div>
  </div>
 </div>
 <div class="list-item-detailclear"></div>
       </div>
</div>
 <div class="list-item-right">
 <div class="wrap">
<div class="list-item-buttons">
<span>
 <a href="https://s.1688.com/company/similar.htm?memberIds=b2b-33881859280605a&keywords=%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE" offerId="" offer-id="offer1"  offer-stat="similarshop" target="_blank" rel="nofollow">相似店铺&gt;</a>
<a href="https://shop1412n70r41354.1688.com" offerId="" offer-id="offer1"  offer-stat="thisshop" target="_blank" rel="nofollow">进入本店铺&gt;</a>
</span>
</div>
  <div class="list-item-itemsWrap">
 <ul>
   <li>
 <a offer-id="offer1" offerId="557313327257" offer-stat="pic_1"  target="_blank" href="https://detail.1688.com/offer/557313327257.html">
 <span class="item-offer-title"><span>鼠标垫厂家定做广告鼠标垫 橡胶广告鼠标垫  硅胶PVC鼠标垫</span></span>
   <img alt="鼠标垫厂家定做广告鼠标垫 橡胶广告鼠标垫  硅胶PVC鼠标垫" src="https://cbu01.alicdn.com/img/ibank/2017/813/580/4563085318_482929558.search.jpg" class="cover"/>
   </a>
 <div>
  <span class="price" title="￥1.10"><i>￥</i>1.10</span>
   </div>
</li>
  <li>
 <a offer-id="offer2" offerId="557313327252" offer-stat="pic_2"  target="_blank" href="https://detail.1688.com/offer/557313327252.html">
 <span class="item-offer-title"><span>定做广告鼠标垫 定制鼠标垫 彩色鼠标垫 礼品鼠标垫</span></span>
   <img alt="定做广告鼠标垫 定制鼠标垫 彩色鼠标垫 礼品鼠标垫" src="https://cbu01.alicdn.com/img/ibank/2017/974/280/4563082479_482929558.search.jpg" class="cover"/>
   </a>
 <div>
  <span class="price" title="￥0.80"><i>￥</i>0.80</span>
   </div>
</li>
  <li>
 <a offer-id="offer3" offerId="579250299424" offer-stat="pic_3"  target="_blank" href="https://detail.1688.com/offer/579250299424.html">
 <span class="item-offer-title"><span>广告手提纸袋定做纸质企业宣传白卡纸重庆牛皮纸袋定制纸质包邮</span></span>
   <img alt="广告手提纸袋定做纸质企业宣传白卡纸重庆牛皮纸袋定制纸质包邮" src="https://cbu01.alicdn.com/img/ibank/2018/504/319/8528913405_482929558.search.jpg" class="cover"/>
   </a>
 <div>
  <span class="price" title="￥1.80"><i>￥</i>1.80</span>
  <span class="volume" title="累计成交1000个">成交<em>1000</em>个</span>
  </div>
</li>
</ul>
</div>
<div class="list-item-qrcode">
 <div class="corner"></div>
 <div class="qrcode" offerId="" offer-id="offer1"  offer-stat="twodimensioncode" target="_blank" rel="nofollow">
 <img data-src="http://ma.m.1688.com/touch/code/sCode?w=123&amp;h=123&amp;el=m&amp;type=company&amp;id=b2b-33881859280605a"/>
 <br />
 扫一扫, 进入手机旺铺
 </div>
 </div>
</div>
</div>
</li>
<li id="offer2" class="company-list-item" itemid="28216178" companyid="lwc417162934"  trace="companyTemplate" memberId="lwc417162934" nowCount="2" offerState="m000000" >
<div class="list-item-left">
<div class="bg"></div>
<div class="wrap">
 <div class="list-item-title">
      <a class="list-item-title-text" offer-id="offer2"  rel="nofollow" offerId="" offer-stat="com" title="重庆星鹏玻璃有限公司" target="_blank" href="https://cqxpglass.1688.com" gotodetail="2" >重庆星鹏玻璃有限公司</a>
 <a class="alitalk alitalk-on" title="点此可直接与对方在线咨询产品、交流洽谈。还支持语音视频和多方商务洽谈" offer-id="offer2" rel="nofollow"  offerId="" offer-stat="alitalk" alitalk="{'infoId':'','id':'lwc417162934','type':'company','categoryId':'0'}" href="#"></a>
<a class="sw-ui-icon-callme" style="display:none;" offerId="" offer-id="offer2" rel="nofollow"  offer-stat="mfhj" target="_self" href="#" data-callme-id="lwc417162934" ></a>
</div>
<div class="list-item-icons">

     <a target="_blank" offer-id="offer2"  offer-stat="tp" offerId="" title="阿里巴巴建议您优先选择诚信通会员" href="https://cqxpglass.1688.com/page/creditdetail.htm" class="icons-identification sw-ui-icon-cxt16x16" rel="nofollow">
 <i></i>
  <em>8</em>年 | 
   </a>


          
</div>
 <div class="list-item-detail">
   
 <div class="detail-left">
<div class="detail-float-items">
 <span class="detail-field-name">主营产品:</span>
 <a target="_blank" offer-stat="mainProduct" offerId="" offer-id="offer2"  href="https://cqxpglass.1688.com/page/offerlist.htm" rel="nofollow">
   <span>玻璃小酒杯;</span>
   <span>玻璃分酒器;</span>
   <span>玻璃酒具;</span>
   <span>烟;</span>
   </a>
</div>
<div>
<span class="detail-field-name">所在地:</span>
<a class="sm-offerResult-areaaddress" title=" 重庆市 空港工业园  宝圣路89号" offer-id="offer2" offerId=""  offer-stat="local" target="_blank" href="https://cqxpglass.1688.com/page/contactinfo.htm?appfrom=searchweb" rel="nofollow"> 重庆市 空港工业园  宝圣路89号</a>
 </div>
<div>
<span class="detail-field-name">员工人数:</span>
<a href="https://cqxpglass.1688.com/page/creditdetail.htm" offerId="" title="501 - 1000 人" offer-id="offer2"  offer-stat="employee" target="_blank" rel="nofollow">501 - 1000 人</a>
</div>
 <div>
<a href="https://cx.1688.com/certificate/image/certificateImageView.htm?memberId=lwc417162934" offerId="" offer-id="offer2"  offer-stat="certificate" target="_blank" rel="nofollow">资质证书&gt;</a>
 <a href="https://cqxpglass.1688.com/page/creditdetail.htm" offerId="" offer-id="offer2"  offer-stat="morecompany" target="_blank" rel="nofollow">更多公司信息&gt;</a>
</div>
 </div>
<div class="detail-right">
 <div><span class="detail-field-name">经营模式:</span><b>生产加工</b></div>
  <div title="手工,抛光,开料">
 <span class="detail-field-name">工艺类型:</span>
 <a href="https://cqxpglass.1688.com/page/creditdetail.htm" target="_blank" offer-id="offer2" offerId=""  offer-stat="detail" rel="nofollow">手工,抛光,开料</a>
 </div>
  <div title="来图加工,来样加工">
 <span class="detail-field-name">加工方式:</span>
 <a href="https://cqxpglass.1688.com/page/creditdetail.htm" target="_blank" offer-id="offer2" offerId=""  offer-stat="detail" rel="nofollow">来图加工,来样加工</a>
 </div>
  <div title="">
 <span class="detail-field-name">厂房面积:</span>
 <a href="https://cqxpglass.1688.com/page/creditdetail.htm" target="_blank" offer-id="offer2" offerId=""  offer-stat="detail" rel="nofollow">--</a>
 </div>
  </div>
 </div>
 <div class="list-item-detailclear"></div>
       </div>
</div>
 <div class="list-item-right">
 <div class="wrap">
<div class="list-item-buttons">
<span>
 <a href="https://s.1688.com/company/similar.htm?memberIds=lwc417162934&keywords=%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE" offerId="" offer-id="offer2"  offer-stat="similarshop" target="_blank" rel="nofollow">相似店铺&gt;</a>
<a href="https://cqxpglass.1688.com" offerId="" offer-id="offer2"  offer-stat="thisshop" target="_blank" rel="nofollow">进入本店铺&gt;</a>
</span>
</div>
  <div class="list-item-itemsWrap">
 <ul>
   <li>
 <a offer-id="offer1" offerId="1108945182" offer-stat="pic_1"  target="_blank" href="https://detail.1688.com/offer/1108945182.html">
 <span class="item-offer-title"><span>星鹏牌机器吹制高脚杯红酒酒杯质量好【服务周到】</span></span>
   <img alt="星鹏牌机器吹制高脚杯红酒酒杯质量好【服务周到】" src="https://cbu01.alicdn.com/img/ibank/2011/173/460/459064371_1580434641.search.jpg" class="cover"/>
   </a>
 <div>
  <span class="price" title="￥5.00"><i>￥</i>5.00</span>
   </div>
</li>
</ul>
</div>
<div class="list-item-qrcode">
 <div class="corner"></div>
 <div class="qrcode" offerId="" offer-id="offer2"  offer-stat="twodimensioncode" target="_blank" rel="nofollow">
 <img data-src="http://ma.m.1688.com/touch/code/sCode?w=123&amp;h=123&amp;el=m&amp;type=company&amp;id=lwc417162934"/>
 <br />
 扫一扫, 进入手机旺铺
 </div>
 </div>
</div>
</div>
</li>
<li id="offer3" class="company-list-item" itemid="26847168" companyid="rszs888"  trace="companyTemplate" memberId="rszs888" nowCount="3" offerState="m000000" data-credit-detail>
<div class="list-item-left">
<div class="bg"></div>
<div class="wrap">
 <div class="list-item-title">
      <a class="list-item-title-text" offer-id="offer3"  rel="nofollow" offerId="" offer-stat="com" title="重庆荣盛展示服务有限公司" target="_blank" href="https://rszs888.1688.com" gotodetail="2" >重庆荣盛展示服务有限公司</a>
 <a class="alitalk alitalk-on" title="点此可直接与对方在线咨询产品、交流洽谈。还支持语音视频和多方商务洽谈" offer-id="offer3" rel="nofollow"  offerId="" offer-stat="alitalk" alitalk="{'infoId':'','id':'rszs888','type':'company','categoryId':'0'}" href="#"></a>
<a class="sw-ui-icon-callme" style="display:none;" offerId="" offer-id="offer3" rel="nofollow"  offer-stat="mfhj" target="_self" href="#" data-callme-id="rszs888" ></a>
</div>
<div class="list-item-icons">

     <a target="_blank" offer-id="offer3"  offer-stat="tp" offerId="" title="阿里巴巴建议您优先选择诚信通会员" href="https://rszs888.1688.com/page/creditdetail.htm" class="icons-identification sw-ui-icon-cxt16x16" rel="nofollow">
 <i></i>
  <em>9</em>年 | 
   </a>


          
</div>
 <div class="list-item-detail">
   
 <div class="detail-left">
<div class="detail-float-items">
 <span class="detail-field-name">主营产品:</span>
 <a target="_blank" offer-stat="mainProduct" offerId="" offer-id="offer3"  href="https://rszs888.1688.com/page/offerlist.htm" rel="nofollow">
   <span>会展服务;</span>
   <span>展览展示器材设;</span>
   <span>画展展;</span>
   </a>
</div>
<div>
<span class="detail-field-name">所在地:</span>
<a class="sm-offerResult-areaaddress" title=" 重庆市江北区 江北区五红路金科丽苑巴渝居16-4" offer-id="offer3" offerId=""  offer-stat="local" target="_blank" href="https://rszs888.1688.com/page/contactinfo.htm?appfrom=searchweb" rel="nofollow"> 重庆市江北区 江北区五红路金...</a>
 </div>
<div>
<span class="detail-field-name">员工人数:</span>
<a href="https://rszs888.1688.com/page/creditdetail.htm" offerId="" title="11 - 50 人" offer-id="offer3"  offer-stat="employee" target="_blank" rel="nofollow">11 - 50 人</a>
</div>
 <div>
<a href="https://cx.1688.com/certificate/image/certificateImageView.htm?memberId=rszs888" offerId="" offer-id="offer3"  offer-stat="certificate" target="_blank" rel="nofollow">资质证书&gt;</a>
 <a href="https://rszs888.1688.com/page/creditdetail.htm" offerId="" offer-id="offer3"  offer-stat="morecompany" target="_blank" rel="nofollow">更多公司信息&gt;</a>
</div>
 </div>
<div class="detail-right">
 <div><span class="detail-field-name">经营模式:</span><b>商业服务</b></div>
  <div title="">
 <span class="detail-field-name">累计成交数:</span>
 <a href="https://rszs888.1688.com/page/creditdetail_remark.htm" target="_blank" offer-id="offer3" offerId=""  offer-stat="detail" rel="nofollow">--</a>
 </div>
  <div title="">
 <span class="detail-field-name">累计买家数:</span>
 <a href="https://rszs888.1688.com/page/creditdetail_remark.htm" target="_blank" offer-id="offer3" offerId=""  offer-stat="detail" rel="nofollow">--</a>
 </div>
  <div title="">
 <span class="detail-field-name">重复采购率:</span>
 <a href="https://rszs888.1688.com/page/creditdetail_remark.htm" target="_blank" offer-id="offer3" offerId=""  offer-stat="detail" rel="nofollow">--</a>
 </div>
  </div>
 </div>
 <div class="list-item-detailclear"></div>
       </div>
</div>
 <div class="list-item-right">
 <div class="wrap">
<div class="list-item-buttons">
<span>
 <a href="https://s.1688.com/company/similar.htm?memberIds=rszs888&keywords=%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE" offerId="" offer-id="offer3"  offer-stat="similarshop" target="_blank" rel="nofollow">相似店铺&gt;</a>
<a href="https://rszs888.1688.com" offerId="" offer-id="offer3"  offer-stat="thisshop" target="_blank" rel="nofollow">进入本店铺&gt;</a>
</span>
</div>
  <div class="list-item-itemsWrap">
 <ul>
   <li>
 <a offer-id="offer1" offerId="37706445725" offer-stat="pic_1"  target="_blank" href="https://detail.1688.com/offer/37706445725.html">
 <span class="item-offer-title"><span>会议厅布置-展板租赁-标摊搭建-重庆桁架-玻璃展示柜-设计策划</span></span>
   <img alt="会议厅布置-展板租赁-标摊搭建-重庆桁架-玻璃展示柜-设计策划" src="https://cbu01.alicdn.com/img/ibank/2014/467/300/1295003764_1504708030.search.jpg" class="cover"/>
   </a>
 <div>
  <span class="price" title="￥1.00"><i>￥</i>1.00</span>
   </div>
</li>
  <li>
 <a offer-id="offer2" offerId="853471538" offer-stat="pic_2"  target="_blank" href="https://detail.1688.com/offer/853471538.html">
 <span class="item-offer-title"><span>供应展台设计 搭建 会务及活动策划、展架 婚庆 桁架 太空架 标摊</span></span>
   <img alt="供应展台设计 搭建 会务及活动策划、展架 婚庆 桁架 太空架 标摊" src="https://cbu01.alicdn.com/img/ibank/2012/173/073/604370371_1504708030.search.jpg" class="cover"/>
   </a>
 <div>
   </div>
</li>
</ul>
</div>
<div class="list-item-qrcode">
 <div class="corner"></div>
 <div class="qrcode" offerId="" offer-id="offer3"  offer-stat="twodimensioncode" target="_blank" rel="nofollow">
 <img data-src="http://ma.m.1688.com/touch/code/sCode?w=123&amp;h=123&amp;el=m&amp;type=company&amp;id=rszs888"/>
 <br />
 扫一扫, 进入手机旺铺
 </div>
 </div>
</div>
</div>
</li>
</ul>

<script type="text/javascript">
 var companyCoaseParam = {
  'object_type':'offer',
 'page_area':3,
 'object_ids':'557313327257,1,11;557313327252,1,12;579250299424,1,13;1108945182,1,21;37706445725,1,31;853471538,1,32;',
 'category_id':'',
 'keyword':'%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE',
 'page_size':'6',
 'page_no':'1',
 'gold_ad_ids':'',
 'isHasGoldAds':false,
 'fnType':'companyoffer',
 'coaseType':'specificSpider'
  };
</script>
<script type="text/javascript">
var coaseParam = {
   'object_ids':'b2b-33881859280605a,1;lwc417162934,1;rszs888,1;',
 'category_id':'',
 'keyword':'%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE',
 'page_size':'30',
 'page_no':'1',
 'gold_ad_ids':'',
 'isHasGoldAds':false,
 'fnType':'company',
 'coaseType':'specificSpider'
 }
</script>



  </div>
 </div>
 

 
<div id="companybottomp4p" class="sw-mod-bottomp4p sw-layout-mod" data-spm="ad2">
 <ul>

 </ul>
</div>


 
 <div class="sw-mod-moreInfo sw-layout-mod" id="sw_mod_moreInfo" trace="bottomMoreInfo">
没有找到适合的<strong>广告服务 广告策划</strong>供应商？
 <a rel="nofollow" class="sm-moreInfo-link sw-ui-btn-g20" href="https://go.1688.com/buyoffer/post_offer.htm?formType=full&amp;source_type=sousuo2" target="_blank"><span>马上发布询价单</span></a>
 <a data-spm-protocol="i" href="https://index.1688.com/alizs/top.htm" class="sm-moreInfo-link" cvalue="searchtop" target="_blank"><i class="sm-moreInfo-rankIcon"></i>查看搜索排行榜</a>
<a rel="nofollow" class="sm-moreInfo-link sm-moreInfo-link-slashend" href="https://baike.1688.com/doc/add.html?keywords=%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE" cvalue="wikihelp" target="_blank">去生意经求助</a>
</div>

   <div id="p4poffer" class="sw-mod-bottomp4p sw-layout-mod"></div>
 <script type="text/javascript">
 var p4pObject = {
 keyword:"%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE",
 catid:"",
 cat:"",
 tag:"",
 count:"6",
 beginPage:"1",
 needNextGroup:false,
 pid:"819072_1008",
 p4p:"p4pOffers",
 mt:"ec",
 forumid:"",
 source:"",
 dcatid:"2421",
spuid:"",
 bottomP4P:"p4pOffers"
 };
 </script>
     <script>
 if(typeof(iSearchPV)!='undefined'){
 iSearchPV.iSubject.push("relative_show");
 }
 </script>
<div id="sw_mod_interest" class="sw-mod-interest sw-layout-mod" trace="relwords">

 <strong >您还可以找：</strong>
  <a href="https://s.1688.com/company/-B9E3B8E6B2DFBBAEB9ABCBBE.html?rs=1" cvalue="广告策划公司" clickword="广告策划公司">广告策划公司</a>
  <a href="https://s.1688.com/company/-B1A6B0B2C7F820B9E3B8E6B2DFBBAE.html?rs=1" cvalue="宝安区 广告策划" clickword="宝安区 广告策划">宝安区 广告策划</a>
  <a href="https://s.1688.com/company/-B9E3B8E6C9E8BCC6B2DFBBAE.html?rs=1" cvalue="广告设计策划" clickword="广告设计策划">广告设计策划</a>
  <a href="https://s.1688.com/company/-B9E3B8E6B9ABCBBE.html?rs=1" cvalue="广告公司" clickword="广告公司">广告公司</a>
  <a href="https://s.1688.com/company/-B9E3D6DDCAD0B9E3B8E6B2DFBBAEB9ABCBBE.html?rs=1" cvalue="广州市广告策划公司" clickword="广州市广告策划公司">广州市广告策划公司</a>
  <a href="https://s.1688.com/company/-B9E3B8E6D6C6D7F7.html?rs=1" cvalue="广告制作" clickword="广告制作">广告制作</a>
  <a href="https://s.1688.com/company/-D3AACFFAB2DFBBAE.html?rs=1" cvalue="营销策划" clickword="营销策划">营销策划</a>
  <a href="https://s.1688.com/company/-C6B7C5C6B2DFBBAE.html?rs=1" cvalue="品牌策划" clickword="品牌策划">品牌策划</a>
  <a href="https://s.1688.com/company/-BBEEB6AFB2DFBBAE.html?rs=1" cvalue="活动策划" clickword="活动策划">活动策划</a>
  <a href="https://s.1688.com/company/-B2DFBBAEB9ABCBBE.html?rs=1" cvalue="策划公司" clickword="策划公司">策划公司</a>
  <a href="https://s.1688.com/company/-BABCD6DDB2DFBBAE.html?rs=1" cvalue="杭州策划" clickword="杭州策划">杭州策划</a>
  <a href="https://s.1688.com/company/-C6F3D2B5B2DFBBAE.html?rs=1" cvalue="企业策划" clickword="企业策划">企业策划</a>
 </div>

  
   
 <div id="sw_mod_bottomsearch" class="sw-mod-bottomsearch">
 
 <div class="sm-bottom-search-content fd-clr">
 <ul class="sm-bottom-search-tabs fd-clr" trace="productlinetabs">
<li class="sm-bottom-search-tab">
<a class="sm-bottom-search-tabLink" data-type="bot_产品" href="https://s.1688.com/selloffer/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html">产品</a>
</li>
<li class="sm-bottom-search-tab">
<span class="sm-bottom-search-tabSelected">供应商</span>
</li>
<li class="sm-bottom-search-tab">
<a class="sm-bottom-search-tabLink" data-type="bot_求购" href="https://s.1688.com/newbuyoffer/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html">求购</a>
</li>
<li class="sm-bottom-search-tab">
<a class="sm-bottom-search-tabLink" data-type="bot_生意经" href="https://s.1688.com/wiki/-B9E3B8E6B7FECEF120B9E3B8E6B2DFBBAE.html">生意经</a>
</li>
  </ul>
 <div class="bottom-seach-input fd-clr">
 <form method="get" name="listSearchBomfrm" id="sform" action="https://s.1688.com/company/company_search.htm">
 <input class="sm-bottom-search-s_key" type="text" maxLength="54" accesskey="s" name="keywords" value="广告服务 广告策划" id="Banner_TextBox2" />
<button class="sm-bottom-search-icon" trace="topbutton" type="submit" data-header-trace="sale_top_all_b">&#337</button>
<input type="hidden" value="y" name="n"/>
 </form>
 </div>
 </div>
</div>

 <div class="sw-mod-surence" id="sw_mod_surence">

<ul class="sm-surence-items fd-clr">
<li class="sm-surence-item sm-surence-trustBrand ">
<a class="sw-ui-icon-cxt16x16" rel="nofollow" trace="productName_tp_down" traceproductname="sale" href="//cxt.1688.com/register.html" target="_blank">经过认证，生意安心</a>
</li>
<li class="sm-surence-item sm-surence-guarantee ">
<a class="sw-ui-icon-payGuarantee" rel="nofollow" trace="productName_cxbz_down" traceproductname="sale" href="//page.1688.com/buyerprotection/buyer.html" target="_blank">交易有保障，采购更放心</a>
</li>
<li class="sm-surence-item sm-surence-alipay ">
<a class="sw-ui-icon-alipay" rel="nofollow" trace="productName_alipay_down" traceproductname="sale" href="//view.1688.com/cms/services/aliguide/bd_zfb.html?tracelog=kf_2012_budian_tyjy9" target="_blank">买卖无风险，就靠支付宝</a>
</li>
</ul>
</div>
 <div id="footer">
    <div id="footer-v0">
        <div class="footer-container">
            <div class="ali-pages">
                <p id="copyright">&copy; 2010-2018 1688.com 版权所有</p>
                <ul>
                    <li><a rel="nofollow" href="//rule.1688.com/policy/copyright.html" target="_self" title="著作权与商标声明">著作权与商标声明</a> |</li>
                    <li><a rel="nofollow" href="//rule.1688.com/policy/legal.html" target="_self" title="法律声明">法律声明</a> |</li>
                    <li><a rel="nofollow" href="//rule.1688.com/policy/terms.htm" target="_self" title="服务条款">服务条款</a> |</li>
                    <li><a rel="nofollow" href="//rule.1688.com/policy/privacy.html" target="_self" title="隐私政策">隐私政策</a> |</li>
                    <li><a rel="nofollow" href="//page.1688.com/shtml/about/ali_group1.shtml" target="_self" title="关于阿里巴巴">关于阿里巴巴</a> |</li>
                    <li><a rel="nofollow" href="//114.1688.com/kf/contact.html?tracelog=kf_2012_budian_allcontact" target="_self" title="联系我们">联系我们</a> |</li>
                    <li><a href="//114.1688.com/sitemap.html" target="_self" title="网站导航">网站导航</a></li>
                </ul>
            </div>
            <div class="ali-group">
                <dl>
                  	<dd>
                        <a rel="nofollow" href="http://www.alibabagroup.com/cn/global/home" title="阿里巴巴集团">阿里巴巴集团</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="//www.alibaba.com/" title="阿里巴巴国际站">阿里巴巴国际站</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="//www.1688.com/" title="阿里巴巴中国站">阿里巴巴中国站</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="//www.aliexpress.com/" title="全球速卖通">全球速卖通</a>
                        |
                    </dd>
                    
                    <dd>
                        <a rel="nofollow" href="//www.taobao.com/" title="淘宝网">淘宝网</a>
                        |
                    </dd>
                    <dd>
                        <a rel="nofollow" href="//www.tmall.com/" title="天猫">天猫</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="//ju.taobao.com/" title="聚划算">聚划算</a>
                        |
                    </dd>
                    <dd>
                        <a rel="nofollow" href="http://www.etao.com/" title="一淘">一淘</a>
                        |
                    </dd>
                  	<dd>
                        <a href="//www.alitrip.com/" title="阿里旅行 · 去啊">阿里旅行 · 去啊</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="http://www.alimama.com/" title="阿里妈妈">阿里妈妈</a>
                        |
                    </dd>
                    <dd>
                        <a rel="nofollow" href="http://www.xiami.com/" title="虾米">虾米</a>
                        |
                    </dd>
                    <dd>
                        <a rel="nofollow" href="//www.aliyun.com/" title="阿里云计算">阿里云计算</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="//www.yunos.com/" title="YunOS">YunOS</a>
                        |
                    </dd>
                 	<dd>
                        <a rel="nofollow" href="//aliqin.tmall.com/" title="阿里通信">阿里通信</a>
                        |
                    </dd>
                  	<dd>
                        <a rel="nofollow" href="//www.net.cn/" title="万网">万网</a>
                        |
                    </dd>
                    <dd>
                        <a rel="nofollow" href="http://www.uc.cn/" title="UC">UC</a>
                        |
                    </dd>
                    <dd>
                        <a rel="nofollow" href="//www.alipay.com/" title="支付宝">支付宝</a>
                       	|
                    </dd>
                    <dd>
                          <a rel="nofollow" href="https://www.laiwang.com/" title="来往">来往</a>
                       	|
                  	</dd>
                    <dd>
                          <a rel="nofollow" href="http://www.dingtalk.com/?lwfrom=20150130161950940" title="钉钉">钉钉</a>
                         |
                  	</dd>
                    <dd>
                          <a rel="nofollow" href="http://www.alihealth.cn/" title="阿里健康">阿里健康</a>
                         |
                    </dd>  
                    <dd>
                          <a href="//onetouch.alibaba.com" title="一达通">一达通</a>
                      	|
                    </dd>
                  <dd>
                          <a href="http://taobao.lazada.sg" title="Lazada">Lazada</a>
                    </dd>
                </dl>
            </div>
        </div>
    </div>
</div>
 <form action="https://s.1688.com/company/company_search.htm" method="get" name="frmAreaSearch" id="frmFiltSearch" style="display:none">
<button class="hidden" type="submit" id="J_submitBtn">搜索</button>
  <input type="hidden" value="" name="isCreditFlag"/>
  <input type="hidden" value="广告服务 广告策划" name="keywords"/>
  <input type="hidden" value="" name="promotionSale"/>
  <input type="hidden" value="" name="location"/>
  <input type="hidden" value="" name="categoryId"/>
  <input type="hidden" value="" name="shidirz"/>
  <input type="hidden" value="" name="rzReport"/>
  <input type="hidden" value="" name="enterpriseId"/>
  <input type="hidden" value="" name="employeesCount"/>
  <input type="hidden" value="" name="longi"/>
  <input type="hidden" value="" name="city"/>
  <input type="hidden" value="" name="memberIds"/>
  <input type="hidden" value="" name="annualRevenue"/>
  <input type="hidden" value="" name="serviceId"/>
  <input type="hidden" value="" name="dis"/>
  <input type="hidden" value="pop" name="sortType"/>
  <input type="hidden" value="重庆" name="province"/>
  <input type="hidden" value="" name="memberTags"/>
  <input type="hidden" value="" name="feature"/>
  <input type="hidden" value="" name="lati"/>
  <input type="hidden" value="" name="biztype"/>
<input type="hidden" value="y" name="n"/>
<input type="hidden" value="y" name="filt"/>
</form>
<div id="sm_scrolltop" class="sm-scrolltop" data-config='{"feedback":"//club.1688.com/thread/addThread.htm?circleId=100753","investigate":"//survey.1688.com/survey/4MQiN4CKx","help":"//page.1688.com/html/help_pop.html"}'>

</div>
 </div>

 </div>
 

<script type="text/javascript" src="//astyle.alicdn.com/??fdevlib/js/fdev-v4/app/jengine/seed.js,fdevlib/js/fdev-v4/core/fdev-min.js,app/search/js/list/cml/appstart/start.min.js,fdevlib/js/lofty/port/lofty.js,app/search/app.config.js,fdevlib/js/lofty/lang/log.js,fdevlib/js/app/butterfly/lang/loader.js,fdevlib/js/lofty/lang/class.js,fdevlib/js/app/butterfly/context/application.js,app/search/js/list/cml/appstart/appstart.js?_v=716edfebdb148bbfaa3bf0386cb91e91.js"></script></body>
</html>
<script type="text/javascript">
 try{var _click_data=_click_data||[];_click_data.push({"click":{"2-showstyle":[{"d":["sale_$[attr:ctype]"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"935"}],"2-pageNode":[{"d":["page_num=$[attr:beginpage]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1608"},{"d":["page_num=$[attr:data-page]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"18155"}],"2-broadNavTrace":[{"d":["click_item=$[attr:clickType]"],"t":"2","l":"","i":"15104"}],"2-offerZeroTraceTemplate":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"14202"}],"2-extendWords":[{"d":["click_item=extendWords"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17872"},{"d":["click_item=extendWords"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"11920"}],"2-promotion":[{"d":["cx_$[attr:ctype]"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"1016"}],"2-offerTraceTemplate4individual":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]&offer_flag=$[attr:offer-flag]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17811"}],"2-recwords":[{"d":["asxg_word=$[attr:cvalue]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1611"}],"2-industryOfferTrace":[{"d":["sale_search_window_8_$[attr:clickListIndex]_$[attr:clickofferstate]_j0_$[attr:offer-stat]_$[attr:clickoffercatid]_$[attr:offerid]_%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"965"},{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"964"}],"2-offerTraceTemplate4Bid":[{"d":["dmtype=1002&keyword=%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE&pid=819010_1008&categoryid=$[attr:clickoffercatid]&offerid=$[attr:offerid]&pos=$[attr:offer-stat]"],"t":"2","l":"https://stat.1688.com/ad.html","i":"984"},{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]&offer_flag=$[attr:offer-flag]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"973"},{"d":["sale_search_window_8_$[attr:clickListIndex]_$[attr:clickofferstate]_j0_$[attr:offer-stat]_$[attr:clickoffercatid]_$[attr:offerid]_%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"972"}],"2-offerPreCompanyTraceTemplate":[{"d":["click_value=$[attr:offer-stat]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"12201"}],"2-companyTemplate":[{"d":["rank=$[attr:nowCount]&member_id=$[attr:memberId]&offer_feature=$[attr:offerState]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1610"}],"2-buttonTracelog":[{"d":["page_num=page"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1609"}],"2-companyQRWTemplate":[{"d":["rank=$[attr:nowCount]&member_id=$[attr:memberId]&offer_feature=$[attr:offerState]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17904"}],"2-offerTraceTemplate4Finder":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]&offer_flag=$[attr:offer-flag]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17810"}],"2-companyLessI2ITemplate":[{"d":["rank=$[attr:nowCount]&member_id=$[attr:memberId]&offer_feature=$[attr:offerState]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17906"}],"2-xsOfferTraceTemplate":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1171"}],"2-companyZeroI2ITemplate":[{"d":["rank=$[attr:nowCount]&member_id=$[attr:memberId]&offer_feature=$[attr:offerState]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17907"}],"2-filtbar":[{"d":["filt_type=$[attr:trace]&filt_value=$[attr:clickval]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1607"},{"d":["spudetail_search_screen_$[attr:ctype]"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"932"},{"d":["filt_type=$[attr:ctype]&filt_value=click&filt_linkage=linkage"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"933"}],"2-offerFiltBarActivityLink":[{"d":["20130321_list_more"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"1011"}],"2-broadOutTrace":[{"d":["click_item=$[attr:clickIndex]"],"t":"2","l":"","i":"15103"}],"2-offerLessTraceTemplate":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"14101"}],"2-searchbar":[{"d":["click_pos=$[attr:ctype]&click_value=$[attr:cvalue]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1618"}],"2-featureTag":[{"d":["sale_search_featureTag"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"988"}],"2-morefinder":[{"d":["click_value=$[attr:cvalue]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17809"}],"2-likeshareTrace":[{"d":["offer_id=$[attr:offer-id]&click_item=$[attr:click-item]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"13601"}],"2-moreurl":[{"d":["click_item=moreurl"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"13701"}],"2-similarDesignSearch":[{"d":["sale_search_click_similarDesign"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"987"}],"2-individuation":[{"d":["click_item=$[attr:ctype]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17959"}],"2-offerTraceTemplate":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]&offer_flag=$[attr:offer-flag]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"970"},{"d":["sale_search_window_8_$[attr:clickListIndex]_$[attr:clickofferstate]_j0_$[attr:offer-stat]_$[attr:clickoffercatid]_$[attr:offerid]_%B9%E3%B8%E6%B7%FE%CE%F1+%B9%E3%B8%E6%B2%DF%BB%AE"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"971"}],"2-imallSpuTrace":[{"d":["offer_type=$[attr:offertype]&offer_id=$[attr:offerid]&click_item=$[attr:offer-stat]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1760"},{"d":["offer_type=$[attr:offertype]&click_item=$[attr:spu-stat]&offer_id=$[attr:spuid]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1759"}],"2-caigouoffertemplate":[{"d":["rank=$[attr:clickindex]&offer_id=$[attr:offerid]&click_item=$[attr:offeritem]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"18270"}],"2-productTab":[{"d":["sale_tab_$[attr:ctype]"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"934"}],"2-filtbarActive":[{"d":["filt_type=$[attr:ctype]&filt_value=click&filt_linkage=linkage"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"14801"}],"2-relwords":[{"d":["reltiv_word=$[attr:cvalue]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1612"}],"2-finderblock":[{"d":["click_item=$[attr:ctype]&click_value=$[attr:cvalue]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17815"}],"2-recentwords":[{"d":["sale_search_$[attr:cType]_$[attr:cText]"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"17817"},{"d":["sect=searchbar&click_pos=$[attr:cType]&click_value=$[attr:cText]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"17816"}],"2-sameDesignSearch":[{"d":["sale_search_click_sameDesign"],"t":"1","l":"https://stat.1688.com/search/queryreport.html","i":"986"}],"2-brandShopTip":[{"d":["click_item=brandlink"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"14001"}],"2-offerQRWTraceTemplate":[{"d":["rank=$[attr:clicklistindex]&member_id=$[attr:companyid]&offer_feature=$[attr:clickofferstate]&click_item=$[attr:offer-stat]&offer_id=$[attr:offerid]&offer_catid=$[attr:clickoffercatid]"],"t":"2","l":"","i":"15211"}],"2-breadcrumb":[{"d":["click_pos=$[attr:ctype]&click_value=$[attr:cvalue]"],"t":"2","l":"https://stat.1688.com/search/queryreport.html","i":"1606"}]},"ajaxexpo":{},"ajaxclick":{},"expo":[]});
 var _click_url ="https://stat\.1688\.com\/search\/queryreport\.html";
 var _expo_url ="https://ctr.1688.com/ctr.html";
}catch(e){}</script>
<script type="text/javascript">
(function() {
var el=document.getElementById('easytraceJS');if(el)return;
el=document.createElement('script');el.id='easytraceJS'; el.type = 'text/javascript'; el.async = true;
el.src = 'https://astyle.alicdn.com/app/tools/js/click/click-20121008.js'; 
document.body.appendChild(el);
})();</script>

    '''
    sel=Selector(text=ttt)

    for company_item in sel.xpath('//li[@class="company-list-item"]'):
        dict_1=AlishopSpider().jixi(company_item)
        print(dict_1)