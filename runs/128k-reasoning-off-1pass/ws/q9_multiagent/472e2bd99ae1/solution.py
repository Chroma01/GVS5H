import sys
import heapq

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

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

    # Sort A, B, C in descending order
    # We will access them as A[0] is the largest, etc.
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # We need to find the K-th largest value among N^3 combinations.
    # The combinations are A[i]*B[j] + B[j]*C[k] + C[k]*A[i].
    # For a fixed j, the values A[i]*B[j] + B[j]*C[k] + C[k]*A[i] form a matrix M_j indexed by (i, k).
    # Since A and C are sorted descending and all elements are positive, M_j is sorted in both dimensions
    # (monotonically decreasing).
    # We want the K-th largest value across all N such matrices.
    
    # We can use a priority queue (max-heap) to extract the largest values one by one.
    # State in heap: (-value, j, i, k)
    # We start with the largest element from each matrix M_j, which is at (i=0, k=0).
    # To avoid duplicates, we track visited states (j, i, k).
    
    pq = []
    visited = set()
    
    # Add the top element (0,0) for each j
    # Note: If N is very large, this loop is O(N).
    # Given N <= 2*10^5, this is acceptable.
    for j in range(N):
        # Calculate value for A[0], B[j], C[0]
        val = A[0] * B[j] + B[j] * C[0] + C[0] * A[0]
        # State: (j, 0, 0)
        state = (j, 0, 0)
        if state not in visited:
            visited.add(state)
            heapq.heappush(pq, (-val, j, 0, 0))
            
    # Extract K times
    ans = 0
    count = 0
    
    while pq and count < K:
        neg_val, j, i, k = heapq.heappop(pq)
        val = -neg_val
        ans = val
        count += 1
        
        # Generate neighbors
        # Neighbors are (i-1, k) and (i, k-1)
        # We use the visited set to avoid duplicates.
        
        # Check (i-1, k)
        if i > 0:
            state_up = (j, i-1, k)
            if state_up not in visited:
                visited.add(state_up)
                # Calculate value
                v_up = A[i-1] * B[j] + B[j] * C[k] + C[k] * A[i-1]
                heapq.heappush(pq, (-v_up, j, i-1, k))
                
        # Check (i, k-1)
        if k > 0:
            state_left = (j, i, k-1)
            if state_left not in visited:
                visited.add(state_left)
                # Calculate value
                v_left = A[i] * B[j] + B[j] * C[k-1] + C[k-1] * A[i]
                heapq.heappush(pq, (-v_left, j, i, k-1))
                
    print(ans)

if __name__ == '__main__':
    solve()