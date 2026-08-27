import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    q = int(data[0])
    queries = list(map(int, data[1:1 + q]))
    if not queries:
        return
    max_a = max(queries)
    # largest integer m with m*m <= max_a
    limit = int(max_a ** 0.5)
    while (limit + 1) * (limit + 1) <= max_a:
        limit += 1
    while limit * limit > max_a:
        limit -= 1

    # smallest prime factor sieve up to `limit`
    spf = list(range(limit + 1))
    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:  # i is prime
            step = i
            start = i * i
            for j in range(start, limit + 1, step):
                if spf[j] == j:
                    spf[j] = i

    # distinct prime factor count via recurrence
    # cnt[x] = cnt[x // spf[x]] + (1 if spf[x // spf[x]] != spf[x] else 0)
    cnt = [0] * (limit + 1)
    squares = []
    for x in range(2, limit + 1):
        p = spf[x]
        y = x // p
        c = cnt[y] + (1 if y > 1 and spf[y] != p else (1 if y == 1 else 0))
        # simpler: if y == 1, x is prime -> 1 distinct; handled below
        cnt[x] = c
    # The recurrence above is slightly convoluted; recompute cleanly.
    cnt[1] = 0
    for x in range(2, limit + 1):
        p = spf[x]
        y = x // p
        if y == 1:
            cnt[x] = 1
        elif spf[y] == p:
            cnt[x] = cnt[y]
        else:
            cnt[x] = cnt[y] + 1
        if cnt[x] == 2:
            squares.append(x * x)

    squares.sort()
    out = []
    for a in queries:
        idx = bisect_right(squares, a) - 1
        out.append(str(squares[idx]))
    sys.stdout.write("\n".join(out) + "\n")

main()