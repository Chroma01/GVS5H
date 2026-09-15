import sys


def solve():
    buf = sys.stdin.buffer.read()
    if not buf:
        return

    L = len(buf)
    i = 0

    # Parse N.
    while i < L and buf[i] <= 32:
        i += 1
    N = 0
    while i < L and 48 <= buf[i] <= 57:
        N = N * 10 + (buf[i] - 48)
        i += 1

    # Read exactly 3^N bits.  This accepts both contiguous and spaced digits.
    m = 3 ** N
    states = [0] * m
    j = 0
    while i < L and j < m:
        ch = buf[i]
        if ch == 48:          # '0'
            states[j] = 2     # (cost=1) << 1 | value=0
            j += 1
        elif ch == 49:        # '1'
            states[j] = 3     # (cost=1) << 1 | value=1
            j += 1
        i += 1

    # Bottom-up DP.
    # State: (minimum flips to change this node's output) << 1 | original output.
    while len(states) > 1:
        Ls = len(states)
        n = Ls // 3
        nxt = [0] * n
        j = 0

        for k in range(0, Ls, 3):
            a = states[k]
            b = states[k + 1]
            c = states[k + 2]

            va = a & 1
            vb = b & 1
            vc = c & 1

            # Original majority value of this node.
            p = (va & vb) | (va & vc) | (vb & vc)

            ca = a >> 1
            cb = b >> 1
            cc = c >> 1

            # Cost to force each child to output the opposite of p.
            if p:
                # Need children to output 0.
                x = ca if va else 0
                y = cb if vb else 0
                z = cc if vc else 0
            else:
                # Need children to output 1.
                x = 0 if va else ca
                y = 0 if vb else cb
                z = 0 if vc else cc

            # Sum of the two smallest costs.
            mcost = x
            if y > mcost:
                mcost = y
            if z > mcost:
                mcost = z
            cost = x + y + z - mcost

            nxt[j] = (cost << 1) | p
            j += 1

        states = nxt

    sys.stdout.write(str(states[0] >> 1) + "\n")


if __name__ == "__main__":
    solve()