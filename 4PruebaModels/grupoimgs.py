import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configurar el dispositivo (GPU o CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Ruta al modelo guardado y al conjunto de prueba
model_path = 'D:\\Documentos\\UCC\\Machine Learning\\kode\\scripts\\Models\\modeloAvesResnet50.pth'
test_data_dir = 'D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAvesProcess\\val'

# Cargar el modelo completo
model = torch.load(model_path, map_location=device)  # Cargar el modelo completo
model = model.to(device)  # Mover modelo al dispositivo
model.eval()

# Transformación para las imágenes
test_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Cargar datos de prueba
test_data = ImageFolder(test_data_dir, transform=test_transforms)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

# Inicializar variables para la matriz de confusión
all_labels = []
all_predictions = []

# Evaluación del modelo
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)  # Mover datos al dispositivo
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        all_labels.extend(labels.cpu().numpy())  # Convertir a numpy
        all_predictions.extend(predicted.cpu().numpy())  # Convertir a numpy

# Calcular precisión
correct = sum(p == l for p, l in zip(all_predictions, all_labels))
total = len(all_labels)
print(f'Precisión en el conjunto de prueba: {100 * correct / total:.2f}%')

# Crear matriz de confusión
cm = confusion_matrix(all_labels, all_predictions)
class_labels = test_data.classes

# Guardar matriz de confusión como CSV
cm_df = pd.DataFrame(cm, index=class_labels, columns=class_labels)
cm_df.to_csv("matriz_confusion.csv", index=True, header=True)
print("Matriz de confusión guardada en 'matriz_confusion.csv'.")

# Mostrar los datos numéricos en consola
print("\nMatriz de Confusión (datos numéricos):")
print(cm_df)

# Graficar la matriz de confusión
plt.figure(figsize=(20, 20))
cmd = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)
cmd.plot(cmap="Blues", xticks_rotation="vertical", ax=plt.gca())
cmd.ax_.set_title("Matriz de Confusión", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
