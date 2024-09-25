import streamlit as st
import os
from app import getfolders, crop_images_in_folder,resize_images_in_folder, remove_background,fillbgimages_in_folder
import pandas as pd


def main():
    st.title("Procesamiento de Imágenes")
    base_folder = st.text_input("Ruta del dataset", "E:\OneDrive - Universidad Cooperativa de Colombia\entrega dataset")
    especies=getfolders(base_folder)
    data =[]
    for  especie in especies:
        data.append({ "name": especie, "procesar": False})
    df = pd.DataFrame(data)
    edited_especies = st.data_editor(df,width =500,column_config={"name": st.column_config.TextColumn(label="🐦")},disabled=["name"])
    favorite_command = edited_especies.loc[edited_especies['procesar']==True]["name"]
    
    folders = []
    for row in favorite_command.values:
        folders.append(row+"")

    percent_complete=0
    step=1/len(folders) if len(folders)>0 else 0.1

    progress_text = "procesando, por favor espere ..."
    my_bar = st.progress(0, text=progress_text)
    col1, col2 ,col3 = st.columns(3)
    with col1:
        on = st.toggle("")
    if on:
        with col2:
            if st.button("Redimensionar Imágenes"):
                for folder in folders:
                    resize_images_in_folder(f"{base_folder}\{folder}")
                    my_bar.progress(percent_complete + step, text=progress_text)
                my_bar.empty()
                st.success("Imágenes recortadas y redimensionadas con éxito!")
    else:
        with col2:
            if st.button("Recortar Imágenes"):
                for folder in folders:
                    crop_images_in_folder(f"{base_folder}\{folder}")
                    my_bar.progress(percent_complete + step, text=progress_text)
                my_bar.empty()
                st.success("Imágenes recortadas con éxito!")
    with col3:
        if st.button("Remover Fondo"):
            for folder in folders:
                no_bg_folder = os.path.join(f"{base_folder}\{folder}", "no_background")
                remove_background(f"{base_folder}\{folder}\\cropped_images_square", no_bg_folder)
                my_bar.progress(percent_complete + step, text=progress_text)
            my_bar.empty()
            st.success("Fondo removido de las imágenes con éxito!")
    if st.button("Rellenar Fondo"):
            for folder in folders:
                fillbgimages_in_folder(f"{base_folder}\{folder}")
                my_bar.progress(percent_complete + step, text=progress_text)
            my_bar.empty()
            st.success("Fondo removido de las imágenes con éxito!")

if __name__ == "__main__":
    main()