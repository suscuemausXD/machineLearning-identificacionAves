import cv2
from PIL import Image
import numpy as np
import os
import winsound

def crop_and_resize_image(image_path, output_size=(224, 224)):
    # Cargar la imagen usando PIL y convertirla a formato compatible con OpenCV
    image = Image.open(image_path).convert("RGB")
    cv_image = np.array(image)
    
    # Convertir la imagen a escala de grises para detectar el objeto principal
    gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)  # Invertir para que el ave esté en blanco
    
    # Encontrar contornos del ave
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Recortar al área del contorno más grande (suponiendo que es el ave)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cv_image = cv_image[y:y+h, x:x+w]
    
    # Redimensionar la imagen
    cv_image = cv2.resize(cv_image, output_size, interpolation=cv2.INTER_AREA)
    
    # Convertir de nuevo a imagen PIL para guardar o mostrar
    final_image = Image.fromarray(cv_image)
    return final_image

def process_images_in_folder(input_folder, output_folder, output_size=(224, 224), background_color=(255, 255, 255)):
    # Recorrer las carpetas y subcarpetas en input_folder
    for root, _, files in os.walk(input_folder):
        # Crear la carpeta correspondiente en output_folder
        relative_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, relative_path)
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in files:
            # Procesar solo imágenes con extensiones válidas
            if filename.endswith((".jpg", ".png", ".jfif")):
                image_path = os.path.join(root, filename)
                
                # Procesar la imagen
                processed_image = crop_and_resize_image(image_path, output_size)
                
                # Guardar la imagen procesada en la carpeta correspondiente en output_folder
                output_path = os.path.join(output_dir, filename)
                processed_image.save(output_path)
                print(f"Imagen procesada y guardada en: {output_path}")

# Ejemplo de uso
input_folder = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAves"
output_folder = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAvesCut"

# Procesar todas las imágenes en la estructura de carpetas
process_images_in_folder(input_folder, output_folder)
winsound.PlaySound("C:\\Users\\Jesús Cuellar\\Downloads\\alarm.wav", winsound.SND_FILENAME)
