import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))
    blocks = [(int(next(it)), int(next(it))) for _ in range(M)]

    out = sys.stdout

    if A == B:
        # Fixed step size A: path is forced to be 1, 1+A, 1+2A, ...
        if (N - 1) % A != 0:
            out.write("No\n")
            return
        for (L, R) in blocks:
            # smallest position >= L of the form 1 + k*A
            k = (L - 1 + A - 1) // A  # ceil((L-1)/A), L > 1 so k >= 1
            if 1 + k * A <= R:
                out.write("No\n")
                return
        out.write("Yes\n")
        return

    # A < B: sliding window DP.
    # bits: bit k (0-indexed) = reachability of position (cur - k), k = 0..B-1.
    # Invariant: we know exact reachability for the window (cur-B, cur].
    LIMIT = B * B + B          # free-run length guaranteeing saturation
    bmask = (1 << B) - 1
    wmask = (1 << (B - A + 1)) - 1
    shift = A - 1

    cur = 1
    bits = 1  # position 1 is reachable

    def advance(target):
        # All positions in (cur, target] are free; target >= cur.
        # Returns False iff nothing can be reachable beyond cur.
        nonlocal cur, bits
        d = target - cur
        if d <= 0:
            return True
        if d > LIMIT:
            if bits == 0:
                return False
            # Saturation: from any reachable x in the window, position x+B is
            # reachable (one jump), and from a point p0 > cur the reachable set
            # after t steps is the full interval [p0+t*A, p0+t*B]; it contains B
            # consecutive positions within distance <= B*B, after which every
            # free position is reachable.  d > B*B + B guarantees room.
            bits = bmask
            cur = target
            return True
        for _ in range(d):
            r = 1 if ((bits >> shift) & wmask) else 0
            bits = ((bits << 1) | r) & bmask
        cur = target
        return True

    ok = True
    for (L, R) in blocks:
        # Free segment up to the square just before the block.
        if not advance(L - 1):
            ok = False
            break
        # Cross the blocked segment: positions L..R become unreachable.
        # new bit k = old bit (k - (R - L + 1)); low bits become 0.
        s = R - L + 1
        if s >= B:
            bits = 0
        else:
            bits = (bits << s) & bmask
        cur = R

    if ok:
        ok = advance(N)

    out.write("Yes\n" if (ok and (bits & 1)) else "No\n")

main()