# Gomoku (5 en linea)
# Basado en mi codigo de Twixt pero adaptado para Go-moku

import os
import time
import copy
import numpy as np
import random

clear = lambda: os.system('cls')

# Variables globales
BOARD_SIZE = 15  # Tablero 15x15 para Gomoku
board = []
x_turns = []
o_turns = []

# Direcciones para verificar 5 en linea
DIRECTIONS = [
    (1, 0),   # Horizontal
    (0, 1),   # Vertical
    (1, 1),   # Diagonal principal
    (1, -1)   # Diagonal secundaria
]

benchmark = {
    'nodos_expandidos': 0,
    'profundidad_maxima': 0,
    'tiempo': 0,
    'ganador': '',
    'puntaje': 0
}

def random_player(state):
    return random.choice(state.get_valid_moves())

def greedy_player(state):
    player = state.player
    opponent = "O" if player == "X" else "X"
    valid_moves = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if state.board[y][x] == "."]

    best_move = None
    best_score = -1

    for move in valid_moves:
        temp_board = copy.deepcopy(state.board)
        temp_board[move[1]][move[0]] = player

        # Contar la mayor línea que se forma
        max_line = 0
        for dx, dy in DIRECTIONS:
            count, _ = count_line_length(temp_board, move[0], move[1], dx, dy, player)
            max_line = max(max_line, count)

        # Victoria inmediata => elegir ya
        if max_line >= 5:
            return move

        # Si es mejor que lo anterior, actualizar
        if max_line > best_score:
            best_score = max_line
            best_move = move

    return best_move

def worst_player(state):
    worst = float('inf')
    worst_move = None
    for move, child in state.children():
        score = child.combined_heuristic()
        if score < worst:
            worst = score
            worst_move = move
    return worst_move

def check_win(board, player_moves, player):    
    for x, y in player_moves:
        for dx, dy in DIRECTIONS:
            count = 1
            # Contar hacia una direccion
            for i in range(1, 5):
                nx, ny = x + i * dx, y + i * dy
                if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE) or board[ny][nx] != player:
                    break
                count += 1
            # Contar hacia la direccion opuesta
            for i in range(1, 5):
                nx, ny = x - i * dx, y - i * dy
                if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE) or board[ny][nx] != player:
                    break
                count += 1
            if count >= 5:
                return True
    return False

def count_line_length(board, x, y, dx, dy, player):
    #Cuenta la longitud de linea desde una posicion en una direccion
    count = 1
    spaces = 0
    
    # Contar hacia una direccion
    for i in range(1, 5):
        nx, ny = x + i * dx, y + i * dy
        if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
            break
        if board[ny][nx] == player:
            count += 1
        elif board[ny][nx] == '.':
            spaces += 1
        else:
            break
    
    # Contar hacia la direccion opuesta
    for i in range(1, 5):
        nx, ny = x - i * dx, y - i * dy
        if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
            break
        if board[ny][nx] == player:
            count += 1
        elif board[ny][nx] == '.':
            spaces += 1
        else:
            break
    
    return count, spaces

def find_winning_moves(board, player):
    #Encuentra movimientos que ganan inmediatamente
    winning_moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == '.':
                # Simula el movimiento
                board[y][x] = player
                # Verifica si gana
                player_moves = []
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if board[i][j] == player:
                            player_moves.append((j, i))
                
                if check_win(board, player_moves, player):
                    winning_moves.append((x, y))
                
                # Restaura el tablero
                board[y][x] = '.'
    
    return winning_moves

def find_blocking_moves(board, player):
    # Encuentra movimientos que bloquean amenazas del oponente
    opponent = "O" if player == "X" else "X"
    blocking_moves = []
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == '.':
                # Verifica si este movimiento bloquea una amenaza
                for dx, dy in DIRECTIONS:
                    # Busca amenazas del oponente en esta direccion
                    for i in range(-4, 5):
                        nx, ny = x + i * dx, y + i * dy
                        if (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and 
                            board[ny][nx] == opponent):
                            # Cuenta la linea del oponente
                            count, spaces = count_line_length(board, nx, ny, dx, dy, opponent)
                            if count >= 4 and spaces > 0:
                                # Verifica si nuestro movimiento esta en una posicion vacia de la amenaza
                                for j in range(-4, 5):
                                    mx, my = nx + j * dx, ny + j * dy
                                    if (0 <= mx < BOARD_SIZE and 0 <= my < BOARD_SIZE and 
                                        board[my][mx] == '.' and (mx, my) == (x, y)):
                                        blocking_moves.append((x, y))
                                        break
                            if (x, y) in blocking_moves:
                                break
                    if (x, y) in blocking_moves:
                        break
    
    return list(set(blocking_moves))  # Eliminar duplicados

def find_threatening_moves(board, player):
    #  Encuentra movimientos que crean amenazas (3 o 4 en linea) o al meos lo intenta XD
    threatening_moves = []
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == '.':
                # Simula el movimiento
                board[y][x] = player
                
                # Verifica amenazas en todas las direcciones
                max_threat = 0
                for dx, dy in DIRECTIONS:
                    count, spaces = count_line_length(board, x, y, dx, dy, player)
                    if count >= 3 and spaces > 0:
                        max_threat = max(max_threat, count)
                
                # Restaura el tablero
                board[y][x] = '.'
                
                if max_threat >= 3:
                    threatening_moves.append((x, y, max_threat))
    
    return threatening_moves

class GameState:
    def __init__(self, board, my_moves, enemy_moves, player, weights):
        self.board = copy.deepcopy(board)
        self.my_moves = my_moves.copy()
        self.enemy_moves = enemy_moves.copy()
        self.player = player
        self.weights = weights

    def winner_points(self):
        if check_win(self.board, self.my_moves, self.player):
            return 1
        elif check_win(self.board, self.enemy_moves, "O" if self.player == "X" else "X"):
            return -1
        return 0

    def get_valid_moves(self):
        valid_moves = set()
        directions = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                      (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                      (0, -2), (0, -1), (0, 1), (0, 2),
                      (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                      (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]

        pieces = self.my_moves + self.enemy_moves
        if not pieces:
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

        for x, y in pieces:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[ny][nx] == '.':
                    valid_moves.add((nx, ny))

        # Si casi no hay jugadas, permite explorar todo el tablero
        if len(valid_moves) < 10:
            for y in range(BOARD_SIZE):
                for x in range(BOARD_SIZE):
                    if self.board[y][x] == '.':
                        valid_moves.add((x, y))

        return list(valid_moves)
        
    # Esto hace que: La IA solo explore zonas cercanas a la acción.
    # Se reduzca drásticamente el número de nodos, mejorando velocidad.

    def make_move(self, move):
        self.my_moves.append(move)
        self.board[move[1]][move[0]] = self.player

    def children(self):
        options = self.get_valid_moves()
        opponent = "O" if self.player == "X" else "X"

        def priority(move):
            if move in find_winning_moves(self.board, self.player):
                return 0
            if move in find_winning_moves(self.board, opponent):
                return 1
            temp_board = copy.deepcopy(self.board)
            temp_board[move[1]][move[0]] = self.player
            for dx, dy in DIRECTIONS:
                count, _ = count_line_length(temp_board, move[0], move[1], dx, dy, self.player)
                if count >= 3:
                    return 2
            return 3

        options.sort(key=priority)
        children = []
        for option in options:
            child = copy.deepcopy(self)
            child.make_move(option)
            child.player = opponent
            child.my_moves, child.enemy_moves = child.enemy_moves, child.my_moves
            children.append((option, child))

        return children
        
    def is_terminal(self):
        return (len(self.get_valid_moves()) == 0 or 
                check_win(self.board, self.my_moves, self.player) or
                check_win(self.board, self.enemy_moves, "O" if self.player == "X" else "X"))

    def combined_heuristic(self):
        return combined_heuristic(self.board, self.my_moves, self.enemy_moves, self.player, self.weights)

def combined_heuristic(board, my_moves, enemy_moves, player, _, ): # estaba weights pero lo quite para pruebas con otra logica aqui
    opponent = "O" if player == "X" else "X"

    # 0- Victoria / derrota inmediata
    if check_win(board, my_moves, player):
        return 10000
    if check_win(board, enemy_moves, opponent):
        return -10000

    score = 0

    # 1- Amenazas propias
    threatening_moves = find_threatening_moves(board, player)
    fours = sum(1 for _, _, t in threatening_moves if t == 4)
    threes = sum(1 for _, _, t in threatening_moves if t == 3)
    twos = sum(1 for _, _, t in threatening_moves if t == 2)

    # 2- Valoracion si tiene 4 y penalizacion si el enemigo tiene 4
    if fours >= 2:
        score += 9000
    elif fours == 1:
        score += 1000
    score += threes * 200  # más valor a 3 seguidas
    score += twos * 80     # más valor a 2 seguidas

    # 3- Amenazas del rival
    opponent_threatening_moves = find_threatening_moves(board, opponent)
    opp_fours = sum(1 for _, _, t in opponent_threatening_moves if t == 4)
    opp_threes = sum(1 for _, _, t in opponent_threatening_moves if t == 3)
    opp_twos = sum(1 for _, _, t in opponent_threatening_moves if t == 2)

    # # 4- Doble amenaza
    if opp_fours >= 2:
        score -= 9000
    elif opp_fours == 1:
        score -= 5000
    score -= opp_threes * 500
    score -= opp_twos * 100

    # 6- Control del centro
    center_x, center_y = BOARD_SIZE // 2, BOARD_SIZE // 2
    for x, y in my_moves:
        dist = abs(x - center_x) + abs(y - center_y)
        score += (BOARD_SIZE - dist) * 5  # menos peso para no eclipsar cadenas

    return score

    # Esto hace que la IA: Prefiera jugadas con doble amenaza. (osea que se pueda ganar por varios lados evitanod jugar una esquina por ejemplo)
    # Bloquee al instante si el rival tiene doble amenaza.    

class MinimaxSolver:
    def __init__(self, player, weights, time_limit):
        self.player = player
        self.player_name = player
        self.weights = weights
        self.time_limit = time_limit
        self.start_time = None
        self.nodes = 0
        self.max_depth = 0
    
    def _timeout(self):
        return (time.time() - self.start_time) >= self.time_limit

    def solve(self, state):
        self.start_time = time.time()
        best_move = None
        depth = 1

        # Ganar inmediatamente si se puede
        winning_moves = find_winning_moves(state.board, self.player_name)
        if winning_moves:
            return winning_moves[0]

        # Bloquear inmediatamente si el rival puede ganar
        opponent = "O" if self.player_name == "X" else "X"
        blocking_moves = find_winning_moves(state.board, opponent)
        if blocking_moves:
            return blocking_moves[0]

        # Busqueda iterativa por profundidad
        while time.time() - self.start_time < self.time_limit:
            self.nodes = 0
            move, _ = self.__maximize(state, -np.inf, np.inf, depth)
            if time.time() - self.start_time < self.time_limit and move is not None:
                best_move = move
                self.max_depth = depth
            depth += 1

        # Si nunca encontro nada, juega al azar
        if best_move is None:
            valid_moves = state.get_valid_moves()
            if valid_moves:
                best_move = random.choice(valid_moves)

        benchmark['nodos_expandidos'] += self.nodes
        benchmark['profundidad_maxima'] = max(benchmark['profundidad_maxima'], self.max_depth)
        return best_move

    def __maximize(self, state, alpha, beta, depth):
        self.nodes += 1
        if self._timeout():
            return None, state.combined_heuristic()
        if state.is_terminal():
            return None, state.winner_points()
        
        if depth == 0:
            return None, state.combined_heuristic()
        
        max_child, max_utility = None, -np.inf

        for option, child in state.children():
            if self._timeout():
                break
            if child.player == self.player_name:
                _, utility = self.__maximize(child, alpha, beta, depth - 1)
            else:
                _, utility = self.__minimize(child, alpha, beta, depth - 1)

            if utility > max_utility:
                max_child, max_utility = option, utility

            if max_utility >= beta:
                break
            alpha = max(alpha, max_utility)

        return max_child, max_utility
    
    def __minimize(self, state, alpha, beta, depth):
        self.nodes += 1
        if self._timeout():
            return None, state.combined_heuristic()
        if state.is_terminal():
            return None, state.winner_points()
        
        if depth == 0:
            return None, state.combined_heuristic()
        
        min_child, min_utility = None, np.inf

        for option, child in state.children():
            if self._timeout():
                break
            if child.player == self.player_name:
                _, utility = self.__maximize(child, alpha, beta, depth - 1)
            else:
                _, utility = self.__minimize(child, alpha, beta, depth - 1)

            if utility < min_utility:
                min_child, min_utility = option, utility
            
            if min_utility <= alpha:
                break

            beta = min(beta, min_utility)

        return min_child, min_utility

def get_player_type(name):
    valid_types = ["humano", "ia", "random", "greedy", "worst"]
    while True:
        tipo = input(f"\nSelecciona tipo de jugador para {name} ({'/'.join(valid_types)}): ").strip().lower()
        if tipo in valid_types:
            return tipo
        print("Entrada invalida. invalida. Elige uno de:", ", ".join(valid_types))

def show_board():
    print("   " + " ".join([f"{i:2}" for i in range(1, BOARD_SIZE + 1)]))
    for i in range(len(board)):
        line = f"{i+1:2} "
        for cell in board[i]:
            line += " " + cell + " "
        print(line)
    print("\nTurno del jugador:", "X" if len(x_turns) <= len(o_turns) else "O")

def main():
    global board, x_turns, o_turns, benchmark
    
    # Inicializar tablero
    board = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    x_turns = []
    o_turns = []
    benchmark = {
        'nodos_expandidos': 0,
        'profundidad_maxima': 0,
        'tiempo': 0,
        'ganador': '',
        'puntaje': 0
    }
    
    # Configuracion de jugadores
    player_X_type = get_player_type("Jugador X")
    player_O_type = get_player_type("Jugador O")
    
    # Configuracion de IA MEJORADA
    weights = [3]  
    time_limit = 3  # segundos 
    
    clear()
    print("=" * 50)
    print("¡Bienvenido al juego de Gomoku!")
    print("=" * 50)
    print("\nInstrucciones:")
    print("- Conecta 5 fichas en linea para ganar")
    print("- Ingresa las coordenadas en formato 'x y' (ejemplo: 8 8)")
    print(f"- Las coordenadas van de 1 a {BOARD_SIZE}")
    print("=" * 50)
    input("\nPresiona Enter para comenzar...")
    clear()
    
    turn = 1
    
    while True:
        current_player = "X" if turn % 2 == 1 else "O"
        player_type = player_X_type if current_player == "X" else player_O_type
        is_ia = player_type != "humano"
        
        show_board()
        
        if is_ia:
            print(f"\nMaquina pensando ({current_player})...")
            state = GameState(
                    board, 
                    x_turns.copy() if current_player == "X" else o_turns.copy(),
                    o_turns.copy() if current_player == "X" else x_turns.copy(),
                    current_player, weights
                )        
            
            start_time = time.time()

            if player_type == "random":
                move = random_player(state)

            elif player_type == "greedy":
                move = greedy_player(state)

            elif player_type == "worst":
                move = worst_player(state)            
            else: # Minimax
                solver = MinimaxSolver(current_player, weights, time_limit)
                move = solver.solve(state)
                benchmark['nodos_expandidos'] += solver.nodes
                benchmark['profundidad_maxima'] = max(benchmark['profundidad_maxima'], solver.max_depth)

            elapsed = time.time() - start_time
            benchmark['tiempo'] += elapsed
            print(f"La maquina penso durante {elapsed:.2f} segundos")

        else:
            try:
                entrada = input(f"\nIngresa coordenadas para {current_player} (x y): ").split()
                if len(entrada) != 2:
                    print("Entrada invalida")
                    continue
                x, y = int(entrada[0]) - 1, int(entrada[1]) - 1
                if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE) or board[y][x] != ".":
                    print("Movimiento invalido.")
                    continue
                move = (x, y)
            except:
                print("Error en la entrada")
                continue
        
        # Realizar movimiento
        if current_player == "X":
            x_turns.append(move)
        else:
            o_turns.append(move)
        
        board[move[1]][move[0]] = current_player
        turn += 1
        
        # Verificar victoria
        if check_win(board, x_turns if current_player == "X" else o_turns, current_player):
            show_board()
            print(f"\n¡El jugador {current_player} ha ganado!")
            benchmark['ganador'] = current_player
            benchmark['puntaje'] = 1 if current_player == 'X' else -1
            break
        
        # Verificar empate
        if len(x_turns) + len(o_turns) >= BOARD_SIZE * BOARD_SIZE:
            show_board()
            print("\n¡Empate!")
            break
    
    print("\nResumen del benchmark:")
    print(f"Ganador: {benchmark['ganador']}")
    print(f"Puntaje: {benchmark['puntaje']}")
    print(f"Tiempo total pensando: {benchmark['tiempo']:.2f} segundos")
    print(f"Nodos expandidos: {benchmark['nodos_expandidos']}")
    print(f"Profundidad alcanzada: {benchmark['profundidad_maxima']}")

if __name__ == "__main__":
    main() 


# ==============================================
# Configuraciones de experimentos
# ==============================================
experimentos = [
    {"nombre": "pesos_1", "pesos": [1, 2, 3, 4, 5], "tiempo": 3},
    {"nombre": "pesos_2", "pesos": [5, 4, 3, 2, 1], "tiempo": 3},
    {"nombre": "heuristica_1", "pesos": [1, 0, 0, 0, 0], "tiempo": 3},
    {"nombre": "heuristica_2", "pesos": [1, 1, 0, 0, 0], "tiempo": 3},
    {"nombre": "heuristica_3", "pesos": [1, 1, 1, 0, 0], "tiempo": 3},
    {"nombre": "heuristica_4", "pesos": [1, 1, 1, 1, 0], "tiempo": 3},
    {"nombre": "heuristica_5", "pesos": [1, 1, 1, 1, 1], "tiempo": 3},
    {"nombre": "tiempo_1s", "pesos": [1, 1, 1, 1, 1], "tiempo": 1},
    {"nombre": "tiempo_3s", "pesos": [1, 1, 1, 1, 1], "tiempo": 3},
    {"nombre": "tiempo_10s", "pesos": [1, 1, 1, 1, 1], "tiempo": 10},
]

# Aunque al final termine haciendo los experimentos manualmente ya que esto me dio muchos errores 