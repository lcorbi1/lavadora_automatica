from machine import Pin

calculoVazao = 0
contador = 0
#fluxoAcumulado = 0
metroCubico = 0
ContaAgua = 0


#def Vazao(cont):
def Vazao(x):
    global contador
    contador = contador + 1
    fluxoAcumulado = (contador * 2.25)/1000
    print(f'Litros por minuto: {fluxoAcumulado}L ou {contador * 2.25}mL')


p2 = Pin(2, Pin.IN, Pin.PULL_UP)
p2.irq(trigger=machine.Pin.IRQ_RISING, handler=Vazao)

"""
while True:
    #contador = 0      
    
    calculoVazao = (contador * 2.25)    #2.25ml cada vez que tem um giro completo, contabiliza 2.25ml/por giro    Ex: 1000 giros --> 2.250ml
    fluxoAcumulado = fluxoAcumulado + (calculoVazao/1000) #Converte para Litros                                -->    2.250/1000 --> 2,25L         
    metroCubico = fluxoAcumulado/1000  # Converte o litro acima para volume em metros cúbicos                  -->    2,25 /1000 --> 0,00225m³
    ContaAgua = metroCubico * 3.59   #R$3.59/m3 de agua
    calculoVazao = calculoVazao * 60   #converte pra minuto --> ml/min                                         -->    2.250ml * 60 --> 135.000ml/min
    calculoVazao = calculoVazao / 1000   #vazao instantanea L/min                                              -->    135.000/1000 --> 135L/min
    #print(f'Litros por minuto: {calculoVazao}L/min ')   #2.25ml cada vez que tem um giro completo, contabiliza 2.25ml/por giro
    
"""