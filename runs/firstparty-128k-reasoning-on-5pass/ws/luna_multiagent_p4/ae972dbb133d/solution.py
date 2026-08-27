import sys

MOD = 998244353


class ParityDSU:
    __slots__ = ("parent", "size", "xr", "components")

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.xr = [0] * n
        self.components = n

    def find(self, x):
        p = self.parent[x]
        if p == x:
            return x, 0
        r, d = self.find(p)
        self.xr[x] ^= d
        self.parent[x] = r
        return r, self.xr[x]

    def union(self, x, y, w):
        rx, dx = self.find(x)
        ry, dy = self.find(y)

        if rx == ry:
            return (dx ^ dy) == w

        if self.size[rx] > self.size[ry]:
            rx, ry = ry, rx
            dx, dy = dy, dx

        self.parent[rx] = ry
        self.xr[rx] = dx ^ dy ^ w
        self.size[ry] += self.size[rx]
        self.components -= 1
        return True


def solve_case(h, w, grid):
    # col_pref[j] stores XOR of A-types in rows 1..current_row-1.
    col_pref = [0] * w
    constraints = []

    for i, row in enumerate(grid):
        row_parity = 0
        horizontal_prefix = 0

        for j, ch in enumerate(row):
            is_a = 1 if ch == "A" else 0
            row_parity ^= is_a

            # Prefix of A-types in columns 1..j.
            if j > 0:
                horizontal_prefix ^= is_a

            if ch == "B":
                # h[i][j] = r_i XOR horizontal_prefix
                # v[i][j] = c_j XOR col_pref[j]
                # Type B requires h[i][j] XOR v[i][j] = 1.
                weight = 1 ^ horizontal_prefix ^ col_pref[j]
                constraints.append((i, h + j, weight))

        if row_parity:
            return 0

        # After processing row i, it contributes to vertical prefixes
        # only when i >= 1; row 0 is absorbed into the column closure test.
        if i >= 1:
            for j, ch in enumerate(row):
                if ch == "A":
                    col_pref[j] ^= 1

    # Column closure requires the XOR over all A-types in each column to be 0.
    first_row = grid[0]
    for j, ch in enumerate(first_row):
        if col_pref[j] ^ (1 if ch == "A" else 0):
            return 0

    dsu = ParityDSU(h + w)
    for x, y, parity in constraints:
        if not dsu.union(x, y, parity):
            return 0

    return pow(2, dsu.components, MOD)


def main():
    input = sys.stdin.buffer.readline
    t = int(input())
    answers = []

    for _ in range(t):
        h, w = map(int, input().split())
        grid = [input().strip().decode() for _ in range(h)]
        answers.append(str(solve_case(h, w, grid)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()