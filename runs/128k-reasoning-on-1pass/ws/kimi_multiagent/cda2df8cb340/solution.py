import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    total = sum(A)
    # P0 = sum_{i<=j} (A_i + A_j) = (N+1) * sum(A)
    ans = (n + 1) * total

    max_sum = 2 * max(A)  # A_i + A_j <= max_sum, so 2^k > max_sum contributes nothing

    k = 1
    while (1 << k) <= max_sum:
        M = 1 << k
        mask = M - 1
        cnt = {}
        sm = {}
        for v in A:
            r = v & mask
            if r in cnt:
                cnt[r] += 1
                sm[r] += v
            else:
                cnt[r] = 1
                sm[r] = v

        Pk = 0
        for r, c in cnt.items():
            comp = (-r) & mask
            if comp < r:
                continue  # already handled as the complementary pair
            s = sm[r]
            if comp == r:
                # self-complementary class: sum_{i<=j in class} (v_i + v_j)
                Pk += (c + 1) * s
            else:
                cc = cnt.get(comp)
                if cc is not None:
                    Pk += c * sm[comp] + cc * s

        # Pk is exactly divisible by 2^k (each included sum is), so shift is exact
        ans -= Pk >> k
        k += 1

    print(ans)

main()