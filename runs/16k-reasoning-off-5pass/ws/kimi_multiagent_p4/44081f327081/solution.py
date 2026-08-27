import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    m = max(a)

    f = [0] * (m + 1)
    for v in a:
        f[v] += 1

    # cnt[d] = number of elements divisible by d
    cnt = [0] * (m + 1)
    for d in range(1, m + 1):
        s = f[d::d]
        if s:
            cnt[d] = sum(s)

    # best[x] = largest divisor d of x with cnt[d] >= K
    # iterate d ascending, overwrite multiples: last (largest) qualifying d wins
    best = [0] * (m + 1)
    for d in range(1, m + 1):
        if cnt[d] >= k:
            best[d::d] = [d] * len(best[d::d])

    out = sys.stdout
    out.write('\n'.join(map(str, (best[v] for v in a))))
    out.write('\n')

solve()