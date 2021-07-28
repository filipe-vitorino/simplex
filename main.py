from simplex import * 

def main():
    #Leitura do arquivo de entrada
    tam = input().split()
    m = int(tam[0])
    n = int(tam[1])
    entrada = input().split()
    c = []
    for aux in entrada:
       c.append((int(aux)))
    c = np.array(c)
    matrix_entrada = np.zeros((m,n+1))
    for li in range(m):
        lj = 0
        entrada = input().split()
        for aux in entrada:
            matrix_entrada[li][lj] = int(aux) 
            lj = lj + 1

    #Com a matrix de entrada criamos o vero-tm
    vero = inicia_vero(matrix_entrada, c, m, n)    
    
    status = 0
    #verifica se ha uma entrada negativa em b
    need_aux = any(vero[1: , -1] < 0)    
    #se possuir, a pl recisa de operacoes auxiliares
    if(need_aux):
        vero = vero_to_auxiliar(vero, m, n)    
        #forma canonica
        for i in range(1, len(vero)):
            vero[0] = vero[0] - vero[i]

        vero, status = simplex_primal(vero,m)
        if (np.isclose(vero[0][-1], 0)):
            vero = return_aux_to_vero(vero,c,m,n)
            vero, status = simplex_primal(vero,m)
        else:
            status = -1

    else:
        vero, status = simplex_primal(vero,m)
        
    
    show_result(vero, m, n, status)

if __name__ == "__main__":
    main()