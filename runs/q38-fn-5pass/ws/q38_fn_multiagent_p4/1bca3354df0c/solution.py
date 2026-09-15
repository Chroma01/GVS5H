import sys
import gc

# Types:
# 0: I  isolated vertex
# 1: O  non-isolated component of odd total size
# 2: Q  even total size, both bipartition sides odd
# 3: E  even total size, both bipartition sides even


def compute_dp(B):
    """
    Compute the truncated Sprague-Grundy class (0, 1, or 2) of the merge-only
    game for all states with total number of components <= B.
    """
    base = B + 1
    si = base * base * base
    so = base * base
    sq = base

    arr = bytearray(base ** 4)

    # value mask for child class c and delta d:
    # bit 0 set if option value 0 exists, bit 1 set if option value 1 exists
    vm0 = (1, 2, 0)  # delta 0: class 0 -> 0, class 1 -> 1, class 2 -> none
    vm1 = (2, 1, 0)  # delta 1: class 0 -> 1, class 1 -> 0, class 2 -> none

    # Index deltas for each legal merge.
    # I I -> Q, delta 0
    d00 = -2 * si + sq

    # I O -> E delta 1, or Q delta 0
    d01E = -si - so + 1
    d01Q = -si - so + sq

    # I Q -> O, delta 0
    d02 = -si - sq + so

    # I E -> O, delta 1
    d03 = -si - 1 + so

    # O O -> E delta 1, or Q delta 0
    d11E = -2 * so + 1
    d11Q = -2 * so + sq

    # O Q -> O, delta 0
    d12 = -sq

    # O E -> O, delta 1
    d13 = -1

    # Q Q -> E, delta 1
    d22 = -2 * sq + 1

    # Q E -> Q, delta 1
    d23 = -1

    # E E -> E, delta 1
    d33 = -1

    for total in range(1, B + 1):
        imax = total if total < base else B
        for i in range(imax + 1):
            rem1 = total - i
            omax = rem1 if rem1 < base else B
            bi = i * si
            for o in range(omax + 1):
                rem2 = rem1 - o
                qmax = rem2 if rem2 < base else B
                bio = bi + o * so
                for q in range(qmax + 1):
                    e = rem2 - q
                    idx = bio + q * sq + e
                    mask = 0

                    if i >= 2:
                        mask |= vm0[arr[idx + d00]]

                    if mask != 3 and i >= 1 and o >= 1:
                        mask |= vm1[arr[idx + d01E]]
                        if mask != 3:
                            mask |= vm0[arr[idx + d01Q]]

                    if mask != 3 and i >= 1 and q >= 1:
                        mask |= vm0[arr[idx + d02]]

                    if mask != 3 and i >= 1 and e >= 1:
                        mask |= vm1[arr[idx + d03]]

                    if mask != 3 and o >= 2:
                        mask |= vm1[arr[idx + d11E]]
                        if mask != 3:
                            mask |= vm0[arr[idx + d11Q]]

                    if mask != 3 and o >= 1 and q >= 1:
                        mask |= vm0[arr[idx + d12]]

                    if mask != 3 and o >= 1 and e >= 1:
                        mask |= vm1[arr[idx + d13]]

                    if mask != 3 and q >= 2:
                        mask |= vm1[arr[idx + d22]]

                    if mask != 3 and q >= 1 and e >= 1:
                        mask |= vm1[arr[idx + d23]]

                    if mask != 3 and e >= 2:
                        mask |= vm1[arr[idx + d33]]

                    if mask == 3:
                        arr[idx] = 2
                    elif mask & 1:
                        arr[idx] = 1
                    else:
                        arr[idx] = 0

    return arr, base


def verify_period(arr, B, P, T):
    """
    Finite verification of period P from threshold T:
    checks g(..., x, ...) == g(..., x-P, ...) for every coordinate x in [T, B].
    """
    base = B + 1
    si = base * base * base
    so = base * base
    sq = base

    for total in range(B + 1):
        for i in range(total + 1):
            rem1 = total - i
            for o in range(rem1 + 1):
                rem2 = rem1 - o
                for q in range(rem2 + 1):
                    e = rem2 - q
                    idx = i * si + o * so + q * sq + e

                    if i >= T:
                        if arr[idx] != arr[idx - P * si]:
                            return False
                    if o >= T:
                        if arr[idx] != arr[idx - P * so]:
                            return False
                    if q >= T:
                        if arr[idx] != arr[idx - P * sq]:
                            return False
                    if e >= T:
                        if arr[idx] != arr[idx - P]:
                            return False
    return True


_TABLE_CACHE = None


def get_table():
    global _TABLE_CACHE
    if _TABLE_CACHE is not None:
        return _TABLE_CACHE

    # (B, candidates).  A candidate (P, T) is usable only if the capped window
    # [T, T+P-1]^4 has total size at most B, so the DP contains all capped states.
    configs = [
        (80, [(4, 16), (8, 12), (2, 16), (1, 16)]),
        (96, [(4, 20), (8, 16), (2, 20), (1, 20)]),
    ]

    for cfg_idx, (B, cands) in enumerate(configs):
        arr, base = compute_dp(B)

        for P, T in cands:
            C = T + P - 1
            if C <= B and 4 * C <= B and verify_period(arr, B, P, T):
                _TABLE_CACHE = (arr, base, P, T, B)
                return _TABLE_CACHE

        if cfg_idx == len(configs) - 1:
            # Last-resort fallback.  In practice the verified branch above is used.
            _TABLE_CACHE = (arr, base, 8, 16, B)
            return _TABLE_CACHE

        del arr
        gc.collect()

    # Should never reach here.
    arr, base = compute_dp(80)
    _TABLE_CACHE = (arr, base, 8, 12, 80)
    return _TABLE_CACHE


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    # If N is odd, every terminal complete bipartite graph has an even number
    # of edges, so the whole game length parity is exactly M mod 2.
    if N & 1:
        print("Aoki" if (M & 1) else "Takahashi")
        return

    cnt = [0, 0, 0, 0]  # I, O, Q, E
    prod_parity = 0

    if M == 0:
        cnt[0] = N
        del data
    else:
        adj = [[] for _ in range(N)]
        pos = 2
        for _ in range(M):
            u = int(data[pos]) - 1
            v = int(data[pos + 1]) - 1
            pos += 2
            adj[u].append(v)
            adj[v].append(u)
        del data

        color = [-1] * N

        for s in range(N):
            if color[s] != -1:
                continue

            color[s] = 0
            stack = [s]
            c0 = 1
            c1 = 0

            while stack:
                v = stack.pop()
                cv = color[v]
                nv = cv ^ 1
                for to in adj[v]:
                    if color[to] == -1:
                        color[to] = nv
                        if nv == 0:
                            c0 += 1
                        else:
                            c1 += 1
                        stack.append(to)

            size = c0 + c1
            if size == 1:
                typ = 0
            elif size & 1:
                typ = 1
            else:
                if (c0 & 1) and (c1 & 1):
                    typ = 2
                else:
                    typ = 3

            cnt[typ] += 1
            prod_parity ^= (c0 & 1) & (c1 & 1)

        del adj, color
        gc.collect()

    # K = total currently missing allowed internal edges.
    # K mod 2 = sum(a_i*b_i) - M = (#Q mod 2) xor (M mod 2).
    kpar = (prod_parity ^ (M & 1)) & 1

    i, o, q, e = cnt
    total_comp = i + o + q + e

    # Safe fast paths.
    if total_comp == 1:
        cls = 0
    elif i == 0:
        # Closed form for states with no isolated vertices:
        # class = 0 if o == 0, 2 if o == 2, otherwise q parity.
        if o == 0:
            cls = 0
        elif o == 2:
            cls = 2
        else:
            cls = q & 1
    else:
        arr, base, P, T, B = get_table()

        if total_comp <= B:
            ci, co, cq, ce = i, o, q, e
        else:
            def cap(x):
                if x < T:
                    return x
                return T + ((x - T) % P)

            ci = cap(i)
            co = cap(o)
            cq = cap(q)
            ce = cap(e)

        idx = ci * (base * base * base) + co * (base * base) + cq * base + ce
        cls = arr[idx]

    if cls == 0:
        win = (kpar == 1)
    elif cls == 1:
        win = (kpar == 0)
    else:
        win = True

    print("Aoki" if win else "Takahashi")


if __name__ == "__main__":
    main()