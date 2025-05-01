# ticket_manager.py
import csv
from datetime import datetime
from tkinter import messagebox, simpledialog
import random

from utils.classifier import clasificar_ticket
from utils.decision_tree import decidir_prioridad
from knowledge_base import soluciones_predefinidas
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

    # Fecha y hora actuales
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prioridad
    prioridad = decidir_prioridad(descripcion)

    # Verificar si puede resolverse automáticamente
    solucion = soluciones_predefinidas.get(categoria.lower(), None)
    if solucion:
        estado = "Resuelto automáticamente"
    else:
        estado = "Derivado a encargado"
    
    ticket = {
        "Nombre": nombre,
        "Categoría": categoria,
        "Descripción": descripcion,
        "FechaHora": fecha_hora,
        "Prioridad": prioridad,
        "Estado": estado,
        "Solución": solucion if solucion else "Pendiente derivación"
    }

    guardar_ticket(ticket)
    messagebox.showinfo("Ticket Creado", f"Ticket registrado exitosamente.\nEstado: {estado}")

# Ver historial de tickets
def ver_historial():
    from tkinter import Toplevel, ttk
    
    try:
        with open('ticket_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            tickets = list(reader)

            if not tickets:
                messagebox.showinfo("Historial", "No hay tickets registrados aún.")
                return

            # Crear ventana para el historial
            historial_window = Toplevel()
            historial_window.title("Historial de Tickets")
            historial_window.geometry("1000x600")
            
            # Frame para la tabla
            frame = ttk.Frame(historial_window)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Crear Treeview (tabla)
            tree = ttk.Treeview(frame, columns=list(tickets[0].keys()), show='headings')
            
            # Configurar columnas
            for col in tickets[0].keys():
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')
            
            # Ajustar tamaño de columnas importantes
            tree.column("Descripción", width=250)
            tree.column("Solución", width=250)
            
            # Añadir scrollbars
            vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Grid layout
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')
            
            # Configurar expansión
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            # Insertar datos
            for ticket in tickets:
                tree.insert('', 'end', values=list(ticket.values()))
                
            # Estilo
            style = ttk.Style()
            style.theme_use('clam')
            style.configure("Treeview", 
                          background="#f0f0f0",
                          foreground="black",
                          rowheight=25,
                          fieldbackground="#f0f0f0")
            style.map('Treeview', background=[('selected', '#0078d7')])
            
            # Botón de cerrar
            btn_cerrar = ttk.Button(historial_window, text="Cerrar", command=historial_window.destroy)
            btn_cerrar.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de tickets no encontrado.")


def crear_ticket_frame(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Header
    header = ttk.Frame(frame)
    header.pack(fill='x', pady=(0, 20))
    ttk.Label(header, text="Crear Nuevo Ticket", font=('Helvetica', 20)).pack(side='left')
    
    # Form fields
    form_frame = ttk.Frame(frame)
    form_frame.pack(fill='both', expand=True)
    
    # Add form fields
    ttk.Label(form_frame, text="Nombre:").pack(pady=5)
    nombre_entry = ttk.Entry(form_frame, width=50)
    nombre_entry.pack(pady=5)
    
    ttk.Label(form_frame, text="Descripción:").pack(pady=5)
    desc_entry = ttk.Text(form_frame, width=50, height=5)
    desc_entry.pack(pady=5)
    
    def submit():
        nombre = nombre_entry.get()
        descripcion = desc_entry.get("1.0", "end-1c")
        
        if not nombre or not descripcion:
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
            
        # Rest of the ticket creation logic
        categoria = clasificar_ticket(descripcion)
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prioridad = decidir_prioridad(descripcion)
        
        solucion = soluciones_predefinidas.get(categoria.lower(), None)
        estado = "Resuelto automáticamente" if solucion else "Derivado a encargado"
        
        ticket = {
            "Nombre": nombre,
            "Categoría": categoria,
            "Descripción": descripcion,
            "FechaHora": fecha_hora,
            "Prioridad": prioridad,
            "Estado": estado,
            "Solución": solucion if solucion else "Pendiente derivación"
        }
        
        guardar_ticket(ticket)
        messagebox.showinfo("Éxito", "Ticket creado exitosamente")
        nombre_entry.delete(0, 'end')
        desc_entry.delete("1.0", "end")
    
    ttk.Button(form_frame, text="Crear Ticket", command=submit).pack(pady=20)

def ver_historial_frame(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Header
    header = ttk.Frame(frame)
    header.pack(fill='x', pady=(0, 20))
    ttk.Label(header, text="Historial de Tickets", font=('Helvetica', 20)).pack(side='left')
    
    try:
        with open('ticket_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            tickets = list(reader)

            if not tickets:
                ttk.Label(frame, text="No hay tickets registrados aún.").pack(pady=20)
                return

            # Create Treeview
            tree = ttk.Treeview(frame, columns=list(tickets[0].keys()), show='headings')
            
            # Configure columns
            for col in tickets[0].keys():
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')
            
            tree.column("Descripción", width=250)
            tree.column("Solución", width=250)
            
            # Add scrollbars
            vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Grid layout
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            for ticket in tickets:
                tree.insert('', 'end', values=list(ticket.values()))

    except FileNotFoundError:
        ttk.Label(frame, text="No se encontró el archivo de tickets.").pack(pady=20)
