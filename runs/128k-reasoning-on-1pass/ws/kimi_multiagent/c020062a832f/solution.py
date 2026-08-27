import sys

class BIT:
    __slots__ = ("n", "tree")
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, v):
        tree = self.tree
        n = self.n
        while i <= n:
            tree[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        tree = self.tree
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    A = data[2:2 + N]

    bit = BIT(M)
    ans = 0
    seen = 0
    for a in A:
        # previous elements strictly greater than a
        ans += seen - bit.sum(a + 1)
        bit.add(a + 1, 1)
        seen += 1

    # delta[v]: change in inversion count when all positions with value v wrap
    # from M-1 to 0. For position p: (p-1) - (N-p) = 2*p - N - 1.
    delta = [0] * M
    base = -N - 1
    for p, a in enumerate(A, 1):
        delta[a] += 2 * p + base

    out = []
    for k in range(M):
        out.append(str(ans))
        if k + 1 < M:
            ans += delta[M - 1 - k]

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()