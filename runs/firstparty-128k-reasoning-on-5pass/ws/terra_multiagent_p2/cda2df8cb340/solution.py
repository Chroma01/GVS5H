import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]
    
    total = sum(a)
    answer = (n + 1) * total

    max_k = (2 * max(a)).bit_length() - 1

    for k in range(1, max_k + 1):
        mask = (1 << k) - 1
        cnt = {}
        sm = {}

        for x in a:
            r = x & mask
            cnt[r] = cnt.get(r, 0) + 1
            sm[r] = sm.get(r, 0) + x

        divisible_sum = 0

        for r, c in cnt.items():
            q = (-r) & mask
            if r > q:
                continue

            cq = cnt.get(q, 0)
            if cq == 0:
                continue

            if r == q:
                # All unordered pairs i <= j inside this bucket.
                # Each value appears in exactly c + 1 pair sums.
                divisible_sum += (c + 1) * sm[r]
            else:
                # Every element of one bucket pairs with every element
                # of the complementary residue bucket.
                divisible_sum += sm[r] * cq + c * sm[q]

        answer -= divisible_sum >> k

    print(answer)

if __name__ == "__main__":
    solve()