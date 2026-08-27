import sys

MOD = 998244353


class ParityDSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.xr = [0] * n  # xor from node to its parent
        self.components = n

    def find(self, x):
        nodes = []
        y = x
        dist = 0
        while self.parent[y] != y:
            nodes.append(y)
            dist ^= self.xr[y]
            y = self.parent[y]

        root = y
        acc = 0
        for v in reversed(nodes):
            acc ^= self.xr[v]
            self.parent[v] = root
            self.xr[v] = acc
        return root, dist

    def union(self, a, b, w):
        ra, da = self.find(a)
        rb, db = self.find(b)

        if ra == rb:
            return (da ^ db) == w

        # Required xor between the two roots.
        rel = da ^ db ^ w

        if self.size[ra] < self.size[rb]:
            self.parent[ra] = rb
            self.xr[ra] = rel
            self.size[rb] += self.size[ra]
        else:
            self.parent[rb] = ra
            self.xr[rb] = rel
            self.size[ra] += self.size[rb]

        self.components -= 1
        return True


def solve_case(h, w, grid):
    col_parity = [0] * w

    for row in grid:
        row_parity = 0
        for j, ch in enumerate(row):
            if ch == 65:  # ord('A')
                row_parity ^= 1
                col_parity[j] ^= 1
        if row_parity:
            return 0

    if any(col_parity):
        return 0

    dsu = ParityDSU(h + w)
    col_prefix = [0] * w

    for i, row in enumerate(grid):
        row_prefix = 0

        for j, ch in enumerate(row):
            if ch == 66:  # ord('B')
                # R_i xor C_j = 1 xor (#A before j in row i)
                #                   xor (#A before i in column j)
                relation = 1 ^ row_prefix ^ col_prefix[j]
                if not dsu.union(i, h + j, relation):
                    return 0

            if ch == 65:
                row_prefix ^= 1

        for j, ch in enumerate(row):
            if ch == 65:
                col_prefix[j] ^= 1

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