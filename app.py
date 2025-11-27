import streamlit as st

from sections import inicio, asignacion1, asignacion2, asignacion3

st.set_page_config(page_title="Proyecto final", page_icon="🏴‍☠️", layout="wide")

st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Ir a:", ["Inicio", "Asignación 1", "Asignación 2", "Asignación 3"])

if opcion == "Inicio":
    inicio()
elif opcion == "Asignación 1":
    asignacion1()
elif opcion == "Asignación 2":
    asignacion2()
elif opcion == "Asignación 3":
    asignacion3()