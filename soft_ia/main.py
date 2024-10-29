from IA import IA_Incêndios
import numpy as np
import os
from sql import inserirDados
import datetime
from serial_Arduino import obterMsgSerial
chama = 0
fumaca = 0
temperatura = 0
umidade = 0
fumacaBool = 0
import time

if __name__ == "__main__":
    os.system("cls")

    ia = IA_Incêndios("Braganca Paulista", range(2020, 2022+1))
    ia.impotarDados()
    ia.tratarDados()
    #ia.analisarDados()
    ia.converterEmClassificação([0, 300, 500, 1000, 4000, np.inf], 
                                ["Segurança OK", 
                                "Baixo Risco de Incêndio", 
                                "Médio Risco de Incéndio", 
                                "Alerta! Alto risco de incêndio", 
                                "ALERTA! Altíssimo risco de incêndio"])
    ia.treinarIa()

    while True:
        try:
            dados = obterMsgSerial("COM3")
        except PermissionError as e:
            print(e)
            continue
        resultado = ia.preverIncendio(float(dados["Temperatura"]), float(dados["Umidade"]))

        if chama == 1 and fumaca == 1: resultado = "Alerta: Chama e fumaça detectados!"
        elif chama == 1: resultado = "Alerta: Chama detectada!"
        elif float(dados["Fumaça"]) > 1100: resultado = "Alerta: Fumaça detectada!"

        if(fumaca > 1023):
            fumacaBool = 1
        else:
            fumacaBool = 0
        

        inserirDados(dados["Umidade"], dados["Temperatura"], chama, fumacaBool, str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")), resultado)
        time.sleep(10)