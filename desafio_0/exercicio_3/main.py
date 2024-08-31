import os

os.system('cls')

def gerar_subconjuntos(conjunto, max_size=float('inf'), min_size=0, distinct_only = False, sort_subsets= False):   #Gera todos os subconjuntos 
        
    if distinct_only:
        conjunto = list(set(conjunto)) #Transformo em 'set' para tirar as duplicatas
    
    list_subset = [[]]
    
    for elemento in conjunto:
        aux_list = []
        for subset in list_subset:
            novo_subconjunto = subset + [elemento]     # Cria um novo subconjunto adicionando o elemento atual    
            aux_list.append(novo_subconjunto)       # Adiciona o novo subconjunto à lista de novos subconjuntos
        list_subset.extend(aux_list)           # Adiciona os novos subconjuntos à lista principal
    
    
    if max_size >=0:
        limited_list_size=[]
        
        for i in list_subset:
            if len(i)<=max_size:
                limited_list_size.append(i)
        
        list_subset = limited_list_size 
    
    if min_size:
        
        min_list_size = []
        
        for i in list_subset:
            if len(i) >= min_size:
                min_list_size.append(i)
            list_subset = min_list_size
        
        """for i in min_list_size:
            if i in list_subset:
                list_subset.remove(i)"""
                
    if sort_subsets:
        sorted_subsets = []
        for i in list_subset:
            sorted_subsets.append(sorted(i))
        list_subset = sorted_subsets
    
        sorted_by_length =[]
        
        for i in range(len(list_subset) + 1):
            for subset in list_subset:
                if len(subset) == i:
                    sorted_by_length.append(subset)
        list_subset = sorted_by_length
    
    
    return list_subset
    

if __name__ == "__main__":
    conjunto = [1,2]
    subconjuntos = gerar_subconjuntos(conjunto)

    print(subconjuntos)
