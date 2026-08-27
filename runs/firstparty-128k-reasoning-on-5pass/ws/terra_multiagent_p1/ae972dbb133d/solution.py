import sys
from array import array

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    answers = []

    for _ in range(t):
        h = int(next(it))
        w = int(next(it))
        grid = [next(it) for _ in range(h)]

        cells = h * w
        n = 2 * cells

        parent = array('i', range(n))
        parity = bytearray(n)  # value[x] XOR value[parent[x]]
        rank = bytearray(n)
        components = n
        bad = False

        def find(x):
            total = 0
            y = x
            while parent[y] != y:
                total ^= parity[y]
                y = parent[y]
            root = y

            result = total
            y = x
            while parent[y] != y:
                nxt = parent[y]
                edge_parity = parity[y]
                parent[y] = root
                parity[y] = total
                total ^= edge_parity
                y = nxt

            return root, result

        def unite(x, y, val):
            nonlocal components, bad

            rx, px = find(x)
            ry, py = find(y)

            if rx == ry:
                if (px ^ py) != val:
                    bad = True
                return

            root_parity = px ^ py ^ val

            if rank[rx] < rank[ry]:
                parent[rx] = ry
                parity[rx] = root_parity
            else:
                parent[ry] = rx
                parity[ry] = root_parity
                if rank[rx] == rank[ry]:
                    rank[rx] += 1

            components -= 1

        for i in range(h):
            if bad:
                break

            row_base = i * w
            prev_row_base = ((i - 1) % h) * w
            s = grid[i]

            for j in range(w):
                left = row_base + ((j - 1) % w)
                right = row_base + j

                top = cells + prev_row_base + j
                bottom = cells + row_base + j

                if s[j] == 65:  # A
                    unite(left, right, 1)
                    if bad:
                        break
                    unite(top, bottom, 1)
                else:  # B
                    unite(left, right, 0)
                    if bad:
                        break
                    unite(top, bottom, 0)
                    if bad:
                        break
                    unite(right, bottom, 1)

                if bad:
                    break

        if bad:
            answers.append("0")
        else:
            answers.append(str(pow(2, components, MOD)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()