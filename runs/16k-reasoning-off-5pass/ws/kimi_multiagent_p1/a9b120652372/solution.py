import sys

def solve_one(n, A, B):
    p = [i for i in range(n) if A[i] == '1']
    q = [i for i in range(n) if B[i] == '1']
    m, r = len(p), len(q)
    if m < r:
        return -1
    if r == 1:
        return max(abs(p[0] - q[0]), abs(p[-1] - q[0]))

    # Greedy min-max monotone surjection f: group i -> target f[i]
    f = [0] * m
    j = 0
    for i in range(1, m):
        if j + 1 < r and (m - 1 - i) >= (r - 1 - (j + 1)):
            if abs(p[i] - q[j + 1]) <= abs(p[i] - q[j]):
                j += 1
        f[i] = j
    if f[m - 1] != r - 1:
        return -1

    delta = [q[f[i]] - p[i] for i in range(m)]
    for i in range(m - 1):
        if delta[i] < delta[i + 1]:
            return -1

    def plateau_mask(dl):
        mask = 0
        i = 0
        L = len(dl)
        while i < L - 1:
            if dl[i] == dl[i + 1]:
                mask |= 1 << (dl[i] & 1)
                while i < L - 1 and dl[i] == dl[i + 1]:
                    i += 1
            else:
                i += 1
        return mask

    def min_D(dl, mask):
        mx = max(abs(x) for x in dl)
        if mask == 3:
            return None
        if mask == 0:
            return mx
        need = 0 if mask == 1 else 1
        return mx if (mx & 1) == need else mx + 1

    mask = plateau_mask(delta)
    D = min_D(delta, mask)
    if D is not None:
        return D

    best = [None]

    def consider(nf):
        nd = [q[nf[i]] - p[i] for i in range(m)]
        for i in range(m - 1):
            if nd[i] < nd[i + 1]:
                return
        nmask = plateau_mask(nd)
        d = min_D(nd, nmask)
        if d is not None and (best[0] is None or d < best[0]):
            best[0] = d

    def assign_with_forced(a, t):
        # greedy assignment but with f[a] forced to t (a >= 1)
        nf = [0] * m
        jj = 0
        for i in range(1, m):
            if i == a:
                if t < jj or (m - 1 - i) < (r - 1 - t):
                    return None
                jj = t
            else:
                if jj + 1 < r and (m - 1 - i) >= (r - 1 - (jj + 1)):
                    if abs(p[i] - q[jj + 1]) <= abs(p[i] - q[jj]):
                        jj += 1
            nf[i] = jj
        if nf[m - 1] != r - 1:
            return None
        return nf

    # Mixed plateau parities: try local repairs per plateau run.
    i = 0
    while i < m - 1:
        if delta[i] == delta[i + 1]:
            s = i
            v = delta[i]
            while i < m - 1 and delta[i] == delta[i + 1]:
                i += 1
            e = i  # run is [s, e], value v
            # Option A (v < 0): bump f[e] up by one, re-greedy the suffix.
            if v < 0 and f[e] + 1 < r and (m - 1 - e) >= (r - 1 - (f[e] + 1)):
                nf = assign_with_forced(e, f[e] + 1)
                if nf is not None:
                    consider(nf)
            # Option B (v > 0): force f[s] down by one, re-greedy the rest.
            if v > 0 and s > 0 and f[s] - 1 >= 0:
                nf = assign_with_forced(s, f[s] - 1)
                if nf is not None:
                    consider(nf)
            # Option C (v >= 0): alternative tie-break, advance earlier.
            if v >= 0 and f[s] + 1 < r and (m - 1 - s) >= (r - 1 - (f[s] + 1)):
                nf = assign_with_forced(s, f[s] + 1) if s > 0 else None
                if nf is not None:
                    consider(nf)
        else:
            i += 1

    return best[0] if best[0] is not None else -1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx]); idx += 1
        A = data[idx].decode(); idx += 1
        B = data[idx].decode(); idx += 1
        out.append(str(solve_one(n, A, B)))
    sys.stdout.write('\n'.join(out) + '\n')

main()