import sys

MOD = 998244353


def compose(r, m):
    """Return the relation obtained by applying r, then m."""
    out = 0
    for a in range(2):
        for b in range(2):
            if r & (1 << (2 * a + b)):
                for c in range(2):
                    if m & (1 << (2 * b + c)):
                        out |= 1 << (2 * a + c)
    return out


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1]

    comp = [[0] * 16 for _ in range(16)]
    for r in range(16):
        for m in range(16):
            comp[r][m] = compose(r, m)

    # Bit (2*a+b) represents a transition from cycle state a to b.
    #
    # At a zero-spoke vertex, the cycle contribution is 1 + a - b:
    # d=0: (a,b)=(0,1) -> mask 2
    # d=1: (0,0) or (1,1) -> mask 9
    # d=2: (a,b)=(1,0) -> mask 4
    zero_masks = (2, 9, 4)

    # At a one-spoke vertex, the spoke may contribute either 0 or 1:
    # d=0: cycle contribution 0
    # d=1: cycle contribution 1, or 0 plus incoming spoke
    # d=2: cycle contribution 2, or 1 plus incoming spoke
    # d=3: cycle contribution 2 plus incoming spoke
    one_masks = (2, 11, 13, 4)

    # For each relation state and vertex type, merge equal resulting
    # relation states while retaining the number of distinct symbols
    # (observed indegrees) producing each result.
    transitions = []
    for masks in (zero_masks, one_masks):
        table = []
        for r in range(16):
            counts = {}
            for mask in masks:
                t = comp[r][mask]
                counts[t] = counts.get(t, 0) + 1
            table.append(tuple(counts.items()))
        transitions.append(table)

    # The initial relation is identity: initial and final cycle states agree.
    dp = [0] * 16
    dp[9] = 1

    for ch in s:
        table = transitions[1 if ch == ord('1') else 0]
        ndp = [0] * 16

        for r, value in enumerate(dp):
            if value:
                for t, multiplicity in table[r]:
                    ndp[t] += value * multiplicity

        for i in range(16):
            ndp[i] %= MOD
        dp = ndp

    # A local indegree word is realizable on the cycle iff the final
    # relation contains (0,0) or (1,1).
    answer = 0
    for relation, value in enumerate(dp):
        if relation & 9:
            answer += value

    print(answer % MOD)


if __name__ == "__main__":
    main()