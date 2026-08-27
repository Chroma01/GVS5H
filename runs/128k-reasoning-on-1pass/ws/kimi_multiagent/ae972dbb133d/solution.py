import sys
from array import array

MOD = 998244353
A_BYTE = 65


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos])
    pos += 1
    answers = []

    for _ in range(T):
        H = int(data[pos])
        W = int(data[pos + 1])
        pos += 2
        rows = data[pos:pos + H]
        pos += H

        n = H + W
        parent = array("i", range(n))
        size = array("i", [1]) * n

        # xor_to_parent[x] = value[x] XOR value[parent[x]]
        xor_to_parent = bytearray(n)

        components = n
        ok = True

        def find(x):
            root = x
            parity = 0
            while parent[root] != root:
                parity ^= xor_to_parent[root]
                root = parent[root]

            # Compress the path while preserving parities to the root.
            node = x
            prefix = 0  # value[x] XOR value[node]
            while parent[node] != node:
                nxt = parent[node]
                old = xor_to_parent[node]
                xor_to_parent[node] = parity ^ prefix
                parent[node] = root
                prefix ^= old
                node = nxt

            return root, parity

        def union(a, b, want):
            nonlocal components, ok

            ra, pa = find(a)
            rb, pb = find(b)

            if ra == rb:
                if (pa ^ pb) != want:
                    ok = False
                return

            # value[ra] XOR value[rb] needed for value[a] XOR value[b] = want
            x = pa ^ pb ^ want

            if size[ra] < size[rb]:
                parent[ra] = rb
                xor_to_parent[ra] = x
                size[rb] += size[ra]
            else:
                parent[rb] = ra
                xor_to_parent[rb] = x
                size[ra] += size[rb]

            components -= 1

        # col_a_prefix[j] = parity of A cells in column j in rows before i.
        col_a_prefix = bytearray(W)

        for i, row in enumerate(rows):
            row_a_parity = 0  # parity of A cells in this row before column j

            for j, ch in enumerate(row):
                if ch == A_BYTE:
                    row_a_parity ^= 1
                    col_a_prefix[j] ^= 1
                else:
                    # For a B cell:
                    # row_variable[i] XOR col_variable[j]
                    # = 1 XOR horizontal_A_prefix XOR vertical_A_prefix.
                    union(
                        i,
                        H + j,
                        1 ^ row_a_parity ^ col_a_prefix[j],
                    )
                    if not ok:
                        break

            # A cells flip the horizontal edge state; an odd number makes
            # the toroidal wraparound inconsistent.
            if row_a_parity:
                ok = False
            if not ok:
                break

        # Likewise, every column must contain an even number of A cells.
        if ok and any(col_a_prefix):
            ok = False

        if not ok:
            answers.append("0")
        else:
            answers.append(str(pow(2, components, MOD)))

    sys.stdout.write("\n".join(answers) + "\n")


if __name__ == "__main__":
    solve()