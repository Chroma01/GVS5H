import sys
import heapq

def solve():
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))
    A.sort()
    B.sort()
    C.sort()
    
    # Pack indices into a single integer for visited set: i * N^2 + j * N + k
    N2 = N * N
    def pack(i, j, k):
        return (i * N + j) * N + k
    
    # Max-heap using negative values
    start_i, start_j, start_k = N-1, N-1, N-1
    val = A[start_i] * B[start_j] + B[start_j] * C[start_k] + C[start_k] * A[start_i]
    heap = [(-val, start_i, start_j, start_k)]
    visited = set()
    visited.add(pack(start_i, start_j, start_k))
    
    for _ in range(K):
        neg_v, i, j, k = heapq.heappop(heap)
        v = -neg_v
        if _ == K - 1:
            print(v)
            return
        
        # Neighbors: (i-1, j, k), (i, j-1, k), (i, j, k-1)
        if i > 0:
            ni = i - 1
            key = pack(ni, j, k)
            if key not in visited:
                visited.add(key)
                nv = A[ni] * B[j] + B[j] * C[k] + C[k] * A[ni]
                heapq.heappush(heap, (-nv, ni, j, k))
        if j > 0:
            nj = j - 1
            key = pack(i, nj, k)
            if key not in visited:
                visited.add(key)
                nv = A[i] * B[nj] + B[nj] * C[k] + C[k] * A[i]
                heapq.heappush(heap, (-nv, i, nj, k))
        if k > 0:
            nk = k - 1
            key = pack(i, j, nk)
            if key not in visited:
                visited.add(key)
                nv = A[i] * B[j] + B[j] * C[nk] + C[nk] * A[i]
                heapq.heappush(heap, (-nv, i, j, nk))

if __name__ == "__main__":
    solve()