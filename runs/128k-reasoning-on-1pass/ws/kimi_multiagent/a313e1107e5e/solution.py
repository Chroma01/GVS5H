import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, q = data[0], data[1]
    A = [0] * (n + 1)

    p = 2
    for i in range(1, n + 1):
        A[i] = data[p]
        p += 1

    queries = []
    for qi in range(q):
        R = data[p]
        X = data[p + 1]
        p += 2
        queries.append((X, R, qi))

    # dp[i] = LIS length ending at i (strictly increasing values)
    comp = {v: i + 1 for i, v in enumerate(sorted(set(A[1:])))}
    m = len(comp)
    bit_val = [0] * (m + 1)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        c = comp[A[i]]

        best = 0
        j = c - 1
        while j > 0:
            if bit_val[j] > best:
                best = bit_val[j]
            j -= j & -j

        d = best + 1
        dp[i] = d

        j = c
        while j <= m:
            if d > bit_val[j]:
                bit_val[j] = d
            j += j & -j

    # Offline: activate positions by A_i <= X, query max dp among indices <= R
    order = sorted(range(1, n + 1), key=A.__getitem__)
    queries.sort()

    bit_idx = [0] * (n + 1)
    ans = [0] * q
    ptr = 0

    for X, R, qi in queries:
        while ptr < n and A[order[ptr]] <= X:
            i = order[ptr]
            d = dp[i]
            j = i
            while j <= n:
                if d > bit_idx[j]:
                    bit_idx[j] = d
                j += j & -j
            ptr += 1

        res = 0
        j = R
        while j > 0:
            if bit_idx[j] > res:
                res = bit_idx[j]
            j -= j & -j

        ans[qi] = res

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()