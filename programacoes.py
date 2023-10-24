from machine import Pin, Timer
import time


pin_liga_lavadora = Pin(15, Pin.OUT)
pin_sensor_nivel_agua_enchendo = Pin(14, Pin.IN, Pin.PULL_DOWN)  #Sensor de fluxo
pin_sensor_nivel_agua_drenando = Pin(11, Pin.IN, Pin.PULL_DOWN)  #Sensor de fluxo
pin_liga_valvulaSol_enxer = Pin(13, Pin.OUT)
pin_liga_valvulaSol_esvaziar = Pin(12, Pin.OUT)

# Cada vez que uma opção for selecionada, verificar primeiro se está em funcionamento
em_funcionamento = False

tempo_funcionamento = Timer()
rc = 2

#------------------------------------------------------------------------------------------- 

def checa_ligado():
    if em_funcionamento:
        # Escrever no Display: Em funcionamento!
        rc = 1
        return rc
    else:
        # Liberado para funcionar
        rc = 0
        return rc

def colocar_de_molho():
    time.sleep(420)
    

def resetar():
    machine


def Enxaguar():
    rc = checa_ligado()
    print("Enxaguando....")
    em_funcionamento = True
    return em_funcionamento
    