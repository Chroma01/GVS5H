import sys
import numpy as np

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); P = int(data[1])
    H = N // 2
    MAXE = N * (N - 1) // 2
    L = MAXE + 1  # max polynomial length

    # factorials and inverse factorials mod P (P > N >= 2, prime)
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % P

    # binomial rows pw[t] = (1+x)^t mod P, as int64 numpy arrays
    pw = [np.array([1], dtype=np.int64)]
    for t in range(1, MAXE + 1):
        prev = pw[t - 1]
        row = np.empty(t + 1, dtype=np.int64)
        row[0] = 1
        row[t] = 1
        if t > 1:
            row[1:t] = (prev[:-1] + prev[1:]) % P
        pw.append(row)

    # f_{a,b}(x) = sum_j (-1)^j C(b,j) (1+x)^{a(b-j)}  (every vertex in current
    # layer has >=1 neighbor in previous layer), for 1 <= a,b <= H
    f = [[None] * (H + 1) for _ in range(H + 1)]
    for a in range(1, H + 1):
        for b in range(1, H + 1):
            poly = np.zeros(a * b + 1, dtype=np.int64)
            cmb = 1  # C(b, j)
            for j in range(0, b + 1):
                if j:
                    cmb = cmb * (b - j + 1) // j
                w = pw[a * (b - j)]
                c = cmb % P
                if j & 1:
                    poly[:len(w)] -= c * w
                else:
                    poly[:len(w)] += c * w
            poly %= P
            f[a][b] = poly

    MASK = (1 << 15) - 1

    # g_{a,s}(x) = inv_fact[s] * f_{a,s}(x) * (1+x)^{C(s,2)} mod P,
    # stored with 15-bit splits for overflow-safe convolution
    g0 = [[None] * (H + 1) for _ in range(H + 1)]
    g1 = [[None] * (H + 1) for _ in range(H + 1)]
    for a in range(1, H + 1):
        for s in range(1, H + 1):
            w = pw[s * (s - 1) // 2]
            fa = f[a][s]
            a0 = fa & MASK; a1 = fa >> 15
            b0 = w & MASK; b1 = w >> 15
            c0 = np.convolve(a0, b0)
            c1 = np.convolve(a0, b1) + np.convolve(a1, b0)
            c2 = np.convolve(a1, b1)
            conv = (c0 % P) + ((c1 % P) << 15) + ((c2 % P) << 30)
            conv %= P
            conv = (conv * inv_fact[s]) % P
            if len(conv) > L:
                conv = conv[:L]
            g0[a][s] = conv & MASK
            g1[a][s] = conv >> 15

    def convolve_mod(arr, a, s):
        # multiply polynomial arr by g_{a,s}, mod P, truncated to length L
        b0 = g0[a][s]; b1 = g1[a][s]
        a0 = arr & MASK
        a1 = arr >> 15
        c0 = np.convolve(a0, b0)
        c1 = np.convolve(a0, b1) + np.convolve(a1, b0)
        c2 = np.convolve(a1, b1)
        res = (c0 % P) + ((c1 % P) << 15) + ((c2 % P) << 30)
        res %= P
        if len(res) > L:
            res = res[:L]
        return res

    # layer DP: state (e, o, a, p) -> polynomial
    # e = sum of even-layer sizes (includes L0 = {1}), o = sum of odd-layer sizes,
    # a = size of last layer, p = parity of last layer
    states = {(1, 0, 1, 0): np.array([1], dtype=np.int64)}
    for v in range(1, N):
        new_states = {}
        for (e, o, a, p), poly in states.items():
            if e + o != v:
                continue
            if p == 0:
                smax = H - o
            else:
                smax = H - e
            for s in range(1, smax + 1):
                c = convolve_mod(poly, a, s)
                if p == 0:
                    key = (e, o + s, s, 1)
                else:
                    key = (e + s, o, s, 0)
                t = new_states.get(key)
                if t is None:
                    new_states[key] = c
                else:
                    if len(t) < len(c):
                        t, c = c, t
                    t[:len(c)] = (t[:len(c)] + c) % P
                    new_states[key] = t
        # carry over states not processed this round
        for k, pv in states.items():
            if k[0] + k[1] != v:
                new_states[k] = pv
        states = new_states

    ans = np.zeros(L, dtype=np.int64)
    for (e, o, a, p), poly in states.items():
        if e == H and o == H:
            ans[:len(poly)] = (ans[:len(poly)] + poly) % P
    ans = (ans * fact[N - 1]) % P

    out = ' '.join(str(int(ans[M])) for M in range(N - 1, MAXE + 1))
    sys.stdout.write(out + '\n')

main()