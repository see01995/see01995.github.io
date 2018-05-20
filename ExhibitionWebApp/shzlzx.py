from selenium import webdriver  
import selenium
import re
import json
   
#chromedriver = r"C:\Users\Sun\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\selenium\chromedriver.exe"  
chromedriver = r"D:\test\chromedriver.exe"  

browser = webdriver.Chrome(chromedriver)  

url = "http://www.shzlzx.com.cn/shzlzx/page/exhibitor.htm"

page_num = 1

def get_expo_list(page):
    browser.get("http://www.shzlzx.com.cn/shzlzx/page/exhibitor_cn.htm")  
    expo_list = browser.find_elements_by_tag_name("tbody")[2].find_elements_by_tag_name('tr')
    #expo_list = browser.find_elements_by_tag_name("iframe")
    print(len(expo_list))
    page_json = []
    for idx,expo in enumerate(expo_list):
        info_list = expo.find_elements_by_tag_name("td")
        item_json = dict()
        item_json.update({"name":"上海展览中心"})
        item_json.update({"show":info_list[1].text})
        item_json.update({"addr":"上海市静安区延安中路1000号"})
        item_json.update({"url":browser.current_url})
        item_json.update({"hall":"无信息"})
        date_info = info_list[0].text.split('-')
        for idx,date in enumerate(date_info):
            temp = date.split(".")
            if(len(temp[0])==1):
                temp[0] = "0"+temp[0]
            if(len(temp[1])==1):
                temp[1] = "0"+temp[1]
            date_info[idx] = temp[0]+"/"+temp[1]
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
            if(month in "2018/"+item["start"]):
                print('ok')
                expo_json['2018'][str(m+1)].append(item)
    print(expo_json)
    print(len(expo_json))
print(expo_json)

browser.quit()  

fp = open('shzlzx.json','w')
json.dump(expo_json,fp)
fp.close()
