pattern = {
"SNIEC":{
    "name": "上海新国际博览中心",
    "url": "http://www.sniec.net",
    "addr": "中国上海浦东新区龙阳路2345号",
    "url_pattern": "http://www.sniec.net/cn/visit_exhibition.php?month={year}-{month:02d}",
    "refine_lineno": 350,
    "refine_pattern": ['<h1>(?P<showname>.*?)</h1>',
                       '<span>展厅 *(?P<hall>.*?) *\| *(?P<startdate>.*?) - (?P<enddate>.*?)</span>'],
    #"info_pattern": "<h1>(?P<showname>.*?)</h1>.*?<span>展厅 *(?P<hall>.*?) *\| *(?P<startdate>.*?) - (?P<enddate>.*?)</span>",
    "info_pattern": "<h1>(?P<showname>.*?)</h1><span>展厅 *(?P<hall>.*?) *\| *(?P<startdate>.*?) - (?P<enddate>.*?)</span>",
    "date_pattern": "%Y/%m/%d",
    "default": True
},
"SHEXPO":{
    "name": "上海世博展览馆",
    "url": "http://www.shexpocenter.com",
    "addr": "上海市浦东新区国展路1099号",
    "url_pattern": "http://www.shexpocenter.com/ExAgenda.aspx?Year={year}&month={month}",
    "refine_lineno": 250,
    "refine_pattern": ['■ <a id="gvEx_ct.*?>(?P<showname>.*?)</a>',
                       '时间：<span.*?>(?P<startdate>.*?)--(?P<enddate>.*?)</span>',
                       '馆号：<span.*?>(?P<hall>.*?)</span>'],
    #"info_pattern": '<a id=.*?>(?P<showname>.*?)</a>.*?时间.*?>(?P<startdate>.*?)--(?P<enddate>.*?)</span>.*?馆号.*?>(?P<hall>.*?)</span>',
    "info_pattern": '■ <a id=.*?>(?P<showname>.*?)</a>时间.*?>(?P<startdate>.*?)--(?P<enddate>.*?)</span>馆号.*?>(?P<hall>.*?)</span>',
    "date_pattern": "%Y.%m.%d",
    "default": False
}
}
