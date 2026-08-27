import sys

def solve() -> None:
    data = sys.stdin.read().splitlines()
    if not data:
        return
    K = int(data[0].strip())
    S = data[1].strip()
    T = data[2].strip()
    n = len(S)
    m = len(T)

    # If length difference exceeds K, impossible immediately.
    if abs(n - m) > K:
        print("No")
        return

    # Banded Levenshtein DP. Only cells with |i - j| <= K are needed.
    # Use two rolling arrays of size 2K+1 (max 41), indexed by j - (i - K).
    INF = 10**9
    size = 2 * K + 1

    # Initialize DP for i = 0.
    # Valid j range: 0 .. min(m, K)
    i = 0
    low0 = 0
    high0 = min(m, K)
    offset0 = i - K  # -K
    dp_prev = [INF] * size
    for j in range(low0, high0 + 1):
        dp_prev[j - offset0] = j

    # Process rows i = 1 .. n
    for i in range(1, n + 1):
        dp_cur = [INF] * size
        low = max(0, i - K)
        high = min(m, i + K)
        offset = i - K

        # Base case: j == low == 0 -> DP[i][0] = i (delete all i chars)
        if low == 0:
            dp_cur[0 - offset] = i

        # Compute DP for j in [low+1, high]
        for j in range(low + 1, high + 1):
            # Indices into the rolling arrays.
            # dp_prev represents row i-1; its offset is (i-1)-K.
            # dp_cur represents row i; its offset is i-K.
            idx_up   = j - ((i - 1) - K)          # dp_prev index for (i-1, j)
            idx_left = (j - 1) - offset          # dp_cur index for (i, j-1)
            idx_diag = (j - 1) - ((i - 1) - K)   # dp_prev index for (i-1, j-1)

            # Safely read values; they are guaranteed to be in range because of the band.
            cost_del = dp_prev[idx_up] + 1
            cost_ins = dp_cur[idx_left] + 1
            cost_sub = dp_prev[idx_diag] + (0 if S[i-1] == T[j-1] else 1)

            best = cost_del
            if cost_ins < best:
                best = cost_ins
            if cost_sub < best:
                best = cost_sub

            dp_cur[j - offset] = best

        dp_prev = dp_cur

    # Retrieve DP[n][m].
    i = n
    low = max(0, i - K)
    high = min(m, i + K)
    offset = i - K
    if low <= m <= high:
        dist = dp_prev[m - offset]
    else:
        # This should be unreachable because we already checked |n-m| <= K.
        dist = INF

    print("Yes" if dist <= K else "No")

if __name__ == "__main__":
    solve()