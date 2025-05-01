from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import csv
from collections import Counter

def generar_reportes_frame(parent):
    # Crear un widget principal con área de desplazamiento
    main_widget = QWidget()
    scroll = QScrollArea()
    scroll.setWidget(main_widget)
    scroll.setWidgetResizable(True)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    scroll.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: white;
        }
    """)
    
    layout = QVBoxLayout(main_widget)
    layout.setSpacing(20)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Header
    header_label = QLabel("Reportes de Tickets")
    header_label.setStyleSheet("""
        QLabel {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px 0;
        }
    """)
    layout.addWidget(header_label)
    
    try:
        with open('ticket_data.csv', mode='r') as file:
            tickets = list(csv.DictReader(file))
            
        if not tickets:
            label = QLabel("No hay datos para generar reporte.")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            return frame
        
        # Estadísticas
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        stats_layout = QVBoxLayout(stats_frame)
        
        # Conteos
        conteo_cat = Counter(t['Categoría'] for t in tickets)
        conteo_pri = Counter(t['Prioridad'] for t in tickets)
        
        # Define priority order and colors
        prioridades_orden = ['Alta', 'Media', 'Baja']
        conteo_pri_ordenado = {p: conteo_pri.get(p, 0) for p in prioridades_orden}
        colors = ['#ff7f7f', '#ffcc7f', '#7fcc7f']  # Red, Orange, Green
        
        # Mostrar estadísticas
        stats_header = QLabel("Estadísticas")
        stats_header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px 0;")
        stats_layout.addWidget(stats_header)
        
        # Create statistics container
        stats_container = QWidget()
        stats_layout_h = QHBoxLayout(stats_container)
        
        # Categoría section
        cat_frame = QFrame()
        cat_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #2c3e50;
                margin: 5px 0;
            }
        """)
        cat_layout = QVBoxLayout(cat_frame)
        
        cat_header = QLabel("Distribución por Categoría:")
        cat_header.setStyleSheet("font-weight: bold; font-size: 15px;")
        cat_layout.addWidget(cat_header)
        
        total_tickets = sum(conteo_cat.values())
        for categoria, cantidad in conteo_cat.items():
            porcentaje = (cantidad / total_tickets) * 100
            cat_label = QLabel(f"{categoria}: {cantidad} tickets ({porcentaje:.1f}%)")
            cat_layout.addWidget(cat_label)
        
        stats_layout_h.addWidget(cat_frame)
        
        # Seccion
        pri_frame = QFrame()
        pri_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 5px;
                padding: 10px;
                margin-left: 10px;
            }
            QLabel {
                color: #2c3e50;
                margin: 5px 0;
            }
        """)
        pri_layout = QVBoxLayout(pri_frame)
        
        pri_header = QLabel("Distribución por Prioridad:")
        pri_header.setStyleSheet("font-weight: bold; font-size: 15px;")
        pri_layout.addWidget(pri_header)
        
        for prioridad in ['Alta', 'Media', 'Baja']:
            cantidad = conteo_pri.get(prioridad, 0)
            pri_label = QLabel(f"{prioridad}: {cantidad} tickets")
            pri_layout.addWidget(pri_label)
        
        stats_layout_h.addWidget(pri_frame)
        
        stats_layout.addWidget(stats_container)

        spacer = QLabel()
        spacer.setFixedHeight(20)
        stats_layout.addWidget(spacer)
        
        # Sección de gráficos
        charts_container = QFrame()
        charts_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        charts_grid = QVBoxLayout(charts_container)
        
        # Primera fila: gráficos de barras
        row1_container = QWidget()
        row1_layout = QHBoxLayout(row1_container)
        
        # Contenedor de gráfico de categorías
        cat_chart_container = QFrame()
        cat_chart_layout = QVBoxLayout(cat_chart_container)
        fig1 = plt.figure(figsize=(6, 5))
        ax1 = fig1.add_subplot(111)
        ax1.bar(conteo_cat.keys(), conteo_cat.values(), color='skyblue')
        ax1.set_title("Tickets por Categoría")
        ax1.set_xlabel("Categoría")
        ax1.set_ylabel("Número de Tickets")
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout(pad=1.5)
        canvas1 = FigureCanvas(fig1)
        canvas1.setMinimumSize(400, 300)
        cat_chart_layout.addWidget(canvas1)
        row1_layout.addWidget(cat_chart_container)
        
        # Contenedor de gráfico de prioridades
        pri_chart_container = QFrame()
        pri_chart_layout = QVBoxLayout(pri_chart_container)
        fig2 = plt.figure(figsize=(6, 5))
        ax2 = fig2.add_subplot(111)
        ax2.bar(conteo_pri_ordenado.keys(), conteo_pri_ordenado.values(), color=colors)
        ax2.set_title("Tickets por Prioridad")
        ax2.set_xlabel("Prioridad")
        ax2.set_ylabel("Número de Tickets")
        fig2.tight_layout(pad=1.5)
        canvas2 = FigureCanvas(fig2)
        canvas2.setMinimumSize(400, 300)
        pri_chart_layout.addWidget(canvas2)
        row1_layout.addWidget(pri_chart_container)
        
        # Primera fila
        charts_grid.addWidget(row1_container)
        
        # Segunda fila
        row2_container = QWidget()
        row2_layout = QHBoxLayout(row2_container)
        
        pie_chart_container = QFrame()
        pie_chart_layout = QVBoxLayout(pie_chart_container)
        fig3 = plt.figure(figsize=(8, 6))
        ax3 = fig3.add_subplot(111)
        wedges, texts, autotexts = ax3.pie(
            conteo_cat.values(),
            labels=conteo_cat.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Pastel1.colors
        )
        ax3.set_title("Distribución Porcentual por Categoría")
        fig3.tight_layout(pad=2)
        canvas3 = FigureCanvas(fig3)
        canvas3.setMinimumSize(500, 400)
        pie_chart_layout.addWidget(canvas3)
        row2_layout.addWidget(pie_chart_container)
        
        # Agregar segunda fila
        charts_grid.addWidget(row2_container)
        
        # Agregar contenedor de gráficos al diseño de estadísticas
        stats_layout.addWidget(charts_container)
        
        # Agregar marco de estadísticas al diseño principal
        layout.addWidget(stats_frame)
        
    except FileNotFoundError:
        label = QLabel("Error: Archivo de tickets no encontrado.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
    
    parent.addWidget(scroll)
    parent.setCurrentWidget(scroll)
    return scroll
