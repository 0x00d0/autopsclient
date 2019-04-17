#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import logging

Params = {

    "server": "autops服务端地址",
    "port": autops服务端端口,
    "url": "/assets/report/",
    "request_timeout": 30,

}

# 日至文件配置
LOGPATH = os.path.join(os.path.dirname(os.getcwd()), 'logs', 'cmdg.log')
logging.basicConfig(filename=LOGPATH, format='%(asctime)s - %(levelname)s -%(filename)s[:%(lineno)d] -  %(message)s',
                    level=logging.INFO)


