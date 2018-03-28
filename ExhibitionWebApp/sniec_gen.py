from urllib import request
import re
from datetime import *
import json

#from log import *
from expo_info import *

pattern = {
"SNIEC":{
    "name": "上海新国际博览中心",
    "url": "http://www.sniec.net",
    "addr": "中国上海浦东新区龙阳路2345号",
    "url_pattern": "http://www.sniec.net/cn/visit_exhibition.php?month={year}-{month:02d}",
    "refine_pattern": ['<h1>(?P<showname>.*?)</h1>',
                       '<span>展厅 *(?P<hall>.*?) *\| *(?P<startdate>.*?) - (?P<enddate>.*?)</span>'],
    #"info_pattern": "<h1>(?P<showname>.*?)</h1>.*?<span>展厅 *(?P<hall>.*?) *\| *(?P<startdate>.*?) - (?P<enddate>.*?)</span>",
    "info_pattern": "<h1>(?P<showname>.*?)</h1>.*?<span>展厅 *(?P<hall>.*?) *\| *(?P<startdate>.*?) - (?P<enddate>.*?)</span>",
    "date_pattern": "%Y/%m/%d",
    "page_pattern": "<div class=\"pn\">[0-9]/(?P<page>[0-9])</div>",
    "page_url_pattern": "http://www.sniec.net/cn/visit_exhibition.php?month={year}-{month:02d}&page={page}"
}
}

def gen_url_list(abb,year,month):
    url_list = []
    page_num = 1 
    url = pattern[abb]['url_pattern'].format(year=year,month=month)
    print('init_url:{}'.format(url))
    if(pattern[abb]['page_pattern'] != ""):
        page = request.urlopen(url)
        lines = page.read()
        m = re.search(pattern[abb]['page_pattern'].encode('utf-8'),lines,re.S)
        if(m != None):
            page_num = int(m.group('page'))
        print('page_num:{:d}'.format(page_num))
    if(page_num > 1):
        for i in range(page_num):
            url_list.append(pattern[abb]['page_url_pattern'].format(year=year,month=month,page=str(i+1)))
    else:
        url_list.append(url)
    return url_list

def get_expo_list(abb,year,month):
    expo_list = []
    url_list = gen_url_list(abb,year,month)

    for url in url_list:
        print(url)
        page = request.urlopen(url)
        print('urlopen done')
        lines = page.read().replace(b'&nbsp;',b'')
        print(len(lines))
        #fp = open(abb+str(year)+str(month)+'.html','wb')
        #fp.write(lines)
        #fp.close()
        match_list = re.findall(pattern[abb]['info_pattern'].encode('utf-8'),lines,re.S)
        for m in match_list:
            expo = expo_info(pattern[abb]['name'],pattern[abb]['addr'],url)
            expo.show       = m[0].decode() #showname
            expo.hall       = m[1].decode() #hall
            expo.startdate  = datetime.strptime(m[2].decode(),pattern[abb]['date_pattern']) #startdate
            expo.enddate    = datetime.strptime(m[3].decode(),pattern[abb]['date_pattern']) #enddate
            expo_list.append(expo)
        print('pattern search done')
        if(len(expo_list)==0):
            print("{}  {}/{}  无展会\n\n请确认下网址的正确性：\n\n{}".format(pattern[abb]['name'],year,month,url))
    return expo_list

if __name__ == '__main__' :
    now = datetime.now()
    expo_list = list()
    json_list = list()
    for key,place in pattern.items():
        for i in range(12):
            expo_list += get_expo_list(key,now.year,i+1)
    for expo in expo_list:
        expo.show_info()
        #expo.gen_json()
        json_list.append(expo.gen_json())

    print(json_list)
    fp = open('sneic.json','w')
    json.dump({str(now.year):json_list},fp)
    fp.close()
