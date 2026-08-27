import sys

# Increase recursion depth just in case, though not used here.
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
    except StopIteration:
        return
    
    T = int(T_str)
    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = next(iterator)
            B = next(iterator)
        except StopIteration:
            break
            
        # Extract 1-based indices of pieces in A
        pos_A = [i + 1 for i, c in enumerate(A) if c == '1']
        # Extract 1-based indices of target positions in B
        pos_B = [i + 1 for i, c in enumerate(B) if c == '1']
        
        m = len(pos_A)
        k = len(pos_B)
        
        # If number of pieces doesn't match, impossible
        if m != k:
            results.append("-1")
            continue
        
        # If A and B are identical, 0 operations
        if pos_A == pos_B:
            results.append("0")
            continue
            
        # Check function for a given K
        def check(K):
            # We need to match pos_B[j] with some pos_A[i]
            # Constraints for matching pos_B[j] to pos_A[i]:
            # 1. Absolute shift: |pos_A[i] - pos_B[j]| <= K
            # 2. Gap constraint (for j > 0): 
            #    pos_A[i] - pos_A[prev_idx_A] >= pos_B[j] - pos_B[prev_idx]
            #    pos_A[i] - pos_A[prev_idx_A] <= (pos_B[j] - pos_B[prev_idx]) + 2*K
            
            ptr = 0
            prev_idx_A = -1
            prev_pos_B_val = 0
            
            for j in range(k):
                target = pos_B[j]
                
                if j == 0:
                    # First piece: only absolute constraint
                    # Find smallest i such that |pos_A[i] - target| <= K
                    # i.e., target - K <= pos_A[i] <= target + K
                    
                    lower = target - K
                    upper = target + K
                    
                    # Advance ptr to find first valid
                    while ptr < m and pos_A[ptr] < lower:
                        ptr += 1
                    
                    if ptr == m or pos_A[ptr] > upper:
                        return False
                    
                    prev_idx_A = ptr
                    prev_pos_B_val = target
                else:
                    prev_target = pos_B[j-1]
                    prev_prev_idx = prev_idx_A
                    
                    # Constraints:
                    # 1. pos_A[i] > pos_A[prev_idx_A] (guaranteed if we advance ptr)
                    # 2. pos_A[i] - pos_A[prev_idx_A] >= target - prev_target
                    # 3. pos_A[i] - pos_A[prev_idx_A] <= (target - prev_target) + 2*K
                    # 4. |pos_A[i] - target| <= K
                    
                    min_gap = target - prev_target
                    max_gap = min_gap + 2 * K
                    
                    # We need pos_A[i] >= pos_A[prev_idx_A] + min_gap
                    # And pos_A[i] <= pos_A[prev_idx_A] + max_gap
                    # And pos_A[i] >= target - K
                    # And pos_A[i] <= target + K
                    
                    lb1 = pos_A[prev_idx_A] + min_gap
                    lb2 = target - K
                    lower = max(lb1, lb2)
                    
                    ub1 = pos_A[prev_idx_A] + max_gap
                    ub2 = target + K
                    upper = min(ub1, ub2)
                    
                    # Advance ptr to find first valid
                    while ptr < m and pos_A[ptr] < lower:
                        ptr += 1
                    
                    if ptr == m or pos_A[ptr] > upper:
                        return False
                    
                    prev_idx_A = ptr
                    prev_pos_B_val = target
            
            return True

        # Binary search for minimum K
        low = 0
        high = N # Max possible shift is N
        ans = -1
        
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()