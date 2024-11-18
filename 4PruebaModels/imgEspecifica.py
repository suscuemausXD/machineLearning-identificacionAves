import torch
from torchvision import models, transforms
from PIL import Image

# Definir el dispositivo (GPU si está disponible, de lo contrario CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo completo
modelo_path = 'D:\\Documentos\\UCC\\Machine Learning\\kode\\scripts\\Models\\modeloAvesResnet50.pth'
model = torch.load(modelo_path)
model = model.to(device)  # Mover el modelo al dispositivo
model.eval()

# Transformaciones para la imagen
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Función para predecir la clase de una imagen
def predecir_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen).convert('RGB')
    imagen = transform(imagen).unsqueeze(0)  # Agregar dimensión batch
    imagen = imagen.to(device)  # Mover la imagen al mismo dispositivo que el modelo
    with torch.no_grad():
        salida = model(imagen)
        _, prediccion = torch.max(salida, 1)
    return prediccion.item()

# Probar con una imagen específica
ruta_imagen_prueba = 'D:\\Documentos\\UCC\\Machine Learning\\kode\\scripts\\4PruebaModels\\imgProb\\images.jpg'
prediccion = predecir_imagen(ruta_imagen_prueba)
print(f'La clase predicha para la imagen es: {prediccion}')
