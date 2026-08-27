import sys

MOD = 998244353

def state_of(parent):
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ha = find(0) == find(1)
    hb = find(0) == find(2)
    ab = find(1) == find(2)

    if ha and hb:
        return 4
    if ha:
        return 1
    if hb:
        return 2
    if ab:
        return 3
    return 0

def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    # States describe connectivity among:
    # 0 = hub, 1 = vertex 0, 2 = current rim vertex.
    # 0: all separate, 1: hub-0, 2: hub-current,
    # 3: 0-current, 4: all connected.
    dp = [0] * 5

    # Initialize using vertices 0, 1 and all available edges among
    # hub-0, 0-1, hub-1.
    choices0 = 2 if s[0] == '1' else 1
    choices1 = 2 if s[1] == '1' else 1

    for take_spoke0 in range(choices0):
        for take_rim in range(2):
            for take_spoke1 in range(choices1):
                parent = [0, 1, 2]

                def find(x):
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x

                ok = True
                for u, v, take in (
                    (0, 1, take_spoke0),
                    (1, 2, take_rim),
                    (0, 2, take_spoke1),
                ):
                    if take:
                        ru = find(u)
                        rv = find(v)
                        if ru == rv:
                            ok = False
                            break
                        parent[ru] = rv

                if ok:
                    dp[state_of(parent)] += 1

    a, b, c, d, e = dp

    # Add vertices 2..N-1. At each step choose the new rim edge and,
    # if present, the new spoke; discard choices creating a cycle.
    for i in range(2, n):
        na = (2 * a + c + d) % MOD
        nb = (2 * b + e) % MOD

        if s[i] == '0':
            nc = c
            nd = d
            ne = e
        else:
            nc = (2 * a + 2 * c + d) % MOD
            nd = d
            ne = (2 * b + d + 2 * e) % MOD

        a, b, c, d, e = na, nb, nc, nd, ne

    # Add the closing rim edge N-1 -- 0.
    # It has two choices unless its endpoints are already connected.
    ans = (2 * (a + b + c) + d + e) % MOD
    print(ans)

if __name__ == "__main__":
    main()