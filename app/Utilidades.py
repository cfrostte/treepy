"""Clases con funcionalidades utilizadas por cualquier modulo"""

import datetime
import sys

class Logger(object):

    @staticmethod
    def init(clase):
        n = datetime.datetime.now()
        l = "Logs/{}_{}-{}-{}_{}-{}-{}.log"
        log = l.format(clase.__name__, n.year, n.month, n.day, n.hour, n.minute, n.second)
        sys.stdout = open(log, "w")

    @staticmethod
    def debug(texto):
        texto = '\n[LOG] {}:{}:{} > ' + str(texto).upper() + '\n'
        h = datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        s = datetime.datetime.now().second
        print(texto.format(h, m, s))
    