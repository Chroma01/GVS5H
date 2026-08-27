import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    # ---------- Step 1: directed absorption edges between adjacent slimes ----------
    # Boundary i (between slime i and i+1, 0-indexed):
    #   A[i] > A[i+1] : slime i+1 absorbable from the left  (direction = True)
    #   A[i] < A[i+1] : slime i   absorbable from the right (direction = False)
    #   equal         : no edge (strict inequality never holds across this boundary)
    edges = []
    for i in range(n - 1):
        if A[i] > A[i + 1]:
            edges.append((A[i + 1], i, True))
        elif A[i] < A[i + 1]:
            edges.append((A[i], i, False))
    # Kruskal-like: increasing order of the absorbed slime's value
    edges.sort()

    # ---------- Step 2: build the merge tree ----------
    # Node ids: 0..n-1 leaves, n.. internal nodes (created in merge order).
    # child1 = absorbing side, child2 = absorbed side.
    # sumv = component total; reqL/reqR = threshold M such that an outsider of
    # size S at that boundary can absorb the whole component iff S > M.
    maxnodes = 2 * n
    child1 = [0] * maxnodes
    child2 = [0] * maxnodes
    sumv = [0] * maxnodes
    reqL = [0] * maxnodes
    reqR = [0] * maxnodes
    for i in range(n):
        sumv[i] = A[i]
        reqL[i] = A[i]
        reqR[i] = A[i]

    # DSU parent (path-compressed; ONLY for component rooting during the sweep)
    dsu = list(range(maxnodes))
    # Tree parent links (never compressed; used for answer extraction)
    tree_par = list(range(maxnodes))
    left_end = [0] * maxnodes
    right_end = [0] * maxnodes
    for i in range(n):
        left_end[i] = i
        right_end[i] = i

    def find(x):
        r = x
        while dsu[r] != r:
            r = dsu[r]
        while dsu[x] != r:
            dsu[x], x = r, dsu[x]
        return r

    nxt = n
    for _, i, direction in edges:
        cl = find(i)
        cr = find(i + 1)
        if cl == cr:
            continue
        u = nxt
        nxt += 1
        s = sumv[cl] + sumv[cr]
        sumv[u] = s
        if direction:  # cl (left) absorbs cr (right)
            child1[u] = cl
            child2[u] = cr
            reqL[u] = reqL[cl]
            r = reqR[cl] - sumv[cr]
            reqR[u] = reqR[cr] if reqR[cr] >= r else r
        else:          # cr (right) absorbs cl (left)
            child1[u] = cr
            child2[u] = cl
            reqR[u] = reqR[cr]
            l = reqL[cr] - sumv[cl]
            reqL[u] = reqL[cl] if reqL[cl] >= l else l
        tree_par[cl] = u
        tree_par[cr] = u
        dsu[cl] = u
        dsu[cr] = u
        left_end[u] = left_end[cl]
        right_end[u] = right_end[cr]

    total_nodes = nxt

    # ---------- Step 3a: bottom-up reach[u] ----------
    # reach[u] = max size any seed inside u can have after absorbing ALL of u.
    # A seed reaching the top of u must come from a side that can absorb the
    # other child: absorber side needs reach[c1] > req_facing(c2);
    # absorbed side needs sumv[c2] > req_facing(c1) (it must first absorb all
    # of c2, so it arrives with exactly sumv[c2]).
    reach = [0] * maxnodes
    for i in range(n):
        reach[i] = A[i]
    for u in range(n, total_nodes):
        c1 = child1[u]
        c2 = child2[u]
        # c1 (absorber) and c2 (absorbed): determine facing threshold of c2.
        # c2 lies entirely on one side of c1.
        if left_end[c2] > right_end[c1]:
            need2 = reqL[c2]   # c2 is to the right of c1
        else:
            need2 = reqR[c2]   # c2 is to the left of c1
        if left_end[c1] > right_end[c2]:
            need1 = reqL[c1]
        else:
            need1 = reqR[c1]
        best = 0
        if reach[c1] > need2:
            best = sumv[u]          # some seed in c1 absorbs c2, then all of u
        if sumv[c2] > need1:
            best = sumv[u]          # seed in c2 absorbs c1, then all of u
        if best == 0:
            best = reach[c1]        # nobody completes u; best partial from c1
        reach[u] = best

    # ---------- Step 3b: top-down final[u] ----------
    # final[u] = best achievable answer among seeds whose climb reaches u.
    # Roots: a seed reaching the root ends with the root's full sum.
    final = [0] * maxnodes
    # roots are nodes whose tree_par points to themselves
    for u in range(total_nodes):
        if tree_par[u] == u:
            final[u] = sumv[u]
    # process internal nodes in reverse creation order (parents after children
    # in creation order, so reverse = top-down)
    for u in range(total_nodes - 1, n - 1, -1):
        c1 = child1[u]
        c2 = child2[u]
        if left_end[c2] > right_end[c1]:
            need2 = reqL[c2]
        else:
            need2 = reqR[c2]
        if left_end[c1] > right_end[c2]:
            need1 = reqL[c1]
        else:
            need1 = reqR[c1]
        fu = final[u]
        # absorber side: seeds that can absorb c2 continue upward with fu,
        # otherwise their best is what they achieved inside c1 (reach[c1]).
        if reach[c1] > need2:
            if fu > final[c1]:
                final[c1] = fu
        else:
            if reach[c1] > final[c1]:
                final[c1] = reach[c1]
        # absorbed side: any seed completing c2 arrives with exactly sumv[c2];
        # it continues upward iff sumv[c2] > need1, else stops with sumv[c2].
        if sumv[c2] > need1:
            if fu > final[c2]:
                final[c2] = fu
        else:
            if sumv[c2] > final[c2]:
                final[c2] = sumv[c2]

    ans = [str(final[k]) for k in range(n)]
    sys.stdout.write(' '.join(ans) + '\n')


main()