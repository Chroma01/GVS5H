import sys
from array import array

def solve():
    tokens = sys.stdin.buffer.read().split()
    n = int(tokens[0])
    k = int(tokens[1])
    a = array('i', (int(x) for x in tokens[2:]))
    del tokens

    if k == 1:
        sys.stdout.write("\n".join(map(str, a)))
        return

    m = max(a)
    size = m + 1

    freq = array('i', [0]) * size
    distinct = 0
    for x in a:
        if freq[x] == 0:
            distinct += 1
        freq[x] += 1

    support = array('i', [0]) * size
    f = freq
    spt = support

    for d in range(1, size):
        total = 0
        for x in range(d, size, d):
            total += f[x]
        spt[d] = total

    best = array('i', [0]) * size
    remaining = distinct

    for d in range(m, 0, -1):
        if spt[d] < k:
            continue
        for x in range(d, size, d):
            if f[x] and best[x] == 0:
                best[x] = d
                remaining -= 1
        if remaining == 0:
            break

    sys.stdout.write("".join(str(best[x]) + "\n" for x in a))

if __name__ == "__main__":
    solve()