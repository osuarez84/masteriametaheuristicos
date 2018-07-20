# -*- coding: utf-8 -*-


import random
import math
import numpy as np
import decimal
import csv

# Creamos una sol inicial mediante una permutación 
# de la lista inicial de los objetos
def  random_permutation(n):
    # Genera una solucion inicial de manera aleatoria
    # la solucion es un vector de unos y ceros indicando
    # si se selecciona o no dicho objeto para ser introducido
    # en la mochila    
    return (np.random.randint(2, size = n))
        
    

# Computamos un vecino utilizando distancia de Hamming
def neighbor(n):

    idx = random.randrange(0, len(n))
    
    # usamos distancia de Hamming para generar un vecino: 
    #toggleamos el valor de ese elemento
    if(n[idx] == 1):
        n[idx] = 0
    else:
        n[idx] = 1
            
    return n
            
    
def printIter(b_sol, b_cost, c, t):
    print("Temperatura: %.2f" % t)
    print("Iteracion: %d" % c)
    print("Mejor solucion: %s" % str(b_sol))
    print("Coste mejor solucion: %.2f" % b_cost)
    
# Computo de la probabilidad de aceptar
# una solución que ha empeorado el coste
def acceptance_probability(old, new, t):
    #print("Temperatura: "+ str(t))
    #print("Old cost: "+str(old))
    #print("New cost: "+str(new))
    return decimal.Decimal(((new - old) / t)).exp()



# Computo de la función de coste: en este caso...
# el sumatorio de los valores de los items de la mochila
def cost(s, p, r, ks, c):
    cost_val = 0
    
    # computamos el coste
    for i in range(0,len(s)):
        cost_val += s[i] * p[i]
        
    # comprobamos si sobrepasa alguna constraint,
    # en caso de que si imponemos penalización
    # a la funcion de coste
    
    for i in range(0,len(r)):
        x = 0.0
        
        for j in range(0, len(r[0])):
            x += r[i][j] * s[j]
        
    # si supera el peso de alguna constraint penalizamos     
        if(x > ks[i]):
            cost_val = 0
            break
    
    return cost_val



# Algorítmo Simulated Annealing
# En este ejemplo guardamos la mejor
# solución encontrada durante la búsqueda.
def anneal(sol, p_v, r_v, ks_w_v, optimal):

    T = 8000.0
    T_min = 0.01
    alpha = 0.8
    
    # iteraciones en cada temperatura
    iterations_T = 2000
    
    # contador de numero de eval de funcion de coste
    contador = 0
    
    # iteraciones totales
    total_iter = 100000
    
    old_cost = cost(sol, p_v, r_v, ks_w_v, contador)
    best_sol = sol
    best_cost = old_cost
    
    # escribimos fichero
    f = open('SA.csv','w', newline='')  
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    
    while (T > T_min):
        i = 1
        while (i <= iterations_T) & (contador <= total_iter): 
            new_sol = neighbor(sol)
            new_cost = cost(new_sol, p_v, r_v, ks_w_v, contador)
            contador += 1
            
            ap = acceptance_probability(old_cost, new_cost, T)
                
            # Si solución mejora anterior aceptamos siempre
            if new_cost > old_cost:
                sol = new_sol
                old_cost = new_cost
                # Guardamos la mejor solucion que hayamos encontrado
                if(old_cost > best_cost):
                    best_sol = sol
                    best_cost = old_cost
            # si no seleccionamos la nueva bajo cierta probabilidad
            elif(ap > random.uniform(0,1)):
                sol = new_sol
                old_cost = new_cost
                
            # printeamos en pantalla iteracion, mejor solucion y fitness
            printIter(best_sol, best_cost, contador, T)
                
            # si encontramos optimo salimos y printeamos
            if(best_cost == optimal):
                break
            
            # siguiente iteración
            i += 1
            
            # escribimos al fichero csv los datos
            myData = [str(T), str(best_cost), str(contador)]
            writer.writerow(myData)
        
        
        # rompemos el outer loop si hemos encontrado el optimo
        if(best_cost == optimal):
            print('Se ha encontrado el optimo!')
            break
        
        
        # enfriamiento temperatura
        T = T*alpha
    
    f.close()
    
    return best_sol, best_cost

###############################################################################

if __name__ == "__main__":
      
    filepath = 'knapsack_instance.txt'
    
    # Formato del problema:
    #     10 6                              constraints + n objetos
    #     100 600 1200 2400 500 2000        p => valores objetos
    #     80 96 20 36 44 48 10 18 22 24     ks_w => pesos maximos constraints
    #     8 12 13 64 22 41                  r[][] => todas las constraints
    #     8 12 13 75 22 41
    #     3 6 4 18 6 4
    #     5 10 8 32 6 12
    #     5 13 8 42 6 20
    #     5 13 8 48 6 20
    #     0 0 0 0 8 0
    #     3 0 4 0 8 0
    #     3 2 4 0 8 4
    #     3 2 4 8 8 4
    #    
    #     3800                              Optimo conocido
    
    
    
    
    # [1]
    # cargamos y preparamos el problema y las variables
    with open(filepath) as fp:
        line = fp.readline()
        
        # leemos constraints y variables
        f = list(map(int, line.split()))
        p = []
        a = int(f[1] / 10)
        # solamente hay una fila
        if(a == 0):
            a = 1
            
        n_obj = f[1]

        # sacamos valores objetos
        for i in range(0,a):
            aux = fp.readline()
            p.extend(list(map(float, aux.split())))
    
        # leemos pesos maximos mochilas
        b = int(f[0] / 10)
        if(b == 0):
            b = 1
        
        ks_w = []
        for i in range(0,b):
            aux = fp.readline()
            ks_w.extend(list(map(float, aux.split())))
        
        
        # leemos capacidades constraints
        # creamos el 2D array vacio
        w, h = f[1], f[0]
        r = [[0 for x in range(w)] for y in range(h)] 

        for i in range(0,f[0]):
            temp = []
            for j in range(0,a):
                aux = fp.readline()
                temp.extend(list(map(float, aux.split())))
                
                
            r[i][:] = temp
            
                
        # leemos el optimo
        aux = fp.readline()
        opt = fp.readline()
        opt = list(map(float, opt.split()))
        
                
    # [2]
    # lanzamos el algoritmo
    init_sol = random_permutation(n_obj)
    final_sol, cost_sol = anneal(init_sol, p, r, ks_w, opt)
    
    