import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
        
        intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            intervals.append((L, R))
    except StopIteration:
        return

    # Sort intervals by L (problem statement says they are sorted, but good practice)
    intervals.sort()
    
    # Current set of reachable positions
    # We start at position 1.
    # Note: If N=1, we are already there, but constraints say N >= 2.
    reachable = {1}
    
    # Process each bad interval
    for idx, (L, R) in enumerate(intervals):
        # Filter reachable positions that are strictly less than L
        # Because we cannot land on any square in [L, R]
        current_reachable = [x for x in reachable if x < L]
        
        if not current_reachable:
            print("No")
            return
        
        # Generate next reachable positions
        next_reachable = set()
        
        for x in current_reachable:
            # Try all jump sizes from A to B
            for k in range(A, B + 1):
                y = x + k
                
                # Check if we reached N
                if y == N:
                    print("Yes")
                    return
                
                # If we jump over the bad interval (y > R), it's a valid landing spot
                # If y < L, it's a valid landing spot before the bad interval
                # If L <= y <= R, it's a bad square, so we cannot land there.
                if y > R or y < L:
                    next_reachable.add(y)
        
        if not next_reachable:
            print("No")
            return
        
        # Optimization: Check the gap to the next interval
        # If there is a large gap between R and the next L, the set of reachable positions
        # will eventually fill up the window [next_L - B, next_L - 1].
        
        if idx < len(intervals) - 1:
            next_L, next_R = intervals[idx + 1]
            
            # The condition for "full window" assumption:
            # If the gap between the end of current bad interval (R) and start of next (next_L)
            # is large enough, we can assume all positions in [next_L - B, next_L - 1] are reachable.
            # Specifically, if next_L - R > B, then R + B < next_L.
            # This means the jump from R (or any pos <= R) can overshoot the gap.
            # But to ensure we can reach EVERY position in [next_L - B, next_L - 1],
            # we need the previous reachable set to cover the "source" positions.
            # Since our previous reachable set contains positions up to R (and potentially lower),
            # and the gap is large, we can effectively "slide" the reachable window.
            # The standard condition used in competitive programming for this problem is:
            # if (next_L - R) > B, then we can assume the window [next_L - B, next_L - 1] is fully reachable.
            
            if (next_L - R) > B:
                # Replace reachable with the full window [next_L - B, next_L - 1]
                # We must ensure these positions are valid (>= 1).
                start_pos = next_L - B
                if start_pos < 1:
                    start_pos = 1
                
                # We only care about positions < next_L
                # Construct the new set
                # Since B is small (<= 20), this loop is fast.
                new_reachable = set()
                for p in range(start_pos, next_L):
                    new_reachable.add(p)
                reachable = new_reachable
            else:
                # Gap is small, keep the computed next_reachable
                reachable = next_reachable
        else:
            # No more intervals, just keep next_reachable
            reachable = next_reachable

    # After processing all intervals, check if we can reach N
    # We need to find if there exists x in reachable such that x + k = N for some k in [A, B]
    for x in reachable:
        for k in range(A, B + 1):
            if x + k == N:
                print("Yes")
                return
    
    print("No")

if __name__ == '__main__':
    solve()