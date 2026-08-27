import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    NEG = -10**30

    # dp[i] = max total score considering first i elements (1-indexed),
    #         where element i is left unmatched (all before i are matched).
    # dp[0] = 0 (empty prefix, nothing unmatched).
    #
    # Transition: either keep i unmatched after dp[i-1] (so i-1 was unmatched too),
    # or match i with some j < i where (i - j) is odd (so the elements between
    # j and i can be perfectly matched), giving dp[j-1] + |a[j] - a[i]|.
    #
    # |a[j] - a[i]| = max(a[i] - a[j], a[j] - a[i]), so:
    #   dp[i] = max(dp[i-1],
    #               max over valid j of (dp[j-1] - a[j]) + a[i],
    #               max over valid j of (dp[j-1] + a[j]) - a[i])
    # Valid j requires j and i to have opposite parity, i.e. (j-1) and (i-1)
    # have the same parity. We maintain running maxima of dp[j-1] - a[j] and
    # dp[j-1] + a[j] grouped by parity of (j-1).

    # best_minus[p] = max of dp[j-1] - a[j] over j with (j-1) % 2 == p
    # best_plus[p]  = max of dp[j-1] + a[j] over j with (j-1) % 2 == p
    best_minus = [NEG, NEG]
    best_plus = [NEG, NEG]

    dp_prev = 0  # dp[i-1], starts as dp[0] = 0
    ans = 0

    for i in range(1, n + 1):
        x = a[i - 1]
        p = (i - 1) & 1  # parity of i-1; j must satisfy (j-1) % 2 == p

        cand = dp_prev  # leave i unmatched, extending dp[i-1]
        if best_minus[p] != NEG:
            v = best_minus[p] + x
            if v > cand:
                cand = v
        if best_plus[p] != NEG:
            v = best_plus[p] - x
            if v > cand:
                cand = v

        dpi = cand
        if dpi > ans:
            ans = dpi

        # Now position i becomes a candidate j for future indices:
        # update structures with dp[i-1] - a[i] and dp[i-1] + a[i]
        # (these use dp[j-1] = dp[i-1], parity of j-1 = parity of i-1 = p)
        vm = dp_prev - x
        if vm > best_minus[p]:
            best_minus[p] = vm
        vp = dp_prev + x
        if vp > best_plus[p]:
            best_plus[p] = vp

        dp_prev = dpi

    print(ans)

main()