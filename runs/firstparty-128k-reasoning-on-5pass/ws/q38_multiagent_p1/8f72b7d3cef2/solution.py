import sys
from bisect import bisect_left, bisect_right


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    P = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        s += int(data[i])
        P[i] = s
    del data

    # E[x] = P[x] + A[x] = 2P[x] - P[x-1], for 1 <= x < n
    # D[y] = 2P[y] - P[y+1], for 1 <= y < n
    E = [0] * n
    D = [0] * n
    for i in range(1, n):
        pi = P[i]
        E[i] = pi + pi - P[i - 1]
        D[i] = pi + pi - P[i + 1]

    # R[x] first stores Rmax[x]: largest stable right endpoint y for left x.
    R = [0] * (n + 1)
    R[0] = n
    m = n - 1

    if m:
        order = list(range(1, n))
        order.sort(key=D.__getitem__)
        bit = [0] * (n + 1)
        ptr = 0
        br = bisect_right

        for x in range(1, n):
            px = P[x]

            # Activate all y with D[y] <= P[x].
            while ptr < m:
                y = order[ptr]
                if D[y] > px:
                    break
                # y <= x can never be useful for this or any later x.
                if y > x:
                    i = y
                    # bit[n] is never queried here because U < n in queries.
                    while i < n:
                        if bit[i] >= y:
                            break
                        bit[i] = y
                        i += i & -i
                ptr += 1

            u = br(P, E[x]) - 1
            if u >= n:
                R[x] = n
            elif u > x:
                i = u
                best = 0
                while i:
                    b = bit[i]
                    if b > best:
                        best = b
                        if best == u:
                            break
                    i -= i & -i
                R[x] = best if best > x else -1
            else:
                R[x] = -1

        del bit, D

    # left[k] = X_k = max{x < k | Rmax[x] >= k}
    left = [0] * (n + 1)
    st = []
    append = st.append
    pop = st.pop
    for k in range(1, n + 1):
        append(k - 1)
        while st and R[st[-1]] < k:
            pop()
        left[k] = st[-1]
    del st, append, pop

    # Reuse R as Lmin[y]: smallest stable left endpoint x for right y.
    R[n] = 0

    if m:
        order.sort(key=E.__getitem__, reverse=True)
        INF = n + 1
        bit = [INF] * (n + 1)
        ptr = 0
        bl = bisect_left

        for y in range(n - 1, 0, -1):
            py = P[y]

            # Activate all x with E[x] >= P[y].
            while ptr < m:
                x = order[ptr]
                if E[x] < py:
                    break
                # x >= y can never be useful for this or any later (smaller) y.
                if x < y:
                    rev = n - x + 1
                    i = rev
                    while i <= n:
                        if bit[i] <= x:
                            break
                        bit[i] = x
                        i += i & -i
                ptr += 1

            dy = py + py - P[y + 1]
            if dy <= 0:
                R[y] = 0
            else:
                l = bl(P, dy)
                if l >= y:
                    R[y] = INF
                else:
                    i = n - l + 1
                    best = INF
                    while i:
                        b = bit[i]
                        if b < best:
                            best = b
                            if best == l:
                                break
                        i -= i & -i
                    R[y] = best if best < y else INF

        del order, bit, E

    # Compute answers:
    # Y_k = min{y >= k | Lmin[y] < k}
    # answer[k] = P[Y_k] - P[X_k]
    st = []
    append = st.append
    pop = st.pop
    for k in range(n, 0, -1):
        append(k)
        while st and R[st[-1]] >= k:
            pop()
        y = st[-1]
        left[k] = P[y] - P[left[k]]

    del st, append, pop, P, R

    sys.stdout.write(' '.join(map(str, left[1:])))


if __name__ == '__main__':
    solve()