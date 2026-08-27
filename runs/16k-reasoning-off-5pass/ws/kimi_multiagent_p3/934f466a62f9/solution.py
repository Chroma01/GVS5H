import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        X = [0] * n
        Y = [0] * n
        Z = [0] * n
        for i in range(n):
            X[i] = int(data[pos])
            Y[i] = int(data[pos + 1])
            Z[i] = int(data[pos + 2])
            pos += 3
        m = 2 * k
        best = 0
        # 8 sign patterns: bit0 -> X sign, bit1 -> Y sign, bit2 -> Z sign
        for mask in range(8):
            sx = 1 if (mask & 1) else -1
            sy = 1 if (mask & 2) else -1
            sz = 1 if (mask & 4) else -1
            w = [0] * n
            for i in range(n):
                w[i] = sx * X[i] + sy * Y[i] + sz * Z[i]
            idx = sorted(range(n), key=lambda i: -w[i])[:m]
            total = 0
            for j in range(0, m, 2):
                a = idx[j]
                b = idx[j + 1]
                p = X[a] + X[b]
                q = Y[a] + Y[b]
                r = Z[a] + Z[b]
                total += p if p >= q and p >= r else (q if q >= r else r)
            if total > best:
                best = total
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")

main()