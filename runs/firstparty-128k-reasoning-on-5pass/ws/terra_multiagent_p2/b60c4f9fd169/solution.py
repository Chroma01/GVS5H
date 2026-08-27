import sys


def main():
    data = sys.stdin.read().split()
    if len(data) < 3:
        return

    k = int(data[0])
    s = data[1]
    t = data[2]

    n = len(s)
    m = len(t)

    if abs(n - m) > k:
        print("No")
        return

    inf = k + 1
    offset = k + 1
    width = 2 * k + 3

    # prev[offset + d] = edit distance for the previous row,
    # where d = column - row. Sentinel cells remain inf.
    prev = [inf] * width
    for j in range(min(m, k) + 1):
        prev[offset + j] = j

    for i in range(1, n + 1):
        low_d = max(-k, -i)
        high_d = min(k, m - i)

        cur = [inf] * width
        ch = s[i - 1]
        alive = False

        start = offset + low_d
        end = offset + high_d

        for q in range(start, end + 1):
            d = q - offset
            j = i + d

            # Delete S[i-1]: dp[i-1][j] + 1
            best = prev[q + 1] + 1

            # Insert T[j-1]: dp[i][j-1] + 1
            candidate = cur[q - 1] + 1
            if candidate < best:
                best = candidate

            # Replace/match S[i-1] with T[j-1].
            if j > 0:
                candidate = prev[q] + (ch != t[j - 1])
                if candidate < best:
                    best = candidate

            if best <= k:
                cur[q] = best
                alive = True

        if not alive:
            print("No")
            return

        prev = cur

    answer_diagonal = m - n
    if prev[offset + answer_diagonal] <= k:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()