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

    # Sort arrays in descending order to easily access largest elements
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Function to compute the value for indices i, j, k
    def get_val(i, j, k):
        return A[i] * B[j] + B[j] * C[k] + C[k] * A[i]

    # Max-heap: store (-value, i, j, k) because Python's heapq is a min-heap
    # We want to extract the largest value, so we store negative values.
    heap = []
    
    # Initial state: (0, 0, 0)
    # Push the largest possible value
    initial_val = get_val(0, 0, 0)
    heapq.heappush(heap, (-initial_val, 0, 0, 0))
    
    # Visited set to avoid duplicates? 
    # Actually, the generation strategy below ensures each state is pushed exactly once.
    # So we don't need a visited set if we follow the rules strictly.
    # Rules:
    # From (i, j, k):
    # 1. Always push (i+1, j, k) if i+1 < N
    # 2. If i == 0, push (i, j+1, k) if j+1 < N
    # 3. If i == 0 and j == 0, push (i, j, k+1) if k+1 < N
    
    ans = 0
    
    for _ in range(K):
        if not heap:
            break
            
        neg_val, i, j, k = heapq.heappop(heap)
        val = -neg_val
        ans = val
        
        # Generate next states
        # 1. Move in A dimension
        if i + 1 < N:
            new_val = get_val(i + 1, j, k)
            heapq.heappush(heap, (-new_val, i + 1, j, k))
            
        # 2. Move in B dimension, only if we are at the start of A dimension for this block
        if i == 0 and j + 1 < N:
            new_val = get_val(i, j + 1, k)
            heapq.heappush(heap, (-new_val, i, j + 1, k))
            
        # 3. Move in C dimension, only if we are at the start of A and B dimensions
        if i == 0 and j == 0 and k + 1 < N:
            new_val = get_val(i, j, k + 1)
            heapq.heappush(heap, (-new_val, i, j, k + 1))
            
    print(ans)

if __name__ == '__main__':
    solve()