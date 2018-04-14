import numpy as np
from random import sample

def creacion_ordenes(cant_tipos_produc, cant_ordenes, min_size, max_size):

    lista_ordenes = []  # Lista donde se almacenan todas las ordenes
    # Creacion de las ordenes
    for i in range(cant_ordenes):
        lista_ordenes.append(np.random.randint(1, cant_tipos_produc + 1, np.random.randint(min_size, max_size)))

    return lista_ordenes

def construccion_mapa(almacen_actual):
    return  [[0, 0, 0, 0, 0, 0, 0],
            [0, almacen_actual[0], almacen_actual[1], 0, almacen_actual[2], almacen_actual[3], 0],
            [0, almacen_actual[4], almacen_actual[5], 0, almacen_actual[6], almacen_actual[7], 0],
            [0, almacen_actual[8], almacen_actual[9], 0, almacen_actual[10], almacen_actual[11], 0],
            [0, almacen_actual[12], almacen_actual[13], 0, almacen_actual[14], almacen_actual[15], 0],
            [0, 0, 0, 0, 0, 0, 0]]

def dist_manhatann(inicio, fin, np_mapa):

    coor_inicio = np.where(np_mapa==inicio)
    coor_fin = np.where(np_mapa == fin)
    distancia = (abs(coor_inicio[0][0]-coor_fin[0][0])+abs(coor_inicio[1][0]-coor_fin[1][0]))
    return distancia

def creacion_poblacion(individuo_ejemplo, size_poblacion):
    # Creacion de poblacion
    poblacion = []
    for i in range(size_poblacion):
        poblacion.append(np.random.permutation(individuo_ejemplo)) #Permutando aleatoriamente obtenemos el nuevo individuo
        np.random.seed(np.random.randint(0,500)) #Cambiamos la semilla para que cada orden sea distinta a las otras
    return poblacion

def fitness_interno(lista_ordenes, almacen_actual):

    np_mapa = np.array(construccion_mapa(almacen_actual))
    dist_total = 0
    for j,i in enumerate(lista_ordenes): #Iteramos sobre todas las ordenes
        i = np.concatenate([[0],i]) #Agregamos la bahia al principio

        # Ordena el vector segun la distancia de manhatann utilizando busqueda avara
        for pasadas in range(len(i)-1):
            aux = []
            for k in range(pasadas,len(i)-1):
                aux.append(dist_manhatann(i[pasadas],i[k+1],np_mapa))
            pos_min = aux.index(min(aux))
            dist_total += min(aux)
            i[pasadas + 1], i[pos_min + pasadas + 1] = (i[pos_min + pasadas + 1], i[pasadas + 1]) #Intercambiamos posiciones

        lista_ordenes[j] = i #Añadimos la nueva orden ya ordenada
    promedio_dist = dist_total / len(lista_ordenes)
    print(np_mapa)
    return lista_ordenes, promedio_dist

if __name__ == "__main__" :

    np.random.seed(101) #Para que siempre trabajemos con las mismas ordenes
    lista_ordenes = creacion_ordenes(16,3,4,10)
    ejemplo_almacen = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    print(lista_ordenes)
    lista_ordenes_ordenada, fitness = fitness_interno(lista_ordenes,ejemplo_almacen)
    print(lista_ordenes_ordenada)
    print(fitness)



