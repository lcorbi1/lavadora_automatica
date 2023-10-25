#Programa tanquinho como máquina de lavar roupa

from machine import ADC, Pin, Timer, I2C, lightsleep
#from pico_i2c_lcd import I2cLcd
import time, math

#---------------------------PINs-------------------------------
pin_liga_lavadora = Pin(15, Pin.OUT)
pin_sensor_nivel_agua_enchendo = Pin(2, Pin.IN, Pin.PULL_DOWN)  #Sensor de fluxo
pin_recebe_sinal_tanqueCheio = Pin(3, Pin.IN, Pin.PULL_DOWN)
pin_envia_sinal_tanqueCheio = Pin(4, Pin.OUT)
pin_sensor_nivel_agua_drenando = Pin(11, Pin.IN, Pin.PULL_DOWN)  #Sensor de fluxo
pin_liga_modRele_valvulaSol_encher = Pin(13, Pin.OUT)
pin_liga_modRele_valvulaSol_esvaziar = Pin(12, Pin.OUT)

#---------------------------LCDs-------------------------------
#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
#I2C_ADDR = i2c.scan()[0]
#lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

#lcd.putstr("Lavadora Auto")
#lcd.move_to(0, 1)   #(coluna, linha)
#lcd.putstr("--------------")
#sleep(5)
#lcd.clear()

#-----------------------SENSOR DE FLUXO AGUA----------------------

calculoVazao = 0
contador = 0
metroCubico = 0
ContaAgua = 0
fluxo_de_agua = 0

#--------------------------PROGRAMAÇÔES---------------------------
muito_sujo = 28 #funciona por 7 minutos
jeans = 21   #molho por 7 minutos
dia_a_dia = 14  #funciona por por 7 minutos
enxaguar = 12  #funciona por 5 minutos
delicado = 9  #funciona por 2 minutos
molho = 7 # molho por 7 minutos
desligado = 0 #desliga

opcao = {"muito_sujo": muito_sujo, "jeans": jeans, "dia_a_dia": dia_a_dia, "enxaguar": enxaguar, "delicado": delicado, "molho": molho, "desligado": desligado}

#--------------------------VARIAVEIS--------------------------------
# Cada vez que uma opção for selecionada, verificar primeiro se está em funcionamento
em_funcionamento = False
tempo_funcionamento = Timer()
rc = 2
lavadora = 0
lavadora_acionada = False
#--------------------------Volume do Tanquinho----------------------
#raio = 0.30  # 30cm de raio
#altura = 0.55   # 55cm de altura


raio = 0.05  # 30cm de raio
altura = 0.05   # 55cm de altura
#--------------------------FUNCOES-----------------------------------
def volume_tanquinho(r=raio, a=altura):
    """ Retorna o volume total, considerando que 1m³ = 1000 litros """
    PI = math.pi
    area = PI * math.pow(r,2)
    volume = (area * a) * 1000
    # Retorna o volume em LITROS
    return volume


def Vazao(x):
    lavadora_acionada = False
    global contador
    contador = contador + 1
    global fluxoAcumulado
    fluxoAcumulado = (contador * 2.25)/1000
    
    global litragem_max_tanquinho
    litragem_max_tanquinho = volume_tanquinho()
    
    print(f'Litros por minuto: {fluxoAcumulado}L ou {contador * 2.25}mL')
    pin_liga_modRele_valvulaSol_encher.value(1)  #Liga valvula solenoide
    
    if fluxoAcumulado >= litragem_max_tanquinho:
        print(f'DESLIGA VALVULA SOLENOIDE DE ENCHER -- > Lavadora: {lavadora}  --> Lavadora Acionada: {lavadora_acionada}')
        pin_liga_modRele_valvulaSol_encher.value(0)   #Desliga valvula solenoide
        pin_liga_lavadora.value(1)   #Liga a maquina de lavar
        # Enviar sinal para desligar a maquina de lavar depois de 7 minutos
        lavadora_acionada = True
        pin_envia_sinal_tanqueCheio.value(1)
        pin_envia_sinal_tanqueCheio.value(0)
        

def setaLavadoraLigada(arg):
    lavadora = 1  #Seta lavadora ligada
    return lavadora

def temporizador_lavadora_ligada(pin):
    
    # Essa funcao temporizador_lavadora_ligada nao pode chamar direto a funcao setaLavadoraLigada, só deve chamar e atribuir lavadora = 1 caso a interrupcao pin_recebe_sinal_tanqueCheio seja chamada
    
    if lavadora_acionada == True:
        x = setaLavadoraLigada(pin)    ##  <<-----  Aqui ta chamando a funcao acima SEMPRE, independente da IRQ
        print(f'Lavadora: {x}')
        if x == 1:
            time.sleep(30)
            pin_liga_lavadora.value(0)  #Desliga lavadora
            #lavadora = 0 #Seta lavadora desligada
            x = 0
            lavadora = x
            print(f'Lavadora desligada: {lavadora}  --> Lavadora Acionada: {lavadora_acionada}')
    else:
        x = 0    ##  <<-----  Aqui ta chamando a funcao acima SEMPRE, independente da IRQ
        print(f'Lavadora: {x}')


tempo_funcionamento.init(period = 10000, mode = Timer.PERIODIC, callback = temporizador_lavadora_ligada)
    
    
def Checar_nivel_de_agua():
    ## Passos
    # 1 - Fazer leitura da bóia/fluxo de agua que entrou --> Variavel --> fluxo_de_agua
    # 2 - Checar se em algum momento a valvula de drenar agua funcionou: SE sim = checar se esvaziou o fluxo_de_agua acima, a mesma quantidade.
    # 3 - Todas as funcoes de programacao devem checar o nivel de agua antes.
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

#----------------------FUNÇÕES DE PROGRAMAÇÃO--------------------
def Enxaguar():
    print("Enxaguando....")


def Delicado():
    print("Delicado....")


def Molho():
    print("Molho.....")
    

def Desligar():
    """Desliga TUDO..."""
    pin_liga_lavadora.value(0)
    pin_liga_modRele_valvulaSol_encher.value(0)
    pin_liga_modRele_valvulaSol_esvaziar.value(0)
    
def Muito_Sujo():
    print("Muito Sujo....")
    """
1) Liga valvula Encher
2) Esperar encher o volume maximo "litragem_max_tanquinho"
3) Desligar valvula de encher
4) Ligar motor do tanquinho
5) Esperar 7 minutos de funcionamento
6) Desligar motor do tanquinho
7) Esperar 7 minutos de molho
8) Ligar motor do tanquinho
9) Esperar 7 minutos de funcionamento
10) Desligar motor do tanquinho
11) Ligar valvula de drenagem até não passar mais agua e desligar.

    """
    
    #Liga valvula Encher
    
    
    

def Jeans():
    print("Jeans.....")
    
def Dia_a_Dia():
    print("Dia a Dia.....")
    
    
#----------------------FUNÇÃO SUB-MAIN--------------------

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
        
        
#-----------------------INTERRUPÇÕES-------------------------

pin_sensor_nivel_agua_enchendo.irq(trigger=machine.Pin.IRQ_RISING, handler=Vazao)
pin_recebe_sinal_tanqueCheio.irq(trigger=machine.Pin.IRQ_RISING, handler=setaLavadoraLigada)

#--------------------FUNÇÃO *****MAIN*******----------------
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


#----------------------CHAMADA DA FUNÇÃO MAIN--------------------
#escolher_opcao()