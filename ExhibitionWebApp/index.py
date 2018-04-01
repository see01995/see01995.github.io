from browser import document, alert, window
from browser import html as HTML
import json

from expo_info import *

jq = window.jQuery

def add_place(name,abb,default=False):
    place_label = HTML.LABEL(name,Class='am-checkbox')
    print(abb)
    print(default)
    if(default == True):
        print('Checked')
        place_ckbox = HTML.INPUT('',Type='checkbox',Value=abb,Name='cbx',Checked='')
    else:
        print('Unchecked')
        place_ckbox = HTML.INPUT('',Type='checkbox',Value=abb,Name='cbx')
    place_label <= place_ckbox
    return place_label

document['place_list'] <= add_place('上海新国际博览中心','SNIEC',True)

def get_file_text(file_name):
    fake_qs = '?foo={}'.format(window.Date.new().getTime())
    print(file_name+fake_qs)
    return open(file_name+fake_qs).read()

def gen_li(item,level=''):
    item_title = HTML.A(item['show'],href=item['url'])
    item_text1  = HTML.DIV('展馆：{}'.format(item['name']),Class='am-list-item-text')
    time_text   = HTML.SPAN('时间：{}-{}'.format(item['start'],item['end']),Class=level)
    item_text2  = HTML.DIV('',Class='am-list-item-text')
    item_text2 <= time_text
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

def check_date(expo):
    now_date    = list(map(lambda x:int(x),document['datepicker'].value.split('-'))) #0:year,1:month,2:day
    start_date  = list(map(lambda x:int(x),expo['start'].split('/')))
    end_date    = list(map(lambda x:int(x),expo['end'].split('/')))
    now   = now_date[0]*10000 + now_date[1]*100 + now_date[2]
    start = start_date[0]*10000 + start_date[1]*100 + start_date[2]
    end   = end_date[0]*10000 + end_date[1]*100 + end_date[2]
    if(now>=start and now<=end):
        return 0
    elif(now<start):
        return start-now
    else:
        return -1

def refresh():
    print('refresh')
    expo_list = []
    document['expo_list'].clear()

    for item in document.get(name="cbx"):
        if(item.checked==True):
            date_info = document['datepicker'].value.split('-') #0:year,1:month,2:day
            lines = get_file_text(item.value.lower()+'.json')
            expo_list = json.loads(lines)[date_info[0]][str(int(date_info[1]))]
            #show_expo_list(expo_list_year)
            #expo_list += list(filter(lambda x: (x['start'][:7]==date_info[0]+'/'+date_info[1])or(x['end'][:7]==date_info[0]+'/'+date_info[1]),expo_list_year))
            #show_expo_list(expo_list)

    latest_expo = 1
    goto_li = ''
    for expo in expo_list:
        left_days = check_date(expo)
        if(left_days==0):
            li = gen_li(expo,'am-text-danger')
            document['expo_list'] <= li
            if(goto_li == ''):
                goto_li = li
        elif(left_days>0 and latest_expo==1):
            latest_expo = 0
            li = gen_li(expo,'am-text-success')
            document['expo_list'] <= li
            if(goto_li == ''):
                goto_li = li
        else:
            document['expo_list'] <= gen_li(expo)
    print('Hello world!')
    goto_li.scrollIntoView()

def onPlaceSelected(ev):
    refresh()
jq('#my-popup').on('close.modal.amui',onPlaceSelected)

def onDateChanged(ev):
    refresh()
jq('#datepicker').datepicker().on('changeDate.datepicker.amui',onDateChanged)

now = window.Date()
jq('#datepicker').datepicker('setValue',now)

list_height = document.documentElement.clientHeight - document['expo_list'].offsetTop
document['expo_list'].height=list_height-document['expo_list'].abs_left

refresh()
