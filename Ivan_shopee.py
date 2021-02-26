# -*- coding: utf-8 -*-
"""
author:rifleak74,linzino
"""
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
from tqdm import tqdm
# selenium
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
import time
import re
import platform
import random

my_headers = {'authority' : 'shopee.tw',
     'method': 'GET',
     'path': '/api/v1/item_detail/?item_id=1147052312&shop_id=17400098',
     'scheme': 'https',
     'accept': '*/*',
     'accept-encoding': 'gzip, deflate, br',
     'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
     'cookie': '_ga=GA1.2.1087113924.1519696808; SPC_IA=-1; SPC_F=SDsFai6wYMRFvHCNzyBRCvFIp92UnuU3; REC_T_ID=f2be85da-1b61-11e8-a60b-d09466041854; __BWfp=c1519696822183x3c2b15d09; __utmz=88845529.1521362936.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _atrk_siteuid=HEgUlHUKcEXQZWpB; SPC_EC=-; SPC_U=-; SPC_T_ID="vBBUETICFqj4EWefxIdZzfzutfKhrgytH2wyevGxiObL3hFEfy0dpQSOM/yFzaGYQLUANrPe7QZ4hqLZotPs72MhLd8aK0qhIwD5fqDrlRs="; SPC_T_IV="IpxA2sGrOUQhMH4IaolDSA=="; cto_lwid=2fc9d64c-3cfd-4cf9-9de7-a1516b03ed79; csrftoken=EDL9jQV76T97qmB7PaTPorKtfMlU7eUO; bannerShown=true; _gac_UA-61915057-6=1.1529645767.EAIaIQobChMIwvrkw8bm2wIVkBiPCh2bZAZgEAAYASAAEgIglPD_BwE; _gid=GA1.2.1275115921.1529896103; SPC_SI=2flgu0yh38oo0v2xyzns9a2sk6rz9ou8; __utma=88845529.1087113924.1519696808.1528465088.1529902919.7; __utmc=88845529; appier_utmz=%7B%22csr%22%3A%22(direct)%22%2C%22timestamp%22%3A1529902919%7D; _atrk_sync_cookie=true; _gat=1',
     'if-none-match': "55b03-9ff4fb127aff56426f5ec9022baec594",
     'referer': 'https://shopee.tw/6-9-%F0%9F%87%B0%F0%9F%87%B7%E9%9F%93%E5%9C%8B%E9%80%A3%E7%B7%9A-omg!%E6%96%B0%E8%89%B2%E7%99%BB%E5%A0%B4%F0%9F%94%A5%E4%BA%A4%E5%8F%89%E7%BE%8E%E8%83%8CBra%E5%BD%88%E5%8A%9B%E8%83%8C%E5%BF%83-i.17400098.1147052312',
     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
     'x-api-source': 'pc',
     'x-requested-with': 'XMLHttpRequest'
      }     


# exception
class Error(Exception):
    """Base class for all exceptions raised by this module"""
    pass

class UnknownUrlType(Error):
    """Unknow url's Type, except 'posts', 'photos' or 'videos'. """
    pass

class PageNotFound(Error):
    """Can not fetch page by given url"""
    pass

class NotFoundProduct(Error):
    """Can not found any product"""
    pass
            
class productDetail:
    def __init__(self, item_id = '106182554', shop_id = '4929170'):
        self.item_id = item_id
        self.shop_id = shop_id
        
    # 進入每個商品，抓取買家留言
    def goods_comments(self):
        url = 'https://shopee.tw/api/v1/comment_list/?item_id='+ str(self.item_id) + '&shop_id=' + str(self.shop_id) + '&offset=0&limit=200&flag=1&filter=0'
        r = requests.get(url,headers = my_headers)
        st= r.text.replace("\\n","^n")
        st=st.replace("\\t","^t")
        st=st.replace("\\r","^r")
        
        gj=json.loads(st)
        return gj['comments']
    
    # 進入每個商品，抓取賣家更細節的資料（商品文案、SKU）
    def goods_detail(self):
        url = 'https://shopee.tw/api/v2/item/get?itemid=' + str(self.item_id) + '&shopid=' + str(self.shop_id)
        r = requests.get(url,headers = my_headers)
        st= r.text.replace("\\n","^n")
        st=st.replace("\\t","^t")
        st=st.replace("\\r","^r")
        
        gj=json.loads(st)
        return gj

    def __repr__(self):
        return 'productDetail("{}")'.format(self.item_id)
    
    def __str__(self):
        return '商品ID：' + self.item_id

class search:
    '''
    快速爬取API
    每次請求最多可以請求100個商品，但沒有商品文案、SKU、TAG等等
    '''
    def __init__(self, keyword = '關鍵字', page=0):
            self.keyword = keyword
            self.page = page
            
    #專門用來請求蝦皮
    def request_shopee(self):
        url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=' + self.keyword + '&limit=100&newest=' + str(self.page*100) + '&order=desc&page_type=search&version=2'
        #開始請求
        list_req = requests.get(url,headers = my_headers)
        soup = BeautifulSoup(list_req.content, "html.parser")
        #將扒下來的文字轉成Json
        getjson=json.loads(soup.text)
        
        return getjson
    
    
    #抓到該關鍵字共有多少商品
    def get_all_number(self):
        getjson = search(self.keyword, self.page).request_shopee()
        return getjson['total_count']
    
    def __repr__(self):
        return 'search("{}")'.format(self.keyword)
    
    def __str__(self):
        return '關鍵字：' + self.keyword


class Crawler:
    #開啟selenium的driver
    def __init__(self, keyword = '關鍵字', page='頁數'):
        self.keyword = keyword
        self.page = page
        
        # 判斷是甚麼作業系統，決定selenium使用的工具
        theOS = list(platform.uname())[0]
        if theOS == 'Windows':
            theOS = theOS + '\\'
            self.ecode = 'utf-8-sig'
        else:
            theOS = theOS + '/'
            self.ecode = 'utf-8'
        
        # 設定基本參數
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        #此處必須換成自己電腦的User-Agent
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        
        # PhantomJS driver 路徑 似乎只能絕對路徑
        self.driver = webdriver.PhantomJS(executable_path = theOS+'phantomjs', desired_capabilities=desired_capabilities)
        
        # 關閉通知提醒
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        
        # 開啟瀏覽器
        self.driver = webdriver.Chrome(theOS+'chromedriver',chrome_options=chrome_options)
        time.sleep(5)
        
    def shopee(self):
        self.driver.get('https://shopee.tw/search?keyword=' + self.keyword )
        time.sleep(2)
        
        # 檢查有沒有頁數xl，沒有頁數代表沒資料
        if len(self.driver.find_elements_by_class_name('shopee-mini-page-controller__total')) == 0:
            raise NotFoundProduct
            
        # 若沒有給頁數，直接抓到尾頁
        if self.page == '頁數':
            self.page = int(self.driver.find_element_by_class_name('shopee-mini-page-controller__total').text)

        print('---------- 開始進行爬蟲 ----------')
        tStart = time.time()#計時開始
        
        container_product = pd.DataFrame()
        container_comment = pd.DataFrame()
        for i in range(int(self.page)):

            itemid = []
            shopid =[]
            name = []
            brand = []
            stock = []
            price = []
            ctime = []
            currency = []
            description = []
            discount = []
            can_use_bundle_deal = []
            can_use_wholesale = []
            tier_variations = []
            hashtag_list = []
            historical_sold = []
            is_cc_installment_payment_eligible = []
            is_official_shop = []
            is_pre_order = []
            is_slash_price_item = []
            liked_count = []
            shop_location = []
            SKU = []
            view_count = []
            cmt_count = []
            five_star = []
            four_star = []
            three_star = []
            two_star = []
            one_star = []
            rating_star = []
            rcount_with_context =[]
            rcount_with_image =[]
            
            self.driver.get('https://shopee.tw/search?keyword=' + self.keyword + '&page=' + str(i))
        
            # 滾動頁面
            for scroll in range(6):
                self.driver.execute_script('window.scrollBy(0,1000)')
                time.sleep(2)
            
            #取得商品內容
            for item, thename in zip(self.driver.find_elements_by_xpath('//*[@data-sqe="link"]'), self.driver.find_elements_by_xpath('//*[@data-sqe="name"]')):
                #商品ID、商家ID
                getID = item.get_attribute('href')
                theitemid = int((getID[getID.rfind('.')+1:]))
                theshopid = int(getID[ getID[:getID.rfind('.')].rfind('.')+1 :getID.rfind('.')]) 
                itemid.append(theitemid)
                shopid.append(theshopid)
                
                #商品名稱
                getname = thename.text.split('\n')[0]
                name.append(getname)
                
                #價格
                thecontent = item.text
                thecontent = thecontent[(thecontent.find(getname)) + len(getname):]
                thecut = thecontent.split('\n')
        
                if re.search('市|區|縣|鄉|海外|中國大陸', thecontent): #有時會沒有商品地點資料
                    if re.search('已售出', thecontent): #有時會沒銷售資料
                        if '出售' in thecut[-3][1:]:
                            theprice = thecut[-4][1:]
                        else:
                            theprice = thecut[-3][1:]
        
                    else:
                        theprice = thecut[-2][1:]
                else:
                    if re.search('已售出', thecontent): #有時會沒銷售資料
                        theprice = thecut[-2][1:]
                    else:
                        theprice = thecut[-1][1:]
                        
                theprice = theprice.replace('$','')
                theprice = theprice.replace(',','')
                theprice = theprice.replace('售','')
                theprice = theprice.replace('出','')
                theprice = theprice.replace(' ','')
                if ' - ' in theprice:
                    theprice = (int(theprice.split(' - ')[0]) +int(theprice.split(' - ')[1]))/2
                if '-' in theprice:
                    theprice = (int(theprice.split('-')[0]) +int(theprice.split('-')[1]))/2
                price.append(int(theprice))
                
                #請求商品詳細資料
                itemDetail = productDetail(item_id = theitemid, shop_id = theshopid).goods_detail()['item']
                
                brand.append(itemDetail['brand']) #品牌
                stock.append(itemDetail['stock']) #存貨數量
                ctime.append(itemDetail['ctime']) #上架時間
                currency.append(itemDetail['currency']) #交易貨幣種類
                description.append(itemDetail['description']) #商品文案
                discount.append(itemDetail['discount']) #折數
                can_use_bundle_deal.append(itemDetail['can_use_bundle_deal']) #可否搭配購買
                can_use_wholesale.append(itemDetail['can_use_wholesale']) #可否大量批貨購買
                tier_variations.append(itemDetail['tier_variations']) #選項
                hashtag_list.append(itemDetail['hashtag_list']) #tag
                historical_sold.append(itemDetail['historical_sold']) #歷史銷售量
                is_cc_installment_payment_eligible.append(itemDetail['is_cc_installment_payment_eligible']) #可否分期付款
                is_official_shop.append(itemDetail['is_official_shop']) #是否官方賣家帳號
                is_pre_order.append(itemDetail['is_pre_order']) #是否可預購
                is_slash_price_item.append(itemDetail['is_slash_price_item']) #是否減價
                liked_count.append(itemDetail['liked_count']) #喜愛數量
                
                #SKU
                all_sku=[]
                for sk in itemDetail['models']:
                    all_sku.append(sk['name'])
                SKU.append(all_sku) #SKU
                view_count.append(itemDetail['view_count']) #瀏覽人數
                shop_location.append(itemDetail['shop_location']) #商家地點
                cmt_count.append(itemDetail['cmt_count']) #評價數量
                five_star.append( itemDetail['item_rating']['rating_count'][5] ) #五星
                four_star.append( itemDetail['item_rating']['rating_count'][4] ) #四星
                three_star.append( itemDetail['item_rating']['rating_count'][3] ) #三星
                two_star.append( itemDetail['item_rating']['rating_count'][2] ) #二星
                one_star.append( itemDetail['item_rating']['rating_count'][1] ) #一星
                rating_star.append(itemDetail['item_rating']['rating_star']) #評分
                rcount_with_context.append(itemDetail['item_rating']['rcount_with_context']) #附上評論
                rcount_with_image.append(itemDetail['item_rating']['rcount_with_image']) #附上圖片
                
                #評論詳細資料
                iteComment = productDetail(item_id = theitemid, shop_id = theshopid).goods_comments()
                userid = [] #使用者ID
                anonymous = [] #是否匿名
                commentTime = [] #留言時間
                is_hidden = [] #是否隱藏
                orderid = [] #訂單編號
                comment_rating_star = [] #給星
                comment = [] #留言內容
                product_SKU = [] #商品規格
                
                for comm in iteComment:
                    userid.append(comm['userid'])
                    anonymous.append(comm['anonymous'])
                    commentTime.append(comm['ctime'])
                    is_hidden.append(comm['is_hidden'])
                    orderid.append(comm['orderid'])
                    comment_rating_star.append(comm['rating_star'])
                    try:
                        comment.append(comm['comment'])
                    except:
                        comment.append(None)
                    
                    p=[]
                    for pro in comm['product_items']:
                        try:
                            p.append(pro['model_name'])
                        except:
                            p.append(None)
                            
                    product_SKU.append(p)
                    
                commDic = {
                    '商品ID':[ theitemid for x in range(len(iteComment)) ],
                    '賣家ID':[ theshopid for x in range(len(iteComment)) ],
                    '商品名稱':[ getname for x in range(len(iteComment)) ],
                    '價格':[ int(theprice) for x in range(len(iteComment)) ],
                    '使用者ID':userid,
                    '是否匿名':anonymous,
                    '留言時間':commentTime,
                    '是否隱藏':is_hidden,
                    '訂單編號':orderid,
                    '給星':comment_rating_star,
                    '留言內容':comment,
                    '商品規格':product_SKU
                    }

                container_comment = pd.concat([container_comment,pd.DataFrame(commDic)], axis=0)
                
            dic = {
                    '商品ID':itemid,
                    '賣家ID':shopid,
                    '商品名稱':name,
                    '品牌':brand,
                    '存貨數量':stock,
                    '價格':price,
                    '上架時間':ctime,
                    '交易貨幣種類':currency,
                    '商品文案':description,
                    '折數':discount,
                    '可否搭配購買':can_use_bundle_deal,
                    '可否大量批貨購買':can_use_wholesale,
                    '選項':tier_variations,
                    'Tag':hashtag_list,
                    '歷史銷售量':historical_sold,
                    '可否分期付款':is_cc_installment_payment_eligible,
                    '是否官方賣家帳號':is_official_shop,
                    '是否可預購':is_pre_order,
                    '是否減價':is_slash_price_item,
                    '喜愛數量':liked_count,
                    '商家地點':shop_location,
                    'SKU':SKU,
                    '瀏覽人數':view_count,
                    '評價數量':cmt_count,
                    '五星':five_star,
                    '四星':four_star,
                    '三星':three_star,
                    '二星':two_star,
                    '一星':one_star,
                    '評分':rating_star,
                    '附上評論':rcount_with_context,
                    '附上圖片':rcount_with_image
                    }

            #資料整合
            container_product = pd.concat([container_product,pd.DataFrame(dic)], axis=0)
            #暫時存檔紀錄
            container_product.to_csv('shopeeAPIData'+str(i+1)+'_Product.csv', encoding = self.ecode)
            container_comment.to_csv('shopeeAPIData'+str(i+1)+'_Comment.csv', encoding = self.ecode)
        
            print('目前累積商品： ' + str(len(container_product)) + ' 留言累積' + str(len(container_comment)))
            time.sleep(random.randint(5,10))
        
        container_product.to_csv(self.keyword +'_商品資料.csv', encoding = self.ecode)
        container_comment.to_csv(self.keyword +'_留言資料.csv', encoding = self.ecode)
        
        tEnd = time.time()#計時結束
        totalTime = int(tEnd - tStart)
        minute = totalTime // 60
        second = totalTime % 60
        print('資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')
        
    def __repr__(self):
        return 'Crawler("{}")'.format(self.keyword)
    
    def __str__(self):
        return '關鍵字：' + self.keyword + '\n頁數：' + self.page

def main():
    print('\n請輸入您想爬的商品關鍵字：')
    keyword = input() 
    
    print('\n請輸入您想爬幾頁：')
    page = input()
    
    Crawler(keyword = keyword, page=page).shopee()
    
   
        
if __name__ == '__main__':
    main()
