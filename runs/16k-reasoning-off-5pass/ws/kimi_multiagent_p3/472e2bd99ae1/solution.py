import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    K = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos+N]]; pos += N
    B = [int(x) for x in data[pos:pos+N]]; pos += N
    C = [int(x) for x in data[pos:pos+N]]; pos += N

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    def val(i, j, k):
        return A[i]*B[j] + B[j]*C[k] + C[k]*A[i]

    # Max-heap via negated values. Each entry: (-value, i, j, k)
    heap = [(-val(0, 0, 0), 0, 0, 0)]
    visited = {(0, 0, 0)}

    ans = 0
    for _ in range(K):
        negv, i, j, k = heapq.heappop(heap)
        ans = -negv
        # neighbors: increment one index (arrays sorted descending => values nonincreasing)
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