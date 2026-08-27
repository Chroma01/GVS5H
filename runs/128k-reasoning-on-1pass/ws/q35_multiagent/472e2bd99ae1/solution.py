import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    N = int(next(iterator))
    K = int(next(iterator))
    
    A = [int(next(iterator)) for _ in range(N)]
    B = [int(next(iterator)) for _ in range(N)]
    C = [int(next(iterator)) for _ in range(N)]
    
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    heap = []
    init_val = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    heapq.heappush(heap, (-init_val, 0, 0, 0))
    
    for _ in range(K):
        val, i, j, k = heapq.heappop(heap)
        if _ == K - 1:
            print(-val)
            return
            
        if i + 1 < N:
            v = A[i+1]*B[j] + B[j]*C[k] + C[k]*A[i+1]
            heapq.heappush(heap, (-v, i+1, j, k))
            
        if i == 0 and j + 1 < N:
            v = A[0]*B[j+1] + B[j+1]*C[k] + C[k]*A[0]
            heapq.heappush(heap, (-v, 0, j+1, k))
            
        if i == 0 and j == 0 and k + 1 < N:
            v = A[0]*B[0] + B[0]*C[k+1] + C[k+1]*A[0]
            heapq.heappush(heap, (-v, 0, 0, k+1))

if __name__ == '__main__':
    solve()