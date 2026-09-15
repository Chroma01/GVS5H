import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    Ls = [0] * n
    Rs = [0] * n
    for i in range(n):
        Ls[i] = int(data[pos]); pos += 1
        Rs[i] = int(data[pos]); pos += 1
    q = int(data[pos]); pos += 1
    xs = list(map(int, data[pos:pos + q]))

    # Only distinct query values matter; sorted order keeps ratings non-decreasing.
    sorted_xs = sorted(set(xs))
    m = len(sorted_xs)

    size = 1
    log = 0
    while size < m:
        size <<= 1
        log += 1
    NEG = -(1 << 60)
    # mx[k] = max over subtree k, INCLUDING lz[k], EXCLUDING ancestors' lazies.
    mx = [NEG] * (2 * size)
    lz = [0] * size
    for i in range(m):
        mx[size + i] = sorted_xs[i]
    for i in range(size - 1, 0, -1):
        a = mx[2 * i]; b = mx[2 * i + 1]
        mx[i] = a if a > b else b

    for idx in range(n):
        L = Ls[idx]; R = Rs[idx]

        # first position with value >= L  (pure reads, no modification)
        if mx[1] < L:
            continue
        k = 1; acc = 0
        while k < size:
            acc += lz[k]
            c = k << 1
            if mx[c] + acc >= L:
                k = c
            else:
                k = c | 1
        p = k - size

        # first position with value >= R+1
        target = R + 1
        if mx[1] < target:
            qq = m
        else:
            k = 1; acc = 0
            while k < size:
                acc += lz[k]
                c = k << 1
                if mx[c] + acc >= target:
                    k = c
                else:
                    k = c | 1
            qq = k - size

        # add 1 to [p, qq-1]
        if p <= qq - 1:
            l = p + size
            r = qq + size          # exclusive
            l0 = l; r0 = r
            while l < r:
                if l & 1:
                    mx[l] += 1
                    if l < size:
                        lz[l] += 1
                    l += 1
                if r & 1:
                    r -= 1
                    mx[r] += 1
                    if r < size:
                        lz[r] += 1
                l >>= 1
                r >>= 1
            for i in range(1, log + 1):
                kk = l0 >> i
                a = mx[2 * kk]; b = mx[2 * kk + 1]
                mx[kk] = (a if a > b else b) + lz[kk]
                kk = (r0 - 1) >> i
                a = mx[2 * kk]; b = mx[2 * kk + 1]
                mx[kk] = (a if a > b else b) + lz[kk]

    # Push all lazies so leaves hold final ratings.
    for k in range(1, size):
        z = lz[k]
        if z:
            c = k << 1
            mx[c] += z
            if c < size:
                lz[c] += z
            c += 1
            mx[c] += z
            if c < size:
                lz[c] += z
            lz[k] = 0

    ansmap = {}
    base = size
    for i in range(m):
        ansmap[sorted_xs[i]] = mx[base + i]

    out = []
    for x in xs:
        out.append(str(ansmap[x]))
    sys.stdout.write("\n".join(out) + "\n")

main()