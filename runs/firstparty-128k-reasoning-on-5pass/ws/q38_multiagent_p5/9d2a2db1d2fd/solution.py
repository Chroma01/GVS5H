import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    H = data[p]
    W = data[p + 1]
    p += 2

    N = H * W
    F = data[p:p + N]
    p += N

    Q = data[p]
    p += 1

    y = [0] * Q
    z = [0] * Q
    bot = [1] * Q
    pend = [None] * N
    rem = 0

    for qi in range(Q):
        a = data[p]
        b = data[p + 1]
        yy = data[p + 2]
        c = data[p + 3]
        d = data[p + 4]
        zz = data[p + 5]
        p += 6

        u = (a - 1) * W + (b - 1)
        v = (c - 1) * W + (d - 1)

        y[qi] = yy
        z[qi] = zz

        if u == v:
            bot[qi] = F[u]
        else:
            rem += 1

            s = pend[u]
            if s is None:
                pend[u] = {qi}
            else:
                s.add(qi)

            s = pend[v]
            if s is None:
                pend[v] = {qi}
            else:
                s.add(qi)

    del data

    if rem:
        m = H * (W - 1) + (H - 1) * W
        edges = [0] * m
        idx = 0

        for i in range(H):
            base = i * W
            end = base + W - 1
            for u in range(base, end):
                v = u + 1
                fu = F[u]
                fv = F[v]
                w = fu if fu < fv else fv
                edges[idx] = (w << 40) | (u << 20) | v
                idx += 1

        for i in range(H - 1):
            base = i * W
            for u in range(base, base + W):
                v = u + W
                fu = F[u]
                fv = F[v]
                w = fu if fu < fv else fv
                edges[idx] = (w << 40) | (u << 20) | v
                idx += 1

        del F

        edges.sort(reverse=True)

        parent = list(range(N))
        sz = [1] * N
        MASK = (1 << 20) - 1

        def find(x, parent=parent):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        pend_local = pend
        bot_local = bot
        sz_local = sz
        find_local = find

        for e in edges:
            w = e >> 40
            u = (e >> 20) & MASK
            v = e & MASK

            ru = find_local(u)
            rv = find_local(v)
            if ru == rv:
                continue

            if sz_local[ru] < sz_local[rv]:
                ru, rv = rv, ru

            set_ru = pend_local[ru]
            set_rv = pend_local[rv]

            if set_ru is None:
                if set_rv:
                    pend_local[ru] = set_rv
            elif set_rv is None:
                if not set_ru:
                    set_ru.clear()
                    pend_local[ru] = None
            else:
                if len(set_ru) <= len(set_rv):
                    small = set_ru
                    large = set_rv
                else:
                    small = set_rv
                    large = set_ru

                if len(small) <= 8:
                    if w == 1:
                        for qid in small:
                            if qid in large:
                                large.remove(qid)
                                rem -= 1
                            else:
                                large.add(qid)
                    else:
                        for qid in small:
                            if qid in large:
                                bot_local[qid] = w
                                large.remove(qid)
                                rem -= 1
                            else:
                                large.add(qid)
                    small.clear()
                else:
                    common = small & large
                    if common:
                        if w != 1:
                            for qid in common:
                                bot_local[qid] = w
                        rem -= len(common)

                        large.difference_update(common)
                        small.difference_update(common)
                        large.update(small)
                        small.clear()
                        common.clear()
                    else:
                        large.update(small)
                        small.clear()

                if large:
                    pend_local[ru] = large
                else:
                    pend_local[ru] = None
                    large.clear()

            parent[rv] = ru
            sz_local[ru] += sz_local[rv]
            pend_local[rv] = None

            if rem == 0:
                break

        del edges, parent, sz, pend_local, pend, find_local, find
    else:
        del F, pend

    out = []
    append = out.append
    y_local = y
    z_local = z
    bot_local = bot

    for qi in range(Q):
        yy = y_local[qi]
        zz = z_local[qi]
        b = bot_local[qi]

        if yy < zz:
            if b >= yy:
                append(str(zz - yy))
            else:
                append(str(yy + zz - 2 * b))
        else:
            if b >= zz:
                append(str(yy - zz))
            else:
                append(str(yy + zz - 2 * b))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()