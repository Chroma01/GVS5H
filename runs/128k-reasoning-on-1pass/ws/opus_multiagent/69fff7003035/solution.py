import sys

def main():
    p = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])

    # digit-length classes
    Ds = []
    cs = []
    Ss = []
    for d in range(1, 8):
        lo = 10**(d-1)
        hi = min(N, 10**d - 1)
        if hi < lo:
            continue
        c = hi - lo + 1
        Ds.append(d)
        cs.append(c)
        Ss.append(((lo + hi) * c // 2) % p)
    m = len(Ds)
    A = [pow(10, d, p) for d in Ds]

    # Q(x) = prod (1 + a_d x), degree m
    Q = [1]
    for a in A:
        newQ = [0]*(len(Q)+1)
        for i, qc in enumerate(Q):
            newQ[i] = (newQ[i] + qc) % p
            newQ[i+1] = (newQ[i+1] + qc*a) % p
        Q = newQ
    # R(x) = sum_d c_d a_d prod_{d'!=d} (1 + a_{d'} x), degree m-1
    R = [0]*m
    for t in range(m):
        Pp = [1]
        for s in range(m):
            if s == t:
                continue
            a = A[s]
            newP = [0]*(len(Pp)+1)
            for i, pc in enumerate(Pp):
                newP[i] = (newP[i] + pc) % p
                newP[i+1] = (newP[i+1] + pc*a) % p
            Pp = newP
        coef = (cs[t] % p) * A[t] % p
        for i, pc in enumerate(Pp):
            R[i] = (R[i] + coef*pc) % p

    # modular inverses 1..N
    inv = [0]*(N+2)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N+1):
        inv[i] = (p - (p//i) * inv[p % i]) % p

    # factorials
    fact = [1]*(N+1)
    for i in range(1, N+1):
        fact[i] = fact[i-1]*i % p

    # build F coefficients via ODE recurrence
    # (n+1) f_{n+1} = sum_{j=0}^{m-1} r_j f_{n-j} - sum_{j=1}^{m} q_j (n+1-j) f_{n+1-j}
    fa = [0]*(m + N + 2)
    dfa = [0]*(m + N + 2)
    fa[m] = 1
    dfa[m] = 0

    parts = []
    for j in range(m):
        rj = R[j] % p
        if rj:
            idx = "i" if j == 0 else "i-%d" % j
            parts.append("+%d*fa[%s]" % (rj, idx))
    for j in range(1, m+1):
        qj = Q[j] % p
        if qj:
            k = j-1
            idx = "i" if k == 0 else "i-%d" % k
            parts.append("-%d*dfa[%s]" % (qj, idx))
    expr = "".join(parts) if parts else "0"
    src = ("def build(N,m,fa,dfa,inv,p):\n"
           " for n in range(N):\n"
           "  i=m+n\n"
           "  s=(" + expr + ")%p\n"
           "  dfa[i+1]=s\n"
           "  fa[i+1]=s*inv[n+1]%p\n")
    ns = {}
    exec(src, ns)
    ns['build'](N, m, fa, dfa, inv, p)

    f = fa[m:m+N+1]  # f_0 .. f_N

    # weights w[k] = k! (N-1-k)!
    w = [0]*N
    for k in range(N):
        w[k] = fact[k]*fact[N-1-k] % p

    ftail = f[1:]  # f_1 .. f_N
    ans = 0
    for t in range(m):
        a = A[t]
        g = 1
        tot = 0
        for wk, fk1 in zip(w, ftail):
            tot = (tot + wk*g) % p
            g = (fk1 - a*g) % p
        ans = (ans + Ss[t]*tot) % p

    sys.stdout.write(str(ans % p) + "\n")

main()