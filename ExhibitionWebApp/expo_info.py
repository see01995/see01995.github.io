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
        print("----------------")
        print("name  : {}".format(self.name))
        print("show  : {}".format(self.show))
        print("addr  : {}".format(self.addr))
        print("url   : {}".format(self.url))
        print("hall  : {}".format(self.hall))
        print("start : {}".format(self.startdate.strftime('%Y/%m/%d')))
        print("end   : {}".format(self.enddate.strftime('%Y/%m/%d')))

    def gen_json(self):
        data = dict()
        data.update({"name":self.name})
        data.update({"show":self.show})
        data.update({"addr":self.addr})
        data.update({"url":self.url})
        data.update({"hall":self.hall})
        data.update({"start":self.startdate.strftime('%Y/%m/%d')})
        data.update({"end":self.enddate.strftime('%Y/%m/%d')})
        return data
