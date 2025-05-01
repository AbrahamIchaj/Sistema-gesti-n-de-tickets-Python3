# report_generator.py
import csv
import matplotlib.pyplot as plt
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generar_reportes():
    try:
        with open('ticket_data.csv', mode='r') as file:
            tickets = list(csv.DictReader(file))
            
        if not tickets:
            messagebox.showinfo("Información", "No hay datos para generar reporte.")
            return
            
        # Define colors and fonts
        COLORS = {
            'bg': '#ecf0f1',
            'frame_bg': '#ffffff',
            'text': '#2c3e50'
        }
        FONT = ('Helvetica', 12)
        TITLE_FONT = ('Helvetica', 14, 'bold')
        
        # Create report window with style
        report_window = tk.Toplevel()
        report_window.title("Reportes de Tickets")
        report_window.geometry("1000x1000")
        report_window.configure(bg=COLORS['bg'])
        
        # Main container with style
        main_frame = ttk.Frame(report_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure style for frames
        style = ttk.Style()
        style.configure('Custom.TLabelframe', background=COLORS['frame_bg'])
        style.configure('Custom.TFrame', background=COLORS['frame_bg'])
        
        # Statistics frame with style
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", style='Custom.TLabelframe')
        stats_frame.pack(fill=tk.X, pady=5)
        
        # Create statistics labels
        conteo_cat = Counter(t['Categoría'] for t in tickets)
        conteo_est = Counter(t['Estado'] for t in tickets)
        conteo_pri = Counter(t['Prioridad'] for t in tickets)
        
        # Category distribution with styled labels
        label = ttk.Label(stats_frame, text="Distribución por Categoría:", font=TITLE_FONT)
        label.grid(row=0, column=0, sticky=tk.W)
        
        for i, (cat, cnt) in enumerate(conteo_cat.items(), 1):
            ttk.Label(
                stats_frame,
                text=f"{cat}: {cnt} tickets ({cnt/len(tickets):.1%})",
                font=FONT
            ).grid(row=i, column=0, sticky=tk.W)
        
        # Priority distribution with styled labels
        ttk.Label(
            stats_frame,
            text="\nDistribución por Prioridad:",
            font=TITLE_FONT
        ).grid(row=0, column=1, sticky=tk.W, padx=(20,0))
        
        for i, (pri, cnt) in enumerate(conteo_pri.items(), 1):
            ttk.Label(
                stats_frame,
                text=f"{pri}: {cnt} tickets",
                font=FONT
            ).grid(row=i, column=1, sticky=tk.W, padx=(20,0))
        
        # Charts container with style
        charts_container = ttk.Frame(main_frame, style='Custom.TFrame')
        charts_container.pack(fill=tk.BOTH, expand=True)
        
        # Category chart frame with style
        cat_frame = ttk.LabelFrame(
            charts_container,
            text="Distribución por Categoría",
            style='Custom.TLabelframe'
        )
        cat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create and embed category chart
        fig1 = plt.figure(figsize=(5, 4))
        ax1 = fig1.add_subplot(111)
        ax1.bar(conteo_cat.keys(), conteo_cat.values(), color='skyblue')
        ax1.set_title("Tickets por Categoría")
        ax1.set_xlabel("Categoría")
        ax1.set_ylabel("Número de Tickets")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=cat_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame for priority chart
        pri_frame = ttk.LabelFrame(
            charts_container,
            text="Distribución por Prioridad",
            style='Custom.TLabelframe'
        )
        pri_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create and embed priority chart
        fig2 = plt.figure(figsize=(5, 4))
        ax2 = fig2.add_subplot(111)
        
        # Ordenar por prioridad (Alta, Media, Baja)
        prioridades_orden = ['Alta', 'Media', 'Baja']
        conteo_pri_ordenado = {p: conteo_pri.get(p, 0) for p in prioridades_orden}
        
        colors = ['#ff7f7f', '#ffcc7f', '#7fcc7f']  # Rojo, Amarillo, Verde
        ax2.bar(conteo_pri_ordenado.keys(), conteo_pri_ordenado.values(), color=colors)
        ax2.set_title("Tickets por Prioridad")
        ax2.set_xlabel("Prioridad")
        ax2.set_ylabel("Número de Tickets")
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=pri_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame for pie chart
        pie_frame = ttk.LabelFrame(
            main_frame,
            text="Distribución Porcentual por Categoría",
            style='Custom.TLabelframe'
        )
        pie_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create and embed pie chart
        fig3 = plt.figure(figsize=(6, 4))
        ax3 = fig3.add_subplot(111)
        
        # Calculate percentages
        total = sum(conteo_cat.values())
        percentages = [f'{(count/total)*100:.1f}%' for count in conteo_cat.values()]
        
        # Create pie chart with percentages
        wedges, texts, autotexts = ax3.pie(
            conteo_cat.values(),
            labels=conteo_cat.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Pastel1.colors,
            wedgeprops=dict(width=0.4, edgecolor='w')
        )
        
        ax3.set_title("Distribución Porcentual por Categoría")
        plt.tight_layout()
        
        canvas3 = FigureCanvasTkAgg(fig3, master=pie_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Styled close button
        close_btn = ttk.Button(
            main_frame,
            text="Cerrar",
            command=report_window.destroy,
            style='Custom.TButton'
        )
        close_btn.pack(pady=10)
        
        # Configure button style
        style.configure(
            'Custom.TButton',
            font=FONT,
            background=COLORS['bg'],
            foreground=COLORS['text']
        )

    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de tickets no encontrado.")
