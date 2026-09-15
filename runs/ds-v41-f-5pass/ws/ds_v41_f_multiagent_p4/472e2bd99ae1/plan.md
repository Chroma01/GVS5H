```python
import sys
import heapq

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]
    
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    def f(i, j, k):
        return A[i]*B[j] + B[j]*C[k] + C[k]*A[i]
    
    heap = []
    val0 = f(0, 0, 0)
    heapq.heappush(heap, (-val0, 0, 0, 0))
    visited = set()
    visited.add(0)  # code for (0,0,0)
    
    N2 = N * N
    for pop_cnt in range(K):
        neg_val, i, j, k = heapq.heappop(heap)
        if pop_cnt == K - 1:
            print(-neg_val)
            return
        
        # neighbor i+1
        if i + 1 < N:
            ni, nj, nk = i + 1, j, k
            code = ni * N2 + nj * N + nk
            if code not in visited:
                visited.add(code)
                val = A[ni]*B[nj] + B[nj]*C[nk] + C[nk]*A[ni]
                heapq.heappush(heap, (-val, ni, nj, nk))
        # neighbor j+1
        if j + 1 < N:
            ni, nj, nk = i, j + 1, k
            code = ni * N2 + nj * N + nk
            if code not in visited:
                visited.add(code)
                val = A[ni]*B[nj] + B[nj]*C[nk] + C[nk]*A[ni]
                heapq.heappush(heap, (-val, ni, nj, nk))
        # neighbor k+1
        if k + 1 < N:
            ni, nj, nk = i, j, k + 1
            code = ni * N2 + nj * N + nk
            if code not in visited:
                visited.add(code)
                val = A[ni]*B[nj] + B[nj]*C[nk] + C[nk]*A[ni]
                heapq.heappush(heap, (-val, ni, nj, nk))

if __name__ == "__main__":
    solve()
```