import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # c_k = #{j > k : P_j <= k} = k - #{j <= k : P_j <= k}
    # base = sum k * c_k ; sumc = sum c_k ; first_k = min{k : c_k >= 1}
    base = 0
    sumc = 0
    first_k = -1
    cnt = 0  # f(k) = #{j <= k : P_j <= k}
    for k in range(1, n):
        if P[k - 1] <= k:
            cnt += 1
        ck = k - cnt
        if ck:
            base += k * ck
            sumc += ck
            if first_k == -1:
                first_k = k

    # inversion parity via Fenwick tree
    bit = [0] * (n + 1)
    inv = 0
    for idx, v in enumerate(P):
        s = 0
        i = v
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        inv += idx - s
        i = v
        while i <= n:
            bit[i] += 1
            i += i & (-i)

    ans = base
    if (sumc & 1) != (inv & 1):
        # Total swap count must match inv(P) mod 2. One extra crossing at
        # boundary k (x_k = c_k + 1) is feasible iff c_k >= 1 (a value > k
        # on the left of k does a round trip paired against mandatory
        # traffic). Cheapest such boundary is first_k. A mismatch with
        # first_k = 1 cannot occur for N = 2 (there c_1 = inv), so this
        # is always feasible.
        ans += first_k
    print(ans)

solve()