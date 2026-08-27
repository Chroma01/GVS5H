import sys
import heapq

def solve():
    # Read all input from stdin
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

    # Sort arrays in descending order to prioritize larger values
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Max-heap using negative values since Python has min-heap
    # Store tuples: (-value, i, j, k)
    # Using 0-based indexing for arrays
    
    # Initial state: (0, 0, 0)
    # Value = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    
    start_val = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    
    heap = []
    heapq.heappush(heap, (-start_val, 0, 0, 0))
    
    visited = set()
    visited.add((0, 0, 0))
    
    ans = 0
    
    for _ in range(K):
        if not heap:
            break
            
        neg_val, i, j, k = heapq.heappop(heap)
        val = -neg_val
        ans = val
        
        # Generate neighbors: (i+1, j, k), (i, j+1, k), (i, j, k+1)
        neighbors = []
        if i + 1 < N:
            neighbors.append((i + 1, j, k))
        if j + 1 < N:
            neighbors.append((i, j + 1, k))
        if k + 1 < N:
            neighbors.append((i, j, k + 1))
            
        for ni, nj, nk in neighbors:
            if (ni, nj, nk) not in visited:
                visited.add((ni, nj, nk))
                n_val = A[ni] * B[nj] + B[nj] * C[nk] + C[nk] * A[ni]
                heapq.heappush(heap, (-n_val, ni, nj, nk))
                
    print(ans)

if __name__ == '__main__':
    solve()