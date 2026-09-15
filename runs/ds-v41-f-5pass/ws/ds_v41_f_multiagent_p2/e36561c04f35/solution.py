import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); pos += 1
        A = data[pos:pos + N]; pos += N

        last = [-1] * (N + 2)          # highest level index for each value
        size = N + 2                   # Fenwick upper bound (levels <= #runs <= N)
        bit = [0] * (size + 1)         # bit over levels, stores total length per level
        num_levels = 0
        inversions = 0
        total = 0

        i = 0
        while i < N:
            cur = A[i]
            j = i + 1
            while j < N and A[j] == cur:
                j += 1
            L = j - i                  # run length
            i = j
            v = int(cur)

            lvl = last[v]
            if lvl < 0:
                # brand new value -> create a new top level
                last[v] = num_levels
                p = num_levels + 1
                while p <= size:
                    bit[p] += L
                    p += p & (-p)
                num_levels += 1
                total += L
            else:
                # total length stored at levels strictly greater than lvl
                p = lvl + 1
                s = 0
                while p > 0:
                    s += bit[p]
                    p -= p & (-p)
                w = total - s
                c = w * L
                if c <= 1:
                    # reuse level lvl  (cost c inversions, saves a deletion)
                    inversions += c
                    p = lvl + 1
                    while p <= size:
                        bit[p] += L
                        p += p & (-p)
                    total += L
                else:
                    # create a new top level for v
                    last[v] = num_levels
                    p = num_levels + 1
                    while p <= size:
                        bit[p] += L
                        p += p & (-p)
                    num_levels += 1
                    total += L

        out.append(str(num_levels + inversions))

    sys.stdout.write("\n".join(out))

main()