```python
import sys

class BIT:
    __slots__ = ("n", "tree")
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    def add(self, i, v):
        n = self.n
        tree = self.tree
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

    pos = [[] for _ in range(M)]
    for i, a in enumerate(A, 1):
        pos[a].append(i)

    bit = BIT(M)
    ans = 0
    seen = 0
    for a in A:
        ans += seen - bit.sum(a + 1)  # previous values > a
        bit.add(a + 1, 1)
        seen += 1

    delta = [0] * M
    for v in range(1, M):
        s = 0
        for p in pos[v]:
            s += 2 * p - N - 1
        delta[v] = s

    out = []
    for k in range(M):
        out.append(str(ans))
        if k + 1 < M:
            ans += delta[M - k - 1]

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```