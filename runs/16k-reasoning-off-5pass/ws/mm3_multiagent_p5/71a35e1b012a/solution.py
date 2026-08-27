import sys
import heapq

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    ops = []
    for i in range(M):
        L, R = map(int, input().split())
        ops.append((L, R, i))
    
    # Sort operations by L and by R
    ops_by_L = sorted(ops, key=lambda x: x[0])
    ops_by_R = sorted(ops, key=lambda x: x[1])
    
    # Data structures for sets
    # max_heap_A: for Set A (L <= cur <= R), max R
    # min_heap_B: for Set B (L > cur), min R
    max_heap_A = []
    min_heap_B = []
    count_C = 0  # number of operations in Set C (R < cur)
    
    used = [False] * M
    in_set = [0] * M  # 0: none, 1: A, 2: B, 3: C
    op_choice = [0] * M
    
    # Initially, all operations are in Set B (since cur=1, L>1)
    for L, R, idx in ops:
        heapq.heappush(min_heap_B, (R, idx))
        in_set[idx] = 2
    
    idx_L = 0
    idx_R = 0
    cur = 1
    right = N
    
    while cur <= right:
        # Move ops with L == cur from B to A
        while idx_L < M and ops_by_L[idx_L][0] == cur:
            L, R, idx = ops_by_L[idx_L]
            idx_L += 1
            if not used[idx]:
                in_set[idx] = 1
                heapq.heappush(max_heap_A, (-R, idx))
        
        # Move ops with R < cur from A to C
        while idx_R < M and ops_by_R[idx_R][1] < cur:
            L, R, idx = ops_by_R[idx_R]
            idx_R += 1
            if not used[idx] and in_set[idx] == 1:
                in_set[idx] = 3
                count_C += 1
        
        # Clean heaps
        while max_heap_A and (used[max_heap_A[0][1]] or in_set[max_heap_A[0][1]] != 1):
            heapq.heappop(max_heap_A)
        while min_heap_B and (used[min_heap_B[0][1]] or in_set[min_heap_B[0][1]] != 2):
            heapq.heappop(min_heap_B)
        
        # Check Set C: if any, we can finish immediately using type 2
        if count_C > 0:
            # Find any unused op in C. We can pick the one with max R for efficiency, but any works.
            # Scan backwards from idx_R-1 to find one.
            found = False
            for j in range(idx_R-1, -1, -1):
                idx = ops_by_R[j][2]
                if not used[idx] and in_set[idx] == 3:
                    used[idx] = True
                    op_choice[idx] = 2
                    in_set[idx] = 0
                    count_C -= 1
                    # This covers [R+1, N], and since R < cur, we cover [cur, N]
                    cur = right + 1
                    found = True
                    break
            if not found:
                print(-1)
                return
            continue
        
        # Decide between Set A and Set B
        if max_heap_A:
            # Use type 1 with max R
            negR, idx = max_heap_A[0]
            R = -negR
            used[idx] = True
            op_choice[idx] = 1
            in_set[idx] = 0
            heapq.heappop(max_heap_A)
            cur = R + 1
        elif min_heap_B:
            # Use type 2 with min R
            R, idx = min_heap_B[0]
            used[idx] = True
            op_choice[idx] = 2
            in_set[idx] = 0
            heapq.heappop(min_heap_B)
            # Type 2 covers [R+1, N], so we set right = R
            right = R
        else:
            # No available operations
            print(-1)
            return
    
    # Output result
    K = sum(1 for c in op_choice if c != 0)
    print(K)
    print(' '.join(map(str, op_choice)))

if __name__ == "__main__":
    solve()