import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = [0] * M
    Y = [0] * M
    Z = [0] * M
    for i in range(M):
        X[i] = int(next(it))
        Y[i] = int(next(it))
        Z[i] = int(next(it))
    result = [0] * (N + 1)
    MAX_BIT = 30  # because Z_i <= 1e9 < 2^30
    for b in range(MAX_BIT + 1):
        parent = list(range(N + 1))
        xor_par = [0] * (N + 1)
        size = [1] * (N + 1)

        def find(x):
            if parent[x] != x:
                r, px = find(parent[x])
                parent[x] = r
                xor_par[x] ^= px
            return parent[x], xor_par[x]

        def union(x, y, w):
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                return (px ^ py) == w
            if size[rx] < size[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            xor_par[ry] = w ^ px ^ py
            size[rx] += size[ry]
            return True

        consistent = True
        for i in range(M):
            zb = (Z[i] >> b) & 1
            x = X[i]
            y = Y[i]
            if x == y:
                if zb != 0:
                    consistent = False
                    break
                continue
            if not union(x, y, zb):
                consistent = False
                break
        if not consistent:
            print(-1)
            return

        # Determine bits for this position
        cnt1 = [0] * (N + 1)
        parity = [0] * (N + 1)
        root_of = [0] * (N + 1)
        for i in range(1, N + 1):
            r, p = find(i)
            root_of[i] = r
            parity[i] = p
            cnt1[r] += p

        root_bit = [0] * (N + 1)
        for i in range(1, N + 1):
            if root_of[i] == i:
                c = cnt1[i]
                s = size[i]
                root_bit[i] = 0 if (2 * c <= s) else 1

        for i in range(1, N + 1):
            r = root_of[i]
            bit_val = root_bit[r] ^ parity[i]
            result[i] |= (bit_val << b)

    sys.stdout.write(' '.join(str(result[i]) for i in range(1, N + 1)))

if __name__ == "__main__":
    solve()