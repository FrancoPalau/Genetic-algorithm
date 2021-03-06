import numpy as np
import matplotlib.pyplot as plt

# TO DO LIST:
#             _ Ver tema de copia de mejores padres
#             _ Agregar algoritmo con restricciones para el fitness interno (ver opcion tabla)
#             _ Optimizar la construccion del mapa


def creacion_ordenes(cant_tipos_produc, cant_ordenes, min_size, max_size):
    """
    Funcion que recibe la cantidad de tipos de productos, la cantidad de ordenes,
    y el maximo y minimo tamaño posible de las ordenes.
    Se crea una lista donde se almacenan las ordenes creadas (numpy arrays).
    Se crean tantas ordenes como cant_ordenes.
    Cada orden puede tener una longitud variable entre [min_size,max_size] y contener
    cualquier tipo de producto desde 1 hasta cant_tipos_produc
    """
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
            [0, 0, 0, 0, 0, 0, 0],
            [0, almacen_actual[16], almacen_actual[17], 0, almacen_actual[18], almacen_actual[19], 0],
            [0, almacen_actual[20], almacen_actual[21], 0, almacen_actual[22], almacen_actual[23], 0],
            [0, almacen_actual[24], almacen_actual[25], 0, almacen_actual[26], almacen_actual[27], 0],
            [0, almacen_actual[28], almacen_actual[29], 0, almacen_actual[30], almacen_actual[31], 0],
            [0, 0, 0, 0, 0, 0, 0]]

def dist_manhatann(inicio, fin, np_mapa):
    coor_inicio = np.where(np_mapa==inicio)
    coor_fin = np.where(np_mapa == fin)
    distancia = (abs(coor_inicio[0][0]-coor_fin[0][0])+abs(coor_inicio[1][0]-coor_fin[1][0]))
    return distancia

def creacion_poblacion(individuo_ejemplo, size_poblacion):
    """
    Funcion que recibe un individuo ejemplo (numpy array) y el tamaño
    de la poblacion (int). A ese individuo ejemplo se le realizan permutaciones
    aleatorias para crear una poblacion donde todos los individuos contienen
    todos los tipos de productos (sin repeticion) y a su vez son aleatoriamente
    distintos de los otros.
    Retorna la poblacion creada (list of numpy arrays)
    """
    poblacion = []
    for i in range(size_poblacion):
        poblacion.append(np.random.permutation(individuo_ejemplo)) #Permutando aleatoriamente obtenemos el nuevo individuo
    return poblacion

def fitness_interno(lista_ordenes, almacen_actual):
    """
    Funcion que dada una lista de ordenes (list of numpy arrays) y una configuracion
    del almacen (almacen_actual, numpy array) calcula el fitness para ese almacen (individuo).
    Este fitness es la distancia promedio por orden, basada en la distancia de Manhatann y
    resuelta con un algoritmo de busqueda avara.
    Retorna el valor de fitness para el almacen dado
    """
    np_mapa = np.array(construccion_mapa(almacen_actual)) #Armamos el mapa segun nuestro layout
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

    promedio_dist = dist_total / len(lista_ordenes)
    return promedio_dist

def seleccion_padres(fitness_actual, poblacion_actual):
    """
    Funcion que recibe la poblacion actual (list of numpy arrays)
    y ordena los individuos segun su fitness.
    Retorna los k/2 mejores individuos, donde k es la cantidad de
    individuos de toda la poblacion.
    """
    poblacion_aux = poblacion_actual.copy()
    fitness_sorted = sorted(fitness_actual)
    for i in range(int(len(fitness_actual) / 2)):
        poblacion_actual[i] = poblacion_aux[fitness_actual.index(fitness_sorted[i])]
        fitness_actual[fitness_actual.index(fitness_sorted[i])] = -1
    # poblacion_actual[int((len(fitness_actual) / 2)):] = poblacion_actual[:int((len(fitness_actual) / 2))]
    return poblacion_actual[:int((len(fitness_actual) / 2))]

def cruzamiento(poblacion_actual):
    """
    Funcion que recibe la poblacion actual (list of numpy arrays)
    y realiza un cruce de orden, donde se obtienen 2 nuevos hijos
    y se modifica la poblacion actual.
    No retorna nada ya que la poblacion se pasa por referencia.
    """
    for i in range(0,len(poblacion_actual)-1,2):
        p_cruce_1 = np.random.randint(0, len(poblacion_actual[0]) - 1)
        p_cruce_2 = np.random.randint(p_cruce_1 + 1, len(poblacion_actual[0]))
        aux1 = poblacion_actual[i][p_cruce_1:p_cruce_2]
        aux2 = poblacion_actual[i+1][p_cruce_1:p_cruce_2]
        aux_ord_1 = np.concatenate([poblacion_actual[i][p_cruce_2:],poblacion_actual[i][:p_cruce_2]])
        aux_ord_2 = np.concatenate([poblacion_actual[i+1][p_cruce_2:],poblacion_actual[i+1][:p_cruce_2]])
        dif = len(poblacion_actual[i]) - p_cruce_1
        for gen in aux_ord_1:
            if gen not in aux2:
                aux2 = np.append(aux2,[gen])
        poblacion_actual[i] = np.concatenate([aux2[dif:],aux2[:dif]])
        for gen in aux_ord_2:
            if gen not in aux1:
                aux1 = np.append(aux1, [gen])
        poblacion_actual[i+1] = np.concatenate([aux1[dif:], aux1[:dif]])

def mutacion(poblacion_actual):
    """
    Funcion que recibe la poblacion actual (list of numpy arrays)
    y realiza una mutacion por cada individuo.
    Esta mutacion consiste en seleccionar 2 genes al azar e intercambiarlos.
    No retorna nada ya que la poblacion se pasa por referencia.
    """
    for i in range(0, len(poblacion_actual)):
        gen_1 = np.random.randint(0, len(poblacion_actual[0]))
        gen_2 = np.random.randint(0, len(poblacion_actual[0]))
        poblacion_actual[i][gen_1], poblacion_actual[i][gen_2] = (poblacion_actual[i][gen_2], poblacion_actual[i][gen_1])


if __name__ == "__main__" :

    fig, axes = plt.subplots()

    #----Creacion de las Ordenes----#
    np.random.seed(101) #Para que siempre trabajemos con las mismas ordenes
    lista_ordenes = creacion_ordenes(32,20,4,10)

    #----Creacion de la poblacion inicial----#
    ejemplo_almacen = np.arange(1,33)
    poblacion_actual = creacion_poblacion(ejemplo_almacen,100)

    #----Calculo del fitness de la poblacion inicial----#
    fitness_actual = []
    for individuo in poblacion_actual:
        fitness_actual.append(fitness_interno(lista_ordenes.copy(),individuo))
    fitness_prom = sum(fitness_actual)/len(poblacion_actual)

    #----Loop del algo genetico----#
    vec_fit_prom = []
    vec_fit_prom.append(fitness_prom)
    vec_fit_best = []
    vec_fit_best.append(min(fitness_actual))
    vec_it = []
    it = 0
    vec_it.append(it)
    while(it < 3):

        #----Seleccion Padres----#
        poblacion_actual = seleccion_padres(fitness_actual,poblacion_actual)
        mejores_padres = poblacion_actual.copy()

        #----Evolucion----#
        cruzamiento(poblacion_actual)
        mutacion(poblacion_actual)

        #----Añado los hijos con los mejores padres a la poblacion---#
        poblacion_actual = np.concatenate([mejores_padres,poblacion_actual])

        #----Calculo fitness----#
        fitness_actual = []
        for individuo in poblacion_actual:
            fitness_actual.append(fitness_interno(lista_ordenes.copy(), individuo))
        fitness_prom = sum(fitness_actual) / len(poblacion_actual)

        print("IT:",it,"Fitness",fitness_prom, "Best Fitness", min(fitness_actual))

        vec_fit_prom.append(fitness_prom)
        vec_fit_best.append(min(fitness_actual))
        it+=1
        vec_it.append(it)

    #---Graficamos---#
    axes.set_xlabel('Iteraciones')
    axes.set_ylabel('Fitness')
    axes.set_title('Fitness almacen')
    plt.plot(vec_it,vec_fit_prom, label="Fitness promedio")
    plt.plot(vec_it,vec_fit_best, label="Mejor Fitness")
    plt.legend()
    plt.show()

