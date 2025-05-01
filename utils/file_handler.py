# utils/file_handler.py
import csv
import os

def guardar_ticket(ticket):
    existe = os.path.isfile('ticket_data.csv')
    with open('ticket_data.csv', mode='a', newline='') as file:
        fieldnames = ["Nombre", "Categoría", "Descripción", "FechaHora", "Prioridad", "Estado", "Solución"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not existe:
            writer.writeheader()

        writer.writerow(ticket)
