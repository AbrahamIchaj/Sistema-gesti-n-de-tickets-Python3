# ticket_manager.py
import csv
from datetime import datetime
from tkinter import messagebox, simpledialog
import random

from utils.classifier import clasificar_ticket
from utils.decision_tree import decidir_prioridad
from knowledge_base import soluciones_predefinidas
from utils.file_handler import guardar_ticket
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QPushButton, QTableWidget, QTableWidgetItem,
                            QScrollArea, QHeaderView, QMessageBox, QLineEdit, QTextEdit)
from PyQt5.QtCore import Qt

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
    frame = QWidget()
    layout = QVBoxLayout(frame)
    
    # Header
    header_label = QLabel("Crear Nuevo Ticket")
    header_label.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 20px 0;
    """)
    layout.addWidget(header_label)
    
    # Form fields
    form_layout = QVBoxLayout()
    
    # Nombre field
    nombre_label = QLabel("Nombre:")
    nombre_input = QLineEdit()
    nombre_input.setStyleSheet("padding: 8px;")
    form_layout.addWidget(nombre_label)
    form_layout.addWidget(nombre_input)
    
    # Descripción field
    desc_label = QLabel("Descripción:")
    desc_input = QTextEdit()
    desc_input.setStyleSheet("padding: 8px;")
    form_layout.addWidget(desc_label)
    form_layout.addWidget(desc_input)
    
    # Submit button
    submit_btn = QPushButton("Crear Ticket")
    submit_btn.setStyleSheet("""
        QPushButton {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
    """)
    
    def submit():
        nombre = nombre_input.text()
        descripcion = desc_input.toPlainText()
        
        if not nombre or not descripcion:
            QMessageBox.critical(frame, "Error", "Todos los campos son requeridos")
            return
            
        # Ticket logic
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
        QMessageBox.information(frame, "Éxito", "Ticket creado exitosamente")
        nombre_input.clear()
        desc_input.clear()
    
    submit_btn.clicked.connect(submit)
    form_layout.addWidget(submit_btn)
    
    layout.addLayout(form_layout)
    parent.addWidget(frame)
    parent.setCurrentWidget(frame)
    return frame

def ver_historial_frame(parent):
    frame = QWidget()
    layout = QVBoxLayout(frame)
    
    # Header
    header_label = QLabel("Historial de Tickets")
    header_label.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 20px 0;
    """)
    layout.addWidget(header_label)
    
    try:
        with open('ticket_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            tickets = list(reader)

            if not tickets:
                empty_label = QLabel("No hay tickets registrados aún.")
                empty_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(empty_label)
                parent.addWidget(frame)
                parent.setCurrentWidget(frame)
                return

            # Crear tabla
            table = QTableWidget()
            headers = list(tickets[0].keys())
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(tickets))
            
            # Configurar tabla para adaptarse al ancho
            table.horizontalHeader().setStretchLastSection(True)
            for i in range(len(headers)):
                if headers[i] in ["Descripción", "Solución"]:
                    table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
                else:
                    table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            
            table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    gridline-color: #d0d0d0;
                    border: 1px solid #d0d0d0;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                    font-weight: bold;
                }
            """)
            
            # Insertar datos
            for row, ticket in enumerate(tickets):
                for col, (key, value) in enumerate(ticket.items()):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                    table.setItem(row, col, item)
            
            layout.addWidget(table)

    except FileNotFoundError:
        error_label = QLabel("No se encontró el archivo de tickets.")
        error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(error_label)
    
    parent.addWidget(frame)
    parent.setCurrentWidget(frame)
    return frame
