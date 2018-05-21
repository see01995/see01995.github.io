from selenium import webdriver  
import selenium
import re
import json
   
#chromedriver = r"C:\Users\Sun\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\selenium\chromedriver.exe"  
chromedriver = r"D:\test\chromedriver.exe"  

browser = webdriver.Chrome(chromedriver)  

url = "http://www.szcec.com.cn/szcec/page/exhibitor.htm"

page_num = 1

import sys

def get_expo_list(page):
    browser.get("http://www.szcec.com/Schedule/index.html")  
    expo_list = browser.find_elements_by_tag_name("td")
    #expo_list = browser.find_elements_by_tag_name("iframe")
    print(len(expo_list))
    page_json = []
    for idx,expo in enumerate(expo_list):
        if("日-" not in expo.text):
            continue
        item_json = dict()
        item_json.update({"name":"深圳会展中心"})
        item_json.update({"show":expo_list[idx-1].text})
        item_json.update({"addr":"深圳市福田区福华三路深圳会展中心"})
        item_json.update({"url":browser.current_url})
        item_json.update({"hall":"无信息"})
        date_info = expo.text.split('-')
        for idx,date in enumerate(date_info):
            temp = date.replace("月","/")
            temp = temp.replace("日","")
            date_info[idx] = "2018/"+temp
        item_json.update({"start":date_info[0]})
        item_json.update({"end":date_info[1]})
        page_json.append(item_json)

    return page_json

def gen_expo_list_by_month(expo_list,year,month):
    pass

expo_json = dict()
expo_json['2018'] = dict()
for m in range(12):
    expo_json['2018'][str(m+1)] = list()
for i in range(page_num):
    expo_page_json = get_expo_list(str(i+1))
    print('-----------------')
    print(len(expo_page_json))
    for m in range(12):
        month = "2018/{:02d}/".format(m+1)
        print('month={:s}'.format(month))
        for item in expo_page_json:
            print(item["start"])
            if(month in item["start"]):
                print('ok')
                expo_json['2018'][str(m+1)].append(item)
    print(expo_json)
    print(len(expo_json))
print(expo_json)

browser.quit()  

fp = open('szcec.json','w')
json.dump(expo_json,fp)
fp.close()
