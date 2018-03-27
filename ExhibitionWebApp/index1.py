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

class item_info(expo_info):
    def gen_li(self):
        item_title = HTML.A(self.show,href=self.url)
        item_text1  = HTML.DIV('展馆：{}'.format(self.name),Class='am-list-item-text')
        item_text2  = HTML.DIV('时间：{}-{}'.format(self.startdate.strftime('%Y/%m/%d'),self.enddate.strftime('%Y/%m/%d')),Class='am-list-item-text')
        item_text3  = HTML.DIV('展厅：{}'.format(self.hall),Class='am-list-item-text')
        item_text4  = HTML.DIV('地址：{}'.format(self.addr),Class='am-list-item-text')
        list_item  = HTML.LI('',Class='am-g am-list-item-desced')
        list_item <= item_title
        list_item <= item_text1
        list_item <= item_text2
        list_item <= item_text3
        list_item <= item_text4
        return list_item

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

def refresh():
    expo_list = []
    lines = get_file_text('sneic.json')
    #print(lines)
    expo_json = json.loads(lines)
    print(expo_json)
    document['expo_list'].clear()
    for item in document.get(name="cbx"):
        if(item.checked==True):
            expo_list += get_expo_list(item.value)
    for expo in expo_list:
        #expo.show_info()
        document['expo_list'] <= expo.gen_li()

def onPlaceSelected(ev):
    refresh()
jq('#my-popup').on('close.modal.amui',onPlaceSelected)

def onDateChanged(ev):
    refresh()
jq('#datepicker').datetimepicker().on('changeDate',onDateChanged)

now = datetime.now().date().strftime('%Y-%m')
jq('#datepicker').datetimepicker('update',now)
refresh()


