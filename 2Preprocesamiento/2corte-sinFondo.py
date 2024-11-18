import cv2
import winsound
from PIL import Image
import numpy as np
import io
import os
from rembg import remove

def crop_resize_remove_bg(image_path, output_size=(224, 224), background_color=(255, 255, 255)):
    # Cargar la imagen y eliminar el fondo
    with open(image_path, "rb") as img_file:
        input_image = img_file.read()
    
    no_bg_data = remove(input_image)
    no_bg_image = Image.open(io.BytesIO(no_bg_data)).convert("RGBA")
    
    # Crear una nueva imagen con fondo sólido
    solid_bg_image = Image.new("RGBA", no_bg_image.size, background_color + (255,))
    solid_bg_image.paste(no_bg_image, mask=no_bg_image.split()[3])  # Usar el canal alfa como máscara
    
    # Convertir a OpenCV para manipulación
    cv_image = np.array(solid_bg_image.convert("RGB"))
    
    # Convertir la imagen a escala de grises para detectar contornos
    gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Recortar al área del contorno más grande (suponiendo que es el ave)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cv_image = cv_image[y:y+h, x:x+w]
    
    # Redimensionar manteniendo la relación de aspecto
    h, w, _ = cv_image.shape
    aspect_ratio = w / h
    
    if aspect_ratio > 1:  # Imagen más ancha que alta
        new_w = output_size[0]
        new_h = int(new_w / aspect_ratio)
    else:  # Imagen más alta que ancha
        new_h = output_size[1]
        new_w = int(new_h * aspect_ratio)
    
    resized_image = cv2.resize(cv_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Crear fondo sólido y centrar la imagen redimensionada
    final_image = Image.new("RGB", output_size, background_color)
    resized_pil_image = Image.fromarray(resized_image)
    
    # Calcular la posición para centrar la imagen redimensionada
    x_offset = (output_size[0] - new_w) // 2
    y_offset = (output_size[1] - new_h) // 2
    final_image.paste(resized_pil_image, (x_offset, y_offset))
    
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
                processed_image = crop_resize_remove_bg(image_path, output_size, background_color)
                
                # Guardar la imagen procesada en la carpeta correspondiente en output_folder
                output_path = os.path.join(output_dir, filename)
                processed_image.save(output_path)
                print(f"Imagen procesada y guardada en: {output_path}")

# Ejemplo de uso
input_folder = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAves"
output_folder = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAvesProcess"

# Procesar todas las imágenes en la estructura de carpetas
process_images_in_folder(input_folder, output_folder)
winsound.PlaySound("C:\\Users\\Jesús Cuellar\\Downloads\\alarm.wav", winsound.SND_FILENAME)