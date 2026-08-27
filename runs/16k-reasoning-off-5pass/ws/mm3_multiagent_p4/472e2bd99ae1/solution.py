import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    N_sq = N * N
    visited = set()
    # initial state (0,0,0)
    key0 = 0
    visited.add(key0)
    val0 = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    heap = [(-val0, key0)]
    heapq.heapify(heap)
    
    ans = None
    for _ in range(K):
        neg_val, key = heapq.heappop(heap)
        val = -neg_val
        ans = val
        
        # decode key to get i, j, k
        k = key % N
        temp = key // N
        j = temp % N
        i = temp // N
        
        # generate neighbors
        # neighbor 1: (i+1, j, k)
        if i + 1 < N:
            new_key = (i + 1) * N_sq + j * N + k
            if new_key not in visited:
                visited.add(new_key)
                new_val = A[i+1]*B[j] + B[j]*C[k] + C[k]*A[i+1]
                heapq.heappush(heap, (-new_val, new_key))
        # neighbor 2: (i, j+1, k)
        if j + 1 < N:
            new_key = i * N_sq + (j + 1) * N + k
            if new_key not in visited:
                visited.add(new_key)
                new_val = A[i]*B[j+1] + B[j+1]*C[k] + C[k]*A[i]
                heapq.heappush(heap, (-new_val, new_key))
        # neighbor 3: (i, j, k+1)
        if k + 1 < N:
            new_key = i * N_sq + j * N + (k + 1)
            if new_key not in visited:
                visited.add(new_key)
                new_val = A[i]*B[j] + B[j]*C[k+1] + C[k+1]*A[i]
                heapq.heappush(heap, (-new_val, new_key))
    
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()