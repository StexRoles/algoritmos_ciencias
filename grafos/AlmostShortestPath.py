import heapq

def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    inf = float('inf')
    
    while True:
        N, M = int(input[ptr]), int(input[ptr+1])
        ptr +=2
        if N ==0 and M ==0:
            break
        S = int(input[ptr])
        D = int(input[ptr+1])
        ptr +=2
        
        # Inicializar grafos
        graph = [[] for _ in range(N)]
        reverse_graph = [[] for _ in range(N)]
        edges = []
        for _ in range(M):
            u = int(input[ptr])
            v = int(input[ptr+1])
            p = int(input[ptr+2])
            ptr +=3
            graph[u].append( (v, p) )
            reverse_graph[v].append( (u, p) )
            edges.append( (u, v, p) )
        
        # Dijkstra desde S en grafo original
        def dijkstra(g, start, n):
            dist = [inf] * n
            dist[start] = 0
            heap = [ (0, start) ]
            heapq.heapify(heap)
            while heap:
                current_dist, u = heapq.heappop(heap)
                if current_dist > dist[u]:
                    continue
                for v, p in g[u]:
                    if dist[v] > dist[u] + p:
                        dist[v] = dist[u] + p
                        heapq.heappush(heap, (dist[v], v))
            return dist
        
        dist_S = dijkstra(graph, S, N)
        if dist_S[D] == inf:
            print(-1)
            continue
        
        # Dijkstra desde D en grafo invertido (distancia de cualquier nodo a D)
        dist_D = dijkstra(reverse_graph, D, N)
        
        # Filtrar aristas prohibidas
        forbidden = set()
        min_dist = dist_S[D]
        for u, v, p in edges:
            if dist_S[u] + p + dist_D[v] == min_dist:
                forbidden.add( (u, v, p) )
        
        # Construir nuevo grafo sin aristas prohibidas
        new_graph = [[] for _ in range(N)]
        for u, v, p in edges:
            if (u, v, p) not in forbidden:
                new_graph[u].append( (v, p) )
        
        # Dijkstra en nuevo grafo
        new_dist = dijkstra(new_graph, S, N)
        if new_dist[D] == inf:
            print(-1)
        else:
            print(new_dist[D])

if __name__ == "__main__":
    main()