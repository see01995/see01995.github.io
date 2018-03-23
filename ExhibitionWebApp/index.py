from browser import document, alert, window
from browser import html as HTML
from urllib import request
import re
from datetime import *

#from log import *

from pattern import *

jq = window.jQuery

jq('#datepicker').datetimepicker({'format': 'yyyy-mm',
                                  'autoclose': 'true',
                                  'viewMode': 'years',
                                  'minView': 'months',
                                  'viewSelect': 'years',
                                  'todayHighlight': 'true',
                                  'todayBtn': 'true'})

class expo_info:
    def __init__(self,name='',addr='',url=''):
        self.name       = name
        self.addr       = addr
        self.url        = url
        self.show       = ''
        self.hall       = ''
        self.startdate  = None
        self.enddate    = None
        self.list_item  = None

    def show_info(self):
        print("name  : {}".format(self.name))
        print("show  : {}".format(self.show))
        print("addr  : {}".format(self.addr))
        print("url   : {}".format(self.url))
        print("hall  : {}".format(self.hall))
        print("start : {}".format(self.startdate.strftime('%Y/%m/%d')))
        print("end   : {}".format(self.enddate.strftime('%Y/%m/%d')))

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

for key,place in pattern.items():
    print(place['default'])
    document['place_list'] <= add_place(place['name'],key,place['default'])
    #jq(':checkbox').data("am-ucheck")
    #for cbx in document.select('input[type=checkbox]'):
    #    jq(cbx).data("am-ucheck")

def get_expo_list(abb):
    expo_list = []
    date_info = document['datepicker'].value.split('-')
    print(date_info)
    info_url = pattern[abb]['url_pattern'].format(year=int(date_info[0]),month=int(date_info[1]))
    print(info_url)
    page = request.urlopen(info_url)
    print('urlopen done')
    lines = page.read().split('\n')
    print(len(lines))
    lines = lines[pattern[abb]['refine_lineno']:-1]
    print(len(lines))
    refine_text = ''
    mdict = {}
    for line in lines:
        line = line.strip()
        for ptn in pattern[abb]['refine_pattern']:
            m = re.match(ptn,line)
            if m!=None:
                #print(m.group(0))
                mdict.update(m.groupdict())
                if len(mdict) == 4:
                    print(mdict)
                    expo = expo_info(pattern[abb]['name'],pattern[abb]['addr'],info_url)
                    expo.show       = mdict['showname']
                    expo.hall       = mdict['hall'].replace('&nbsp;','')
                    expo.startdate  = datetime.strptime(mdict['startdate'].replace('&nbsp;',''),pattern[abb]['date_pattern'])
                    expo.enddate    = datetime.strptime(mdict['enddate'],pattern[abb]['date_pattern'])
                    expo_list.append(expo)
                    mdict = {}
    print('pattern search done')
    if(len(expo_list)==0):
        alert("{}  {}/{}  无展会\n\n请确认下网址的正确性：\n\n{}".format(pattern[abb]['name'],date_info[0],date_info[1],info_url))
    return expo_list

def refresh():
    expo_list = []
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


