import sys

def solve():
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

    # Convert to 0-indexed
    X -= 1
    P = [p - 1 for p in P]
    Q = [q - 1 for p in Q]
    
    # Check if there are any balls at all
    has_balls = False
    for i in range(N):
        if A[i] == 1 or B[i] == 1:
            has_balls = True
            break
            
    if not has_balls:
        print(0)
        return

    # For permutation graphs, nodes are in the same cycle iff they are in the same component.
    # We need to check for each box i that has balls:
    # - If A[i] == 1, then i and X must be in the same cycle in the red permutation graph (edges i -> P[i])
    # - If B[i] == 1, then i and X must be in the same cycle in the blue permutation graph (edges i -> Q[i])
    
    # To check if two nodes are in the same cycle in a permutation graph, we can use the fact that
    # in a permutation, each node has exactly one outgoing and one incoming edge. The graph is a collection of disjoint cycles.
    # Two nodes are in the same cycle if and only if they are in the same connected component.
    # We can use Union-Find or simply traverse to find the cycle representative.
    
    # Let's use a simple approach: for each permutation, find the cycle representative for each node.
    # The cycle representative can be the smallest index in the cycle, or we can just check reachability.
    # Since it's a permutation, we can find the cycle containing X and mark all nodes in that cycle.
    
    def get_cycle_nodes(perm, target):
        """Returns a set of all nodes in the same cycle as target in the permutation graph."""
        cycle_nodes = set()
        curr = target
        while curr not in cycle_nodes:
            cycle_nodes.add(curr)
            curr = perm[curr]
        return cycle_nodes
    
    red_cycle_X = get_cycle_nodes(P, X)
    blue_cycle_X = get_cycle_nodes(Q, X)
    
    # Check if X itself is in its own cycle (it always is, but we need the set)
    # Now, for each box i that has balls:
    # - If A[i] == 1, check if i is in red_cycle_X
    # - If B[i] == 1, check if i is in blue_cycle_X
    # If any check fails, return -1.
    # Otherwise, the answer is the number of boxes that have at least one ball.
    
    ans = 0
    for i in range(N):
        if A[i] == 1 or B[i] == 1:
            ans += 1
            if A[i] == 1 and i not in red_cycle_X:
                print(-1)
                return
            if B[i] == 1 and i not in blue_cycle_X:
                print(-1)
                return
                
    print(ans)

solve()