#--------INICIALIZAR ARCHIVOS-----------------#
archivo = open("C:/Users/romer/Desktop/Python/automatas/dfa_input.txt", "r")
salida = open("C:/Users/romer/Desktop/Python/automatas/salida_min.txt", "w")

datos = archivo.read().splitlines()

estados = []

estados_not_print = [] #Esto es solo para hacer los for entre los estados, no imprimira en la salida

finales = []

movements = {}

alfabeto = []

marcados = []

no_marcados = []

#------------OBTENCION DE DATOS---------------------#
for i in datos:

    if datos.index(i) > datos.index("Estados") and datos.index(i) < datos.index("Alfabeto"):
        if i[0] == '*' or i[0] == '>':
            movements[i[1:]] = {}
            estados_not_print.append(i[1:])
            estados.append(i)
            if i[0] == '*':
                finales.append(i[1:])
        else:
            movements[i] = {} #Para casos donde el alfabeto sea del tipo q0,q1,q2 
            estados_not_print.append(i)
            estados.append(i)

    elif datos.index(i) > datos.index("Alfabeto") and datos.index(i) < datos.index("Transiciones"):
        alfabeto.append(i)
    
    elif datos.index(i) > datos.index("Transiciones"):
        lista = i.split()
        if lista[1] not in movements[lista[0]]:
            movements[lista[0]][lista[1]] = [lista[3]]
        else:
            movements[lista[0]][lista[1]].append(lista[3])

print("Estados",estados)
print("Alfabeto",alfabeto)
print("Transiciones",movements,"\n")



#-----------PRIMER PASO DE PARES--------------#
for i in estados_not_print:
    for j in estados_not_print:
        if bool(i in finales) != bool(j in finales):
            if (j,i) not in marcados:
                marcados.append((i,j))
        else:
             if (j,i) not in no_marcados and i != j:
                no_marcados.append((i,j))



#----------CICLO DEL ALGORITMO------------------#
stop = False
while stop==False:
    size = len(marcados)

    for pair in no_marcados:
        for letter in alfabeto:
            tupla = tuple((movements[pair[0]][letter][0], movements[pair[1]][letter][0]))
            if tupla in marcados and pair not in marcados:
                marcados.append(pair)
                no_marcados.remove(pair)

    if len(marcados) == size:
        break


for e in estados_not_print:
    inTuple = 0
    for tupla in no_marcados:
        if e in tupla:
            inTuple += 1
    if inTuple == 0:
        no_marcados.append(tuple(e))



print("NO MARCADOS: ",no_marcados)


new_movements = {}
stop2 = False

while stop2 == False:
    len_mark = len(no_marcados)
    remove = []
    string = list(no_marcados[0])

    for tupla in no_marcados:
        for x in tupla:
            if x in string:
                string += list(tupla)
                remove.append(tupla)
                break



    for re in remove:
        no_marcados.remove(re)

    lista_str = list(set(string))
    if lista_str:  
        lista_str.sort()
        str_dic = '{'+ ','.join(str(letter) for letter in lista_str) + '}'
        new_movements[str_dic] = {}

    if len_mark == len(no_marcados) or len(no_marcados) == 0:
        break

for left in no_marcados:
    str_dic = '{'+ ','.join(str(letter) for letter in left) + '}'
    new_movements[str_dic] = {}

print(new_movements)

salida.close()
archivo.close()