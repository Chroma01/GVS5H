import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    T = data[0]
    idx = 1
    out = []
    INF = 1 << 100

    for _ in range(T):
        N = data[idx]
        K = data[idx + 1]
        idx += 2

        # Enough bits to store counts, and also safe for small N when
        # adding a few change-keys in the baseline evaluation.
        SHIFT = max(N.bit_length(), 4)
        MASK = (1 << SHIFT) - 1

        vals = []
        maxv = 0
        for _ in range(N):
            x = data[idx]
            y = data[idx + 1]
            z = data[idx + 2]
            idx += 3

            # Double all coordinates so that WQS penalties are integral.
            x2 = x << 1
            y2 = y << 1
            z2 = z << 1

            if x2 > maxv:
                maxv = x2
            if y2 > maxv:
                maxv = y2
            if z2 > maxv:
                maxv = z2

            vals.append(x2 << SHIFT)
            vals.append(y2 << SHIFT)
            vals.append(z2 << SHIFT)

        target = K << 1
        L = len(vals)

        def eval_mu(mu, vals=vals, L=L, SHIFT=SHIFT, INF=INF):
            """
            Returns the best encoded code for parity 0 under penalty mu.
            code = (adjusted_doubled_value << SHIFT) + selected_count.
            """
            ms = mu << SHIFT
            base = 0
            parity = 0

            # For each toggle mask 1..7, keep the best 3 change candidates.
            tk = [INF] * 21
            ti = [-1] * 21

            def add(t, key, cid, tk=tk, ti=ti):
                b = (t - 1) * 3
                k2 = tk[b + 2]
                if key < k2:
                    k1 = tk[b + 1]
                    if key < k1:
                        k0 = tk[b]
                        if key < k0:
                            tk[b + 2] = k1
                            ti[b + 2] = ti[b + 1]
                            tk[b + 1] = k0
                            ti[b + 1] = ti[b]
                            tk[b] = key
                            ti[b] = cid
                        else:
                            tk[b + 2] = k1
                            ti[b + 2] = ti[b + 1]
                            tk[b + 1] = key
                            ti[b + 1] = cid
                    else:
                        tk[b + 2] = key
                        ti[b + 2] = cid

            for i in range(0, L, 3):
                cx = vals[i] - ms + 1
                cy = vals[i + 1] - ms + 1
                cz = vals[i + 2] - ms + 1

                # Best independent choice for this cake:
                # skip has code 0, color choices have code (value<<SHIFT)+1.
                best = 0
                bm = 0
                if cx > best:
                    best = cx
                    bm = 1
                if cy > best:
                    best = cy
                    bm = 2
                if cz > best:
                    best = cz
                    bm = 4

                base += best
                parity ^= bm

                # Changes from the chosen best option to every other option.
                # key = best_code - option_code.
                if bm == 0:
                    add(1, -cx, i)
                    add(2, -cy, i)
                    add(4, -cz, i)
                elif bm == 1:
                    add(1, best, i)       # to skip
                    add(3, best - cy, i)  # X -> Y
                    add(5, best - cz, i)  # X -> Z
                elif bm == 2:
                    add(2, best, i)       # to skip
                    add(3, best - cx, i)  # Y -> X
                    add(6, best - cz, i)  # Y -> Z
                else:  # bm == 4
                    add(4, best, i)       # to skip
                    add(5, best - cx, i)  # Z -> X
                    add(6, best - cy, i)  # Z -> Y

            if parity == 0:
                return base

            cands = []
            for t in range(1, 8):
                b = (t - 1) * 3
                k = tk[b]
                if k < INF:
                    cands.append((k, ti[b], t))
                k = tk[b + 1]
                if k < INF:
                    cands.append((k, ti[b + 1], t))
                k = tk[b + 2]
                if k < INF:
                    cands.append((k, ti[b + 2], t))

            best_key = INF
            lc = len(cands)

            # One change.
            for k, cid, t in cands:
                if t == parity and k < best_key:
                    best_key = k

            # Two changes.
            for i in range(lc):
                k1, id1, t1 = cands[i]
                for j in range(i + 1, lc):
                    k2, id2, t2 = cands[j]
                    if id1 != id2 and (t1 ^ t2) == parity:
                        s = k1 + k2
                        if s < best_key:
                            best_key = s

            # Three changes.
            for i in range(lc):
                k1, id1, t1 = cands[i]
                for j in range(i + 1, lc):
                    k2, id2, t2 = cands[j]
                    if id1 == id2:
                        continue
                    need = (t1 ^ t2) ^ parity
                    for l in range(j + 1, lc):
                        k3, id3, t3 = cands[l]
                        if id3 != id1 and id3 != id2 and t3 == need:
                            s = k1 + k2 + k3
                            if s < best_key:
                                best_key = s

            # A feasible fallback is to skip all baseline-selected cakes.
            if best_key == INF or best_key > base:
                best_key = base

            return base - best_key

        lo = 0
        hi = maxv + 1
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            code = eval_mu(mid)
            if (code & MASK) >= target:
                lo = mid
            else:
                hi = mid - 1

        code = eval_mu(lo)
        adjusted_doubled = code >> SHIFT
        ans = (adjusted_doubled + lo * target) // 2
        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()