import sys

# Increase recursion depth just in case, though not strictly needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Fast I/O
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
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
            
        # Identify positions of '1's (0-indexed)
        pos_A = [i for i, c in enumerate(A) if c == '1']
        pos_B = [i for i, c in enumerate(B) if c == '1']
        
        # Basic checks
        # We need at least as many pieces in A as in B to cover all '1's in B
        if len(pos_A) < len(pos_B):
            results.append("-1")
            continue
            
        # Precompute gaps for A
        # gaps_A[i] = pos_A[i+1] - pos_A[i]
        # This represents the distance between consecutive pieces in A
        gaps_A = [pos_A[i+1] - pos_A[i] for i in range(len(pos_A) - 1)]
        
        # Precompute gaps for B
        # gaps_B[i] = pos_B[i+1] - pos_B[i]
        gaps_B = [pos_B[i+1] - pos_B[i] for i in range(len(pos_B) - 1)]
        
        # Check function for binary search
        def check(K):
            # 1. Find first piece in A such that x >= y_1 - K
            # This ensures the leftmost piece can move right to y_1 within K operations
            target_start = pos_B[0] - K
            idx = 0
            # Since pos_A is sorted, we can just scan.
            while idx < len(pos_A) and pos_A[idx] < target_start:
                idx += 1
            
            if idx == len(pos_A):
                return False
            
            current_idx = idx
            
            # Iterate through gaps_B
            for g in gaps_B:
                # We need to find next piece such that sum of gaps from current_idx to next_idx
                # is in [g, g + 2*K]
                # Lower bound: sum >= g (we can only reduce gaps, not increase them)
                # Upper bound: sum - 2*K >= g  => sum <= g + 2*K (we can reduce by at most 2 per op)
                
                min_next_pos = pos_A[current_idx] + g
                max_next_pos = pos_A[current_idx] + g + 2 * K
                
                found = False
                # Scan forward to find the first valid piece
                # We must pick the earliest valid piece to leave maximum room for subsequent gaps
                while current_idx + 1 < len(pos_A):
                    current_idx += 1
                    if pos_A[current_idx] >= min_next_pos:
                        if pos_A[current_idx] <= max_next_pos:
                            found = True
                            break
                        else:
                            # pos_A[current_idx] is too far.
                            # Since pos_A is sorted, any subsequent piece will be even further.
                            # So this gap cannot be covered.
                            return False
                    # If pos_A[current_idx] < min_next_pos, we continue to next piece to increase distance.
                
                if not found:
                    return False
            
            # After covering all gaps, check the last piece constraint
            # The last piece used is at pos_A[current_idx]
            # We need pos_A[current_idx] <= pos_B[-1] + K
            # This ensures the rightmost piece can move left to y_m within K operations
            if pos_A[current_idx] > pos_B[-1] + K:
                return False
                
            return True

        # Binary Search for minimum K
        low = 0
        high = N
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