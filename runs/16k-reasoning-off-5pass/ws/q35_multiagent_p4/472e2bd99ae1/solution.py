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

    # Function to compute the value for indices i, j, k
    def get_value(i, j, k):
        return A[i] * B[j] + B[j] * C[k] + C[k] * A[i]

    # Max-heap using negative values since heapq is a min-heap
    # Store tuples: (-value, i, j, k)
    heap = []
    
    # Visited set to avoid duplicates
    visited = set()
    
    # Initial state
    initial_val = get_value(0, 0, 0)
    heapq.heappush(heap, (-initial_val, 0, 0, 0))
    visited.add((0, 0, 0))
    
    ans = 0
    
    # Pop K times to find the K-th largest value
    for _ in range(K):
        neg_val, i, j, k = heapq.heappop(heap)
        ans = -neg_val
        
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
                val = get_value(ni, nj, nk)
                heapq.heappush(heap, (-val, ni, nj, nk))
                
    print(ans)

if __name__ == '__main__':
    solve()