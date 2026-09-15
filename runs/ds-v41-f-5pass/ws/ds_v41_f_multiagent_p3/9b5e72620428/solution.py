import sys
from bisect import bisect_left
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])

    fa = []
    fb = []
    for i in range(1, 1 + n):
        v = int(data[i])
        if v != -1:
            fa.append(v)
    for i in range(1 + n, 1 + 2 * n):
        v = int(data[i])
        if v != -1:
            fb.append(v)

    pA = len(fa)
    pB = len(fb)
    T = pA + pB - n
    if T <= 0:
        # Enough free slots: pick S = L (or 0 if no fixed values at all).
        sys.stdout.write("Yes\n")
        return

    # Every fixed value needs a non-negative partner, so S >= max fixed value.
    L = max(max(fa), max(fb))
    cA = Counter(fa)
    cB = Counter(fb)

    prod = len(cA) * len(cB)

    # Fast path with numpy for the heavy O(|dA|*|dB|) aggregation.
    if prod > 600000:
        try:
            import numpy as np
            uA = np.fromiter(cA.keys(), dtype=np.int32)
            cAv = np.fromiter(cA.values(), dtype=np.int32)
            uB = np.fromiter(cB.keys(), dtype=np.int32)
            cBv = np.fromiter(cB.values(), dtype=np.int32)

            # values up to 1e9 so sums <= 2e9 fit in int32
            sums = uA[:, None] + uB[None, :]
            mask = sums >= L
            Sf = sums[mask]
            if Sf.size == 0:
                sys.stdout.write("No\n")
                return
            del sums
            addfull = np.minimum(cAv[:, None], cBv[None, :])
            addf = addfull[mask]
            del addfull, mask

            uniq, inv = np.unique(Sf, return_inverse=True)
            tot = np.bincount(inv, weights=addf)
            if tot.max() >= T:
                sys.stdout.write("Yes\n")
            else:
                sys.stdout.write("No\n")
            return
        except Exception:
            pass  # fall back to pure Python

    # Pure Python: accumulate M(S) = sum_a min(cntA[a], cntB[S-a]) per sum.
    dB = sorted(cB.items())
    valsB = [b for b, _ in dB]
    cntsB = [c for _, c in dB]
    m = len(valsB)

    accum = {}
    get = accum.get
    for a, ca in cA.items():
        base = L - a
        i0 = bisect_left(valsB, base)
        if i0 >= m:
            continue
        for b, cb in zip(valsB[i0:], cntsB[i0:]):
            s = a + b
            add = ca if ca < cb else cb
            v = get(s)
            if v is None:
                v = add
            else:
                v += add
            if v >= T:
                sys.stdout.write("Yes\n")
                return
            accum[s] = v

    sys.stdout.write("No\n")

main()