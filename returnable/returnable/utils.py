# -*- coding: utf-8 -*-
# Copyright (c) 2020, Warehouseman and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import os
import errno

def LG(txt, end = "\n"):
  filename = '/dev/shm/erpnext/result.log'

  if os.path.exists(filename):
    append_write = 'a' # append if already exists
  else:
    try:
      os.makedirs('/dev/shm/erpnext')
    except OSError as e:
      if e.errno != errno.EEXIST:
            raise
    append_write = 'w' # make a new file if not

  logfile = open(filename,append_write)
  logfile.write(txt + end)
  logfile.close()

