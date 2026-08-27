import sys
import math
from array import array

def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)
    k = next(it)
    a = array('I', it)
    del it

    if k == 1:
        sys.stdout.write('\n'.join(map(str, a)))
        sys.stdout.write('\n')
        return

    if k == n:
        g = 0
        for x in a:
            g = math.gcd(g, x)
        sys.stdout.write((str(g) + '\n') * n)
        return

    m = max(a)
    freq = [0] * (m + 1)
    present = []

    for x in a:
        if freq[x] == 0:
            present.append(x)
        freq[x] += 1

    cnt = [0] * (m + 1)
    limit = m + 1

    for d in range(1, limit):
        total = 0
        for x in range(d, limit, d):
            total += freq[x]
        cnt[d] = total

    ans = [0] * (m + 1)
    remaining = len(present)

    for d in range(m, 0, -1):
        if cnt[d] < k:
            continue
        for x in range(d, limit, d):
            if freq[x] and ans[x] == 0:
                ans[x] = d
                remaining -= 1
        if remaining == 0:
            break

    sys.stdout.write('\n'.join(str(ans[x]) for x in a))
    sys.stdout.write('\n')

if __name__ == "__main__":
    solve()