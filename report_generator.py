# report_generator.py
import csv
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

def generar_reportes():
    categorias = []
    estados = []
    tiempos_resolucion = []
    
    try:
        with open('ticket_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                categorias.append(row['Categoría'])
                estados.append(row['Estado'])
                
                # Calculate resolution times for resolved tickets
                if row['Estado'] == 'Resuelto automáticamente':
                    fecha_creacion = datetime.strptime(row['FechaHora'], "%Y-%m-%d %H:%M:%S")
                    tiempos_resolucion.append(0)  # Instant for automatic resolution
                
        if not categorias:
            print("No hay datos para generar reporte.")
            return

        # Statistics
        conteo_cat = Counter(categorias)
        conteo_est = Counter(estados)
        
        # Print detailed report
        print("\n====== REPORTE DETALLADO DE TICKETS ======")
        print("\n=== Tickets por Categoría ===")
        for categoria, cantidad in conteo_cat.items():
            print(f"{categoria}: {cantidad} tickets")

        print("\n=== Estados de Tickets ===")
        for estado, cantidad in conteo_est.items():
            print(f"{estado}: {cantidad}")
            
        print("\n=== Estadísticas de Resolución ===")
        total_tickets = len(categorias)
        auto_resueltos = conteo_est['Resuelto automáticamente']
        derivados = conteo_est.get('Derivado a encargado', 0)
        
        print(f"Total de tickets: {total_tickets}")
        print(f"Resueltos automáticamente: {auto_resueltos} ({(auto_resueltos/total_tickets)*100:.1f}%)")
        print(f"Derivados: {derivados} ({(derivados/total_tickets)*100:.1f}%)")

        # Generate graphs
        plt.figure(figsize=(15, 5))
        
        # Categories plot
        plt.subplot(121)
        plt.bar(conteo_cat.keys(), conteo_cat.values(), color='skyblue')
        plt.title("Tickets por Categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Número de Tickets")
        plt.xticks(rotation=45)
        
        # Status plot
        plt.subplot(122)
        plt.pie(conteo_est.values(), labels=conteo_est.keys(), autopct='%1.1f%%')
        plt.title("Estado de Tickets")
        
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Archivo de tickets no encontrado.")
