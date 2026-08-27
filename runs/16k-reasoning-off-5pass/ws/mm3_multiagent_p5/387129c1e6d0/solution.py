import sys
import threading
from collections import defaultdict
import bisect

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    try:
        N = int(next(it))
    except StopIteration:
        return
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))
    
    xmap = defaultdict(list)  # x -> list of y
    ymap = defaultdict(list)  # y -> list of x
    # Read houses
    for _ in range(N):
        hx = int(next(it))
        hy = int(next(it))
        xmap[hx].append(hy)
        ymap[hy].append(hx)
    
    # Sort each list
    for lst in xmap.values():
        lst.sort()
    for lst in ymap.values():
        lst.sort()
    
    cx, cy = Sx, Sy
    count = 0
    
    for _ in range(M):
        d = next(it)
        c = int(next(it))
        if d == 'U':
            ny = cy + c
            nx = cx
            lo, hi = cy, ny
            lst = xmap.get(cx)
            if lst is not None:
                i = bisect.bisect_left(lst, lo)
                j = bisect.bisect_right(lst, hi)
                if i < j:
                    matched = lst[i:j]
                    count += len(matched)
                    # Remove matched y's from xmap[cx]
                    if i == 0 and j == len(lst):
                        del xmap[cx]
                    else:
                        del xmap[cx][i:j]
                    # Remove cx from ymap[hy] for each hy in matched
                    for hy in matched:
                        lst2 = ymap.get(hy)
                        if lst2 is not None:
                            k = bisect.bisect_left(lst2, cx)
                            if k < len(lst2) and lst2[k] == cx:
                                if len(lst2) == 1:
                                    del ymap[hy]
                                else:
                                    del lst2[k]
            cy = ny
        elif d == 'D':
            ny = cy - c
            nx = cx
            lo, hi = ny, cy
            lst = xmap.get(cx)
            if lst is not None:
                i = bisect.bisect_left(lst, lo)
                j = bisect.bisect_right(lst, hi)
                if i < j:
                    matched = lst[i:j]
                    count += len(matched)
                    if i == 0 and j == len(lst):
                        del xmap[cx]
                    else:
                        del xmap[cx][i:j]
                    for hy in matched:
                        lst2 = ymap.get(hy)
                        if lst2 is not None:
                            k = bisect.bisect_left(lst2, cx)
                            if k < len(lst2) and lst2[k] == cx:
                                if len(lst2) == 1:
                                    del ymap[hy]
                                else:
                                    del lst2[k]
            cy = ny
        elif d == 'L':
            nx = cx - c
            ny = cy
            lo, hi = nx, cx
            lst = ymap.get(cy)
            if lst is not None:
                i = bisect.bisect_left(lst, lo)
                j = bisect.bisect_right(lst, hi)
                if i < j:
                    matched = lst[i:j]
                    count += len(matched)
                    if i == 0 and j == len(lst):
                        del ymap[cy]
                    else:
                        del ymap[cy][i:j]
                    for hx in matched:
                        lst2 = xmap.get(hx)
                        if lst2 is not None:
                            k = bisect.bisect_left(lst2, cy)
                            if k < len(lst2) and lst2[k] == cy:
                                if len(lst2) == 1:
                                    del xmap[hx]
                                else:
                                    del lst2[k]
            cx = nx
        elif d == 'R':
            nx = cx + c
            ny = cy
            lo, hi = cx, nx
            lst = ymap.get(cy)
            if lst is not None:
                i = bisect.bisect_left(lst, lo)
                j = bisect.bisect_right(lst, hi)
                if i < j:
                    matched = lst[i:j]
                    count += len(matched)
                    if i == 0 and j == len(lst):
                        del ymap[cy]
                    else:
                        del ymap[cy][i:j]
                    for hx in matched:
                        lst2 = xmap.get(hx)
                        if lst2 is not None:
                            k = bisect.bisect_left(lst2, cy)
                            if k < len(lst2) and lst2[k] == cy:
                                if len(lst2) == 1:
                                    del xmap[hx]
                                else:
                                    del lst2[k]
            cx = nx
    
    print(f"{cx} {cy} {count}")

def main():
    solve()

if __name__ == "__main__":
    main()