import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    A = [int(x) for x in data[idx:idx + N]]

    # Group positions (0-indexed) by value
    pos_by_val = [[] for _ in range(M)]
    for p, v in enumerate(A):
        pos_by_val[v].append(p)

    # Fenwick tree over positions
    bit = [0] * (N + 1)

    def bit_add(i, delta):
        i += 1
        while i <= N:
            bit[i] += delta
            i += i & (-i)

    def bit_sum(i):
        # sum over positions [0, i)
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    # inv_lt[t] = inversions among elements with A_i < t, for t = 0..M
    inv_lt = [0] * (M + 1)
    cur = 0
    total = 0
    for v in range(M):
        group = pos_by_val[v]
        if group:
            # count: for each p, number of already-inserted (value < v) elements at positions > p
            for p in group:
                cur += total - bit_sum(p + 1)
            for p in group:
                bit_add(p, 1)
            total += len(group)
        inv_lt[v + 1] = cur

    # inv_ge[t] = inversions among elements with A_i >= t, for t = 0..M
    for i in range(N + 1):
        bit[i] = 0
    inv_ge = [0] * (M + 1)
    cur = 0
    # inv_ge[M] = 0 (no element >= M)
    for v in range(M - 1, -1, -1):
        group = pos_by_val[v]
        if group:
            # count: for each p, number of already-inserted (value > v) elements at positions < p
            for p in group:
                cur += bit_sum(p)
            for p in group:
                bit_add(p, 1)
        inv_ge[v] = cur

    # cross[t] = #{(i<j): A_i < t <= A_j} = posSum(S) - |S|(|S|+1)/2, S = {i: A_i >= t}
    cross = [0] * (M + 1)
    cnt = 0
    pos_sum = 0
    # cross[M] = 0
    for t in range(M - 1, 0, -1):
        group = pos_by_val[t]
        if group:
            cnt += len(group)
            pos_sum += sum(group) + len(group)  # 1-indexed positions
        cross[t] = pos_sum - cnt * (cnt + 1) // 2

    out = []
    for k in range(M):
        t = M - k
        out.append(str(inv_lt[t] + inv_ge[t] + cross[t]))
    sys.stdout.write("\n".join(out) + "\n")

main()