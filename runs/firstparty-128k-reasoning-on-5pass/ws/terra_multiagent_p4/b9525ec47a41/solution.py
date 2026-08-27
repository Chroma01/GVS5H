import sys

MOD = 998244353

def main():
    input = sys.stdin.readline
    N = int(input())
    s = input().strip()

    # State for the processed path, retaining:
    # H = hub, A = vertex 0, C = current last rim vertex.
    #
    # 0: H | A | C
    # 1: HA | C
    # 2: HC | A
    # 3: AC | H
    # 4: HAC
    state_id = {
        (0, 1, 2): 0,
        (0, 0, 1): 1,
        (0, 1, 0): 2,
        (0, 1, 1): 3,
        (0, 0, 0): 4,
    }

    # Initialize vertices 0 and 1.
    # Possible edges: 0-1, H-0 if s[0], H-1 if s[1].
    dp = [0] * 5
    for use_path in range(2):
        for use_h0 in range(2 if s[0] == '1' else 1):
            for use_h1 in range(2 if s[1] == '1' else 1):
                parent = [0, 1, 2]

                def find(x):
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x

                valid = True
                for x, y, use in ((1, 2, use_path), (0, 1, use_h0), (0, 2, use_h1)):
                    if use:
                        rx = find(x)
                        ry = find(y)
                        if rx == ry:
                            valid = False
                            break
                        parent[rx] = ry

                if valid:
                    roots = [find(i) for i in range(3)]
                    canon = {}
                    labels = []
                    for r in roots:
                        if r not in canon:
                            canon[r] = len(canon)
                        labels.append(canon[r])
                    dp[state_id[tuple(labels)]] += 1

    # Add vertices 2 through N-1.
    for i in range(2, N):
        d0, d1, d2, d3, d4 = dp

        # Edges from the old current vertex to the new vertex may be
        # absent/present. The new spoke may be absent/present according to s[i].
        #
        # With no new spoke:
        # n0 = 2d0+d2+d3, n1 = 2d1+d4, n2=d2, n3=d3, n4=d4.
        #
        # With a new spoke:
        # n0 = 2d0+d2+d3, n1 = 2d1+d4,
        # n2 = 2d0+2d2+d3, n3=d3, n4=2d1+d3+2d4.
        n0 = 2 * d0 + d2 + d3
        n1 = 2 * d1 + d4

        if s[i] == '0':
            dp = [n0 % MOD, n1 % MOD, d2, d3, d4]
        else:
            n2 = 2 * d0 + 2 * d2 + d3
            n4 = 2 * d1 + d3 + 2 * d4
            dp = [n0 % MOD, n1 % MOD, n2 % MOD, d3, n4 % MOD]

    # First count forests without closing rim edge (N-1, 0).
    # The closing edge can additionally be included exactly when A and C
    # are disconnected, namely in states 0, 1, 2.
    ans = sum(dp) + dp[0] + dp[1] + dp[2]
    print(ans % MOD)

if __name__ == "__main__":
    main()