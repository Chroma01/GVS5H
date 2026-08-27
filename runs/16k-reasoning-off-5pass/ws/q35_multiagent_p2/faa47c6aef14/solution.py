import sys
from collections import deque

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    
    N = int(next(iterator))
    X = int(next(iterator))
    
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(iterator))
        
    B = [0] * (N + 1)
    for i in range(1, N + 1):
        B[i] = int(next(iterator))
        
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = int(next(iterator))
        
    Q = [0] * (N + 1)
    for i in range(1, N + 1):
        Q[i] = int(next(iterator))
        
    # Build reverse graphs for reachability to X
    # rev_P[u] contains list of v such that P[v] = u
    rev_P = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        rev_P[P[i]].append(i)
        
    rev_Q = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        rev_Q[Q[i]].append(i)
        
    # Find all nodes that can reach X in red graph (using reverse BFS from X)
    can_reach_X_red = [False] * (N + 1)
    queue = deque([X])
    can_reach_X_red[X] = True
    while queue:
        u = queue.popleft()
        for v in rev_P[u]:
            if not can_reach_X_red[v]:
                can_reach_X_red[v] = True
                queue.append(v)
                
    # Find all nodes that can reach X in blue graph
    can_reach_X_blue = [False] * (N + 1)
    queue = deque([X])
    can_reach_X_blue[X] = True
    while queue:
        u = queue.popleft()
        for v in rev_Q[u]:
            if not can_reach_X_blue[v]:
                can_reach_X_blue[v] = True
                queue.append(v)
                
    # Check feasibility
    for i in range(1, N + 1):
        if i == X:
            continue
        if A[i] == 1 and not can_reach_X_red[i]:
            print(-1)
            return
        if B[i] == 1 and not can_reach_X_blue[i]:
            print(-1)
            return
            
    # Find active boxes for red balls
    # Active red boxes: reachable from initial red positions in forward red graph, and can reach X
    # We can compute this by starting BFS from all initial red positions in the forward red graph,
    # but only visiting nodes that can reach X.
    # Alternatively, we can do BFS from X in reverse red graph, but only starting from nodes that have initial red balls or are reachable from them.
    # Actually, the set of active red boxes is: {i | i can reach X in red graph AND there exists a path from some initial red box to i in red graph}
    # This is equivalent to: i is in can_reach_X_red AND i is reachable from some j with A[j]==1 in the forward red graph.
    
    # Let's compute reachable_from_initial_red: set of nodes reachable from any node with A[i]==1 in forward red graph.
    # But we only care about nodes that can also reach X.
    
    # Efficient approach: 
    # 1. Start BFS from all nodes with A[i]==1 in the forward red graph to find all nodes reachable from initial red balls.
    # 2. Intersect with can_reach_X_red.
    
    reachable_from_initial_red = [False] * (N + 1)
    queue = deque()
    for i in range(1, N + 1):
        if A[i] == 1:
            reachable_from_initial_red[i] = True
            queue.append(i)
            
    while queue:
        u = queue.popleft()
        v = P[u]
        if not reachable_from_initial_red[v]:
            reachable_from_initial_red[v] = True
            queue.append(v)
            
    # Active red boxes are those that are both reachable from initial red balls and can reach X
    active_red = [False] * (N + 1)
    for i in range(1, N + 1):
        if reachable_from_initial_red[i] and can_reach_X_red[i]:
            active_red[i] = True
            
    # Similarly for blue balls
    reachable_from_initial_blue = [False] * (N + 1)
    queue = deque()
    for i in range(1, N + 1):
        if B[i] == 1:
            reachable_from_initial_blue[i] = True
            queue.append(i)
            
    while queue:
        u = queue.popleft()
        v = Q[u]
        if not reachable_from_initial_blue[v]:
            reachable_from_initial_blue[v] = True
            queue.append(v)
            
    active_blue = [False] * (N + 1)
    for i in range(1, N + 1):
        if reachable_from_initial_blue[i] and can_reach_X_blue[i]:
            active_blue[i] = True
            
    # The answer is the number of boxes i != X that are in active_red or active_blue
    ans = 0
    for i in range(1, N + 1):
        if i == X:
            continue
        if active_red[i] or active_blue[i]:
            ans += 1
            
    print(ans)

solve()