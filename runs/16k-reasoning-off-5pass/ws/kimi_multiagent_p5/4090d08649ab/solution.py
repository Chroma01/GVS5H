import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))

    # f(L,R) = (#distinct values in range) - (# v such that both v and v+1 appear)
    # answer = D - P

    # D: sum of distinct counts over all subarrays.
    # Position i contributes to subarrays where it is the first occurrence of A_i.
    last = {}
    D = 0
    for i, a in enumerate(A):
        p = last.get(a, -1)
        D += (i - p) * (n - i)
        last[a] = i

    # occurrence lists per value (naturally sorted by construction)
    pos = {}
    for i, a in enumerate(A):
        pos.setdefault(a, []).append(i)

    total_sub = n * (n + 1) // 2

    def count_missing(plist):
        # subarrays avoiding every index in plist (plist sorted)
        res = 0
        prev = -1
        for p in plist:
            gap = p - prev - 1
            res += gap * (gap + 1) // 2
            prev = p
        gap = n - prev - 1
        res += gap * (gap + 1) // 2
        return res

    P = 0
    for v, pv in pos.items():
        w = v + 1
        pw = pos.get(w)
        if pw is None:
            continue
        miss_v = count_missing(pv)
        miss_w = count_missing(pw)
        # two-pointer merge of two sorted lists, O(len)
        i = j = 0
        lv, lw = len(pv), len(pw)
        merged = []
        while i < lv and j < lw:
            if pv[i] <= pw[j]:
                merged.append(pv[i]); i += 1
            else:
                merged.append(pw[j]); j += 1
        if i < lv:
            merged.extend(pv[i:])
        else:
            merged.extend(pw[j:])
        miss_both = count_missing(merged)
        # inclusion-exclusion: subarrays containing at least one v and one w
        P += total_sub - miss_v - miss_w + miss_both

    print(D - P)

solve()