import random
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

# Función para generar una tarjeta de bingo
def generar_tarjeta(dimension, espacio_vacio):
    numeros = random.sample(range(1, 100), dimension * dimension)  # Genera números únicos
    tarjeta = [numeros[i * dimension:(i + 1) * dimension] for i in range(dimension)]

    # Si el usuario quiere un espacio vacío y la dimensión es impar
    if espacio_vacio.lower() == 'sí' and dimension % 2 != 0:
        centro = dimension // 2
        tarjeta[centro][centro] = ' '

    return tarjeta

# Función para generar un archivo PDF individual con estilo mejorado
def generar_pdf_individual(tarjeta, dimension, jugador):
    # Crear la carpeta 'bingo' si no existe
    if not os.path.exists('bingo'):
        os.makedirs('bingo')

    archivo_pdf = f'bingo/jugador_{jugador}.pdf'
    pdf = canvas.Canvas(archivo_pdf, pagesize=letter)
    width, height = letter
    pdf.setFont("Helvetica-Bold", 36)

    # Dibujar la franja azul superior
    pdf.setFillColor(colors.blue)
    pdf.rect(0, height - 100, width, 100, fill=1)
    pdf.setFillColor(colors.white)
    pdf.drawCentredString(width / 2, height - 75, "BINGO")

    # Crear tabla para el cartón de bingo
    tabla_data = [[str(num) for num in fila] for fila in tarjeta]

    # Crear tabla con estilos estéticos
    tabla = Table(tabla_data, colWidths=[1.5 * inch] * dimension, rowHeights=[1.5 * inch] * dimension)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightyellow),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 28),
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Primera fila con fondo azul claro
    ]))

    # Centramos la tabla en la página
    table_width = dimension * 1.5 * inch
    table_height = dimension * 1.5 * inch
    x_offset = (width - table_width) / 2
    y_offset = (height - table_height) / 2 - 50  # Aseguramos espacio suficiente bajo la franja azul

    # Dibujar la tabla en el PDF
    tabla.wrapOn(pdf, width, height)
    tabla.drawOn(pdf, x_offset, y_offset)

    pdf.save()
    print(f"El archivo 'jugador_{jugador}.pdf' ha sido generado en la carpeta 'bingo'.")

# Función principal
def juego_bingo():
    # Preguntar al usuario por las dimensiones del bingo
    dimension_str = input("¿Cuáles son las dimensiones del bingo? (e.g., 3x3, 4x4, 5x5): ").strip()
    dimension = int(dimension_str.split('x')[0])

    # Preguntar si el bingo tendrá un espacio vacío
    espacio_vacio = input("¿El bingo tendrá un espacio vacío? (Respuestas válidas: sí o no): ").strip().lower()

    # Preguntar cuántos jugadores participarán
    num_jugadores = int(input("¿Cuántos jugadores participarán?: ").strip())

    # Generar las tarjetas para cada jugador
    for jugador in range(1, num_jugadores + 1):
        tarjeta = generar_tarjeta(dimension, espacio_vacio)
        generar_pdf_individual(tarjeta, dimension, jugador)

# Ejecutar el juego de bingo
juego_bingo()
