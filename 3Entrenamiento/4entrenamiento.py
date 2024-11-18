import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm
from torch.optim.lr_scheduler import StepLR
import matplotlib.pyplot as plt
import winsound

# Configuración básica
data_dir = "D:\\Documentos\\UCC\\Machine Learning\\kode\\dataSetAvesProcess"
batch_size = 32
num_epochs = 75
num_classes = 54  # Número de especies
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
patience = 7  # Número de épocas sin mejora antes de detener el entrenamiento

# Transformaciones para preprocesamiento
data_transforms = {
    "train": transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]),
    "val": transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

# Función de entrenamiento con curvas de aprendizaje
def train_model(model, criterion, optimizer, scheduler, num_epochs=25, patience=5):
    best_model_wts = model.state_dict()
    best_acc = 0.0
    epochs_without_improvement = 0

    # Historial para curvas de aprendizaje
    train_losses = []
    val_losses = []
    train_accuracies = []
    val_accuracies = []

    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        print("-" * 10)

        for phase in ["train", "val"]:
            if phase == "train":
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in tqdm(dataloaders[phase]):
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(image_datasets[phase])
            epoch_acc = running_corrects.double() / len(image_datasets[phase])

            print(f"{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

            if phase == "train":
                train_losses.append(epoch_loss)
                train_accuracies.append(epoch_acc.item())
                scheduler.step()
            else:
                val_losses.append(epoch_loss)
                val_accuracies.append(epoch_acc.item())

                if epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = model.state_dict()
                    epochs_without_improvement = 0
                else:
                    epochs_without_improvement += 1

                if epochs_without_improvement >= patience:
                    print("Entrenamiento detenido por evaluación temprana.")
                    model.load_state_dict(best_model_wts)
                    plot_learning_curves(train_losses, val_losses, train_accuracies, val_accuracies)
                    return model

        torch.cuda.empty_cache()

    model.load_state_dict(best_model_wts)
    plot_learning_curves(train_losses, val_losses, train_accuracies, val_accuracies)
    return model

# Función para graficar curvas de aprendizaje
def plot_learning_curves(train_losses, val_losses, train_accuracies, val_accuracies):
    epochs = range(1, len(train_losses) + 1)

    plt.figure(figsize=(12, 5))

    # Pérdidas
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_losses, label="Entrenamiento")
    plt.plot(epochs, val_losses, label="Validación")
    plt.title("Pérdida por Época")
    plt.xlabel("Época")
    plt.ylabel("Pérdida")
    plt.legend()

    # Precisión
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accuracies, label="Entrenamiento")
    plt.plot(epochs, val_accuracies, label="Validación")
    plt.title("Precisión por Época")
    plt.xlabel("Época")
    plt.ylabel("Precisión")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Carga de datos
    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")
    image_datasets = {
        "train": datasets.ImageFolder(train_dir, data_transforms["train"]),
        "val": datasets.ImageFolder(val_dir, data_transforms["val"])
    }
    dataloaders = {
        "train": DataLoader(image_datasets["train"], batch_size=batch_size, shuffle=True, num_workers=4),
        "val": DataLoader(image_datasets["val"], batch_size=batch_size, shuffle=False, num_workers=4)
    }

    # Modelo preentrenado
    model = models.resnet50(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    # Parámetros y optimización
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = StepLR(optimizer, step_size=60, gamma=0.1)

    # Entrenar el modelo
    model = train_model(model, criterion, optimizer, scheduler, num_epochs=num_epochs, patience=patience)

    # Guardar el modelo entrenado
    torch.save(model, "D:\\Documentos\\UCC\\Machine Learning\\kode\\scripts\\Models\\modeloAvesResnet50.pth")
    print("Entrenamiento completo y modelo guardado.")
    winsound.PlaySound("C:\\Users\\Jesús Cuellar\\Downloads\\alarm.wav", winsound.SND_FILENAME)
