import os
from PIL import Image
import random
import winsound
def contar_imagenes_y_completar(ruta_dataset, minimo_imagenes=1020):
    # Recorre cada carpeta de especie dentro del dataset
    for especie in os.listdir(ruta_dataset):
        ruta_especie = os.path.join(ruta_dataset, especie)
        
        if os.path.isdir(ruta_especie):  # Confirma que es una carpeta
            imagenes = [img for img in os.listdir(ruta_especie) if img.endswith(('.jpg', '.jpeg', '.png', 'jfif'))]
            cantidad_imagenes = len(imagenes)
            print(f"Especie: {especie} - Imágenes actuales: {cantidad_imagenes}")
            
            if cantidad_imagenes < minimo_imagenes:
                # Duplica y rota imágenes para completar el mínimo necesario
                faltantes = minimo_imagenes - cantidad_imagenes
                indice = 0
                
                while faltantes > 0:
                    imagen_path = os.path.join(ruta_especie, imagenes[indice % cantidad_imagenes])
                    imagen = Image.open(imagen_path)
                    
                    # Convertir la imagen a RGB si está en RGBA
                    if imagen.mode == 'RGBA':
                        imagen = imagen.convert('RGB')

                    # Rotación aleatoria de 90, 180 o 270 grados
                    angulo = random.choice([90, 180, 270])
                    imagen_rotada = imagen.rotate(angulo)
                    
                    # Guardar la imagen rotada en la carpeta
                    nueva_imagen_path = os.path.join(ruta_especie, f"copia_{indice}.jpg")
                    imagen_rotada.save(nueva_imagen_path)
                    
                    indice += 1
                    faltantes -= 1
                
                print(f"Especie {especie} completada con {minimo_imagenes} imágenes.")

# Ruta del dataset
ruta_dataset = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAves"
contar_imagenes_y_completar(ruta_dataset)
winsound.PlaySound("C:\\Users\\Jesús Cuellar\\Downloads\\alarm.wav", winsound.SND_FILENAME)