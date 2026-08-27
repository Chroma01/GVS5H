import sys

MOD = 998244353


class WeightedDSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.xor_to_parent = [0] * n
        self.components = n
        self.ok = True

    def find(self, x):
        if self.parent[x] == x:
            return x, 0
        p = self.parent[x]
        r, v = self.find(p)
        self.xor_to_parent[x] ^= v
        self.parent[x] = r
        return self.parent[x], self.xor_to_parent[x]

    def union(self, a, b, w):
        ra, xa = self.find(a)
        rb, xb = self.find(b)

        if ra == rb:
            if (xa ^ xb) != w:
                self.ok = False
            return

        # If rb becomes a child of ra, then:
        # value[rb] xor value[ra] = xa xor xb xor w.
        rel = xa ^ xb ^ w

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
            # Reversing the relation does not change XOR parity.
        self.parent[rb] = ra
        self.xor_to_parent[rb] = rel
        self.size[ra] += self.size[rb]
        self.components -= 1


def solve():
    input = sys.stdin.buffer.readline
    t = int(input())
    answers = []

    for _ in range(t):
        h, w = map(int, input().split())
        grid = [input().strip() for _ in range(h)]

        dsu = WeightedDSU(h + w)
        col_prefix = [0] * w
        bad = False

        for r in range(h):
            row_prefix = 0
            row_parity = 0
            for c, ch in enumerate(grid[r]):
                is_a = 1 if ch == 65 else 0  # ord('A') == 65

                if is_a:
                    row_parity ^= 1

                # x[r,c] = row variable xor row_prefix
                # y[r,c] = column variable xor col_prefix[c]
                if not is_a:
                    rhs = 1 ^ row_prefix ^ col_prefix[c]
                    dsu.union(r, h + c, rhs)

                row_prefix ^= is_a
                col_prefix[c] ^= is_a

            if row_parity:
                bad = True

        for value in col_prefix:
            if value:
                bad = True

        if not dsu.ok:
            bad = True

        if bad:
            answers.append("0")
        else:
            answers.append(str(pow(2, dsu.components, MOD)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()