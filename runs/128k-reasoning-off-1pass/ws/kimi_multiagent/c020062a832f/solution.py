import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = list(map(int, data[2:2 + n]))

    # base inversion count of A via Fenwick tree over values 0..m-1
    size = m + 2
    bit = [0] * size

    def bit_add(i, v):
        i += 1
        while i < size:
            bit[i] += v
            i += i & -i

    def bit_sum(i):  # sum over values [0, i]
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    base = 0
    for v in A:
        seen = bit_sum(m - 1)   # number of earlier elements
        le = bit_sum(v)         # earlier elements with value <= v
        base += seen - le       # earlier elements with value > v
        bit_add(v, 1)

    # For a pair (i<j) with unequal values u = min, v = max:
    #   order flips at k = M - v (larger wraps) and flips back at k = M - u (smaller wraps).
    # Inversion pair (A_i > A_j):     -1 at k = M - max, +1 at k = M - min.
    # Non-inversion pair (A_i < A_j): +1 at k = M - max, -1 at k = M - min.
    # Net effect per element with value v at position i:
    #   plus[M - v]  += (# earlier elements with value != v)
    #   minus[M - v] += (# later   elements with value != v)
    plus = [0] * (m + 1)
    minus = [0] * (m + 1)

    freq = [0] * m
    seen = 0
    for v in A:
        plus[m - v] += seen - freq[v]   # earlier values != v
        freq[v] += 1
        seen += 1

    freq = [0] * m
    later = 0
    for v in reversed(A):
        minus[m - v] += later - freq[v]  # later values != v
        freq[v] += 1
        later += 1

    out = []
    cur = base
    out.append(str(cur))
    for k in range(1, m):
        cur += plus[k] - minus[k]
        out.append(str(cur))
    sys.stdout.write("\n".join(out) + "\n")

main()