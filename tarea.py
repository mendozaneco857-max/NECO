import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# Detectar modo
MODO_STREAMLIT = "streamlit" in sys.argv[0]

if MODO_STREAMLIT:
    import streamlit as st


# =========================================
# 4–8 LECTURA CSV (CORREGIDO)
# =========================================
def leer_csv(datos_prueba_2):

    df = pd.read_csv(datos_prueba_2)

    print("\n✔ Archivo CSV leído correctamente")
    print(f"Total de registros: {len(df)}")

    print("\n=== BASE DE DATOS ===")
    print(df)

    print("\n=== VISTA PARCIAL ===")
    print(df.head())
    print("...")
    print(df.tail())

    # En Streamlit también mostrar
    if MODO_STREAMLIT:
        st.success("✔ Archivo cargado correctamente")
        st.info(f"Total de registros: {len(df)}")
        st.subheader("📊 Base de datos")
        st.dataframe(df)

    return df


# =========================================
# CUALITATIVA
# =========================================
def cualitativa(df, col):
    conteo = df[col].value_counts()

    tabla = pd.DataFrame({
        "fi": conteo,
        "hi": conteo / len(df)
    })

    tabla["hip"] = tabla["hi"] * 100
    tabla["Fi"] = tabla["fi"].cumsum()
    tabla["Hi"] = tabla["hi"].cumsum()

    if MODO_STREAMLIT:
        st.subheader(f"Cualitativa: {col}")
        st.dataframe(tabla)
    else:
        print("\n=== TABLA CUALITATIVA ===")
        print(tabla)

    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    for i, v in enumerate(conteo.values):
        ax.text(i, v, str(v), ha='center')

    if MODO_STREAMLIT:
        st.pyplot(fig)
    else:
        plt.show()

    fig2, ax2 = plt.subplots()
    conteo.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")

    if MODO_STREAMLIT:
        st.pyplot(fig2)
    else:
        plt.show()


# =========================================
# DISCRETA
# =========================================
def discreta(df, col):
    datos = df[col]
    freq = datos.value_counts().sort_index()

    tabla = pd.DataFrame({"fi": freq})
    tabla["hi"] = tabla["fi"] / len(df)

    if MODO_STREAMLIT:
        st.subheader(f"Discreta: {col}")
        st.dataframe(tabla)
    else:
        print("\n=== TABLA DISCRETA ===")
        print(tabla)

    print("\n=== MEDIDAS ===")
    print("Media:", np.mean(datos))
    print("Mediana:", np.median(datos))
    print("Moda:", datos.mode()[0])
    print("Varianza:", np.var(datos))
    print("Desv:", np.std(datos))
    print("Max:", np.max(datos))
    print("Min:", np.min(datos))
    print("Rango:", np.ptp(datos))

    if MODO_STREAMLIT:
        st.write({
            "Media": np.mean(datos),
            "Mediana": np.median(datos),
            "Moda": datos.mode()[0],
            "Varianza": np.var(datos),
            "Desv": np.std(datos),
            "Max": np.max(datos),
            "Min": np.min(datos),
            "Rango": np.ptp(datos)
        })

    fig, ax = plt.subplots()
    ax.stem(freq.index, freq.values)

    if MODO_STREAMLIT:
        st.pyplot(fig)
    else:
        plt.show()


# =========================================
# CONTINUA
# =========================================
def continua(df, col):
    datos = df[col]

    n = len(datos)
    k = int(1 + 3.322 * np.log10(n))

    intervalos = pd.cut(datos, bins=k)
    freq = intervalos.value_counts().sort_index()

    tabla = pd.DataFrame({"fi": freq})
    tabla["hi"] = tabla["fi"] / n
    tabla["hip"] = tabla["hi"] * 100
    tabla["Fi"] = tabla["fi"].cumsum()
    tabla["Hi"] = tabla["hi"].cumsum()

    if MODO_STREAMLIT:
        st.subheader(f"Continua: {col}")
        st.dataframe(tabla)
    else:
        print("\n=== TABLA CONTINUA ===")
        print(tabla)

    fig1, ax1 = plt.subplots()
    ax1.hist(datos, bins=k)

    if MODO_STREAMLIT:
        st.pyplot(fig1)
    else:
        plt.show()

    marcas = [i.mid for i in tabla.index]

    fig2, ax2 = plt.subplots()
    ax2.plot(marcas, tabla["fi"], marker="o")

    if MODO_STREAMLIT:
        st.pyplot(fig2)
    else:
        plt.show()

    limites = [i.right for i in tabla.index]

    fig3, ax3 = plt.subplots()
    ax3.plot(limites, tabla["Fi"], marker="o")

    if MODO_STREAMLIT:
        st.pyplot(fig3)
    else:
        plt.show()


# =========================================
# TERMINAL
# =========================================
def modo_terminal():
    df = leer_csv("datos_prueba_2.csv")

    cualitativa(df, "Carrera")
    discreta(df, "Materias_Aprobadas")
    continua(df, "Edad")

    print("\n✅ PROGRAMA FINALIZADO")


# =========================================
# STREAMLIT
# =========================================
def modo_streamlit():
    st.set_page_config(page_title="Sistema Estadístico")
    st.title("📊 Sistema Estadístico")

    archivo = st.file_uploader("Sube tu CSV", type=["csv"])

    if archivo:
        df = leer_csv(archivo)

        col1 = st.selectbox("Cualitativa", df.columns)
        col2 = st.selectbox("Discreta", df.columns)
        col3 = st.selectbox("Continua", df.columns)

        if st.button("Procesar"):
            cualitativa(df, col1)
            discreta(df, col2)
            continua(df, col3)

            st.success("Proceso completado")


# =========================================
# MAIN
# =========================================
if __name__ == "__main__":
    if MODO_STREAMLIT:
        modo_streamlit()
    else:
        modo_terminal()