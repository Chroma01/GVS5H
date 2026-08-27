import sys
import heapq

def solve():
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    NN = N * N
    visited = set()
    heap = []
    
    def f(i, j, k):
        return A[i] * B[j] + B[j] * C[k] + C[k] * A[i]
    
    start_val = f(0, 0, 0)
    heapq.heappush(heap, (-start_val, 0, 0, 0))
    visited.add(0)
    
    for _ in range(K):
        neg_val, i, j, k = heapq.heappop(heap)
        val = -neg_val
        if _ == K - 1:
            print(val)
            return
        
        # Neighbor (i+1, j, k)
        ni = i + 1
        if ni < N:
            key = ni * NN + j * N + k
            if key not in visited:
                v = f(ni, j, k)
                heapq.heappush(heap, (-v, ni, j, k))
                visited.add(key)
        
        # Neighbor (i, j+1, k)
        nj = j + 1
        if nj < N:
            key = i * NN + nj * N + k
            if key not in visited:
                v = f(i, nj, k)
                heapq.heappush(heap, (-v, i, nj, k))
                visited.add(key)
        
        # Neighbor (i, j, k+1)
        nk = k + 1
        if nk < N:
            key = i * NN + j * N + nk
            if key not in visited:
                v = f(i, j, nk)
                heapq.heappush(heap, (-v, i, j, nk))
                visited.add(key)

solve()