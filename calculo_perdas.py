###########################################################################
# Script Python para cálculo de perdas de chaveamento na topologia        #
# sete níveis proposta.                                                   #
#                                                                         #
# Versão utilizada: Python 2.7                                            #
###########################################################################

###########################################################################
# IMPORTAÇÃO DE BIBLIOTECAS                                               #
###########################################################################

# Habilita resultado real da divisão (e não apenas parte inteira)
from __future__ import division

# Importa funções matemáticas utilizadas
from math import sin, pi, asin, sqrt, floor, ceil

# Importa biblioteca para geração de gráficos
from pylab import plot, show, xlabel, ylabel, legend, xlim, ylim

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
Ief = 50     # Aef

# Corrente Linear
I_linear = False # "True" ou "False"

# Defasamento Corrente, utilizado apenas para corrente linear 
I_def = 30/180*pi # rad (-pi/2 <= I_def <= pi/2)

# Fator de Crista, utilizado apenas para corrente não linear.
# Simula Carga não linear como pulsos semi-senoidais (positivo e negativo)
fat_crista = 3.0 # fat_crista >= srqt(2)

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
    """retorna perda em W da CHAVE em funcao da corrente"""
    #TODO CORRIGIR VALORES E EQUACAO
    Vceon = 1.5 + 0.05*i
    return Vceon * i
    
def perdaChaveamentoQ(i):
    """retorna perda em J da CHAVE em funcao da corrente"""
    Eon = 0.001 * i
    Eoff = 0.002 * i
    return Eon+Eoff

def perdaConducaoD(i):
    """retorna perda em W do DIODO em funcao da corrente"""
    #TODO CORRIGIR VALORES E EQUACAO
    Vceon = 1.5 + 0.05*i
    return Vceon * i
    
def perdaChaveamentoD(i):
    """retorna perda em J do DIODO em funcao da corrente"""
    Eon = 0.001 * i
    Eoff = 0.002 * i
    return Eon+Eoff

###########################################################################
# DEFINIÇÃO DE FUNÇÕES AUXILIARES                                         #
###########################################################################
def perdaQ(i,d,):
    pass
    
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

def formaDeOndaCorrenteLinear(angulo,defasamento,fatorDeCrista):
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

def formaDeOndaCorrenteNaoLinear(angulo,defasamento,fatorDeCrista):
    """
    Retorna o valor de uma corrente normalizada de 1 A eficaz
    para um ângulo da senoide tal que 0 <= angulo <2*pi
    com fator de crista "fatorDeCrista" determinado pelo usuário.
    Simula corrente não linear como um pulso senoidal centrado
    nos picos da senoide da tensão, similar a uma carga retificada.
    defasamento ignorado.
    """
    # Amplitude == pico (Pico = FC*Ieficaz)
    amplitude = fatorDeCrista 

    # largura em radianos do pulso senoidal
    alpha = 2*pi / fatorDeCrista**2

    # Ângulos de conducao do pulso senoidal  
    inicioPos =   pi/2 - alpha/2     #no semiciclo positivo
    finalPos  =   pi/2 + alpha/2     #no semiciclo positivo
    inicioNeg = 3*pi/2 - alpha/2     #no semiciclo negativo
    finalNeg  = 3*pi/2 + alpha/2     #no semiciclo negativo
    largura   = (finalPos-inicioPos) #Largura em rad do pulso.

    # Se o ângulo em questão não está dentro do período do pulso
    # Retorna "0", pois não conduz, corrente é nula.
    if ((angulo < inicioPos) or                       
        (angulo > finalPos and angulo < inicioNeg) or 
        (angulo > finalNeg)):
        return 0

    # Se ângulo está dentro dos limites
    else:
        #Verifica semi-ciclo
        if angulo < pi:
            #semiciclo positivo
            corrente = sin((pi*angulo - pi*inicioPos)/largura)
            
        else:
            # semiciclo negativo
            # corrente_neg(ang) = -corrente_pos(ang-pi)
            corrente = -sin((pi*(angulo-pi) - pi*inicioPos)/largura)

        #Retorna valor da corrente
        return corrente*amplitude

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
# DEFINIÇÃO DE FUNÇÕES TEMPORARIAS (apenas para desenvolvimento do codigo)#
###########################################################################
def plotlevels():
    """
    Desenha linhas verticais nos angulos theta1 e theta2;
    Desenha linhas horizontais nos níveis de tensão V1 e V2.
    """
    plot([0,mf],[V1,V1])
    plot([0,mf],[V2,V2])
    ang1 = theta1*mf/(2*pi)
    ang2 = theta2*mf/(2*pi)
    plot([ang1,ang1],[0,V1+V2])
    plot([ang2,ang2],[0,V1+V2])


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

# Se Corrente for Linear:
if(I_linear ==True):
    # Defasamento Corrente, utilizado apenas para corrente linear 
    validacao("I_def", (-pi/2 <= I_def <= pi/2) )
    # Utiliza a função formaDeOndaCorrenteLinear para a corrente.
    formaDeOndaCorrente = formaDeOndaCorrenteLinear
    # Fator de Crista Padrão
    fat_crista = sqrt(2)
    
# Se corrente for Não Linear    
else:
    # Fator de Crista é no mínimo raiz(2) para carga não linear.
    validacao("fat_crista", fat_crista >= sqrt(2) )
    # Utiliza a função formaDeOndaCorrenteLinear para a corrente.
    formaDeOndaCorrente = formaDeOndaCorrenteNaoLinear
    # Defasamento padrao
    I_def = 0
 
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
tt0  = arredondaAngulo(theta0)
tt1  = arredondaAngulo(theta1)
tt2  = arredondaAngulo(theta2)
tt3  = arredondaAngulo(theta3)
tt4  = arredondaAngulo(theta4)
tt5  = arredondaAngulo(theta5)
tt6  = arredondaAngulo(theta6)
tt7  = arredondaAngulo(theta7)
tt8  = arredondaAngulo(theta8)
pi1  = arredondaAngulo(pi)
pi2 = arredondaAngulo(2*pi)

#número de chaveamentos em cada intervalo
chA = mf * ((tt1 - tt0) + (pi1 - tt4)) / (2*pi) 
chB = mf * ((tt2 - tt1) + (tt4 - tt3)) / (2*pi) 
chC = mf * ((tt3 - tt2)              ) / (2*pi) 
chD = mf * ((tt5 - pi1) + (pi2 - tt8)) / (2*pi) 
chE = mf * ((tt6 - tt5) + (tt8 - tt7)) / (2*pi)
chF = mf * ((tt7 - tt6)              ) / (2*pi)

#perdas por chave em cada etapa
#	Q1	Q4	Q5	Q2	Q3	Q6
#A	0	D’	D	0	1	0
#B	D	0	D’	0	D’	D
#C	1	0	0	0	D’	D’
#An	0	1	0	0	D’	D
#Bn	0	D’	D	D	0	D’
#Cn	0	D	D’	1	0	0

# Vetores para armazenar dados calculados em cada ciclo de chaveamento.
RAZAOCICLICA = []
CORRENTE     = []
TENSAOREF    = []
POTENCIAINST = []

#Variáveis para salvar as perdas em cada chave e diodo
perda_S1Q = 0
perda_S1D = 0
perda_S2Q = 0
perda_S2D = 0
perda_S3Q = 0
perda_S3D = 0
perda_S4Q = 0
perda_S4D = 0
perda_S5Q = 0
perda_S5D = 0
perda_S6Q = 0
perda_S6D = 0

# Temos "mf" ciclos de chaveamento durante um ciclo do sinal de referencia
# Para cada ciclo de chaveamento, será calculado o ângulo do chaveamento,
# a tensão de referencia, a corrente resultante e as perdas em cada chave
# e diodo.
for i in range(int(mf)): # loop de i variando de 0,1,2 ... "mf"
    # Calculo do Ângulo em que se inicia este ciclo de chaveamento
    angulo = 2*pi * (i/int(mf))
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
    elif intervalo == "B":
        d = (vref-V1)/(V2-V1)      
    elif intervalo == "C":
        d = (vref-V2)/(V1)        
    elif intervalo == "D":
        d = 1-(-vref)/V1 
    elif intervalo == "E":
        d = 1-(-vref-V1)/(V2-V1)       
    elif intervalo == "F":
        d = 1-(-vref-V2)/(V1)

    # Cálculo das perdas para as chaves
    if(angulo < pi):
        perda_Qs = perdaChaveamentoQ(i)
        perda_Qc = perdaConducaoQ(i)
        perda_Ds = perdaChaveamentoD(i)
        perda_Dc = perdaConducaoD(i)
    else:        
        perda_Qs = perdaChaveamentoQ(-i)
        perda_Qc = perdaConducaoQ(-i)
        perda_Ds = perdaChaveamentoD(-i)
        perda_Dc = perdaConducaoD(-i)

    # As perdas calculadas são adicionadas às chaves de acordo com o estado
    # de cada chave no intervalo.
    # i) Perda de condução às chaves em função do tempo ativo (1, d ou 1-d)
    # ii) Perda de comutação às chaves que comutaram neste intervalo.
    # iii) Avaliação da adição das perdas à chave ou ao diodo em função do
    #      sentido da corrente.
    if intervalo == "A":
        perda_S1Q += 0                          #0
        perda_S1D += 0                          #0
        perda_S2Q += 0                          #0
        perda_S2D += 0                          #0
        perda_S3Q += perda_Qc                   #1
        perda_S3D += 0                          #1  #TODO Corrente reversa
        perda_S4Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S4D += 0                          #D' #TODO Corrente reversa
        perda_S5Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S5D += perda_Dc*( d ) + perda_Ds  #D
        perda_S6Q += 0                          #0
        perda_S6D += 0	                        #0
        
    elif intervalo == "B":
        perda_S1Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S1D += 0                          #D  #TODO Corrente reversa
        perda_S2Q += 0                          #0
        perda_S2D += 0                          #0
        perda_S3Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S3D += 0                          #D' #TODO Corrente reversa
        perda_S4Q += 0                          #0
        perda_S4D += 0                          #0
        perda_S5Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S5D += perda_Dc*(1-d) + perda_Ds  #D'
        perda_S6Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S6D += perda_Dc*( d ) + perda_Ds  #D
        
    elif intervalo == "C":
        perda_S1Q += perda_Qc                   #1
        perda_S1D += 0                          #1  #TODO Corrente reversa
        perda_S2Q += 0                          #0
        perda_S2D += 0                          #0
        perda_S3Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S3D += 0                          #D #TODO Corrente reversa
        perda_S4Q += 0	                        #0
        perda_S4D += 0	                        #0
        perda_S5Q += 0	                        #0
        perda_S5D += 0	                        #0
        perda_S6Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S6D += perda_Dc*(1-d) + perda_Ds  #D'
        
    elif intervalo == "D":
        perda_S1Q += 0                          #0
        perda_S1D += 0                          #0
        perda_S2Q += 0                          #0
        perda_S2D += 0                          #0
        perda_S3Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S3D += 0                          #D  #TODO Corrente reversa
        perda_S4Q += perda_Qc                   #1
        perda_S4D += 0                          #1  #TODO Corrente reversa
        perda_S5Q += 0                          #0
        perda_S5D += 0	                        #0
        perda_S6Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S6D += perda_Dc*(1-d) + perda_Ds  #D'
        
    elif intervalo == "E":
        perda_S1Q += 0                          #0
        perda_S1D += 0                          #0
        perda_S2Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S2D += 0                          #D' #TODO Corrente reversa
        perda_S3Q += 0                          #0
        perda_S3D += 0                          #0
        perda_S4Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S4D += 0                          #D  #TODO Corrente reversa
        perda_S5Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S5D += perda_Dc*(1-d) + perda_Ds  #D'
        perda_S6Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S6D += perda_Dc*( d ) + perda_Ds  #D
        
    else: #intervalo == "F"
        perda_S1Q += 0                          #0
        perda_S1D += 0                          #0
        perda_S2Q += perda_Qc                   #1
        perda_S2D += 0                          #1  #TODO Corrente reversa
        perda_S3Q += 0	                        #0
        perda_S3D += 0	                        #0
        perda_S4Q += perda_Qc*(1-d) + perda_Qs  #D'
        perda_S4D += 0                          #D' #TODO Corrente reversa
        perda_S5Q += perda_Qc*( d ) + perda_Qs  #D
        perda_S5D += perda_Dc*( d ) + perda_Ds  #D
        perda_S6Q += 0	                        #0
        perda_S6D += 0	                        #0
        
    # Salva os valores calculados neste chaveamento nos vetores
    # Para criação de gráfico.
    RAZAOCICLICA.append(d)
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

if I_linear:
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

print("Perdas nas chaves:")
print("    S1 Q = "+'{0:.2f}'.format(perda_S1Q)+" W")
print("       D = "+'{0:.2f}'.format(perda_S1D)+" W")
print("    S2 Q = "+'{0:.2f}'.format(perda_S2Q)+" W")
print("       D = "+'{0:.2f}'.format(perda_S2D)+" W")
print("    S3 Q = "+'{0:.2f}'.format(perda_S3Q)+" W")
print("       D = "+'{0:.2f}'.format(perda_S3D)+" W")
print("    S4 Q = "+'{0:.2f}'.format(perda_S4Q)+" W")
print("       D = "+'{0:.2f}'.format(perda_S4D)+" W")
print("    S5 Q = "+'{0:.2f}'.format(perda_S5Q)+" W")
print("       D = "+'{0:.2f}'.format(perda_S5D)+" W")
print("    S6 Q = "+'{0:.2f}'.format(perda_S6Q)+" W")
print("       D = "+'{0:.2f}'.format(perda_S6D)+" W")

print("\n")
potencia_saida = sum(POTENCIAINST)/len(POTENCIAINST)
perdas_bidir_ponte = perda_S1Q +   perda_S1D + perda_S2Q +   perda_S2D +  \
                     perda_S3Q +   perda_S3D + perda_S4Q +   perda_S4D +  \
                     perda_S5Q + 2*perda_S5D + perda_S6Q + 2*perda_S6D

perdas_bidir_2ch   = perda_S1Q +   perda_S1D + perda_S2Q +   perda_S2D +  \
                     perda_S3Q +   perda_S3D + perda_S4Q +   perda_S4D +  \
                     perda_S5Q +   perda_S5D + perda_S6Q +   perda_S6D

rend_ponte = (potencia_saida - perdas_bidir_ponte) / potencia_saida * 100
rend_2ch   = (potencia_saida - perdas_bidir_2ch  ) / potencia_saida * 100

print("Topologia com chave bidirecional em ponte de diodo")
print("    Rendimento = "+'{0:.2f}'.format(rend_ponte)+" %")
print("Topologia com chave bidirecional em anti-série")
print("    Rendimento = "+'{0:.2f}'.format(rend_2ch)  +" %")

plot([100*x for x in RAZAOCICLICA],label=u"Razão Cíclica (%)")
plot(CORRENTE,label=u"Corrente (A)")
plot(TENSAOREF,label=u"Tensão de Referência (V)")
legend()
xlabel(u"Índice do Ciclo de Chaveamento")
ylabel(u"Amplitude")
xlim([0,mf])
ylim([min(-V1-V2,min(CORRENTE))*1.1,max(V1+V2,max(CORRENTE))*1.1])
#plotlevels()
show()


print "\n\n"
print perda_S1Q, perda_S1D
print perda_S2Q, perda_S2D
print perda_S3Q, perda_S3D
print perda_S4Q, perda_S4D
print perda_S5Q, perda_S5D
print perda_S6Q, perda_S6D
        
#corrente = [100*formaDeOndaCorrenteNaoLinear(x*2*pi/360) for x in range(360)]
#corrente2 = [100*formaDeOndaCorrente(x*2*pi/360) for x in range(360)]

#plot([Ar*sin(x*2*pi/mf) for x in range(int(mf))])
#plot(corrente)
#plot(corrente2)
