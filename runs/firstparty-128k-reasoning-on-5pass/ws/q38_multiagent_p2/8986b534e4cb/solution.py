import sys
from bisect import bisect_left, bisect_right


def solve_case(N, persons, queries):
    M = len(persons)
    INF = M + 1

    L = [0] * M
    R = [0] * M
    Sgn = [0] * M
    for i, (S, T) in enumerate(persons):
        if S < T:
            L[i] = S - 1
            R[i] = T - 1
            Sgn[i] = 0
        else:
            L[i] = T - 1
            R[i] = S - 1
            Sgn[i] = 1

    nxt = [INF] * M

    # Bad pairs sharing an endpoint: any sign, same l or same r.
    last_l = [INF] * N
    last_r = [INF] * N
    for i in range(M - 1, -1, -1):
        li = L[i]
        ri = R[i]
        c = last_l[li]
        if c < nxt[i]:
            nxt[i] = c
        c = last_r[ri]
        if c < nxt[i]:
            nxt[i] = c
        last_l[li] = i
        last_r[ri] = i
    del last_l, last_r

    def process_sign(sgn, L=L, R=R, Sgn=Sgn, nxt=nxt, N=N, M=M):
        intervals = [i for i in range(M) if Sgn[i] == sgn]
        if not intervals:
            return

        vals = [None] * N
        used = []
        for i in intervals:
            li = L[i]
            if vals[li] is None:
                vals[li] = []
                used.append(li)
            vals[li].append(R[i])

        bits = [None] * N
        cnt = [0] * N
        maxv = [-1] * N
        top = [0] * N

        for li in used:
            lst = vals[li]
            lst.sort()
            w = 1
            for j in range(1, len(lst)):
                x = lst[j]
                if x != lst[w - 1]:
                    lst[w] = x
                    w += 1
            if w < len(lst):
                del lst[w:]
            K = len(lst)
            bits[li] = [0] * (K + 1)
            top[li] = 1 << (K.bit_length() - 1)

        id_map = {}
        comp_idx = [-1] * M
        bl = bisect_left
        SHIFT = N.bit_length()
        for i in intervals:
            li = L[i]
            ri = R[i]
            idx = bl(vals[li], ri)
            comp_idx[i] = idx
            id_map[(li << SHIFT) | ri] = i

        size = 1
        while size < N:
            size <<= 1
        tree = [-1] * (2 * size)

        def seg_update(pos, val, tree=tree, size=size):
            idx = pos + size
            if tree[idx] == val:
                return
            tree[idx] = val
            idx >>= 1
            while idx:
                left = tree[idx << 1]
                right = tree[(idx << 1) | 1]
                new = left if left >= right else right
                if tree[idx] == new:
                    break
                tree[idx] = new
                idx >>= 1

        def find_prefix(x, th, tree=tree, size=size):
            if x < 0:
                return -1
            if tree[1] <= th:
                return -1
            if x + 1 == size:
                node = 1
                while node < size:
                    right = (node << 1) | 1
                    if tree[right] > th:
                        node = right
                    else:
                        node = right - 1
                return node - size

            r = size + x + 1
            l = size
            while l < r:
                if r & 1:
                    r -= 1
                    if tree[r] > th:
                        node = r
                        while node < size:
                            right = (node << 1) | 1
                            if tree[right] > th:
                                node = right
                            else:
                                node = right - 1
                        return node - size
                l >>= 1
                r >>= 1
            return -1

        def bit_add(li, idx, delta, bits=bits):
            bit = bits[li]
            K = len(bit) - 1
            if K == 1:
                bit[1] += delta
                return
            i = idx + 1
            while i <= K:
                bit[i] += delta
                i += i & -i

        def bit_max(li, vals=vals, bits=bits, cnt=cnt, top=top):
            total = cnt[li]
            if total == 0:
                return -1
            bit = bits[li]
            K = len(bit) - 1
            if K == 1:
                return vals[li][0]
            idx = 0
            bitmask = top[li]
            while bitmask:
                ni = idx + bitmask
                if ni <= K and bit[ni] < total:
                    idx = ni
                    total -= bit[ni]
                bitmask >>= 1
            pos = idx + 1
            return vals[li][pos - 1]

        def successor(li, th, vals=vals, bits=bits, cnt=cnt, top=top, br=bisect_right):
            total = cnt[li]
            if total == 0:
                return None
            vals_l = vals[li]
            K = len(vals_l)
            if K == 1:
                val = vals_l[0]
                if val > th:
                    return (val, 0)
                return None

            pos = br(vals_l, th)
            if pos >= K:
                return None
            bit = bits[li]

            s = 0
            i = pos
            while i > 0:
                s += bit[i]
                i -= i & -i
            if s == total:
                return None

            k = s + 1
            idx = 0
            bitmask = top[li]
            while bitmask:
                ni = idx + bitmask
                if ni <= K and bit[ni] < k:
                    idx = ni
                    k -= bit[ni]
                bitmask >>= 1
            pos1 = idx + 1
            return (vals_l[pos1 - 1], pos1 - 1)

        for cur in intervals:
            li = L[cur]
            ri = R[cur]

            # Earlier intervals p < li < rv < ri.
            while True:
                p = find_prefix(li - 1, li)
                if p < 0:
                    break
                res = successor(p, li)
                if res is None:
                    break
                rv, idx = res
                if rv >= ri:
                    break

                old = id_map[(p << SHIFT) | rv]
                if nxt[old] > cur:
                    nxt[old] = cur

                bit_add(p, idx, -1)
                cnt[p] -= 1
                if rv == maxv[p]:
                    if cnt[p] == 0:
                        newmax = -1
                    else:
                        newmax = bit_max(p)
                    maxv[p] = newmax
                    seg_update(p, newmax)

            # Earlier intervals li < p < ri < rv.
            while True:
                p = find_prefix(ri - 1, ri)
                if p < 0 or p <= li:
                    break
                res = successor(p, ri)
                if res is None:
                    break
                rv, idx = res

                old = id_map[(p << SHIFT) | rv]
                if nxt[old] > cur:
                    nxt[old] = cur

                bit_add(p, idx, -1)
                cnt[p] -= 1
                if rv == maxv[p]:
                    if cnt[p] == 0:
                        newmax = -1
                    else:
                        newmax = bit_max(p)
                    maxv[p] = newmax
                    seg_update(p, newmax)

            idx = comp_idx[cur]
            bit_add(li, idx, 1)
            cnt[li] += 1
            if ri > maxv[li]:
                maxv[li] = ri
                seg_update(li, ri)

    process_sign(0)
    process_sign(1)

    suf = [INF] * (M + 1)
    for i in range(M - 1, -1, -1):
        v = nxt[i]
        if suf[i + 1] < v:
            v = suf[i + 1]
        suf[i] = v

    out = []
    for Lq, Rq in queries:
        if suf[Lq - 1] > Rq - 1:
            out.append("Yes")
        else:
            out.append("No")
    return out


def brute_case(N, persons, queries):
    M = len(persons)
    L = [0] * M
    R = [0] * M
    Sgn = [0] * M
    for i, (S, T) in enumerate(persons):
        if S < T:
            L[i] = S - 1
            R[i] = T - 1
            Sgn[i] = 0
        else:
            L[i] = T - 1
            R[i] = S - 1
            Sgn[i] = 1

    out = []
    for Lq, Rq in queries:
        parent = list(range(N))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra = find(a)
            rb = find(b)
            if ra != rb:
                parent[rb] = ra

        for i in range(Lq - 1, Rq):
            union(L[i], R[i])

        comp = [find(i) for i in range(N)]
        adj = [[] for _ in range(N)]
        ok = True

        for i in range(Lq - 1, Rq):
            if Sgn[i] == 0:
                u = comp[L[i]]
                for x in range(L[i] + 1, R[i]):
                    v = comp[x]
                    if u == v:
                        ok = False
                        break
                    adj[u].append(v)
            else:
                v = comp[L[i]]
                for x in range(L[i] + 1, R[i]):
                    u = comp[x]
                    if u == v:
                        ok = False
                        break
                    adj[u].append(v)
            if not ok:
                break

        if ok:
            color = [0] * N

            def dfs(u):
                color[u] = 1
                for v in adj[u]:
                    if color[v] == 1:
                        return True
                    if color[v] == 0 and dfs(v):
                        return True
                color[u] = 2
                return False

            for i in range(N):
                if color[i] == 0 and dfs(i):
                    ok = False
                    break

        out.append("Yes" if ok else "No")
    return out


def self_test():
    import random

    sys.setrecursionlimit(1000000)

    def check(N, persons, queries, expected):
        got = solve_case(N, persons, queries)
        if got != expected:
            print("MISMATCH")
            print(N, persons, queries)
            print("expected", expected)
            print("got", got)
            raise AssertionError

    check(
        5,
        [(4, 2), (1, 3), (3, 5), (2, 4)],
        [(1, 3), (2, 4)],
        ["Yes", "No"],
    )
    check(
        7,
        [(1, 5), (2, 4), (4, 6), (7, 1), (5, 3), (1, 6)],
        [(1, 6), (4, 4), (2, 5)],
        ["No", "Yes", "Yes"],
    )

    # Same-sign shared endpoint cases.
    check(4, [(1, 4), (1, 3)], [(1, 2)], ["No"])
    check(4, [(1, 4), (2, 4)], [(1, 2)], ["No"])
    # Same-sign strict crossing.
    check(5, [(1, 4), (2, 5)], [(1, 2)], ["No"])
    # Opposite-sign strict crossing is feasible.
    check(5, [(1, 4), (5, 2)], [(1, 2)], ["Yes"])

    random.seed(12345)
    for _ in range(100):
        N = random.randint(3, 6)
        pairs = [
            (S, T)
            for S in range(1, N + 1)
            for T in range(1, N + 1)
            if abs(S - T) > 1
        ]
        random.shuffle(pairs)
        M = random.randint(1, len(pairs))
        persons = pairs[:M]
        maxq = M * (M + 1) // 2
        Q = random.randint(1, min(20, maxq))
        queries = []
        for __ in range(Q):
            Lq = random.randint(1, M)
            Rq = random.randint(Lq, M)
            queries.append((Lq, Rq))

        expected = brute_case(N, persons, queries)
        got = solve_case(N, persons, queries)
        if got != expected:
            print("RANDOM MISMATCH")
            print(N, persons, queries)
            print("expected", expected)
            print("got", got)
            raise AssertionError

    print("self-test passed")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        self_test()
        return

    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, Q = data[0], data[1], data[2]
    idx = 3

    persons = []
    for _ in range(M):
        persons.append((data[idx], data[idx + 1]))
        idx += 2

    queries = []
    for _ in range(Q):
        queries.append((data[idx], data[idx + 1]))
        idx += 2

    del data

    ans = solve_case(N, persons, queries)
    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()