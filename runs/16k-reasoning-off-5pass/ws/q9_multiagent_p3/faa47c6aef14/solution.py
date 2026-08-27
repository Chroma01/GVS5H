import sys

# Increase recursion depth just in case, though iterative approach is used
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
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
            
        P = []
        for _ in range(N):
            P.append(int(next(iterator)) - 1) # 0-indexed
            
        Q = []
        for _ in range(N):
            Q.append(int(next(iterator)) - 1) # 0-indexed
    except StopIteration:
        return

    # Identify initial balls
    initial_red = [i for i in range(N) if A[i] == 1]
    initial_blue = [i for i in range(N) if B[i] == 1]
    
    # Identify cycle containing X in P
    cycle_P = []
    curr = X
    while True:
        cycle_P.append(curr)
        curr = P[curr]
        if curr == X:
            break
    
    # Identify cycle containing X in Q
    cycle_Q = []
    curr = X
    while True:
        cycle_Q.append(curr)
        curr = Q[curr]
        if curr == X:
            break
            
    # Check validity for Red: all initial red balls must be in cycle_P
    set_P = set(cycle_P)
    set_Q = set(cycle_Q)
    
    for i in initial_red:
        if i not in set_P:
            print("-1")
            return
            
    for i in initial_blue:
        if i not in set_Q:
            print("-1")
            return
            
    # Determine operations for Red
    # We need to mark nodes in cycle_P that are on the path from some ball-bearing node to X.
    # In the cycle list [X, v1, v2, ..., vk], the path from v_i to X is v_i -> ... -> v_k.
    # The union of paths from all ball-bearing nodes is the path from the node with the 
    # largest index (farthest from X in the cycle order) that has a ball.
    
    ops = [False] * N
    
    # Red
    max_idx_P = -1
    # cycle_P[0] is X. We look for balls at indices 1 to len-1.
    for idx, node in enumerate(cycle_P):
        if node == X: 
            continue
        if A[node] == 1:
            max_idx_P = idx
            
    if max_idx_P != -1:
        # Mark from max_idx_P to the end (excluding X which is at 0, but the list ends at vk)
        # The nodes to operate are cycle_P[max_idx_P] ... cycle_P[-1]
        # Fixed range to include the last element (predecessor of X)
        for i in range(max_idx_P, len(cycle_P)):
            ops[cycle_P[i]] = True
            
    # Blue
    max_idx_Q = -1
    for idx, node in enumerate(cycle_Q):
        if node == X: 
            continue
        if B[node] == 1:
            max_idx_Q = idx
            
    if max_idx_Q != -1:
        for i in range(max_idx_Q, len(cycle_Q)):
            ops[cycle_Q[i]] = True
            
    print(sum(ops))

if __name__ == '__main__':
    solve()