import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [int(next(it)) for _ in range(N)]
    # pos[x] = current index of value x (1-indexed)
    pos = [0] * (N + 1)
    for i, v in enumerate(P, 1):
        pos[v] = i

    class Fenwick:
        __slots__ = ('n', 'bit')
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, delta):
            n = self.n
            bit = self.bit
            while i <= n:
                bit[i] += delta
                i += i & -i
        def sum(self, i):
            s = 0
            bit = self.bit
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s

    bit = Fenwick(N)
    for i in range(1, N + 1):
        bit.add(i, 1)

    total = 0
    for v in range(1, N + 1):
        # current position of v = (v-1) filled slots to the left + number of free slots up to original pos[v]
        cur = (v - 1) + bit.sum(pos[v])
        steps = cur - v
        if steps > 0:
            total += steps * (v + cur - 1) // 2
        bit.add(pos[v], -1)

    print(total)

if __name__ == "__main__":
    solve()