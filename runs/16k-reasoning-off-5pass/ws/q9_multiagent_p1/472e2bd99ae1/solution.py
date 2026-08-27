import sys
import heapq

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
            
        C = []
        for _ in range(N):
            C.append(int(next(iterator)))
            
    except StopIteration:
        return

    # Sort arrays in descending order to ensure monotonicity.
    # The function f(i, j, k) = A[i]*B[j] + B[j]*C[k] + C[k]*A[i] is non-increasing
    # with respect to i, j, k when arrays are sorted descending (since values >= 1).
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # We need the K-th largest value.
    # We use a max-heap. Python's heapq is a min-heap, so we store negative values.
    # State: (value, i, j, k)
    # We start with the largest possible value at indices (0, 0, 0)
    
    # Initial value calculation
    # A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    current_val = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    
    # Max-heap using negative values
    heap = [(-current_val, 0, 0, 0)]
    
    # Visited set to avoid duplicates
    # Storing tuples (i, j, k)
    visited = set()
    visited.add((0, 0, 0))
    
    kth_largest = 0
    
    # We need to extract the largest K times
    for _ in range(K):
        if not heap:
            break
            
        neg_val, i, j, k = heapq.heappop(heap)
        val = -neg_val
        
        kth_largest = val
        
        # Generate neighbors: (i+1, j, k), (i, j+1, k), (i, j, k+1)
        # Since arrays are sorted descending, increasing indices decreases (or keeps same) the value.
        # We only push if indices are within bounds [0, N-1]
        
        # Neighbor 1: increment i
        if i + 1 < N:
            if (i + 1, j, k) not in visited:
                visited.add((i + 1, j, k))
                val_next = A[i+1] * B[j] + B[j] * C[k] + C[k] * A[i+1]
                heapq.heappush(heap, (-val_next, i + 1, j, k))
        
        # Neighbor 2: increment j
        if j + 1 < N:
            if (i, j + 1, k) not in visited:
                visited.add((i, j + 1, k))
                val_next = A[i] * B[j+1] + B[j+1] * C[k] + C[k] * A[i]
                heapq.heappush(heap, (-val_next, i, j + 1, k))
                
        # Neighbor 3: increment k
        if k + 1 < N:
            if (i, j, k + 1) not in visited:
                visited.add((i, j, k + 1))
                val_next = A[i] * B[j] + B[j] * C[k+1] + C[k+1] * A[i]
                heapq.heappush(heap, (-val_next, i, j, k + 1))
                
    print(kth_largest)

if __name__ == '__main__':
    solve()