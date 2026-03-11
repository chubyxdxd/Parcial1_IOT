import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import math
from datetime import datetime

# -CONFIGURACIÓN-
config = {
    'host': 'localhost',
    'user': 'fabricio',     
    'password': 'efenomas',
    'database': 'Series'
}

def calcular_seno_taylor(x, n):
    aproximacion = 0
    for i in range(n):
        coeficiente = (-1)**i
        numerador = x**(2*i + 1)
        denominador = math.factorial(2*i + 1)
        aproximacion += coeficiente * (numerador / denominador)
    valor_real = math.sin(x)
    return aproximacion, abs(valor_real - aproximacion)

def calcular_coseno_taylor(x, n):
    aproximacion = 0
    for i in range(n):
        coeficiente = (-1)**i
        numerador = x**(2*i)
        denominador = math.factorial(2*i)
        aproximacion += coeficiente * (numerador / denominador)
    valor_real = math.cos(x)
    return aproximacion, abs(valor_real - aproximacion)

def calcular_arctan_taylor(x, n):
    aproximacion = 0
    for i in range(n):
        coeficiente = (-1)**i
        numerador = x**(2*i + 1)
        denominador = 2*i + 1
        aproximacion += coeficiente * (numerador / denominador)
    valor_real = math.atan(x)
    return aproximacion, abs(valor_real - aproximacion)

# -COLORES Y UI-
BG = "#EEF2FF"
CARD = "#FFFFFF"
TEXT = "#1F2937"

SERIE_A = "#4F46E5" 
SERIE_B = "#06B6D4" 
SERIE_C = "#10B981" 
CRUD = "#F59E0B"

NOMBRES_TABLAS = {'A': 'seno', 'B': 'coseno', 'C': 'arctan'}
NOMBRES_MOSTRAR = {'A': 'Seno', 'B': 'Coseno', 'C': 'Arctan'}

id_usuario_actual = ""

def limpiar():
    for widget in frame.winfo_children():
        widget.destroy()

# botones
def boton_moderno(texto, color, comando, fila):
    contenedor = tk.Frame(frame, bg=color)
    contenedor.grid(row=fila, column=0, sticky="ew", pady=8, padx=20)

    label = tk.Label(
        contenedor, text=texto, bg=color, fg="white",
        font=("Segoe UI", 14, "bold"), cursor="hand2", pady=12
    )
    label.pack(fill="both", expand=True)

    def hover_on(e):
        contenedor.config(bg="#333333")
        label.config(bg="#333333")

    def hover_off(e):
        contenedor.config(bg=color)
        label.config(bg=color)

    contenedor.bind("<Button-1>", lambda e: comando())
    label.bind("<Button-1>", lambda e: comando())
    contenedor.bind("<Enter>", hover_on)
    label.bind("<Enter>", hover_on)
    contenedor.bind("<Leave>", hover_off)
    label.bind("<Leave>", hover_off)

# 
def guardar_usuario():
    global id_usuario_actual
    entrada = entry.get().strip()
    if not entrada.isdigit():
        messagebox.showwarning("Error", "Para MySQL, el ID debe ser un número entero.")
        return
    id_usuario_actual = int(entrada)
    messagebox.showinfo("Identificación", f"Conectado exitosamente con el ID: {id_usuario_actual}")
    menu_series()

# Menu
def menu_series():
    limpiar()
    frame.grid_columnconfigure(0, weight=1)

    tk.Label(frame, text=f"Usuario ID: {id_usuario_actual} | Servidor: Localhost", font=("Segoe UI", 10), bg=CARD, fg="#10B981").grid(row=0, column=0, pady=(0, 10))
    tk.Label(frame, text="Selecciona una serie", font=("Segoe UI", 22, "bold"), bg=CARD, fg=TEXT).grid(row=1, column=0, pady=20)

    boton_moderno("Serie Seno", SERIE_A, lambda: crud('A'), 2)
    boton_moderno("Serie Coseno", SERIE_B, lambda: crud('B'), 3)
    boton_moderno("Serie Arctan", SERIE_C, lambda: crud('C'), 4)

# -CRUD-
def crud(opcion):
    tabla_db = NOMBRES_TABLAS[opcion]
    nombre_mostrar = NOMBRES_MOSTRAR[opcion]
    limpiar()
    frame.grid_columnconfigure(0, weight=1)

    tk.Label(frame, text=f"Gestión: {nombre_mostrar}", font=("Segoe UI", 22, "bold"), bg=CARD, fg=TEXT).grid(row=0, column=0, pady=20)

    boton_moderno("Calcular y Enviar datos", CRUD, lambda: pantalla_crear(tabla_db, nombre_mostrar, opcion), 1)
    boton_moderno("Leer (Ver registro por ID)", CRUD, lambda: accion_rapida("Leer", tabla_db), 2)
    # --- AQUI AGREGAMOS EL BOTON DE EDITAR ---
    boton_moderno("Editar/Actualizar (Por ID)", CRUD, lambda: accion_rapida("Actualizar", tabla_db), 3)
    boton_moderno("Eliminar (Por ID)", "#EF4444", lambda: accion_rapida("Eliminar", tabla_db), 4)

    tk.Button(frame, text="Volver", command=menu_series, bg="#9CA3AF", fg="white", relief="flat").grid(row=5, column=0, pady=15)

# Calcular 
def pantalla_crear(tabla_db, nombre_mostrar, opcion):
    limpiar()
    frame.grid_columnconfigure(0, weight=1)

    tk.Label(frame, text=f"Generar - {nombre_mostrar}", font=("Segoe UI", 22, "bold"), bg=CARD, fg=TEXT).grid(row=0, column=0, pady=20)

    tk.Label(frame, text="Valor de X (Radianes):", font=("Segoe UI", 12), bg=CARD).grid(row=1, column=0, pady=5)
    entry_x = tk.Entry(frame, font=("Segoe UI", 14))
    entry_x.grid(row=2, column=0, pady=5, ipadx=10, ipady=6)

    tk.Label(frame, text="Número de Iteraciones (n):", font=("Segoe UI", 12), bg=CARD).grid(row=3, column=0, pady=5)
    entry_it = tk.Entry(frame, font=("Segoe UI", 14))
    entry_it.grid(row=4, column=0, pady=10, ipadx=10, ipady=6)

    boton_moderno("Generar y Enviar", "#6366F1", lambda: ejecutar_calculos(tabla_db, entry_x.get(), entry_it.get(), opcion), 5)

    tk.Button(frame, text="Volver", command=lambda: crud(opcion), bg="#9CA3AF", fg="white", relief="flat").grid(row=6, column=0, pady=15)

# enviar
def ejecutar_calculos(tabla, x_val, it_val, opcion):
    try:
        x_valor = float(x_val)
        iteraciones = int(it_val)
    except ValueError:
        messagebox.showwarning("Error", "Ingrese valores numéricos válidos.")
        return

    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()
        
        for i in range(1, iteraciones + 1):
            if tabla == "seno":
                resultado, error = calcular_seno_taylor(x_valor, i)
            elif tabla == "coseno":
                resultado, error = calcular_coseno_taylor(x_valor, i)
            else:
                resultado, error = calcular_arctan_taylor(x_valor, i)
            
            ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = f"INSERT INTO {tabla} (idu, nregistro, x, res, error, timed) VALUES (%s, %s, %s, %s, %s, %s)"
            datos = (id_usuario_actual, i, x_valor, resultado, error, ahora)
            cursor.execute(sql, datos)
            
        conexion.commit()
        cursor.close()
        conexion.close()
        
        messagebox.showinfo("Éxito", f"¡Se han calculado y enviado {iteraciones} registros a la tabla {tabla}!")
        crud(opcion)

    except mysql.connector.Error as err:
        messagebox.showerror("Error de BD", f"Error MySQL: {err}")

# Eliminacion, lectura y actualización
def accion_rapida(accion, tabla):
    id_registro = simpledialog.askinteger(accion, f"Ingrese el ID del registro en la tabla {tabla}:")
    if not id_registro: return

    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor(dictionary=True)

        # Buscar si el registro existe primero
        cursor.execute(f"SELECT * FROM {tabla} WHERE id = %s", (id_registro,))
        reg = cursor.fetchone()

        if not reg:
            messagebox.showwarning("No encontrado", "No existe ese ID en la base de datos.")
            cursor.close()
            conexion.close()
            return

        if accion == "Leer":
            info = f"Tabla: {tabla.upper()} | ID: {reg['id']}\n\nUsuario: {reg['idu']}\nTérminos (n): {reg['nregistro']}\nValor X: {reg['x']}\nResultado: {reg['res']:.6f}\nError: {reg['error']:.2e}\nFecha: {reg['timed']}"
            messagebox.showinfo("Registro Encontrado", info)

        elif accion == "Actualizar":
            nuevo_res = simpledialog.askfloat("Actualizar", f"Valor actual: {reg['res']:.6f}\nIngrese el nuevo valor del resultado:")
            if nuevo_res is not None:
                ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Hacemos el UPDATE del resultado y la fecha
                sql = f"UPDATE {tabla} SET res = %s, timed = %s WHERE id = %s"
                cursor.execute(sql, (nuevo_res, ahora, id_registro))
                conexion.commit()
                messagebox.showinfo("Éxito", "El registro fue actualizado correctamente.")

        elif accion == "Eliminar":
            cursor.execute(f"DELETE FROM {tabla} WHERE id = %s", (id_registro,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")

        cursor.close()
        conexion.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# inicializar
root = tk.Tk()
root.title("Cliente IoT - Series Taylor")
root.geometry("600x650")
root.configure(bg=BG)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = tk.Frame(root, bg=CARD, padx=40, pady=40)
frame.grid(row=0, column=0, sticky="nsew")

tk.Label(frame, text="Acceso al Dispositivo IoT", font=("Segoe UI", 22, "bold"), bg=CARD, fg=TEXT).grid(row=0, column=0, pady=20)
tk.Label(frame, text="Ingresa tu ID Numérico de Operador", font=("Segoe UI", 12), bg=CARD, fg="#6B7280").grid(row=1, column=0, pady=(0, 5))

entry = tk.Entry(frame, font=("Segoe UI", 14))
entry.grid(row=2, column=0, pady=15, ipadx=20, ipady=6)

boton_moderno("Conectar al Servidor", "#6366F1", guardar_usuario, 3)
root.mainloop()
