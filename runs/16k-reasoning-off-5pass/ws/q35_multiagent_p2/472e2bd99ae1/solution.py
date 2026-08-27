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
    def get_val(i, j, k):
        return A[i] * B[j] + B[j] * C[k] + C[k] * A[i]

    # Max-heap: store (-value, i, j, k) because heapq is a min-heap
    # We want to extract the largest value, so we store negative values.
    heap = []
    
    # Visited set to avoid processing the same triplet multiple times
    visited = set()
    
    # Initial state: indices (0, 0, 0)
    # Since arrays are sorted descending, this is the maximum possible value.
    start_val = get_val(0, 0, 0)
    heapq.heappush(heap, (-start_val, 0, 0, 0))
    visited.add((0, 0, 0))
    
    ans = 0
    
    # Extract the K-th largest element
    for _ in range(K):
        neg_val, i, j, k = heapq.heappop(heap)
        ans = -neg_val
        
        # Generate neighbors: increment one index at a time
        # Neighbor 1: (i+1, j, k)
        if i + 1 < N:
            if (i + 1, j, k) not in visited:
                visited.add((i + 1, j, k))
                val = get_val(i + 1, j, k)
                heapq.heappush(heap, (-val, i + 1, j, k))
        
        # Neighbor 2: (i, j+1, k)
        if j + 1 < N:
            if (i, j + 1, k) not in visited:
                visited.add((i, j + 1, k))
                val = get_val(i, j + 1, k)
                heapq.heappush(heap, (-val, i, j + 1, k))
                
        # Neighbor 3: (i, j, k+1)
        if k + 1 < N:
            if (i, j, k + 1) not in visited:
                visited.add((i, j, k + 1))
                val = get_val(i, j, k + 1)
                heapq.heappush(heap, (-val, i, j, k + 1))
                
    print(ans)

if __name__ == '__main__':
    solve()