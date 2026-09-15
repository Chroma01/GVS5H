import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    A = data[1:1 + n]
    del data

    if n == 0:
        print(0)
        return

    sum_a = sum(A)
    total = (n + 1) * sum_a
    max_a = max(A)

    # Maximum possible pair sum is 2 * max_a.
    K = (2 * max_a).bit_length() - 1
    ans = total

    # For the packed dictionary:
    # value = count * INC + sum_of_values_in_residue.
    # INC is larger than any possible residue sum, so no carry into count.
    shift = sum_a.bit_length()
    if shift == 0:
        shift = 1
    inc = 1 << shift
    sum_mask = inc - 1

    arr = A
    limit = 4 * n  # use arrays while the modulus is not too large

    for k in range(1, K + 1):
        M = 1 << k
        mask = M - 1
        D = 0

        if M <= limit:
            cnt = [0] * M
            sm = [0] * M

            cnt_l = cnt
            sm_l = sm
            mask_l = mask

            for a in arr:
                r = a & mask_l
                cnt_l[r] += 1
                sm_l[r] += a

            half = M >> 1

            # Residue 0 is self-complementary.
            c = cnt_l[0]
            if c:
                D += (c + 1) * sm_l[0]

            # Cross complementary residues r and M-r, for 0 < r < M/2.
            for r in range(1, half):
                c = cnt_l[r]
                if c:
                    cr = M - r
                    c2 = cnt_l[cr]
                    if c2:
                        D += c * sm_l[cr] + c2 * sm_l[r]

            # Residue M/2 is self-complementary.
            c = cnt_l[half]
            if c:
                D += (c + 1) * sm_l[half]

        else:
            groups = {}
            get = groups.get
            inc_l = inc
            mask_l = mask

            for a in arr:
                r = a & mask_l
                groups[r] = get(r, 0) + inc_l + a

            half = M >> 1
            get2 = groups.get
            shift_l = shift
            sum_mask_l = sum_mask

            for r, v in groups.items():
                if r == 0:
                    c = v >> shift_l
                    s = v & sum_mask_l
                    D += (c + 1) * s
                elif r < half:
                    v2 = get2(M - r)
                    if v2 is not None:
                        c = v >> shift_l
                        s = v & sum_mask_l
                        c2 = v2 >> shift_l
                        s2 = v2 & sum_mask_l
                        D += c * s2 + c2 * s
                elif r == half:
                    c = v >> shift_l
                    s = v & sum_mask_l
                    D += (c + 1) * s

        ans -= D >> k

        # If no pair sum is divisible by 2^k, no larger power can divide one.
        if D == 0:
            break

    print(ans)


if __name__ == "__main__":
    solve()