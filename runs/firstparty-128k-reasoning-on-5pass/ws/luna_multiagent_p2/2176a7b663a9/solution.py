import sys
from bisect import bisect_left, bisect_right

INF = 10**30


class MinSegTree:
    __slots__ = ("n", "base", "tag")

    def __init__(self, values, size):
        n = 1
        while n < size:
            n <<= 1
        self.n = n
        base = [INF] * (2 * n)
        for i, v in enumerate(values):
            base[n + i] = v
        for i in range(n - 1, 0, -1):
            a = base[i << 1]
            b = base[i << 1 | 1]
            base[i] = a if a < b else b
        self.base = base
        self.tag = [INF] * (2 * n)

    def update(self, ql, qr, value):
        if ql >= qr:
            return
        n = self.n
        base = self.base
        tag = self.tag

        def rec(node, left, right):
            if qr <= left or right <= ql:
                return
            if ql <= left and right <= qr:
                if value < tag[node]:
                    tag[node] = value
                return
            mid = (left + right) >> 1
            rec(node << 1, left, mid)
            rec(node << 1 | 1, mid, right)

        rec(1, 0, n)

    def query(self, ql, qr):
        if ql >= qr:
            return INF
        n = self.n
        base = self.base
        tag = self.tag

        def rec(node, left, right, carried):
            if qr <= left or right <= ql:
                return INF
            cur = carried
            if tag[node] < cur:
                cur = tag[node]
            if ql <= left and right <= qr:
                return base[node] + cur
            mid = (left + right) >> 1
            a = rec(node << 1, left, mid, cur)
            b = rec(node << 1 | 1, mid, right, cur)
            return a if a < b else b

        return rec(1, 0, n, INF)


def main():
    input = sys.stdin.buffer.readline

    N = int(input())
    W = list(map(int, input().split()))
    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i], R[i] = map(int, input().split())

    Q = int(input())
    S = [0] * Q
    T = [0] * Q
    for i in range(Q):
        s, t = map(int, input().split())
        S[i] = s - 1
        T[i] = t - 1

    answer = [INF] * Q

    # Direct edges.
    for qi in range(Q):
        s = S[qi]
        t = T[qi]
        if R[s] < L[t] or R[t] < L[s]:
            answer[qi] = W[s] + W[t]

    # Two-edge paths with the intermediate vertex on the same side
    # of both endpoints.
    order_r = sorted(range(N), key=R.__getitem__)
    order_l = sorted(range(N), key=L.__getitem__)

    pref_r = [INF] * (N + 1)
    for i, v in enumerate(order_r):
        pref_r[i + 1] = min(pref_r[i], W[v])

    suff_l = [INF] * (N + 1)
    for i in range(N - 1, -1, -1):
        suff_l[i] = min(suff_l[i + 1], W[order_l[i]])

    r_values = [R[v] for v in order_r]
    l_values = [L[v] for v in order_l]

    for qi in range(Q):
        s = S[qi]
        t = T[qi]

        p = bisect_left(r_values, min(L[s], L[t]))
        if p:
            answer[qi] = min(answer[qi], W[s] + W[t] + pref_r[p])

        p = bisect_right(l_values, max(R[s], R[t]))
        if p < N:
            answer[qi] = min(answer[qi], W[s] + W[t] + suff_l[p])

    # Cross-sided two-edge paths, handled offline with a Fenwick tree.
    def cross_two(first_is_left):
        # Intermediate k satisfies:
        #   R[k] < L[first] and L[k] > R[second]
        queries = []
        for qi in range(Q):
            a = S[qi] if first_is_left else T[qi]
            b = T[qi] if first_is_left else S[qi]
            queries.append((L[a], R[b], qi))

        queries.sort()
        vertices = sorted(range(N), key=R.__getitem__)

        # Fenwick tree over reversed L-order, storing minimum W.
        bit = [INF] * (N + 2)

        def bit_update(pos, value):
            while pos <= N:
                if value < bit[pos]:
                    bit[pos] = value
                pos += pos & -pos

        def bit_query(pos):
            res = INF
            while pos:
                if bit[pos] < res:
                    res = bit[pos]
                pos -= pos & -pos
            return res

        ptr = 0
        for left_bound, right_bound, qi in queries:
            while ptr < N and R[vertices[ptr]] < left_bound:
                v = vertices[ptr]
                lp = bisect_left(l_values, L[v])
                rev = N - lp
                bit_update(rev, W[v])
                ptr += 1

            # L[k] > right_bound.
            p = bisect_right(l_values, right_bound)
            count = N - p
            if count > 0:
                best = bit_query(count)
                if best < INF:
                    s = S[qi]
                    t = T[qi]
                    answer[qi] = min(answer[qi], W[s] + W[t] + best)

    cross_two(True)
    cross_two(False)

    # Three-edge paths.
    #
    # side_m: 0 => m is left of t, 1 => m is right of t
    # relation: 0 => k is left of m, 1 => k is right of m
    # side_k: 0 => k is left of s, 1 => k is right of s
    #
    # Each pass sweeps the admissible m vertices and range-updates all
    # admissible k coordinates. The segment tree stores min(W[k]+W[m]).
    sorted_by_r = sorted(range(N), key=R.__getitem__)
    sorted_by_l = sorted(range(N), key=L.__getitem__)

    def run_three(side_m, relation, side_k):
        key_values = R if side_k == 0 else L
        coords = sorted(set(key_values))
        pos = {x: i for i, x in enumerate(coords)}
        base_values = [INF] * len(coords)
        for v in range(N):
            p = pos[key_values[v]]
            if W[v] < base_values[p]:
                base_values[p] = W[v]

        seg = MinSegTree(base_values, len(coords))

        if side_m == 0:
            m_order = sorted_by_r
            q_order = sorted(
                range(Q),
                key=lambda qi: L[T[qi]]
            )
            ptr = 0

            for qi in q_order:
                threshold = L[T[qi]]
                while ptr < N and R[m_order[ptr]] < threshold:
                    m = m_order[ptr]
                    if relation == 0:
                        # k left of m: R[k] < L[m]
                        end = bisect_left(coords, L[m])
                        seg.update(0, end, W[m])
                    else:
                        # k right of m: L[k] > R[m]
                        start = bisect_right(coords, R[m])
                        seg.update(start, len(coords), W[m])
                    ptr += 1

                s = S[qi]
                if side_k == 0:
                    end = bisect_left(coords, L[s])
                    best = seg.query(0, end)
                else:
                    start = bisect_right(coords, R[s])
                    best = seg.query(start, len(coords))

                if best < INF:
                    answer[qi] = min(answer[qi], W[s] + W[T[qi]] + best)
        else:
            m_order = sorted_by_l[::-1]
            q_order = sorted(
                range(Q),
                key=lambda qi: R[T[qi]],
                reverse=True
            )
            ptr = 0

            for qi in q_order:
                threshold = R[T[qi]]
                while ptr < N and L[m_order[ptr]] > threshold:
                    m = m_order[ptr]
                    if relation == 0:
                        end = bisect_left(coords, L[m])
                        seg.update(0, end, W[m])
                    else:
                        start = bisect_right(coords, R[m])
                        seg.update(start, len(coords), W[m])
                    ptr += 1

                s = S[qi]
                if side_k == 0:
                    end = bisect_left(coords, L[s])
                    best = seg.query(0, end)
                else:
                    start = bisect_right(coords, R[s])
                    best = seg.query(start, len(coords))

                if best < INF:
                    answer[qi] = min(answer[qi], W[s] + W[T[qi]] + best)

    for side_m in (0, 1):
        for relation in (0, 1):
            for side_k in (0, 1):
                run_three(side_m, relation, side_k)

    out = []
    for x in answer:
        out.append(str(x if x < INF else -1))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()