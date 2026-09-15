import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    half = N // 2
    D = N * (N - 1) // 2
    max_extra_bound = D - (N - 1)

    C2 = [i * (i - 1) // 2 for i in range(N + 1)]
    maxC2 = C2[N]

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    maxv = max(N, max_extra_bound) + 1
    invs = [0] * (maxv + 1)
    if maxv >= 1:
        invs[1] = 1
    for i in range(2, maxv + 1):
        invs[i] = (P - (P // i) * invs[P % i] % P) % P

    stride = N + 1

    # Build all structurally possible BFS-layer prefix states.
    # State: (used_vertices, even_count, previous_layer_size, previous_parity)
    start = (1, 1, 1, 0)
    state_to_id = {start: 0}
    states = [start]
    trans = [[]]
    by_used = [[] for _ in range(N + 1)]
    by_used[1].append(0)

    queue = [0]
    head = 0

    def can_finish(u, e, par):
        if e > half or u - e > half:
            return False
        r = N - u
        if r == 0:
            return e == half
        npar = 1 - par
        if npar == 0:
            # Next layer is even: at least one even vertex must be added.
            if e + 1 > half:
                return False
            if e + r < half:
                return False
        else:
            # Next layer is odd: at most r-1 even vertices can be added.
            if e + (r - 1) < half:
                return False
        return True

    while head < len(queue):
        sid = queue[head]
        head += 1
        u, e, p, par = states[sid]
        if u == N:
            continue

        npar = 1 - par
        max_b = N - u
        row_base = p * stride

        if npar == 0:
            for b in range(1, max_b + 1):
                ne = e + b
                if ne > half:
                    break
                nu = u + b
                if not can_finish(nu, ne, npar):
                    continue
                dest = (nu, ne, b, npar)
                did = state_to_id.get(dest)
                if did is None:
                    did = len(states)
                    state_to_id[dest] = did
                    states.append(dest)
                    trans.append([])
                    by_used[nu].append(did)
                    queue.append(did)
                trans[sid].append((did, row_base + b))
        else:
            for b in range(1, max_b + 1):
                nu = u + b
                if nu - e > half:
                    break
                if not can_finish(nu, e, npar):
                    continue
                dest = (nu, e, b, npar)
                did = state_to_id.get(dest)
                if did is None:
                    did = len(states)
                    state_to_id[dest] = did
                    states.append(dest)
                    trans.append([])
                    by_used[nu].append(did)
                    queue.append(did)
                trans[sid].append((did, row_base + b))

    S = len(states)

    # Keep only states that can actually reach a balanced final state.
    good = [False] * S
    for sid in by_used[N]:
        good[sid] = True

    for u in range(N - 1, 0, -1):
        for sid in by_used[u]:
            for dest, _ in trans[sid]:
                if good[dest]:
                    good[sid] = True
                    break

    new_id = [-1] * S
    new_states = []
    new_by_used = [[] for _ in range(N + 1)]
    for sid in range(S):
        if good[sid]:
            nid = len(new_states)
            new_id[sid] = nid
            new_states.append(states[sid])
            new_by_used[states[sid][0]].append(nid)

    new_trans = [[] for _ in range(len(new_states))]
    for sid in range(S):
        nid = new_id[sid]
        if nid != -1:
            for dest, idx in trans[sid]:
                nd = new_id[dest]
                if nd != -1:
                    new_trans[nid].append((nd, idx))

    states = new_states
    S = len(states)
    trans = [tuple(lst) for lst in new_trans]
    by_used = [tuple(lst) for lst in new_by_used]
    final_states = by_used[N]

    del state_to_id, good, new_id, new_trans, new_states, new_by_used, queue

    if not final_states:
        sys.stdout.write(" ".join(["0"] * (max_extra_bound + 1)) + "\n")
        return

    # Maximum possible extra edges among valid layer sequences.
    maxe = [-1] * S
    maxe[0] = 0
    for u in range(1, N):
        for sid in by_used[u]:
            m = maxe[sid]
            if m < 0:
                continue
            p = states[sid][2]
            base = p * stride
            for dest, idx in trans[sid]:
                b = idx - base
                nm = m + b * (p - 1) + C2[b]
                if nm > maxe[dest]:
                    maxe[dest] = nm

    deg = max(maxe[sid] for sid in final_states)
    if deg < 0:
        deg = 0
    if deg > max_extra_bound:
        deg = max_extra_bound

    fac_size = stride * stride

    def build_factor(t, N=N, P=P, stride=stride, invfact=invfact,
                     invs=invs, C2=C2, maxC2=maxC2, fac_size=fac_size):
        fac = [0] * fac_size

        if t == 0:
            pow_e = [1] * (maxC2 + 1)
        else:
            one = (1 + t) % P
            pow_e = [1] * (maxC2 + 1)
            for e in range(1, maxC2 + 1):
                pow_e[e] = pow_e[e - 1] * one % P

        common = [0] * (N + 1)
        for b in range(1, N + 1):
            common[b] = invfact[b] * pow_e[C2[b]] % P

        if t == 0:
            for a in range(1, N + 1):
                base = a
                gp = 1
                row = a * stride
                for b in range(1, N + 1):
                    gp = gp * base % P
                    fac[row + b] = common[b] * gp % P
        else:
            inv_t = invs[t]
            for a in range(1, N + 1):
                g = (pow_e[a] - 1) * inv_t % P
                if g == 0:
                    continue
                gp = 1
                row = a * stride
                for b in range(1, N + 1):
                    gp = gp * g % P
                    fac[row + b] = common[b] * gp % P

        return fac

    used_range = range(1, N)

    def evaluate(fac, S=S, P=P, trans=trans, by_used=by_used,
                 final_states=final_states, used_range=used_range):
        dp = [0] * S
        dp[0] = 1
        Ploc = P
        transloc = trans
        byloc = by_used

        for u in used_range:
            for sid in byloc[u]:
                val = dp[sid]
                if val >= Ploc:
                    val %= Ploc
                if val:
                    for dest, idx in transloc[sid]:
                        dp[dest] += val * fac[idx]

        total = 0
        for sid in final_states:
            total += dp[sid]
        return total % Ploc

    factN1 = fact[N - 1]

    # Evaluate the final polynomial A(x) = (N-1)! * H(x)
    # at x = 0, 1, ..., deg.
    y = []
    for t in range(deg + 1):
        fac = build_factor(t)
        y.append(evaluate(fac) * factN1 % P)

    # Newton interpolation from values at 0..deg to power-basis coefficients.
    diff = y[:]
    coeff = [0] * (deg + 1)
    term = [1]  # binom(x, 0)
    Ploc = P
    invsloc = invs

    for k in range(deg + 1):
        dk = diff[0]
        if dk:
            for j, v in enumerate(term):
                coeff[j] += dk * v

        if k == deg:
            break

        for i in range(deg - k):
            v = diff[i + 1] - diff[i]
            if v < 0:
                v += Ploc
            diff[i] = v

        new = [0] * (k + 2)
        for j, v in enumerate(term):
            new[j] -= k * v
            new[j + 1] += v

        inv = invsloc[k + 1]
        term = [(new[j] * inv) % Ploc for j in range(k + 2)]

    coeff = [c % Ploc for c in coeff]

    ans = []
    for e in range(max_extra_bound + 1):
        if e <= deg:
            ans.append(str(coeff[e]))
        else:
            ans.append("0")

    sys.stdout.write(" ".join(ans) + "\n")


if __name__ == "__main__":
    solve()