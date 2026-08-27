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

    # Sort arrays in descending order to easily access largest elements
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Max-heap: store (-value, i, j, k) because Python's heapq is a min-heap
    # We negate the value to simulate max-heap behavior
    # Initial state: indices (0, 0, 0)
    # Value: A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    
    start_val = A[0] * B[0] + B[0] * C[0] + C[0] * A[0]
    
    # Heap stores tuples: (-value, i, j, k)
    heap = [(-start_val, 0, 0, 0)]
    
    # We need to extract the K-th largest element
    # Since we are using a max-heap (via negation), the first pop is the largest,
    # the second pop is the second largest, ..., the K-th pop is the K-th largest.
    
    ans = -1
    
    for _ in range(K):
        if not heap:
            break
            
        neg_val, i, j, k = heapq.heappop(heap)
        current_val = -neg_val
        ans = current_val
        
        # Generate neighbors based on the rule to avoid duplicates:
        # 1. (i+1, j, k) - always allowed if within bounds
        # 2. (i, j+1, k) - only allowed if i == 0
        # 3. (i, j, k+1) - only allowed if i == 0 and j == 0
        
        # Neighbor 1: (i+1, j, k)
        if i + 1 < N:
            ni, nj, nk = i + 1, j, k
            val = A[ni] * B[nj] + B[nj] * C[nk] + C[nk] * A[ni]
            heapq.heappush(heap, (-val, ni, nj, nk))
            
        # Neighbor 2: (i, j+1, k)
        if i == 0 and j + 1 < N:
            ni, nj, nk = i, j + 1, k
            val = A[ni] * B[nj] + B[nj] * C[nk] + C[nk] * A[ni]
            heapq.heappush(heap, (-val, ni, nj, nk))
            
        # Neighbor 3: (i, j, k+1)
        if i == 0 and j == 0 and k + 1 < N:
            ni, nj, nk = i, j, k + 1
            val = A[ni] * B[nj] + B[nj] * C[nk] + C[nk] * A[ni]
            heapq.heappush(heap, (-val, ni, nj, nk))
            
    print(ans)

if __name__ == '__main__':
    solve()