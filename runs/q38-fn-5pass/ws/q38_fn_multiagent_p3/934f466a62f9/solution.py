import sys

INF = 10 ** 30
NEG_INF = -10 ** 30


def add_min(lst, item):
    """Keep two smallest (key, id) tuples."""
    if len(lst) < 2:
        lst.append(item)
        if len(lst) == 2 and lst[0][0] > lst[1][0]:
            lst[0], lst[1] = lst[1], lst[0]
    elif item[0] < lst[1][0]:
        lst[1] = item
        if lst[0][0] > lst[1][0]:
            lst[0], lst[1] = lst[1], lst[0]


def add_max(lst, item):
    """Keep two largest (key, id) tuples."""
    if len(lst) < 2:
        lst.append(item)
        if len(lst) == 2 and lst[0][0] < lst[1][0]:
            lst[0], lst[1] = lst[1], lst[0]
    elif item[0] > lst[1][0]:
        lst[1] = item
        if lst[0][0] < lst[1][0]:
            lst[0], lst[1] = lst[1], lst[0]


def combine_min(l1, l2):
    """Minimum sum of two distinct-id items from two top-two lists."""
    best = INF
    for c1, id1 in l1:
        for c2, id2 in l2:
            if id1 != id2:
                s = c1 + c2
                if s < best:
                    best = s
    return best


def combine_max(l1, l2):
    """Maximum sum of two distinct-id items from two top-two lists."""
    best = NEG_INF
    for v1, id1 in l1:
        for v2, id2 in l2:
            if id1 != id2:
                s = v1 + v2
                if s > best:
                    best = s
    return best


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    T = next(it)
    ans = []

    for _ in range(T):
        N = next(it)
        K = next(it)

        X = [0] * N
        Y = [0] * N
        Z = [0] * N
        M = [0] * N
        D = [0] * N

        for i in range(N):
            x = next(it)
            y = next(it)
            z = next(it)
            X[i] = x
            Y[i] = y
            Z[i] = z

            if x >= y and x >= z:
                M[i] = x
                D[i] = 0
            elif y >= z:
                M[i] = y
                D[i] = 1
            else:
                M[i] = z
                D[i] = 2

        order = list(range(N))
        order.sort(key=M.__getitem__, reverse=True)

        need = 2 * K
        selected = order[:need]
        unselected = order[need:]

        base = 0
        mask = 0
        for i in selected:
            base += M[i]
            mask ^= 1 << D[i]

        if mask == 0:
            ans.append(str(base))
            continue

        # recolor_top2[u][v]: selected cakes with default u, recolor to v.
        recolor_top2 = [[[] for _ in range(3)] for __ in range(3)]
        # selected_m_top2[u]: selected cakes with default u, smallest M.
        selected_m_top2 = [[] for _ in range(3)]

        for i in selected:
            d = D[i]
            m = M[i]
            add_min(selected_m_top2[d], (m, i))

            if d != 0:
                add_min(recolor_top2[d][0], (m - X[i], i))
            if d != 1:
                add_min(recolor_top2[d][1], (m - Y[i], i))
            if d != 2:
                add_min(recolor_top2[d][2], (m - Z[i], i))

        # unselected_top2[c]: unselected cakes with largest value in color c.
        unselected_top2 = [[] for _ in range(3)]
        for i in unselected:
            add_max(unselected_top2[0], (X[i], i))
            add_max(unselected_top2[1], (Y[i], i))
            add_max(unselected_top2[2], (Z[i], i))

        def edge_cost(u, v):
            """Minimum loss for one operation toggling colors u and v,
            removing base color u and adding color v.
            """
            best = INF

            # Recolor a selected cake.
            if recolor_top2[u][v]:
                best = recolor_top2[u][v][0][0]

            # Swap a selected cake with an unselected cake.
            if selected_m_top2[u] and unselected_top2[v]:
                cost = selected_m_top2[u][0][0] - unselected_top2[v][0][0]
                if cost < best:
                    best = cost

            return best

        def pair_cost(e, f):
            """Minimum loss for two directed operations e and f,
            using distinct selected cakes and distinct unselected cakes.
            """
            u1, v1 = e
            u2, v2 = f
            best = INF

            # Recolor + Recolor
            val = combine_min(recolor_top2[u1][v1], recolor_top2[u2][v2])
            if val < best:
                best = val

            # Recolor e + Swap f
            if unselected_top2[v2]:
                val = combine_min(recolor_top2[u1][v1], selected_m_top2[u2])
                if val < INF:
                    val -= unselected_top2[v2][0][0]
                    if val < best:
                        best = val

            # Swap e + Recolor f
            if unselected_top2[v1]:
                val = combine_min(recolor_top2[u2][v2], selected_m_top2[u1])
                if val < INF:
                    val -= unselected_top2[v1][0][0]
                    if val < best:
                        best = val

            # Swap + Swap
            if u1 == u2:
                sel = combine_min(selected_m_top2[u1], selected_m_top2[u1])
            else:
                sel = combine_min(selected_m_top2[u1], selected_m_top2[u2])

            if sel < INF:
                un = combine_max(unselected_top2[v1], unselected_top2[v2])
                if un > NEG_INF:
                    val = sel - un
                    if val < best:
                        best = val

            return best

        odd = [i for i in range(3) if (mask >> i) & 1]
        # The number of selected cakes is even, so exactly two colors are odd.
        if len(odd) != 2:
            ans.append(str(base))
            continue

        a, b = odd
        c = 3 - a - b

        loss = edge_cost(a, b)
        tmp = edge_cost(b, a)
        if tmp < loss:
            loss = tmp

        # Two-edge paths through the remaining color c.
        orientations = (
            ((a, c), (b, c)),
            ((a, c), (c, b)),
            ((c, a), (b, c)),
            ((c, a), (c, b)),
        )
        for e, f in orientations:
            val = pair_cost(e, f)
            if val < loss:
                loss = val

        # Safety clamp; mathematically 0 <= loss <= base.
        if loss < 0:
            loss = 0
        if loss > base:
            loss = base

        ans.append(str(base - loss))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()