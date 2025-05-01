# utils/file_handler.py
import csv
import os

def guardar_ticket(ticket):
    file_exists = os.path.exists('ticket_data.csv')
    
    fieldnames = [
        "Nombre", "Categoría", "Descripción", "FechaHora",
        "Prioridad", "Estado", "Solución", "Requiere_Profesional"
    ]
    
    with open('ticket_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(ticket)
