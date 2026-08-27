import sys
from bisect import bisect_left

# Increase recursion depth just in case, though not used here
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N_str = next(iterator)
            N = int(N_str)
            A = next(iterator)
            B = next(iterator)
        except StopIteration:
            break
        
        # Get positions of '1's (0-indexed)
        # Using list comprehension is efficient enough for N <= 10^6
        A_pos = [i for i, c in enumerate(A) if c == '1']
        B_pos = [i for i, c in enumerate(B) if c == '1']
        
        cntA = len(A_pos)
        cntB = len(B_pos)
        
        # If we have fewer pieces in A than needed in B, it's impossible
        # because pieces cannot be split, only merged.
        if cntA < cntB:
            results.append("-1")
            continue
        
        # Binary search for the minimum number of operations M
        # The answer is the minimum M such that we can map B_pos to a subsequence of A_pos
        # where each mapped piece is within distance M, and gaps in A are sufficient.
        
        low = 0
        high = N
        ans = N
        
        while low <= high:
            mid = (low + high) // 2
            
            possible = True
            last_A_idx = -1 # Index in A_pos of the last selected piece
            
            for j in range(cntB):
                target = B_pos[j]
                min_val = target - mid
                max_val = target + mid
                
                if j == 0:
                    lower_bound = min_val
                else:
                    prev_target = B_pos[j-1]
                    gap_needed = target - prev_target
                    # We need A_pos[k] >= last_A_val + gap_needed
                    # last_A_val is A_pos[last_A_idx]
                    lower_bound = max(min_val, A_pos[last_A_idx] + gap_needed)
                
                # Find first index in A_pos > last_A_idx with value >= lower_bound
                idx = bisect_left(A_pos, lower_bound, lo=last_A_idx + 1)
                
                if idx >= len(A_pos) or A_pos[idx] > max_val:
                    possible = False
                    break
                
                last_A_idx = idx
            
            if possible:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()