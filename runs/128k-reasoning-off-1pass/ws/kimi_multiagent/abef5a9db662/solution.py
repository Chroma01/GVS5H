import sys

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    V = 500000
    Ls = [0] * N
    Rs = [0] * N
    for i in range(N):
        Ls[i] = int(data[p]); Rs[i] = int(data[p + 1]); p += 2
    Q = int(data[p]); p += 1
    queries = data[p:p + Q]

    # BIT over difference array d[1..V], initially d[i] = 1 (cur[x] = x).
    # For the all-ones array, BIT[i] = i & -i.
    bit = [0] * (V + 1)
    for i in range(1, V + 1):
        bit[i] = i & -i

    hb = 1 << (V.bit_length() - 1)  # highest power of two <= V

    for i in range(N):
        Li = Ls[i]
        Ri1 = Rs[i] + 1
        # a = first index with prefix-sum >= Li  (lower_bound(Li) + 1)
        pos = 0
        acc = 0
        k = hb
        while k:
            nxt = pos + k
            if nxt <= V and acc + bit[nxt] < Li:
                acc += bit[nxt]
                pos = nxt
            k >>= 1
        a = pos + 1
        # b = last index with prefix-sum <= Ri  (lower_bound(Ri+1))
        pos = 0
        acc = 0
        k = hb
        while k:
            nxt = pos + k
            if nxt <= V and acc + bit[nxt] < Ri1:
                acc += bit[nxt]
                pos = nxt
            k >>= 1
        b = pos
        if a <= b:
            # range add +1 on cur[a..b]  <=>  d[a] += 1, d[b+1] -= 1
            j = a
            while j <= V:
                bit[j] += 1
                j += j & -j
            if b < V:
                j = b + 1
                while j <= V:
                    bit[j] -= 1
                    j += j & -j

    # Recover d from BIT in O(V): process indices in decreasing order.
    for i in range(V, 0, -1):
        j = i + (i & -i)
        if j <= V:
            bit[j] -= bit[i]
    # Prefix-sum in place: bit[x] becomes cur[x] = final rating for initial x.
    for i in range(2, V + 1):
        bit[i] += bit[i - 1]

    out = [str(bit[int(q)]) for q in queries]
    sys.stdout.write("\n".join(out) + "\n")

main()