import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    k = int(data[0])
    s = data[1]
    t = data[2]

    if abs(len(s) - len(t)) > k:
        print("No")
        return

    # Remove common prefix.
    left = 0
    ls = len(s)
    lt = len(t)
    while left < ls and left < lt and s[left] == t[left]:
        left += 1

    # Remove common suffix without overlapping the removed prefix.
    rs = ls
    rt = lt
    while rs > left and rt > left and s[rs - 1] == t[rt - 1]:
        rs -= 1
        rt -= 1

    s = s[left:rs]
    t = t[left:rt]

    # Edit distance is symmetric; fewer DP rows is preferable.
    if len(s) > len(t):
        s, t = t, s

    n = len(s)
    m = len(t)

    if m - n > k:
        print("No")
        return

    if n == 0:
        print("Yes" if m <= k else "No")
        return

    inf = k + 1
    width = 2 * k + 1
    offset = k

    # prev[d + offset] is DP[i-1][i-1+d].
    prev = [inf] * width
    for j in range(min(k, m) + 1):
        prev[offset + j] = j

    cur = [inf] * width

    for i in range(1, n + 1):
        low_d = max(-k, -i)
        high_d = min(k, m - i)
        ch = s[i - 1]

        d = low_d
        j = i + d
        while d <= high_d:
            idx = offset + d

            # Substitute / match from DP[i-1][j-1].
            if j > 0:
                best = prev[idx] + (ch != t[j - 1])
            else:
                best = inf

            # Delete from S: DP[i-1][j].
            if d < k:
                value = prev[idx + 1] + 1
                if value < best:
                    best = value

            # Insert into S: DP[i][j-1].
            if j > 0 and d > -k:
                value = cur[idx - 1] + 1
                if value < best:
                    best = value

            cur[idx] = best if best <= k else inf
            d += 1
            j += 1

        prev, cur = cur, prev

    print("Yes" if prev[offset + (m - n)] <= k else "No")


if __name__ == "__main__":
    main()