import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    s = data[1]
    MOD = 998244353
    inv2 = (MOD + 1) // 2
    ONE = 49  # ord('1')

    M_total = s.count(b'1')

    # Pre = 2^{#marked before position i}, initially for i = N-1
    Pre = pow(2, M_total - (1 if s[N - 1] == ONE else 0), MOD)

    # 4x4 matrix M: state 0=(0,false), 1=(0,true), 2=(2,false), 3=(2,true)
    # M[s][t] = ways to go from start state s at position i to final state t
    M = [1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1]
    M2 = [0] * 16

    ans = 0

    for i in range(N - 1, -1, -1):
        m = Pre

        # contribution for anchor label L=0 (state 0)
        tot0 = M[0] + M[1] + M[2] + M[3]
        tot0 %= MOD
        bad0 = M[0]
        # contribution for anchor label L=2 (state 2)
        tot2 = M[8] + M[9] + M[10] + M[11]
        tot2 %= MOD
        bad2 = M[10]  # column 2 in row 2

        ans = (ans + m * tot0 - bad0 + m * tot2 - bad2) % MOD

        if i == 0:
            break

        if s[i] == ONE:
            # marked position
            n0 = (M[0] + M[4] + M[8]) % MOD
            n1 = (M[1] + M[5] + M[9]) % MOD
            n2 = (M[2] + M[6] + M[10]) % MOD
            n3 = (M[3] + M[7] + M[11]) % MOD

            n4 = (M[0] + 2 * M[4] + M[8]) % MOD
            n5 = (M[1] + 2 * M[5] + M[9]) % MOD
            n6 = (M[2] + 2 * M[6] + M[10]) % MOD
            n7 = (M[3] + 2 * M[7] + M[11]) % MOD

            n8 = (M[0] + M[8] + M[12]) % MOD
            n9 = (M[1] + M[9] + M[13]) % MOD
            n10 = (M[2] + M[10] + M[14]) % MOD
            n11 = (M[3] + M[11] + M[15]) % MOD

            n12 = (M[0] + M[8] + 2 * M[12]) % MOD
            n13 = (M[1] + M[9] + 2 * M[13]) % MOD
            n14 = (M[2] + M[10] + 2 * M[14]) % MOD
            n15 = (M[3] + M[11] + 2 * M[15]) % MOD
        else:
            # unmarked position
            n0 = (M[0] + M[8]) % MOD
            n1 = (M[1] + M[9]) % MOD
            n2 = (M[2] + M[10]) % MOD
            n3 = (M[3] + M[11]) % MOD

            n4 = (M[0] + M[4] + M[8]) % MOD
            n5 = (M[1] + M[5] + M[9]) % MOD
            n6 = (M[2] + M[6] + M[10]) % MOD
            n7 = (M[3] + M[7] + M[11]) % MOD

            n8, n9, n10, n11 = n0, n1, n2, n3

            n12 = (M[0] + M[8] + M[12]) % MOD
            n13 = (M[1] + M[9] + M[13]) % MOD
            n14 = (M[2] + M[10] + M[14]) % MOD
            n15 = (M[3] + M[11] + M[15]) % MOD

        M2[0], M2[1], M2[2], M2[3] = n0, n1, n2, n3
        M2[4], M2[5], M2[6], M2[7] = n4, n5, n6, n7
        M2[8], M2[9], M2[10], M2[11] = n8, n9, n10, n11
        M2[12], M2[13], M2[14], M2[15] = n12, n13, n14, n15
        M, M2 = M2, M

        if s[i - 1] == ONE:
            Pre = Pre * inv2 % MOD

    # no forced position at all
    ans = (ans + pow(2, M_total, MOD)) % MOD
    print(ans)

if __name__ == "__main__":
    main()