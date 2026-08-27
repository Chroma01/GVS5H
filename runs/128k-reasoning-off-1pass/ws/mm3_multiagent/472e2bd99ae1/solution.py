import sys
import heapq
from bisect import bisect_left

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]

    # sort A and B descending to enable efficient enumeration of largest products
    A.sort(reverse=True)
    B.sort(reverse=True)
    # C sorted ascending for binary search (lower bound)
    C.sort()

    # ---- enumerate K largest products A[i] * B[j] ----
    pairs = []                     # (base, a, bj)
    # max-heap via negative values
    heap = [(-(A[0] * B[0]), 0, 0)]
    visited = {(0, 0)}
    needed = K
    while needed > 0 and heap:
        neg_val, i, j = heapq.heappop(heap)
        val = -neg_val
        a = A[i]
        bj = B[j]
        pairs.append((val, a, bj))
        # move down in A (i+1, j)
        ni = i + 1
        if ni < N and (ni, j) not in visited:
            heapq.heappush(heap, (-(A[ni] * B[j]), ni, j))
            visited.add((ni, j))
        # move right in B (i, j+1)
        nj = j + 1
        if nj < N and (i, nj) not in visited:
            heapq.heappush(heap, (-(A[i] * B[nj]), i, nj))
            visited.add((i, nj))
        needed -= 1

    # ---- binary search on answer ----
    # upper bound: max possible value
    max_val = A[0] * B[0] + B[0] * C[-1] + C[-1] * A[0]
    lo = 0
    hi = max_val
    C_list = C
    N_val = N
    pair_list = pairs
    K_limit = K

    while lo < hi:
        mid = (lo + hi + 1) // 2
        cnt = 0
        for base, a, bj in pair_list:
            if cnt >= K_limit:
                break
            if mid <= base:
                cnt += N_val
                continue
            need = mid - base
            denom = a + bj
            # ceil division: smallest C_k with C_k * denom >= need
            t = need // denom
            if need % denom != 0:
                t += 1
            idx = bisect_left(C_list, t)
            cnt += N_val - idx
            if cnt >= K_limit:
                break
        if cnt >= K_limit:
            lo = mid
        else:
            hi = mid - 1

    print(lo)

if __name__ == "__main__":
    solve()