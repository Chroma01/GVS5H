import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
        
        bad_intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            bad_intervals.append((L, R))
            
    except StopIteration:
        return

    # Identify critical points (checkpoints)
    # We start at 1.
    # We must land on R_i + 1 to clear bad intervals [L_i, R_i].
    # We want to reach N.
    # Also, we might need to consider N itself as a checkpoint.
    
    checkpoints = set()
    checkpoints.add(1)
    checkpoints.add(N)
    
    for L, R in bad_intervals:
        # The first safe square after a bad interval is R + 1
        # We add this to checkpoints.
        # Note: Constraints say R < N, so R + 1 <= N is guaranteed if R < N.
        # However, if R + 1 > N, it's outside the board, so we ignore.
        if R + 1 <= N:
            checkpoints.add(R + 1)
            
    # Sort checkpoints to process in order
    sorted_checkpoints = sorted(list(checkpoints))
    
    # Map value to index for quick lookup if needed, or just use binary search
    # Since M is small (2e4), number of checkpoints is at most 2e4 + 2.
    # We can just iterate.
    
    # BFS / Reachability
    # reachable[i] will be True if sorted_checkpoints[i] is reachable
    reachable = [False] * len(sorted_checkpoints)
    
    # Start at 1 (index 0)
    # It is guaranteed that 1 is the first element because 1 < L_i for all i (L_i > 1)
    # and 1 <= N.
    if sorted_checkpoints[0] == 1:
        reachable[0] = True
        
    queue = [0]
    head = 0
    
    while head < len(queue):
        u_idx = queue[head]
        head += 1
        u = sorted_checkpoints[u_idx]
        
        # If we reached N, we can stop early
        if u == N:
            print("Yes")
            return

        # Try to reach all subsequent checkpoints T
        # Optimization: We only need to check T that are reachable from u
        # based on the logic derived:
        # 1. If T - u <= B: check if A <= T - u <= B
        # 2. If T - u > B: 
        #    - If B > A: T is reachable (gap is large enough to bridge)
        #    - If B == A: T is reachable if (T - u) % A == 0
        
        # We iterate through all T > u
        for v_idx in range(u_idx + 1, len(sorted_checkpoints)):
            v = sorted_checkpoints[v_idx]
            dist = v - u
            
            if dist > B:
                # Gap is larger than max jump
                if B > A:
                    # Can definitely reach v because we can adjust steps to cover the gap
                    # and the gap contains no bad squares (by definition of v being a checkpoint)
                    # Since the gap is large, we can reach any point in it, including v.
                    reachable[v_idx] = True
                    queue.append(v_idx)
                else:
                    # B == A
                    if dist % A == 0:
                        reachable[v_idx] = True
                        queue.append(v_idx)
            else:
                # dist <= B
                if A <= dist <= B:
                    reachable[v_idx] = True
                    queue.append(v_idx)
                    
    # If we finished BFS and haven't returned, check if N is reachable
    if reachable[-1]:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()