import sys


def main():
    data = sys.stdin.buffer.read().split()
    k = int(data[0])
    s = data[1].decode()
    t = data[2].decode()

    if abs(len(s) - len(t)) > k:
        print("No")
        return

    # Remove a common prefix and suffix.
    left = 0
    common = min(len(s), len(t))
    while left < common and s[left] == t[left]:
        left += 1

    right_s = len(s)
    right_t = len(t)
    while right_s > left and right_t > left and s[right_s - 1] == t[right_t - 1]:
        right_s -= 1
        right_t -= 1

    s = s[left:right_s]
    t = t[left:right_t]

    # Use the longer string as the row dimension.
    if len(s) < len(t):
        s, t = t, s

    n = len(s)
    m = len(t)

    if abs(n - m) > k:
        print("No")
        return

    if n == 0:
        print("Yes")
        return

    inf = k + 1

    # Row 0: dp[0][j] = j inside the band.
    prev_lo = 0
    prev_hi = min(m, k)
    prev = [inf, inf] + list(range(prev_hi + 1)) + [inf, inf]

    for i in range(1, n + 1):
        lo = max(0, i - k)
        hi = min(m, i + k)
        width = hi - lo + 1
        cur = [inf] * (width + 4)
        ch = s[i - 1]

        for idx, j in enumerate(range(lo, hi + 1)):
            deletion = prev[j - prev_lo + 2] + 1
            insertion = cur[idx + 1] + 1

            # There is no replacement transition for j == 0:
            # dp[i][0] can only be reached through deletions.
            if j == 0:
                replacement = inf
            else:
                replacement = prev[j - prev_lo + 1] + (ch != t[j - 1])

            best = deletion
            if insertion < best:
                best = insertion
            if replacement < best:
                best = replacement

            cur[idx + 2] = best

        prev = cur
        prev_lo = lo

        if min(cur) > k:
            print("No")
            return

    print("Yes" if prev[m - prev_lo + 2] <= k else "No")


if __name__ == "__main__":
    main()