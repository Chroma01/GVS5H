import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a_start = 1
    b_start = 1 + n
    c_start = 1 + 2 * n

    # D: 1 -> 0, P: 0 -> 1, K: 1 -> 1 (may be flipped off and later on)
    D = []
    P = []
    K = []
    kept_sum = 0

    for i in range(n):
        a = data[a_start + i]
        b = data[b_start + i]
        c = data[c_start + i]

        if a == 1:
            if b == 0:
                D.append(c)
            else:
                K.append(c)
                kept_sum += c
        else:
            if b == 1:
                P.append(c)

    del data

    D.sort(reverse=True)
    P.sort()
    K.sort(reverse=True)

    d = len(D)
    u = len(P)

    # Cost when no common 1 is flipped twice.
    # Down phase: D sorted descending, contribution of rank i (0-indexed) is i * c.
    sumD = 0
    down_cost = 0
    for i, c in enumerate(D):
        sumD += c
        down_cost += i * c

    # Up phase: P sorted ascending, contribution of rank i (0-indexed) is (u - i) * c.
    sumP = 0
    up_cost = 0
    for i, c in enumerate(P):
        sumP += c
        up_cost += (u - i) * c

    total_ops = d + u
    current = down_cost + up_cost + total_ops * kept_sum
    ans = current

    # Process common 1s from largest cost to smallest cost.
    # After processing r of them, exactly the r largest common 1s are flipped twice.
    pD = 0
    sumD_less = sumD       # sum of D elements strictly smaller than current x

    pP = u
    sumP_le = sumP         # sum of P elements <= current x

    removed = 0

    for x in K:
        # Insert x into the down multiset (D plus already removed common 1s).
        # Already removed common 1s are all >= x, so each contributes x.
        while pD < d and D[pD] >= x:
            sumD_less -= D[pD]
            pD += 1
        add_down = (pD + removed) * x + sumD_less

        # Insert x into the up multiset (P plus already removed common 1s).
        # Already removed common 1s are all >= x, so each also contributes x.
        while pP > 0 and P[pP - 1] > x:
            sumP_le -= P[pP - 1]
            pP -= 1
        add_up = sumP_le + (u - pP + removed + 1) * x

        # Moving x from kept to removed:
        # - down_cost increases by add_down
        # - up_cost increases by add_up
        # - total_ops increases by 2
        # - kept_sum decreases by x
        current += add_down + add_up + 2 * kept_sum - (total_ops + 2) * x

        if current < ans:
            ans = current

        kept_sum -= x
        total_ops += 2
        removed += 1

    print(ans)


if __name__ == "__main__":
    solve()