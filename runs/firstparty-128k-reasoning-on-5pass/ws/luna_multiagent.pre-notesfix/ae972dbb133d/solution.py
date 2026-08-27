import sys

MOD = 998244353


class ParityDSU:
    __slots__ = ("parent", "size", "xor_to_parent", "components")

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.xor_to_parent = [0] * n
        self.components = n

    def find(self, x):
        parent = self.parent
        xor_to_parent = self.xor_to_parent

        root = x
        acc = 0
        while parent[root] != root:
            acc ^= xor_to_parent[root]
            root = parent[root]

        total = acc
        y = x
        while parent[y] != y:
            p = parent[y]
            w = xor_to_parent[y]
            parent[y] = root
            xor_to_parent[y] = total
            total ^= w
            y = p

        return root, acc

    def union(self, a, b, w):
        ra, xa = self.find(a)
        rb, xb = self.find(b)

        if ra == rb:
            return (xa ^ xb) == w

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
            xa, xb = xb, xa

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.xor_to_parent[rb] = xa ^ xb ^ w
        self.components -= 1
        return True


def solve_case(h, w, grid):
    # Variables 0..h-1 are row bits x_i.
    # Variables h..h+w-1 are column bits y_j.
    dsu = ParityDSU(h + w)
    column_prefix = [0] * w
    possible = True

    for i in range(h):
        row_prefix = 0
        row = grid[i]

        for j, ch in enumerate(row):
            if ch == 'A':
                row_prefix ^= 1
                column_prefix[j] ^= 1
            else:
                # For a B tile, its horizontal and vertical pair values
                # must be opposite:
                # x_i xor y_j = 1 xor row_prefix xor column_prefix[j].
                rhs = 1 ^ row_prefix ^ column_prefix[j]
                if not dsu.union(i, h + j, rhs):
                    possible = False

        # Horizontal edge recurrence must close around the torus.
        if row_prefix:
            possible = False

    # Vertical edge recurrence must also close around the torus.
    if any(column_prefix):
        possible = False

    if not possible:
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