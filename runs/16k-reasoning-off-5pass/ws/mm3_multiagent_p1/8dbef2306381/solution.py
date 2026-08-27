import sys
from collections import deque
import bisect

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))
    bad_intervals = []
    for _ in range(M):
        L = int(next(it))
        R = int(next(it))
        bad_intervals.append((L, R))

    # Build good segments: intervals of non-bad squares.
    # Bad intervals are disjoint and sorted, L_i > 1, R_i < N.
    good_segments = []
    cur = 1
    for L, R in bad_intervals:
        if cur <= L - 1:
            good_segments.append((cur, L - 1))
        cur = R + 1
    if cur <= N:
        good_segments.append((cur, N))

    # If no good segments? Should not happen because 1 is not bad.
    if not good_segments:
        print("No")
        return

    # Find the segment containing square 1.
    # Since 1 is not bad, it's in the first good segment.
    start_idx = 0  # by construction
    # Segment containing N is the last one (or also find via bisect if needed)
    # We'll check containment during BFS.

    num_segments = len(good_segments)
    visited = [False] * num_segments
    q = deque()
    q.append(start_idx)
    visited[start_idx] = True

    # Precompute left endpoints for bisect
    lefts = [seg[0] for seg in good_segments]

    while q:
        idx = q.popleft()
        l, r = good_segments[idx]
        # If this segment contains N, we can reach N
        if l <= N <= r:
            print("Yes")
            return
        # Try all step sizes
        for step in range(A, B + 1):
            new_l = l + step
            new_r = r + step
            if new_l > N:
                # All further steps will be even larger, break? No, steps increase, new_l only gets larger.
                # But we are iterating step in increasing order; if new_l > N, we can break.
                # However, we are inside a for loop over step; breaking here only breaks the for loop.
                break
            # Find the first segment with right endpoint >= new_l
            # Use bisect_right on lefts to find index where lefts[j] > new_l, then j-1 is candidate.
            j = bisect.bisect_right(lefts, new_l) - 1
            if j < 0:
                continue
            # Actually we need the first segment whose right >= new_l.
            # bisect_right on lefts gives first left > new_l. The segment at j has left <= new_l.
            # We must check if good_segments[j][1] >= new_l.
            # If not, we might need to check j+1? But j+1's left > new_l, so its right could still be >= new_l if it overlaps? Wait, segments are disjoint. If j's right < new_l, then j+1's left > new_l >= j's right+1, so j+1's left > new_l, meaning j+1's right >= j+1's left > new_l, so it could overlap? Actually if j's right < new_l, then j+1's left > new_l, so the interval [new_l, new_r] starts after j ends. It could overlap j+1 if new_l <= j+1's right. But since j+1's left > new_l, we need to check j+1. So we should start from j and move forward while left <= new_r.
            # Simpler: iterate from j onwards while left <= new_r.
            k = j
            while k < num_segments and good_segments[k][0] <= new_r:
                seg_l, seg_r = good_segments[k]
                # Check if this segment intersects [new_l, new_r]
                if seg_r >= new_l:  # this is equivalent to seg_l <= new_r and seg_r >= new_l
                    if not visited[k]:
                        visited[k] = True
                        q.append(k)
                k += 1

    print("No")

if __name__ == "__main__":
    solve()