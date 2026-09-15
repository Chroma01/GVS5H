import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    N = int(data[ptr]); ptr += 1
    M = int(data[ptr]); ptr += 1
    A = int(data[ptr]); ptr += 1
    B = int(data[ptr]); ptr += 1
    Ls = [0] * M
    Rs = [0] * M
    for i in range(M):
        Ls[i] = int(data[ptr]); ptr += 1
        Rs[i] = int(data[ptr]); ptr += 1

    # A bad interval of length >= B is an impassable wall:
    # any jump from p <= L-1 lands at p+k <= L-1+B <= R.
    for i in range(M):
        if Rs[i] - Ls[i] + 1 >= B:
            sys.stdout.write("No\n")
            return

    full = (1 << B) - 1
    if A == B:
        RMASK = 1 << (A - 1)
    else:
        RMASK = full ^ ((1 << (A - 1)) - 1)

    # Sufficient number of good steps for the B-bit window to become full.
    C = A * A + 2 * B + 10

    def advance(mask, length):
        # advance `length` good squares; mask bit k = reach(p-k) after position p
        if length <= 0 or mask == 0:
            return mask
        if A == B:
            # T is a cyclic left rotation of the B bits
            s = length % B
            if s:
                mask = ((mask << s) | (mask >> (B - s))) & full
            return mask
        # A < B : T(mask) = ((mask<<1) | b) & full, b = 1 if mask & RMASK
        rm = RMASK
        fl = full
        steps = C if length > C else length
        cnt = 0
        while cnt < steps:
            if mask & rm:
                mask = ((mask << 1) | 1) & fl
            else:
                mask = (mask << 1) & fl
            cnt += 1
            if mask == fl or mask == 0:
                return mask
        if length > C:
            return fl if mask else 0
        return mask

    mask = 1  # square 1 reachable
    if M == 0:
        mask = advance(mask, N - 1)
    else:
        mask = advance(mask, Ls[0] - 2)
        for i in range(M):
            bl = Rs[i] - Ls[i] + 1
            mask = (mask << bl) & full            # bad block: no new reachability
            if mask == 0:
                break
            if i + 1 < M:
                nl = Ls[i + 1] - 1 - Rs[i]
            else:
                nl = N - Rs[i]
            mask = advance(mask, nl)
            if mask == 0:
                break

    sys.stdout.write("Yes\n" if (mask & 1) else "No\n")

main()