import sys
import heapq

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        C = [int(next(iterator)) for _ in range(N)]
            
    except StopIteration:
        return

    # Sort arrays in descending order to ensure monotonicity
    # f(i, j, k) = A[i]*B[j] + B[j]*C[k] + C[k]*A[i]
    # Since A, B, C are sorted descending, increasing any index decreases or keeps the value same.
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Max-heap to store values. Python's heapq is a min-heap, so we store negative values.
    # We store tuples: (-value, i, j, k)
    pq = []
    
    # To avoid duplicates, we track visited states (i, j, k)
    visited = set()
    
    # Initial state: (0, 0, 0)
    val = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    heapq.heappush(pq, (-val, 0, 0, 0))
    visited.add((0, 0, 0))
    
    kth_largest = 0
    
    # Extract K times
    for _ in range(K):
        if not pq:
            break
            
        neg_val, i, j, k = heapq.heappop(pq)
        kth_largest = -neg_val
        
        # Try incrementing i
        if i + 1 < N:
            if (i + 1, j, k) not in visited:
                visited.add((i + 1, j, k))
                val_new = A[i+1] * B[j] + B[j] * C[k] + C[k] * A[i+1]
                heapq.heappush(pq, (-val_new, i + 1, j, k))
        
        # Try incrementing j
        if j + 1 < N:
            if (i, j + 1, k) not in visited:
                visited.add((i, j + 1, k))
                val_new = A[i] * B[j+1] + B[j+1] * C[k] + C[k] * A[i]
                heapq.heappush(pq, (-val_new, i, j + 1, k))
        
        # Try incrementing k
        if k + 1 < N:
            if (i, j, k + 1) not in visited:
                visited.add((i, j, k + 1))
                val_new = A[i] * B[j] + B[j] * C[k+1] + C[k+1] * A[i]
                heapq.heappush(pq, (-val_new, i, j, k + 1))

    print(kth_largest)

if __name__ == '__main__':
    solve()