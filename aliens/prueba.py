import heapq

def solve_borg_maze():
    input_data = """
2
6 5
#####
#A A#  
#   # A 
#S    #
#####
7 7
#####
# AAA#
#   A#
#   S   #
#   #
#AAAA#
#####
"""
    data = [line.strip('\n') for line in input_data.split('\n') if line.strip()]
    
    index = 0
    N = int(data[index])
    index += 1
    
    for case_num in range(N):
        x, y = map(int, data[index].split())
        index += 1
        
        maze = []
        aliens = []
        start = None
        
        for j in range(y):
            line = data[index][:x]  # Asegurar que no exceda el ancho
            index += 1
            row = list(line.ljust(x))  # Rellenar con espacios si es necesario
            maze.append(row)
            for i, char in enumerate(row):
                if char == 'A':
                    aliens.append((i, j))
                elif char == 'S':
                    start = (i, j)
        
        if not aliens:
            print(0)
            continue
        
        # Incluir el punto de inicio en los puntos importantes
        important_points = [start] + aliens
        num_points = len(important_points)
        
        # Matriz de adyacencia con distancias
        adj = [[0] * num_points for _ in range(num_points)]
        
        # Calcular distancias entre todos los pares de puntos
        for i in range(num_points):
            sx, sy = important_points[i]
            dist = [[-1 for _ in range(x)] for _ in range(y)]
            q = [(sx, sy)]
            dist[sy][sx] = 0
            
            for cx, cy in q:
                for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < x and 0 <= ny < y:
                        if maze[ny][nx] != '#' and dist[ny][nx] == -1:
                            dist[ny][nx] = dist[cy][cx] + 1
                            q.append((nx, ny))
            
            for j in range(num_points):
                tx, ty = important_points[j]
                adj[i][j] = dist[ty][tx] if dist[ty][tx] != -1 else 0
        
        # Algoritmo de Prim para MST
        total_cost = 0
        visited = set([0])  # Comenzar desde el punto S (índice 0)
        heap = []
        
        # Añadir todas las aristas desde el nodo 0
        for j in range(1, num_points):
            if adj[0][j] > 0:
                heapq.heappush(heap, (adj[0][j], j))
        
        while len(visited) < num_points and heap:
            cost, node = heapq.heappop(heap)
            if node not in visited:
                visited.add(node)
                total_cost += cost
                # Añadir nuevas aristas desde este nodo
                for j in range(num_points):
                    if j not in visited and adj[node][j] > 0:
                        heapq.heappush(heap, (adj[node][j], j))
        
        print(total_cost)

solve_borg_maze()