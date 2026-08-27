import sys
from array import array


class DominanceStructure:
    """Dynamic points (key, value), supporting:
       insert(key, value, index)
       max index among inserted points with key in [ql, qr] and value < threshold
    """
    __slots__ = ("size", "nodes", "bits")

    def __init__(self, points, n):
        size = 1
        while size <= n:
            size <<= 1
        self.size = size

        nodes = {}
        for key, value in points:
            p = size + key - 1
            while p:
                nodes.setdefault(p, []).append(value)
                p >>= 1

        for p, vals in nodes.items():
            vals = sorted(set(vals))
            nodes[p] = vals

        bits = {}
        for p, vals in nodes.items():
            bits[p] = array("i", [0]) * (len(vals) + 1)

        self.nodes = nodes
        self.bits = bits

    def update(self, key, value, idx):
        p = self.size + key - 1
        nodes = self.nodes
        bits = self.bits
        while p:
            vals = nodes.get(p)
            if vals is not None:
                lo, hi = 0, len(vals)
                while lo < hi:
                    mid = (lo + hi) >> 1
                    if vals[mid] < value:
                        lo = mid + 1
                    else:
                        hi = mid
                k = lo + 1
                bit = bits[p]
                while k < len(bit):
                    if bit[k] < idx:
                        bit[k] = idx
                    k += k & -k
            p >>= 1

    def _prefix(self, p, threshold):
        vals = self.nodes[p]
        lo, hi = 0, len(vals)
        while lo < hi:
            mid = (lo + hi) >> 1
            if vals[mid] < threshold:
                lo = mid + 1
            else:
                hi = mid
        k = lo
        bit = self.bits[p]
        ans = 0
        while k:
            if ans < bit[k]:
                ans = bit[k]
            k -= k & -k
        return ans

    def query(self, left, right, threshold):
        if left > right:
            return 0
        left += self.size - 1
        right += self.size - 1
        ans = 0
        while left <= right:
            if left & 1:
                if left in self.nodes:
                    v = self._prefix(left, threshold)
                    if ans < v:
                        ans = v
                left += 1
            if not (right & 1):
                if right in self.nodes:
                    v = self._prefix(right, threshold)
                    if ans < v:
                        ans = v
                right -= 1
            left >>= 1
            right >>= 1
        return ans


def main():
    input = sys.stdin.buffer.readline
    n, m, q = map(int, input().split())

    people = []
    plus_points_end = []
    minus_points_end = []
    plus_points_start = []
    minus_points_start = []

    for _ in range(m):
        s, t = map(int, input().split())
        if s < t:
            l, r, sign = s, t, 0
        else:
            l, r, sign = t, s, 1
        people.append((l, r, sign))
        if sign == 0:
            plus_points_end.append((r, l))
            plus_points_start.append((l, r))
        else:
            minus_points_end.append((r, l))
            minus_points_start.append((l, r))

    # For a crossing [a,b], [l,r] with a < l < b < r:
    # query by end b in (l,r), requiring start a < l.
    ds_pe = DominanceStructure(plus_points_end, n)
    ds_me = DominanceStructure(minus_points_end, n)

    # For a crossing [l,a], [r,b] with l < a < r < b:
    # query by start a in (l,r), requiring end b > r.
    # Convert "end > r" into value < threshold by storing -end.
    plus_points_start2 = [(k, n - v + 1) for k, v in plus_points_start]
    minus_points_start2 = [(k, n - v + 1) for k, v in minus_points_start]
    ds_ps = DominanceStructure(plus_points_start2, n)
    ds_ms = DominanceStructure(minus_points_start2, n)

    max_left_plus = [0] * (n + 1)
    max_left_minus = [0] * (n + 1)
    max_right_plus = [0] * (n + 1)
    max_right_minus = [0] * (n + 1)
    last_pair = {}

    bad = [0] * (m + 1)

    for i, (l, r, sign) in enumerate(people, 1):
        if sign == 0:
            d_end = ds_pe
            d_start = ds_ps
            ml = max_left_plus
            mr = max_right_plus
        else:
            d_end = ds_me
            d_start = ds_ms
            ml = max_left_minus
            mr = max_right_minus

        best = 0

        # Same left endpoint or same right endpoint.
        if ml[l] > best:
            best = ml[l]
        if mr[r] > best:
            best = mr[r]

        # Crossing with prior interval starting earlier.
        v = d_end.query(l + 1, r - 1, l)
        if v > best:
            best = v

        # Crossing with prior interval starting inside current interval
        # and ending later.
        # Stored value is n-end+1; end > r iff value < n-r+1.
        v = d_start.query(l + 1, r - 1, n - r + 1)
        if v > best:
            best = v

        # Same geometric interval with opposite orientation.
        v = last_pair.get((l, r, 1 - sign), 0)
        if v > best:
            best = v

        bad[i] = best

        # Insert current person into structures.
        if sign == 0:
            ds_pe.update(r, l, i)
            ds_ps.update(l, n - r + 1, i)
            if i > max_left_plus[l]:
                max_left_plus[l] = i
            if i > max_right_plus[r]:
                max_right_plus[r] = i
        else:
            ds_me.update(r, l, i)
            ds_ms.update(l, n - r + 1, i)
            if i > max_left_minus[l]:
                max_left_minus[l] = i
            if i > max_right_minus[r]:
                max_right_minus[r] = i

        last_pair[(l, r, sign)] = i

    size = 1
    while size <= m:
        size <<= 1
    seg = [0] * (2 * size)
    for i in range(1, m + 1):
        seg[size + i - 1] = bad[i]
    for p in range(size - 1, 0, -1):
        seg[p] = max(seg[p << 1], seg[p << 1 | 1])

    def range_max(left, right):
        left += size - 1
        right += size - 1
        ans = 0
        while left <= right:
            if left & 1:
                ans = max(ans, seg[left])
                left += 1
            if not (right & 1):
                ans = max(ans, seg[right])
                right -= 1
            left >>= 1
            right >>= 1
        return ans

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        out.append("Yes\n" if range_max(l, r) < l else "No\n")
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()