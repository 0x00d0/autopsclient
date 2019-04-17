#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time
import urllib.parse
import urllib.request
from conf import settings
from plugins import sys_info


def report_data():
    '''
    收集服务器信息并发送至服务器
    '''
    pass
    asset_data = sys_info.collect()
    data = {'asset_data': json.dumps(asset_data)}
    url = "http://{}:{}{}".format(settings.Params.get('server'), settings.Params.get('port'), settings.Params.get('url'))
    print('发送数据 {}'.format(url))
    try:
        data_encode = urllib.parse.urlencode(data).encode()
        response = urllib.request.urlopen(url=url, data=data_encode, timeout=settings.Params.get('request_time'))
        print('发送数据成功')

    except Exception as e:
        print(e)
