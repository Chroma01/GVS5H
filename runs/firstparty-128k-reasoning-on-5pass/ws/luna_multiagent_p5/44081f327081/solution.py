import sys
from array import array

def solve():
    tokens = sys.stdin.buffer.read().split()
    it = iter(tokens)
    n = int(next(it))
    k = int(next(it))
    a = array('I', (int(x) for x in it))
    del tokens

    m = max(a)

    freq = array('I', [0]) * (m + 1)
    distinct = 0
    for x in a:
        if freq[x] == 0:
            distinct += 1
        freq[x] += 1

    feasible = bytearray(m + 1)

    for d in range(1, m + 1):
        total = 0
        x = d
        while x <= m:
            total += freq[x]
            x += d
        if total >= k:
            feasible[d] = 1

    ans = array('I', [0]) * (m + 1)
    remaining = distinct

    for d in range(m, 0, -1):
        if feasible[d]:
            x = d
            while x <= m:
                if freq[x]:
                    ans[x] = d
                    freq[x] = 0
                    remaining -= 1
                x += d
            if remaining == 0:
                break

    out = bytearray()
    for x in a:
        out.extend(str(ans[x]).encode())
        out.append(10)
    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    solve()