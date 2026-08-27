import sys

def main():
    data = sys.stdin.buffer.read().split()
    k = int(data[0])
    s = data[1]
    t = data[2]

    n = len(s)
    m = len(t)

    if abs(n - m) > k:
        print("No")
        return

    if s == t:
        print("Yes")
        return

    # Edit distance is symmetric; iterating over the shorter string slightly
    # reduces work when the lengths differ.
    if n > m:
        s, t = t, s
        n, m = m, n

    cap = k + 1

    # Index for diagonal d = j - i is off + d.
    # Two sentinel cells allow accesses to p-1 and p+1 at band boundaries.
    off = k + 1
    width = 2 * k + 3

    prev = [cap] * width
    curr = [cap] * width

    # DP row i = 0: dp[0][j] = j.
    initial_hi = min(k, m)
    for d in range(initial_hi + 1):
        prev[off + d] = d

    prev_lo = 0
    prev_hi = initial_hi

    for i in range(1, n + 1):
        lo = max(-k, -i)
        hi = min(k, m - i)
        ch = s[i - 1]

        # In the middle portion, the whole band is valid, so avoid
        # validity checks for each DP state.
        if lo == -k and hi == k:
            for d in range(-k, k + 1):
                p = off + d

                best = prev[p + 1] + 1       # delete from S
                value = curr[p - 1] + 1      # insert into S
                if value < best:
                    best = value

                value = prev[p] + (ch != t[i + d - 1])  # replace/match
                if value < best:
                    best = value

                curr[p] = best if best <= cap else cap
        else:
            for d in range(lo, hi + 1):
                p = off + d
                j = i + d
                best = cap

                # dp[i-1][j] + 1
                if prev_lo <= d + 1 <= prev_hi:
                    value = prev[p + 1] + 1
                    if value < best:
                        best = value

                # dp[i][j-1] + 1
                if d - 1 >= lo:
                    value = curr[p - 1] + 1
                    if value < best:
                        best = value

                # dp[i-1][j-1] + (S[i-1] != T[j-1])
                if j > 0 and prev_lo <= d <= prev_hi:
                    value = prev[p] + (ch != t[j - 1])
                    if value < best:
                        best = value

                curr[p] = best

        prev, curr = curr, prev
        prev_lo, prev_hi = lo, hi

    target_diagonal = m - n
    print("Yes" if prev[off + target_diagonal] <= k else "No")

if __name__ == "__main__":
    main()