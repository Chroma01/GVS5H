import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2+N]]
    P.sort()
    minP = P[0]

    # If the budget cannot even buy one unit of the cheapest product
    if M < minP:
        print(0)
        return

    def cost_gt(L, P=P, M=M):
        total = 0
        for p in P:
            if p > L:
                break
            x = L // p
            c = (x + 1) >> 1
            total += p * c * c
            if total > M:
                return True
        return False

    lo = 0
    hi = 1
    while not cost_gt(hi):
        lo = hi
        hi <<= 1

    while lo + 1 < hi:
        mid = (lo + hi) >> 1
        if cost_gt(mid):
            hi = mid
        else:
            lo = mid

    # Now lo = hi - 1, cost(lo) <= M, cost(hi) > M
    count = 0
    total_cost = 0
    for p in P:
        if p > lo:
            break
        x = lo // p
        c = (x + 1) >> 1
        count += c
        total_cost += p * c * c

    remaining = M - total_cost
    ans = count + remaining // hi
    print(ans)

if __name__ == "__main__":
    solve()