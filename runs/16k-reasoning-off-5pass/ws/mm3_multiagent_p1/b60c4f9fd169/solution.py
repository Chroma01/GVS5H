import sys

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    K = int(data[0].strip())
    S = data[1].strip()
    T = data[2].strip()
    n = len(S)
    m = len(T)

    # Quick reject if length difference exceeds K
    if abs(n - m) > K:
        print("No")
        return

    # Ensure |S| <= |T| to minimise work
    if n > m:
        S, T = T, S
        n, m = m, n

    # Now we compute bounded edit distance with threshold K
    INF = K + 1  # any value > K is treated as INF

    # dp[i] will hold the value for the previous column at row i
    # We only need rows within the band [|j-K|, j+K] intersected with [0, n]
    # We'll store a full array of size n+1 for simplicity, but only fill the band.
    prev = [INF] * (n + 1)
    # Base column j=0: converting S[:i] to empty string costs i deletions
    for i in range(min(n, K) + 1):
        prev[i] = i
    # Rows beyond K are INF, already set.

    # Early exit check: if converting S to T requires 0 ops?
    if n == m and S == T:
        print("Yes")
        return

    # Process columns j = 1 .. m
    for j in range(1, m + 1):
        lo = max(0, j - K)   # minimum i we need to consider
        hi = min(n, j + K)   # maximum i we need to consider

        # Allocate current column, initially INF
        curr = [INF] * (n + 1)

        # If j is within the band, dp[0][j] = j (cost of inserting j chars)
        if 0 >= lo:  # i=0 is in range only if 0 >= lo
            curr[0] = j if j <= K else INF

        # Iterate over rows i in [lo, hi]
        # We must be careful: when i=0 we already handled.
        start = max(lo, 1)
        for i in range(start, hi + 1):
            # deletion: prev[i] + 1
            del_cost = prev[i] + 1
            # insertion: curr[i-1] + 1
            ins_cost = curr[i - 1] + 1
            # replace/match: prev[i-1] + (S[i-1] != T[j-1])
            sub_cost = prev[i - 1] + (0 if S[i - 1] == T[j - 1] else 1)

            best = del_cost
            if ins_cost < best:
                best = ins_cost
            if sub_cost < best:
                best = sub_cost

            if best > K:
                best = INF
            curr[i] = best

        # Early termination: if we have reached the final cell and its value <= K
        if j == m and curr[n] <= K:
            print("Yes")
            return

        # Prepare for next column: swap arrays
        prev = curr

    # After processing all columns, check the last column at row n
    if prev[n] <= K:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()