import sys

MOD = 998244353


class XorDSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.parity = [0] * n  # value[x] xor value[parent[x]]
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            p = self.parent[x]
            r = self.find(p)
            self.parity[x] ^= self.parity[p]
            self.parent[x] = r
        return self.parent[x]

    def union(self, a, b, w):
        # Enforce value[a] xor value[b] == w.
        ra = self.find(a)
        rb = self.find(b)
        xa = self.parity[a]
        xb = self.parity[b]

        if ra == rb:
            return (xa ^ xb) == w

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
            xa, xb = xb, xa

        self.parent[rb] = ra
        self.parity[rb] = xa ^ xb ^ w
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


def solve_case(h, w, grid):
    # p[i] is the first horizontal edge variable of row i.
    # q[j] is the first vertical edge variable of column j.
    dsu = XorDSU(h + w)
    col_prefix = [0] * w
    ok = True

    for i in range(h):
        row_prefix = 0
        s = grid[i]

        for j, ch in enumerate(s):
            # For cell (i,j), the horizontal and vertical common values are:
            # p[i] xor row_prefix and q[j] xor col_prefix[j].
            if ch == 66:  # 'B'
                rhs = 1 ^ row_prefix ^ col_prefix[j]
                if not dsu.union(i, h + j, rhs):
                    ok = False

            if ch == 65:  # 'A'
                row_prefix ^= 1
                col_prefix[j] ^= 1

        # The horizontal variables must be consistent around the row torus.
        if row_prefix:
            ok = False

    # The vertical variables must be consistent around every column torus.
    if any(col_prefix):
        ok = False

    if not ok:
        return 0
    return pow(2, dsu.components, MOD)


def main():
    input = sys.stdin.buffer.readline
    t = int(input())
    answers = []

    for _ in range(t):
        h, w = map(int, input().split())
        grid = [input().strip() for _ in range(h)]
        answers.append(str(solve_case(h, w, grid)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()