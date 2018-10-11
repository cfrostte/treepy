#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import Analisis.utils.source.detection
import Analisis.utils.source.settings as config

# check if the image filename was provided as argument
if(len(sys.argv)>1):
    path = sys.argv[1]
    # file = os.path.basename(path)
    folder = os.path.dirname(path)
else:
    print("***Error: an image/folder name is required as argument\n\t(e.g.: ./main.py image.png)")
    sys.exit()

config.initConfig()  # initialize configuration settings (needs to be done just once)

### set parameters for detection ###
config.setSourceFolderName(folder)
#config.setExclusionMargin(10)
config.setDebugMode(2)
#config.setResize(0.6)
config.setMinAreaSize(150)
config.setDistanceThreshold(200)
# config.setRGBThreshold([(0,103), (0,90), (0,50)])	 # imagen media
config.setRGBThreshold([(0,60), (0,99), (0,70)])  # imagen media
config.initLog('logfile')  # initialize logfile

config.use_auto_distance_thresh = True
config.use_autocontrast = False
# config.use_automatic_segm_threshold = True
config.compute_VARI = True
config.multiprocess_VARI = True
config.algorithm = 2
config.use_polynomial_regression = True

detection.run(path)  # run process

config.closeLog()  # close current logfile
