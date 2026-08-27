import sys

INF = 10**30


def ints():
    data = sys.stdin.buffer.read()
    num = 0
    inside = False
    for c in data:
        if 48 <= c <= 57:
            num = num * 10 + c - 48
            inside = True
        else:
            if inside:
                yield num
                num = 0
                inside = False
    if inside:
        yield num


class ValleyData:
    # Supports:
    # min(W_a + W_b + W_c)
    # where R_a < x, R_c < y, L_b > max(R_a, R_c).
    def __init__(self, left, right, weight, m, reflected=False):
        self.m = m
        coord_size = m + 1
        c = m + 1

        by_r = [INF] * coord_size
        by_l = [INF] * coord_size

        if reflected:
            for l, r, w in zip(left, right, weight):
                nl = c - r
                nr = c - l
                if w < by_r[nr]:
                    by_r[nr] = w
                if w < by_l[nl]:
                    by_l[nl] = w
        else:
            for l, r, w in zip(left, right, weight):
                if w < by_r[r]:
                    by_r[r] = w
                if w < by_l[l]:
                    by_l[l] = w

        pref = [INF] * coord_size
        cur = INF
        for i in range(coord_size):
            v = by_r[i]
            if v < cur:
                cur = v
            pref[i] = cur
        self.pref = pref

        suffix = [INF] * coord_size
        cur = INF
        for i in range(m - 1, -1, -1):
            v = by_l[i + 1]
            if v < cur:
                cur = v
            suffix[i] = cur

        d = [INF] * coord_size
        pref_h = [INF] * coord_size
        cur_h = INF
        for i in range(coord_size):
            if by_r[i] < INF and suffix[i] < INF:
                d[i] = by_r[i] + suffix[i]
                if pref[i] < INF:
                    h = d[i] + pref[i]
                    if h < cur_h:
                        cur_h = h
            pref_h[i] = cur_h
        self.pref_h = pref_h

        size = 1
        while size < coord_size:
            size <<= 1
        tree = [INF] * (size << 1)
        tree[size:size + coord_size] = d
        for i in range(size - 1, 0, -1):
            a = tree[i << 1]
            b = tree[i << 1 | 1]
            tree[i] = a if a < b else b
        self.size = size
        self.tree = tree

    def range_min(self, l, r):
        if l > r:
            return INF
        l += self.size
        r += self.size
        ans = INF
        tree = self.tree
        while l <= r:
            if l & 1:
                if tree[l] < ans:
                    ans = tree[l]
                l += 1
            if not (r & 1):
                if tree[r] < ans:
                    ans = tree[r]
                r -= 1
            l >>= 1
            r >>= 1
        return ans

    def query(self, x, y):
        # Split according to whether R_a >= R_c or R_a < R_c.
        # This routine handles R_a >= R_c.
        ans = INF

        k = x - 1
        if y - 1 < k:
            k = y - 1
        if k >= 0:
            ans = self.pref_h[k]

        # For R_a >= y, the best c is any interval with R_c < y.
        if y <= x - 1:
            p = self.pref[y - 1]
            if p < INF:
                d = self.range_min(y, x - 1)
                if d < INF:
                    v = p + d
                    if v < ans:
                        ans = v
        return ans


def main():
    it = ints()
    n = next(it)
    w = [next(it) for _ in range(n)]

    left = [0] * n
    right = [0] * n
    for i in range(n):
        left[i] = next(it)
        right[i] = next(it)

    m = 2 * n
    c = m + 1

    normal = ValleyData(left, right, w, m, False)
    mirrored = ValleyData(left, right, w, m, True)

    q = next(it)
    out = []

    for _ in range(q):
        s = next(it) - 1
        t = next(it) - 1

        ls, rs = left[s], right[s]
        lt, rt = left[t], right[t]

        # A direct edge is always optimal because all weights are positive.
        if rs < lt or rt < ls:
            out.append(str(w[s] + w[t]))
            continue

        best_mid = INF

        # Two edges: an interval wholly left of both, or wholly right of both.
        v = normal.pref[min(ls, lt) - 1]
        if v < best_mid:
            best_mid = v
        # normal suffix-minimum is not exposed; use the equivalent value
        # through the ValleyData construction's tree is inconvenient here.
        # Compute right-side minima using mirrored prefix minima:
        # L_i > z <=> transformed R_i < c-z.
        z = max(rs, rt)
        v = mirrored.pref[c - z - 1]
        if v < best_mid:
            best_mid = v

        # Three edges, in the two possible alternating orientations.
        # left of s + right of t
        a = normal.pref[ls - 1]
        b = mirrored.pref[c - rt - 1]
        if a < INF and b < INF:
            v = a + b
            if v < best_mid:
                best_mid = v

        # right of s + left of t
        a = mirrored.pref[c - rs - 1]
        b = normal.pref[lt - 1]
        if a < INF and b < INF:
            v = a + b
            if v < best_mid:
                best_mid = v

        # Four edges with a central right-hand peak:
        # a left of s, c left of t, b right of both a and c.
        v1 = normal.query(ls, lt)
        v2 = normal.query(lt, ls)
        if v2 < v1:
            v1 = v2
        if v1 < best_mid:
            best_mid = v1

        # Mirrored version: a right of s, c right of t,
        # b left of both a and c.
        x = c - rs
        y = c - rt
        v1 = mirrored.query(x, y)
        v2 = mirrored.query(y, x)
        if v2 < v1:
            v1 = v2
        if v1 < best_mid:
            best_mid = v1

        if best_mid >= INF:
            out.append("-1")
        else:
            out.append(str(w[s] + w[t] + best_mid))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()