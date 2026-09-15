import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    T = data[idx]
    idx += 1

    out = []
    TOP = 5
    INF = 10**30
    BIT = (1, 2, 4)
    CHANGES = (3, 5, 6)  # (0,1), (0,2), (1,2)

    for _ in range(T):
        N = data[idx]
        K = data[idx + 1]
        idx += 2

        vals = [None] * N
        M = [0] * N

        for i in range(N):
            x = data[idx]
            y = data[idx + 1]
            z = data[idx + 2]
            idx += 3
            vals[i] = (x, y, z)
            M[i] = max(x, y, z)

        need = 2 * K
        order = sorted(range(N), key=M.__getitem__, reverse=True)
        selected = order[:need]
        unselected = order[need:]

        base = [0] * N
        total = 0
        mask = 0

        for i in selected:
            m = M[i]
            total += m
            x, y, z = vals[i]
            if x == m:
                b = 0
            elif y == m:
                b = 1
            else:
                b = 2
            base[i] = b
            mask ^= BIT[b]

        if mask == 0:
            out.append(str(total))
            continue

        defect = mask

        # Selected cakes with smallest M for each base color (best removals for swaps).
        selM = [[] for _ in range(3)]
        for i in reversed(selected):
            b = base[i]
            if len(selM[b]) < TOP:
                selM[b].append(i)

        # Selected cakes with smallest recolor loss for each ordered color pair.
        rec_lists = [[[] for _ in range(3)] for __ in range(3)]
        for i in selected:
            a = base[i]
            mi = M[i]
            vi = vals[i]
            for b in range(3):
                if b != a:
                    rec_lists[a][b].append((mi - vi[b], i))

        # Unselected cakes with largest value for each target color (best additions for swaps).
        add_lists = [[] for _ in range(3)]
        for i in unselected:
            vi = vals[i]
            for b in range(3):
                add_lists[b].append((vi[b], i))

        op_dict = {}

        # Recolor operations: selected base color a -> target color b.
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                lst = rec_lists[a][b]
                if not lst:
                    continue
                lst.sort()
                if len(lst) > TOP:
                    lst = lst[:TOP]

                change = BIT[a] ^ BIT[b]
                for loss, i in lst:
                    key = (change, i, -1)
                    if loss < op_dict.get(key, INF):
                        op_dict[key] = loss

        add_cand = []
        for b in range(3):
            lst = add_lists[b]
            if not lst:
                add_cand.append([])
                continue
            lst.sort(reverse=True)
            if len(lst) > TOP:
                lst = lst[:TOP]
            add_cand.append([i for _, i in lst])

        # Swap operations: remove selected base color a, add unselected cake with target color b.
        for a in range(3):
            if not selM[a]:
                continue
            for b in range(3):
                if a == b or not add_cand[b]:
                    continue
                change = BIT[a] ^ BIT[b]
                for i in selM[a]:
                    mi = M[i]
                    for j in add_cand[b]:
                        loss = mi - vals[j][b]
                        key = (change, i, j)
                        if loss < op_dict.get(key, INF):
                            op_dict[key] = loss

        groups = {3: [], 5: [], 6: []}
        for (change, s, add), loss in op_dict.items():
            if change in groups:
                groups[change].append((s, add, loss))

        min_loss = INF

        # One operation whose parity change is exactly the defect.
        for s, add, loss in groups.get(defect, []):
            if loss < min_loss:
                min_loss = loss

        # Two operations whose changes are the other two non-zero masks.
        if defect in CHANGES:
            others = [c for c in CHANGES if c != defect]
            list1 = groups[others[0]]
            list2 = groups[others[1]]
            list1.sort(key=lambda x: x[2])
            list2.sort(key=lambda x: x[2])

            for s1, add1, l1 in list1:
                if l1 >= min_loss:
                    break
                for s2, add2, l2 in list2:
                    nl = l1 + l2
                    if nl >= min_loss:
                        break
                    if s1 == s2:
                        continue
                    if add1 != -1 and add2 != -1 and add1 == add2:
                        continue
                    min_loss = nl

        # Safety fallback: a single recolor between the two odd colors is always valid.
        if min_loss == INF:
            cols = [c for c in range(3) if (defect >> c) & 1]
            if len(cols) == 2:
                a, b = cols
                for i in selected:
                    if base[i] == a:
                        loss = M[i] - vals[i][b]
                        if loss < min_loss:
                            min_loss = loss
                    elif base[i] == b:
                        loss = M[i] - vals[i][a]
                        if loss < min_loss:
                            min_loss = loss
            if min_loss == INF:
                min_loss = 0

        out.append(str(total - min_loss))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()