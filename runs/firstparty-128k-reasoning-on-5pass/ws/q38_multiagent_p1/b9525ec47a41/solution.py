import sys

MOD = 998244353


def build_tables():
    """
    Build the determinized transition tables.

    For each s in {0, 1}:
      - sub[S][e] is the next subset of {0, 1} after emitting e
        from subset S, where e is indexed as -1, 0, 1, 2.
      - trans[p] is a tuple with one entry for each feasible e.
        p encodes a DFA state as (A << 2) | B, where A is the set of
        current states reachable from start 0 and B from start 1.
    """
    e_vals = (-1, 0, 1, 2)
    feasible = ((0, 1, 2), (0, 1, 2, 3))  # indices for s=0, s=1
    tables = []

    for s in (0, 1):
        sub = [[0] * 4 for _ in range(4)]
        for S in range(4):
            for ei, e in enumerate(e_vals):
                nxt = 0
                for a in (0, 1):
                    if (S >> a) & 1:
                        for b in (0, 1):
                            if s == 0:
                                if a - b == e:
                                    nxt |= 1 << b
                            else:
                                if a - b == e or a - b + 1 == e:
                                    nxt |= 1 << b
                sub[S][ei] = nxt

        trans = []
        for p in range(16):
            A = p >> 2
            B = p & 3
            lst = []
            for ei in feasible[s]:
                na = sub[A][ei]
                nb = sub[B][ei]
                lst.append((na << 2) | nb)
            trans.append(tuple(lst))
        tables.append(trans)

    return tables[0], tables[1]


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    s = b"".join(data[1:])

    # Build the required NFA/DFA transition tables.
    # The update below is an unrolling of these tables for speed.
    trans0, trans1 = build_tables()

    # Active non-dead DFA states:
    # 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15
    # Initial state is (A={0}, B={1}) = (1 << 2) | 2 = 6.
    d1 = d2 = d3 = d4 = d5 = d6 = d7 = d8 = d10 = d12 = d14 = d15 = 0
    d6 = 1

    mod = MOD
    L = len(s)
    i = 0

    # Process in chunks of 16 and reduce modulo only at chunk boundaries.
    while i < L:
        for b in s[i:i + 16]:
            a = d1 + d2 + d3

            # Common transitions for s_i = 0 and s_i = 1.
            n1 = a + d6 + d7
            n2 = a
            n4 = d4 + d8 + d12
            n8 = n4 + d6 + d14
            c5 = d5 + d10 + d15
            n5 = c5 + d14
            n10 = c5 + d7

            if b == 48:  # '0'
                n3 = d3
                n6 = d6
                n7 = d7
                n12 = d12
                n14 = d14
                n15 = d15
            else:        # '1'
                n3 = a + d3
                n6 = 0
                n7 = d6 + d7
                n12 = n4 + d12
                n14 = d6 + d14
                n15 = c5 + d7 + d14 + d15

            d1, d2, d3, d4, d5, d6, d7, d8, d10, d12, d14, d15 = (
                n1, n2, n3, n4, n5, n6, n7, n8, n10, n12, n14, n15
            )

        i += 16

        d1 %= mod
        d2 %= mod
        d3 %= mod
        d4 %= mod
        d5 %= mod
        d6 %= mod
        d7 %= mod
        d8 %= mod
        d10 %= mod
        d12 %= mod
        d14 %= mod
        d15 %= mod

    # Accepting states are those where start 0 can end at 0, or start 1 can end at 1.
    ans = (d2 + d3 + d4 + d5 + d6 + d7 + d10 + d12 + d14 + d15) % mod
    print(ans)


if __name__ == "__main__":
    solve()