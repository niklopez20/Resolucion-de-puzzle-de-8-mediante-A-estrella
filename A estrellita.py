import matplotlib.pyplot as plt
import numpy as np

# Definición de la clase Node para representar un nodo en el árbol de búsqueda
class Node:
    def __init__(self, estado, parent, move, depth, cost):
        self.estado = estado  # Estado actual del nodo
        self.parent = parent  # Nodo padre
        self.move = move  # Movimiento que lleva al estado actual desde el estado del nodo padre
        self.depth = depth  # Profundidad del nodo en el árbol de búsqueda
        self.cost = cost  # Costo acumulado hasta el nodo actual

    def __lt__(self, other):
        return self.cost < other.cost

# Función para generar los movimientos válidos a partir de un estado dado
def generar_movimientos(estado):
    movimientos = []  # Lista para almacenar los movimientos válidos
    i = estado.index(0)  # Índice de la casilla vacía (0)
    if i not in [0, 1, 2]:  # Si la casilla vacía no está en la fila superior, puede moverse hacia arriba
        movimientos.append(-3)  # Añade el movimiento hacia arriba
    if i not in [0, 3, 6]:  # Si la casilla vacía no está en la columna izquierda, puede moverse hacia la izquierda
        movimientos.append(-1)  # Añade el movimiento hacia la izquierda
    if i not in [2, 5, 8]:  # Si la casilla vacía no está en la columna derecha, puede moverse hacia la derecha
        movimientos.append(1)  # Añade el movimiento hacia la derecha
    if i not in [6, 7, 8]:  # Si la casilla vacía no está en la fila inferior, puede moverse hacia abajo
        movimientos.append(3)  # Añade el movimiento hacia abajo
    return movimientos

## Función para realizar un movimiento dado un estado y un paso
def move(estado, paso):
    new_estado = estado[:]  # Copia el estado actual
    i = new_estado.index(0)  # Índice de la casilla vacía (0)
    # Realiza el intercambio de la casilla vacía con la casilla adyacente según el paso dado
    new_estado[i], new_estado[i + paso] = new_estado[i + paso], new_estado[i]
    return new_estado

# Función para calcular la distancia de Manhattan entre dos estados
def distancia_de_manhattan(estado, estado_objetivo):
    distancia = 0
    for i in range(len(estado)):
        if estado[i] != 0:
            # Calcula la fila y la columna actual del número en el estado
            current_row, current_col = i // 3, i % 3
            # Obtiene la fila y la columna objetivo del número en el estado objetivo
            goal_row, goal_col = estado_objetivo.index(estado[i]) // 3, estado_objetivo.index(estado[i]) % 3
            # Calcula la distancia de Manhattan y la suma al total
            distancia += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distancia

# Función para graficar la solución del rompecabezas
def plot_solucioni(solucioni):
    fig, ax = plt.subplots()  # Crea una nueva figura y un conjunto de ejes

    ax.set_title('Solucion del puzzle de 8')  # Establece el título del gráfico

    # Itera sobre los pasos de la solución
    for i in range(len(solucioni)):
        ax.clear()  # Limpia el gráfico antes de dibujar el siguiente estado
        ax.set_title('Solucion del puzzle de 8')  # Establece el título del gráfico

        # Dibuja los cuadros de colores para representar el estado actual del rompecabezas
        ax.matshow(np.reshape(solucioni[i], (3, 3)), cmap='viridis')

        # Añade números dentro de cada cuadro de color para indicar el valor de cada casilla
        for (k, j), val in np.ndenumerate(np.reshape(solucioni[i], (3, 3))):
            ax.text(j, k, str(int(val)), ha='center', va='center', fontsize=20, color='white')

        plt.pause(0.5)  # Pausa la ejecución durante 0.5 segundos para mostrar cada paso de la solución

    plt.show()  # Muestra el gráfico final con la solución

# Función para resolver el rompecabezas de 8 utilizando el algoritmo A*
def resolver_estrellita(initial_estado, estado_objetivo):
    nodo_comienzo = Node(initial_estado, None, None, 0, 0)  # Crea el nodo inicial
    front = [nodo_comienzo]  # Crea una lista para almacenar los nodos en la frontera
    explorado = set()  # Conjunto para almacenar los estados explorados

    while front:  # Mientras haya nodos en la lista de la frontera
        front.sort()  # Ordena la lista de nodos en la frontera según el costo
        nodo_actual = front.pop(0)  # Extrae el primer nodo de la lista (menor costo)
        explorado.add(tuple(nodo_actual.estado))  # Agrega el estado del nodo actual al conjunto de explorados

        if nodo_actual.estado == estado_objetivo:  # Si el estado actual es el estado objetivo
            movimientos = []  # Lista para almacenar los movimientos de la solución
            while nodo_actual.parent is not None:  # Retrocede desde el nodo objetivo hasta el nodo inicial
                movimientos.append(nodo_actual.estado)  # Agrega el estado actual a la lista de movimientos
                nodo_actual = nodo_actual.parent  # Avanza al nodo padre
            movimientos.append(initial_estado)  # Agrega el estado inicial a la lista de movimientos
            movimientos.reverse()  # Invierte la lista de movimientos para obtener la solución
            return movimientos  # Devuelve la lista de movimientos de la solución

        for move_paso in generar_movimientos(nodo_actual.estado):  # Genera los movimientos válidos para el nodo actual
            siguiente_estado = move(nodo_actual.estado, move_paso)  # Calcula el estado siguiente
            if tuple(siguiente_estado) not in explorado:  # Si el estado siguiente no ha sido explorado previamente
                # Calcula el costo del nodo siguiente como la suma de la profundidad y la distancia de Manhattan
                siguiente_costo = nodo_actual.depth + 1 + distancia_de_manhattan(siguiente_estado, estado_objetivo)
                siguiente_nodo = Node(siguiente_estado, nodo_actual, move_paso, nodo_actual.depth + 1, siguiente_costo)  # Crea un nuevo nodo
                front.append(siguiente_nodo)  # Agrega el nuevo nodo a la lista de la frontera

    return None  # Si no se encuentra solución, devuelve None

# Función para solicitar al usuario los estados inicial y final del rompecabezas
def ingresar_estados():
    print("Ingrese el estado inicial del rompecabezas (números del 0 al 8, separados por espacios):")
    initial_estado = list(map(int, input().split()))  # Lee y convierte los números ingresados en una lista de enteros
    print("Ingrese el estado final del rompecabezas (números del 0 al 8, separados por espacios):")
    estado_objetivo = list(map(int, input().split()))  # Lee y convierte los números ingresados en una lista de enteros
    return initial_estado, estado_objetivo

# Obtener entrada del usuario para los estados inicial y final
initial_estado, estado_objetivo = ingresar_estados()

# Resolver el rompecabezas de 8 utilizando el algoritmo A*
solucioni_pasos = resolver_estrellita(initial_estado, estado_objetivo)

# Mostrar resultado
if solucioni_pasos:  # Si se encuentra una solución
    plot_solucioni(solucioni_pasos)  # Graficar la solución
    print(f"Se ha encontrado una solución utilizando el algoritmo A* (A-Estrellita).")  # Mostrar mensaje de éxito
else:
    print(f"No se ha encontrado solución utilizando el algoritmo A* (A-Estrellita).")  # Mostrar mensaje de fracaso
