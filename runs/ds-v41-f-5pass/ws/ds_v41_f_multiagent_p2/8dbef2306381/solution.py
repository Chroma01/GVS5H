import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    ptr = 0
    N = int(data[ptr]); ptr += 1
    M = int(data[ptr]); ptr += 1
    A = int(data[ptr]); ptr += 1
    B = int(data[ptr]); ptr += 1

    # Merge adjacent (or touching) bad intervals into maximal bad blocks.
    blocks = []
    for _ in range(M):
        L = int(data[ptr]); ptr += 1
        R = int(data[ptr]); ptr += 1
        if blocks and L <= blocks[-1][1] + 1:
            if R > blocks[-1][1]:
                blocks[-1] = (blocks[-1][0], R)
        else:
            blocks.append((L, R))

    # Case A == B: fixed step, reachable squares are 1, 1+A, 1+2A, ...
    if A == B:
        if (N - 1) % A != 0:
            sys.stdout.write("No\n")
            return
        for L, R in blocks:
            x = L + ((1 - L) % A)   # smallest x >= L with x % A == 1
            if x <= R:
                sys.stdout.write("No\n")
                return
        sys.stdout.write("Yes\n")
        return

    # Case A < B.
    # A bad block of length >= B can never be jumped over.
    for L, R in blocks:
        if R - L + 1 >= B:
            sys.stdout.write("No\n")
            return

    full = (1 << B) - 1
    # bits A-1..B-1 : predecessors within allowed jump range
    maskA = ((1 << (B - A + 1)) - 1) << (A - 1)
    # If a good run is at least THRESH long, reachability saturates to all-ones
    # (from one reachable t, increments A and A+1 make all t+s, s >= A^2-A, reachable;
    #  first reachable t in a run is within B of its start).
    THRESH = A * A + 2 * B + 5

    reach = 1          # bit j = dp[current_pos - j]; start at position 1
    cur_pos = 2        # next position to process
    ok = True

    for L, R in blocks:
        # ---- good run [cur_pos, L-1] ----
        if cur_pos <= L - 1:
            if reach == 0:
                ok = False
                break
            length = (L - 1) - cur_pos + 1
            if length >= THRESH:
                reach = full
            else:
                cur = reach
                m = maskA
                f = full
                for _ in range(length):
                    if cur == f:
                        break
                    if cur & m:
                        cur = ((cur << 1) | 1) & f
                    else:
                        cur = (cur << 1) & f
                reach = cur
        # ---- bad block [L, R] : all zeros, just shift ----
        blen = R - L + 1
        reach = (reach << blen) & full
        cur_pos = R + 1
        if reach == 0:
            ok = False
            break

    # ---- trailing good run [cur_pos, N] ----
    if ok and cur_pos <= N:
        if reach == 0:
            ok = False
        else:
            length = N - cur_pos + 1
            if length >= THRESH:
                reach = full
            else:
                cur = reach
                m = maskA
                f = full
                for _ in range(length):
                    if cur == f:
                        break
                    if cur & m:
                        cur = ((cur << 1) | 1) & f
                    else:
                        cur = (cur << 1) & f
                reach = cur

    sys.stdout.write("Yes\n" if (ok and (reach & 1)) else "No\n")

main()