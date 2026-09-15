import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N]
    B = data[1 + N:1 + 2 * N]

    ca = A.count(-1)
    cb = B.count(-1)
    K = N - ca - cb

    # If no known-known pair is forced, or only one is forced, it is always possible.
    if K <= 1:
        print("Yes")
        return

    # No unknowns: need a perfect matching with one constant sum.
    if ca == 0 and cb == 0:
        A.sort()
        B.sort(reverse=True)
        s = A[0] + B[0]
        ok = True
        for i in range(N):
            if A[i] + B[i] != s:
                ok = False
                break
        print("Yes" if ok else "No")
        return

    freqA = {}
    freqB = {}
    max_known = -1

    for x in A:
        if x != -1:
            freqA[x] = freqA.get(x, 0) + 1
            if x > max_known:
                max_known = x

    for x in B:
        if x != -1:
            freqB[x] = freqB.get(x, 0) + 1
            if x > max_known:
                max_known = x

    totalA = N - ca
    totalB = N - cb

    if K > totalA or K > totalB or not freqA or not freqB:
        print("No")
        return

    # If one value pair alone can provide K matches, answer immediately.
    max_big_a = -1
    for a, c in freqA.items():
        if c >= K and a > max_big_a:
            max_big_a = a

    max_big_b = -1
    for b, c in freqB.items():
        if c >= K and b > max_big_b:
            max_big_b = b

    if max_big_a != -1 and max_big_b != -1 and max_big_a + max_big_b >= max_known:
        print("Yes")
        return

    # If one side has all distinct known values, every distinct value pair contributes 1.
    unit = (len(freqA) == totalA) or (len(freqB) == totalB)
    minD = min(len(freqA), len(freqB))

    if unit and minD < K:
        print("No")
        return

    # Extreme-candidate shortcut.
    # If a solution exists, choose exactly K known-known matches.
    # Then at most cb known A-values and ca known B-values are unmatched.
    # The smallest matched A is among the first cb+1 sorted known A-values,
    # and the largest matched B is among the first ca+1 sorted known B-values.
    # Hence the target sum is one of their sums.
    takeA = min(cb + 1, totalA)
    takeB = min(ca + 1, totalB)
    cand_prod = takeA * takeB

    if cand_prod <= 100_000 and cand_prod * minD <= 8_000_000:
        knownA = [x for x in A if x != -1]
        knownA.sort()
        knownB = [x for x in B if x != -1]
        knownB.sort(reverse=True)

        candA = knownA[:takeA]
        candB = knownB[:takeB]

        candidates = set()
        for a in candA:
            for b in candB:
                s = a + b
                if s >= max_known:
                    candidates.add(s)

        if len(freqA) <= len(freqB):
            small_items = list(freqA.items())
            other = freqB
        else:
            small_items = list(freqB.items())
            other = freqA

        get = other.get

        for s in candidates:
            total = 0
            for v, c in small_items:
                oc = get(s - v, 0)
                if oc:
                    total += c if c < oc else oc
                    if total >= K:
                        print("Yes")
                        return

        print("No")
        return

    # General case: aggregate contributions of all distinct known-value pairs.
    itemsA = list(freqA.items())
    itemsB = list(freqB.items())

    if len(itemsA) <= len(itemsB):
        outer = itemsA
        inner = itemsB
    else:
        outer = itemsB
        inner = itemsA

    inner.sort()
    outer.sort()

    inner_vals = [v for v, _ in inner]
    inner_counts = [c for _, c in inner]
    outer_vals = [v for v, _ in outer]
    outer_counts = [c for _, c in outer]

    m = len(inner_vals)
    bl = bisect_left
    mk = max_known

    starts = [0] * len(outer_vals)
    pair_count = 0

    for i, a in enumerate(outer_vals):
        st = bl(inner_vals, mk - a)
        starts[i] = st
        if st < m:
            pair_count += m - st

    if pair_count == 0:
        print("No")
        return

    if unit and pair_count < K:
        print("No")
        return

    SHIFT = 12
    MASK = (1 << SHIFT) - 1

    records = [0] * pair_count
    idx = 0
    iv = inner_vals
    ic = inner_counts
    rec = records

    if unit:
        for i, a in enumerate(outer_vals):
            st = starts[i]
            for j in range(st, m):
                rec[idx] = a + iv[j]
                idx += 1
    else:
        ish = [v << SHIFT for v in iv]
        ish_ic = [ish[j] + ic[j] for j in range(m)]
        min_ic = min(ic)
        max_ic = max(ic)

        for i, a in enumerate(outer_vals):
            st = starts[i]
            if st >= m:
                continue

            c = outer_counts[i]
            a_shift = a << SHIFT

            if c <= min_ic:
                base = a_shift | c
                for j in range(st, m):
                    rec[idx] = base + ish[j]
                    idx += 1
            elif c >= max_ic:
                for j in range(st, m):
                    rec[idx] = a_shift + ish_ic[j]
                    idx += 1
            else:
                for j in range(st, m):
                    bc = ic[j]
                    cc = c if c < bc else bc
                    rec[idx] = a_shift + ish[j] + cc
                    idx += 1

    records.sort()

    if unit:
        prev = -1
        cnt = 0

        for x in records:
            if x == prev:
                cnt += 1
                if cnt >= K:
                    print("Yes")
                    return
            else:
                if cnt >= K:
                    print("Yes")
                    return
                prev = x
                cnt = 1

        if cnt >= K:
            print("Yes")
            return
    else:
        prev = -1
        total = 0

        for x in records:
            s = x >> SHIFT
            if s == prev:
                total += x & MASK
                if total >= K:
                    print("Yes")
                    return
            else:
                if total >= K:
                    print("Yes")
                    return
                prev = s
                total = x & MASK

        if total >= K:
            print("Yes")
            return

    print("No")


if __name__ == "__main__":
    solve()