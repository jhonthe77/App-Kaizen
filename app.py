import streamlit as st
import pandas as pd
from datetime import date
import os
import plotly.express as px
import json
import random
from datetime import datetime, timedelta

import pytz
BOGOTA = pytz.timezone("America/Bogota")

# Lista de frases motivacionales
frases_motivacionales = [
    "💡 Cada paso pequeño te acerca a una gran meta.",
    "🔥 La constancia vence al talento cuando el talento no se esfuerza.",
    "🌱 Hoy es un buen día para mejorar un 1%.",
    "⏳ No se trata de hacerlo perfecto, sino de hacerlo cada día.",
    "🚶‍♂️ Sigue caminando, incluso si es lento, lo importante es avanzar.",
    "🏁 Lo difícil de empezar se convierte en fácil con disciplina.",
    "📈 El progreso silencioso es el que más impacta.",
    "🧠 Eres lo que repites cada día. Hazlo con intención.",
    "🧭 No te compares, solo asegúrate de ser mejor que ayer.",
    "🎯 La mejora continua no tiene fin, y ese es su poder."
]




# Configuración general de la app
st.set_page_config(page_title="Kaizen Personal", layout="centered" , initial_sidebar_state="expanded")

# Título principal
st.title("🌱 Kaizen Personal App")
st.caption("Mejora continua, paso a paso.")

# Sidebar para navegación
menu = st.sidebar.radio("📋 Navegación", [
    "🏠 Inicio",
    "✅ Registro Diario",
    "📈 Estadísticas",
    "🔁 Revisión Semanal",
    "⚙️ Objetivos",
])

# Sección: Inicio
if menu == "🏠 Inicio":
    st.header("Bienvenido a tu espacio Kaizen")

    # Mostrar una frase motivacional aleatoria
    frase_del_dia = random.choice(frases_motivacionales)
    st.success(f"🌟 Frase del día: *{frase_del_dia}*")



    st.markdown("""
    Esta aplicación te ayudará a aplicar el método **Kaizen** en tu vida diaria.  
    Aquí podrás registrar tus hábitos, visualizar tu progreso y reflexionar semanalmente.

    ---
    **¿Qué puedes hacer aquí?**
    - Registrar microacciones diarias
    - Ver tus avances con gráficas
    - Reflexionar cada semana para mejorar
    - Establecer objetivos personales por áreas

    Comienza eligiendo una opción en el menú lateral 👈
    """)

# Sección: Registro Diario
elif menu == "✅ Registro Diario":
    st.header("Registro Diario de Hábitos con Inicio y Fin ⏱️ (hora Bogotá)")

    # Cargar hábitos personalizados
    habitos_file = "habitos.json"
    if os.path.exists(habitos_file):
        with open(habitos_file, "r", encoding="utf-8") as f:
            habits = json.load(f)
    else:
        st.warning("No hay hábitos configurados aún. Ve a ⚙️ Objetivos para agregarlos.")
        st.stop()

    # Inicializar estado de sesión por hábito (si no existe)
    for habit in habits:
        if f"{habit}_start" not in st.session_state:
            st.session_state[f"{habit}_start"] = None

    # Mostrar hábitos con botones de inicio y fin
    for habit in habits:
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"### {habit}")

        with col2:
            if st.session_state[f"{habit}_start"] is None:
                if st.button("🟢 Iniciar", key=f"start_{habit}"):
                    # hora con zona de Bogota
                    st.session_state[f"{habit}_start"] = datetime.now(BOGOTA)
            else:
                inicio = st.session_state[f"{habit}_start"]
                st.markdown(f"🕒 Inicio: {inicio.strftime('%H:%M:%S')} (Bogotá)")

        with col3:
            if st.session_state[f"{habit}_start"] is not None:
                if st.button("🔴 Finalizar", key=f"end_{habit}"):
                    hora_inicio = st.session_state[f"{habit}_start"]            # tz-aware (Bogotá)
                    hora_fin = datetime.now(BOGOTA)                            # tz-aware (Bogotá)
                    duracion = round((hora_fin - hora_inicio).total_seconds() / 60, 2)

                    fila = {
                        "Fecha": hora_fin.date().isoformat(),                    # YYYY-MM-DD en zona Bogotá
                        "Hábito": habit,
                        "Hora Inicio": hora_inicio.strftime('%H:%M:%S'),
                        "Hora Fin": hora_fin.strftime('%H:%M:%S'),
                        "Duración (min)": duracion
                    }

                    archivo = "registro_detallado.csv"
                    if os.path.exists(archivo):
                        df = pd.read_csv(archivo)
                    else:
                        df = pd.DataFrame()

                    df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
                    df.to_csv(archivo, index=False)

                    st.success(f"✅ '{habit}' registrado: {duracion} min")
                    st.session_state[f"{habit}_start"] = None


# Sección: Revisión Semanal
elif menu == "🔁 Revisión Semanal":
    st.header("Revisión Kaizen Semanal")
    st.header("🔁 Revisión Kaizen Semanal")
    st.markdown("Reflexiona sobre tu semana y ajusta tu enfoque para la siguiente.")

    semana = date.today().isocalendar().week
    año = date.today().year
    fecha_actual = date.today().isoformat()

    with st.form("revision_kaizen_form"):
        st.subheader(f"📅 Semana {semana} - {año}")
        
        r1 = st.text_area("✅ ¿Qué lograste esta semana de lo que te sientes orgulloso?", "")
        r2 = st.text_area("⚠️ ¿Qué obstáculos encontraste o qué no funcionó bien?", "")
        r3 = st.text_area("🔧 ¿Qué vas a ajustar o intentar mejorar la próxima semana?", "")
        r4 = st.text_area("💡 ¿Qué aprendiste sobre ti esta semana?", "")
        
        submitted = st.form_submit_button("Guardar Revisión")

        if submitted:
            # Cargar datos anteriores si existen
            if os.path.exists("revision_semanal.csv"):
                revisiones_df = pd.read_csv("revision_semanal.csv")
            else:
                revisiones_df = pd.DataFrame()

            nueva_revision = {
                "Fecha": fecha_actual,
                "Semana": semana,
                "Año": año,
                "Logros": r1,
                "Obstáculos": r2,
                "Ajustes": r3,
                "Aprendizaje": r4
            }

            revisiones_df = pd.concat([revisiones_df, pd.DataFrame([nueva_revision])], ignore_index=True)
            revisiones_df.to_csv("revision_semanal.csv", index=False)
            st.success("✅ Revisión guardada correctamente")

    # Mostrar historial de revisiones
    with st.expander("📚 Ver revisiones anteriores"):
        if os.path.exists("revision_semanal.csv"):
            historico_df = pd.read_csv("revision_semanal.csv")
            st.dataframe(historico_df.sort_values(by="Fecha", ascending=False), use_container_width=True)
        else:
            st.info("No hay revisiones guardadas aún.")

# Sección: Objetivos
elif menu == "⚙️ Objetivos":
    st.header("⚙️ Configuración de Objetivos Kaizen")

    # Cargar objetivos en session_state si no existen
    if "objetivos" not in st.session_state:
        if os.path.exists("habitos.json"):
            with open("habitos.json", "r") as f:
                st.session_state.objetivos = json.load(f)
        else:
            st.session_state.objetivos = []

    objetivos = st.session_state.objetivos

    st.subheader("📝 Editar o Eliminar Objetivos Existentes")
    nuevos_objetivos = []
    for i, objetivo in enumerate(objetivos):
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            nuevo_nombre = st.text_input(f"Hábito #{i+1}", value=objetivo, key=f"edit_{i}")
        with col2:
            eliminar = st.checkbox("🗑️", key=f"del_{i}", help="Eliminar este hábito")
        if not eliminar and nuevo_nombre.strip() != "":
            nuevos_objetivos.append(nuevo_nombre.strip())

    st.subheader("➕ Agregar nuevos objetivos")
    nuevo_obj = st.text_input("Escribe un nuevo hábito", key="nuevo_obj")
    if st.button("Agregar hábito"):
        if nuevo_obj.strip():
            nuevos_objetivos.append(nuevo_obj.strip())
            st.session_state.objetivos = nuevos_objetivos
            with open("habitos.json", "w") as f:
                json.dump(st.session_state.objetivos, f, indent=4)
            st.success(f"✅ Hábito agregado: {nuevo_obj.strip()}")

    if st.button("💾 Guardar cambios"):
        # Guardar en JSON
        st.session_state.objetivos = nuevos_objetivos
        with open("habitos.json", "w") as f:
            json.dump(st.session_state.objetivos, f, indent=4)

        # Detectar cambios de nombre de hábitos
        cambios = {old: new for old, new in zip(objetivos, nuevos_objetivos) if old != new}
        if cambios and os.path.exists("registro_detallado.csv"):
            df_detalle = pd.read_csv("registro_detallado.csv")
            for antiguo, nuevo in cambios.items():
                df_detalle["Hábito"] = df_detalle["Hábito"].replace(antiguo, nuevo)
            df_detalle.to_csv("registro_detallado.csv", index=False)

        st.success("✅ Objetivos actualizados con éxito")
   


# Sección: Estadísticas
elif menu == "📈 Estadísticas":
    st.header("📊 Estadísticas Semanales de Tiempo por Hábito")

    archivo = "registro_detallado.csv"
    if not os.path.exists(archivo):
        st.warning("Aún no hay registros. Ve a ✅ Registro Diario para comenzar.")
        st.stop()

    df = pd.read_csv(archivo)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    hoy = pd.to_datetime("today").normalize()
    hace_7_dias = hoy - pd.Timedelta(days=6)

    # Filtrar últimos 7 días
    df_semana = df[df["Fecha"].between(hace_7_dias, hoy)]

    if df_semana.empty:
        st.info("No hay datos de los últimos 7 días.")
    else:
        df_semana["Día"] = df_semana["Fecha"].dt.strftime("%a")
        dias_orden = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        df_semana["Día"] = pd.Categorical(df_semana["Día"], categories=dias_orden, ordered=True)

        # Crear tabs
        tab1, tab2 = st.tabs(["⏱️ Tiempo por hábito", "🔢 Actividades por día"])

        with tab1:
            resumen_duracion = df_semana.groupby(["Día", "Hábito"], observed=True)["Duración (min)"].sum().reset_index()
            resumen_duracion = resumen_duracion.sort_values("Día")

            fig_duracion = px.bar(
                resumen_duracion,
                x="Día",
                y="Duración (min)",
                color="Hábito",
                text="Duración (min)",
                barmode="group",
                title="Duración total por hábito (últimos 7 días)",
                labels={"Día": "Día", "Duración (min)": "Minutos"},
                height=420,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_duracion.update_layout(
                margin=dict(t=50, b=30, l=30, r=30),
                legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
                plot_bgcolor="rgba(0,0,0,0)"
            )
            fig_duracion.update_traces(textposition="outside")
            max_val = df["Duración (min)"].max()
            fig_duracion.update_yaxes(range=[0, max_val * 2.9])
            st.plotly_chart(fig_duracion, use_container_width=True)

        with tab2:
            resumen_actividades = df_semana.groupby(["Día", "Hábito"]).size().reset_index(name="Actividades")
            resumen_actividades = resumen_actividades.sort_values("Día")

            fig_actividades = px.bar(
                resumen_actividades,
                x="Día",
                y="Actividades",
                text="Actividades",
                color="Hábito",
                barmode="group",
                title="Número de actividades registradas (últimos 7 días)",
                labels={"Día": "Día", "Actividades": "Cantidad"},
                height=420,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_actividades.update_layout(
                margin=dict(t=70, b=30, l=30, r=30),
                legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
                plot_bgcolor="rgba(0,0,0,0)"
            )
            fig_actividades.update_traces(textposition="outside")
            max_val = df["Hábito"].count()
            fig_actividades.update_yaxes(range=[0, max_val * 1.5])
            st.plotly_chart(fig_actividades, use_container_width=True)
