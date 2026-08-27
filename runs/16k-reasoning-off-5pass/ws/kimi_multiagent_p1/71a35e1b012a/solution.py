import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = int(next(it))
        R[i] = int(next(it))

    ans = [0] * M

    # ---------- K = 1 ----------
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            ans[i] = 1
            print(1)
            print(' '.join(map(str, ans)))
            return

    # ---------- K = 2 ----------
    # Type A: two intervals covering [1, N]
    left_idx = -1
    for i in range(M):
        if L[i] == 1:
            if left_idx == -1 or R[i] > R[left_idx]:
                left_idx = i
    right_idx = -1
    for i in range(M):
        if R[i] == N:
            if right_idx == -1 or L[i] < L[right_idx]:
                right_idx = i
    if left_idx != -1 and right_idx != -1 and left_idx != right_idx:
        if R[left_idx] >= L[right_idx] - 1:
            ans[left_idx] = 1
            ans[right_idx] = 1
            print(2)
            print(' '.join(map(str, ans)))
            return

    # Type B: I_a superset of I_b, a != b  (then I_a + C_b covers everything)
    contains_pair = None
    sorted_by_L = sorted(range(M), key=lambda i: L[i])
    pos = 0
    bestR = -1
    bestR_idx = -1
    n = M
    while pos < n:
        q = pos
        curL = L[sorted_by_L[pos]]
        while q < n and L[sorted_by_L[q]] == curL:
            q += 1
        if bestR_idx != -1:
            for t in range(pos, q):
                b = sorted_by_L[t]
                if bestR >= R[b]:
                    contains_pair = (bestR_idx, b)
                    break
        if contains_pair:
            break
        if q - pos >= 2:
            gmax_idx = max(range(pos, q), key=lambda t: R[sorted_by_L[t]])
            gmax = sorted_by_L[gmax_idx]
            for t in range(pos, q):
                b = sorted_by_L[t]
                if b != gmax and R[gmax] >= R[b]:
                    contains_pair = (gmax, b)
                    break
        if contains_pair:
            break
        for t in range(pos, q):
            idx = sorted_by_L[t]
            if R[idx] > bestR:
                bestR = R[idx]
                bestR_idx = idx
        pos = q

    if contains_pair:
        a, b = contains_pair
        ans[a] = 1
        ans[b] = 2
        print(2)
        print(' '.join(map(str, ans)))
        return

    # Type C: disjoint pair (then C_a + C_b covers everything)
    minR_idx = min(range(M), key=lambda i: R[i])
    maxL_idx = max(range(M), key=lambda i: L[i])
    if R[minR_idx] < L[maxL_idx]:
        ans[minR_idx] = 2
        ans[maxL_idx] = 2
        print(2)
        print(' '.join(map(str, ans)))
        return

    # ---------- K = 3 ----------
    # Type (iv): 3 intervals covering [1, N]
    if left_idx != -1:
        reach = R[left_idx]
        mid_idx = -1
        for i in range(M):
            if i != left_idx and L[i] <= reach + 1:
                if mid_idx == -1 or R[i] > R[mid_idx]:
                    mid_idx = i
        if mid_idx != -1 and R[mid_idx] > reach:
            reach2 = R[mid_idx]
            end_idx = -1
            for i in range(M):
                if i != left_idx and i != mid_idx and L[i] <= reach2 + 1 and R[i] == N:
                    if end_idx == -1 or L[i] < L[end_idx]:
                        end_idx = i
            if end_idx != -1:
                ans[left_idx] = 1
                ans[mid_idx] = 1
                ans[end_idx] = 1
                print(3)
                print(' '.join(map(str, ans)))
                return

    # Prefix top-2 max-R structure over intervals sorted by L
    idx_by_L = sorted(range(M), key=lambda i: L[i])
    Ls = [L[i] for i in idx_by_L]
    pref_max1 = [-1] * M
    pref_max2 = [-1] * M
    for k in range(M):
        i = idx_by_L[k]
        if k == 0:
            pref_max1[k] = i
            pref_max2[k] = -1
        else:
            p1 = pref_max1[k-1]
            p2 = pref_max2[k-1]
            if p1 == -1 or R[i] >= R[p1]:
                pref_max1[k] = i
                pref_max2[k] = p1
            elif p2 == -1 or R[i] > R[p2]:
                pref_max1[k] = p1
                pref_max2[k] = i
            else:
                pref_max1[k] = p1
                pref_max2[k] = p2

    import bisect

    def query_maxR(x, ex1, ex2):
        # max R among indices with L <= x, excluding ex1 and ex2
        k = bisect.bisect_right(Ls, x) - 1
        if k < 0:
            return (-1, -1)
        c1 = pref_max1[k]
        if c1 != -1 and c1 != ex1 and c1 != ex2:
            return (R[c1], c1)
        c2 = pref_max2[k]
        if c2 != -1 and c2 != ex1 and c2 != ex2:
            return (R[c2], c2)
        # fallback: linear scan (rare)
        best = -1
        besti = -1
        for t in range(k + 1):
            i = idx_by_L[t]
            if i != ex1 and i != ex2 and R[i] > best:
                best = R[i]
                besti = i
        return (best, besti)

    # Type (iii): 1 complement C_b + 2 intervals covering [L_b, R_b]
    found3 = None
    for b in range(M):
        Lb, Rb = L[b], R[b]
        r1, a = query_maxR(Lb, b, -1)
        if a == -1 or r1 < Lb:
            continue
        x2 = r1 + 1
        if x2 > N:
            x2 = N
        r2, c = query_maxR(x2, b, a)
        if c == -1:
            continue
        if r2 >= Rb:
            found3 = (b, a, c)
            break

    if found3:
        b, a, c = found3
        ans[b] = 2
        ans[a] = 1
        ans[c] = 1
        print(3)
        print(' '.join(map(str, ans)))
        return

    # Type (ii): 2 complements + 1 interval containing I_b ∩ I_c
    byL = sorted(range(M), key=lambda i: (-L[i], R[i]))[:2]
    byR = sorted(range(M), key=lambda i: (R[i], -L[i]))[:2]
    for b in byL:
        for c in byR:
            if b == c:
                continue
            segL = L[b] if L[b] > L[c] else L[c]
            segR = R[b] if R[b] < R[c] else R[c]
            if segL > segR:
                continue
            r1, a = query_maxR(segL, b, c)
            if a != -1 and r1 >= segR:
                ans[b] = 2
                ans[c] = 2
                ans[a] = 1
                print(3)
                print(' '.join(map(str, ans)))
                return

    print(-1)

main()