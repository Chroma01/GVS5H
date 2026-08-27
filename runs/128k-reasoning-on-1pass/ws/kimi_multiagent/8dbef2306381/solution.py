import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[:4]
    intervals = []
    p = 4
    for _ in range(M):
        intervals.append((data[p], data[p + 1]))
        p += 2

    # Fixed step length: reachable squares are exactly 1, 1+d, 1+2d, ...
    if A == B:
        d = A
        if (N - 1) % d != 0:
            print("No")
            return

        residue = 1 % d
        for l, r in intervals:
            first = l + ((residue - l) % d)
            if first <= r:
                print("No")
                return

        print("Yes")
        return

    # Touching bad intervals form one contiguous bad block.
    blocks = []
    for l, r in intervals:
        if blocks and l <= blocks[-1][1] + 1:
            if r > blocks[-1][1]:
                blocks[-1][1] = r
        else:
            blocks.append([l, r])

    # A bad block of length B or more cannot be jumped over.
    for l, r in blocks:
        if r - l + 1 >= B:
            print("No")
            return

    diff = B - A

    # Sums of k jumps fill [kA, kB].  These intervals become contiguous
    # once k(B-A) >= A-1, so every offset >= T is representable.
    k0 = (A - 1 + diff - 1) // diff
    T = A * k0
    C = T + 2 * B

    # 1-based compressed board; index 0 is a dummy.
    bad = bytearray(1)
    prev = 1

    for l, r in blocks:
        gap_len = l - prev
        if gap_len > 0:
            kept = gap_len if gap_len <= C else C
            bad.extend(b"\x00" * kept)

        bad.extend(b"\x01" * (r - l + 1))
        prev = r + 1

    final_long = False
    final_start = -1
    final_gap_len = N - prev + 1

    if final_gap_len > C:
        final_long = True
        final_start = len(bad)  # First 1-based index of the final gap.
        bad.extend(b"\x00" * C)
    else:
        bad.extend(b"\x00" * final_gap_len)

    n = len(bad) - 1
    reachable = bytearray(n + 1)
    reachable[1] = 1

    # Number of reachable predecessors in [x-B, x-A].
    window_count = 0
    for x in range(2, n + 1):
        entering = x - A
        if entering >= 1:
            window_count += reachable[entering]

        leaving = x - B - 1
        if leaving >= 1:
            window_count -= reachable[leaving]

        if window_count > 0 and not bad[x]:
            reachable[x] = 1

    if final_long:
        # Any reachable square in the retained prefix implies an early entry
        # into the original final gap, from which N is certainly reachable.
        ok = any(reachable[final_start:])
    else:
        ok = reachable[n] != 0

    print("Yes" if ok else "No")


main()