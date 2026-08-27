import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1]

    # States are partitions of (vertex 0, current vertex, hub):
    # 0: all separate
    # 1: 0 = current != hub
    # 2: 0 = hub != current
    # 3: current = hub != 0
    # 4: all connected
    #
    # At vertex 0, vertices 0 and current are identical.
    # Without its spoke: state 1. With its spoke selected: state 4.
    d0 = 0
    d1 = 1
    d2 = 0
    d3 = 0
    d4 = 1 if s[0] == 49 else 0

    for i in range(1, n):
        if s[i] == 48:
            # Add path edge from previous current vertex to i,
            # then forget the previous vertex.
            nd0 = 2 * d0 + d1 + d3
            nd1 = d1
            nd2 = 2 * d2 + d4
            nd3 = d3
            nd4 = d4
        else:
            # Same path transition, followed by optional spoke (i, hub).
            nd0 = 2 * d0 + d1 + d3
            nd1 = d1
            nd2 = 2 * d2 + d4
            nd3 = 2 * d0 + d1 + 2 * d3
            nd4 = d1 + 2 * d2 + 2 * d4

        d0 = nd0 % MOD
        d1 = nd1 % MOD
        d2 = nd2 % MOD
        d3 = nd3 % MOD
        d4 = nd4 % MOD

    # The closing edge (N-1, 0) can always be omitted.
    # It can be selected iff current and vertex 0 are disconnected:
    # states 0, 2, 3.
    ans = (2 * d0 + d1 + 2 * d2 + 2 * d3 + d4) % MOD
    print(ans)

if __name__ == "__main__":
    main()