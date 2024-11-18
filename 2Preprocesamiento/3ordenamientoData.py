import os
import shutil
from sklearn.model_selection import train_test_split
import winsound
# Ruta a tu dataset original
input_folder = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAvesProcess"
output_train_folder = os.path.join(input_folder, "train")
output_val_folder = os.path.join(input_folder, "val")

# Crear carpetas de destino
os.makedirs(output_train_folder, exist_ok=True)
os.makedirs(output_val_folder, exist_ok=True)

# Iterar sobre las carpetas de especies
for species_folder in os.listdir(input_folder):
    species_path = os.path.join(input_folder, species_folder)
    
    # Saltar las carpetas de train y val si ya existen
    if species_folder in ["train", "val"]:
        continue
    
    if os.path.isdir(species_path):
        # Obtener todas las imágenes de la especie
        images = [img for img in os.listdir(species_path) if img.endswith((".jpg", ".png", ".jfif"))]
        
        # Dividir imágenes en entrenamiento y validación
        train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)
        
        # Crear carpetas específicas para cada especie en train y val
        train_species_folder = os.path.join(output_train_folder, species_folder)
        val_species_folder = os.path.join(output_val_folder, species_folder)
        os.makedirs(train_species_folder, exist_ok=True)
        os.makedirs(val_species_folder, exist_ok=True)
        
        # Mover las imágenes a sus carpetas correspondientes
        for img_name in train_images:
            shutil.move(os.path.join(species_path, img_name), os.path.join(train_species_folder, img_name))
        
        for img_name in val_images:
            shutil.move(os.path.join(species_path, img_name), os.path.join(val_species_folder, img_name))

print("Organización completa. Las imágenes se han dividido en conjuntos de entrenamiento y validación.")
winsound.PlaySound("C:\\Users\\Jesús Cuellar\\Downloads\\alarm.wav", winsound.SND_FILENAME)