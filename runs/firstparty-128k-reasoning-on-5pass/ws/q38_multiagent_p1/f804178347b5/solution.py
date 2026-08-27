import sys
from array import array


def main():
    data = sys.stdin.buffer.read()
    parts = data.split(maxsplit=1)
    if not parts:
        return

    N = int(parts[0])
    rest = parts[1] if len(parts) > 1 else b""
    expected = 3 ** N

    # Convert ASCII '0'/'1' to byte values 0/1, removing whitespace.
    to_bit = bytes.maketrans(b"01", b"\x00\x01")
    delete = b" \n\r\t\v\f"
    values = bytearray(rest.translate(to_bit, delete))
    del data, parts, rest

    # Safety for valid input; normally len(values) == expected.
    if len(values) > expected:
        del values[expected:]
    elif len(values) < expected:
        values.extend(b"\x00" * (expected - len(values)))

    # cost[i] = minimum flips in subtree i to change node i's current value.
    cost = array("H", [1]) * expected
    zero = array("H", [0])

    # For pattern (v0, v1, v2) encoded as 4*v0 + 2*v1 + v2:
    # p_tab[pat] is the majority value.
    # If not all three are equal, idx1/idx2 are the two children matching p.
    p_tab = bytes((0, 0, 0, 1, 0, 1, 1, 1))
    idx1 = bytes((0, 0, 0, 1, 1, 0, 0, 0))
    idx2 = bytes((0, 1, 2, 2, 2, 2, 1, 0))

    while len(values) > 1:
        n = len(values)
        m = n // 3
        new_values = bytearray(m)
        new_cost = zero * m

        vals = values
        costs = cost
        nvals = new_values
        ncosts = new_cost
        pt = p_tab
        i1 = idx1
        i2 = idx2

        i = 0
        for j in range(0, n, 3):
            v0 = vals[j]
            v1 = vals[j + 1]
            v2 = vals[j + 2]
            pat = (v0 << 2) | (v1 << 1) | v2
            p = pt[pat]

            if pat == 0 or pat == 7:
                # All three children already have value p.
                # Need to flip two of them: sum of two smallest costs.
                a = costs[j]
                b = costs[j + 1]
                c = costs[j + 2]
                mx = a
                if b > mx:
                    mx = b
                if c > mx:
                    mx = c
                ncosts[i] = a + b + c - mx
            else:
                # Exactly two children have value p, one is already opposite.
                # Need to flip one of the two matching children.
                a = costs[j + i1[pat]]
                b = costs[j + i2[pat]]
                ncosts[i] = a if a < b else b

            nvals[i] = p
            i += 1

        values = new_values
        cost = new_cost

    print(cost[0])


if __name__ == "__main__":
    main()