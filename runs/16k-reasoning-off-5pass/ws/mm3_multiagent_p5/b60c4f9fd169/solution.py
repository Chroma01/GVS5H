import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    n, m = len(S), len(T)
    if abs(n - m) > K:
        print("No")
        return
    size = 2 * K + 1
    INF = K + 1
    # prev_dp corresponds to row i (i characters of S processed)
    # Initialize for i=0: we can only insert characters of T
    prev_dp = [INF] * size
    for d in range(0, min(K, m) + 1):
        prev_dp[d + K] = d if d <= K else INF
    for i in range(1, n + 1):
        dp = [INF] * size
        # Determine the range of d to iterate to avoid unnecessary checks
        # j = i + d must be in [0, m]
        d_min = max(-K, -i)
        d_max = min(K, m - i)
        for d in range(d_min, d_max + 1):
            j = i + d
            idx = d + K
            # match/mismatch
            cost = 0 if S[i-1] == T[j-1] else 1
            best = prev_dp[idx] + cost
            # delete: from (i-1, j) to (i, j), offset d+1
            if idx + 1 < size:
                v = prev_dp[idx+1] + 1
                if v < best:
                    best = v
            # insert: from (i, j-1) to (i, j), offset d-1
            if idx > 0:
                v = dp[idx-1] + 1
                if v < best:
                    best = v
            if best > INF:
                best = INF
            dp[idx] = best
        prev_dp = dp
    # Check final state (n, m): d = m - n
    final_d = m - n
    if -K <= final_d <= K:
        ans = prev_dp[final_d + K]
        if ans <= K:
            print("Yes")
            return
    print("No")

if __name__ == "__main__":
    solve()