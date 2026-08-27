import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree (1-indexed)
    bit = [0] * (n + 2)

    def add(i, v):
        while i <= n:
            bit[i] += v
            i += i & -i

    def sum_(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    # Inversion parity of P
    inv = 0
    for j, x in enumerate(P):
        # number of previous elements greater than x
        inv += j - sum_(x)
        add(x, 1)
    inv_par = inv & 1

    # Reset BIT
    for i in range(n + 2):
        bit[i] = 0

    pos = [0] * (n + 1)
    for idx, x in enumerate(P, start=1):
        pos[x] = idx

    base = 0
    sumc_par = 0
    min_extra = None
    for v in range(1, n + 1):
        add(pos[v], 1)
        if v < n:  # boundary v (c_N is always 0)
            placed = sum_(v)          # #{u <= v : pos[u] <= v}
            c = v - placed            # crossings needed at boundary v
            if c:
                base += v * c
                sumc_par ^= (c & 1)
                if min_extra is None:
                    min_extra = v

    ans = base
    if sumc_par != inv_par:
        # need one extra swap at the cheapest boundary with c_i >= 1
        ans += min_extra
    print(ans)

main()