#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys


BASE_DIR = os.path.dirname(os.getcwd())

sys.path.append(BASE_DIR)

from core import handler


if __name__ == '__main__':

    handler.report_data()



