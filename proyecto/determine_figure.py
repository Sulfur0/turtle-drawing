import re

from utils import LoggerManager
logger = LoggerManager().getLogger()

def determine_figure(description):
    # parámetro que deberá ser pasado a esta función luego de inicializar la ventana de turtle
    window_size = (30, 30)
    # Definir los patrones para buscar palabras clave en la descripción
    patterns = {
        "figure": r"(square|rectangle|triangle|circle)",
        "dimensions": r"(\d+)\s*by\s*(\d+)|(\d+)\s*x\s*(\d+)|(\d+)\s*",
        "position": r"(centered)|(upper|lower)\s*(left|right|center)?\s*(corner)?"
    }

    # Inicializar variables para almacenar la figura, dimensiones y posición
    figure = None
    dimensions = None
    position = None
    center_of_figure = None

    # Buscar palabras clave en la descripción
    for key, pattern in patterns.items():
        match = re.search(pattern, description)
        if match:
            if key == "figure":
                figure = match.group(1)
            elif key == "dimensions":
                dimensions = [int(num) for num in match.groups() if num]
                logger.info(f'Dimensions: {dimensions}')
            elif key == "position":
                # print("encontrada posicion", match.group(0))
                if(match.group(0) == "centered" and (figure == "square" or figure == "rectangle")):
                    position = match.group(0)
                    i,j = window_size
                    center_of_figure = (int(i/2),int(j/2))

    # Calcular los vértices de la figura
    if figure and dimensions and position:
        vertices = calculate_vertices(figure, dimensions, position, center_of_figure)
        return vertices, dimensions
    else:
        return None

def calculate_vertices(figure, dimensions, position, center_of_figure):
    # Calcular los vértices según la figura, dimensiones y posición
    vertices = []
    if figure == "square" or figure == "rectangle":
        width, height = dimensions
        if "upper" in position:
            y = 0
        else:
            y = height
        if "left" in position:
            x = 0
        elif "right" in position:
            x = width
        elif "centered" in position and center_of_figure != None:
            i, j = center_of_figure 
            x = i - int(width / 2 )
            y = j - int(height / 2 )
        else:
            x = width // 2
        vertices.append((x, y))
        vertices.append((x, y + height))
        vertices.append((x + width, y + height)) 
        vertices.append((x + width, y))
        vertices.append((x, y))
    # agregar casos para otras figuras como triángulos, círculos, etc.
    return vertices

# Testing:

# Ejemplos de descripciones
descriptions = [
    # "square 300x300 upper left",
    # "square 200x200 upper left corner",
    # "rectangle 50x300 upper left corner"
    # "rectangle 50x300 centered"
    "square 10x10 centered",
]

# Procesar cada descripción e imprimir los vértices
# for description in descriptions:
#     vertices = determine_figure(description)
#     print(vertices)
