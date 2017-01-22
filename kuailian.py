# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import traceback
import re

def get_info(soup):
    
    huiyuan  = soup.find_all('div',style="text-align:left;width:120px;margin-top:15px;")

    huiyuan_info_list = []
    if len(huiyuan) != 0:
        for huiyuan_info in huiyuan[0]('p'):
            huiyuan_info_list.append(huiyuan_info('span')[0].text)
        
    return huiyuan_info_list
    
    

def get_user(soup):
        huiyuan  = soup.find_all('div',class_="huiyuan")
        DAUInfo = huiyuan[1].find_all('div',class_="DVUInfo")
        
        user_info_list = []
        if len(DAUInfo) != 0:
            for info in DAUInfo[0].ul('li'):
                user_info_list.append(info.text.split(u'：')[1])
        return user_info_list
        
        
        
def get_yaoqiu(soup):
    yaoqiu = soup.find_all('ul',style="margin-top: 15px;")
    
    yaoqiu_info_list = []
    if len(yaoqiu) != 0:
        for yaoqiu_info in yaoqiu[0]('li'):
    
            if len(yaoqiu_info('span')) == 2:
                yaoqiu_info_list.append(yaoqiu_info('span')[0].text)
                yaoqiu_info_list.append(yaoqiu_info('span')[1].text)
            else:
                yaoqiu_info_list.append(yaoqiu_info('span')[0].text)
            
    return yaoqiu_info_list

def get_yaoqiu_text(soup):
    yaoqiu_text = soup.find_all('span',id='lbAskToOther')
    if len(yaoqiu_text) != 0:
        return re.sub(r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', yaoqiu_text[0].text) 
    else:
        return u""

        
            

if __name__ == '__main__':  
    f = open("./test.csv", "a")  
    f.write('url|姓名|ID|卡别|登陆|到店|关注的人|关注她的人|昵称|性别|年龄|身高|学历|月薪|京房|购车|户籍|婚状|职业|属相|星座|对方最小年龄|对方最大年龄|对方最低身高|对方最高身高|对方学历|对方婚状|择偶要求\r\n')

    
    
    for i in range(166560,177900):
        try:
            r = requests.get("http://www.kl.cc/"+str(i))
            soup = BeautifulSoup(r.text,"html5lib") 
            f.write("\r\n")
            print i
            
            
            f.write(str(i)+"|")
            for info in get_info(soup):
                
                f.write(info.encode('utf8')+"|")

                


            for user in get_user(soup):
                f.write(user.encode('utf8')+"|")

                

            for yaoqiu in get_yaoqiu(soup):
                f.write(yaoqiu.encode('utf8')+"|")

            
            
            yaoqiu_text = get_yaoqiu_text(soup)
            
            f.write(yaoqiu_text.encode('utf8'))
            
            
        except Exception, e:
            print e
            print traceback.format_exc()
    f.close()



