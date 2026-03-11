import streamlit as st
import pandas as pd
import mysql.connector
import time
import math
import plotly.express as px
# --- CONFIGURACIÓN ---
st.set_page_config(page_title="IoT Multi-Series Dashboard", layout="wide")

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="fabricio",
        password="efenomas", 
        database="Series"
    )

def calcular_valor_real(nombre_tabla, x):
    if nombre_tabla == "seno":
        return math.sin(x)
    elif nombre_tabla == "coseno":
        return math.cos(x)
    elif nombre_tabla == "arctan":
        return math.atan(x)
    return 0

def generar_resumen_usuarios():
    try:
        conn = conectar_db()
        # --- NUEVA CONSULTA RELACIONAL (JOIN + UNION) ---
        query = """
            SELECT u.nombre_usuario, COUNT(c.idu) as total_registros
            FROM (
                SELECT idu FROM seno
                UNION ALL
                SELECT idu FROM coseno
                UNION ALL
                SELECT idu FROM arctan
            ) AS c
            JOIN usuarios u ON c.idu = u.id
            GROUP BY u.id, u.nombre_usuario
        """
        df_usuarios = pd.read_sql(query, conn)
        conn.close()

        if not df_usuarios.empty:
            st.subheader("Participación Global por Operador")
            
            fig = px.pie(
                df_usuarios, 
                values='total_registros', 
                names='nombre_usuario', 
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Ver tabla de aportes por usuario"):
                st.dataframe(df_usuarios.sort_values('total_registros', ascending=False), use_container_width=True)
        else:
            st.info("No hay datos de cálculos registrados en el sistema todavía.")
            
    except Exception as e:
        st.error(f"Error al cargar el resumen de usuarios: {e}")

def generar_dashboard_serie(nombre_tabla, titulo):
    try:
        conn = conectar_db()
        query = f"SELECT id, x, res, error FROM {nombre_tabla} ORDER BY id ASC"
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            df['valor_real'] = df['x'].apply(lambda val_x: calcular_valor_real(nombre_tabla, val_x))
            df['objetivo_error'] = 0.0

            ultimo_res = df['res'].iloc[-1]
            ultimo_real = df['valor_real'].iloc[-1]
            
            m1, m2 = st.columns(2)
            m1.metric(f"Registros Totales ({titulo})", len(df))
            m2.metric("Último Resultado", f"{ultimo_res:.6f}", f"Diff: {ultimo_res - ultimo_real:.6f}", delta_color="inverse")

            col_izq, col_der = st.columns(2)
            df_recent = df.tail(30).copy()

            with col_izq:
                st.subheader("Aproximación vs Real")
                st.line_chart(df_recent.set_index('id')[['res', 'valor_real']])
                st.caption("Si las líneas se superponen, la aproximación es exacta.")
            
            with col_der:
                st.subheader("Gráfica del error")
                st.line_chart(df_recent.set_index('id')[['error', 'objetivo_error']])
                st.caption("Se observa la precisión ganada en cada iteración.")
            
            with st.expander("Historial completo"):
                st.dataframe(df.sort_values('id', ascending=False))
        else:
            st.warning(f"Esperando datos...")
            
    except Exception as e:
        st.error(f"Error: {e}")

# INTERFAZ
st.title("Dashboard Control IoT - Taylor")

# pestañas
tabs = st.tabs(["Resumen Global", "Seno", "Coseno", "Arctan"])

while True:
    with tabs[0]:
        generar_resumen_usuarios()
    with tabs[1]:
        generar_dashboard_serie("seno", "Seno")
    with tabs[2]:
        generar_dashboard_serie("coseno", "Coseno")
    with tabs[3]:
        generar_dashboard_serie("arctan", "Arctan")
    
    time.sleep(2)
    st.rerun()
