import argparse
import cv2

import CLI.ecualizador as e
import CLI.binarizador as b
import CLI.deductor as d
import CLI.generador as g

AP = argparse.ArgumentParser()
AP.add_argument("-i", "--img", required=False, help="Imagen a procesar")

ARGUMENTOS = vars(AP.parse_args())

if ARGUMENTOS["img"]:
    IMAGEN = cv2.imread(ARGUMENTOS["img"])
    print()
    print(" > PASO 1")
    e.ecualizar()
    print()
    print(" > PASO 2")
    b.binarizar()
    print()
    print(" > PASO 3")
    d.deducir()
    print()
    print(" > PASO 4")
    g.generar()
    cv2.imshow("Imagen procesada", IMAGEN)
    cv2.waitKey(0)
