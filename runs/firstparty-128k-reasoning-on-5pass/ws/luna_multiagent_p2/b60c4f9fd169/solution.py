import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    k = int(data[0])
    s = data[1].decode()
    t = data[2].decode()

    if abs(len(s) - len(t)) > k:
        print("No")
        return

    # Process the shorter string by rows to minimize the number of iterations.
    if len(s) > len(t):
        s, t = t, s

    n = len(s)
    m = len(t)
    inf = 10**9

    prev = [inf] * (m + 1)
    curr = [inf] * (m + 1)

    initial_hi = min(m, k)
    for j in range(initial_hi + 1):
        prev[j] = j
    if initial_hi < m:
        prev[initial_hi + 1] = inf

    for i in range(1, n + 1):
        lo = max(0, i - k)
        hi = min(m, i + k)

        if lo > 0:
            curr[lo - 1] = inf
        if hi < m:
            curr[hi + 1] = inf

        si = s[i - 1]

        if lo == 0:
            curr[0] = i
            j = 1
        else:
            j = lo

        while j <= hi:
            deletion = prev[j] + 1
            insertion = curr[j - 1] + 1
            replacement = prev[j - 1] + (si != t[j - 1])

            best = deletion
            if insertion < best:
                best = insertion
            if replacement < best:
                best = replacement

            curr[j] = best
            j += 1

        prev, curr = curr, prev

    print("Yes" if prev[m] <= k else "No")


if __name__ == "__main__":
    main()