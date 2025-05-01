# main.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Funciones que conectarán a otros módulos (las crearemos luego)
def crear_ticket():
    from ticket_manager import crear_ticket
    crear_ticket()

def ver_historial():
    from ticket_manager import ver_historial
    ver_historial()

def generar_reportes():
    from report_generator import generar_reportes
    generar_reportes()

def salir():
    if messagebox.askyesno("Salir", "¿Deseas salir de la aplicación?"):
        ventana.destroy()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor Inteligente de Tickets")
ventana.geometry("900x600")
ventana.resizable(False, False)

# Fondo
fondo = Image.open("assets/background.jpg")
fondo = fondo.resize((900, 600))
fondo_tk = ImageTk.PhotoImage(fondo)

label_fondo = tk.Label(ventana, image=fondo_tk)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Logo
logo = Image.open("assets/logo.png")
logo = logo.resize((200, 100))
logo_tk = ImageTk.PhotoImage(logo)

label_logo = tk.Label(ventana, image=logo_tk, bg="white")
label_logo.place(x=350, y=20)

# Botones principales
def crear_boton(ruta_img, texto, comando, x, y):
    img = Image.open(ruta_img)
    img = img.resize((100, 100))
    img_tk = ImageTk.PhotoImage(img)

    boton = tk.Button(ventana, image=img_tk, text=texto, compound="top",
                      command=comando, bg="#f0f0f0", font=("Arial", 12, "bold"),
                      bd=0, highlightthickness=0)
    boton.image = img_tk  # Importante para que no se elimine la imagen
    boton.place(x=x, y=y, width=150, height=150)

# Crear botones
crear_boton("assets/icon_ticket.png", "Nuevo Ticket", crear_ticket, 150, 250)
crear_boton("assets/icon_report.png", "Ver Historial", ver_historial, 375, 250)
crear_boton("assets/icon_exit.png", "Reportes", generar_reportes, 600, 250)

# Botón salir
boton_salir = tk.Button(ventana, text="Salir", command=salir,
                        font=("Arial", 12), bg="red", fg="white")
boton_salir.place(x=750, y=540, width=100, height=40)

ventana.mainloop()
