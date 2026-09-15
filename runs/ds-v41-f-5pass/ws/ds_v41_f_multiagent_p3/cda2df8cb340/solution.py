import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # S0 = sum over all ordered pairs (i,j) of (A_i + A_j)
    S0 = 2 * n * sum(A)

    # D = sum_i f(A_i + A_i) = sum_i odd_part(2*A_i) = sum_i odd_part(A_i)
    D = 0
    for a in A:
        # v2(a) = (a & -a).bit_length() - 1
        D += a >> ((a & -a).bit_length() - 1)

    # Maximum possible sum is 2 * max(A)
    max_sum = 2 * max(A)
    # Largest t such that 2^t <= max_sum
    K = max_sum.bit_length() - 1

    total_sub = 0

    for t in range(1, K + 1):
        mask = (1 << t) - 1
        cnt = {}
        sm = {}

        # Group elements by residue modulo 2^t
        for a in A:
            r = a & mask
            if r in cnt:
                cnt[r] += 1
                sm[r] += a
            else:
                cnt[r] = 1
                sm[r] = a

        # S_t = sum of (A_i + A_j) over ordered pairs with 2^t | (A_i + A_j)
        St = 0
        for r, c in cnt.items():
            s = (-r) & mask
            cs = cnt.get(s)
            if cs is not None:
                sr = sm[r]
                ss = sm[s]
                St += cs * sr + c * ss

        total_sub += St >> t  # S_t is divisible by 2^t

    ans = (S0 + D - total_sub) // 2
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()