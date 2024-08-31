import os

os.system('cls')

def gerar_subconjuntos(conjunto):   #Gera todos os subconjuntos 
        
    list_subset = [[]]
    
    for elemento in conjunto:
        aux_list = []
        for subset in list_subset:
            novo_subconjunto = subset + [elemento]     # Cria um novo subconjunto adicionando o elemento atual    
            aux_list.append(novo_subconjunto)       # Adiciona o novo subconjunto à lista de novos subconjuntos
        list_subset.extend(aux_list)           # Adiciona os novos subconjuntos à lista principal
   
    return list_subset
    

if __name__ == "__main__":
    conjunto = {1,2}
    subconjuntos = gerar_subconjuntos(conjunto)

    print(subconjuntos)
