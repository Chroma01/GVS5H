import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append

    A = 65  # ord('A')
    B = 66  # ord('B')

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2

        start = idx
        idx += H

        # First pass: every row and every column must contain an even number of A tiles.
        col_parity = [0] * W
        invalid = False
        has_b = False

        for r in range(start, idx):
            row = data[r]
            row_parity = 0
            for j, ch in enumerate(row):
                if ch == A:
                    row_parity ^= 1
                    col_parity[j] ^= 1
                else:
                    has_b = True
            if row_parity:
                invalid = True
                break

        if not invalid and any(col_parity):
            invalid = True

        if invalid:
            append("0")
            continue

        # If there are no B tiles, row/column flips are all independent.
        if not has_b:
            append(str(pow(2, H + W, MOD)))
            continue

        n = H + W
        parent = list(range(n))
        rank = [0] * n
        parity = [0] * n  # parity[x] = value[x] xor value[parent[x]]
        comps = n

        # col_pref[j] = xor of A tiles in column j above the current row.
        col_pref = [0] * W

        def find(x, parent=parent, parity=parity):
            total = 0
            while parent[x] != x:
                px = parent[x]
                if parent[px] != px:
                    parity[x] ^= parity[px]
                    parent[x] = parent[px]
                total ^= parity[x]
                x = parent[x]
            return x, total

        # Second pass: add parity constraints from B tiles.
        for i in range(H):
            row = data[start + i]
            left_pref = 0  # xor of A tiles in this row before current column

            for j, ch in enumerate(row):
                if ch == B:
                    # For a B tile:
                    # top = column_flip[j] xor col_pref[j]
                    # left = row_flip[i] xor left_pref
                    # top xor left = 1
                    val = 1 ^ col_pref[j] ^ left_pref

                    ra, pa = find(i)
                    rb, pb = find(H + j)

                    if ra == rb:
                        if (pa ^ pb) != val:
                            invalid = True
                            break
                    else:
                        x = pa ^ pb ^ val
                        if rank[ra] < rank[rb]:
                            parent[ra] = rb
                            parity[ra] = x
                        else:
                            parent[rb] = ra
                            parity[rb] = x
                            if rank[ra] == rank[rb]:
                                rank[ra] += 1
                        comps -= 1
                else:
                    left_pref ^= 1
                    col_pref[j] ^= 1

            if invalid:
                break

        if invalid:
            append("0")
        else:
            append(str(pow(2, comps, MOD)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()