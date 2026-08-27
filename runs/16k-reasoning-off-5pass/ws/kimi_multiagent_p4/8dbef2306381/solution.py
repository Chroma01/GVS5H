import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))
    intervals = [(int(next(it)), int(next(it))) for _ in range(M)]

    full = (1 << B) - 1
    # mask bit j (0-indexed) = reachability of position (cur - j), for j in 0..B-1
    cur = 1
    mask = 1  # position 1 is reachable

    # predecessor bits for a good square: bits A-1 .. B-1 of the mask
    pred_mask = ((1 << (B - A + 1)) - 1) << (A - 1)

    dead = False

    def advance(T):
        # advance cur to T through all-good squares; False if reachability dies
        nonlocal cur, mask
        seen = {}
        while cur < T:
            if mask == 0:
                return False
            if mask == full:
                cur = T
                return True
            rem = T - cur
            prev = seen.get(mask)
            if prev is not None:
                cycle = prev - rem  # > 0
                rem %= cycle
                cur = T - rem
                seen.clear()
                continue
            seen[mask] = rem
            newbit = 1 if (mask & pred_mask) else 0
            mask = ((mask << 1) | newbit) & full
            cur += 1
        return True

    for (L, R) in intervals:
        if not advance(L - 1):
            dead = True
            break
        length = R - L + 1
        if length >= B:
            dead = True
            break
        mask = (mask << length) & full
        cur = R
        if mask == 0:
            dead = True
            break

    if not dead:
        if not advance(N):
            dead = True

    if dead or not (mask & 1):
        sys.stdout.write("No\n")
    else:
        sys.stdout.write("Yes\n")

solve()