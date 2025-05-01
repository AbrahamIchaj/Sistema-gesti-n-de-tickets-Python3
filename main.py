import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os

class ModernDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Tickets")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configurar tema y colores
        self.COLORS = {
            'primary': '#000000',
            'secondary': '#34495e',
            'accent': '#3498db',
            'bg': '#ffffff',
            'text': '#2c3e50',
            'white': '#ffffff'
        }
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Sidebar.TFrame', background=self.COLORS['primary'])
        self.style.configure('Content.TFrame', background=self.COLORS['bg'])
        self.style.configure('Dashboard.TLabel',
                           background=self.COLORS['primary'],
                           foreground=self.COLORS['white'],
                           font=('Helvetica', 12))
        
        self.create_widgets()

    def create_widgets(self):
        # Container principal
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo en sidebar
        try:
            logo = Image.open("assets/logo.png")
            logo = logo.resize((200, 200))
            logo_tk = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.sidebar, image=logo_tk, bg=self.COLORS['primary'])
            logo_label.image = logo_tk
            logo_label.pack(pady=20)
        except:
            # Fallback si no encuentra el logo
            ttk.Label(self.sidebar, text="Sistema de Tickets", 
                     style='Dashboard.TLabel').pack(pady=20)

        # Botones del sidebar
        self.create_sidebar_button("Nuevo Ticket", self.crear_ticket, "icon_ticket.png")
        self.create_sidebar_button("Ver Historial", self.ver_historial, "icon_report.png")
        self.create_sidebar_button("Reportes", self.generar_reportes, "icon_exit.png")
        
        # Botón salir
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill='x', pady=10)
        self.create_sidebar_button("Salir", self.salir, None, True)
        
        # Contenido principal
        self.content = ttk.Frame(self.main_container, style='Content.TFrame')
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.current_content = None
    
    def clear_content(self):
        # Clear current content
        if self.content:
            for widget in self.content.winfo_children():
                widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        # Dashboard header
        header = ttk.Frame(self.content, style='Content.TFrame')
        header.pack(fill=tk.X, padx=20, pady=20)
        ttk.Label(header, 
                 text="Dashboard de Gestión de Tickets",
                 font=('Helvetica', 24),
                 background=self.COLORS['bg']).pack(side=tk.LEFT)
        
        # Grid de estadísticas
        self.create_stats_grid()

    def crear_ticket(self):
        self.clear_content()
        from ticket_manager import crear_ticket_frame
        crear_ticket_frame(self.content)

    def ver_historial(self):
        self.clear_content()
        from ticket_manager import ver_historial_frame
        ver_historial_frame(self.content)

    def generar_reportes(self):
        self.clear_content()
        from report_generator import generar_reportes_frame
        generar_reportes_frame(self.content)

    def create_sidebar_button(self, text, command, icon_path, is_exit=False):
        btn_frame = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        try:
            if icon_path:
                icon = Image.open(f"assets/{icon_path}")
                icon = icon.resize((24, 24))
                icon_tk = ImageTk.PhotoImage(icon)
                icon_label = tk.Label(btn_frame, image=icon_tk, bg=self.COLORS['primary'])
                icon_label.image = icon_tk
                icon_label.pack(side=tk.LEFT, padx=10)
        except:
            pass

        btn = tk.Button(btn_frame,
                       text=text,
                       command=command,
                       font=('Helvetica', 11),
                       bd=0,
                       bg=self.COLORS['primary'] if not is_exit else '#e74c3c',
                       fg=self.COLORS['white'],
                       activebackground=self.COLORS['secondary'] if not is_exit else '#c0392b',
                       activeforeground=self.COLORS['white'],
                       cursor='hand2',
                       width=20,
                       height=2)
        btn.pack(fill=tk.X, padx=5)

    def create_stats_grid(self):
        stats_frame = ttk.Frame(self.content, style='Content.TFrame')
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid
        for i in range(2):
            stats_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            stats_frame.grid_rowconfigure(i, weight=1)
        
        # Crear tarjetas de estadísticas
        self.create_stat_card(stats_frame, "Total Tickets", "0", 0, 0)
        self.create_stat_card(stats_frame, "Tickets Abiertos", "0", 0, 1)
        self.create_stat_card(stats_frame, "Resueltos Hoy", "0", 1, 0)
        self.create_stat_card(stats_frame, "Tiempo Promedio", "0h", 1, 1)

    def create_stat_card(self, parent, title, value, row, col):
        card = ttk.Frame(parent)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configurar estilo de la tarjeta
        card_style = ttk.Frame(card, style='Content.TFrame')
        card_style.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner_frame = tk.Frame(card_style, bg=self.COLORS['white'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        ttk.Label(inner_frame,
                 text=title,
                 font=('Helvetica', 14),
                 background=self.COLORS['white']).pack(pady=(20,5))
        
        ttk.Label(inner_frame,
                 text=value,
                 font=('Helvetica', 24, 'bold'),
                 background=self.COLORS['white']).pack(pady=(5,20))

    def crear_ticket(self):
        from ticket_manager import crear_ticket
        crear_ticket()

    def ver_historial(self):
        from ticket_manager import ver_historial
        ver_historial()

    def generar_reportes(self):
        from report_generator import generar_reportes
        generar_reportes()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir de la aplicación?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDashboard(root)
    root.mainloop()
