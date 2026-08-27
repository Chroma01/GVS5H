import sys

MOD = 998244353
A_INT = 65
A_BYTES = b"A"


class ParityDSU:
    __slots__ = ("parent", "rank", "parity", "comp")

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.parity = [0] * n
        self.comp = n

    def union(self, a, b, w):
        parent = self.parent
        parity = self.parity
        rank = self.rank

        # find a, with path compression
        ra = a
        pa = 0
        while parent[ra] != ra:
            pa ^= parity[ra]
            ra = parent[ra]
        oa = pa
        while parent[a] != a:
            p = parent[a]
            px = parity[a]
            parent[a] = ra
            parity[a] = pa
            pa ^= px
            a = p

        # find b, with path compression
        rb = b
        pb = 0
        while parent[rb] != rb:
            pb ^= parity[rb]
            rb = parent[rb]
        ob = pb
        while parent[b] != b:
            p = parent[b]
            px = parity[b]
            parent[b] = rb
            parity[b] = pb
            pb ^= px
            b = p

        if ra == rb:
            return (oa ^ ob) == w

        val = oa ^ ob ^ w
        if rank[ra] < rank[rb]:
            parent[ra] = rb
            parity[ra] = val
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
            parity[rb] = val
        else:
            parent[rb] = ra
            parity[rb] = val
            rank[ra] += 1

        self.comp -= 1
        return True


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append

    mod = MOD
    a_int = A_INT
    a_bytes = A_BYTES
    dsu_class = ParityDSU

    for _ in range(t):
        H = int(data[idx])
        W = int(data[idx + 1])
        idx += 2

        start = idx
        idx += H
        nvars = H + W

        col = [0] * W
        ok = True
        has_A = False
        has_B = False
        dsu = None
        union = None

        # First pass: row parity, column parity, and special-case detection.
        for k in range(H):
            s = data[start + k]
            cntA = s.count(a_bytes)

            if cntA:
                has_A = True

            if cntA & 1:
                ok = False
                break

            if cntA < W:
                has_B = True

            if cntA == W:
                for j in range(W):
                    col[j] ^= 1
            elif cntA:
                for j, ch in enumerate(s):
                    if ch == a_int:
                        col[j] ^= 1

        if ok:
            if 1 in col:
                ok = False

        if not ok:
            append("0")
            continue

        # All B: complete bipartite B-graph, one component.
        if not has_A:
            append("2")
            continue

        # All A: no row-column constraints.
        if not has_B:
            append(str(pow(2, nvars, mod)))
            continue

        # Second pass: add B-cell XOR constraints.
        dsu = dsu_class(nvars)
        union = dsu.union
        col_pref = col  # all zeros here

        for i in range(H):
            s = data[start + i]
            row_pref = 0
            base = i

            for j, ch in enumerate(s):
                if ch == a_int:
                    row_pref ^= 1
                    col_pref[j] ^= 1
                else:
                    c = 1 ^ row_pref ^ col_pref[j]
                    if not union(base, H + j, c):
                        ok = False
                        break

            if not ok:
                break

        if ok:
            append(str(pow(2, dsu.comp, mod)))
        else:
            append("0")

        dsu = None
        union = None

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()