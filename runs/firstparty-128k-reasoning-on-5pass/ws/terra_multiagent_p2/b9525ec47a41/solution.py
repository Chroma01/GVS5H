import sys

MOD = 998244353

def main():
    input = sys.stdin.readline
    N = int(input())
    s = input().strip()

    # Connectivity states among (H, A=vertex 0, B=current vertex):
    # 0: H | A | B
    # 1: HA | B
    # 2: HB | A
    # 3: AB | H
    # 4: HAB
    state_id = {
        (0, 1, 2): 0,
        (0, 0, 1): 1,
        (0, 1, 0): 2,
        (0, 1, 1): 3,
        (0, 0, 0): 4,
    }

    # Enumerate forests on H, vertex 0, vertex 1.
    edges = []
    if s[0] == '1':
        edges.append((0, 1))  # H-A
    if s[1] == '1':
        edges.append((0, 2))  # H-B
    edges.append((1, 2))      # A-B

    dp = [0] * 5
    for mask in range(1 << len(edges)):
        parent = [0, 1, 2]

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        ok = True
        for j, (u, v) in enumerate(edges):
            if (mask >> j) & 1:
                u = find(u)
                v = find(v)
                if u == v:
                    ok = False
                    break
                parent[u] = v

        if ok:
            roots = [find(i) for i in range(3)]
            remap = {}
            part = []
            for r in roots:
                if r not in remap:
                    remap[r] = len(remap)
                part.append(remap[r])
            dp[state_id[tuple(part)]] += 1

    # Add vertices 2, 3, ..., N-1.
    for i in range(2, N):
        a, b, c, d, e = dp

        if s[i] == '0':
            # Only edge B-C is available.
            dp = [
                (2 * a + c + d) % MOD,
                (2 * b + e) % MOD,
                c,
                d,
                e,
            ]
        else:
            # Both B-C and H-C are available.
            # In state HB|A, selecting both edges creates a cycle.
            # In state HAB, selecting both edges also creates a cycle.
            dp = [
                (2 * a + c + d) % MOD,
                (2 * b + e) % MOD,
                (2 * a + 2 * c + d) % MOD,
                d,
                (2 * b + d + 2 * e) % MOD,
            ]

    # Add or exclude the closing edge between N-1 and 0.
    # It can be included exactly in states where A and B are disconnected.
    a, b, c, d, e = dp
    ans = (2 * (a + b + c) + d + e) % MOD
    print(ans)

if __name__ == "__main__":
    main()