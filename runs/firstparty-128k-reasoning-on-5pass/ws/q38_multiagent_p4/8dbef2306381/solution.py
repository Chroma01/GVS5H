import sys
from collections import deque

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    M = next(it)
    A = next(it)
    B = next(it)

    intervals = []
    for _ in range(M):
        L = next(it)
        R = next(it)
        if intervals and L <= intervals[-1][1] + 1:
            if R > intervals[-1][1]:
                intervals[-1][1] = R
        else:
            intervals.append([L, R])

    K = len(intervals)

    # A bad block of length at least B cannot be jumped over.
    for L, R in intervals:
        if R - L + 1 >= B:
            print("No")
            return

    cand = [1, N]
    for L, R in intervals:
        s = L - B
        if s < 1:
            s = 1
        cand.extend(range(s, L))  # s .. L-1
        s = R + 1
        e = R + B
        if e > N:
            e = N
        cand.extend(range(s, e + 1))  # s .. e

    cand.sort()
    crit = []
    seg_id = []
    idx = 0
    prev = None
    for x in cand:
        if x == prev:
            continue
        prev = x
        while idx < K and intervals[idx][1] < x:
            idx += 1
        if idx < K and intervals[idx][0] <= x <= intervals[idx][1]:
            continue
        crit.append(x)
        seg_id.append(idx)

    if not crit or crit[0] != 1:
        print("No")
        return
    if N == 1:
        print("Yes")
        return

    recent = deque([crit[0]])
    ans = False

    if A == B:
        seg_mask = [0] * (K + 1)
        seg_mask[seg_id[0]] = 1 << (crit[0] % A)
        for i in range(1, len(crit)):
            x = crit[i]
            while recent and x - recent[0] > B:
                recent.popleft()
            ok = False
            if recent and x - recent[0] >= A:
                ok = True
            else:
                seg = seg_id[i]
                if seg_mask[seg] & (1 << (x % A)):
                    ok = True
            if ok:
                if x == N:
                    ans = True
                recent.append(x)
                seg = seg_id[i]
                seg_mask[seg] |= 1 << (x % A)
    else:
        if A == 1:
            T = 1
        else:
            diff = B - A
            k0 = (A - 1 + diff - 1) // diff
            T = k0 * A
        table = [False] * (T + 1)
        for d in range(1, T):
            table[d] = (d + B - 1) // B <= d // A

        seg_reach = [[] for _ in range(K + 1)]
        seg_reach[seg_id[0]].append(crit[0])

        for i in range(1, len(crit)):
            x = crit[i]
            while recent and x - recent[0] > B:
                recent.popleft()
            ok = False
            if recent and x - recent[0] >= A:
                ok = True
            else:
                seg = seg_id[i]
                lst = seg_reach[seg]
                if lst:
                    if x - lst[0] >= T:
                        ok = True
                    else:
                        for u in lst:
                            d = x - u
                            if d < A:
                                break
                            if table[d]:
                                ok = True
                                break
            if ok:
                if x == N:
                    ans = True
                recent.append(x)
                seg_reach[seg_id[i]].append(x)

    print("Yes" if ans else "No")

if __name__ == "__main__":
    main()