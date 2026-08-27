import sys
from heapq import heappush, heappop


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    ptr = 0
    N = data[ptr]
    M = data[ptr + 1]
    Q = data[ptr + 2]
    ptr += 3

    l = [0] * M
    r = [0] * M
    plus = []
    minus = []

    for i in range(M):
        S = data[ptr]
        T = data[ptr + 1]
        ptr += 2
        if S < T:
            l[i] = S - 1
            r[i] = T - 1
            plus.append(i)
        else:
            l[i] = T - 1
            r[i] = S - 1
            minus.append(i)

    q_start = ptr

    INF = 10 ** 9
    nxt = [INF] * M

    last_l = [INF] * N
    last_r = [INF] * N
    for i in range(M - 1, -1, -1):
        li = l[i]
        ri = r[i]
        v = last_l[li]
        if v < nxt[i]:
            nxt[i] = v
        v = last_r[ri]
        if v < nxt[i]:
            nxt[i] = v
        last_l[li] = i
        last_r[ri] = i
    del last_l, last_r

    size = 1
    while size < N:
        size <<= 1
    NINF = -10 ** 9

    alive = bytearray([1]) * M

    def process_sign(indices):
        if not indices:
            return

        min_tree = [INF] * (2 * size)
        max_tree = [NINF] * (2 * size)
        min_heaps = [None] * N
        max_heaps = [None] * N

        def pull_min(v, tree=min_tree):
            v >>= 1
            while v:
                left = v << 1
                a = tree[left]
                b = tree[left | 1]
                nv = a if a < b else b
                if tree[v] == nv:
                    break
                tree[v] = nv
                v >>= 1

        def pull_max(v, tree=max_tree):
            v >>= 1
            while v:
                left = v << 1
                a = tree[left]
                b = tree[left | 1]
                nv = a if a > b else b
                if tree[v] == nv:
                    break
                tree[v] = nv
                v >>= 1

        stack = []
        modified = []
        stack_append = stack.append
        stack_pop = stack.pop
        modified_append = modified.append

        l_arr = l
        r_arr = r
        nxt_arr = nxt
        alive_arr = alive
        hp_push = heappush
        hp_pop = heappop
        sz = size
        inf = INF
        ninf = NINF
        m = M

        for j in indices:
            alive_arr[j] = 1
            L = l_arr[j]
            R = r_arr[j]
            ql = L + 1
            qr = R - 1

            if ql <= qr:
                # Case A: previous l_i < L < r_i < R.
                # Segment tree over r_i, storing minimum l_i.
                stack.clear()
                left = ql + sz
                right = qr + sz
                while left <= right:
                    if left & 1:
                        if min_tree[left] < L:
                            stack_append(left)
                        left += 1
                    if not (right & 1):
                        if min_tree[right] < L:
                            stack_append(right)
                        right -= 1
                    left >>= 1
                    right >>= 1

                modified.clear()
                while stack:
                    v = stack_pop()
                    if v >= sz:
                        coord = v - sz
                        h = min_heaps[coord]
                        if h is not None:
                            while h:
                                key = h[0]
                                idx = key % m
                                if not alive_arr[idx]:
                                    hp_pop(h)
                                    continue
                                val = key // m
                                if val < L:
                                    hp_pop(h)
                                    if j < nxt_arr[idx]:
                                        nxt_arr[idx] = j
                                    alive_arr[idx] = 0

                                    # Refresh the other structure at l_i.
                                    coord2 = l_arr[idx]
                                    h2 = max_heaps[coord2]
                                    if h2 is None:
                                        newval2 = ninf
                                    else:
                                        while h2 and not alive_arr[h2[0] % m]:
                                            hp_pop(h2)
                                        newval2 = -(h2[0] // m) if h2 else ninf
                                    p2 = sz + coord2
                                    if max_tree[p2] != newval2:
                                        max_tree[p2] = newval2
                                        pull_max(p2)
                                else:
                                    break
                            newval = h[0] // m if h else inf
                        else:
                            newval = inf

                        if min_tree[v] != newval:
                            min_tree[v] = newval
                            modified_append(v)
                    else:
                        leftc = v << 1
                        rightc = leftc | 1
                        if min_tree[leftc] < L:
                            stack_append(leftc)
                        if min_tree[rightc] < L:
                            stack_append(rightc)

                for v in modified:
                    pull_min(v)

                # Case B: previous L < l_i < R < r_i.
                # Segment tree over l_i, storing maximum r_i.
                stack.clear()
                left = ql + sz
                right = qr + sz
                while left <= right:
                    if left & 1:
                        if max_tree[left] > R:
                            stack_append(left)
                        left += 1
                    if not (right & 1):
                        if max_tree[right] > R:
                            stack_append(right)
                        right -= 1
                    left >>= 1
                    right >>= 1

                modified.clear()
                while stack:
                    v = stack_pop()
                    if v >= sz:
                        coord = v - sz
                        h = max_heaps[coord]
                        if h is not None:
                            while h:
                                key = h[0]
                                idx = key % m
                                if not alive_arr[idx]:
                                    hp_pop(h)
                                    continue
                                rval = -(key // m)
                                if rval > R:
                                    hp_pop(h)
                                    if j < nxt_arr[idx]:
                                        nxt_arr[idx] = j
                                    alive_arr[idx] = 0

                                    # Refresh the other structure at r_i.
                                    coord2 = r_arr[idx]
                                    h2 = min_heaps[coord2]
                                    if h2 is None:
                                        newval2 = inf
                                    else:
                                        while h2 and not alive_arr[h2[0] % m]:
                                            hp_pop(h2)
                                        newval2 = h2[0] // m if h2 else inf
                                    p2 = sz + coord2
                                    if min_tree[p2] != newval2:
                                        min_tree[p2] = newval2
                                        pull_min(p2)
                                else:
                                    break
                            newval = -(h[0] // m) if h else ninf
                        else:
                            newval = ninf

                        if max_tree[v] != newval:
                            max_tree[v] = newval
                            modified_append(v)
                    else:
                        leftc = v << 1
                        rightc = leftc | 1
                        if max_tree[leftc] > R:
                            stack_append(leftc)
                        if max_tree[rightc] > R:
                            stack_append(rightc)

                for v in modified:
                    pull_max(v)

            # Insert current interval into both structures.
            h = min_heaps[R]
            if h is None:
                h = []
                min_heaps[R] = h
            hp_push(h, L * m + j)
            p2 = sz + R
            if L < min_tree[p2]:
                min_tree[p2] = L
                pull_min(p2)

            h = max_heaps[L]
            if h is None:
                h = []
                max_heaps[L] = h
            hp_push(h, -(R * m) + j)
            p2 = sz + L
            if R > max_tree[p2]:
                max_tree[p2] = R
                pull_max(p2)

    process_sign(plus)
    process_sign(minus)

    suf = [INF] * (M + 1)
    for i in range(M - 1, -1, -1):
        v = nxt[i]
        if suf[i + 1] < v:
            v = suf[i + 1]
        suf[i] = v

    out = []
    for k in range(Q):
        L = data[q_start + 2 * k] - 1
        R = data[q_start + 2 * k + 1] - 1
        out.append("Yes" if suf[L] > R else "No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()