import pygame

# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
ROJO = (255, 0, 0)

# Establecemos el LARGO y ALTO de cada celda de la retícula.
LARGO  = 20
ALTO = 20

# Establecemos el margen entre las celdas.
MARGEN =5

# Creamos un array bidimensional. Un array bidimensional
# no es más que una lista de listas.
grid = []
for fila in range(10):
    # Añadimos un array vacío que contendrá cada celda 
    # en esta fila
    grid.append([])
    for columna in range(10):
        grid[fila].append(0) # Añade una celda

# Establecemos la fila 1, celda 5 a uno. (Recuerda, los números de las filas y
# columnas empiezan en cero.)
grid[1][5] = 1
grid[1][1] = 1

# Inicializamos pygame
pygame.init()

# Establecemos el LARGO y ALTO de la pantalla
DIMENSION_VENTANA = [255, 255]
pantalla = pygame.display.set_mode(DIMENSION_VENTANA)

# Establecemos el título de la pantalla.
pygame.display.set_caption("Retículas y Matrices")

# Iteramos hasta que el usuario pulse el botón de salir.
hecho = False

# Lo usamos para establecer cuán rápido de refresca la pantalla.
reloj = pygame.time.Clock()

# -------- Bucle Principal del Programa-----------
while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # El usuario presiona el ratón. Obtiene su posición.
            pos = pygame.mouse.get_pos()
            # Cambia las coordenadas x/y de la pantalla por coordenadas reticulares
            columna = pos[0] // (LARGO + MARGEN)
            fila = pos[1] // (ALTO + MARGEN)
            # Establece esa ubicación a cero
            grid[fila][columna] = 1
            print("Click ", pos, "Coordenadas de la retícula: ", fila, columna)

    # Establecemos el fondo de pantalla.
    pantalla.fill(NEGRO)

    # Dibujamos la retícula
    for fila in range(10):
        for columna in range(10):
            color = BLANCO
            if grid[fila][columna] == 1:
                color = VERDE
            pygame.draw.rect(pantalla,
                             color,
                             [(MARGEN+LARGO) * columna + MARGEN,
                              (MARGEN+ALTO) * fila + MARGEN,
                              LARGO,
                              ALTO])

    # Limitamos a 60 fotogramas por segundo.
    reloj.tick(60)

    # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()

# Pórtate bien con el IDLE.
pygame.quit()
