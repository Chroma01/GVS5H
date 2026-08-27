import sys
import heapq

def main():
    input = sys.stdin.read().split()
    ptr = 0
    H = int(input[ptr]); ptr += 1
    W = int(input[ptr]); ptr += 1
    F = []
    for _ in range(H):
        row = list(map(int, input[ptr:ptr+W]))
        ptr += W
        F.append(row)
    Q = int(input[ptr]); ptr += 1
    queries = []
    for _ in range(Q):
        A = int(input[ptr]); B = int(input[ptr+1]); Y = int(input[ptr+2])
        C = int(input[ptr+3]); D = int(input[ptr+4]); Z = int(input[ptr+5])
        ptr += 6
        queries.append((A-1, B-1, Y, C-1, D-1, Z))
    
    # Dijkstra on the grid where the cost to move from (i,j) to (i',j') is max(0, F[i][j] - F[i'][j'])
    # This represents the minimum stair cost to adjust floors when moving between blocks.
    INF = float('inf')
    dist = [[INF] * W for _ in range(H)]
    for q in queries:
        a, b, y, c, d, z = q
        if dist[a][b] == INF:
            # Run Dijkstra from (a, b)
            heap = []
            heapq.heappush(heap, (0, a, b))
            dist[a][b] = 0
            while heap:
                cost, i, j = heapq.heappop(heap)
                if cost > dist[i][j]:
                    continue
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < H and 0 <= nj < W:
                        new_cost = cost + max(0, F[i][j] - F[ni][nj])
                        if new_cost < dist[ni][nj]:
                            dist[ni][nj] = new_cost
                            heapq.heappush(heap, (new_cost, ni, nj))
        # The answer is dist[c][d] + abs(y - z)
        print(dist[c][d] + abs(y - z))

if __name__ == "__main__":
    main()