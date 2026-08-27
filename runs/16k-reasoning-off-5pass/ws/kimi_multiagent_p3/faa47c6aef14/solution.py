import sys
from bisect import bisect_left

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    A = [int(data[idx + i]) for i in range(N)]; idx += N
    B = [int(data[idx + i]) for i in range(N)]; idx += N
    P = [int(data[idx + i]) for i in range(N)]; idx += N
    Q = [int(data[idx + i]) for i in range(N)]; idx += N

    def build_chain(perm, balls):
        # Walk the cycle containing X in perm, starting from X.
        # order[k] = c_k where c_0 = X, c_{k+1} = perm[c_k - 1] (1-indexed boxes).
        # Since perm is a permutation, the walk from X must return to X,
        # so termination is guaranteed and the loop closes exactly at X.
        pos = [-1] * (N + 1)  # pos[v] = k if v is the k-th node on X's cycle, -1 otherwise
        order = []
        v = X
        while pos[v] == -1:
            pos[v] = len(order)
            order.append(v)
            v = perm[v - 1]
        L = len(order)
        dmax = 0
        for i in range(1, N + 1):
            if balls[i - 1] > 0:
                if pos[i] == -1:
                    return None  # this ball can never reach X
                d = (L - pos[i]) % L  # steps from box i to X along perm
                if d > dmax:
                    dmax = d
        # Chain: every box with distance 1..dmax must be operated, in decreasing
        # distance order. distance(order[k]) = (L - k) % L, so decreasing distance
        # corresponds to increasing k for k >= 1; need L - k <= dmax => k >= L - dmax.
        # When dmax == 0 (no balls of this color, or all already at X), chain is empty.
        chain = [order[k] for k in range(max(1, L - dmax), L)]
        return chain

    R = build_chain(P, A)
    if R is None:
        print(-1)
        return
    Bch = build_chain(Q, B)
    if Bch is None:
        print(-1)
        return

    # Minimum operations = shortest common supersequence length of the two chains
    # = |R| + |Bch| - |LCS(R, Bch)|.
    # Chains have distinct elements, so LCS reduces to LIS:
    # map each element to its index in R, then take the LIS of the indices of
    # Bch's elements that also appear in R.
    index_in_R = {}
    for i, v in enumerate(R):
        index_in_R[v] = i
    seq = []
    for v in Bch:
        j = index_in_R.get(v)
        if j is not None:
            seq.append(j)
    # Strictly increasing LIS via patience sorting.
    tails = []
    for x in seq:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    lcs = len(tails)
    print(len(R) + len(Bch) - lcs)

solve()