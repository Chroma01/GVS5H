import sys

def solve():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))

    # Convert to 0-indexed
    X -= 1
    P = [p - 1 for p in P]
    Q = [q - 1 for q in Q]

    invP = [0] * N
    invQ = [0] * N
    for i in range(N):
        invP[P[i]] = i
        invQ[Q[i]] = i

    # Build P-cycle from X going backwards (i.e., following invP)
    p_cycle = []
    cur = X
    while True:
        p_cycle.append(cur)
        cur = invP[cur]
        if cur == X:
            break
    # p_cycle[k] is at distance k from X along P
    p_dist = {node: idx for idx, node in enumerate(p_cycle)}

    # Build Q-cycle from X going backwards
    q_cycle = []
    cur = X
    while True:
        q_cycle.append(cur)
        cur = invQ[cur]
        if cur == X:
            break
    q_dist = {node: idx for idx, node in enumerate(q_cycle)}

    # Validate reds and find max distance
    r_max = 0
    for i in range(N):
        if A[i] == 1:
            if i not in p_dist:
                print(-1)
                return
            d = p_dist[i]
            if d > r_max:
                r_max = d

    # Validate blues and find max distance
    b_max = 0
    for i in range(N):
        if B[i] == 1:
            if i not in q_dist:
                print(-1)
                return
            d = q_dist[i]
            if d > b_max:
                b_max = d

    # R_set: nodes at distances 1..r_max in P-cycle
    # B_set: nodes at distances 1..b_max in Q-cycle
    R_set = p_cycle[1:1 + r_max]
    B_set = q_cycle[1:1 + b_max]

    # Compute |R_set ∪ B_set|
    b_set = set(B_set)
    inter = sum(1 for node in R_set if node in b_set)
    ans = len(R_set) + len(B_set) - inter
    print(ans)

solve()