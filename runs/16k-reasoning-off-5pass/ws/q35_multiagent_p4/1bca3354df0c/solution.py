import sys
from collections import deque

def solve():
    # Increase recursion depth just in case, though we use BFS/iterative approaches
    sys.setrecursionlimit(300000)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Step 1: Find connected components and their bipartition sizes
    # colors[i] = 0 or 1, -1 if unvisited
    colors = [-1] * (N + 1)
    components = [] # List of (size_part0, size_part1)

    for i in range(1, N + 1):
        if colors[i] == -1:
            # BFS to find component and bipartition
            q = deque([i])
            colors[i] = 0
            part0 = 0
            part1 = 0
            
            while q:
                u = q.popleft()
                if colors[u] == 0:
                    part0 += 1
                else:
                    part1 += 1
                
                for v in adj[u]:
                    if colors[v] == -1:
                        colors[v] = 1 - colors[u]
                        q.append(v)
                    elif colors[v] == colors[u]:
                        # This should not happen as per problem statement (initially bipartite)
                        pass
            
            components.append((part0, part1))

    # Step 2: Determine the maximum possible |U| * |V|
    # We have components with sizes (a_i, b_i).
    # For each component, we assign either (a_i to U, b_i to V) or (b_i to U, a_i to V).
    # Let diff_i = a_i - b_i.
    # If we choose the first option, contribution to (|U| - |V|) is diff_i.
    # If we choose the second option, contribution to (|U| - |V|) is -diff_i.
    # Let S = sum of chosen signs * diff_i.
    # Then |U| - |V| = S.
    # Also |U| + |V| = N.
    # So 2|U| = N + S => |U| = (N + S) / 2.
    # We want to maximize |U| * |V| = |U| * (N - |U|).
    # This is maximized when |U| is as close to N/2 as possible, i.e., |S| is minimized.
    
    # We need to find the subset sum of diff_i's that is closest to 0.
    # Let D_i = |a_i - b_i|. We want to assign signs s_i in {-1, 1} to D_i
    # such that |sum(s_i * D_i)| is minimized.
    
    diffs = []
    for (a, b) in components:
        diffs.append(abs(a - b))
    
    # DP using bitset to find reachable sums
    # The maximum possible sum is N.
    # We can use an integer as a bitset.
    # bit j is 1 if sum j is reachable.
    # Since we want to minimize absolute sum, we can track reachable sums from 0 to N.
    
    # reachable sums can range from -N to N.
    # Let's just track non-negative sums.
    # If we can form sum S, we can also form -S by flipping all signs.
    # So we just need to find the smallest S >= 0 that is reachable.
    
    # Base case: sum 0 is reachable.
    reachable = 1 # bit 0 is set
    
    max_sum = N
    for d in diffs:
        # Shift left by d to add d to existing sums
        # reachable | (reachable << d)
        # But we only care about sums up to N.
        # We can mask to keep bits within range [0, N]
        # However, Python handles large integers automatically.
        # We just need to ensure we don't go too far, but N is 2e5, so bitset size 2e5 is fine.
        
        # To optimize, we can mask to N bits.
        # mask = (1 << (N + 1)) - 1
        # reachable = (reachable | (reachable << d)) & mask
        
        # Actually, we don't strictly need to mask if we just check bits up to N later,
        # but masking keeps the integer size manageable.
        reachable = reachable | (reachable << d)
        
        # Optional: trim bits above N to save memory/time
        # reachable &= (1 << (N + 1)) - 1

    # Find the smallest S >= 0 such that the S-th bit is set
    min_abs_S = N
    for s in range(N + 1):
        if (reachable >> s) & 1:
            min_abs_S = s
            break
            
    # Calculate |U| and |V|
    # |U| - |V| = min_abs_S or -min_abs_S.
    # |U| + |V| = N
    # 2|U| = N + min_abs_S (assuming S = min_abs_S)
    # Or 2|U| = N - min_abs_S (assuming S = -min_abs_S)
    # In either case, |U| and |V| are (N + min_abs_S)/2 and (N - min_abs_S)/2.
    
    if (N + min_abs_S) % 2 != 0:
        # This should not happen because N and sum of diffs have same parity?
        # sum(a_i + b_i) = N.
        # sum(a_i - b_i) = sum(a_i) - sum(b_i).
        # N = sum(a_i) + sum(b_i).
        # N - sum(a_i - b_i) = 2 sum(b_i) which is even.
        # So N and sum of diffs have same parity.
        # Thus N + min_abs_S is even.
        pass
        
    U = (N + min_abs_S) // 2
    V = N - U
    
    max_edges = U * V
    moves = max_edges - M
    
    if moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()