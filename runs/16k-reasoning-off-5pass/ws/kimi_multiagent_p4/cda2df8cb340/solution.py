import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    total_sum = sum(A)
    answer = (n + 1) * total_sum  # sum over i<=j of (A_i + A_j)

    max_s = 2 * max(A)  # maximum possible A_i + A_j
    t = 1
    while (1 << t) <= max_s:
        M = 1 << t
        mask = M - 1
        groups = {}  # residue -> [count, sum of values]
        for a in A:
            r = a & mask
            g = groups.get(r)
            if g is None:
                groups[r] = [1, a]
            else:
                g[0] += 1
                g[1] += a
        S_t = 0
        for r, (cr, wr) in groups.items():
            r2 = (-r) & mask
            if r2 < r:
                continue
            if r2 == r:
                # pairs i<=j both with residue r: sum of (A_i+A_j) = (cr+1)*wr
                S_t += (cr + 1) * wr
            else:
                g2 = groups.get(r2)
                if g2 is not None:
                    cr2, wr2 = g2
                    S_t += cr * wr2 + cr2 * wr
        # Every summand of S_t is a sum A_i+A_j divisible by 2^t, so S_t is divisible by 2^t.
        answer -= S_t >> t
        t += 1

    print(answer)

main()