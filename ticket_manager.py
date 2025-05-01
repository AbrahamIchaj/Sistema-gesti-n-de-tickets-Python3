# ticket_manager.py
import csv
from datetime import datetime
from tkinter import messagebox, simpledialog
import random

from utils.classifier import clasificar_ticket
from utils.decision_tree import decidir_prioridad
from knowledge_base import soluciones_predefinidas, obtener_solucion  # Updated import
from utils.file_handler import guardar_ticket

# Categorías posibles
CATEGORIAS = ['Agua', 'Electricidad', 'Seguridad', 'Ruido', 'Limpieza']

# Crear nuevo ticket
def crear_ticket():
    nombre = simpledialog.askstring("Nuevo Ticket", "Ingrese su nombre:")
    if not nombre:
        messagebox.showerror("Error", "Nombre no ingresado")
        return

    descripcion = simpledialog.askstring("Nuevo Ticket", "Describa el problema:")
    if not descripcion:
        messagebox.showerror("Error", "Descripción no ingresada")
        return

    # Clasificar automáticamente
    categoria = clasificar_ticket(descripcion)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Usar árbol de decisión para determinar prioridad y necesidad de profesional
    decision = decidir_prioridad(descripcion, categoria)
    prioridad = decision["prioridad"]
    requiere_profesional = decision["professional_required"]

    # Obtener solución basada en la decisión
    if requiere_profesional:
        estado = "Derivado a encargado"
        solucion = f"Se requiere atención profesional. Un especialista en {categoria} será asignado."
        if prioridad == "Alta":
            solucion = f"URGENTE: {solucion} Tiempo estimado de respuesta: 30 minutos."
    else:
        estado = "Auto-resolución sugerida"
        solucion = obtener_solucion(categoria, descripcion)

    ticket = {
        "Nombre": nombre,
        "Categoría": categoria,
        "Descripción": descripcion,
        "FechaHora": fecha_hora,
        "Prioridad": prioridad,
        "Estado": estado,
        "Solución": solucion,
        "Requiere_Profesional": "Sí" if requiere_profesional else "No"
    }

    guardar_ticket(ticket)
    
    mensaje = f"""Ticket registrado exitosamente.
Categoría: {categoria}
Prioridad: {prioridad}
Estado: {estado}
{'IMPORTANTE: Se ha notificado al equipo de especialistas.' if requiere_profesional else 'Se sugiere seguir las instrucciones proporcionadas.'}"""
    
    messagebox.showinfo("Ticket Creado", mensaje)

# Ver historial de tickets
def ver_historial():
    import tkinter as tk
    from tkinter import ttk
    
    # Create history window
    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial de Tickets")
    ventana_historial.geometry("1000x600")
    
    # Create treeview
    tree = ttk.Treeview(ventana_historial)
    tree["columns"] = ("Nombre", "Categoría", "Descripción", "FechaHora", 
                      "Prioridad", "Estado", "Solución", "Requiere_Profesional")
    
    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Nombre", width=100, anchor=tk.CENTER)
    tree.column("Categoría", width=100, anchor=tk.CENTER)
    tree.column("Descripción", width=200, anchor=tk.W)
    tree.column("FechaHora", width=150, anchor=tk.CENTER)
    tree.column("Prioridad", width=80, anchor=tk.CENTER)
    tree.column("Estado", width=150, anchor=tk.CENTER)
    tree.column("Solución", width=200, anchor=tk.W)
    tree.column("Requiere_Profesional", width=100, anchor=tk.CENTER)
    
    # Create headings
    tree.heading("#0", text="")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Categoría", text="Categoría")
    tree.heading("Descripción", text="Descripción")
    tree.heading("FechaHora", text="Fecha y Hora")
    tree.heading("Prioridad", text="Prioridad")
    tree.heading("Estado", text="Estado")
    tree.heading("Solución", text="Solución")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(ventana_historial, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack elements
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    try:
        with open('ticket_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                tree.insert("", "end", values=(
                    row["Nombre"],
                    row["Categoría"],
                    row["Descripción"],
                    row["FechaHora"],
                    row["Prioridad"],
                    row["Estado"],
                    row["Solución"]
                ))
                
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de tickets no encontrado.")
