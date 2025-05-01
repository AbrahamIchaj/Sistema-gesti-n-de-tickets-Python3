from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QFrame, QStackedWidget, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
from PIL import Image
import sys
import os
import csv
from datetime import datetime

class ModernDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Tickets")
        self.setGeometry(100, 100, 1200, 700)
        
        # Configurar colores
        self.COLORS = {
            'primary': '#000000',
            'secondary': '#34495e',
            'accent': '#3498db',
            'bg': '#ffffff',
            'text': '#2c3e50',
            'white': '#ffffff'
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.setup_sidebar(main_layout)
        
        # Contenido principal
        self.setup_main_content(main_layout)
    
    def setup_sidebar(self, main_layout):
        # Crear sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['primary']};
                border: none;
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        
        # Logo
        try:
            logo_pixmap = QPixmap("assets/logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        except:
            logo_label = QLabel("Sistema de Tickets")
            logo_label.setStyleSheet(f"""
                color: {self.COLORS['white']};
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
            """)
            logo_label.setAlignment(Qt.AlignCenter)
        
        sidebar_layout.addWidget(logo_label)
        
        # Botones del sidebar
        buttons = [
            ("Inicio", self.mostrar_dashboard, "home.png"),
            ("Nuevo Ticket", self.crear_ticket, "add.png"),
            ("Ver Historial", self.ver_historial, "record.png"),
            ("Reportes", self.generar_reportes, "reports.png"),
            ("Salir", self.salir, None)
        ]
        
        for text, callback, icon_path in buttons:
            btn = self.create_sidebar_button(text, callback, icon_path, text == "Salir")
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)
    
    def create_sidebar_button(self, text, callback, icon_path, is_exit=False):
        btn = QPushButton(text)
        if icon_path:
            try:
                btn.setIcon(QIcon(f"assets/{icon_path}"))
                btn.setIconSize(QSize(24, 24))
            except:
                pass
        
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {self.COLORS['white']};
                background-color: {'#e74c3c' if is_exit else self.COLORS['primary']};
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
                border-radius: 5px;
                margin: 2px 10px;
            }}
            QPushButton:hover {{
                background-color: {'#c0392b' if is_exit else self.COLORS['secondary']};
            }}
        """)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(callback)
        return btn
    
    def setup_main_content(self, main_layout):
        # Contenedor principal
        self.content_widget = QStackedWidget()
        self.content_widget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {self.COLORS['bg']};
                border: none;
            }}
        """)
        
        # Dashboard inicial
        self.setup_dashboard()
        main_layout.addWidget(self.content_widget)
    
    def setup_dashboard(self):
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Dashboard de Gestión de Tickets")
        title.setStyleSheet(f"""
            color: {self.COLORS['text']};
            font-size: 24px;
            font-weight: bold;
            padding-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Obtener estadísticas de ticket_data.csv
        try:
            with open('ticket_data.csv', mode='r', newline='') as file:
                tickets = list(csv.DictReader(file))
                
                from datetime import datetime
                today = datetime.now().strftime("%Y-%m-%d")
                
                total_tickets = len(tickets)
                tickets_abiertos = sum(1 for t in tickets if t['Estado'] == 'Derivado a encargado')
                resueltos_hoy = sum(1 for t in tickets if t['FechaHora'].startswith(today))
                
                tiempo_promedio = "N/A"
                
                stats = [
                    ("Total Tickets", str(total_tickets)),
                    ("Tickets Abiertos", str(tickets_abiertos)),
                    ("Resueltos Hoy", str(resueltos_hoy)),
                    ("Tiempo Promedio", tiempo_promedio)
                ]
        except FileNotFoundError:
            stats = [
                ("Total Tickets", "0"),
                ("Tickets Abiertos", "0"),
                ("Resueltos Hoy", "0"),
                ("Tiempo Promedio", "0h")
            ]
        
        # Grid de estadísticas
        stats_layout = QHBoxLayout()
        for title, value in stats:
            card = self.create_stat_card(title, value)
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        self.content_widget.addWidget(dashboard)
    
    def create_stat_card(self, title, value):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['white']};
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {self.COLORS['text']};
            font-size: 16px;
        """)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {self.COLORS['accent']};
            font-size: 28px;
            font-weight: bold;
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.setAlignment(Qt.AlignCenter)
        
        return card

    def crear_ticket(self):
        from ticket_manager import crear_ticket_frame
        crear_ticket_frame(self.content_widget)

    def ver_historial(self):
        from ticket_manager import ver_historial_frame
        ver_historial_frame(self.content_widget)

    def generar_reportes(self):
        from report_generator import generar_reportes_frame
        generar_reportes_frame(self.content_widget)

    def salir(self):
        reply = QMessageBox.question(
            self, 'Salir',
            '¿Deseas salir de la aplicación?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()

    def mostrar_dashboard(self):
        # Set the current widget to index 0 (dashboard)
        self.content_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establecer estilo de la aplicación
    app.setStyle("Fusion")
    
    # Configurar fuente predeterminada
    app.setFont(QFont("Segoe UI", 10))
    
    window = ModernDashboard()
    window.show()
    sys.exit(app.exec_())
