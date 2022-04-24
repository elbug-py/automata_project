#--------INICIALIZAR ARCHIVOS-----------------#
archivo = open("C:/Users/romer/Desktop/Python/automatas/nfa4.txt", "r")
salida = open("C:/Users/romer/Desktop/Python/automatas/salida.txt", "w")

datos = archivo.read().splitlines()

estados = []

movements = {}

alfabeto = []

#------------OBTENCION DE DATOS---------------------#
for i in datos:

    if datos.index(i) > datos.index("Estados") and datos.index(i) < datos.index("Alfabeto"):
        if len(i) == 1:
            movements[i] = {}
            estados.append(i)
        else:
            if i[1] == ' ':
                movements[i[2:]] = {}
                estados.append(i)
            else:
                movements[i[1:]] = {} #Para casos donde el alfabeto sea del tipo q0,q1,q2 
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



#-----------PRIMER PASO DE MOVIMIENTOS--------------#
new_movements = {}

for state in movements:
    for letter in movements[state]:
        string = '{'+ ','.join(str(key) for key in movements[state][letter]) + '}'
        new_movements[string] = {}
        for letter in alfabeto:
            new_movements[string][letter] = []


remove = []

for i in new_movements:
    temp = i[1:-1].split(",")
    for j in temp:
        if movements[j]:
            for letter in alfabeto:
                temp2 = movements[j][letter]
                for k in temp2:
                    if k not in new_movements[i][letter]:
                        new_movements[i][letter].append(k)

for i in new_movements:
    if new_movements[i]['0'] and new_movements[i]['1']:
        continue
    else:
        remove.append(i)
        

#------BORRAR VACIOS----------#
for keys in remove:
    del new_movements[keys]

print("Primera Iteracion",new_movements)


#----------ESTO TIENE QUE SER UN CICLO------------------#
stop = False
while stop==False:
    new2 = dict(new_movements)
    list2 = list(new2.keys())


    for state in new2:
        for letter in new2[state]:
            string = '{'+ ','.join(str(key) for key in new2[state][letter]) + '}'
            if string not in list(new_movements.keys()):
                new_movements[string] = {}
                for letter in alfabeto:
                    new_movements[string][letter] = []

    for i in new_movements:
        temp = i[1:-1].split(",")
        for j in temp:
            if movements[j]:
                for letter in alfabeto:
                    temp2 = movements[j][letter]
                    #print(i,letter,temp2)
                    for k in temp2:
                        if k not in new_movements[i][letter]:
                            new_movements[i][letter].append(k)

    if len(list2) == len(list(new_movements.keys())):
        break

print("Resultado final", new_movements)

salida.writelines("Estados\n")
for i in list(new_movements.keys()):
    init = False
    end = False
    string_init = '>'+i[1:-1]
    

    if string_init in estados:
        salida.writelines(f'>{i}\n')
        init = True
    else:
        new_arr = i[1:-1].split(',')
        for j in new_arr:
            string_end = '*'+j
            if string_end in estados:
                salida.writelines(f'*{i}\n')
                end = True
    if init == False and end == False: 
        salida.writelines(f'{i}\n')
        
salida.writelines("Alfabeto\n")
for i in alfabeto:
    salida.writelines(f'{i}\n')
salida.writelines("Transiciones\n")
for i in new_movements:
    for j in alfabeto:
        string = '{'+ ','.join(str(key) for key in new_movements[i][j]) + '}'
        salida.writelines(f'{i} {j} ->  {string}\n')

salida.close()
archivo.close()