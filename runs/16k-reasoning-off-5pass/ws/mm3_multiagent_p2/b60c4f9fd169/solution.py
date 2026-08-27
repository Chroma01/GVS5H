import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)
    if abs(n - m) > K:
        print("No")
        return
    # Banded Ukkonen DP: only cells where |i - j| <= K
    # width of band = 2K + 1
    width = 2 * K + 1
    INF = K + 1  # any value > K is enough
    # Initialize row 0
    # For i=0, valid j are 0..min(m, K)
    prev = [INF] * width
    for j in range(min(m, K) + 1):
        prev[j + K] = j  # offset = j - (0 - K) = j + K
    # Iterate rows
    for i in range(1, n + 1):
        cur = [INF] * width
        j_start = max(0, i - K)
        j_end = min(m, i + K)
        # We need to set the left boundary of the row:
        # dp[i][j_start-1] is out of band, so insert from "infinity"
        # But dp[i][j_start] should be dp[i-1][j_start] + 1 (delete)
        # Actually, for the first valid j (j_start), we must ensure cur[offset_start-1] is large
        # so that insert is not chosen incorrectly. Since cur is initialized to INF,
        # cur[offset_start-1] is INF (out of band or before start).
        for j in range(j_start, j_end + 1):
            offset = j - (i - K)
            # Delete: dp[i-1][j] + 1
            del_cost = prev[offset] + 1
            # Insert: dp[i][j-1] + 1
            ins_cost = cur[offset - 1] + 1
            # Substitute/Match: dp[i-1][j-1] + (0 if match else 1)
            if S[i-1] == T[j-1]:
                sub_cost = prev[offset - 1]
            else:
                sub_cost = prev[offset - 1] + 1
            cur[offset] = min(del_cost, ins_cost, sub_cost)
        prev = cur
    # Check dp[n][m]
    offset_m = m - (n - K)
    if 0 <= offset_m < width and prev[offset_m] <= K:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()