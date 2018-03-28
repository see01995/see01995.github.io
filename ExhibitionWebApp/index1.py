from browser import document, alert, window
from browser import html as HTML
from urllib import request
import re
import json
from datetime import *
import time

#from log import *
from expo_info import *

jq = window.jQuery

jq('#datepicker').datetimepicker({'format': 'yyyy-mm',
                                  'autoclose': 'true',
                                  'viewMode': 'years',
                                  'minView': 'months',
                                  'viewSelect': 'years',
                                  'todayHighlight': 'true',
                                  'todayBtn': 'true'})

def add_place(name,abb,default=False):
    place_label = HTML.LABEL(name,Class='am-checkbox')
    if(default == True):
        place_ckbox = HTML.INPUT('',Type='checkbox',Value=abb,Name='cbx',Checked=True)#,Data-am-ucheck='')
    else:
        place_ckbox = HTML.INPUT('',Type='checkbox',Value=abb,Name='cbx')#,Data-am-ucheck='')
    place_label <= place_ckbox
    return place_label

document['place_list'] <= add_place('上海新国际博览中心','SNIEC')

def get_file_text(file_name):
    fake_qs = '?foo={}'.format(time.time())
    return open(file_name+fake_qs).read()

def gen_li(item):
    item_title = HTML.A(item['show'],href=item['url'])
    item_text1  = HTML.DIV('展馆：{}'.format(item['name']),Class='am-list-item-text')
    item_text2  = HTML.DIV('时间：{}-{}'.format(item['start'],item['end']),Class='am-list-item-text')
    item_text3  = HTML.DIV('展厅：{}'.format(item['hall']),Class='am-list-item-text')
    item_text4  = HTML.DIV('地址：{}'.format(item['addr']),Class='am-list-item-text')
    list_item  = HTML.LI('',Class='am-g am-list-item-desced')
    list_item <= item_title
    list_item <= item_text1
    list_item <= item_text2
    list_item <= item_text3
    list_item <= item_text4
    return list_item

def show_expo_list(li):
    for i in li:
        print("-----------------------")
        print("name  : {}".format(i['name']))
        print("show  : {}".format(i['show']))
        print("addr  : {}".format(i['addr']))
        print("url   : {}".format(i['url']))
        print("hall  : {}".format(i['hall']))
        print("start : {}".format(i['start']))
        print("end   : {}".format(i['end']))

def refresh():
    expo_list = []
    document['expo_list'].clear()

    date_info = document['datepicker'].value.split('-') #0:year,1:month
    lines = get_file_text('sniec.json')
    expo_list_year = json.loads(lines)[date_info[0]]
    show_expo_list(expo_list_year)
    expo_list += list(filter(lambda x: (x['start'][:7]==date_info[0]+'/'+date_info[1])or(x['end'][:7]==date_info[0]+'/'+date_info[1]),expo_list_year))
    show_expo_list(expo_list)
    #for item in document.get(name="cbx"):
    #    if(item.checked==True):
    #        expo_list += json_list.find(name==item.value)
    for expo in expo_list:
        document['expo_list'] <= gen_li(expo)

def onPlaceSelected(ev):
    refresh()
jq('#my-popup').on('close.modal.amui',onPlaceSelected)

def onDateChanged(ev):
    refresh()
jq('#datepicker').datetimepicker().on('changeDate',onDateChanged)

now = datetime.now().date().strftime('%Y-%m')
jq('#datepicker').datetimepicker('update',now)
refresh()


