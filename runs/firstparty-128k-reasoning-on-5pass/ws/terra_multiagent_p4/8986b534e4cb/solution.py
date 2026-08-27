import sys

def solve():
    input = sys.stdin.buffer.readline
    N, M, Q = map(int, input().split())

    left = [0] * M
    right = [0] * M
    sign = [0] * M  # 1: travels right, 0: travels left

    bad = [-1] * M

    last_left = {}
    last_right = {}

    for i in range(M):
        s, t = map(int, input().split())
        if s < t:
            l, r = s, t
            sg = 1
        else:
            l, r = t, s
            sg = 0

        left[i] = l
        right[i] = r
        sign[i] = sg

        p = last_left.get(l)
        if p is not None:
            bad[i] = max(bad[i], p)
        last_left[l] = i

        p = last_right.get(r)
        if p is not None:
            bad[i] = max(bad[i], p)
        last_right[r] = i

    size = 1
    while size <= N:
        size <<= 1

    seg0 = [0] * (size << 1)
    seg1 = [0] * (size << 1)
    touched = []

    def update(pos, val, sg):
        arr = seg1 if sg else seg0
        p = pos + size - 1
        while p:
            if arr[p] == 0:
                touched.append((arr, p))
            if arr[p] < val:
                arr[p] = val
            p >>= 1

    def query(ql, qr, sg):
        if ql > qr:
            return -1
        arr = seg1 if sg else seg0
        l = ql + size - 1
        r = qr + size - 1
        ans = 0
        while l <= r:
            if l & 1:
                if arr[l] > ans:
                    ans = arr[l]
                l += 1
            if not (r & 1):
                if arr[r] > ans:
                    ans = arr[r]
                r -= 1
            l >>= 1
            r >>= 1
        return ans - 1 if ans else -1

    def clear_tree():
        for arr, p in touched:
            arr[p] = 0
        touched.clear()

    sys.setrecursionlimit(1 << 20)

    def cdq(lo, hi):
        if hi - lo <= 1:
            return

        mid = (lo + hi) >> 1
        cdq(lo, mid)
        cdq(mid, hi)

        li = list(range(lo, mid))
        ri = list(range(mid, hi))

        # Crossing type:
        # left[i] < left[j] < right[i] < right[j]
        # Need equal directions.
        li.sort(key=lambda x: left[x])
        ri.sort(key=lambda x: left[x])

        p = 0
        for j in ri:
            lj = left[j]
            while p < len(li) and left[li[p]] < lj:
                i = li[p]
                update(right[i], i + 1, sign[i])
                p += 1
            v = query(lj + 1, right[j] - 1, sign[j])
            if v > bad[j]:
                bad[j] = v
        clear_tree()

        # Crossing type:
        # left[j] < left[i] < right[j] < right[i]
        # Process decreasing right endpoints.
        li.sort(key=lambda x: right[x], reverse=True)
        ri.sort(key=lambda x: right[x], reverse=True)

        p = 0
        for j in ri:
            rj = right[j]
            while p < len(li) and right[li[p]] > rj:
                i = li[p]
                update(left[i], i + 1, sign[i])
                p += 1
            v = query(left[j] + 1, rj - 1, sign[j])
            if v > bad[j]:
                bad[j] = v
        clear_tree()

    cdq(0, M)

    rmq_size = 1
    while rmq_size < M:
        rmq_size <<= 1
    rmq = [-1] * (rmq_size << 1)
    for i, x in enumerate(bad):
        rmq[rmq_size + i] = x
    for i in range(rmq_size - 1, 0, -1):
        a = rmq[i << 1]
        b = rmq[i << 1 | 1]
        rmq[i] = a if a >= b else b

    out = []
    for _ in range(Q):
        L, R = map(int, input().split())
        l = L - 1
        r = R

        a = l + rmq_size
        b = r + rmq_size
        mx = -1
        while a < b:
            if a & 1:
                if rmq[a] > mx:
                    mx = rmq[a]
                a += 1
            if b & 1:
                b -= 1
                if rmq[b] > mx:
                    mx = rmq[b]
            a >>= 1
            b >>= 1

        out.append("Yes" if mx < l else "No")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()