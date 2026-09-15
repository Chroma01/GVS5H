import sys

MOD = 998244353
G = 3

def main():
    sys.setrecursionlimit(1 << 20)
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    if S[0] != 'B' or S[-1] != 'W':
        print(0)
        return
    b = [i+1 for i, ch in enumerate(S) if ch == 'B']
    d = [0]*N
    for t in range(1, N):
        d[t] = b[t] - t
    for t in range(1, N):
        if d[t] > N:
            print(0)
            return
    active = []
    t = 1
    while t <= N-1:
        v = d[t]
        T_start = t
        while t <= N-1 and d[t] == v:
            t += 1
        c = v - T_start - 1
        if c >= 0:
            active.append((T_start, v, c))
    m = len(active)
    fact = [1]*(N+1)
    for i in range(1, N+1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1]*(N+1)
    inv_fact[N] = pow(fact[N], MOD-2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD

    if m == 0:
        print(fact[N])
        return

    T = [0]*(m+1)
    v_arr = [0]*(m+1)
    c_arr = [0]*(m+1)
    for idx, (T_start, vv, cc) in enumerate(active, start=1):
        T[idx] = T_start
        v_arr[idx] = vv
        c_arr[idx] = cc
    f = [0]*(m+1)
    f[0] = 1
    acc = [0]*(m+1)

    try:
        import numpy as np
        HAS_NUMPY = True
    except ImportError:
        HAS_NUMPY = False

    if HAS_NUMPY:
        T_np = np.array(T, dtype=np.int64)
        v_np = np.array(v_arr, dtype=np.int64)
        c_np = np.array(c_arr, dtype=np.int64)
        f_np = np.zeros(m+1, dtype=np.int64)
        f_np[0] = 1
        acc_np = np.zeros(m+1, dtype=np.int64)
        fact_np = np.array(fact, dtype=np.int64)
        inv_fact_np = np.array(inv_fact, dtype=np.int64)

        MAX_LOG = 20
        roots = {}
        iroots = {}
        for k in range(1, MAX_LOG+1):
            length = 1 << k
            half = length >> 1
            wlen = pow(G, (MOD-1)//length, MOD)
            w = np.ones(half, dtype=np.int64)
            for i in range(1, half):
                w[i] = w[i-1] * wlen % MOD
            roots[length] = w
            iwlen = pow(wlen, MOD-2, MOD)
            iw = np.ones(half, dtype=np.int64)
            for i in range(1, half):
                iw[i] = iw[i-1] * iwlen % MOD
            iroots[length] = iw

        rev_cache = {}
        def get_rev(n):
            if n in rev_cache:
                return rev_cache[n]
            logn = n.bit_length() - 1
            idx = np.arange(n, dtype=np.int64)
            rev = np.zeros(n, dtype=np.int64)
            for i in range(logn):
                rev = (rev << 1) | ((idx >> i) & 1)
            rev_cache[n] = rev
            return rev

        def ntt(a, invert):
            n = a.shape[0]
            rev = get_rev(n)
            a[:] = a[rev]
            length = 2
            while length <= n:
                half = length >> 1
                w = iroots[length] if invert else roots[length]
                a = a.reshape(-1, length)
                u = a[:, :half].copy()
                v = a[:, half:] * w % MOD
                a[:, :half] = (u + v) % MOD
                a[:, half:] = (u - v) % MOD
                a = a.reshape(-1)
                length <<= 1
            if invert:
                inv_n = pow(n, MOD-2, MOD)
                a[:] = a * inv_n % MOD

        def convolve(A, B):
            need = len(A) + len(B) - 1
            n = 1
            while n < need:
                n <<= 1
            fa = np.zeros(n, dtype=np.int64)
            fb = np.zeros(n, dtype=np.int64)
            fa[:len(A)] = A
            fb[:len(B)] = B
            ntt(fa, False)
            ntt(fb, False)
            fa = fa * fb % MOD
            ntt(fa, True)
            return fa[:need]

        def add_contrib(l, mid, ml, mr):
            left_size = mid - l + 1
            right_size = mr - ml + 1
            if left_size * right_size <= 2048:
                for j in range(ml, mr+1):
                    vj = int(v_np[j])
                    s = 0
                    for i in range(l, mid+1):
                        d = vj - int(T_np[i]) - 1
                        if d >= 0:
                            s += int(f_np[i]) * int(fact_np[d])
                    acc_np[j] = (int(acc_np[j]) + s) % MOD
                return
            T_min = T_np[l]
            T_max = T_np[mid]
            v_min = v_np[ml]
            v_max = v_np[mr]
            d_min = v_min - T_max - 1
            d_max = v_max - T_min - 1
            if d_max < 0:
                return
            L_A = T_max - T_min + 1
            L_B = d_max - d_min + 1
            A = np.zeros(L_A, dtype=np.int64)
            T_slice = T_np[l:mid+1]
            f_slice = f_np[l:mid+1]
            A[T_slice - T_min] = f_slice
            B = np.zeros(L_B, dtype=np.int64)
            if d_min >= 0:
                B[:] = fact_np[d_min : d_min + L_B]
            else:
                start = -d_min
                B[start:] = fact_np[:L_B - start]
            C = convolve(A, B)
            v_slice = v_np[ml:mr+1]
            y = v_slice - 1 - T_min - d_min
            acc_np[ml:mr+1] = (acc_np[ml:mr+1] + C[y]) % MOD

        def solve(l, r):
            if l == r:
                if l > 0:
                    f_np[l] = (-inv_fact_np[c_np[l]] * acc_np[l]) % MOD
                return
            mid = (l + r) // 2
            solve(l, mid)
            add_contrib(l, mid, mid+1, r)
            solve(mid+1, r)

        solve(0, m)
        ans = 0
        for i in range(m+1):
            ans = (ans + int(f_np[i]) * int(fact_np[N - T_np[i]])) % MOD
        print(ans)

    else:
        def ntt_py(a, invert):
            n = len(a)
            j = 0
            for i in range(1, n):
                bit = n >> 1
                while j & bit:
                    j ^= bit
                    bit >>= 1
                j ^= bit
                if i < j:
                    a[i], a[j] = a[j], a[i]
            length = 2
            while length <= n:
                wlen = pow(G, (MOD-1)//length, MOD)
                if invert:
                    wlen = pow(wlen, MOD-2, MOD)
                half = length >> 1
                for i in range(0, n, length):
                    w = 1
                    for j in range(i, i + half):
                        u = a[j]
                        v = a[j + half] * w % MOD
                        a[j] = (u + v) % MOD
                        a[j + half] = (u - v) % MOD
                        w = w * wlen % MOD
                length <<= 1
            if invert:
                inv_n = pow(n, MOD-2, MOD)
                for i in range(n):
                    a[i] = a[i] * inv_n % MOD

        def convolve_py(A, B):
            need = len(A) + len(B) - 1
            n = 1
            while n < need:
                n <<= 1
            fa = A + [0]*(n - len(A))
            fb = B + [0]*(n - len(B))
            ntt_py(fa, False)
            ntt_py(fb, False)
            for i in range(n):
                fa[i] = fa[i] * fb[i] % MOD
            ntt_py(fa, True)
            return fa[:need]

        def add_contrib(l, mid, ml, mr):
            left_size = mid - l + 1
            right_size = mr - ml + 1
            if left_size * right_size <= 2048:
                for j in range(ml, mr+1):
                    vj = v_arr[j]
                    s = 0
                    for i in range(l, mid+1):
                        d = vj - T[i] - 1
                        if d >= 0:
                            s += f[i] * fact[d]
                    acc[j] = (acc[j] + s) % MOD
                return
            T_min = T[l]
            T_max = T[mid]
            v_min = v_arr[ml]
            v_max = v_arr[mr]
            d_min = v_min - T_max - 1
            d_max = v_max - T_min - 1
            if d_max < 0:
                return
            L_A = T_max - T_min + 1
            L_B = d_max - d_min + 1
            A = [0] * L_A
            for i in range(l, mid+1):
                A[T[i] - T_min] = f[i]
            B = [0] * L_B
            if d_min >= 0:
                B[:] = fact[d_min : d_min + L_B]
            else:
                start = -d_min
                B[start:] = fact[:L_B - start]
            C = convolve_py(A, B)
            for j in range(ml, mr+1):
                y = v_arr[j] - 1 - T_min - d_min
                if 0 <= y < len(C):
                    acc[j] = (acc[j] + C[y]) % MOD

        def solve(l, r):
            if l == r:
                if l > 0:
                    f[l] = (-inv_fact[c_arr[l]] * acc[l]) % MOD
                return
            mid = (l + r) // 2
            solve(l, mid)
            add_contrib(l, mid, mid+1, r)
            solve(mid+1, r)

        solve(0, m)
        ans = 0
        for i in range(m+1):
            ans = (ans + f[i] * fact[N - T[i]]) % MOD
        print(ans)

if __name__ == "__main__":
    main()