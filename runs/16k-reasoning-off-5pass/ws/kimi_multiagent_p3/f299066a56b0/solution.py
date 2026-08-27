import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    half = n // 2
    i = 0          # pointer over smallest half (tops)
    j = half       # pointer over larger half (bottoms)
    pairs = 0
    while i < half and j < n:
        if 2 * a[i] <= a[j]:
            pairs += 1
            i += 1
            j += 1
        else:
            j += 1
    sys.stdout.write(str(pairs) + "\n")

solve()