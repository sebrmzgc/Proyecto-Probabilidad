"""
========================================================================
PROYECTO: CALCULADORA DE TAMAÑO DE MUESTRA (MEDIA Y PROPORCIÓN)
ESCOM - Ingeniería en Sistemas Computacionales
Materia: Probabilidad y Estadística

AUTORES:
- López Sánchez Bethzy Susana
- Parra Jacinto Nataly Aidee
- Ramírez García José Sebastián

INSTRUCCIONES DE EJECUCIÓN:
Este programa utiliza interfaz gráfica (Tkinter) y librerías científicas.
Antes de ejecutar, asegúrese de tener instaladas las dependencias:

    pip install numpy scipy matplotlib

Nota: Tkinter y Math vienen incluidos por defecto en Python.
========================================================================
"""

# Importación de librerías
import tkinter as tk                       # Para la interfaz gráfica
from tkinter import ttk, messagebox        # ttk para estilos, messagebox para mostrar errores
import math                                # Funciones matemáticas básicas
import numpy as np                         # Librería científica (vectores, arrays)
from scipy.stats import norm               # Distribución normal para obtener valores Z
import matplotlib.pyplot as plt            # Para graficar los resultados


# CONFIGURACIÓN DE COLORES Y ESTILO
COLOR_FONDO = "#FFF0F5"       # Color de fondo general de la ventana
COLOR_BOTON_CALC = "#C2185B"  # Color de los botones de calcular
COLOR_BOTON_GRAF = "#00796B"  # Color de los botones de graficar
COLOR_TEXTO = "#4A002C"       # Color de texto principal
FUENTE_TITULO = ("Helvetica", 14, "bold") # Fuente de títulos
FUENTE_TEXTO = ("Helvetica", 10)          # Fuente de texto general

# LÓGICA MATEMÁTICA (Backend)

# Función para obtener el valor Z según el nivel de confianza
def z_score(confianza):
    # norm.ppf: retorna el percentil de la distribución normal
    # Para un intervalo de confianza bilateral
    return norm.ppf(1 - (1 - confianza) / 2)

# Tamaño de muestra para media poblacional
def tamano_muestra_media(confianza, sigma, error):
    z = z_score(confianza)             # Calcula Z según nivel de confianza
    n = (z * sigma / error) ** 2       # Fórmula del tamaño de muestra
    return math.ceil(n), z             # math.ceil para redondear hacia arriba

# Tamaño de muestra para proporción poblacional
def tamano_muestra_proporcion(confianza, p, error):
    z = z_score(confianza)
    n = (z**2 * p * (1 - p)) / (error**2)  # Fórmula para proporción
    return math.ceil(n), z

# FUNCIONES DE GRÁFICA

# Grafica para media poblacional
def mostrar_grafica_media(confianza, sigma, error_usuario):
    z = z_score(confianza)
    e_vals = np.linspace(error_usuario * 0.2, error_usuario * 2.5, 100)  # Rango de errores
    n_vals = (z * sigma / e_vals)**2                                     # Calcula n para cada error

    plt.figure(figsize=(7, 5))
    plt.plot(e_vals, n_vals, label="Curva n vs E", color='#C2185B', linewidth=2)  # Línea principal
    n_calc = (z * sigma / error_usuario)**2
    plt.scatter([error_usuario], [n_calc], color='#00796B', zorder=5, s=100, label=f'Tu caso (n={math.ceil(n_calc)})')  # Punto del usuario
    
    # Configuración de la gráfica
    plt.title("Tamaño de Muestra vs Margen de Error (Media)")
    plt.xlabel("Margen de Error (E)")
    plt.ylabel("Tamaño de muestra (n)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

# Grafica para proporción poblacional
def mostrar_grafica_proporcion(confianza, p, error_usuario):
    z = z_score(confianza)
    e_vals = np.linspace(error_usuario * 0.2, error_usuario * 2.5, 100)
    n_vals = (z**2 * p * (1 - p)) / (e_vals**2)

    plt.figure(figsize=(7, 5))
    plt.plot(e_vals, n_vals, label="Curva n vs E", color='#C2185B', linewidth=2)
    n_calc = (z**2 * p * (1 - p)) / (error_usuario**2)
    plt.scatter([error_usuario], [n_calc], color='#00796B', zorder=5, s=100, label=f'Tu caso (n={math.ceil(n_calc)})')

    plt.title("Tamaño de Muestra vs Margen de Error (Proporción)")
    plt.xlabel("Margen de Error (E)")
    plt.ylabel("Tamaño de muestra (n)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

# INTERFAZ GRÁFICA (Frontend)

# Función que se ejecuta al presionar calcular en Media
def calcular_media():
    try:
        conf = float(entry_m_confianza.get())
        sigma = float(entry_m_sigma.get())
        err = float(entry_m_error.get())
        n, z = tamano_muestra_media(conf, sigma, err)  # Calcula n y z

        # Muestra resultados en la interfaz
        lbl_m_res_n.config(text=f"n = {n}", fg=COLOR_BOTON_CALC)
        lbl_m_res_z.config(text=f"Valor Z utilizado: {z:.4f}")
        # Habilita botón de gráfica con función asociada
        btn_m_graficar.config(state="normal", bg=COLOR_BOTON_GRAF, command=lambda: mostrar_grafica_media(conf, sigma, err))
    except ValueError:
        messagebox.showerror("Error", "Por favor revisa que todos los campos sean números.")

# Función que se ejecuta al presionar calcular en Proporción
def calcular_proporcion():
    try:
        conf = float(entry_p_confianza.get())
        p_val_str = entry_p_p.get()
        p_val = float(p_val_str) if p_val_str else 0.5  # Valor por defecto 0.5 si está vacío
        err = float(entry_p_error.get())
        n, z = tamano_muestra_proporcion(conf, p_val, err)

        lbl_p_res_n.config(text=f"n = {n}", fg=COLOR_BOTON_CALC)
        lbl_p_res_z.config(text=f"Valor Z utilizado: {z:.4f}")
        btn_p_graficar.config(state="normal", bg=COLOR_BOTON_GRAF, command=lambda: mostrar_grafica_proporcion(conf, p_val, err))
    except ValueError:
        messagebox.showerror("Error", "Por favor revisa el campo 1 ya que es de (0-1) o que no hayas ingresado letras.")

# Ventana Principal
root = tk.Tk()
root.title("Calculadora de Muestra")
root.geometry("500x650") # Tamaño de ventana
root.configure(bg=COLOR_FONDO)

# Encabezado
tk.Label(root, text="Calculadora Estadística", font=("Helvetica", 18, "bold"), 
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(15, 5))
tk.Label(root, text="Probabilidad y Estadística", font=("Helvetica", 11, "italic"), 
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=0)

# Estilo para las pestañas
style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
style.configure("TNotebook.Tab", background="#FFD1DC", foreground=COLOR_TEXTO, padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", COLOR_BOTON_CALC)], foreground=[("selected", "white")])

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")

#Pestaña 1: MEDIA
frame_media = tk.Frame(notebook, padx=20, pady=20, bg=COLOR_FONDO)
notebook.add(frame_media, text="  Media Poblacional  ")

tk.Label(frame_media, text="Nivel de Confianza (0-1):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
entry_m_confianza = tk.Entry(frame_media, font=FUENTE_TEXTO)
entry_m_confianza.pack(fill="x", pady=5)
entry_m_confianza.insert(0, "0.95")  # Valor por defecto

tk.Label(frame_media, text="Desviación Estándar (σ):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
entry_m_sigma = tk.Entry(frame_media, font=FUENTE_TEXTO)
entry_m_sigma.pack(fill="x", pady=5)

tk.Label(frame_media, text="Margen de Error (E):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
entry_m_error = tk.Entry(frame_media, font=FUENTE_TEXTO)
entry_m_error.pack(fill="x", pady=5)

btn_m_calc = tk.Button(frame_media, text="CALCULAR TAMAÑO DE MUESTRA", command=calcular_media, 
                       bg=COLOR_BOTON_CALC, fg="white", font=("Helvetica", 10, "bold"), relief="flat", pady=5)
btn_m_calc.pack(pady=15, fill="x")

lbl_m_res_n = tk.Label(frame_media, text="n = -", font=("Helvetica", 20, "bold"), bg=COLOR_FONDO, fg="#888")
lbl_m_res_n.pack(pady=5)
lbl_m_res_z = tk.Label(frame_media, text="Z = -", bg=COLOR_FONDO, fg=COLOR_TEXTO)
lbl_m_res_z.pack()

btn_m_graficar = tk.Button(frame_media, text="Ver Gráfica Interactiva", state="disabled", 
                           bg="#CCC", fg="white", font=("Helvetica", 9), relief="flat")
btn_m_graficar.pack(pady=10)

# Pestaña 2: PROPORCIÓN
frame_prop = tk.Frame(notebook, padx=20, pady=20, bg=COLOR_FONDO)
notebook.add(frame_prop, text="  Proporción Poblacional  ")

tk.Label(frame_prop, text="Nivel de Confianza (0-1):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
entry_p_confianza = tk.Entry(frame_prop, font=FUENTE_TEXTO)
entry_p_confianza.pack(fill="x", pady=5)
entry_p_confianza.insert(0, "0.95")

tk.Label(frame_prop, text="Proporción p (Dejar vacío para 0.5):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
entry_p_p = tk.Entry(frame_prop, font=FUENTE_TEXTO)
entry_p_p.pack(fill="x", pady=5)

tk.Label(frame_prop, text="Margen de Error (E):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w")
entry_p_error = tk.Entry(frame_prop, font=FUENTE_TEXTO)
entry_p_error.pack(fill="x", pady=5)

btn_p_calc = tk.Button(frame_prop, text="CALCULAR TAMAÑO DE MUESTRA", command=calcular_proporcion, 
                       bg=COLOR_BOTON_CALC, fg="white", font=("Helvetica", 10, "bold"), relief="flat", pady=5)
btn_p_calc.pack(pady=15, fill="x")

lbl_p_res_n = tk.Label(frame_prop, text="n = -", font=("Helvetica", 20, "bold"), bg=COLOR_FONDO, fg="#888")
lbl_p_res_n.pack(pady=5)
lbl_p_res_z = tk.Label(frame_prop, text="Z = -", bg=COLOR_FONDO, fg=COLOR_TEXTO)
lbl_p_res_z.pack()

btn_p_graficar = tk.Button(frame_prop, text="Ver Gráfica Interactiva", state="disabled", 
                           bg="#CCC", fg="white", font=("Helvetica", 9), relief="flat")
btn_p_graficar.pack(pady=10)

#Footer: INTEGRANTES
frame_footer = tk.Frame(root, bg=COLOR_FONDO, pady=10)
frame_footer.pack(side="bottom", fill="x")

tk.Label(frame_footer, text="INTEGRANTES DEL EQUIPO", font=("Helvetica", 9, "bold"), 
         bg=COLOR_FONDO, fg=COLOR_BOTON_CALC).pack()

integrantes = [
    "López Sánchez Bethzy Susana",
    "Parra Jacinto Nataly Aidee",
    "Ramírez García José Sebastián"
]

for nombre in integrantes:
    tk.Label(frame_footer, text=nombre, font=("Helvetica", 9), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

# Ejecuta el bucle principal de la ventana
root.mainloop()
