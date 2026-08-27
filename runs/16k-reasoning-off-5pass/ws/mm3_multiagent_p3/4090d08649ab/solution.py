import sys

def solve():
    import sys
    input = sys.stdin.readline
    N_line = input().strip()
    while N_line == '':
        N_line = input().strip()
    N = int(N_line)
    A = list(map(int, input().split()))
    # positions for each value 1..N
    pos = [[] for _ in range(N + 1)]
    for idx, v in enumerate(A, start=1):
        pos[v].append(idx)

    total = N * (N + 1) // 2  # total number of subarrays

    # compute missing[v] for all v = 1..N
    missing = [0] * (N + 1)
    for v in range(1, N + 1):
        lst = pos[v]
        if not lst:
            missing[v] = total
        else:
            prev = 0
            miss = 0
            for p in lst:
                gap = p - prev - 1
                if gap:
                    miss += gap * (gap + 1) // 2
                prev = p
            # after last occurrence
            gap = N - prev
            if gap:
                miss += gap * (gap + 1) // 2
            missing[v] = miss

    # sumC = Σ_v (total - missing[v])
    sum_missing = sum(missing[1:])  # ignore index 0
    sumC = N * total - sum_missing

    # compute Σ J over adjacent pairs
    sumJ = 0
    # for each v, merge pos[v] and pos[v+1]
    # we'll reuse pointers by iterating v from 1 to N-1
    for v in range(1, N):
        P = pos[v]
        Q = pos[v + 1]
        if not P or not Q:
            # join is zero because at least one value missing
            continue
        # missing_v and missing_{v+1} are already computed
        miss_v = missing[v]
        miss_w = missing[v + 1]
        # merge to compute missing_both
        i = 0
        j = 0
        prev = 0
        miss_both = 0
        lenP = len(P)
        lenQ = len(Q)
        while i < lenP or j < lenQ:
            if j == lenQ or (i < lenP and P[i] < Q[j]):
                cur = P[i]
                i += 1
            else:
                cur = Q[j]
                j += 1
            gap = cur - prev - 1
            if gap:
                miss_both += gap * (gap + 1) // 2
            prev = cur
        # after processing all positions
        gap = N - prev
        if gap:
            miss_both += gap * (gap + 1) // 2
        # join count
        join = total - miss_v - miss_w + miss_both
        sumJ += join

    ans = sumC - sumJ
    print(ans)

if __name__ == "__main__":
    solve()