import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1
    Ls = [0] * N
    Rs = [0] * N
    for i in range(N):
        Ls[i] = int(data[ptr]); Rs[i] = int(data[ptr + 1]); ptr += 2
    Q = int(data[ptr]); ptr += 1
    qnums = [int(x) for x in data[ptr:ptr + Q]]

    M = max(qnums)          # valid domain restriction: F(x) evolves independently
    n = M - 1               # number of D entries: D[i] = F[i+1]-F[i], i=1..n
    tr = [0] * (n + 1)      # Fenwick over D; all-ones array -> tree[i]=lowbit(i)
    for i in range(1, n + 1):
        tr[i] = i & (-i)

    total = n               # prefixD(n) = F(M)-F(1)
    base = 1                # F(1)

    bm0 = 0                 # highest power of two <= n (for lower_bound lifting)
    if n:
        bm0 = 1
        while (bm0 << 1) <= n:
            bm0 <<= 1

    for i in range(N):
        L = Ls[i]; R = Rs[i]

        # a = smallest x with F(x) >= L
        T = L - base
        if T <= 0:
            a = 1
        elif T > total:
            a = M + 1
        else:
            pos = 0
            t = T
            bm = bm0
            while bm:
                nx = pos + bm
                if nx <= n and tr[nx] < t:
                    pos = nx
                    t -= tr[nx]
                bm >>= 1
            a = pos + 2

        # b = largest x with F(x) <= R
        U = R - base
        if U < 0:
            b = 0
        elif U >= total:
            b = M
        else:
            pos = 0
            t = U + 1
            bm = bm0
            while bm:
                nx = pos + bm
                if nx <= n and tr[nx] < t:
                    pos = nx
                    t -= tr[nx]
                bm >>= 1
            b = pos + 1

        if a <= b:
            if a == 1:
                base += 1
            else:
                j = a - 1
                while j <= n:
                    tr[j] += 1
                    j += j & (-j)
                total += 1
            if b <= n:
                j = b
                while j <= n:
                    tr[j] -= 1
                    j += j & (-j)
                total -= 1

    out = []
    ap = out.append
    for x in qnums:
        s = 0
        j = x - 1
        while j > 0:
            s += tr[j]
            j -= j & (-j)
        ap(base + s)

    sys.stdout.write('\n'.join(map(str, out)))
    sys.stdout.write('\n')

main()