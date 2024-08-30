import os

os.system('cls')

def par_menor_diferenca(array, allow_duplicates=True, sorted_pairs = False, unique_pairs = False):
    
    menor_diferenca = float('inf')
    pairs = []
    
    if len(array) < 2:
        return []
    
    for i in range(len(array) - 1):
        for j in range(i + 1, len(array)):
            a, b = array[i], array[j]
            
            if abs(a-b) == 0 and allow_duplicates == False:
                pass
                
            elif abs(a - b) < menor_diferenca:
                pairs=[]
                menor_diferenca = abs(a - b) #'abs' retorna o valor absoluto
                pairs.append((a, b))
                
            elif abs(a - b) == menor_diferenca:
                pairs.append((a, b))
                
    if  not allow_duplicates: #Se o parametro 'allow_duplicates' == False
        
        pares_filtrados = []
        
        for a,b in pairs:
            if a != b:
                pares_filtrados.append((a,b))
        pairs = pares_filtrados
        
        
    if sorted_pairs: #Se o parametro 'sorted_pairs' == True
        
        pares_ordenados = []
        
        for par in pairs:
            par_ordenado = tuple(sorted(par))
            pares_ordenados.append(par_ordenado)
            
        pairs = pares_ordenados
        
    if unique_pairs:  #Se o parametro 'unique_pairs' == True
        
        pares_unicos = []
        
        for par in pairs:
            if (par not in pares_unicos) and ((par[1], par[0]) not in pares_unicos):
                pares_unicos.append(par)
        
        pairs = pares_unicos    
                
            
    return pairs


if __name__ == "__main__":
    
    list_size = int(input("Enter list size: "))
    os.system('cls')
    array = []
    
    for i in range(list_size):
        n = int(input(f"Enter the index element {i}: "))
        array.append(n)
        
    os.system('cls')
    print(f"list: {array}\n")

    resultado=par_menor_diferenca(array)

    print(f"Output: {resultado}")