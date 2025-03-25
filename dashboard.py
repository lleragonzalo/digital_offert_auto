import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("📊 Evaluación de Ofertas")

API_URL = "http://127.0.0.1:8000/evaluaciones/"

response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # ✅ Asegurar que las columnas "metodo" y "usuario" existen
    if "metodo" not in df.columns:
        df["metodo"] = "Desconocido"
    if "usuario" not in df.columns:
        df["usuario"] = "No modificado"

    # 📌 Renombrar la columna "usuario" a "Usuario Evaluador"
    df = df.rename(columns={"usuario": "Usuario Evaluador"})

    # 📋 Mostrar tabla con la columna renombrada
    st.subheader("📋 Datos de las Ofertas Evaluadas")
    st.dataframe(df[["id_oferta", "proveedor", "puntaje_total", "estado", "metodo", "Usuario Evaluador"]])

    # 📊 Gráfico de puntajes por proveedor
    st.subheader("📊 Distribución de Puntajes de las Ofertas")
    fig, ax = plt.subplots()
    ax.bar(df["proveedor"], df["puntaje_total"], color='skyblue')
    ax.set_xlabel("Proveedor")
    ax.set_ylabel("Puntaje")
    ax.set_title("Puntajes por Proveedor")
    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.error("⚠️ No se pudieron obtener los datos de la API")
