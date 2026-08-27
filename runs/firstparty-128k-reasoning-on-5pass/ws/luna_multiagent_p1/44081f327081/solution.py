import sys
from array import array

def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)
    k = next(it)

    values = array('i')
    maximum = 0
    for _ in range(n):
        x = next(it)
        values.append(x)
        if x > maximum:
            maximum = x

    size = maximum + 1
    freq = array('i', [0]) * size
    for x in values:
        freq[x] += 1

    count = array('i', [0]) * size
    for d in range(1, size):
        total = 0
        for multiple in range(d, size, d):
            total += freq[multiple]
        count[d] = total

    answer = array('i', [0]) * size
    for d in range(maximum, 0, -1):
        if count[d] < k:
            continue
        for multiple in range(d, size, d):
            if freq[multiple] and answer[multiple] == 0:
                answer[multiple] = d

    out = bytearray()
    for x in values:
        out.extend(str(answer[x]).encode())
        out.append(10)
    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    solve()