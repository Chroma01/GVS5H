import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))
    bad = []
    for _ in range(M):
        L = int(next(it))
        R = int(next(it))
        bad.append((L, R))

    # Build good intervals: gaps between bad intervals and from 1 to first bad, and last bad to N.
    good = []
    prev_end = 1
    for (l, r) in bad:
        if l > prev_end:
            good.append((prev_end, l - 1))
        prev_end = r + 1
    if prev_end <= N:
        good.append((prev_end, N))

    # BFS / interval expansion
    curL, curR = 1, 1
    idx = 0
    n_good = len(good)
    # Find first good interval that starts within reachable + A
    # curR=1, we need intervals with l <= curR + A = 1 + A
    while idx < n_good:
        l, r = good[idx]
        if l > curR + A:
            break
        # This interval is reachable; extend curR to max(curR, r)
        if r > curR:
            curR = r
        idx += 1
        # After extending, maybe more intervals become reachable, so loop continues.
        if curR >= N:
            print("Yes")
            return

    # Check if we can reach N through further expansion? The while loop already exhausted.
    # However, we need to continue: maybe after consuming some intervals, curR grew enough to reach next intervals.
    # The while loop handles that because it checks condition with updated curR each iteration.
    # But we only processed intervals sequentially; we need to keep going while intervals are reachable.
    # Let's restructure: use a while True with index advancing.
    # Actually the loop above already does: each iteration checks the NEXT interval (by index) and if reachable, extends.
    # After extension, we don't re-check previous intervals (already consumed). The loop continues to next.
    # This is correct: we process intervals in order, each at most once.
    # So if loop ends, no more intervals are reachable.

    if curR >= N:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()