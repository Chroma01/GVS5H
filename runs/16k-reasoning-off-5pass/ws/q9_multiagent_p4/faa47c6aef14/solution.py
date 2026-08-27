import sys

# Increase recursion depth to handle deep DFS traversals for large N
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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

    # Convert 1-based indexing to 0-based
    P = [p - 1 for p in P]
    Q = [q - 1 for q in Q]
    X -= 1
    
    # Identify initial presence of Red and Blue balls
    # R[i] = 1 if box i has red balls, else 0
    # B[i] = 1 if box i has blue balls, else 0
    R = [0] * N
    B = [0] * N
    
    for i in range(N):
        if A[i] > 0:
            R[i] = 1
        if B[i] > 0:
            B[i] = 1
            
    # Propagate Red balls
    # If box u has red balls and P[u] != X, then P[u] receives red balls
    # We use BFS to find all boxes that will eventually have red balls
    queue_r = []
    visited_r = [False] * N
    
    for i in range(N):
        if R[i] == 1:
            queue_r.append(i)
            visited_r[i] = True
            
    while queue_r:
        u = queue_r.pop(0)
        v = P[u]
        if v != X and not visited_r[v]:
            visited_r[v] = True
            R[v] = 1
            queue_r.append(v)
            
    # Propagate Blue balls
    # If box u has blue balls and Q[u] != X, then Q[u] receives blue balls
    queue_b = []
    visited_b = [False] * N
    
    for i in range(N):
        if B[i] == 1:
            queue_b.append(i)
            visited_b[i] = True
            
    while queue_b:
        u = queue_b.pop(0)
        v = Q[u]
        if v != X and not visited_b[v]:
            visited_b[v] = True
            B[v] = 1
            queue_b.append(v)
            
    # Identify the set of boxes that need to be operated on (S)
    # A box is in S if it has at least one ball (Red or Blue) and is not X.
    # We never operate on X because it is the target.
    nodes_to_operate = []
    for i in range(N):
        if i == X:
            continue
        if R[i] == 1 or B[i] == 1:
            nodes_to_operate.append(i)
            
    # Build the dependency graph
    # Edge u -> v exists if operating on u sends balls to v (and v is in nodes_to_operate)
    # If v is in nodes_to_operate, it means v != X and v has balls.
    # Since u sends balls to v, v must be emptied after u, creating a dependency u -> v.
    
    adj = [[] for _ in range(N)]
    
    for u in nodes_to_operate:
        # Check Red path
        v = P[u]
        # If v is not X and v has balls (either red or blue), it needs to be operated on
        if v != X and (R[v] == 1 or B[v] == 1):
            adj[u].append(v)
            
        # Check Blue path
        v = Q[u]
        if v != X and (R[v] == 1 or B[v] == 1):
            adj[u].append(v)
            
    # Cycle detection using DFS
    # States: 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * N
    
    def has_cycle(u):
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1:
                return True
            if state[v] == 0:
                if has_cycle(v):
                    return True
        state[u] = 2
        return False
        
    possible = True
    for u in nodes_to_operate:
        if state[u] == 0:
            if has_cycle(u):
                possible = False
                break
                
    if not possible:
        print("-1")
    else:
        print(len(nodes_to_operate))

if __name__ == '__main__':
    solve()