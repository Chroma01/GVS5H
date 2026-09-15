import sys


def solve() -> None:
    buf = sys.stdin.buffer.read()
    if not buf:
        return

    m = len(buf)
    i = 0

    # Parse N.
    while i < m and buf[i] <= 32:
        i += 1

    N = 0
    while i < m and 48 <= buf[i] <= 57:
        N = N * 10 + (buf[i] - 48)
        i += 1

    L = 3 ** N

    # Remove common whitespace from the rest of the input.
    # If unusual characters are present, fall back to keeping only '0' and '1'.
    table = bytes(range(256))
    s = buf[i:].translate(table, b" \n\r\t\v\f")
    if len(s) != L:
        s = bytes(c for c in buf[i:] if c == 48 or c == 49)

    if len(s) > L:
        s = s[:L]

    # Pack each node as (flip_cost << 1) | actual_value.
    # Leaf: actual_value is the bit, flip_cost is 1.
    #   bit 0 -> (1 << 1) | 0 = 2
    #   bit 1 -> (1 << 1) | 1 = 3
    arr = [2 if c == 48 else 3 for c in s]

    # Bottom-up ternary-tree DP.
    while len(arr) > 1:
        new_len = len(arr) // 3
        new = [0] * new_len
        a = arr

        for idx in range(new_len):
            j = idx * 3

            x0 = a[j]
            x1 = a[j + 1]
            x2 = a[j + 2]

            v0 = x0 & 1
            v1 = x1 & 1
            v2 = x2 & 1

            # Parent actual value is the majority of child actual values.
            v = (v0 + v1 + v2) >> 1

            f0 = x0 >> 1
            f1 = x1 >> 1
            f2 = x2 >> 1

            # To flip the parent, target is 1 - v.
            # A child already equal to target costs 0.
            # A child equal to v costs its flip cost.
            c0 = f0 if v0 == v else 0
            c1 = f1 if v1 == v else 0
            c2 = f2 if v2 == v else 0

            # Need at least two children to output the target.
            # Sum of the two smallest costs = total - maximum.
            mx = c0
            if c1 > mx:
                mx = c1
            if c2 > mx:
                mx = c2

            flip = c0 + c1 + c2 - mx
            new[idx] = (flip << 1) | v

        arr = new

    ans = arr[0] >> 1 if arr else 0
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()