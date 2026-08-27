import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    answers = []

    for _ in range(t):
        H = int(next(it))
        W = int(next(it))

        n = H + W
        parent = list(range(n))
        rank = [0] * n
        xor_to_parent = [0] * n

        def find(x):
            if parent[x] != x:
                p = parent[x]
                root, px = find(p)
                xor_to_parent[x] ^= px
                parent[x] = root
            return parent[x], xor_to_parent[x]

        components = n
        possible = True
        column_prefix = [0] * W

        for i in range(H):
            row = next(it)
            row_prefix = 0

            for j, c in enumerate(row):
                if c == 66:  # 'B'
                    if possible:
                        u = i
                        v = H + j
                        required = 1 ^ row_prefix ^ column_prefix[j]

                        ru, xu = find(u)
                        rv, xv = find(v)

                        if ru == rv:
                            if (xu ^ xv) != required:
                                possible = False
                        else:
                            relation = xu ^ xv ^ required
                            if rank[ru] < rank[rv]:
                                parent[ru] = rv
                                xor_to_parent[ru] = relation
                            else:
                                parent[rv] = ru
                                xor_to_parent[rv] = relation
                                if rank[ru] == rank[rv]:
                                    rank[ru] += 1
                            components -= 1

                else:  # 'A'
                    row_prefix ^= 1
                    column_prefix[j] ^= 1

            if row_prefix:
                possible = False

        if any(column_prefix):
            possible = False

        if possible:
            answers.append(str(pow(2, components, MOD)))
        else:
            answers.append("0")

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()