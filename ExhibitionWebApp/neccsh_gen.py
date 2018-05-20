from selenium import webdriver  
import selenium
import re
import json
   
#chromedriver = r"C:\Users\Sun\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\selenium\chromedriver.exe"  
chromedriver = r"D:\test\chromedriver.exe"  

browser = webdriver.Chrome(chromedriver)  

browser.get("http://www.neccsh.com/cecsh/exhibitioninfo/exhibitionlist.jspx?v=1&startday=&exhiNumStr=null&exhiName=&pageNo={}".format('1'))  
page_num = len(browser.find_elements_by_class_name("page-news-list")[0].find_elements_by_tag_name('option'))
print(page_num)

def get_expo_list(page):
    browser.get("http://www.neccsh.com/cecsh/exhibitioninfo/exhibitionlist.jspx?v=1&startday=&exhiNumStr=null&exhiName=&pageNo={}".format(page))  
    expo_list = browser.find_elements_by_class_name("events-info-list")
    name_list = browser.find_elements_by_class_name("page-news-list")[0].find_elements_by_tag_name('h3')
    print(len(expo_list))
    print(len(name_list))
    page_json = []
    for idx,expo in enumerate(expo_list):
        info_list = expo.find_elements_by_tag_name("li")
        item_json = dict()
        item_json.update({"name":"国家会展中心(上海)"})
        item_json.update({"show":name_list[idx].text})
        item_json.update({"addr":"上海市崧泽大道333号"})
        item_json.update({"url":browser.current_url})
        item_json.update({"hall":info_list[1].text.replace("展厅：","")})
        date_info = info_list[0].text.replace("时间：","").split(' -- ')
        item_json.update({"start":date_info[0].replace('-','/')})
        item_json.update({"end":date_info[1].replace('-','/')})
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
        print('month={:02d}'.format(m+1))
        month = "2018/{:02d}/".format(m+1)
        print(month)
        for item in expo_page_json:
            print(item["start"])
            if(month in item["start"]):
                print('ok')
                expo_json['2018'][str(m+1)].append(item)
    print(expo_json)
    print(len(expo_json))
print(expo_json)

browser.quit()  

fp = open('neccsh.json','w')
json.dump(expo_json,fp)
fp.close()
