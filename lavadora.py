#Programa tanquinho como máquina de lavar roupa

from machine import ADC, Pin, Timer, I2C
from pico_i2c_lcd import I2cLcd
import time, math

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

#lcd.putstr("Lavadora Auto")
#lcd.move_to(0, 1)   #(coluna, linha)
#lcd.putstr("--------------")
#sleep(5)
#lcd.clear()

muito_sujo = 28 #funciona por 7 minutos
jeans = 21   #molho por 7 minutos
dia_a_dia = 14  #funciona por por 7 minutos
enxaguar = 12  #funciona por 5 minutos
delicado = 9  #funciona por 2 minutos
molho = 7 # molho por 7 minutos
desligado = 0 #desliga

opcao = {"muito_sujo": muito_sujo, "jeans": jeans, "dia_a_dia": dia_a_dia, "enxaguar": enxaguar, "delicado": delicado, "molho": molho, "desligado": desligado}


pin_liga_lavadora = Pin(15, Pin.OUT)
pin_sensor_nivel_agua_enchendo = Pin(14, Pin.IN, Pin.PULL_DOWN)  #Sensor de fluxo
pin_sensor_nivel_agua_drenando = Pin(11, Pin.IN, Pin.PULL_DOWN)  #Sensor de fluxo
pin_liga_valvulaSol_enxer = Pin(13, Pin.OUT)
pin_liga_valvulaSol_esvaziar = Pin(12, Pin.OUT)

# Cada vez que uma opção for selecionada, verificar primeiro se está em funcionamento
em_funcionamento = False

tempo_funcionamento = Timer()
rc = 2

fluxo_de_agua = 0

######## Volume do Tanquinho
raio = 0.30  # 30cm de raio
altura = 0.55   # 55cm de altura


"""
Se escolher:

muito_sujo --> Motor deve funcionar por 7 minutos, desligar, aguardar 7 minutos, ligar
jeans  --> Motor deve ficar desligado por 7 minutos

"""

def volume_tanquinho(r=raio, a=altura):
    """ Retorna o volume total, considerando que 1m³ = 1000 litros """
    PI = math.pi
    area = PI * math.pow(r,2)
    volume = (area * a) * 1000
    # Retorna o volume em LITROS
    return volume

def detectar_fluxo_de_agua_passado_no_sensor():
    ##### Transformar o sinal analogico do sensor em digital
    ## ex: 0 = vazio, 100 = cheio
    ## Medir o volume interno do tanquinho
    litragem_total = volume_tanquinho()
    return fluxo_de_agua


def Checar_nivel_de_agua():
    ## Passos
    # 1 - Fazer leitura da bóia/fluxo de agua que entrou --> Variavel --> fluxo_de_agua
    # 2 - Checar se em algum momento a valvula de drenar agua funcionou: SE sim = checar se esvaziou o fluxo_de_agua acima, a mesma quantidade.
    # 3 - Todas as funcoes de programacao devem checar o nivel de agua antes.
    pass


def Encher_tanque():
    pass


def checa_ligado():
    print(em_funcionamento)
    if em_funcionamento:
        # Escrever no Display: Em funcionamento!
        rc = 1
        return rc

def colocar_de_molho():
    time.sleep(420)
    

def resetar():
    global rc
    print("REINICIANDOO....")
    em_funcionamento
    rc = 0
    

def programacao_decorada(funcao):
    global rc
    rc = checa_ligado()
    funcao
    em_funcionamento = True
    rc = 1


def Enxaguar():
    print("Enxaguando....")


def Delicado():
    print("Delicado....")


def Molho():
    print("Molho.....")
    

def Desligar():
    print("Desligado...")
    
def Muito_Sujo():
    print("Muito Sujo....")

def Jeans():
    print("Jeans.....")
    
def Dia_a_Dia():
    print("Dia a Dia.....")

def listar_opcao(opcao):
    #print(I2C_ADDR)
    #lcd.blink_cursor_on()
    #lcd.clear()
    #lcd.putstr("Opção:")
    for num, op in enumerate(opcao):
        #lcd.putstr(f'{num + 1}-{op}')
        #lcd.move_to(0,num + 1)
        #sleep(1)
        print(f'{num + 1} -> {op}({opcao[op]} minutos)')
    #sleep(5)
    #lcd.blink_cursor_off()


def escolher_opcao():  
    op = 0
    while op != 8:
        #rc = checa_ligado()
        print(f'RC: {rc}')
        if rc == 1:
            print("EM Funcionamento...")
        print("")
        listar_opcao(opcao)
        print("8 -> SAIR")
        print("9 -> REINICIAR")
        print("")
        op = int(input("Opção: "))
        if op == 1:
            programacao_decorada(Enxaguar)
        elif op == 2:
            programacao_decorada(Delicado)
        elif op == 3:
            programacao_decorada(Molho)
        elif op == 4:
            programacao_decorada(Desligar)
        elif op == 5:
            programacao_decorada(Muito_Sujo)
        elif op == 6:
            programacao_decorada(Jeans)
        elif op == 7:
            programacao_decorada(Dia_a_Dia)
        elif op == 8:
            print("Saindo.....")
        elif op == 9:
            resetar()
        else:
            print("Opção inválida!")
    


#timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)


#while True:
    
escolher_opcao()
