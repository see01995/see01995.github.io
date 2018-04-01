from selenium import webdriver  
import selenium
import re
import json
   
chromedriver = r"C:\Users\Sun\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\selenium\chromedriver.exe"  

browser = webdriver.Chrome(chromedriver)  
   
def get_expo_list(year,month):
    browser.get("http://www.shexpocenter.com/ExAgenda.aspx?Year={}&month={}".format(year,month))  
    month_json = []
    while(True):
        info_list = browser.find_elements_by_class_name("hotel_link")
        for info in info_list:
            print(info.text)
        for i in range(len(info_list)//4):
            item_json = dict()
            item_json.update({"name":"上海世博展览馆"})
            item_json.update({"show":info_list[i*4+0].text})
            item_json.update({"addr":"上海市浦东新区国展路1099号"})
            item_json.update({"url":browser.current_url})
            item_json.update({"hall":info_list[i*4+3].text})
            date_info = info_list[i*4+1].text.replace('.','/').split('--')
            item_json.update({"start":date_info[0]})
            item_json.update({"end":date_info[1]})
            month_json.append(item_json)

        try:
            page_ele = browser.find_element_by_id("tbPager")
        except selenium.common.exceptions.NoSuchElementException:
            break
        m=re.search("第(?P<now_page>[0-9])页/共(?P<last_page>[0-9])页",page_ele.find_element_by_tag_name("span").text)
        if(m!=None):
            print(m.groups())
            if(m.group('now_page') == m.group('last_page')):
                break
            else:
                btn_next = browser.find_element_by_id("gvEx_ctl11_lbnNext")
                btn_next.click()
        else:
            break
    return month_json

expo_json = dict()
expo_json['2018'] = dict()
for i in range(12):
    expo_month_json = get_expo_list('2018',str(i+1))
    expo_json['2018'][str(i+1)] = expo_month_json
    print(expo_json)
print(expo_json)

browser.quit()  

fp = open('shexpo.json','w')
json.dump(expo_json,fp)
fp.close()
