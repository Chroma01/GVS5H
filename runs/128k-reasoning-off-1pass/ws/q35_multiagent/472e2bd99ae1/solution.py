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

    # Sort all arrays in descending order
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Max-heap: we store negative values because Python's heapq is a min-heap
    # Store (-value, i, j, k)
    # Start with the largest possible triple (0, 0, 0)
    start_val = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    
    # Heap elements: (-value, i, j, k)
    heap = [(-start_val, 0, 0, 0)]
    
    # Visited set to avoid duplicates
    visited = set()
    visited.add((0, 0, 0))
    
    ans = 0
    
    # Extract the largest K values
    for _ in range(K):
        if not heap:
            break
            
        neg_val, i, j, k = heapq.heappop(heap)
        val = -neg_val
        ans = val
        
        # Generate neighbors: (i+1, j, k), (i, j+1, k), (i, j, k+1)
        neighbors = [
            (i + 1, j, k),
            (i, j + 1, k),
            (i, j, k + 1)
        ]
        
        for ni, nj, nk in neighbors:
            if ni < N and nj < N and nk < N:
                if (ni, nj, nk) not in visited:
                    visited.add((ni, nj, nk))
                    # Compute the value for this new triple
                    new_val = A[ni] * B[nj] + B[nj] * C[nk] + C[nk] * A[ni]
                    heapq.heappush(heap, (-new_val, ni, nj, nk))
    
    print(ans)

if __name__ == '__main__':
    solve()