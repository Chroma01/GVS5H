import sys
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); X = int(data[1])
    groups = {1: [], 2: [], 3: []}
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((c, a))  # (calorie weight, vitamin value)

    # If any vitamin is missing, its intake stays 0 -> answer 0.
    for vit in (1, 2, 3):
        if not groups[vit]:
            print(0)
            return

    try:
        import numpy as np
        use_np = True
    except ImportError:
        use_np = False

    best = [None] * 4
    sums = [0] * 4

    if use_np:
        for vit in (1, 2, 3):
            arr = np.zeros(X + 1, dtype=np.int64)
            for (w, a) in groups[vit]:
                if w <= X:
                    cand = arr[:X + 1 - w] + a
                    np.maximum(arr[w:], cand, out=arr[w:])
            np.maximum.accumulate(arr, out=arr)
            best[vit] = arr
            sums[vit] = sum(a for (_, a) in groups[vit])
    else:
        for vit in (1, 2, 3):
            arr = [0] * (X + 1)
            for (w, a) in groups[vit]:
                for c in range(X, w - 1, -1):
                    v = arr[c - w] + a
                    if v > arr[c]:
                        arr[c] = v
            best[vit] = arr
            sums[vit] = sum(a for (_, a) in groups[vit])

    hi = min(sums[1], sums[2], sums[3])
    lo = 0
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        ok = True
        total = 0
        if use_np:
            for vit in (1, 2, 3):
                arr = best[vit]
                if int(arr[X]) < mid:
                    ok = False
                    break
                total += int(np.searchsorted(arr, mid, side='left'))
                if total > X:
                    ok = False
                    break
        else:
            for vit in (1, 2, 3):
                arr = best[vit]
                if arr[X] < mid:
                    ok = False
                    break
                total += bisect.bisect_left(arr, mid)
                if total > X:
                    ok = False
                    break
        if ok:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

main()