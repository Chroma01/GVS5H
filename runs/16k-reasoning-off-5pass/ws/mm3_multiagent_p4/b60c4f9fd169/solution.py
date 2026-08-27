import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)
    if abs(n - m) > K:
        print("No")
        return
    INF = K + 1
    size = 2 * K + 1
    # offset d: -K .. K, map to index 0..2K
    off = K
    # prev: for column j-1
    prev = [INF] * size
    # j = 0: i in [0, min(n, K)], d = i - 0 = i
    for i in range(min(n, K) + 1):
        prev[i] = i  # d = i
    # iterate j = 1 .. m
    for j in range(1, m + 1):
        cur = [INF] * size
        d_min = max(-j, -K)
        d_max = min(K, n - j)
        # valid d range for prev (column j-1)
        d_min_prev = max(-(j - 1), -K)
        d_max_prev = min(K, n - (j - 1))
        # Process d from d_min to d_max
        for d in range(d_min, d_max + 1):
            # i = j + d
            i = j + d
            if i == 0:
                # f(0, j) = j
                cur[d + off] = j
                continue
            # f(i-1, j): cur[d-1] if computed
            del_cost = cur[d - 1 + off] if d - 1 >= d_min else INF
            # f(i, j-1): prev[d+1]
            ins_cost = prev[d + 1 + off] if d + 1 <= d_max_prev else INF
            # f(i-1, j-1): prev[d]
            sub_cost = prev[d + off]
            # add substitution cost
            if S[i - 1] != T[j - 1]:
                sub_cost += 1
            cur[d + off] = min(del_cost, ins_cost, sub_cost)
        # check if all cur > K, we can stop
        if min(cur) > K:
            print("No")
            return
        prev = cur
    # after loop, f(n, m) is at d = n - m
    d_final = n - m
    if prev[d_final + off] <= K:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()