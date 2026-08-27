import sys


class DSUParity:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.parity = [0] * n

    def find(self, x):
        if self.parent[x] == x:
            return x
        p = self.parent[x]
        r = self.find(p)
        self.parity[x] ^= self.parity[p]
        self.parent[x] = r
        return r

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        px = self.parity[x]
        py = self.parity[y]

        if rx == ry:
            return

        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
            px, py = py, px

        self.parent[ry] = rx
        self.parity[ry] = px ^ py ^ 1
        self.size[rx] += self.size[ry]


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    dsu = DSUParity(n)
    for _ in range(m):
        u, v = map(int, input().split())
        dsu.union(u - 1, v - 1)

    cnt0 = {}
    cnt1 = {}
    roots = set()

    for v in range(n):
        r = dsu.find(v)
        roots.add(r)
        if dsu.parity[v] == 0:
            cnt0[r] = cnt0.get(r, 0) + 1
        else:
            cnt1[r] = cnt1.get(r, 0) + 1

    odd_roots = []
    for r in roots:
        size = cnt0.get(r, 0) + cnt1.get(r, 0)
        if size & 1:
            odd_roots.append(r)

    odd_count = len(odd_roots)
    component_count = len(roots)

    if odd_count == 0:
        a = sum(cnt0.get(r, 0) for r in roots)
        b = n - a
        remaining = a * b - m
        print("Aoki" if remaining & 1 else "Takahashi")
        return

    if odd_count >= 3:
        print("Takahashi")
        return

    if odd_count == 2:
        print("Aoki")
        return

    # Exactly one odd component.
    # If it is the only component, no merging is possible and the
    # remaining number of moves is fixed.
    if component_count == 1:
        r = odd_roots[0]
        a = cnt0.get(r, 0)
        b = cnt1.get(r, 0)
        remaining = a * b - m
        print("Aoki" if remaining & 1 else "Takahashi")
    else:
        # With one odd component and at least one other component,
        # the first player can choose a merge leading to a losing state.
        print("Aoki")


if __name__ == "__main__":
    solve()