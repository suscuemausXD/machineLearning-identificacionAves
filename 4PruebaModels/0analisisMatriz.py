import pandas as pd
import numpy as np

# Cargar la matriz de confusión desde un archivo CSV
matriz_confusion = pd.read_csv('D:\\Documentos\\UCC\\Machine Learning\\kode\\scripts\\4PruebaModels\\matriz_confusion.csv', index_col=0)

# Convertir la matriz de confusión a un array de numpy para los cálculos
matriz_confusion_numpy = matriz_confusion.to_numpy()

# Inicializar listas para almacenar los resultados
diagonal = []
fuera_diagonal = []

# Iterar sobre cada fila y columna
for i in range(matriz_confusion_numpy.shape[0]):  # Suponiendo que la matriz es cuadrada
    # Sumar todos los elementos fuera de la diagonal
    suma_fuera_diagonal = np.sum(matriz_confusion_numpy[i]) - matriz_confusion_numpy[i, i]
    diagonal_value = matriz_confusion_numpy[i, i]
    
    diagonal.append(diagonal_value)
    fuera_diagonal.append(suma_fuera_diagonal)

# Mostrar los resultados para cada clase
clases = matriz_confusion.shape[0]
for i in range(clases):
    clase_nombre = matriz_confusion.index[i]  # Accede al nombre de la clase desde el índice
    print(f"Clase {clase_nombre}:")
    print(f"  Suma fuera de la diagonal: {fuera_diagonal[i]}")
    print(f"  Valor en la diagonal: {diagonal[i]}")
    print()
