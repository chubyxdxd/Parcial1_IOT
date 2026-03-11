import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import math
from datetime import datetime 

config = {
    'host': '172.27.182.135',
    'user': 'fabricio',
    'password': 'efenomas',
    'database': 'Series'
}


import platform

#  CÁLCULOS TAYLOR
def calcular_seno_taylor(x, n):
    aprox = sum((-1)**i * x**(2*i+1) / math.factorial(2*i+1) for i in range(n))
    return aprox, abs(math.sin(x) - aprox)

def calcular_coseno_taylor(x, n):
    aprox = sum((-1)**i * x**(2*i) / math.factorial(2*i) for i in range(n))
    return aprox, abs(math.cos(x) - aprox)

def calcular_arctan_taylor(x, n):
    aprox = sum((-1)**i * x**(2*i+1) / (2*i+1) for i in range(n))
    return aprox, abs(math.atan(x) - aprox)

#  PALETA & CONSTANTES
BG_DARK   = "#0D0F1A"
BG_CARD   = "#161929"
BG_INPUT  = "#1E2235"
BORDER    = "#2A2F4A"
TEXT_PRI  = "#E8EAFF"
TEXT_SEC  = "#7B82A8"
TEXT_HINT = "#454D70"

ACCENT_A  = "#6C63FF"   # Seno
ACCENT_B  = "#00C2CB"   # Coseno
ACCENT_C  = "#00E899"   # Arctan
ACCENT_W  = "#FF6B6B"   # Error / Eliminar
ACCENT_OK = "#6C63FF"   # Genérico

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_SUB    = ("Courier New", 11)
FONT_BTN    = ("Courier New", 12, "bold")
FONT_LABEL  = ("Courier New", 10)
FONT_INPUT  = ("Courier New", 13)
FONT_SMALL  = ("Courier New", 9)

NOMBRES_TABLAS  = {'A': 'seno', 'B': 'coseno', 'C': 'arctan'}
NOMBRES_MOSTRAR = {'A': 'Seno', 'B': 'Coseno', 'C': 'Arctan'}
ACCENTS_SERIE   = {'A': ACCENT_A, 'B': ACCENT_B, 'C': ACCENT_C}

id_usuario_actual = ""


def popup_error(titulo, mensaje):
    _popup(titulo, mensaje, ACCENT_W, "✖  " + titulo)

def popup_ok(titulo, mensaje):
    _popup(titulo, mensaje, ACCENT_C, "✔  " + titulo)

def popup_info(titulo, mensaje):
    _popup(titulo, mensaje, ACCENT_A, "◉  " + titulo)

def _popup(titulo, mensaje, color, header):
    win = tk.Toplevel(root)
    win.title(titulo)
    win.configure(bg=BG_CARD)
    win.resizable(False, False)
    win.grab_set()

    # Centrar sobre root
    root.update_idletasks()
    x = root.winfo_x() + root.winfo_width()//2 - 220
    y = root.winfo_y() + root.winfo_height()//2 - 100
    win.geometry(f"440x200+{x}+{y}")

    # Barra superior de color
    bar = tk.Frame(win, bg=color, height=4)
    bar.pack(fill="x")

    # Cabecera
    tk.Label(win, text=header, font=("Courier New", 13, "bold"),
             bg=BG_CARD, fg=color).pack(anchor="w", padx=24, pady=(16,4))

    # Separador
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=24)

    # Mensaje
    tk.Label(win, text=mensaje, font=FONT_LABEL, bg=BG_CARD,
             fg=TEXT_PRI, wraplength=390, justify="left").pack(
             anchor="w", padx=24, pady=12)

    # Botón OK
    btn = tk.Frame(win, bg=color, cursor="hand2")
    btn.pack(pady=(0,18))
    lbl = tk.Label(btn, text="  OK  ", font=FONT_BTN, bg=color, fg="white", padx=20, pady=6)
    lbl.pack()

    def cerrar(e=None):
        win.destroy()

    btn.bind("<Button-1>", cerrar)
    lbl.bind("<Button-1>", cerrar)

    def hover_on(e):
        btn.config(bg="#FFFFFF"); lbl.config(bg="#FFFFFF", fg=color)
    def hover_off(e):
        btn.config(bg=color); lbl.config(bg=color, fg="white")

    btn.bind("<Enter>", hover_on); lbl.bind("<Enter>", hover_on)
    btn.bind("<Leave>", hover_off); lbl.bind("<Leave>", hover_off)

    win.wait_window()

def popup_yesno(titulo, mensaje, color=ACCENT_A):
    result = [False]
    win = tk.Toplevel(root)
    win.title(titulo)
    win.configure(bg=BG_CARD)
    win.resizable(False, False)
    win.grab_set()

    root.update_idletasks()
    x = root.winfo_x() + root.winfo_width()//2 - 230
    y = root.winfo_y() + root.winfo_height()//2 - 110
    win.geometry(f"460x210+{x}+{y}")

    tk.Frame(win, bg=color, height=4).pack(fill="x")
    tk.Label(win, text="?  " + titulo, font=("Courier New", 13, "bold"),
             bg=BG_CARD, fg=color).pack(anchor="w", padx=24, pady=(16,4))
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=24)
    tk.Label(win, text=mensaje, font=FONT_LABEL, bg=BG_CARD,
             fg=TEXT_PRI, wraplength=400, justify="left").pack(
             anchor="w", padx=24, pady=12)

    row = tk.Frame(win, bg=BG_CARD)
    row.pack(pady=(0,18))

    def _btn(parent, texto, accion, bg):
        f = tk.Frame(parent, bg=bg, cursor="hand2")
        f.pack(side="left", padx=8)
        l = tk.Label(f, text=texto, font=FONT_BTN, bg=bg, fg="white", padx=18, pady=6)
        l.pack()
        def do(e=None): result[0] = accion; win.destroy()
        f.bind("<Button-1>", do); l.bind("<Button-1>", do)
        def hon(e): f.config(bg="#FFF"); l.config(bg="#FFF", fg=bg)
        def hof(e): f.config(bg=bg); l.config(bg=bg, fg="white")
        f.bind("<Enter>", hon); l.bind("<Enter>", hon)
        f.bind("<Leave>", hof); l.bind("<Leave>", hof)

    _btn(row, " Sí ", True, ACCENT_C)
    _btn(row, " No ", False, ACCENT_W)

    win.wait_window()
    return result[0]

def popup_input(titulo, prompt, tipo="str", color=ACCENT_A):
    result = [None]
    win = tk.Toplevel(root)
    win.title(titulo)
    win.configure(bg=BG_CARD)
    win.resizable(False, False)
    win.grab_set()

    root.update_idletasks()
    x = root.winfo_x() + root.winfo_width()//2 - 220
    y = root.winfo_y() + root.winfo_height()//2 - 120
    win.geometry(f"440x220+{x}+{y}")

    tk.Frame(win, bg=color, height=4).pack(fill="x")
    tk.Label(win, text="▶  " + titulo, font=("Courier New", 13, "bold"),
             bg=BG_CARD, fg=color).pack(anchor="w", padx=24, pady=(14,4))
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=24)
    tk.Label(win, text=prompt, font=FONT_LABEL, bg=BG_CARD,
             fg=TEXT_SEC).pack(anchor="w", padx=24, pady=(10,4))

    entry_frame = tk.Frame(win, bg=color, padx=2, pady=2)
    entry_frame.pack(padx=24, fill="x")
    entry = tk.Entry(entry_frame, font=FONT_INPUT, bg=BG_INPUT,
                     fg=TEXT_PRI, insertbackground=color,
                     relief="flat", bd=6)
    entry.pack(fill="x")
    entry.focus()

    row = tk.Frame(win, bg=BG_CARD)
    row.pack(pady=14)

    def confirmar(e=None):
        val = entry.get().strip()
        try:
            if tipo == "int":
                result[0] = int(val)
            elif tipo == "float":
                result[0] = float(val)
            else:
                result[0] = val
            win.destroy()
        except ValueError:
            entry.config(bg="#3A1A1A")
            entry.after(300, lambda: entry.config(bg=BG_INPUT))

    def cancelar(e=None):
        win.destroy()

    entry.bind("<Return>", confirmar)

    def _btn(parent, texto, accion, bg):
        f = tk.Frame(parent, bg=bg, cursor="hand2")
        f.pack(side="left", padx=6)
        l = tk.Label(f, text=texto, font=FONT_BTN, bg=bg, fg="white", padx=16, pady=5)
        l.pack()
        f.bind("<Button-1>", lambda e: accion())
        l.bind("<Button-1>", lambda e: accion())
        def hon(e): f.config(bg="#FFF"); l.config(bg="#FFF", fg=bg)
        def hof(e): f.config(bg=bg); l.config(bg=bg, fg="white")
        f.bind("<Enter>", hon); l.bind("<Enter>", hon)
        f.bind("<Leave>", hof); l.bind("<Leave>", hof)

    _btn(row, " Confirmar ", confirmar, color)
    _btn(row, " Cancelar  ", cancelar, ACCENT_W)

    win.wait_window()
    return result[0]

#  WIDGET HELPERS

def limpiar():
    for w in frame.winfo_children():
        w.destroy()

def boton_moderno(texto, color, comando, parent, fill=True):
    outer = tk.Frame(parent, bg=color, padx=2, pady=0)
    if fill:
        outer.pack(fill="x", padx=30, pady=6)
    else:
        outer.pack(padx=10, pady=6)

    inner = tk.Frame(outer, bg=BG_INPUT, cursor="hand2")
    inner.pack(fill="both")

    lbl = tk.Label(inner, text=texto, font=FONT_BTN, bg=BG_INPUT,
                   fg=color, pady=13, anchor="center")
    lbl.pack(fill="both", expand=True)

    def on(e):
        inner.config(bg=color); lbl.config(bg=color, fg="white")
    def off(e):
        inner.config(bg=BG_INPUT); lbl.config(bg=BG_INPUT, fg=color)
    def click(e):
        comando()

    for w in (outer, inner, lbl):
        w.bind("<Enter>", on)
        w.bind("<Leave>", off)
        w.bind("<Button-1>", click)

def separador(parent, pady=10):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=30, pady=pady)

def tag_label(parent, texto, color):
    f = tk.Frame(parent, bg=color, padx=8, pady=2)
    f.pack()
    tk.Label(f, text=texto, font=FONT_SMALL, bg=color, fg="white").pack()

def entry_widget(parent, placeholder="", show=None):
    """Entry con borde de color y placeholder."""
    wrap = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    wrap.pack(fill="x", padx=30, pady=(0, 8))
    inner = tk.Frame(wrap, bg=BG_INPUT)
    inner.pack(fill="both")

    kw = dict(font=FONT_INPUT, bg=BG_INPUT, fg=TEXT_PRI,
              insertbackground=ACCENT_A, relief="flat", bd=8, highlightthickness=0)
    if show:
        kw["show"] = show
    e = tk.Entry(inner, **kw)
    e.pack(fill="x")

    # Placeholder
    if placeholder:
        e.insert(0, placeholder)
        e.config(fg=TEXT_HINT)
        def on_focus_in(ev):
            if e.get() == placeholder:
                e.delete(0, "end"); e.config(fg=TEXT_PRI)
        def on_focus_out(ev):
            if not e.get():
                e.insert(0, placeholder); e.config(fg=TEXT_HINT)
        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)

    # Borde activo
    def act(ev): wrap.config(bg=ACCENT_A)
    def des(ev): wrap.config(bg=BORDER)
    e.bind("<FocusIn>", lambda ev: (act(ev),))
    e.bind("<FocusOut>", lambda ev: (des(ev),))

    return e

def guardar_usuario():
    global id_usuario_actual

    entrada_id   = entry_id.get().strip()
    entrada_pass = entry_pass.get().strip()

    if entrada_id in ("", "ID de Operador") or not entrada_id.isdigit():
        popup_error("ID inválido", "El ID de operador debe ser un número entero.")
        return
    if entrada_pass in ("", "Contraseña"):
        popup_error("Contraseña vacía", "Por favor ingrese su contraseña.")
        return

    try:
        conexion = mysql.connector.connect(**config)
        cursor   = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (entrada_id,))
        usuario  = cursor.fetchone()

        if usuario:
            if usuario["password"] == entrada_pass:
                id_usuario_actual = int(entrada_id)
                popup_ok("Acceso concedido", f"Bienvenido, operador {entrada_id}.\nConexión establecida con el servidor.")
                menu_series()
            else:
                popup_error("Acceso denegado", "Contraseña incorrecta.\nVerifique sus credenciales e intente de nuevo.")
        else:
            crear = popup_yesno("Nuevo operador",
                                f"El ID {entrada_id} no está registrado.\n¿Desea crear una cuenta nueva?",
                                ACCENT_A)
            if crear:
                cursor.execute(
                    "INSERT INTO usuarios (id, password, nombre_usuario) VALUES (%s, %s, %s)",
                    (entrada_id, entrada_pass, f"Operador_{entrada_id}")
                )
                conexion.commit()
                id_usuario_actual = int(entrada_id)
                popup_ok("Cuenta creada", f"Operador {entrada_id} registrado correctamente.")
                menu_series()

        cursor.close()
        conexion.close()

    except mysql.connector.Error as err:
        popup_error("Error de conexión", f"MySQL Error:\n{err}")


def menu_series():
    limpiar()

    # Status bar top
    status = tk.Frame(frame, bg=BG_DARK)
    status.pack(fill="x", padx=0, pady=0)
    tk.Label(status, text=f"● CONECTADO  |  OP-{id_usuario_actual}  |  {datetime.now().strftime('%H:%M')}",
             font=FONT_SMALL, bg=BG_DARK, fg=ACCENT_C).pack(side="left", padx=16, pady=6)

    tk.Label(frame, text="SERIES DE TAYLOR", font=("Courier New", 26, "bold"),
             bg=BG_CARD, fg=TEXT_PRI).pack(pady=(28, 4))
    tk.Label(frame, text="Seleccione la función a calcular", font=FONT_SUB,
             bg=BG_CARD, fg=TEXT_SEC).pack(pady=(0, 20))

    separador(frame)

    for codigo, nombre, color, desc in [
        ('A', 'SIN(x)  —  Seno',    ACCENT_A, "Serie de Taylor del seno"),
        ('B', 'COS(x)  —  Coseno',  ACCENT_B, "Serie de Taylor del coseno"),
        ('C', 'ATAN(x) —  Arctan',  ACCENT_C, "Serie de Taylor de la arco tangente"),
    ]:
        card = tk.Frame(frame, bg=BG_INPUT, cursor="hand2")
        card.pack(fill="x", padx=30, pady=5)
        bar = tk.Frame(card, bg=color, width=5)
        bar.pack(side="left", fill="y")
        txt = tk.Frame(card, bg=BG_INPUT)
        txt.pack(side="left", fill="both", expand=True, padx=14, pady=14)
        tk.Label(txt, text=nombre, font=FONT_BTN, bg=BG_INPUT, fg=color).pack(anchor="w")
        tk.Label(txt, text=desc,   font=FONT_LABEL, bg=BG_INPUT, fg=TEXT_SEC).pack(anchor="w")

        _c = codigo
        def hover_on(e, c=card, col=color):
            c.config(bg=col); [w.config(bg=col) for w in c.winfo_children() if isinstance(w, tk.Frame)]
        def hover_off(e, c=card):
            c.config(bg=BG_INPUT); [w.config(bg=BG_INPUT) for w in c.winfo_children() if isinstance(w, tk.Frame)]
        def click_fn(e, co=_c): crud(co)

        for w in [card, txt]:
            w.bind("<Enter>", hover_on)
            w.bind("<Leave>", hover_off)
            w.bind("<Button-1>", click_fn)
        for lbl in txt.winfo_children():
            lbl.bind("<Enter>", hover_on)
            lbl.bind("<Leave>", hover_off)
            lbl.bind("<Button-1>", click_fn)

    separador(frame, pady=14)
    tk.Label(frame, text="INTERNET OF THINGS", font=FONT_SMALL,
             bg=BG_CARD, fg=TEXT_HINT).pack(pady=(0,16))


def crud(opcion):
    tabla_db      = NOMBRES_TABLAS[opcion]
    nombre_mostrar = NOMBRES_MOSTRAR[opcion]
    color         = ACCENTS_SERIE[opcion]
    limpiar()

    # Header con acento
    hdr = tk.Frame(frame, bg=color)
    hdr.pack(fill="x")
    tk.Label(hdr, text=f"  {nombre_mostrar.upper()}  —  Gestión de datos",
             font=("Courier New", 14, "bold"), bg=color, fg="white").pack(
             side="left", padx=16, pady=10)

    tk.Label(frame, text="¿Qué operación desea realizar?", font=FONT_SUB,
             bg=BG_CARD, fg=TEXT_SEC).pack(pady=(22, 12))

    ops = [
        ("  Calcular y Enviar datos",      ACCENT_OK,  lambda: pantalla_crear(tabla_db, nombre_mostrar, opcion)),
        ("  Ver registro por ID",           ACCENT_B,   lambda: accion_rapida("Leer", tabla_db)),
        ("  Editar resultado por ID",        ACCENT_A,   lambda: accion_rapida("Actualizar", tabla_db)),
        ("  Eliminar rango de registros",   ACCENT_W,   lambda: accion_rapida("Eliminar", tabla_db)),
    ]

    for texto, col, cmd in ops:
        boton_moderno(texto, col, cmd, frame)

    separador(frame, pady=12)
    boton_moderno("← Volver al menú principal", TEXT_HINT, menu_series, frame)

#  PANTALLA CALCULAR

def pantalla_crear(tabla_db, nombre_mostrar, opcion):
    color = ACCENTS_SERIE[opcion]
    limpiar()

    hdr = tk.Frame(frame, bg=color)
    hdr.pack(fill="x")
    tk.Label(hdr, text=f"  CALCULAR  —  {nombre_mostrar}",
             font=("Courier New", 14, "bold"), bg=color, fg="white").pack(
             side="left", padx=16, pady=10)

    tk.Label(frame, text="", bg=BG_CARD).pack(pady=6)
    tk.Label(frame, text="Valor de  X  (radianes)", font=FONT_LABEL,
             bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30)
    ex = entry_widget(frame)

    tk.Label(frame, text="Número de iteraciones  (n)", font=FONT_LABEL,
             bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(8,0))
    en = entry_widget(frame)

    # Hints
    hints = tk.Frame(frame, bg=BG_DARK)
    hints.pack(fill="x", padx=30, pady=10)
    tk.Label(hints, text="  ℹ  X ∈ [−2π, 2π]   |   n ∈ [1, 50]",
             font=FONT_SMALL, bg=BG_DARK, fg=TEXT_HINT).pack(
             anchor="w", padx=10, pady=6)
    if tabla_db == "arctan":
        tk.Label(hints, text="  ⚠  Para Arctan: X ∈ (−1, 1)",
                 font=FONT_SMALL, bg=BG_DARK, fg=ACCENT_W).pack(
                 anchor="w", padx=10, pady=(0,6))

    separador(frame, pady=8)

    boton_moderno("▶  Generar y enviar a BD", color,
                  lambda: ejecutar_calculos(tabla_db, ex.get(), en.get(), opcion), frame)
    boton_moderno("← Volver", TEXT_HINT, lambda: crud(opcion), frame)


#  EJECUTAR CÁLCULOS

def ejecutar_calculos(tabla, x_val, it_val, opcion):
    try:
        x_valor    = float(x_val)
        iteraciones = int(it_val)
    except ValueError:
        popup_error("Entrada inválida", "Ingrese valores numéricos válidos en ambos campos.")
        return

    if abs(x_valor) > 2 * math.pi:
        popup_error("Valor fuera de rango",
                    "X debe estar entre −2π y 2π radianes.\n"
                    "Fuera de este rango la serie puede divergir.")
        return

    if tabla == "arctan" and abs(x_valor) > 1.0:
        popup_error("Divergencia matemática",
                    "Para Arctan, X debe estar en (−1, 1).\n"
                    "La serie no converge fuera de este intervalo.")
        return

    if not (1 <= iteraciones <= 50):
        popup_error("Iteraciones inválidas",
                    "El número de iteraciones debe estar entre 1 y 50.")
        return

    try:
        conexion = mysql.connector.connect(**config)
        cursor   = conexion.cursor()

        for i in range(1, iteraciones + 1):
            if tabla == "seno":
                resultado, error = calcular_seno_taylor(x_valor, i)
            elif tabla == "coseno":
                resultado, error = calcular_coseno_taylor(x_valor, i)
            else:
                resultado, error = calcular_arctan_taylor(x_valor, i)

            ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                f"INSERT INTO {tabla} (idu, nregistro, x, res, error, timed) VALUES (%s,%s,%s,%s,%s,%s)",
                (id_usuario_actual, i, x_valor, resultado, error, ahora)
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        popup_ok("Datos enviados",
                 f"{iteraciones} registros insertados correctamente\nen la tabla '{tabla}'.")
        crud(opcion)

    except mysql.connector.Error as err:
        popup_error("Error de base de datos", f"MySQL Error:\n{err}")


def accion_rapida(accion, tabla):
    try:
        conexion = mysql.connector.connect(**config)
        cursor   = conexion.cursor(dictionary=True)

        if accion == "Eliminar":
            id_inicio = popup_input("Eliminar rango", "ID inicial del rango:", tipo="int", color=ACCENT_W)
            if id_inicio is None: return
            id_final  = popup_input("Eliminar rango", "ID final del rango:",   tipo="int", color=ACCENT_W)
            if id_final is None: return

            if id_inicio > id_final:
                popup_error("Rango inválido", "El ID inicial no puede ser mayor que el ID final.")
                return

            confirmar = popup_yesno("Confirmar eliminación",
                                    f"Se eliminarán los registros con ID entre {id_inicio} y {id_final}.\n¿Está seguro?",
                                    ACCENT_W)
            if confirmar:
                cursor.execute(
                    f"DELETE FROM {tabla} WHERE id BETWEEN %s AND %s",
                    (id_inicio, id_final)
                )
                conexion.commit()
                popup_ok("Eliminados", f"Registros {id_inicio} — {id_final} eliminados correctamente.")

        else:
            id_reg = popup_input(accion, f"Ingrese el ID del registro en '{tabla}':", tipo="int", color=ACCENT_A)
            if id_reg is None: return

            cursor.execute(f"SELECT * FROM {tabla} WHERE id = %s", (id_reg,))
            reg = cursor.fetchone()

            if not reg:
                popup_error("No encontrado", f"No existe ningún registro con ID {id_reg} en la tabla '{tabla}'.")
                return

            if accion == "Leer":
                info = (
                    f"Tabla : {tabla.upper()}\n"
                    f"ID    : {reg['id']}\n"
                    f"Usuario: {reg['idu']}\n"
                    f"Términos (n): {reg['nregistro']}\n"
                    f"Valor X: {reg['x']}\n"
                    f"Resultado: {reg['res']:.8f}\n"
                    f"Error   : {reg['error']:.4e}\n"
                    f"Fecha   : {reg['timed']}"
                )
                popup_info("Registro encontrado", info)

            elif accion == "Actualizar":
                nuevo_res = popup_input(
                    "Actualizar resultado",
                    f"Valor actual: {reg['res']:.6f}\nIngrese el nuevo resultado:",
                    tipo="float", color=ACCENT_A
                )
                if nuevo_res is not None:
                    x_val = reg['x']
                    if tabla == "seno":
                        valor_real = math.sin(x_val)
                    elif tabla == "coseno":
                        valor_real = math.cos(x_val)
                    else:
                        valor_real = math.atan(x_val)

                    nuevo_error = abs(valor_real - nuevo_res)
                    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    cursor.execute(
                        f"UPDATE {tabla} SET res=%s, error=%s, timed=%s WHERE id=%s",
                        (nuevo_res, nuevo_error, ahora, id_reg)
                    )
                    conexion.commit()
                    popup_ok("Actualizado",
                             f"Registro ID {id_reg} actualizado.\n"
                             f"Nuevo error calculado: {nuevo_error:.4e}")

        cursor.close()
        conexion.close()

    except Exception as e:
        popup_error("Error inesperado", str(e))

#  VENTANA PRINCIPAL

root = tk.Tk()
root.title("INTERNET OF THINGS")
root.geometry("620x680")
root.configure(bg=BG_DARK)
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Contenedor principal
frame = tk.Frame(root, bg=BG_CARD)
frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
frame.grid_columnconfigure(0, weight=1)

# ─ LOGIN ─
# Banner superior
banner = tk.Frame(frame, bg=ACCENT_A)
banner.pack(fill="x")
tk.Label(banner, text=" INTERNET OF THINGS",
         font=("Courier New", 16, "bold"), bg=ACCENT_A, fg="white").pack(
         side="left", padx=16, pady=12)
tk.Label(banner, text="v2.0  ",
         font=FONT_SMALL, bg=ACCENT_A, fg="#B8B5FF").pack(side="right", pady=12)

tk.Label(frame, text="", bg=BG_CARD).pack(pady=8)
tk.Label(frame, text="ACCESO AL SISTEMA", font=("Courier New", 20, "bold"),
         bg=BG_CARD, fg=TEXT_PRI).pack()
tk.Label(frame, text="Ingrese sus credenciales de operador", font=FONT_SUB,
         bg=BG_CARD, fg=TEXT_SEC).pack(pady=(4,20))

separador(frame)

tk.Label(frame, text="ID DE OPERADOR", font=FONT_LABEL, bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(10,2))
entry_id = entry_widget(frame)

tk.Label(frame, text="CONTRASEÑA", font=FONT_LABEL, bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(8,2))
entry_pass = entry_widget(frame, show= "*")

tk.Label(frame, text="", bg=BG_CARD).pack(pady=4)
boton_moderno("▶  Conectar al servidor", ACCENT_A, guardar_usuario, frame)

separador(frame, pady=16)

tk.Label(frame, text="Servidor: 172.27.182.135  |  DB: Series",
         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_HINT).pack(pady=(0,16))

root.mainloop()
