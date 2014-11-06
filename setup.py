#!/usr/bin/env python
from Tkinter import *
import main
import os
import settings
import getuserinput

if (os.path.exists(settings.main_dir) and os.path.exists(settings.main_dir_hidden) and os.path.isfile(settings.secrets_file)):
    print 'Your credentials exist'
    main.main_func()
else:
    getuserinput.enter()
