# -*- coding: utf-8 -*-
###########################################################################
# Script Python para cálculo de perdas de chaveamento na topologia        #
# sete níveis proposta. Disponível em:                                    #
# https://github.com/martinbra/mestrado_perdas7niveis/                    #
# https://repl.it/KgxZ/0                                                  #
#                                                                         #
# Versão utilizada: Python 2.7                                            #
###########################################################################

###########################################################################
# IMPORTAÇÃO DE BIBLIOTECAS                                               #
###########################################################################

# Habilita resultado real da divisão (e não apenas parte inteira)
from __future__ import division

# Importa funções matemáticas utilizadas
from math import sin, pi, asin, sqrt, floor, ceil, log10

# Importa interpolacao de valor em lista
import scipy.interpolate

###########################################################################
# VARIÁVEIS DEFINIDAS PELO USUÁRIO                                        #
# Usuário deve inserir valores das variaveis para calculo de perdas       #
# chaveamento para as chaves e diodos utilizados.                         #
###########################################################################

# Tensões das fontes de entrada
V1 = 100     # Volts
V2 = 200     # Volts

# Amplitude da senoide de referencia a ser sintetizada
Ar = V1 + V2 # Volts

# Valor eficaz da corrente de saída
Ief = 4.25    # Aef

# Defasamento Corrente, utilizado apenas para corrente linear 
I_def = 0 # rad (-pi/2 <= I_def <= pi/2)

# Frequência da senoide de referência a ser sintetizada
fr = 60      # Hz

# Frequência da portadora/chaveamento
fp = 21600   # Hz

###########################################################################
# DEFINIÇÃO DE FUNÇÕES DE PERDA EM FUNCAO DO COMPONENTE UTILIZADO         #
# Usuário deve inserir equações aproximadas das perdas de condução e de   #
# chaveamento para as chaves e diodos utilizados.                         #
###########################################################################
def perdaConducaoQ(i):
    """retorna perda em J da CHAVE em funcao da corrente"""
    # Para IRG4PC50UD
    if(i<0.2):
        Vceon = 0.707
    else:
        a= 34.494
        b=-45.751198
        c= 15.3045316
        Vceon = (-b+sqrt(b**2 -4*a*(c-i)))/(2*a)

    W = Vceon*i # W
    t = 1/fp # s
    return W*t # J = W*t
    
def perdaChaveamentoQ(i):
    """retorna perda em J da CHAVE em funcao da corrente"""
    # Para IRG4PC50UD
    perdas_a_5ohms = 1.58282
    perdas_a_Rgate = 2.65279
    correcao_perdas = perdas_a_Rgate/perdas_a_5ohms
    x=[0,13.5540,25.1140,39.409,54.0930] # A
    y=[0, 1.1391, 2.3747, 4.484, 6.5859] # mJ
    Eonoff = interpolar(i,x,y)
    return Eonoff/1000 * correcao_perdas # Joule

def perdaConducaoD(i):
    """retorna perda em j do DIODO em funcao da corrente"""
    # Para Diodo inserido em IRG4PC50UD
    if(i<1.3):
        Vceon = 0.8
    else:
        a= 33.050759762
        b=-48.682061178
        c= 19.131811979
        Vceon = (-b+sqrt(b**2 -4*a*(c-i)))/(2*a)

    W = Vceon*i # W
    t = 1/fp # s
    return W*t # J = W*t
    
def perdaChaveamentoD(i,vblock):
    """retorna perda em J do DIODO em funcao da corrente"""
    # Para Diodo inserido em IRG4PC50UD
    Qrr = 300e-9 # C
    return vblock * Qrr # Joule


def perdaConducaoDPonte(i):
    """retorna perda em J do DIODO em funcao da corrente"""
    # UF5408    
    if(i<0.01): Vceon = 0.6
    else:
        Vceon = 0.0430482*log10(i)**4 + 0.1598030*log10(i)**3 + \
                0.2299320*log10(i)**2 + 0.4327740*log10(i) + 1.12748

    W = Vceon*i # W
    t = 1/fp # s
    return W*t # J = W*t
    
def perdaChaveamentoDPonte(i,vblock):
    """retorna perda em J do DIODO em funcao da corrente"""
    # UF5408
    trr = 75e-9 # s
    irr = 0.25  # A
    return vblock * trr * irr / 2 #J

###########################################################################
# DEFINIÇÃO DE FUNÇÕES AUXILIARES                                         #
###########################################################################
def interpolar(x,list_x,list_y):
    """
    Recebe duas listas de mesmo tamanho, de pontos em um grafico.
    Retorna o valor de y interpolado para uma posição x fornecida.
    """
    interpolador_y = scipy.interpolate.interp1d(list_x, list_y)
    return interpolador_y(x)
    
def validacao(nome_variavel,logica_de_teste):
    """
    Valida coerencia de valores de variaveis de acordo com logica
    proposta
    """
    if logica_de_teste == False:
        print("Variavel "+nome_variavel+" fora de limite.")
    
def rms(v):
    """Calcula valor eficaz de uma lista de valores"""
    return (sum([x**2 for x in v])/len(v))**0.5

def media(v):
    """Calcula valor médio de uma lista de valores"""
    return (sum(v)/len(v))

def formaDeOndaCorrente(angulo,defasamento,fatorDeCrista):
    """
    Retorna o valor de uma corrente normalizada de 1 A eficaz
    para um ângulo da senoide tal que 0 <= angulo <2*pi
    com defasamento da corrente igual a "defasamento".
    fatorDeCrista ignorado.
    """
    # Corrente senoidal tem amplitude raiz(2) para valor eficaz ser de 1A.
    amplitude = sqrt(2)
    
    # Valor da corrente no angulo desejado
    corrente = amplitude * sin(angulo + defasamento)

    return corrente

def arredondaAngulo(angulo):
    """Arredonda ângulo de entrada para concluir chaveamento anterior"""
    # Quantidade de chaveamentos por ciclo da referência.
    k = 2*pi/mf
    # Arredonda ângulo para o próximo ângulo de início de chaveamento.
    return k * ceil( angulo/k )

def radParaGraus(rad):
    return 360*rad/(2*pi)

def grausParaRad(graus):
    return 2*pi*graus/360

###########################################################################
# TESTES DE VALIDAÇÃO DAS ENTRADAS                                        #
###########################################################################
# V1 deve ser menor que V2
validacao("V1 e V2", V1 < V2 )
# Não se pode modular tensao maior que as somas das tensoes do barramento
validacao("Ar", Ar <= (V1 + V2) )
# Não se possui sete niveis se amplitude for menor que V2:
validacao("Ar", Ar > V2 )
# Não se pode modular se portadora tiver frequência menor que referencia
validacao("fp", fp > fr )
# Não se pode modular se portadora tiver frequência menor que referencia
validacao("fp", fp > fr )

# Defasamento Corrente 
validacao("I_def", (-pi/2 <= I_def and I_def <= pi/2) )
# Fator de Crista Padrão
fat_crista = sqrt(2)
 
###########################################################################
# CALCULO DE PARAMETROS DE CHAVEAMENTO                                    #
###########################################################################
# Amplitude da portadora
Ap = V1
# Número de portadoras
np = 6
# Índice de Modulação de Amplitude
# ma = Ar / (V1 + V2) ou formalmente:
ma = 2*Ar/(np*Ap)

# Índice de Modulação de Frequência
mf = fp/fr

# Ângulos teóricos de mudança de estado
theta0  =   0
theta1  =   asin( V1/Ar )
theta2  =   asin( V2/Ar )
theta3  =   pi - theta2 
theta4  =   pi - theta1
theta5  =   pi + theta1
theta6  =   pi + theta2
theta7  = 2*pi - theta2 
theta8  = 2*pi - theta1

# Ângulos reais de mudança de estado
tt0 = arredondaAngulo(theta0)
tt1 = arredondaAngulo(theta1)
tt2 = arredondaAngulo(theta2)
tt3 = arredondaAngulo(theta3)
tt4 = arredondaAngulo(theta4)
tt5 = arredondaAngulo(theta5)
tt6 = arredondaAngulo(theta6)
tt7 = arredondaAngulo(theta7)
tt8 = arredondaAngulo(theta8)
pi1 = arredondaAngulo(pi)
pi2 = arredondaAngulo(2*pi)

#número de chaveamentos em cada intervalo
chA = mf * ((tt1 - tt0) + (pi1 - tt4)) / (2*pi) 
chB = mf * ((tt2 - tt1) + (tt4 - tt3)) / (2*pi) 
chC = mf * ((tt3 - tt2)              ) / (2*pi) 
chD = mf * ((tt5 - pi1) + (pi2 - tt8)) / (2*pi) 
chE = mf * ((tt6 - tt5) + (tt8 - tt7)) / (2*pi)
chF = mf * ((tt7 - tt6)              ) / (2*pi)

# Vetores para armazenar dados calculados em cada ciclo de chaveamento.
RAZAOCICLICA = []
CORRENTE     = []
TENSAOREF    = []
POTENCIAINST = []

#Variáveis para salvar as perdas em cada chave e diodo
perda_S1Q = [] # Perda da Chave S1
perda_S1D = [] # Perda do Diodo em paralelo com a chave S1
perda_S2Q = [] # Perda da Chave S2
perda_S2D = [] # Perda do Diodo em paralelo com a chave S2
perda_S3Q = [] # Perda da Chave S3
perda_S3D = [] # Perda do Diodo em paralelo com a chave S3
perda_S4Q = [] # Perda da Chave S4
perda_S4D = [] # Perda do Diodo em paralelo com a chave S4

perda_S5pQ  = [] # Perda da Chave S5 (Chave bidirecional em ponte de diodo)
perda_S5pDp = [] # Perda do Diodo da Ponte em S5 (conduz com i_positivo)
perda_S5pDn = [] # Perda do Diodo da Ponte em S5 (conduz com i_negativo)
 
perda_S6pQ  = [] # Perda da Chave S6 (Chave bidirecional em ponte de diodo)
perda_S6pDp = [] # Perda do Diodo da Ponte em S6 (conduz com i_positivo)
perda_S6pDn = [] # Perda do Diodo da Ponte em S6 (conduz com i_negativo)

perda_S5sQp = [] # Perda da Chave S5 (Chave bidirecional em série p/ i+)
perda_S5sQn = [] # Perda da Chave S5 (Chave bidirecional em série p/ i-)
perda_S5sDp = [] # Perda do Diodo em S5 (Chave bidir. em série p/ i+)
perda_S5sDn = [] # Perda do Diodo em S5 (Chave bidir. em série p/ i-)

perda_S6sQp = [] # Perda da Chave S6 (Chave bidirecional em série p/ i+)
perda_S6sQn = [] # Perda da Chave S6 (Chave bidirecional em série p/ i-)
perda_S6sDp = [] # Perda do Diodo em S6 (Chave bidir. em série p/ i+)
perda_S6sDn = [] # Perda do Diodo em S6 (Chave bidir. em série p/ i-)

i_S1Q = [] # Corrente na Chave S1
i_S1D = [] # Corrente no Diodo em paralelo com a chave S1
i_S2Q = [] # Corrente na Chave S2
i_S2D = [] # Corrente no Diodo em paralelo com a chave S2
i_S3Q = [] # Corrente na Chave S3
i_S3D = [] # Corrente no Diodo em paralelo com a chave S3
i_S4Q = [] # Corrente na Chave S4
i_S4D = [] # Corrente no Diodo em paralelo com a chave S4

i_S5pQ  = [] # Corrente na Chave S5 (Chave bidirecional em ponte de diodo)
i_S5pDp = [] # Corrente no Diodo da Ponte em S5 (conduz com i_positivo)
i_S5pDn = [] # Corrente no Diodo da Ponte em S5 (conduz com i_negativo)

i_S6pQ  = [] # Corrente na Chave S6 (Chave bidirecional em ponte de diodo)
i_S6pDp = [] # Corrente no Diodo da Ponte em S6 (conduz com i_positivo)
i_S6pDn = [] # Corrente no Diodo da Ponte em S6 (conduz com i_negativo)

i_S5sQp = [] # Corrente na Chave S5 (Chave bidirecional em série p/ i+)
i_S5sQn = [] # Corrente na Chave S5 (Chave bidirecional em série p/ i-)
i_S5sDp = [] # Corrente no Diodo em S5 (Chave bidir. em série p/ i+)
i_S5sDn = [] # Corrente no Diodo em S5 (Chave bidir. em série p/ i-)

i_S6sQp = [] # Corrente na Chave S6 (Chave bidirecional em série p/ i+)
i_S6sQn = [] # Corrente na Chave S6 (Chave bidirecional em série p/ i-)
i_S6sDp = [] # Corrente no Diodo em S6 (Chave bidir. em série p/ i+)
i_S6sDn = [] # Corrente no Diodo em S6 (Chave bidir. em série p/ i-)

# Temos "mf" ciclos de chaveamento durante um ciclo do sinal de referencia
# Para cada ciclo de chaveamento, será calculado o ângulo do chaveamento,
# a tensão de referencia, a corrente resultante e as perdas em cada chave
# e diodo.
for k in range(int(mf)): # loop de k variando de 0,1,2 ... "mf"
    # Calculo do Ângulo em que se inicia este ciclo de chaveamento
    angulo = 2*pi * (k/int(mf))
    #Adicão de meio ciclo para calcular valores médios do chaveamento
    angulo += 2*pi * 1/(2*mf)
    
    # Valor instantâneo da tensão de referência neste ângulo.
    vref = Ar*sin(angulo)
    
    # Valor instantâneo da corrente neste ângulo.
    i = Ief * formaDeOndaCorrente(angulo,I_def,fat_crista)

    # Determinação do intervalo de chaveamento referido
    if(angulo <= theta1):
        intervalo = "A"
    elif(angulo <= theta2):
        intervalo = "B"
    elif(angulo <= theta3):
        intervalo = "C"
    elif(angulo <= theta4):
        intervalo = "B"    
    elif(angulo <= pi):
        intervalo = "A"  
    elif(angulo <= theta5):
        intervalo = "D" 
    elif(angulo <= theta6):
        intervalo = "E"      
    elif(angulo <= theta7):
        intervalo = "F" 
    elif(angulo <= theta8):
        intervalo = "E"
    else: # angulo <= 2*pi:
        intervalo = "D"

    # Cálculo da razão cíclica em função do intervalo.
    if intervalo == "A":
        d = vref/V1
        vblock = V1
    elif intervalo == "B":
        d = (vref-V1)/(V2-V1)  
        vblock = V2    
    elif intervalo == "C":
        d = (vref-V2)/(V1) 
        vblock = V1+V2           
    elif intervalo == "D":
        d = 1-(-vref)/V1 
        vblock = V1         
    elif intervalo == "E":
        d = 1-(-vref-V1)/(V2-V1) 
        vblock = V2               
    elif intervalo == "F":
        d = 1-(-vref-V2)/(V1)
        vblock = V1+V2          

    
    # Calculo da Perda de condução e de chaveamento em função da corrente.
    # A perda será somada posteriormente às chaves em condução/comutação.
    iabs = abs(i)
    perda_Qs  = perdaChaveamentoQ(iabs) 
    perda_Qc  = perdaConducaoQ(iabs)
    perda_Ds  = perdaChaveamentoD(iabs,abs(vblock)) 
    perda_Dc  = perdaConducaoD(iabs)
    perda_DPs = perdaChaveamentoDPonte(iabs,abs(vblock))
    perda_DPc = perdaConducaoDPonte(iabs)

    # Determinação do Sentido da Corrente
    i_positivo = (i >= 0)    

    # As perdas calculadas são adicionadas às chaves de acordo com o estado
    # de cada chave no intervalo.
    # i) Perda de condução às chaves em função do tempo ativo (1, d ou 1-d)
    # ii) Perda de comutação às chaves que comutaram neste intervalo.
    # iii) Avaliação da adição das perdas à chave ou ao diodo em função do
    #      sentido da corrente.
    if intervalo == "A" and i_positivo:
        perda_S3Q.append(perda_Qc *( 1 ))
        perda_S4D.append(perda_Dc *(1-d) + perda_Ds)
        perda_S5pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S5pDp.append(perda_DPc*( d ) + perda_DPs)
        
        perda_S5sQp.append(perda_Qc*( d ) + perda_Qs)
        perda_S5sDp.append(perda_Dc*( d ) + perda_Ds)
        
    elif intervalo == "A" and not i_positivo:
        perda_S3D.append(perda_Dc *( 1 ))
        perda_S4Q.append(perda_Qc *(1-d) + perda_Qs)
        perda_S5pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S5pDn.append(perda_DPc*( d ) + perda_DPs)
        
        perda_S5sQn.append(perda_Qc*( d ) + perda_Qs)
        perda_S5sDn.append(perda_Dc*( d ) + perda_Ds)
        
    elif intervalo == "B" and i_positivo:
        perda_S1Q.append(perda_Qc *( d ) + perda_Qs)
        perda_S3Q.append(perda_Qc *(1-d) + perda_Qs)
        perda_S5pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S5pDp.append(perda_DPc*(1-d) + perda_DPs)
        perda_S6pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S6pDp.append(perda_DPc*( d ) + perda_DPs)
		
        perda_S5sQp.append(perda_Qc*(1-d) + perda_Qs)
        perda_S5sDp.append(perda_Dc*(1-d) + perda_Ds)
        perda_S6sQp.append(perda_Qc*( d ) + perda_Qs)
        perda_S6sDp.append(perda_Dc*( d ) + perda_Ds)
		
    elif intervalo == "B" and not i_positivo:
        perda_S1D.append(perda_Dc *( d ) + perda_Ds)
        perda_S3D.append(perda_Dc *(1-d) + perda_Ds)
        perda_S5pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S5pDn.append(perda_DPc*(1-d) + perda_DPs)
        perda_S6pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S6pDn.append(perda_DPc*( d ) + perda_DPs)
		
        perda_S5sQn.append(perda_Qc*(1-d) + perda_Qs)
        perda_S5sDn.append(perda_Dc*(1-d) + perda_Ds)
        perda_S6sQn.append(perda_Qc*( d ) + perda_Qs)
        perda_S6sDn.append(perda_Dc*( d ) + perda_Ds)
        
    elif intervalo == "C" and i_positivo:
        perda_S1Q.append(perda_Qc *( 1 ))
        perda_S3Q.append(perda_Qc *( d ) + perda_Qs)
        perda_S6pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S6pDp.append(perda_DPc*(1-d) + perda_DPs)
		
        perda_S6sQp.append(perda_Qc*(1-d) + perda_Qs)
        perda_S6sDp.append(perda_Dc*(1-d) + perda_Ds)
        
    elif intervalo == "C" and not i_positivo:
        perda_S1D.append(perda_Dc *( 1 ))
        perda_S3D.append(perda_Dc *( d ) + perda_Ds)
        perda_S6pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S6pDn.append(perda_DPc*(1-d) + perda_DPs)
		
        perda_S6sQn.append(perda_Qc*(1-d) + perda_Qs)
        perda_S6sDn.append(perda_Dc*(1-d) + perda_Ds)
        
    elif intervalo == "D" and i_positivo:
        perda_S3Q.append(perda_Qc *( d ) + perda_Qs)
        perda_S4D.append(perda_Dc *( 1 ))
        perda_S6pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S6pDp.append(perda_DPc*(1-d) + perda_DPs)
		
        perda_S6sQp.append(perda_Qc*(1-d) + perda_Qs)
        perda_S6sDp.append(perda_Dc*(1-d) + perda_Ds)
        
    elif intervalo == "D" and not i_positivo:
        perda_S3D.append(perda_Dc *( d ) + perda_Ds)
        perda_S4Q.append(perda_Qc *( 1 ))
        perda_S6pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S6pDn.append(perda_DPc*(1-d) + perda_DPs)
		
        perda_S6sQn.append(perda_Qc*(1-d) + perda_Qs)
        perda_S6sDn.append(perda_Dc*(1-d) + perda_Ds)
        
    elif intervalo == "E" and i_positivo:
        perda_S2D.append(perda_Dc *(1-d) + perda_Ds)
        perda_S4D.append(perda_Dc *( d ) + perda_Ds)
        perda_S5pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S5pDp.append(perda_DPc*(1-d) + perda_DPs)
        perda_S6pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S6pDp.append(perda_DPc*( d ) + perda_DPs)
		
        perda_S5sQp.append(perda_Qc*(1-d) + perda_Qs)
        perda_S5sDp.append(perda_Dc*(1-d) + perda_Ds)
        perda_S6sQp.append(perda_Qc*( d ) + perda_Qs)
        perda_S6sDp.append(perda_Dc*( d ) + perda_Ds)
        
    elif intervalo == "E" and not i_positivo:
        perda_S2Q.append(perda_Qc *(1-d) + perda_Qs)
        perda_S4Q.append(perda_Qc *( d ) + perda_Qs)
        perda_S5pQ.append(perda_Qc *(1-d) + perda_Qs)
        perda_S5pDn.append(perda_DPc*(1-d) + perda_DPs)
        perda_S6pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S6pDn.append(perda_DPc*( d ) + perda_DPs)
		
        perda_S5sQn.append(perda_Qc*(1-d) + perda_Qs)
        perda_S5sDn.append(perda_Dc*(1-d) + perda_Ds)
        perda_S6sQn.append(perda_Qc*( d ) + perda_Qs)
        perda_S6sDn.append(perda_Dc*( d ) + perda_Ds)
        
    elif intervalo == "F" and i_positivo:
        perda_S2D.append(perda_Dc *( 1 ))
        perda_S4D.append(perda_Dc *(1-d) + perda_Ds)
        perda_S5pQ.append(perda_Qc *( d ) + perda_Qs)
        perda_S5pDp.append(perda_DPc*( d ) + perda_DPs)
		
        perda_S5sQp.append(perda_Qc*( d ) + perda_Qs)
        perda_S5sDp.append(perda_Dc*( d ) + perda_Ds)

    elif intervalo == "F" and not i_positivo:
        perda_S2Q.append(perda_Qc*( 1 ))
        perda_S4Q.append(perda_Qc*(1-d) + perda_Qs)
        perda_S5pQ.append(perda_Qc*( d ) + perda_Qs)
        perda_S5pDn.append(perda_DPc*( d ) + perda_DPs)
		
        perda_S5sQn.append(perda_Qc*( d ) + perda_Qs)
        perda_S5sDn.append(perda_Dc*( d ) + perda_Ds)

    else:
        print "error", intervalo, i_positivo
		
    if intervalo == "A" and i_positivo:
        i_S3Q.append(iabs*( 1 ))
        i_S4D.append(iabs*(1-d))
        i_S5pQ.append(iabs*( d ))
        i_S5pDp.append(iabs*( d ))
        
        i_S5sQp.append(iabs*( d ))
        i_S5sDp.append(iabs*( d ))
        
    elif intervalo == "A" and not i_positivo:
        i_S3D.append(iabs*( 1 ))
        i_S4Q.append(iabs*(1-d))
        i_S5pQ.append(iabs*( d ))
        i_S5pDn.append(iabs*( d ))
        
        i_S5sQn.append(iabs*( d ))
        i_S5sDn.append(iabs*( d ))
        
    elif intervalo == "B" and i_positivo:
        i_S1Q.append(iabs*( d ))
        i_S3Q.append(iabs*(1-d))
        i_S5pQ.append(iabs*(1-d))
        i_S5pDp.append(iabs*(1-d))
        i_S6pQ.append(iabs*( d ))
        i_S6pDp.append(iabs*( d ))
		
        i_S5sQp.append(iabs*(1-d))
        i_S5sDp.append(iabs*(1-d))
        i_S6sQp.append(iabs*( d ))
        i_S6sDp.append(iabs*( d ))
		
    elif intervalo == "B" and not i_positivo:
        i_S1D.append(iabs*( d ))
        i_S3D.append(iabs*(1-d))
        i_S5pQ.append(iabs*(1-d))
        i_S5pDn.append(iabs*(1-d))
        i_S6pQ.append(iabs*( d ))
        i_S6pDn.append(iabs*( d ))
		
        i_S5sQn.append(iabs*(1-d))
        i_S5sDn.append(iabs*(1-d))
        i_S6sQn.append(iabs*( d ))
        i_S6sDn.append(iabs*( d ))
        
    elif intervalo == "C" and i_positivo:
        i_S1Q.append(iabs*( 1 ))
        i_S3Q.append(iabs*( d ))
        i_S6pQ.append(iabs*(1-d))
        i_S6pDp.append(iabs*(1-d))
		
        i_S6sQp.append(iabs*(1-d))
        i_S6sDp.append(iabs*(1-d))
        
    elif intervalo == "C" and not i_positivo:
        i_S1D.append(iabs*( 1 ))
        i_S3D.append(iabs*( d ))
        i_S6pQ.append(iabs*(1-d))
        i_S6pDn.append(iabs*(1-d))
		
        i_S6sQn.append(iabs*(1-d))
        i_S6sDn.append(iabs*(1-d))
        
    elif intervalo == "D" and i_positivo:
        i_S3Q.append(iabs*( d ))
        i_S4D.append(iabs*( 1 ))
        i_S6pQ.append(iabs*(1-d))
        i_S6pDp.append(iabs*(1-d))
		
        i_S6sQp.append(iabs*(1-d))
        i_S6sDp.append(iabs*(1-d))
        
    elif intervalo == "D" and not i_positivo:
        i_S3D.append(iabs*( d ))
        i_S4Q.append(iabs*( 1 ))
        i_S6pQ.append(iabs*(1-d))
        i_S6pDn.append(iabs*(1-d))
		
        i_S6sQn.append(iabs*(1-d))
        i_S6sDn.append(iabs*(1-d))
        
    elif intervalo == "E" and i_positivo:
        i_S2D.append(iabs*(1-d))
        i_S4D.append(iabs*( d ))
        i_S5pQ.append(iabs*(1-d))
        i_S5pDp.append(iabs*(1-d))
        i_S6pQ.append(iabs*( d ))
        i_S6pDp.append(iabs*( d ))
		
        i_S5sQp.append(iabs*(1-d))
        i_S5sDp.append(iabs*(1-d))
        i_S6sQp.append(iabs*( d ))
        i_S6sDp.append(iabs*( d ))
        
    elif intervalo == "E" and not i_positivo:
        i_S2Q.append(iabs*(1-d))
        i_S4Q.append(iabs*( d ))
        i_S5pQ.append(iabs*(1-d))
        i_S5pDn.append(iabs*(1-d))
        i_S6pQ.append(iabs*( d ))
        i_S6pDn.append(iabs*( d ))
		
        i_S5sQn.append(iabs*(1-d))
        i_S5sDn.append(iabs*(1-d))
        i_S6sQn.append(iabs*( d ))
        i_S6sDn.append(iabs*( d ))
        
    elif intervalo == "F" and i_positivo:
        i_S2D.append(iabs*( 1 ))
        i_S4D.append(iabs*(1-d))
        i_S5pQ.append(iabs*( d ))
        i_S5pDp.append(iabs*( d ))
		
        i_S5sQp.append(iabs*( d ))
        i_S5sDp.append(iabs*( d ))

    elif intervalo == "F" and not i_positivo:
        i_S2Q.append(iabs*( 1 ))
        i_S4Q.append(iabs*(1-d))
        i_S5pQ.append(iabs*( d ))
        i_S5pDn.append(iabs*( d ))
		
        i_S5sQn.append(iabs*( d ))
        i_S5sDn.append(iabs*( d ))

    else:
        print "error", intervalo, i_positivo

    #Insere ZERO nos vetores que não foram atualizados.
    if (k+1) > len(perda_S1Q):    perda_S1Q.append(0)
    if (k+1) > len(perda_S1D):    perda_S1D.append(0)
    if (k+1) > len(perda_S2Q):    perda_S2Q.append(0)
    if (k+1) > len(perda_S2D):    perda_S2D.append(0)
    if (k+1) > len(perda_S3Q):    perda_S3Q.append(0)
    if (k+1) > len(perda_S3D):    perda_S3D.append(0)
    if (k+1) > len(perda_S4Q):    perda_S4Q.append(0)
    if (k+1) > len(perda_S4D):    perda_S4D.append(0)
    if (k+1) > len(perda_S5pQ):   perda_S5pQ.append(0)
    if (k+1) > len(perda_S5pDp):  perda_S5pDp.append(0)
    if (k+1) > len(perda_S5pDn):  perda_S5pDn.append(0)
    if (k+1) > len(perda_S6pQ):   perda_S6pQ.append(0)
    if (k+1) > len(perda_S6pDp):  perda_S6pDp.append(0)
    if (k+1) > len(perda_S6pDn):  perda_S6pDn.append(0)
    if (k+1) > len(perda_S5sQp):  perda_S5sQp.append(0)
    if (k+1) > len(perda_S5sQn):  perda_S5sQn.append(0)
    if (k+1) > len(perda_S5sDp):  perda_S5sDp.append(0)
    if (k+1) > len(perda_S5sDn):  perda_S5sDn.append(0)
    if (k+1) > len(perda_S6sQp):  perda_S6sQp.append(0)
    if (k+1) > len(perda_S6sQn):  perda_S6sQn.append(0)
    if (k+1) > len(perda_S6sDp):  perda_S6sDp.append(0)
    if (k+1) > len(perda_S6sDn):  perda_S6sDn.append(0)
	
    if (k+1) > len(i_S1Q):    i_S1Q.append(0)
    if (k+1) > len(i_S1D):    i_S1D.append(0)
    if (k+1) > len(i_S2Q):    i_S2Q.append(0)
    if (k+1) > len(i_S2D):    i_S2D.append(0)
    if (k+1) > len(i_S3Q):    i_S3Q.append(0)
    if (k+1) > len(i_S3D):    i_S3D.append(0)
    if (k+1) > len(i_S4Q):    i_S4Q.append(0)
    if (k+1) > len(i_S4D):    i_S4D.append(0)
    if (k+1) > len(i_S5pQ):   i_S5pQ.append(0)
    if (k+1) > len(i_S5pDp):  i_S5pDp.append(0)
    if (k+1) > len(i_S5pDn):  i_S5pDn.append(0)
    if (k+1) > len(i_S6pQ):   i_S6pQ.append(0)
    if (k+1) > len(i_S6pDp):  i_S6pDp.append(0)
    if (k+1) > len(i_S6pDn):  i_S6pDn.append(0)
    if (k+1) > len(i_S5sQp):  i_S5sQp.append(0)
    if (k+1) > len(i_S5sQn):  i_S5sQn.append(0)
    if (k+1) > len(i_S5sDp):  i_S5sDp.append(0)
    if (k+1) > len(i_S5sDn):  i_S5sDn.append(0)
    if (k+1) > len(i_S6sQp):  i_S6sQp.append(0)
    if (k+1) > len(i_S6sQn):  i_S6sQn.append(0)
    if (k+1) > len(i_S6sDp):  i_S6sDp.append(0)
    if (k+1) > len(i_S6sDn):  i_S6sDn.append(0)
    
    # Salva os valores calculados neste chaveamento nos vetores
    # Para criação de gráfico.
    RAZAOCICLICA.append(d * 100) # Transforma em porcentagem
    CORRENTE.append(i)
    TENSAOREF.append(vref)
    POTENCIAINST.append(vref*i)

print("Resultados:")
print("Valores de entrada:")
print("V1           = "+str(V1)+" V")
print("V2           = "+str(V1)+" V")
print("Vref         = "+str(Ar)+" V") 
print("Vref eficaz  = "+str(Ar/sqrt(2))+" Vef")
print("Vref calc.   = "+str(rms(TENSAOREF))+" Vef")
print("Ief          = "+str(Ief)+" Aef")
print("Ief calculado= "+str(rms(CORRENTE))+" Aef")

print("I_def        = "+str(I_def)+" rad")
print("             = "+str(radParaGraus(I_def))+" graus")

print("Fator de Crista  = "+str(fat_crista))
print("Freq Vref        = "+str(fr)+" Hz")
print("Freq chaveamento = "+str(fp)+" Hz")
print("Índice de Modulação de Amplitude,  ma = "+str(ma))
print("Índice de Modulação de Frequência, mf = "+str(mf))

angulos = [tt0,tt1,tt2,tt3,tt4,pi,tt5,tt6,tt7,tt8]
str_angulos = ", ".join([str(radParaGraus(r)) for r in angulos])
print("Ângulos das mudanças de estado:\n    "+str_angulos)

chaveamentos = [chA, chB, chC, chD, chE, chF]
str_chaveamentos = ", ".join([str(int(c)) for c in chaveamentos])
print("Número de ciclos em cada intervalo (A a F):\n    "+str_chaveamentos)

sum_S1Q = sum(perda_S1Q)
sum_S1D = sum(perda_S1D)
sum_S2Q = sum(perda_S2Q)
sum_S2D = sum(perda_S2D)
sum_S3Q = sum(perda_S3Q)
sum_S3D = sum(perda_S3D)
sum_S4Q = sum(perda_S4Q)
sum_S4D = sum(perda_S4D)
sum_S5pQ = sum(perda_S5pQ)
sum_S5pDp = sum(perda_S5pDp)
sum_S5pDn = sum(perda_S5pDn)
sum_S6pQ = sum(perda_S6pQ)
sum_S6pDp = sum(perda_S6pDp)
sum_S6pDn = sum(perda_S6pDn)
sum_S5sQp = sum(perda_S5sQp)
sum_S5sQn = sum(perda_S5sQn)
sum_S5sDp = sum(perda_S5sDp)
sum_S5sDn = sum(perda_S5sDn)
sum_S6sQp = sum(perda_S6sQp)
sum_S6sQn = sum(perda_S6sQn)
sum_S6sDp = sum(perda_S6sDp)
sum_S6sDn = sum(perda_S6sDn)

print("Perdas nas chaves:")
print("    S1 Q  = "+'{0:.2f}'.format(sum_S1Q) + " W. Imed = " \
                                                    + str(media(i_S1Q  )))
print("       D  = "+'{0:.2f}'.format(sum_S1D) + " W. Imed = " \
                                                    +str(media(i_S1D  )))
print("    S2 Q  = "+'{0:.2f}'.format(sum_S2Q) + " W. Imed = " \
                                                    +str(media(i_S2Q  )))
print("       D  = "+'{0:.2f}'.format(sum_S2D) + " W. Imed = " \
                                                    +str(media(i_S2D  )))
print("    S3 Q  = "+'{0:.2f}'.format(sum_S3Q) + " W. Imed = " \
                                                    +str(media(i_S3Q  )))
print("       D  = "+'{0:.2f}'.format(sum_S3D) + " W. Imed = " \
                                                    +str(media(i_S3D  )))
print("    S4 Q  = "+'{0:.2f}'.format(sum_S4Q) + " W. Imed = " \
                                                    +str(media(i_S4Q  )))
print("       D  = "+'{0:.2f}'.format(sum_S4D) + " W. Imed = " \
                                                    +str(media(i_S4D  )))
print(" Chave bidirecional com ponte de diodos:")
print("    S5 Q  = "+'{0:.2f}'.format(sum_S5pQ) +" W. Imed = " \
                                                    +str(media(i_S5pQ) ))
print("       Dp = "+'{0:.2f}'.format(sum_S5pDp)+" W. Imed = " \
                                                    +str(media(i_S5pDp)))
print("       Dn = "+'{0:.2f}'.format(sum_S5pDn)+" W. Imed = " \
                                                    +str(media(i_S5pDn)))
print("    S6 Q  = "+'{0:.2f}'.format(sum_S6pQ) +" W. Imed = " \
                                                    +str(media(i_S6pQ )))
print("       Dp = "+'{0:.2f}'.format(sum_S6pDp)+" W. Imed = " \
                                                    +str(media(i_S6pDp)))
print("       Dn = "+'{0:.2f}'.format(sum_S6pDn)+" W. Imed = " \
                                                    +str(media(i_S6pDn)))
print(" Chave bidirecional em anti-série:")
print("    S5 Qp = "+'{0:.2f}'.format(sum_S5sQp)+" W. Imed = " \
                                                    +str(media(i_S5sQp)))
print("       Qn = "+'{0:.2f}'.format(sum_S5sQn)+" W. Imed = " \
                                                    +str(media(i_S5sQn)))
print("       Dp = "+'{0:.2f}'.format(sum_S5sDp)+" W. Imed = " \
                                                    +str(media(i_S5sDp)))
print("       Dn = "+'{0:.2f}'.format(sum_S5sDn)+" W. Imed = " \
                                                    +str(media(i_S5sDn)))
print("    S6 Qp = "+'{0:.2f}'.format(sum_S6sQp)+" W. Imed = " \
                                                    +str(media(i_S6sQp)))
print("       Qn = "+'{0:.2f}'.format(sum_S6sQn)+" W. Imed = " \
                                                    +str(media(i_S6sQn)))
print("       Dp = "+'{0:.2f}'.format(sum_S6sDp)+" W. Imed = " \
                                                    +str(media(i_S6sDp)))
print("       Dn = "+'{0:.2f}'.format(sum_S6sDn)+" W. Imed = " \
                                                    +str(media(i_S6sDn)))

print("\n")
potencia_saida = sum(POTENCIAINST)/len(POTENCIAINST)
perdasJ_bidir_ponte = sum_S1Q  +   sum_S1D   + sum_S2Q + sum_S2D +  \
                      sum_S3Q  +   sum_S3D   + sum_S4Q + sum_S4D +  \
                      sum_S5pQ + 2*sum_S5pDp + 2*sum_S5pDn       +  \
                      sum_S6pQ + 2*sum_S6pDp + 2*sum_S6pDn

perdasJ_bidir_2ch   = sum_S1Q   + sum_S1D   + sum_S2Q   + sum_S2D   +  \
                      sum_S3Q   + sum_S3D   + sum_S4Q   + sum_S4D   +  \
                      sum_S5sQp + sum_S5sDp + sum_S5sQn + sum_S5sDn +  \
                      sum_S6sQp + sum_S6sDp + sum_S6sQn + sum_S6sDn

#Perdas em J calculadas para 1 ciclo.
#Perdas em W calculadas para 1 segundo = perdasJ / t_ciclo = perdasJ*fr
perdasW_bidir_ponte = perdasJ_bidir_ponte * fr
perdasW_bidir_2ch   = perdasJ_bidir_2ch   * fr

print("perdas (ponte) = "+str(perdasW_bidir_ponte)+" W")
print("perdas (série) = "+str(perdasW_bidir_2ch)+" W")
                 
rend_ponte = (potencia_saida - perdasW_bidir_ponte) / potencia_saida * 100
rend_2ch   = (potencia_saida - perdasW_bidir_2ch  ) / potencia_saida * 100
print("Potencia Total das fontes = "+str(potencia_saida)+" W")
print("Potencia De saída (ponte) = " \
                             +str(potencia_saida-perdasW_bidir_ponte)+" W")
print("Potencia De saída (série) = " \
                             +str(potencia_saida-perdasW_bidir_2ch)+" W")

print("Topologia com chave bidirecional em ponte de diodo")
print("    Rendimento = "+'{0:.2f}'.format(rend_ponte)+" %")
print("Topologia com chave bidirecional em anti-série")
print("    Rendimento = "+'{0:.2f}'.format(rend_2ch)  +" %")
