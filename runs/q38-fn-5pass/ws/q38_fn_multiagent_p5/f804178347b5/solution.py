import sys


def solve():
    parts = sys.stdin.buffer.read().split(maxsplit=1)
    if not parts:
        return

    N = int(parts[0])
    rest = parts[1] if len(parts) > 1 else b""

    # Map ASCII '0'/'1' to byte values 0/1, and delete every other byte.
    # This robustly handles both contiguous strings and whitespace-separated bits.
    table = bytes.maketrans(b"01", b"\x00\x01")
    delete = bytes(i for i in range(256) if i not in (48, 49))
    vals = bytearray(rest.translate(table, delete))

    expected = 3 ** N
    if len(vals) > expected:
        vals = vals[:expected]

    del parts, rest

    m = len(vals)
    if m == 0:
        return

    # For each node:
    #   vals[i]  = current value of the node
    #   costs[i] = minimum changes in its subtree to flip it to the opposite value
    costs = [1] * m

    while m > 1:
        nm = m // 3
        nvals = bytearray(nm)
        ncosts = [0] * nm

        v = vals
        c = costs
        nv = nvals
        nc = ncosts

        j = 0
        k = 0
        while j < nm:
            v0 = v[k]
            v1 = v[k + 1]
            v2 = v[k + 2]

            s = v0 + v1 + v2
            pv = s >> 1          # majority: 1 if sum >= 2, else 0
            nv[j] = pv
            target = pv ^ 1      # value needed to flip this parent

            # Cost to make each child equal to target.
            if v0 == target:
                c0 = 0
            else:
                c0 = c[k]

            if v1 == target:
                c1 = 0
            else:
                c1 = c[k + 1]

            if v2 == target:
                c2 = 0
            else:
                c2 = c[k + 2]

            # Sum of the two smallest among c0, c1, c2.
            if c0 <= c1:
                if c1 <= c2:
                    nc[j] = c0 + c1
                else:
                    nc[j] = c0 + c2
            else:
                if c0 <= c2:
                    nc[j] = c0 + c1
                else:
                    nc[j] = c1 + c2

            j += 1
            k += 3

        vals = nvals
        costs = ncosts
        m = nm

    sys.stdout.write(str(costs[0]) + "\n")


if __name__ == "__main__":
    solve()