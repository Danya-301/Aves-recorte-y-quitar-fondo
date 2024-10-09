import torch
from pathlib import Path
from PIL import Image
import numpy as np

# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Ruta a la carpeta de imágenes
image_folder = Path("C:/Users/dmedina/Documents/Daniel/Ucc/10mo/Electiva 3/Prueba/Accipiter sp/cropped_images_square/")
output_folder = Path("processed_images/")
output_folder.mkdir(exist_ok=True)

# Dimensiones de redimensionado final
FINAL_WIDTH = 224
FINAL_HEIGHT = 224

def process_image(image_path):
    # Cargar la imagen
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    # Realizar detección de objetos
    results = model(img)
    detections = results.xyxy[0]  # Obtener detecciones en formato (x1, y1, x2, y2, conf, class)
    
    # Filtrar solo detecciones de aves (basado en la clase 'bird' en el modelo YOLO)
    bird_detections = [d for d in detections if d[5] == 14]  # Clase 14 corresponde a 'bird'
    
    if len(bird_detections) == 0:
        print(f"No se detectaron aves en la imagen: {image_path.name}")
        return
    
    # Seleccionar la detección con mayor confianza
    best_detection = max(bird_detections, key=lambda x: x[4])
    x1, y1, x2, y2, conf, cls = best_detection.tolist()
    
    # Asegurar que los límites están dentro de la imagen
    x1, y1, x2, y2 = max(0, x1), max(0, y1), min(img_width, x2), min(img_height, y2)
    
    # Recortar la imagen alrededor del ave detectada
    bird_img = img.crop((x1, y1, x2, y2))
    
    # Redimensionar la imagen recortada al tamaño final deseado
    bird_img_resized = bird_img.resize((FINAL_WIDTH, FINAL_HEIGHT), Image.ANTIALIAS)
    
    # Guardar la imagen procesada
    output_image_path = output_folder / image_path.name
    bird_img_resized.save(output_image_path)
    print(f"Imagen procesada guardada en: {output_image_path}")

# Procesar todas las imágenes en la carpeta
for image_path in image_folder.glob("*.*"):
    process_image(image_path)
