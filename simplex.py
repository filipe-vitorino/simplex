import numpy as np
# importing the library
#from memory_profiler import profile


#funcao auxiliar para debugg
def printa_resume(lista,m):
    
    for i in range(0,len(lista)):
        for j in range(m ,len(lista[i])):
            print("%.2f" % lista[i][j], end=' |')
        print('\n')
    print("\n")

#funcao auxiliar para debugg
def printa_all(lista):
    print("\n")
    for i in range(0,len(lista)):
        for j in range(0 ,len(lista[i])):
            print("%.2f" % lista[i][j], end=' |')
        print()
    print("\n")


#funcoes que encontra colunas compostas apenas de 0s, e um 1
#retorna um vetor em que onde se encontra base atribuiu a linha onde esta o 1
#e onde nao e base atribiu 0
def encontra_base(lista, m,n):
    j = 0
    k = 0
    col_base = np.zeros(n + m)
    
    while (j < n + m):
        base = True
        encontou = 0
        pos_linha = 0
        if(lista[0][j + m]  == 0):
            for i in range(1, len(lista)):
                if( lista[i][j + m] != 0 and lista[i][j+ m] != 1):
                    base = False
                    break
                if( lista[i][j + m] == 1):
                    pos_linha = i
                    encontou += 1
        else:
            base = False 
        
        if(base and encontou == 1):
            col_base[j] = pos_linha
        
        j += 1

    return(col_base)

#funcao para mostrar o resultado na tela
#indicamos se a funcao e otia/ilimitada/inviavel
#indicamos a funcao objetivo (z) caso otima
#indicamos a solucao viavel caso otima/ilimitada
#indicamos o vetor operacao caso otima/inviavel (o vetor operacao é o respectivo certificado)
#precisamos criar um certificado de ilimitada segundo as notas de aulos para pl ilimitadas
def show_result(matriz, m, n, status):
    
    
    pl_is = ''    
    base = encontra_base(matriz, m, n)

    if(status == 0):
        pl_is = 'otima'
    
    if(status == -1):    
        pl_is = 'inviavel'
    #na funcao do simples ele retorna a coluna onde as linhas todas sao negativas (caso ocorra)
    #lago sabemos que se satus > 0 temos uma pl ilimitada e o valor do status representa a coluna canditada a ilimitada
    if(status > 0):
        pl_is = 'ilimitada'
    
    print(pl_is)
    if(pl_is == 'otima'):
        #so printamos z caso otimo
        result = matriz[0][-1]
        print("%.7f" % result)
    
    if(pl_is != 'inviavel'):
        #so podemos mostras as solucoes viaveis caso nao seja inviavel
        for i in range(0,n):
            #encontramos no vero onde e base e seu valor correspondende tem b
            if (base[i] == 0 ):
                print("%.7f" % 0, end = ' ' )
            else:
                print( "%.7f" %  matriz[ int(base[i]) ][-1], end = ' ')
        
        print()
    
    if(pl_is != 'ilimitada' ):
        #certificados onde nao e ilimitada e o vetor de operacao da tableux vero tm
        for i in range(0,m):
            print("%.7f" % matriz[0][i], end = ' ' )
    else:
        #se ilimitada precisamos contruir nosso certificado usando a coluna onde se encontrou todos os valores negativos
        candidata = status
        certificado = np.zeros(n + m)
        for i in range(0, len(certificado)):
            if(base[i] != 0):
                certificado[i] = -1 * matriz[ int( base[i] )][ candidata ]
        
        certificado [candidata - m ] = 1
        for i in range(0, n):
            print("%.7f" % certificado[i] ,end = ' ')
        

#funcao operacao do simplex
def simplex_primal(vero, start):
  
    end_lin = len(vero[0])
    end_col = len(vero[:,0])
    b = end_lin - 1
    
    #verifica se existe entradas negativas
    #enquanto houver faça a escolha de base e os pivoteamentos
    while ( (vero[0, start : b] >= 0).all() == False ):  
        col = 0
        i = start  #comeca a partir da matriz de operacao

        #encontra a priemira coluna com entrada negativa
        while (i < end_lin - 1):
            if (vero[0][i] < 0):
                col = i  
                break  
            i += 1
        
        #escolher a linha do pivot
        #encontrar menor bij/Aij onde Aij > 0
        menor = 100000000
        lin = 0
        j = 1
        while (j < end_col):
            if (vero[j][col] > 0): 
                aux = vero[j][b] / vero[j][col]
                if (aux < menor):
                    menor = aux
                    lin = j            
            j += 1

        #se percorrer todas as linhas e nao conseguir achar um pivot
        #logo existe uma coluna onde todas as linhas sao negativas
        #uma pl ilimitada, retorna a coluna candidata a ilimitada 
        if (lin == 0):
            return vero, col

        #pivot
        elem = vero[lin][col]  
        vero[lin] = vero[lin] / elem

        #pivotear linhas de cima e baixo
        i = 0
        while (i < end_col):
            if i != lin:
                vero[i] = vero[i] - (vero[i][col] * vero[lin])
            i += 1

    return vero, 0


#Reunir matriz de operacao, matrix A, vetor b, vetor -c em um unico tableux
#registrado pelo coutinho como VEROtm
def inicia_vero(matriz, c, m, n):

    A = np.array(matriz[:,0:n])
    b = np.array(matriz[:,-1])

    identity = np.identity(m)
    matrix_operacao = np.vstack([np.zeros(m), identity])
        
    A = np.vstack([c * -1, A])
    base = np.vstack([np.zeros(m), identity])
    b = np.append(0,b)
    vero = np.column_stack((matrix_operacao,A,base,b))
    
    return vero

#funcao que retorna uma matrix identidade mais uma linha zerada 
def cria_base(tam):
    identity = np.identity(tam)
    base = np.vstack([np.zeros(tam), identity])
    return base


#Quando ha entrada negativa em b
#sao necessarios operacoes preventivas antes de aplicar o simplex
#(1)precisa primeiro remover as entraadas negativas, com operacao de multiplicacao (*-1)
#(2)preisa adicionar variaveis auxiliar (n confundir com variaveis de folga)
#(3) e trocar o vetor -c do tabloux por um vetor de 0s e 1s (1 apenas em cima das variaveis novas) 
def vero_to_auxiliar(vero, m, n):

    linhas = vero.shape[0]
    #(1)
    for i in range(1, linhas):
        if (vero[i][-1] < 0):
            vero[i] = vero[i] * -1

    base = cria_base(m)   
    #2
    vero = np.column_stack((vero[1: , : -1 ], base[1:, : ], vero[1:, -1] ))
    #(3)   
    start = 2*m + n
    new_line = np.zeros(start)
    line_aux = np.ones(m)
    new_line = np.append(new_line, line_aux)
    new_line = np.append(new_line, 0)

    vero = np.vstack([new_line, vero])
    return vero



#Apos realizarmos operacoes de simplex no vero auxiliar 
#e encontrarmos um valor objetivo = 0
#sabemos que a pl é viavel
#logo precisamos prepara-la pra outra rodada do simplex
#(1)removemos as variaveis auxiliares do tableux
#(2)retornamos o vetor -c
#(3)recomecamos as operacoes da matriz de operacao
def return_aux_to_vero(vero, c, m, n):
    start = 2*m + n  
    start_vero = m - 1
    #(1)
    vero = np.delete(vero, np.s_[start : start+m ],axis=1)    
    #(2)
    vero[0, start_vero + 1 : start_vero + n + 1  ] = c * -1
    #(3)
    vero[0, : m] = np.zeros(m)
    
    return vero
        