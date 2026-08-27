import sys

MOD = 998244353


def build_transitions():
    trans = [[0] * 4 for _ in range(2)]

    # s_i = 0: output is c = 1 + x - z
    for x in range(2):
        for z in range(2):
            c = 1 + x - z
            trans[0][c] |= 1 << (2 * x + z)

    # s_i = 1: output is c + b, where b is 0 or 1
    for x in range(2):
        for z in range(2):
            c = 1 + x - z
            bit = 1 << (2 * x + z)
            trans[1][c] |= bit
            trans[1][c + 1] |= bit

    return trans


def build_composition():
    comp = [[0] * 16 for _ in range(16)]
    for r in range(16):
        for t in range(16):
            result = 0
            for start in range(2):
                for end in range(2):
                    possible = False
                    for middle in range(2):
                        if (r >> (2 * start + middle)) & 1:
                            if (t >> (2 * middle + end)) & 1:
                                possible = True
                                break
                    if possible:
                        result |= 1 << (2 * start + end)
            comp[r][t] = result
    return comp


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    trans = build_transitions()
    comp = build_composition()

    # Relation from the initial cycle state a_0 to the current state.
    # Identity relation: 0 -> 0 and 1 -> 1.
    dp = [0] * 16
    dp[9] = 1

    for ch in s:
        typ = ord(ch) - ord('0')
        ndp = [0] * 16

        for relation, count in enumerate(dp):
            if count == 0:
                continue
            for output in range(4):
                edge_relation = trans[typ][output]
                if edge_relation:
                    new_relation = comp[relation][edge_relation]
                    ndp[new_relation] = (ndp[new_relation] + count) % MOD

        dp = ndp

    # A degree word is realizable on the cycle iff some initial state
    # returns to itself, i.e. the final relation contains (0,0) or (1,1).
    answer = 0
    for relation, count in enumerate(dp):
        if relation & 1 or relation & 8:
            answer = (answer + count) % MOD

    print(answer)


if __name__ == "__main__":
    solve()