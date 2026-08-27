import sys

def main():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return
    s = data[1]
    mod = 998244353

    # Counts for reachable non-dead DFA masks:
    # 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 15
    # Mask 0 is dead and is omitted.
    c1 = c2 = c3 = c4 = c5 = c8 = c9 = c10 = c11 = c12 = c13 = c15 = 0
    c9 = 1  # initial identity relation: (0,0) and (1,1)
    cnt = 0

    for ch in s:
        # Common subexpressions from old state.
        y123 = c1 + c2 + c3
        y48 = c4 + c8
        y510 = c5 + c10
        y911 = c9 + c11
        y913 = c9 + c13
        t4812 = y48 + c12
        t51015 = y510 + c15

        if ch == 48:  # '0': x_i can be 0, 1, 2
            n3 = c3
            n9 = c9
            n11 = c11
            n12 = c12
            n13 = c13
            n15 = c15
        else:         # '1': x_i can be 0, 1, 2, 3
            n3 = y123 + c3
            n9 = 0
            n11 = y911
            n12 = t4812 + c12
            n13 = y913
            n15 = t51015 + c11 + c13 + c15

        n1 = y123
        n2 = y123 + y911
        n4 = t4812 + y913
        n5 = t51015 + c11
        n8 = t4812
        n10 = t51015 + c13

        c1 = n1
        c2 = n2
        c3 = n3
        c4 = n4
        c5 = n5
        c8 = n8
        c9 = n9
        c10 = n10
        c11 = n11
        c12 = n12
        c13 = n13
        c15 = n15

        cnt += 1
        if cnt == 64:
            c1 %= mod
            c2 %= mod
            c3 %= mod
            c4 %= mod
            c5 %= mod
            c8 %= mod
            c9 %= mod
            c10 %= mod
            c11 %= mod
            c12 %= mod
            c13 %= mod
            c15 %= mod
            cnt = 0

    ans = (c1 + c3 + c5 + c8 + c9 + c10 + c11 + c12 + c13 + c15) % mod
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()