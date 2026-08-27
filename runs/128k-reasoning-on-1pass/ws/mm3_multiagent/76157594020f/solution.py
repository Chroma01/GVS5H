import random, itertools, math

def brute_min_length(s, numOps):
    n = len(s)
    best = n  # max possible run length
    # iterate over all masks of flips
    for mask in range(1 << n):
        if bin(mask).count('1') > numOps:
            continue
        # construct flipped string
        t = list(s)
        flips = 0
        for i in range(n):
            if (mask >> i) & 1:
                t[i] = '1' if t[i] == '0' else '0'
        # compute longest run
        cur = 1
        max_run = 1
        for i in range(1, n):
            if t[i] == t[i-1]:
                cur += 1
            else:
                cur = 1
            if cur > max_run:
                max_run = cur
        if max_run < best:
            best = max_run
    return best

def feasible_dp(L, s, numOps):
    n = len(s)
    if L >= n:
        return True
    INF = 10**9
    # dp0[k] = min flips to end with a run of 0 of length k (1..L)
    dp0 = [INF] * (L+1)
    dp1 = [INF] * (L+1)
    # init first character
    c0 = 0 if s[0] == '0' else 1
    c1 = 1 - c0
    dp0[1] = c0
    dp1[1] = c1
    for i in range(1, n):
        c0 = 0 if s[i] == '0' else 1
        c1 = 1 - c0
        # compute min over any run length for each bit from previous dp
        minPrev0 = min(dp0[1:])  # min flips ending with 0
        minPrev1 = min(dp1[1:])  # min flips ending with 1
        ndp0 = [INF] * (L+1)
        ndp1 = [INF] * (L+1)
        # start a new run of length 1 of bit 0: previous must be bit 1
        ndp0[1] = minPrev1 + c0
        # start a new run of length 1 of bit 1: previous must be bit 0
        ndp1[1] = minPrev0 + c1
        # continue the same bit
        for k in range(2, L+1):
            val = dp0[k-1] + c0
            if val < ndp0[k]:
                ndp0[k] = val
            val = dp1[k-1] + c1
            if val < ndp1[k]:
                ndp1[k] = val
        dp0, dp1 = ndp0, ndp1
    minFlips = min(min(dp0[1:]), min(dp1[1:]))
    return minFlips <= numOps

def solve_min_length(s, numOps):
    n = len(s)
    low, high = 1, n
    while low < high:
        mid = (low + high) // 2
        if feasible_dp(mid, s, numOps):
            high = mid
        else:
            low = mid + 1
    return low

# Test against brute force for many random small cases
def test():
    for n in range(1, 9):
        for _ in range(200):
            s = ''.join(random.choice('01') for _ in range(n))
            for ops in range(0, n+1):
                brute = brute_min_length(s, ops)
                fast = solve_min_length(s, ops)
                if brute != fast:
                    print("Mismatch!", s, ops, brute, fast)
                    return
    print("All random tests passed.")

test()