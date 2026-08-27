import sys

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    NEG = -1 << 60
    for _ in range(t):
        n = int(data[pos]); pos += 1
        arr = data[pos:pos + n]; pos += n

        # ---- run-length compress (tokens compared as raw bytes: canonical decimals) ----
        v = []
        s = []
        va = v.append
        sa = s.append
        prev = None
        for x in arr:
            if x == prev:
                s[-1] += 1
            else:
                va(x); sa(1); prev = x
        R = len(v)

        # ---- 2-state run DP over products of disjoint adjacent run transpositions ----
        # dpA[i] : runs 0..i-1 placed, last placed run is (i-1)   (block ending at i-1 is a singleton)
        # dpB[i] : runs 0..i-1 placed, last placed run is (i-2)   (pair (i-2,i-1) placed swapped)
        dpA = [NEG] * (R + 1)
        dpB = [NEG] * (R + 2)
        dpA[0] = 0
        for i in range(R):
            ai = dpA[i]          # always finite (identity path)
            bi = dpB[i]

            # place single run i  (never merges with run i-1: adjacent runs have different values)
            best = ai
            if bi != NEG:
                c = bi + 1 if (i >= 2 and v[i] == v[i - 2]) else bi
                if c > best:
                    best = c
            if best > dpA[i + 1]:
                dpA[i + 1] = best

            # place pair (i, i+1) swapped as [i+1, i], weighted swap cost s[i]*s[i+1]
            j = i + 1
            if j < R:
                cand = ai + 1 if (i >= 1 and v[j] == v[i - 1]) else ai
                if bi != NEG:
                    c2 = bi + 1 if (i >= 2 and v[j] == v[i - 2]) else bi
                    if c2 > cand:
                        cand = c2
                cand -= s[i] * s[j]
                if cand > dpB[i + 2]:
                    dpB[i + 2] = cand

        g = dpA[R]
        if dpB[R] > g:
            g = dpB[R]
        out.append(R - g)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()