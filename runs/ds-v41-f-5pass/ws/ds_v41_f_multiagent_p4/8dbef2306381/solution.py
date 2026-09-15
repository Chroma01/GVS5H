import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0]); M = int(data[1]); A = int(data[2]); B = int(data[3])

    # Merge touching/overlapping bad intervals into maximal bad blocks.
    merged = []
    idx = 4
    for _ in range(M):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        if merged and L <= merged[-1][1] + 1:
            if R > merged[-1][1]:
                merged[-1] = (merged[-1][0], R)
        else:
            merged.append((L, R))

    # Case A == B: the path is forced.
    if A == B:
        if (N - 1) % A != 0:
            sys.stdout.write("No\n"); return
        K = (N - 1) // A
        for L, R in merged:
            klo = (L - 1 + A - 1) // A   # smallest k with 1+k*A >= L
            khi = (R - 1) // A           # largest  k with 1+k*A <= R
            if klo <= khi:               # some forced square is bad
                sys.stdout.write("No\n"); return
        sys.stdout.write("Yes\n"); return

    # Case A < B: a maximal bad block of length >= B cannot be crossed.
    for L, R in merged:
        if R - L + 1 >= B:
            sys.stdout.write("No\n"); return

    full = (1 << B) - 1
    band = ((1 << (B - A + 1)) - 1) << (A - 1)   # bits [A-1, B-1]
    T = A * A + B + 5                            # safe saturation bound

    mask = 1   # bit 0 = current square reachable
    x = 1
    ok = True

    for L, R in merged:
        g = L - 1 - x            # all-good squares x+1 .. L-1
        if g > 0:
            if mask == 0:
                ok = False; break
            if g >= T:
                mask = full      # all-ones is a fixed point
            else:
                for _ in range(g):
                    if mask == full:
                        break
                    if mask & band:
                        mask = ((mask << 1) | 1) & full
                    else:
                        mask = (mask << 1) & full
            x = L - 1
        b = R - L + 1            # bad block: new bits forced to 0
        mask = (mask << b) & full
        if mask == 0:
            ok = False; break
        x = R

    if ok:
        g = N - x
        if g > 0:
            if mask == 0:
                ok = False
            elif g >= T:
                mask = full
            else:
                for _ in range(g):
                    if mask == full:
                        break
                    if mask & band:
                        mask = ((mask << 1) | 1) & full
                    else:
                        mask = (mask << 1) & full
        if ok:
            ok = (mask & 1) == 1

    sys.stdout.write("Yes\n" if ok else "No\n")

main()