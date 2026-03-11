#  Sistema IoT: Análisis de Convergencia de Series de Taylor

Este proyecto es una simulación de un entorno IoT (Internet de las Cosas) utilizando una arquitectura Cliente-Servidor desacoplada. El sistema permite el cálculo, envío, almacenamiento relacional y visualización en tiempo real de aproximaciones matemáticas utilizando las Series de Taylor para funciones trigonométricas (Seno, Coseno y Arcotangente).

##  Arquitectura del Sistema

El proyecto está dividido en tres capas principales: una interfaz de cliente (Edge/Nodo), una base de datos relacional centralizada, y un panel de visualización de datos (Dashboard).

### 1. Cliente IoT (Nodo de Procesamiento)
**Archivo:** `cliente.py`
**Tecnologías:** Python, Tkinter, `mysql-connector-python`, `math`

Actúa como el dispositivo en campo (sensor/operador). Su función principal es recolectar parámetros del usuario, realizar el cómputo matemático pesado y enviar los resultados a la base de datos.
* **Autenticación Relacional:** Sistema de login que verifica o registra nuevos operadores en la base de datos central.
* **Procesamiento Matemático:** Calcula la aproximación de Taylor y el error absoluto respecto al valor real de la librería `math`.
* **Validación Estricta:** Implementa filtros matemáticos (ej. restringe el cálculo de Arctan al rango [-1, 1] para evitar divergencias).
* **Gestión de Datos (CRUD):** Permite crear, leer, actualizar (recalculando el error dinámicamente) y eliminar registros por lotes desde la interfaz gráfica.

### 2. Servidor de Monitoreo (Dashboard Analítico)
**Archivo:** `servidor.py`
**Tecnologías:** Python, Streamlit, Pandas, Plotly

Actúa como el centro de control principal. Consume los datos de la base de datos MySQL en tiempo real y genera analíticas visuales sin intervenir en el cálculo primario.
* **Despliegue Local:** Se inicializa desde la terminal con el comando `streamlit run servidor.py` y la interfaz interactiva se visualiza en cualquier navegador web accediendo a `http://localhost:8501/`.
* **Monitoreo en Tiempo Real:** Utiliza un bucle de refresco asíncrono (`st.rerun()`) para actualizar las gráficas automáticamente cuando el cliente inyecta nuevos datos.
* **Análisis de Convergencia:** Gráficas comparativas entre la aproximación de Taylor y el valor matemático real (Ground Truth).
* **Seguimiento del Error:** Visualización de la caída del error absoluto a medida que aumentan las iteraciones ($n$).
* **Analítica Global:** Gráficos interactivos de Plotly generados a partir de consultas SQL avanzadas (`JOIN` y `UNION ALL`) para auditar la participación de cada nodo/usuario en el sistema.

### 3. Base de Datos Relacional
**Tecnología:** MySQL (Stack LAMP)
* Base de datos montada sobre un entorno Linux nativo (Stack LAMP), prescindiendo de emuladores para un rendimiento más apegado a la industria.
* Modelo relacional con una tabla central de `usuarios` conectada a tablas transaccionales (`seno`, `coseno`, `arctan`).
* Implementa **Integridad Referencial** mediante Llaves Foráneas (Foreign Keys) y reglas de mantenimiento automático (`ON DELETE CASCADE`).

---
*Desarrollado como proyecto de integración de Ingeniería Mecatrónica y Ciencias de la Computación.*
