"""Clases con funcionalidades utilizadas por cualquier modulo"""

import datetime
import sys

class Logger(object):

    @staticmethod
    def init(clase):
        now = datetime.datetime.now()
        log = "Logs/{}_{}-{}-{}_{}-{}-{}.log"
        log = log.format(clase.__name__, now.year, now.month, now.day, now.hour, now.minute, now.second)
        sys.stdout = open(log, "w")

    @staticmethod
    def debug(texto):
        texto = '\n[LOG] {}:{}:{} > ' + str(texto).upper() + '\n'
        h = datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        s = datetime.datetime.now().second
        print(texto.format(h, m, s))
    