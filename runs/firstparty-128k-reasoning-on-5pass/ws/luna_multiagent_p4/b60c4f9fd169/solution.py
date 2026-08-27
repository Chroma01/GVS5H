import sys

def main():
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = data[1]
    T = data[2]

    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        print("No")
        return

    INF = K + 1
    width = 2 * K + 1

    prev_lo = 0
    prev_hi = min(m, K)
    prev = [INF] * width
    for j in range(prev_lo, prev_hi + 1):
        prev[j - prev_lo] = j

    for i in range(1, n + 1):
        lo = max(0, i - K)
        hi = min(m, i + K)
        cur = [INF] * width

        for j in range(lo, hi + 1):
            idx = j - lo

            if j == 0:
                cur[idx] = i
                continue

            best = INF

            # Delete S[i-1].
            if prev_lo <= j <= prev_hi:
                best = min(best, prev[j - prev_lo] + 1)

            # Insert T[j-1].
            if j - 1 >= lo:
                best = min(best, cur[idx - 1] + 1)

            # Match or replace.
            if prev_lo <= j - 1 <= prev_hi:
                cost = 0 if S[i - 1] == T[j - 1] else 1
                best = min(best, prev[j - 1 - prev_lo] + cost)

            cur[idx] = min(best, INF)

        prev = cur
        prev_lo = lo
        prev_hi = hi

    print("Yes" if prev_lo <= m <= prev_hi and prev[m - prev_lo] <= K else "No")


if __name__ == "__main__":
    main()