import fs from 'fs';
import path from 'path';
import axios from 'axios';

// Ruta donde se encuentran los archivos JSON
const jsonDir = './json-files-dataAves';  // Cambia esta ruta según donde estén tus archivos JSON
const imagesDir = './dataSetAves';    // Carpeta principal donde se guardarán las imágenes

// Función para crear una carpeta si no existe
function createFolderIfNotExists(folderPath) {
    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
    }
}

// Función para descargar y guardar una imagen
async function downloadImage(url, outputPath) {
    const response = await axios.get(url, { responseType: 'stream' });
    response.data.pipe(fs.createWriteStream(outputPath));
    return new Promise((resolve, reject) => {
        response.data.on('end', () => resolve());
        response.data.on('error', (err) => reject(err));
    });
}

async function processJsonFiles() {
    // Crear carpeta principal de imágenes si no existe
    createFolderIfNotExists(imagesDir);

    // Leer todos los archivos JSON en la carpeta especificada
    const jsonFiles = fs.readdirSync(jsonDir).filter(file => file.endsWith('.json'));

    for (const file of jsonFiles) {
        const jsonFilePath = path.join(jsonDir, file);
        const jsonData = JSON.parse(fs.readFileSync(jsonFilePath, 'utf-8'));

        // Crear una carpeta específica para cada archivo JSON
        const folderName = path.parse(file).name; // Nombre de la carpeta sin extensión
        const folderPath = path.join(imagesDir, folderName);
        createFolderIfNotExists(folderPath);

        console.log(`Descargando imágenes para ${folderName}...`);

        for (let i = 0; i < jsonData.length; i++) {
            const imageUrl = jsonData[i].image;
            const imageName = `image_${i + 1}.jpg`;  // Nombre de la imagen
            const imagePath = path.join(folderPath, imageName);

            try {
                await downloadImage(imageUrl, imagePath);
                console.log(`Imagen ${i + 1} guardada en ${folderName}.`);
            } catch (error) {
                console.error(`Error al descargar la imagen ${imageUrl}: ${error.message}`);
            }
        }
    }

    console.log('Descarga de imágenes completada.');
}

processJsonFiles().catch(console.error);
