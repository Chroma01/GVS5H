import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    A = sorted((int(x) for x in data[idx:idx+N]), reverse=True); idx += N
    B = sorted((int(x) for x in data[idx:idx+N]), reverse=True); idx += N
    C = sorted((int(x) for x in data[idx:idx+N]), reverse=True); idx += N

    def val(i, j, k):
        return A[i]*B[j] + B[j]*C[k] + C[k]*A[i]

    # Max-heap via negated values. Entries: (-value, i, j, k)
    heap = [(-val(0, 0, 0), 0, 0, 0)]
    visited = {(0, 0, 0)}
    ans = 0
    for _ in range(K):
        negv, i, j, k = heapq.heappop(heap)
        ans = -negv
        if i + 1 < N and (i+1, j, k) not in visited:
            visited.add((i+1, j, k))
            heapq.heappush(heap, (-val(i+1, j, k), i+1, j, k))
        if j + 1 < N and (i, j+1, k) not in visited:
            visited.add((i, j+1, k))
            heapq.heappush(heap, (-val(i, j+1, k), i, j+1, k))
        if k + 1 < N and (i, j, k+1) not in visited:
            visited.add((i, j, k+1))
            heapq.heappush(heap, (-val(i, j, k+1), i, j, k+1))
    sys.stdout.write(str(ans) + "\n")

main()