import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos+1]); pos += 2
        X = [0]*N; Y = [0]*N; Z = [0]*N
        for i in range(N):
            X[i] = int(data[pos]); Y[i] = int(data[pos+1]); Z[i] = int(data[pos+2])
            pos += 3
        # M_i = max coordinate, g_i = argmax color (ties -> lowest index)
        M = [0]*N; g = [0]*N
        for i in range(N):
            x, y, z = X[i], Y[i], Z[i]
            if x >= y and x >= z:
                M[i] = x; g[i] = 0
            elif y >= z:
                M[i] = y; g[i] = 1
            else:
                M[i] = z; g[i] = 2
        order = sorted(range(N), key=lambda i: -M[i])
        sel = [False]*N
        base = 0
        twoK = 2*K
        for t in range(twoK):
            i = order[t]
            sel[i] = True
            base += M[i]
        cnt = [0, 0, 0]
        for i in range(N):
            if sel[i]:
                cnt[g[i]] += 1
        odd = [c for c in range(3) if cnt[c] & 1]
        if not odd:
            out.append(str(base))
            continue
        p, q = odd
        r = 3 - p - q

        # top-2 structures
        rem2 = [[], [], []]      # per color: (M_i, i) for selected cakes of that argmax color
        rec2 = {}                # (u,v): (M_i - coord_i(v), i) for selected with g_i == u
        add2 = [[], [], []]      # per color v: (coord_j(v), j) for unselected
        for i in range(N):
            if sel[i]:
                u = g[i]; mi = M[i]
                rem2[u].append((mi, i))
                xi, yi, zi = X[i], Y[i], Z[i]
                if u == 0:
                    rec2.setdefault((0,1), []).append((mi - yi, i))
                    rec2.setdefault((0,2), []).append((mi - zi, i))
                elif u == 1:
                    rec2.setdefault((1,0), []).append((mi - xi, i))
                    rec2.setdefault((1,2), []).append((mi - zi, i))
                else:
                    rec2.setdefault((2,0), []).append((mi - xi, i))
                    rec2.setdefault((2,1), []).append((mi - yi, i))
            else:
                add2[0].append((X[i], i))
                add2[1].append((Y[i], i))
                add2[2].append((Z[i], i))
        for c in range(3):
            rem2[c] = heapq.nsmallest(2, rem2[c])
            add2[c] = heapq.nlargest(2, add2[c])
        for key in rec2:
            rec2[key] = heapq.nsmallest(2, rec2[key])

        def edge_moves(u, v):
            # moves flipping parity of colors u and v: (cost, sel_id, unsel_id)
            mv = []
            for cost, i in rec2.get((u, v), ()):
                mv.append((cost, i, -1))
            for cost, i in rec2.get((v, u), ()):
                mv.append((cost, i, -1))
            au = add2[v]; av = add2[u]
            for mi, i in rem2[u]:
                for val, j in au:
                    mv.append((mi - val, i, j))
            for mi, i in rem2[v]:
                for val, j in av:
                    mv.append((mi - val, i, j))
            return mv

        direct = min(m[0] for m in edge_moves(p, q))
        INF = float('inf')
        path = INF
        E1 = edge_moves(p, r)
        E2 = edge_moves(r, q)
        for c1, s1, a1 in E1:
            for c2, s2, a2 in E2:
                if s1 != s2 and (a1 == -1 or a2 == -1 or a1 != a2):
                    tot = c1 + c2
                    if tot < path:
                        path = tot
        out.append(str(base - min(direct, path)))
    sys.stdout.write("\n".join(out) + "\n")

main()