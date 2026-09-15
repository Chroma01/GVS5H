import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    T = int(data[ptr]); ptr += 1
    out = []

    for _ in range(T):
        N = int(data[ptr]); K = int(data[ptr + 1]); ptr += 2
        X = [0] * N; Y = [0] * N; Z = [0] * N
        W = [0] * N; base = [0] * N
        for i in range(N):
            x = int(data[ptr]); y = int(data[ptr + 1]); z = int(data[ptr + 2]); ptr += 3
            X[i] = x; Y[i] = y; Z[i] = z
            if x >= y and x >= z:
                W[i] = x; base[i] = 0
            elif y >= z:
                W[i] = y; base[i] = 1
            else:
                W[i] = z; base[i] = 2

        M = 2 * K
        order = sorted(range(N), key=lambda i: W[i], reverse=True)

        inT = [False] * N
        G = 0
        cnt = [0, 0, 0]
        for k in range(M):
            i = order[k]
            inT[i] = True
            G += W[i]
            cnt[base[i]] += 1

        if (cnt[0] & 1) == 0 and (cnt[1] & 1) == 0 and (cnt[2] & 1) == 0:
            out.append(str(G))
            continue

        odd = [c for c in range(3) if cnt[c] & 1]
        A, B = odd[0], odd[1]
        C = 3 - A - B
        CO = (X, Y, Z)

        Titems = [[], [], []]
        nont = []
        for i in range(N):
            if inT[i]:
                Titems[base[i]].append(i)
            else:
                nont.append(i)

        cand = 5
        nonT_top = [sorted(nont, key=lambda j, t=t: -CO[t][j])[:cand] for t in range(3)]
        T_rem = [sorted(Titems[c], key=lambda i: W[i])[:cand] for c in range(3)]

        cache = {}

        def op_cands(s, t):
            key = (s, t)
            r = cache.get(key)
            if r is not None:
                return r
            lst = []
            ct = CO[t]
            # recolour a base-s item (kept in selection) to colour t
            for cost, i in sorted((W[i] - ct[i], i) for i in Titems[s])[:cand]:
                lst.append((cost, (i,)))
            # swap: drop a base-s item, add a non-base item coloured t
            for i in T_rem[s]:
                wi = W[i]
                for j in nonT_top[t]:
                    lst.append((wi - ct[j], (i, j)))
            lst.sort(key=lambda p: p[0])
            cache[key] = lst
            return lst

        INF = float('inf')
        best = INF
        # one op with flip set {A,B}
        for (s, t) in ((A, B), (B, A)):
            for cost, _ in op_cands(s, t):
                if cost < best:
                    best = cost

        # two ops with flip sets {A,C} and {B,C} (all four direction pairs)
        combos = (((C, A), (C, B)),
                  ((C, A), (B, C)),
                  ((A, C), (C, B)),
                  ((A, C), (B, C)))
        for (o1, o2) in combos:
            c1 = op_cands(o1[0], o1[1])
            c2 = op_cands(o2[0], o2[1])
            for cost1, u1 in c1:
                if cost1 >= best:
                    break
                s1 = set(u1)
                for cost2, u2 in c2:
                    tot = cost1 + cost2
                    if tot >= best:
                        break
                    if len(s1 | set(u2)) == len(u1) + len(u2):
                        best = tot

        out.append(str(G - best))

    sys.stdout.write('\n'.join(out) + '\n')


main()