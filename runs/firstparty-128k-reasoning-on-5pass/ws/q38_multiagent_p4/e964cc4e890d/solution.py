import sys
import random
from itertools import combinations, permutations

MOD = 998244353
G = 3

fact = [1]
invfact = [1]

NTT_MAX = 0
PW_FWD = None
PW_INV = None
INV_LEN = None


def ensure_fact(n):
    cur = len(fact) - 1
    if n <= cur:
        return
    fact.extend([1] * (n - cur))
    for i in range(cur + 1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact.extend([1] * (n - cur))
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, cur, -1):
        invfact[i - 1] = invfact[i] * i % MOD


def ensure_ntt(max_n):
    global NTT_MAX, PW_FWD, PW_INV, INV_LEN
    if max_n <= NTT_MAX:
        return

    max_log = max_n.bit_length() - 1
    PW_FWD = [None] * (max_log + 1)
    PW_INV = [None] * (max_log + 1)
    INV_LEN = [1] * (max_log + 1)

    inv2 = (MOD + 1) // 2
    for k in range(1, max_log + 1):
        length = 1 << k
        wlen = pow(G, (MOD - 1) // length, MOD)
        wlen_inv = pow(wlen, MOD - 2, MOD)
        half = length >> 1

        arr = [1] * half
        arr_inv = [1] * half
        for i in range(1, half):
            arr[i] = arr[i - 1] * wlen % MOD
            arr_inv[i] = arr_inv[i - 1] * wlen_inv % MOD

        PW_FWD[k] = arr
        PW_INV[k] = arr_inv
        INV_LEN[k] = INV_LEN[k - 1] * inv2 % MOD

    NTT_MAX = max_n


def ntt(a):
    pw_fwd = PW_FWD
    mod = MOD
    n = len(a)
    length = n
    k = n.bit_length() - 1

    while length > 1:
        half = length >> 1
        pw = pw_fwd[k]
        for start in range(0, n, length):
            i = start
            j = start + half
            for w in pw:
                u = a[i]
                v = a[j]
                x = u + v
                if x >= mod:
                    x -= mod
                y = u - v
                if y < 0:
                    y += mod
                a[i] = x
                a[j] = y * w % mod
                i += 1
                j += 1
        length >>= 1
        k -= 1


def intt(a):
    pw_inv = PW_INV
    inv_len = INV_LEN
    mod = MOD
    n = len(a)
    length = 2
    k = 1

    while length <= n:
        half = length >> 1
        pw = pw_inv[k]
        for start in range(0, n, length):
            i = start
            j = start + half
            for w in pw:
                u = a[i]
                v = a[j] * w % mod
                x = u + v
                if x >= mod:
                    x -= mod
                y = u - v
                if y < 0:
                    y += mod
                a[i] = x
                a[j] = y
                i += 1
                j += 1
        length <<= 1
        k += 1

    inv_n = inv_len[n.bit_length() - 1]
    for i in range(n):
        a[i] = a[i] * inv_n % mod


def convolve(a, b):
    n = len(a) + len(b) - 1
    if n <= 0:
        return []
    size = 1 << (n - 1).bit_length()
    ensure_ntt(size)

    fa = a[:] + [0] * (size - len(a))
    fb = b[:] + [0] * (size - len(b))

    ntt(fa)
    ntt(fb)

    mod = MOD
    for i in range(size):
        fa[i] = fa[i] * fb[i] % mod

    intt(fa)
    return fa[:n]


def compute_T(N, S):
    # T[i] for i = 0..N-2 is the number of Ws before the (i+2)-th B.
    T = [0] * (N - 1)
    w = 0
    b = 0
    for ch in S:
        if ch == 'W':
            w += 1
        else:
            b += 1
            c = b - 1
            if 1 <= c <= N - 1:
                T[c - 1] = w
    return T


def cdq_count(N, S):
    if N == 0:
        return 1
    if S[0] == 'W' or S[-1] == 'B':
        return 0

    ensure_fact(N)
    M = N - 1
    if M == 0:
        return fact[N]

    T = compute_T(N, S)
    B = [0] * M
    add = [0] * M

    BLOCK = 32
    DIRECT_M = 32
    DIRECT_R = 32
    DIRECT_PROD = 16384

    mod = MOD
    fact_l = fact
    invfact_l = invfact
    T_l = T
    B_l = B
    add_l = add

    def solve(l, r):
        if r - l <= BLOCK:
            for i in range(l, r):
                c = i + 1
                t = T_l[i]
                if t >= c:
                    s = fact_l[t] + add_l[i]
                    maxj = i - 1
                    if maxj > t - 1:
                        maxj = t - 1
                    if maxj >= l:
                        for j in range(l, maxj + 1):
                            bj = B_l[j]
                            if bj:
                                s += bj * fact_l[t - j - 1]
                    s %= mod
                    B_l[i] = (-invfact_l[t - c] * s) % mod
                else:
                    B_l[i] = 0
            return

        mid = (l + r) >> 1
        solve(l, mid)

        m = mid - l
        t0 = T_l[mid]
        t1 = T_l[r - 1]
        R = t1 - t0

        if R >= 0 and t1 >= l + 1:
            if m <= DIRECT_M or R <= DIRECT_R or m * (R + 1) <= DIRECT_PROD:
                # Direct contribution from left half to right half.
                for p in range(m):
                    val = B_l[l + p]
                    if val == 0:
                        continue

                    start = t0 - l - p - 1
                    if start < 0:
                        j0 = -start
                        if j0 > R:
                            continue
                        start_idx = 0
                        pos = mid + j0
                    else:
                        start_idx = start
                        pos = mid

                    end = mid + R + 1
                    count = end - pos

                    if val == 1:
                        for idx in range(start_idx, start_idx + count):
                            x = add_l[pos] + fact_l[idx]
                            if x >= mod:
                                x -= mod
                            add_l[pos] = x
                            pos += 1
                    else:
                        for idx in range(start_idx, start_idx + count):
                            prod = val * fact_l[idx] % mod
                            x = add_l[pos] + prod
                            if x >= mod:
                                x -= mod
                            add_l[pos] = x
                            pos += 1
            else:
                # NTT contribution.
                nonzero = False
                for i in range(l, mid):
                    if B_l[i]:
                        nonzero = True
                        break

                if nonzero:
                    need = R + 2 * m - 1
                    size = 1 << (need - 1).bit_length()
                    ensure_ntt(size)

                    fa = [0] * size
                    fa[:m] = B_l[l:mid]

                    lenF = R + m
                    fb = [0] * size
                    start = t0 - mid

                    if start < 0:
                        z = -start
                        if z < lenF:
                            fb[z:lenF] = fact_l[:lenF - z]
                    else:
                        seg = fact_l[start:start + lenF]
                        if len(seg) < lenF:
                            seg += [0] * (lenF - len(seg))
                        fb[:lenF] = seg

                    ntt(fa)
                    ntt(fb)

                    for i in range(size):
                        fa[i] = fa[i] * fb[i] % mod
                    del fb

                    intt(fa)

                    base = m - 1
                    for j in range(R + 1):
                        v = fa[base + j]
                        if v:
                            x = add_l[mid + j] + v
                            if x >= mod:
                                x -= mod
                            add_l[mid + j] = x

        solve(mid, r)

    solve(0, M)

    ans = fact_l[N]
    for i in range(M):
        b = B_l[i]
        if b:
            ans = (ans + b * fact_l[N - i - 1]) % mod
    return ans


def recurrence_count(N, S):
    if N == 0:
        return 1
    if S[0] == 'W' or S[-1] == 'B':
        return 0

    ensure_fact(N)
    T = compute_T(N, S)
    B = [0] * N
    active = []

    for c in range(1, N):
        t = T[c - 1]
        if t < c:
            continue
        s = fact[t]
        for d in active:
            s += B[d] * fact[t - d]
        B[c] = (-invfact[t - c] * (s % MOD)) % MOD
        active.append(c)

    ans = fact[N]
    for c in active:
        ans = (ans + B[c] * fact[N - c]) % MOD
    return ans


def brute_count(N, S, shortcut=True):
    if shortcut and (S[0] == 'W' or S[-1] == 'B'):
        return 0

    cut_c = []
    cut_t = []
    c = 0
    t = 0
    for ch in S[:-1]:
        if ch == 'B':
            c += 1
        else:
            t += 1
        cut_c.append(c)
        cut_t.append(t)

    m = len(cut_c)
    cnt = 0

    for p in permutations(range(N)):
        idx = 0
        mx = -1
        for i in range(m):
            target = cut_c[i]
            while idx < target:
                v = p[idx]
                if v > mx:
                    mx = v
                idx += 1
            if mx < cut_t[i]:
                break
        else:
            cnt += 1
    return cnt


def all_balanced_strings(N):
    L = 2 * N
    for wpos in combinations(range(L), N):
        arr = ['B'] * L
        for i in wpos:
            arr[i] = 'W'
        yield ''.join(arr)


def random_balanced_string(N, rng, force_good=False):
    if force_good:
        arr = ['B'] * (2 * N)
        arr[0] = 'B'
        arr[-1] = 'W'
        mid = ['W'] * (N - 1) + ['B'] * (N - 1)
        rng.shuffle(mid)
        arr[1:-1] = mid
        return ''.join(arr)

    arr = ['W'] * N + ['B'] * N
    rng.shuffle(arr)
    return ''.join(arr)


def run_self_tests():
    # NTT sanity check.
    rng = random.Random(0)
    for _ in range(20):
        n1 = rng.randint(1, 20)
        n2 = rng.randint(1, 20)
        a = [rng.randrange(MOD) for _ in range(n1)]
        b = [rng.randrange(MOD) for _ in range(n2)]
        c = convolve(a, b)
        d = [0] * (n1 + n2 - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    d[i + j] = (d[i + j] + x * y) % MOD
        if c != d:
            raise AssertionError("NTT convolution mismatch")

    # Exhaustive small validation.
    for N in range(1, 6):
        for S in all_balanced_strings(N):
            br = brute_count(N, S, shortcut=False)
            rec = recurrence_count(N, S)
            cdq = cdq_count(N, S)
            if br != rec or br != cdq:
                raise AssertionError(f"mismatch N={N} S={S} brute={br} rec={rec} cdq={cdq}")

    # Random validation against the O(N^2) recurrence.
    rng = random.Random(123456789)
    for N in range(6, 11):
        for _ in range(8):
            S = random_balanced_string(N, rng, force_good=True)
            rec = recurrence_count(N, S)
            cdq = cdq_count(N, S)
            if rec != cdq:
                raise AssertionError(f"mismatch N={N} S={S} rec={rec} cdq={cdq}")
            if N <= 7:
                br = brute_count(N, S, shortcut=True)
                if br != rec:
                    raise AssertionError(f"brute mismatch N={N} S={S}")

        for _ in range(4):
            S = random_balanced_string(N, rng, force_good=False)
            rec = recurrence_count(N, S)
            cdq = cdq_count(N, S)
            if rec != cdq:
                raise AssertionError(f"mismatch N={N} S={S} rec={rec} cdq={cdq}")

    # Larger random checks to exercise the NTT path.
    for _ in range(3):
        N = 1000
        S = random_balanced_string(N, rng, force_good=True)
        rec = recurrence_count(N, S)
        cdq = cdq_count(N, S)
        if rec != cdq:
            raise AssertionError(f"large random mismatch N={N} S={S}")

    # Samples.
    assert cdq_count(2, "BWBW") == 1
    assert recurrence_count(2, "BWBW") == 1
    assert cdq_count(4, "BWWBWBWB") == 0
    assert cdq_count(9, "BWWBWBBBWWBWBBWWBW") == 240792


def main():
    sys.setrecursionlimit(1_000_000)
    data = sys.stdin.read().split()
    if not data:
        run_self_tests()
        print("OK")
        return

    N = int(data[0])
    S = data[1].strip()
    print(cdq_count(N, S))


if __name__ == "__main__":
    main()