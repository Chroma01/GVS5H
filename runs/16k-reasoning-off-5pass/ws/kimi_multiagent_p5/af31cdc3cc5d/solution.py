import sys
import random

def solve_formula(A):
    s = sorted(A)
    n = len(s)
    k = n // 2
    return sum(s[n - k:]) - sum(s[:k])

def solve_dp(A):
    n = len(A)
    NEG = -1
    dp = [[0] * n for _ in range(n)]
    # dp[l][r] = best score using only elements in A[l..r], possibly leaving some unmatched
    # Recurrence: dp[l][r] = max(dp[l+1][r], max over k in (l+1..r) of |A[l]-A[k]| + dp[l+1][k-1] + dp[k+1][r])
    # This is the standard non-crossing matching DP (O(N^3) worst case but fine for tiny N).
    for length in range(1, n + 1):
        for l in range(0, n - length + 1):
            r = l + length - 1
            best = dp[l + 1][r] if l + 1 <= r else 0
            for k in range(l + 1, r + 1):
                left = dp[l + 1][k - 1] if l + 1 <= k - 1 else 0
                right = dp[k + 1][r] if k + 1 <= r else 0
                cand = abs(A[l] - A[k]) + left + right
                if cand > best:
                    best = cand
            dp[l][r] = best
    return dp[0][n - 1]

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    print(solve_formula(A))

if __name__ == "__main__":
    # Stress test harness (only runs when executed directly with an argument "stress")
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        random.seed(12345)
        bad = 0
        for trial in range(20000):
            n = random.randint(2, 12)
            A = [random.randint(1, 8) for _ in range(n)]
            f = solve_formula(A)
            d = solve_dp(A)
            if f != d:
                bad += 1
                print("MISMATCH", A, "formula=", f, "dp=", d)
                if bad > 5:
                    break
        print("done, mismatches:", bad)
    else:
        main()