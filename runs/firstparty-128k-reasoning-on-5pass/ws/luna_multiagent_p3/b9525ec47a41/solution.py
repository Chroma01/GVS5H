import sys

MOD = 998244353


def compose(r, t):
    """Return the Boolean relation obtained by applying r, then t."""
    result = 0

    # Relation bits:
    # 1: 0 -> 0, 2: 0 -> 1, 4: 1 -> 0, 8: 1 -> 1
    if r & 1:
        if t & 1:
            result |= 1
        if t & 2:
            result |= 2
    if r & 2:
        if t & 4:
            result |= 1
        if t & 8:
            result |= 2
    if r & 4:
        if t & 1:
            result |= 4
        if t & 2:
            result |= 8
    if r & 8:
        if t & 4:
            result |= 4
        if t & 8:
            result |= 8

    return result


def main():
    n = int(sys.stdin.readline())
    s = sys.stdin.readline().strip()

    compose_table = [[compose(a, b) for b in range(16)] for a in range(16)]

    # x_i = 1 iff the cycle edge {i, i+1} is directed i -> i+1.
    # For vertex i, the cycle contribution is 1 + x_{i-1} - x_i.
    #
    # Relation bit layout:
    #   bit 0: 0 -> 0
    #   bit 1: 0 -> 1
    #   bit 2: 1 -> 0
    #   bit 3: 1 -> 1
    #
    # Inactive spoke (s_i = 0):
    #   d=0: 0 -> 1
    #   d=1: 0 -> 0 or 1 -> 1
    #   d=2: 1 -> 0
    inactive = (2, 9, 4)

    # Active spoke (s_i = 1). The spoke contributes either 0 or 1
    # to d_i:
    #   d=0: 0 -> 1
    #   d=1: 0 -> 0, 0 -> 1, 1 -> 1
    #   d=2: 0 -> 0, 1 -> 0, 1 -> 1
    #   d=3: 1 -> 0
    active = (2, 11, 13, 4)

    # The relation before processing any vertex is the identity.
    dp = [0] * 16
    dp[9] = 1

    for ch in s:
        choices = active if ch == "1" else inactive
        ndp = [0] * 16

        for relation, count in enumerate(dp):
            if count == 0:
                continue
            row = compose_table[relation]
            for local_relation in choices:
                new_relation = row[local_relation]
                ndp[new_relation] += count
                if ndp[new_relation] >= MOD:
                    ndp[new_relation] -= MOD

        dp = ndp

    # A cyclic orientation exists exactly when the composed relation
    # contains 0 -> 0 or 1 -> 1.
    answer = 0
    for relation, count in enumerate(dp):
        if relation & 1 or relation & 8:
            answer += count

    print(answer % MOD)


if __name__ == "__main__":
    main()