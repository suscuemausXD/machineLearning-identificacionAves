import os

def contar_imagenes_en_carpetas(ruta_carpeta_principal):
    # Definir extensiones de imagen comunes
    extensiones_imagen = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    
    # Recorrer todas las subcarpetas
    for nombre_carpeta in os.listdir(ruta_carpeta_principal):
        ruta_subcarpeta = os.path.join(ruta_carpeta_principal, nombre_carpeta)
        
        # Verificar si es una carpeta
        if os.path.isdir(ruta_subcarpeta):
            # Contar solo archivos con extensiones de imagen
            contador_imagenes = sum(
                1 for archivo in os.listdir(ruta_subcarpeta)
                if os.path.splitext(archivo)[1].lower() in extensiones_imagen
            )
            print(f"Carpeta '{nombre_carpeta}': {contador_imagenes} imágenes")

# Ejemplo de uso
ruta_carpeta_principal = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAves"
contar_imagenes_en_carpetas(ruta_carpeta_principal)
