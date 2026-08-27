import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def main():
    N, X = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    # convert to 0-indexed
    P = [p-1 for p in P]
    Q = [q-1 for q in Q]
    X -= 1

    # Find P-cycle containing X
    cycleP = []
    cur = X
    while True:
        cycleP.append(cur)
        cur = P[cur]
        if cur == X:
            break
    setP = set(cycleP)

    # Check reds are in P-cycle
    for i in range(N):
        if A[i] == 1 and i not in setP:
            print(-1)
            return

    # Compute distances to X in P-cycle
    dP = {}
    dist = 0
    cur = X
    while True:
        dP[cur] = dist
        cur = P[cur]
        dist += 1
        if cur == X:
            break

    # Find Q-cycle containing X
    cycleQ = []
    cur = X
    while True:
        cycleQ.append(cur)
        cur = Q[cur]
        if cur == X:
            break
    setQ = set(cycleQ)

    # Check blues are in Q-cycle
    for i in range(N):
        if B[i] == 1 and i not in setQ:
            print(-1)
            return

    # Compute distances to X in Q-cycle
    dQ = {}
    dist = 0
    cur = X
    while True:
        dQ[cur] = dist
        cur = Q[cur]
        dist += 1
        if cur == X:
            break

    # Determine max distances for reds and blues
    max_red_dist = -1
    for i in range(N):
        if A[i] == 1:
            max_red_dist = max(max_red_dist, dP[i])

    max_blue_dist = -1
    for i in range(N):
        if B[i] == 1:
            max_blue_dist = max(max_blue_dist, dQ[i])

    # Build red order: vertices in P-cycle with 0 < dP <= max_red_dist, sorted by dP descending
    if max_red_dist == -1:
        red_order = []
    else:
        red_order = [v for v in cycleP if 0 < dP[v] <= max_red_dist]
        red_order.sort(key=lambda v: dP[v], reverse=True)

    # Build blue order: vertices in Q-cycle with 0 < dQ <= max_blue_dist, sorted by dQ descending
    if max_blue_dist == -1:
        blue_order = []
    else:
        blue_order = [v for v in cycleQ if 0 < dQ[v] <= max_blue_dist]
        blue_order.sort(key=lambda v: dQ[v], reverse=True)

    # Merge sequences to find minimum number of operations
    i = j = 0
    ops = 0
    a = len(red_order)
    b = len(blue_order)
    while i < a or j < b:
        if i < a and j < b and red_order[i] == blue_order[j]:
            ops += 1
            i += 1
            j += 1
        elif i < a:
            ops += 1
            i += 1
        else:
            ops += 1
            j += 1
    print(ops)

if __name__ == "__main__":
    main()