import sys

def solve_case(a):
    # Compress equal consecutive elements: each compressed run can always be
    # deleted in one operation, so only the run-color sequence matters here.
    b = []
    for x in a:
        if not b or b[-1] != x:
            b.append(x)

    m = len(b)
    if m <= 1:
        return m

    # dp[i] stores the best reduction obtainable in the prefix ending at i.
    # The transitions maintain alternating equal-pair structures.  This is a
    # compact implementation of the standard last-occurrence DP.
    #
    # For each value x, best[x] is the best state before a previous occurrence
    # of x.  active[x] stores candidates which have seen x once and are waiting
    # for a second color to complete an alternating structure.
    dp = [0] * (m + 1)
    last = {}
    open_best = {}
    ans = 0

    for i, x in enumerate(b, 1):
        cur = dp[i - 1]

        if x in open_best:
            cur = max(cur, open_best[x] + 1)

        if x in last:
            base = dp[last[x] - 1]
            old = open_best.get(x, -10**9)
            if base > old:
                open_best[x] = base

        last[x] = i
        dp[i] = cur
        if cur > ans:
            ans = cur

    return m - ans

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    p = 1
    out = []
    for _ in range(t):
        n = data[p]
        p += 1
        a = data[p:p + n]
        p += n
        out.append(str(solve_case(a)))
    print("\n".join(out))

if __name__ == "__main__":
    main()