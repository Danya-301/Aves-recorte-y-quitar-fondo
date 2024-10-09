import streamlit as st
import os
from app import getfolders, crop_images_in_folder, resize_images_in_folder, remove_background, fillbgimages_in_folder
import pandas as pd

def main():
    st.title("Procesamiento de Imágenes")

    base_folder = r"C:\Users\dmedina\Documents\Daniel\Ucc\10mo\Electiva 3\DataSet"
    folders = getfolders(base_folder)

    st.info(f"Seleccione las carpetas que desea procesar. Total de carpetas disponibles: {len(folders)}")

    # Crear un DataFrame con las carpetas y checkboxes
    df = pd.DataFrame({
        'Carpeta': folders,
        'Procesar': [False] * len(folders)
    })

    # Mostrar la tabla editable
    edited_df = st.data_editor(df, hide_index=True, num_rows="dynamic")

    if st.button("Iniciar Procesamiento"):
        selected_folders = edited_df[edited_df['Procesar']]['Carpeta'].tolist()
        
        if not selected_folders:
            st.warning("Por favor, seleccione al menos una carpeta para procesar.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, folder in enumerate(selected_folders):
                folder_path = os.path.join(base_folder, folder)
                status_text.text(f"Procesando: {folder}")

                # Paso 1: Redimensionar
                resized_folder = resize_images_in_folder(folder_path)
                progress_bar.progress((i + 0.33) / len(selected_folders))

                # Paso 2: Remover fondo
                no_bg_folder = remove_background(resized_folder)
                progress_bar.progress((i + 0.66) / len(selected_folders))

                # Paso 3: Rellenar fondo
                fillbgimages_in_folder(no_bg_folder)
                progress_bar.progress((i + 1) / len(selected_folders))

            progress_bar.progress(1.0)
            status_text.text("Procesamiento completo finalizado con éxito!")
            st.success(f"Se han procesado {len(selected_folders)} carpetas.")

if __name__ == "__main__":
    main()