import sys
from collections import Counter

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]

    af = [x for x in A if x != -1]
    bf = [x for x in B if x != -1]

    pa = len(af)
    pb = len(bf)
    wa = n - pa
    wb = n - pb

    # Required number of fixed-A/fixed-B complementary matches.
    need = max(0, pa - wb, pb - wa)

    if need == 0:
        print("Yes")
        return

    if not af or not bf or need > min(pa, pb):
        print("No")
        return

    lower = max(max(af), max(bf))

    # If only one complementary fixed pair is needed, no enumeration is needed.
    if need == 1:
        if max(af) + max(bf) >= lower:
            print("Yes")
        else:
            print("No")
        return

    ca = Counter(af)
    cb = Counter(bf)
    ai = list(ca.items())
    bi = list(cb.items())

    # Encode (sum, contribution) into one integer.
    # contribution = min(countA[x], countB[y]) <= N <= 2000.
    SHIFT = 11
    MASK = (1 << SHIFT) - 1
    encoded = []

    for x, cx in ai:
        for y, cy in bi:
            s = x + y
            if s >= lower:
                w = cx if cx < cy else cy
                encoded.append((s << SHIFT) | w)

    if not encoded:
        print("No")
        return

    encoded.sort()

    current_sum = -1
    matched = 0

    for z in encoded:
        s = z >> SHIFT
        w = z & MASK
        if s != current_sum:
            if matched >= need:
                print("Yes")
                return
            current_sum = s
            matched = w
        else:
            matched += w

    print("Yes" if matched >= need else "No")


if __name__ == "__main__":
    solve()