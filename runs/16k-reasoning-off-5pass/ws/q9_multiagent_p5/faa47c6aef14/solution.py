import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        P = [int(next(iterator)) for _ in range(N)]
        Q = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Adjust to 0-based indexing
    X -= 1
    P = [p - 1 for p in P]
    Q = [q - 1 for q in Q]

    # Identify initially non-empty boxes
    initially_non_empty = set()
    for i in range(N):
        if A[i] + B[i] > 0:
            initially_non_empty.add(i)

    # If no balls at all, 0 operations needed
    if not initially_non_empty:
        print(0)
        return

    # Build the original graph (forward) and reverse graph
    # Original graph: u -> v means balls move from u to v
    # Reverse graph: v -> u means u can reach v (used to find nodes that can reach X)
    
    # Forward graph: adj[u] contains list of v such that u -> v
    # Reverse graph: rev_adj[v] contains list of u such that u -> v
    
    adj = [[] for _ in range(N)]
    rev_adj = [[] for _ in range(N)]

    for i in range(N):
        p_target = P[i]
        q_target = Q[i]
        
        # Add edges: i -> P[i] and i -> Q[i]
        adj[i].append(p_target)
        rev_adj[p_target].append(i)
        
        adj[i].append(q_target)
        rev_adj[q_target].append(i)

    # Step 1: Find S_reach (nodes that can reach X)
    # BFS starting from X in the reverse graph
    s_reach = set()
    queue = [X]
    s_reach.add(X)
    
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        for v in rev_adj[u]:
            if v not in s_reach:
                s_reach.add(v)
                queue.append(v)

    # Step 2: Find S_active (nodes that will contain balls)
    # BFS starting from initially_non_empty in the forward graph
    s_active = set()
    queue = list(initially_non_empty)
    s_active.update(initially_non_empty)
    
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        for v in adj[u]:
            if v not in s_active:
                s_active.add(v)
                queue.append(v)

    # Step 3: Check if all active nodes can reach X
    # i.e., S_active must be a subset of S_reach
    if not s_active.issubset(s_reach):
        print(-1)
    else:
        # The answer is the number of nodes that need to be operated on
        # which is exactly the size of S_active
        print(len(s_active))

if __name__ == '__main__':
    solve()