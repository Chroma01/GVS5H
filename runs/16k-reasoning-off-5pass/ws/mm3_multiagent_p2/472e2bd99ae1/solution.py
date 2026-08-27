import sys
import heapq

def solve():
    import sys
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    # Max-heap using negative values
    # Start with the maximum element (0,0,0)
    start_val = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    heap = [(-start_val, 0, 0, 0)]
    
    # Visited set using integer encoding to save memory
    # key = i * N * N + j * N + k
    NN = N * N
    visited = set()
    visited.add(0)
    
    ans = 0
    for _ in range(K):
        neg_val, i, j, k = heapq.heappop(heap)
        ans = -neg_val
        # Push neighbors: (i+1, j, k), (i, j+1, k), (i, j, k+1)
        ni = i + 1
        if ni < N:
            key = ni * NN + j * N + k
            if key not in visited:
                val = A[ni] * B[j] + B[j] * C[k] + C[k] * A[ni]
                heapq.heappush(heap, (-val, ni, j, k))
                visited.add(key)
        nj = j + 1
        if nj < N:
            key = i * NN + nj * N + k
            if key not in visited:
                val = A[i] * B[nj] + B[nj] * C[k] + C[k] * A[i]
                heapq.heappush(heap, (-val, i, nj, k))
                visited.add(key)
        nk = k + 1
        if nk < N:
            key = i * NN + j * N + nk
            if key not in visited:
                val = A[i] * B[j] + B[j] * C[nk] + C[nk] * A[i]
                heapq.heappush(heap, (-val, i, j, nk))
                visited.add(key)
    
    print(ans)

if __name__ == "__main__":
    solve()