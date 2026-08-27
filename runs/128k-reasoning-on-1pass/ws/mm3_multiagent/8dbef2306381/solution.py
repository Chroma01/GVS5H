import sys
from array import array

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))

    bad = [(int(next(it)), int(next(it))) for _ in range(M)]

    # Build alternating safe / bad intervals
    intervals = []                     # each element: ('safe', L, R) or ('bad', L, R)
    prev_end = 0
    for L, R in bad:
        safe_start = prev_end + 1
        safe_end = L - 1
        if safe_start <= safe_end:
            intervals.append(('safe', safe_start, safe_end))
        intervals.append(('bad', L, R))
        prev_end = R
    # final safe part (guaranteed non‑empty)
    safe_start = prev_end + 1
    safe_end = N
    if safe_start <= safe_end:
        intervals.append(('safe', safe_start, safe_end))

    # ----- pre‑compute transition tables for safe steps (binary lifting) -----
    ALL_BITS = (1 << B) - 1
    RANGE_MASK = (1 << (B - A + 1)) - 1          # bits (A‑1) … (B‑1)

    # one safe step
    def trans_good(mask: int) -> int:
        new_bit = 1 if ((mask >> (A - 1)) & RANGE_MASK) else 0
        return ((mask << 1) & ALL_BITS) | new_bit

    LOG = (N).bit_length()          # ≤ 40 for N ≤ 10^12
    size = 1 << B                   # number of possible masks (≤ 1 048 576)

    # level 0 : 1 step
    nxt0 = array('I', (trans_good(m) for m in range(size)))
    nxt = [nxt0]

    # higher levels : 2^k steps
    for _ in range(1, LOG):
        prev = nxt[-1]
        cur = array('I', (prev[prev[m]] for m in range(size)))
        nxt.append(cur)

    # apply t safe steps using binary lifting
    def apply_good_steps(state: int, steps: int) -> int:
        bit = 0
        while steps:
            if steps & 1:
                state = nxt[bit][state]
            steps >>= 1
            bit += 1
        return state

    # ----- walk through the intervals -----
    cur_pos = 1               # last processed square
    cur_mask = 1              # only square 1 is reachable (bit0 = 1)

    for typ, L, R in intervals:
        if typ == 'safe':
            steps = R - cur_pos
            if steps > 0:
                cur_mask = apply_good_steps(cur_mask, steps)
                cur_pos = R
                if cur_mask == 0 and cur_pos != N:
                    print('No')
                    return
        else:  # bad interval
            length = R - L + 1
            if length >= B:
                cur_mask = 0
            else:
                cur_mask = (cur_mask << length) & ALL_BITS
            cur_pos = R
            if cur_mask == 0 and cur_pos != N:
                print('No')
                return

    # after the loop cur_pos == N
    print('Yes' if (cur_mask & 1) else 'No')


if __name__ == "__main__":
    solve()