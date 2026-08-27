import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = data[1].decode()
    MOD = 998244353

    # d[i] = (#W - #B) in first i characters, i = 0..2N
    M = 2 * N
    d = [0] * (M + 1)
    for i, ch in enumerate(S, 1):
        d[i] = d[i-1] + (1 if ch == 'W' else -1)

    # sufmin[i] = min over j >= i of d[j]
    sufmin = [0] * (M + 2)
    sufmin[M] = d[M]
    for i in range(M - 1, -1, -1):
        sufmin[i] = d[i] if d[i] < sufmin[i+1] else sufmin[i+1]

    # v-DP with generating functions in the basis x^k/k!:
    # state c[k], F(x) = sum c[k] x^k / k!.
    #   W-step: c[k] -> c[k] + c[k+1], then c[0] = 0
    #   B-step: c[k] -> k*c[k-1] + (k+d)*c[k], then c[0] = 0
    # Answer = c[0] after last step (no zeroing at the end).
    #
    # To make this O(N) total, note the operators applied to the
    # polynomial F.  W: F -> F + F'.  B: F -> (x+d)F + xF'.
    # With G = e^x F:  W: G -> G';  B: G -> xG' + dG.
    # Track G's coefficients g[k]:  W: g[k] -> (k+1) g[k+1];
    # B: g[k] -> (k+d) g[k].  Zeroing F(0)=0 <=> subtract F(0)*e^x
    # from G, i.e. g[k] -= F(0)/k!.  F(0) = G(0) = g[0].
    #
    # We only ever need F(0) at each step (to zero it) and the final
    # F(0).  F(0) = g[0].  But zeroing shifts all g[k] by -g[0]/k!,
    # so we must track the full vector... unless we reorganize.
    #
    # Alternative exact O(N^2)-worst-case but practically fast method:
    # direct v-DP with arrays, v bounded by number of B's so far.
    # Worst case O(N^2) -- too slow for N=2e5 in Python.
    #
    # Instead we use the operator structure to get O(N):
    # Process the string; maintain polynomial G as coefficient list g.
    # W-step: differentiation -> shift left with factor (k+1): O(len)
    # B-step: multiply each g[k] by (k+d): O(len)
    # Zeroing: g[k] -= g[0] * inv_fact[k]: O(len)
    # Each step is O(current degree).  Degree grows by 0 on W (shifts
    # down, degree drops by 1 effectively... actually differentiation
    # lowers degree by 1) and stays on B.  e^x factor makes G infinite,
    # but we can truncate: F has degree <= v_max <= N, and G = e^x F
    # needs coefficients up to degree N to recover F(0)?? No --
    # F(0) = g[0] only.  But the W-step differentiation needs g[1] to
    # update g[0], which needs g[2], etc.  So we need all coefficients
    # up to the max degree that can propagate down to index 0.
    # Max relevant degree = number of W's remaining + current degree.
    # Safest: keep degrees 0..N.  Each step O(N) -> O(N^2).  Too slow.
    #
    # FINAL approach: O(N^2) v-DP is too slow; use the following
    # O(N log N)-style approach is unavailable, so we implement the
    # v-DP with the observation that v <= min(#B so far, #W remaining)
    # and use arrays with running bounds.  For N=2e5 worst case this
    # is still O(N^2) (e.g. B...BW...W).  We accept the operator/EGF
    # method with truncation and prove the needed bound:
    #
    # Claim: after processing i characters, F has degree <= v_max(i)
    # where v_max(i) = number of B's in first i chars (waiting blacks
    # can't exceed blacks seen).  Also coefficients g[k] for k > K_i
    # cannot influence future g[0] where K_i = v_max(i) + (W's left).
    # This still gives O(N^2) worst case.
    #
    # Given the difficulty, we fall back to the exact v-DP implemented
    # with Python lists and tight bounds; this is O(sum_i v_max(i)).
    # For the constraints (N=2e5) this may be too slow in the worst
    # case, but it is the correct algorithm; we optimize with arrays.

    # v-DP, array-based with tight v bounds.
    # f[v] for v in [0..vmax]
    f = [0] * (N + 2)
    f[0] = 1
    vmax = 0
    di = 0  # balance before current character
    for i, ch in enumerate(S, 1):
        if ch == 'B':
            # f'(v) = (v + di) f(v) + f(v-1); v in [0..vmax+1]
            nvmax = vmax + 1
            nf = [0] * (nvmax + 2)
            # match term (stays at v), weight u = v + di
            # defer term: from v-1
            # do it in one pass
            # note di <= 0 possible; u = v+di could be 0 -> term vanishes naturally
            prev = 0  # f[v-1]
            for v in range(0, vmax + 1):
                fv = f[v]
                if fv:
                    u = v + di
                    if u > 0:
                        nf[v] = (nf[v] + fv * u) % MOD
                    nf[v+1] = (nf[v+1] + fv) % MOD
            di -= 1
            vmax = nvmax
        else:
            # f'(v) = f(v) + (v+1) f(v+1); v in [0..vmax]
            nf = [0] * (vmax + 2)
            for v in range(0, vmax + 1):
                fv = f[v]
                if fv:
                    nf[v] = (nf[v] + fv) % MOD
                    nf[v-1] = (nf[v-1] + fv * v) % MOD if v >= 1 else nf[v-1]
            # handle v=0 match term separately (v>=1 required)
            di += 1
            # vmax unchanged (W can't increase waiting blacks)
        # zero out state 0 unless last character
        if i < M:
            nf[0] = 0
        f = nf
    print(f[0] % MOD)

main()