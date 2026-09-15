import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    offA = 1
    offB = 1 + N
    offC = 1 + 2 * N

    # R: mandatory 1 -> 0 (negative flips)
    # P: mandatory 0 -> 1 (positive flips)
    # E: optional equal-1 indices (can be temporarily turned off/on)
    R = []
    P = []
    E = []

    W0 = 0
    sumR = 0
    sumP = 0

    for i in range(N):
        a = data[offA + i]
        b = data[offB + i]
        c = data[offC + i]

        if a == 1:
            W0 += c
            if b == 1:
                E.append(c)
            else:
                R.append(c)
                sumR += c
        else:
            if b == 1:
                P.append(c)
                sumP += c

    del data

    R.sort(reverse=True)
    P.sort()
    E.sort(reverse=True)

    # Cost with no temporary off/on pairs.
    w = W0
    cost = 0
    for c in R:
        w -= c
        cost += w
    for c in P:
        w += c
        cost += w

    ans = cost

    r = len(R)
    r_ptr = 0
    r_gt_sum = 0

    p_ptr = len(P)
    p_lt_sum = sumP

    K = len(E)
    i = 0
    group_sum = 0  # sum of E values in previous (strictly larger) groups
    twoW0 = 2 * W0

    # Scan prefixes of E sorted decreasingly, group by equal C.
    while i < K:
        c = E[i]
        j = i + 1
        while j < K and E[j] == c:
            j += 1

        # Mandatory removals with weight > c.
        while r_ptr < r and R[r_ptr] > c:
            r_gt_sum += R[r_ptr]
            r_ptr += 1

        # Mandatory additions with weight < c.
        while p_ptr > 0 and P[p_ptr - 1] >= c:
            p_lt_sum -= P[p_ptr - 1]
            p_ptr -= 1

        # For the first element of this equal-C group:
        # negative greater sum = R greater + all previous E groups
        # positive less sum = P less (previous E are >= c)
        sum_gt = r_gt_sum + group_sum

        # Marginal cost of adding the first temporary pair of this weight.
        delta = (
            twoW0
            - sum_gt
            - sumR
            - group_sum
            + p_lt_sum
            - c * (1 + r - r_ptr + p_ptr)
        )

        # Inside the same equal-C group, each additional pair increases
        # the current negative sum by c and the number of negative flips
        # after the new off-flip by 1, so delta decreases by 2*c.
        step = 2 * c
        for _ in range(j - i):
            cost += delta
            if cost < ans:
                ans = cost
            delta -= step

        group_sum += c * (j - i)
        i = j

    print(ans)


if __name__ == "__main__":
    solve()