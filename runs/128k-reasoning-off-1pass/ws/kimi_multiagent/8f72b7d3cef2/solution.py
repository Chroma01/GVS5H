import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # prefix sums
    P = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        s += A[i]
        P[i] = s

    # Build max-Cartesian tree, leftmost maximum as root (pop strictly on '<'),
    # so equal values form a right-going chain (spine).
    lc = [0] * (n + 1)
    rc = [0] * (n + 1)
    par = [0] * (n + 1)
    stack = []
    for i in range(1, n + 1):
        last = 0
        ai = A[i]
        while stack and A[stack[-1]] < ai:
            last = stack.pop()
        if stack:
            rc[stack[-1]] = i
            par[i] = stack[-1]
        if last:
            lc[i] = last
            par[last] = i
        stack.append(i)
    root = stack[0]

    # Pre-order (root before children); reversed => every node after its descendants.
    order = [root]
    for x in order:
        l = lc[x]
        r = rc[x]
        if l:
            order.append(l)
        if r:
            order.append(r)

    # subtree interval bounds (Cartesian subtree = contiguous interval)
    Lb = [0] * (n + 1)
    Rb = [0] * (n + 1)
    for x in reversed(order):
        l = lc[x]
        r = rc[x]
        Lb[x] = Lb[l] if l else x
        Rb[x] = Rb[r] if r else x

    # components of the laminar family
    comp_sum = [0]   # 1-indexed
    comp_link = [0]  # promotion pointer (component absorbed as members into a bigger root)
    home = [0] * (n + 1)  # home component per array index
    resL = [0] * (n + 1)  # leftmost forest-root component of subtree interval
    resR = [0] * (n + 1)  # rightmost forest-root component

    for x in reversed(order):
        p = par[x]
        if p and rc[p] == x and A[x] == A[p]:
            continue  # non-primary node: handled inside its parent's spine
        M = A[x]
        # walk the equal-value right spine: g_1 = x, g_{i+1} = rc[g_i] while equal
        spine = [x]
        g = x
        while True:
            r = rc[g]
            if r and A[r] == M:
                spine.append(r)
                g = r
            else:
                break
        m = len(spine)
        # segments: S_j = lc[spine[j]] (left of spine[j]); tail S_m = rc[spine[-1]]
        segs = [lc[g] for g in spine]
        tail = rc[spine[-1]]
        any_seg = tail != 0
        if not any_seg:
            for sg in segs:
                if sg:
                    any_seg = True
                    break

        if not any_seg:
            # degenerate: whole interval equals M -> forest of singletons
            first = last_c = 0
            for g in spine:
                comp_sum.append(M)
                comp_link.append(0)
                c = len(comp_sum) - 1
                home[g] = c
                if first == 0:
                    first = c
                last_c = c
            resL[x] = first
            resR[x] = last_c
            continue

        # single root component R = [Lb[x], Rb[x]]
        comp_sum.append(P[Rb[x]] - P[Lb[x] - 1])
        comp_link.append(0)
        R = len(comp_sum) - 1

        # membership of maxima: qualifying iff at least one adjacent segment nonempty
        for j in range(m):
            g = spine[j]
            left_seg = segs[j]                                  # S_j (left of g)
            right_seg = segs[j + 1] if j + 1 < m else tail      # S_{j+1} (right of g)
            if left_seg or right_seg:
                home[g] = R
            else:
                comp_sum.append(M)                              # stuck singleton child
                comp_link.append(0)
                home[g] = len(comp_sum) - 1

        # promotions of touching segment roots (strict >)
        for j in range(m):
            sg = segs[j]
            if sg:
                # S_j lies between spine[j-1] and spine[j]
                if j >= 1:
                    lb = resL[sg]                               # touches spine[j-1]
                    if comp_sum[lb] > M:
                        comp_link[lb] = R
                rb = resR[sg]                                   # touches spine[j]
                if comp_sum[rb] > M:
                    comp_link[rb] = R
        if tail:
            lb = resL[tail]                                     # S_m touches spine[m-1]
            if comp_sum[lb] > M:
                comp_link[lb] = R

        resL[x] = R
        resR[x] = R

    # resolve answers: follow promotion chains with path compression
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        c = home[i]
        path = []
        while comp_link[c]:
            path.append(c)
            c = comp_link[c]
        for c0 in path:
            comp_link[c0] = c
        ans[i] = comp_sum[c]

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

main()