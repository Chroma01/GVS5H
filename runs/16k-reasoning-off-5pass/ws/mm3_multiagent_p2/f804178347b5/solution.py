import sys
sys.setrecursionlimit(10000000)

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    A = data[1].strip()
    L = len(A)
    # Precompute current root value by applying operation N times
    cur = A
    while len(cur) > 1:
        nxt = []
        for i in range(0, len(cur), 3):
            a, b, c = cur[i], cur[i+1], cur[i+2]
            # majority
            if a == b or a == c:
                maj = a
            else:
                maj = b
            nxt.append(maj)
        cur = ''.join(nxt)
    cur_root = int(cur)  # 0 or 1

    # DP: returns (cost0, cost1) for substring A[l:r] (half-open)
    # where the substring length is a power of 3 (3^k for some k)
    def dp(l, r):
        length = r - l
        if length == 1:
            val = int(A[l])
            if val == 0:
                return (0, 1)  # cost0=0, cost1=1
            else:
                return (1, 0)  # cost0=1, cost1=0
        third = length // 3
        c0_1, c1_1 = dp(l, l + third)
        c0_2, c1_2 = dp(l + third, l + 2 * third)
        c0_3, c1_3 = dp(l + 2 * third, r)
        # cost to make majority 0: need at least two zeros among children
        # possibilities: (0,0,0), (0,0,1), (0,1,0), (1,0,0)
        cost0 = min(
            c0_1 + c0_2 + c0_3,
            c0_1 + c0_2 + c1_3,
            c0_1 + c1_2 + c0_3,
            c1_1 + c0_2 + c0_3
        )
        # cost to make majority 1: need at least two ones among children
        cost1 = min(
            c1_1 + c1_2 + c1_3,
            c1_1 + c1_2 + c0_3,
            c1_1 + c0_2 + c1_3,
            c0_1 + c1_2 + c1_3
        )
        return (cost0, cost1)

    total_cost0, total_cost1 = dp(0, L)
    target = 1 - cur_root
    if target == 0:
        print(total_cost0)
    else:
        print(total_cost1)

if __name__ == "__main__":
    solve()