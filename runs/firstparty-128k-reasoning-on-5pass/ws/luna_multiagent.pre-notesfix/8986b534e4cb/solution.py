import sys
import heapq
from array import array


class ReportTree:
    __slots__ = ("n", "mode", "agg", "heaps", "eligible")

    def __init__(self, n, mode, eligible):
        self.n = n
        self.mode = mode  # 0: minimum a, 1: maximum b
        size = 1
        while size < n:
            size <<= 1
        self.n = size
        inf = n + 1
        if mode == 0:
            self.agg = array("i", [inf]) * (2 * size)
        else:
            self.agg = array("i", [-1]) * (2 * size)
        self.heaps = {}
        self.eligible = eligible

    def _pull(self, p):
        agg = self.agg
        if self.mode == 0:
            v = agg[p << 1]
            if agg[p << 1 | 1] < v:
                v = agg[p << 1 | 1]
        else:
            v = agg[p << 1]
            if agg[p << 1 | 1] > v:
                v = agg[p << 1 | 1]
        agg[p] = v

    def _clean_leaf(self, pos):
        h = self.heaps.get(pos)
        if h is None:
            return
        if self.mode == 0:
            while h and not self.eligible[h[0][1]]:
                heapq.heappop(h)
            value = h[0][0] if h else self.n + 1
        else:
            while h and not self.eligible[h[0][1]]:
                heapq.heappop(h)
            value = -h[0][0] if h else -1

        p = self.n + pos
        self.agg[p] = value
        p >>= 1
        while p:
            self._pull(p)
            p >>= 1

    def insert(self, pos, x, idx):
        h = self.heaps.get(pos)
        if h is None:
            h = []
            self.heaps[pos] = h
        if self.mode == 0:
            heapq.heappush(h, (x, idx))
        else:
            heapq.heappush(h, (-x, idx))

        p = self.n + pos
        if self.mode == 0:
            self.agg[p] = h[0][0]
        else:
            self.agg[p] = -h[0][0]
        p >>= 1
        while p:
            self._pull(p)
            p >>= 1

    def report(self, left, right, threshold):
        if left > right:
            return []
        result = []
        self._report(1, 0, self.n - 1, left, right, threshold, result)
        return result

    def _report(self, p, nl, nr, ql, qr, threshold, result):
        if nr < ql or qr < nl:
            return

        if self.mode == 0:
            if self.agg[p] >= threshold:
                return
        else:
            if self.agg[p] <= threshold:
                return

        if nl == nr:
            self._clean_leaf(nl)
            h = self.heaps.get(nl)
            if h is None:
                return

            if self.mode == 0:
                while h:
                    a, idx = h[0]
                    if not self.eligible[idx]:
                        heapq.heappop(h)
                    elif a < threshold:
                        heapq.heappop(h)
                        self.eligible[idx] = False
                        result.append(idx)
                    else:
                        break
            else:
                while h:
                    neg_b, idx = h[0]
                    b = -neg_b
                    if not self.eligible[idx]:
                        heapq.heappop(h)
                    elif b > threshold:
                        heapq.heappop(h)
                        self.eligible[idx] = False
                        result.append(idx)
                    else:
                        break

            self._clean_leaf(nl)
            return

        mid = (nl + nr) >> 1
        self._report(p << 1, nl, mid, ql, qr, threshold, result)
        self._report(p << 1 | 1, mid + 1, nr, ql, qr, threshold, result)


def main():
    input = sys.stdin.buffer.readline
    n, m, q = map(int, input().split())

    left = [0] * m
    right = [0] * m
    sign = [0] * m

    same_left = [[] for _ in range(n)]
    same_right = [[] for _ in range(n)]

    for i in range(m):
        s, t = map(int, input().split())
        s -= 1
        t -= 1
        if s < t:
            a, b, sg = s, t, 1
        else:
            a, b, sg = t, s, -1

        left[i] = a
        right[i] = b
        sign[i] = sg
        same_left[a].append(i)
        same_right[b].append(i)

    eligible = [False] * m
    next_conflict = [m] * m

    trees = {
        1: (
            ReportTree(n, 0, eligible),  # key: right endpoint, minimum left
            ReportTree(n, 1, eligible),  # key: left endpoint, maximum right
        ),
        -1: (
            ReportTree(n, 0, eligible),
            ReportTree(n, 1, eligible),
        ),
    }

    for j in range(m):
        a = left[j]
        b = right[j]
        sg = sign[j]

        # Intervals with the same left or the same right endpoint conflict.
        for i in same_left[a]:
            if i < j and eligible[i]:
                eligible[i] = False
                next_conflict[i] = j

        for i in same_right[b]:
            if i < j and eligible[i]:
                eligible[i] = False
                next_conflict[i] = j

        # Strict crossings with the same travel direction:
        #
        # A=[x,y], B=[a,b], x<a<y<b
        # and
        # A=[x,y], B=[a,b], a<x<b<y.
        t1, t2 = trees[sg]

        # Prior A with x<a<y<b:
        #     x < a, a < y < b
        found = t1.report(a + 1, b - 1, a)
        for i in found:
            next_conflict[i] = j

        # Prior A with a<x<b<y:
        #     a < x < b, y > b
        found = t2.report(a + 1, b - 1, b)
        for i in found:
            next_conflict[i] = j

        # This interval remains eligible as a future prior interval,
        # even if it already conflicts with an earlier interval.
        eligible[j] = True
        t1.insert(b, a, j)
        t2.insert(a, b, j)

    boundary = [m] * m
    cur = m
    for i in range(m - 1, -1, -1):
        if next_conflict[i] < cur:
            cur = next_conflict[i]
        boundary[i] = cur

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        out.append("Yes" if boundary[l] > r else "No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()