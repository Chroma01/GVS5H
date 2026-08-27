import sys

def solve():
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline
    
    N, X = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    
    X -= 1
    P = [p - 1 for p in P]
    Q = [q - 1 for q in Q]
    
    # Find the P-cycle containing X and compute distances
    visited_red = [False] * N
    dist_red = [-1] * N
    cur = X
    d = 0
    while not visited_red[cur]:
        visited_red[cur] = True
        dist_red[cur] = d
        d += 1
        cur = P[cur]
    
    # Find the Q-cycle containing X and compute distances
    visited_blue = [False] * N
    dist_blue = [-1] * N
    cur = X
    d = 0
    while not visited_blue[cur]:
        visited_blue[cur] = True
        dist_blue[cur] = d
        d += 1
        cur = Q[cur]
    
    # Check reachability: every ball must be in the same cycle as X for its color
    for i in range(N):
        if A[i] == 1 and not visited_red[i]:
            print(-1)
            return
        if B[i] == 1 and not visited_blue[i]:
            print(-1)
            return
    
    total_red = sum(A)
    total_blue = sum(B)
    
    # If no balls, already in goal state
    if total_red + total_blue == 0:
        print(0)
        return
    
    # Determine which colors have balls
    has_red = total_red > 0
    has_blue = total_blue > 0
    
    if has_red and has_blue:
        # Both colors have balls: need union of required operation sets
        d_red = 0
        for i in range(N):
            if A[i] == 1:
                d_red = max(d_red, dist_red[i])
        
        d_blue = 0
        for i in range(N):
            if B[i] == 1:
                d_blue = max(d_blue, dist_blue[i])
        
        # Count union of nodes at distance 1..d_red in red cycle and 1..d_blue in blue cycle
        union_count = 0
        for i in range(N):
            if i == X:
                continue
            in_red_op = visited_red[i] and 1 <= dist_red[i] <= d_red
            in_blue_op = visited_blue[i] and 1 <= dist_blue[i] <= d_blue
            if in_red_op or in_blue_op:
                union_count += 1
        print(union_count)
    elif has_red:
        d_red = 0
        for i in range(N):
            if A[i] == 1:
                d_red = max(d_red, dist_red[i])
        print(d_red)
    else:  # has_blue
        d_blue = 0
        for i in range(N):
            if B[i] == 1:
                d_blue = max(d_blue, dist_blue[i])
        print(d_blue)

solve()