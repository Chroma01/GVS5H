import sys

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(H)]

    Q, sh, sw = map(int, input().split())
    sh -= 1
    sw -= 1

    # Process along the longer direction, so transfer matrices have
    # dimension K = min(H, W).
    transposed = W < H
    K = W if transposed else H
    C = H if transposed else W

    # This matrix-product method is practical for narrow grids.
    # A fallback DP is retained for wider grids.
    if K <= 8:
        size = 1
        while size < C:
            size <<= 1

        kk = K * K
        seg = [[0] * kk for _ in range(size * 2)]

        for p in range(size, size + C):
            mat = seg[p]
            for i in range(K):
                mat[i * K + i] = 1

        def get_values(col):
            if transposed:
                return A[col]
            return [A[r][col] for r in range(K)]

        def make_matrix(col):
            vals = get_values(col)
            mat = [0] * kk
            for j in range(K):
                prod = 1
                for i in range(j, K):
                    prod = prod * vals[i] % MOD
                    mat[i * K + j] = prod
            return mat

        def mul(right, left):
            res = [0] * kk
            for i in range(K):
                ib = i * K
                for m in range(i + 1):
                    rv = right[ib + m]
                    if rv:
                        mb = m * K
                        for j in range(m + 1):
                            res[ib + j] += rv * left[mb + j]
                for j in range(i + 1):
                    res[ib + j] %= MOD
            return res

        for c in range(C):
            seg[size + c] = make_matrix(c)

        for p in range(size - 1, 0, -1):
            seg[p] = mul(seg[p * 2 + 1], seg[p * 2])

        out = []

        for _ in range(Q):
            d, x = input().split()
            x = int(x)

            if d == b"L":
                sw -= 1
            elif d == b"R":
                sw += 1
            elif d == b"U":
                sh -= 1
            else:
                sh += 1

            old = A[sh][sw]
            A[sh][sw] = x

            col = sh if transposed else sw
            row = sw if transposed else sh

            # A change of one entry in a column transfer matrix is rank one:
            # delta * u * v^T, with u_i nonzero only for i >= row and
            # v_j nonzero only for j <= row.
            delta = (x - old) % MOD
            node = size + col
            leaf = seg[node]

            if delta:
                vals = get_values(col)

                u = [0] * K
                prod = 1
                for i in range(row, K):
                    if i > row:
                        prod = prod * vals[i] % MOD
                    u[i] = prod

                v = [0] * K
                prod = 1
                for j in range(row, -1, -1):
                    if j < row:
                        prod = prod * vals[j] % MOD
                    v[j] = prod

                for i in range(row, K):
                    ui = delta * u[i] % MOD
                    base = i * K
                    for j in range(row + 1):
                        leaf[base + j] = (leaf[base + j] + ui * v[j]) % MOD

                child = node
                node >>= 1

                while node:
                    if child == node * 2:
                        # Changed left child:
                        # P = right * left
                        right = seg[node * 2 + 1]
                        left = seg[node * 2]

                        nu = [0] * K
                        for i in range(K):
                            total = 0
                            base = i * K
                            for m in range(i + 1):
                                total += right[base + m] * u[m]
                            nu[i] = total % MOD

                        nv = [0] * K
                        for j in range(K):
                            total = 0
                            for m in range(j, K):
                                total += v[m] * left[m * K + j]
                            nv[j] = total % MOD
                    else:
                        # Changed right child:
                        # P = right * left
                        right = seg[node * 2 + 1]
                        left = seg[node * 2]

                        nu = [0] * K
                        for i in range(K):
                            total = 0
                            base = i * K
                            for m in range(i + 1):
                                total += right[base + m] * u[m]
                            nu[i] = total % MOD

                        nv = [0] * K
                        for j in range(K):
                            total = 0
                            for m in range(j, K):
                                total += v[m] * left[m * K + j]
                            nv[j] = total % MOD

                    cur = seg[node]
                    for i in range(K):
                        ui = nu[i]
                        if ui:
                            base = i * K
                            for j in range(i + 1):
                                cur[base + j] = (cur[base + j] + ui * nv[j]) % MOD

                    u, v = nu, nv
                    child = node
                    node >>= 1

            out.append(str(seg[1][(K - 1) * K]))

        sys.stdout.write("\n".join(out))
        return

    # Exact general fallback.
    out = []
    for _ in range(Q):
        d, x = input().split()
        x = int(x)

        if d == b"L":
            sw -= 1
        elif d == b"R":
            sw += 1
        elif d == b"U":
            sh -= 1
        else:
            sh += 1

        A[sh][sw] = x

        dp = [0] * W
        for r in range(H):
            row = A[r]
            if r == 0:
                cur = row[0]
            else:
                cur = dp[0] * row[0] % MOD
            dp[0] = cur

            for c in range(1, W):
                cur = (cur + dp[c]) * row[c] % MOD
                dp[c] = cur

        out.append(str(dp[-1]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()