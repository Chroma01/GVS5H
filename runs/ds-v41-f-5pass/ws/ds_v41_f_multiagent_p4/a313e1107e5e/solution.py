import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    q = int(data[pos]); pos += 1

    A = [int(data[pos + i]) for i in range(n)]
    pos += n

    # --- Step 1: dp[i] = length of longest strictly increasing subsequence ending at i ---
    vals = sorted(set(A))
    comp = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed compression
    m = len(vals)

    bit = [0] * (m + 1)  # Fenwick tree for prefix maximum over values
    dp = [0] * n
    for i in range(n):
        c = comp[A[i]]
        # query max over values strictly less than A[i] -> compressed prefix c-1
        best = 0
        j = c - 1
        while j > 0:
            v = bit[j]
            if v > best:
                best = v
            j -= j & (-j)
        d = best + 1
        dp[i] = d
        # point update at c with max
        j = c
        while j <= m:
            if bit[j] < d:
                bit[j] = d
            j += j & (-j)

    # --- Step 2: answer queries = max dp[i] with i <= R and A[i] <= X (offline) ---
    order = sorted(range(n), key=lambda i: A[i])

    queries = []
    for k in range(q):
        R = int(data[pos]); pos += 1
        X = int(data[pos]); pos += 1
        queries.append((X, R, k))
    queries.sort()

    bit2 = [0] * (n + 1)  # Fenwick tree for prefix maximum over positions
    ans = [0] * q

    ptr = 0
    for X, R, k in queries:
        while ptr < n and A[order[ptr]] <= X:
            i = order[ptr]
            d = dp[i]
            j = i + 1
            while j <= n:
                if bit2[j] < d:
                    bit2[j] = d
                j += j & (-j)
            ptr += 1
        best = 0
        j = R
        while j > 0:
            v = bit2[j]
            if v > best:
                best = v
            j -= j & (-j)
        ans[k] = best

    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

main()