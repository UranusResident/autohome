# -*- coding: utf-8 -*-
#from scrapy.selector import Selector
from scrapy.spiders import Spider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from cardata.items import CardataItem
import scrapy
from scrapy import log
import re

from bs4 import  BeautifulSoup

import sys
reload(sys)  
sys.setdefaultencoding('utf-8')

class CommentSpider(Spider):
    name = "car"
    allowed_domains = ["autohome.com.cn"]
    start_urls=["http://www.autohome.com.cn/suv/#pvareaid=103421"]


    rules=[
        Rule(SgmlLinkExtractor(allow=('/suv/', )), callback='getContent'),
        Rule(SgmlLinkExtractor(allow=('/stopselling/', )), callback='parse'),
    ]


    def parse(self,response):


        allCon=response.selector.xpath('//div[@class="tab-content"]/div/div[@class="uibox"]')

        for ulbox in allCon:
            if ulbox is not None:
                car_name=ulbox.xpath('//div[@class="uibox-con rank-list rank-list-pic"]/dl/dd/div[@class="h3-tit"]/text()')
                #print 'name====>',car_name
                
                teach_price=ulbox.xpath('//div[@class="uibox-con rank-list rank-list-pic"]/dl/dd/ul[@class="rank-list-ul"]/li/div/a[@class="red"]/text()')
                #print 'price=====<',teach_price.extract()

                a_link=ulbox.xpath('//div[@class="uibox-con rank-list rank-list-pic"]/dl/dd/ul[@class="rank-list-ul"]/li/div/a[contains(@href, "k.autohome.com.cn")]/@href')

                #print "a_link====",a_link.extract() 
                for link in a_link:
                    
                    yield Request(link.extract(),callback=self.getContent)






    def getContent(self,response):

        reg=re.compile('\s+')

        item=CardataItem()


        #print '===========>',response.url

        #使用extract(),返回结果为单一化的unicode字符串列表。
        username=response.selector.xpath('//div[@class="usercont"]/div[@class="usercont-name fn-clear"]/div[@class="name-text"]/p/a/text()').extract()

        #print 'username=======',username
        item['car_owner']=username

        #混合使用BeautifulSoup
        soup = BeautifulSoup(response.body,"lxml")

        # con_info=soup.find('div',{'class':'mouthcon'}).find('div',{'class':'mouthcon-cont fn-clear'})
        con_info=soup.find_all('div',{'class':'mouthcon'})#.find_all('div',{'class':'mouthcon-cont fn-clear'})

        #print 'always========================>',con_info
        for sub_con_info in con_info:
            

        
            info=sub_con_info.find('div',{'class':'mouthcon-cont-left'}).find('div',{'class':'choose-con mt-10'})


            #print 'aaaa=============>',info


            if info is not None:
                
                dl=[dl.text for dl in info.find_all('dl')]

                #购买车型
                print 'car_type======>',re.sub(reg,'',dl[0])
                item['car_type']=re.sub(reg,'',dl[0])
                #购买地点
                print 'buy_car_address======>',re.sub(reg,'',dl[1])
                item['buy_car_address']=re.sub(reg,'',dl[1])
                #经销商
                print 'buy_car_dealer======>',re.sub(reg,'',dl[2])
                item['buy_car_dealer']=re.sub(reg,'',dl[2])
                #购车时间
                print 'buy_car_date======>',re.sub(reg,'',dl[3])
                item['buy_car_date']=re.sub(reg,'',dl[3])

                #油耗#目前行驶
                print 'oil_wear======>',re.sub(reg,'',dl[5])
                item['oil_wear']=re.sub(reg,'',dl[5])



                #空间
                print 'space======>',re.sub(reg,'',dl[6])
                item['space']=re.sub(reg,'',dl[6])

                #动力
                print 'power======>',re.sub(reg,'',dl[7])
                item['power']=re.sub(reg,'',dl[7])

                #操控
                print 'control======>',re.sub(reg,'',dl[8])
                item['control']=re.sub(reg,'',dl[8])

                #油耗（评分）
                print 'oil_wear_star======>',re.sub(reg,'',dl[9])
                item['oil_wear_star']=re.sub(reg,'',dl[9])

                #舒适性
                print 'confort======>',re.sub(reg,'',dl[10])
                item['confort']=re.sub(reg,'',dl[10])

                #外观 
                print 'shape======>',re.sub(reg,'',dl[11])
                item['shape']=re.sub(reg,'',dl[11])

                #内饰
                print 'trim======>',re.sub(reg,'',dl[12])
                item['trim']=re.sub(reg,'',dl[12])

                #性价比
                print 'cost_effective======>',re.sub(reg,'',dl[13])
                item['cost_effective']=re.sub(reg,'',dl[13])


            #购车目的
            mouthcon_cont_left=sub_con_info.find('div',{'class':'mouthcon-cont-left'})
            if mouthcon_cont_left is not None:
                mt_10=mouthcon_cont_left.find('div',{'class':'choose-con mt-10'})
                if mt_10 is not None:
                    aim=mt_10.find('dl',{'class':'choose-dl border-b-no'})
                    if aim is not None:
                        print 'aim======>',re.sub(reg,'',aim.get_text())
                        item['buy_car_aim']=re.sub(reg,'',aim.get_text())


            #评论
            al=sub_con_info.find('div',{'class':'mouthcon-cont-right commentParentBox'})
            if al is not None:
                con_comment=al.find('div',{'class':'mouth-main'})
                if con_comment is not None:
                    mouth_item=con_comment.find('div',{'class':'mouth-item'})
                    if mouth_item is not None:
                        comment_title=mouth_item.find('div',{'class':'cont-title fn-clear'})#.get_text()
                        #评论标题
                        if comment_title is not None:

                            item['comment_title']=re.sub(reg,'',comment_title.get_text())

                            print 'comment_title======>',re.sub(reg,'',comment_title.get_text())

                        comment_text=mouth_item.find('div',{'class':'text-con height-list'})

                        #评论内容
                        if comment_text is not None:

                            item['comment_content']=re.sub(reg,'',comment_text.get_text())

                            print 'comment_content======>',item['comment_content']


                        yield item


        
        



        








        # start_index = Url.find('comments')
        # URL = Url[0:start_index+8]
        # ID = filter(str.isdigit,URL)
        # comment_item=sel.xpath('//*[@class="comment"]')
        # for items in comment_item:
        #     item = DoubantestItem()
        #     item['ID']=ID
        #     item['user_name']=items.xpath('h3/span[@class="comment-info"]/a/text()').extract()
        #     score=items.xpath('h3/span[@class="comment-info"]').xpath('span[2]/@title')

        #     item['user_score']=score.extract()
        #     item['comment_data']=items.xpath('h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').extract()
        #     item['comment']=items.xpath('p/text()').extract()
        #     yield item


        # for url in sel.xpath("//*[@class='next']/@href").extract():
        #     yield Request(URL+url,callback=self.parse,meta={'cookiejar': response.meta['cookiejar']})




