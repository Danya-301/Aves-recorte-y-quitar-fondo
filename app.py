import os
from PIL import Image
from rembg import remove
import cv2

CONST_OUTPUT_WIDTH = 224

def getfolders(folder_path):
    # Verifica si el folder_path es válido
    if not os.path.exists(folder_path):
        return []  # Retorna una lista vacía si la ruta no existe
    
    # Lista únicamente los directorios en la carpeta especificada
    return [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]


def crop_images_in_folder(folder_path, output_size=(224, 224)):
    """
    Itera a través de las imágenes en una carpeta y las recorta al tamaño especificado.
    Guarda las imágenes recortadas en un subdirectorio llamado 'result'.
    
    Args:
    folder_path (str): Ruta a la carpeta que contiene las imágenes
    output_size (tuple): Tamaño de salida deseado (ancho, alto)
    """
    output_folder = os.path.join(folder_path, "result")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            with Image.open(file_path) as img:
                width, height = img.size
                left = (width - output_size[0]) // 2
                top = (height - output_size[1]) // 2
                right = left + output_size[0]
                bottom = top + output_size[1]

                cropped_img = img.crop((left, top, right, bottom))
                
                output_filename = f"cropped_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                cropped_img.save(output_path)

    print(f"Todas las imagenes han sido cortadas. Estan guardadas en: {output_folder}")

def resize_images_in_folder(folder_path, output_size=(224, 224)):
    # Crear carpetas de salida
    output_folder = os.path.join(folder_path, "cropped_images_square")
    os.makedirs(output_folder, exist_ok=True)

    # Parte 1: Recortar las imágenes para hacerlas cuadradas
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Definir el área de recorte para hacer la imagen cuadrada
                if width > height:
                    new_width = height
                    left = (width - new_width) // 2
                    upper = 0
                    right = left + new_width
                    lower = height
                else:
                    new_height = width
                    left = 0
                    upper = (height - new_height) // 2
                    right = width
                    lower = upper + new_height

                # Recortar la imagen
                cropped_img = img.crop((left, upper, right, lower))
                resize_img = cropped_img.resize(output_size)
                
                # Guardar la imagen recortada
                output_filename = f"resize_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                resize_img.save(output_path)
    

    print(f"Todas las imágenes han sido recortadas y redimensionadas. Las imágenes recortadas están en: {output_folder}, y las redimensionadas en: ")

def remove_background(input_folder, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"nobg_{os.path.splitext(filename)[0]}.png")

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path, format='PNG')

    print(f"Fondo removido. Imagenes procesadas estan guardadas en: {output_folder}")


def fillbgimages_in_folder(folder_path):
    input_folder = folder_path
    output_folder = os.path.join(folder_path, "fillbg_images")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(input_folder, filename)
            with Image.open(file_path) as img:
                # Create a new image with a green background
               # Create a new image with a sky blue background
                sky_blue_background = Image.new("RGBA", (CONST_OUTPUT_WIDTH, CONST_OUTPUT_WIDTH), (186, 202, 227, 255))
                
                # Paste the original image on top of the sky blue background
                sky_blue_background.paste(img, (0, 0), img)
                
                # Convert to RGB mode to remove alpha channel (transparency)
                green_image = sky_blue_background.convert("RGB")
                # Save the result
                output_filename = f"fillbg{filename}"
                output_path = os.path.join(output_folder, output_filename)
                green_image.save(output_path)

    print(f"Todas las imagenes han sido rellenadas. Estan guardadas en: {output_folder}")

