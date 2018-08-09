#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import detection
import settings as config

# check if the image filename was provided as argument
if(len(sys.argv)>1):
    file = os.path.basename(sys.argv[1])
    folder = os.path.dirname(sys.argv[1])
else:
    print("***Error: an image filename is required as argument\n\t(e.g.: ./main.py image.png)")
    sys.exit()

# initialize configuration settings (needs to be done just once)
config.initConfig()

### set parameters for detection ###
config.setSourceFolderName(folder)
#config.setExclusionMargin(10)
config.setDebugMode(2)
#config.setResize(0.6)
config.setMinAreaSize(200)
# config.setRGBThreshold([(0,103), (0,90), (0,50)])	#imagen media
config.setRGBThreshold([(0,60), (0,99), (0,70)])	#imagen media
#initialize log
config.initLog('logfile')

config.use_autocontrast = False
# config.use_automatic_segm_threshold = True
config.compute_VARI = True
config.multiprocess_VARI = True
config.algorithm = 2

config.use_polynomial_regression = True

# run process
detection.run(sys.argv[1])

# close current log
config.closeLog()
