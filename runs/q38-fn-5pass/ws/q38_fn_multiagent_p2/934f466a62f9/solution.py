import sys
from itertools import combinations_with_replacement

# All possible masks of one state change are 1..6.
# Mask 7 cannot be produced by changing one cake's state.
MASK_COMBOS = [[] for _ in range(8)]
for r in (1, 2, 3):
    for combo in combinations_with_replacement(range(1, 7), r):
        x = 0
        for m in combo:
            x ^= m
        if x:
            MASK_COMBOS[x].append(combo)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    T = next(it)
    out = []
    INF = 10**30
    combos = MASK_COMBOS

    for _ in range(T):
        N = next(it)
        K = next(it)

        xs = [0] * N
        ys = [0] * N
        zs = [0] * N
        maxv = 0

        for i in range(N):
            x = next(it)
            y = next(it)
            z = next(it)
            x2 = x * 2
            y2 = y * 2
            z2 = z * 2
            xs[i] = x2
            ys[i] = y2
            zs[i] = z2
            if x2 > maxv:
                maxv = x2
            if y2 > maxv:
                maxv = y2
            if z2 > maxv:
                maxv = z2

        # Keep top 3 candidates for a mask, sorted by (loss, -delta, idx).
        # nd stores -delta, so smaller nd means larger selected-count gain.
        def add(lst, loss, nd, idx):
            l = len(lst)
            if l == 3:
                last = lst[2]
                if loss > last[0] or (
                    loss == last[0] and (nd > last[1] or (nd == last[1] and idx >= last[2]))
                ):
                    return
                item = (loss, nd, idx)
                if item < lst[0]:
                    lst[2] = lst[1]
                    lst[1] = lst[0]
                    lst[0] = item
                elif item < lst[1]:
                    lst[2] = lst[1]
                    lst[1] = item
                else:
                    lst[2] = item
            elif l == 0:
                lst.append((loss, nd, idx))
            elif l == 1:
                item = (loss, nd, idx)
                if item < lst[0]:
                    lst.insert(0, item)
                else:
                    lst.append(item)
            else:
                item = (loss, nd, idx)
                if item >= lst[1]:
                    lst.append(item)
                elif item < lst[0]:
                    lst.insert(0, item)
                else:
                    lst.insert(1, item)

        def calc(mu):
            base_val = 0
            base_cnt = 0
            base_mask = 0
            top = [[] for _ in range(8)]

            add_local = add
            xs_l = xs
            ys_l = ys
            zs_l = zs
            N_l = N

            for i in range(N_l):
                g0 = xs_l[i] - mu
                g1 = ys_l[i] - mu
                g2 = zs_l[i] - mu

                # Best color gain, with first-color tie-breaking.
                if g0 >= g1:
                    if g0 >= g2:
                        m = g0
                        state = 0
                    else:
                        m = g2
                        state = 2
                else:
                    if g1 >= g2:
                        m = g1
                        state = 1
                    else:
                        m = g2
                        state = 2

                # Tie with unused: prefer selected to maximize count.
                if m >= 0:
                    base_val += m
                    base_cnt += 1
                    bit = 1 << state
                    base_mask ^= bit

                    # selected -> unused
                    add_local(top[bit], m, 1, i)

                    # selected -> another selected color
                    if state == 0:
                        add_local(top[3], m - g1, 0, i)
                        add_local(top[5], m - g2, 0, i)
                    elif state == 1:
                        add_local(top[3], m - g0, 0, i)
                        add_local(top[6], m - g2, 0, i)
                    else:
                        add_local(top[5], m - g0, 0, i)
                        add_local(top[6], m - g1, 0, i)
                else:
                    # unused -> selected color
                    add_local(top[1], -g0, -1, i)
                    add_local(top[2], -g1, -1, i)
                    add_local(top[4], -g2, -1, i)

            if base_mask == 0:
                return base_val, base_cnt // 2

            best_loss = INF
            best_nd = INF

            for combo in combos[base_mask]:
                l = len(combo)

                if l == 1:
                    for a in top[combo[0]]:
                        loss = a[0]
                        nd = a[1]
                        if loss < best_loss or (loss == best_loss and nd < best_nd):
                            best_loss = loss
                            best_nd = nd

                elif l == 2:
                    m1, m2 = combo
                    list1 = top[m1]
                    list2 = top[m2]
                    if not list1 or not list2:
                        continue

                    if m1 == m2:
                        n1 = len(list1)
                        for ai in range(n1):
                            a = list1[ai]
                            for bj in range(ai + 1, n1):
                                b = list1[bj]
                                loss = a[0] + b[0]
                                nd = a[1] + b[1]
                                if loss < best_loss or (loss == best_loss and nd < best_nd):
                                    best_loss = loss
                                    best_nd = nd
                    else:
                        for a in list1:
                            i1 = a[2]
                            la = a[0]
                            na = a[1]
                            for b in list2:
                                if i1 != b[2]:
                                    loss = la + b[0]
                                    nd = na + b[1]
                                    if loss < best_loss or (loss == best_loss and nd < best_nd):
                                        best_loss = loss
                                        best_nd = nd

                else:
                    m1, m2, m3 = combo
                    list1 = top[m1]
                    list2 = top[m2]
                    list3 = top[m3]
                    if not list1 or not list2 or not list3:
                        continue

                    for a in list1:
                        i1 = a[2]
                        la = a[0]
                        na = a[1]
                        for b in list2:
                            if i1 == b[2]:
                                continue
                            i2 = b[2]
                            lab = la + b[0]
                            nab = na + b[1]
                            for c in list3:
                                if c[2] != i1 and c[2] != i2:
                                    loss = lab + c[0]
                                    nd = nab + c[1]
                                    if loss < best_loss or (loss == best_loss and nd < best_nd):
                                        best_loss = loss
                                        best_nd = nd

            # Safety fallback: choose no pairs.
            if best_loss == INF:
                best_loss = base_val
                best_nd = base_cnt

            selected = base_cnt - best_nd
            if selected < 0:
                selected = 0

            return base_val - best_loss, selected // 2

        lo = 0
        hi = maxv + 1

        while hi - lo > 1:
            mid = (lo + hi) // 2
            _, cnt = calc(mid)
            if cnt >= K:
                lo = mid
            else:
                hi = mid

        val, _ = calc(lo)
        ans = (val + 2 * lo * K) // 2
        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()