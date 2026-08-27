import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    s = data[1] if len(data) > 1 else b''
    MOD = 998244353

    # positions of '1'
    try:
        import numpy as np
        arr = np.frombuffer(s, dtype=np.uint8)
        pos = np.flatnonzero(arr == 49)  # ord('1')
        k = int(pos.size)
        use_np = True
    except Exception:
        np = None
        pos = [i for i, ch in enumerate(s) if ch == 49]
        k = len(pos)
        use_np = False

    if k == 0:
        sys.stdout.write(str((pow(2, N, MOD) - 1) % MOD) + "\n")
        return

    # cyclic gaps
    if use_np:
        if k == 1:
            gaps = np.array([N], dtype=np.int64)
        else:
            p64 = pos.astype(np.int64)
            gaps = np.empty(k, dtype=np.int64)
            gaps[:k-1] = p64[1:] - p64[:-1]
            gaps[k-1] = N - p64[k-1] + p64[0]
        # sanity
        # assert int(gaps.sum()) == N
        # vectorized binary exponentiation: 2^g mod MOD
        e = gaps.copy()
        res = np.ones(k, dtype=np.int64)
        base = np.full(k, 2 % MOD, dtype=np.int64)
        while True:
            mask = (e & 1).astype(np.int64)
            # multiply res by base where mask==1
            mult = np.where(mask == 1, base, 1)
            res = (res * mult) % MOD
            e >>= 1
            if not e.any():
                break
            base = (base * base) % MOD
        ps = res.tolist()
    else:
        if k == 1:
            gaps = [N]
        else:
            gaps = [pos[j+1] - pos[j] for j in range(k-1)]
            gaps.append(N - pos[k-1] + pos[0])
        mx = max(gaps)
        pw = [1] * (mx + 1)
        for i in range(1, mx + 1):
            pw[i] = pw[i-1] * 2 % MOD
        ps = [pw[g] for g in gaps]

    a, b, c, d = 1, 0, 0, 1
    for p in ps:
        u = a * p % MOD
        v = c * p % MOD
        a = (u + u + b) % MOD
        b = -u
        c = (v + v + d) % MOD
        d = -v

    ans = (a + d - 2) % MOD
    sys.stdout.write(str(ans) + "\n")

main()