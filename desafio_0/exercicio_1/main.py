import os

os.system("cls")

def listaAsteristicos(n):
    lista = []
    
    for i in range(n):
        lista.append("*" * (i+1))
    
    return lista


if __name__ == "__main__":
    
    try:
        listSize = int(input("Enter the list size: "))
        print(listaAsteristicos(listSize))
    
    except ValueError:
        print("\nEnter a int number")