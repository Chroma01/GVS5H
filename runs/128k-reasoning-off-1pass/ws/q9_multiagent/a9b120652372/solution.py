import sys
import bisect

# Increase recursion depth just in case, though we use iterative approach
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

        # Extract 0-based indices of '1's
        posA = [i for i, c in enumerate(A) if c == '1']
        posB = [i for i, c in enumerate(B) if c == '1']

        # Feasibility check: We cannot create pieces.
        if len(posA) < len(posB):
            results.append("-1")
            continue

        # Optimization: If counts match, the mapping is fixed (j-th piece of A to j-th of B).
        # We just need the max displacement.
        if len(posA) == len(posB):
            max_disp = 0
            for i in range(len(posA)):
                d = abs(posB[i] - posA[i])
                if d > max_disp:
                    max_disp = d
            results.append(str(max_disp))
            continue

        # If counts differ (len(posA) > len(posB)), we need to find a mapping.
        # We binary search for the minimum K (operations).
        # Range for K: [0, 2*N] is safe. Max displacement is N.
        
        low = 0
        high = 2 * N
        ans = -1

        # Check function for a given K
        def check(K):
            # We need to select indices u_0, u_1, ..., u_{m-1} from posB (m = len(posA))
            # such that:
            # 1. posA[j] - K <= posB[u_j] <= posA[j] + K
            # 2. posB[u_j] >= posB[u_{j-1}] (non-decreasing mapping)
            # 3. posB[u_j] <= posB[u_{j-1}] + (posA[j] - posA[j-1]) (gap constraint)
            
            # Greedy Strategy:
            # For each piece j in A, pick the SMALLEST valid posB[u_j].
            # Why smallest?
            # - It minimizes the lower bound for the next piece (posB[u_{j+1}] >= posB[u_j]).
            # - It keeps the current value low, which helps satisfy the upper bound constraint 
            #   (posB[u_{j+1}] <= posB[u_j] + delta) for the next step if delta is small.
            #   Although a larger posB[u_j] increases the upper bound for u_{j+1}, 
            #   it also increases the lower bound. The lower bound constraint is usually 
            #   the tighter one for "reachability" when we need to hit specific targets.
            #   Specifically, if we pick a larger value, we might force the next piece to be 
            #   larger than its valid range [L_{j+1}, R_{j+1}].
            
            current_b_val = -1 # Value of posB[u_{j-1}]
            
            for j in range(len(posA)):
                a_val = posA[j]
                
                # Constraint 1: Displacement
                min_val = a_val - K
                max_val = a_val + K
                
                # Constraint 2 & 3: Relative to previous
                # Lower bound: max(min_val, current_b_val)
                # Upper bound: max_val, and if current_b_val exists: current_b_val + (a_val - prev_a_val)
                
                lower = min_val
                if current_b_val != -1:
                    lower = max(lower, current_b_val)
                
                upper = max_val
                if current_b_val != -1:
                    delta = a_val - posA[j-1]
                    upper = min(upper, current_b_val + delta)
                
                # Find smallest element in posB >= lower
                idx = bisect.bisect_left(posB, lower)
                
                if idx >= len(posB):
                    return False
                
                candidate = posB[idx]
                
                if candidate > upper:
                    return False
                
                # Valid candidate found. Update current_b_val.
                current_b_val = candidate
            
            return True

        # Binary Search
        l, r = 0, 2 * N
        res = -1
        
        while l <= r:
            mid = (l + r) // 2
            if check(mid):
                res = mid
                r = mid - 1
            else:
                l = mid + 1
        
        results.append(str(res))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()