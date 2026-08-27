import sys
import heapq

def solve():
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

    # Best-first search over (i, j, k) with value A[i]*B[j] + B[j]*C[k] + C[k]*A[i].
    # All values positive => value is non-increasing as any index increases,
    # so a max-heap expansion from (0,0,0) pops values in descending order.
    start_val = A[0]*B[0] + B[0]*C[0] + C[0]*A[0]
    heap = [(-start_val, 0, 0, 0)]
    visited = set()
    visited.add(0)  # (0*N + 0)*N + 0

    push = heapq.heappush
    pop = heapq.heappop
    ans = 0
    for _ in range(K):
        negv, i, j, k = pop(heap)
        ans = -negv
        # neighbor (i+1, j, k)
        if i + 1 < N:
            code = ((i + 1) * N + j) * N + k
            if code not in visited:
                visited.add(code)
                a = A[i + 1]; b = B[j]; c = C[k]
                push(heap, (-(a*b + b*c + c*a), i + 1, j, k))
        # neighbor (i, j+1, k)
        if j + 1 < N:
            code = (i * N + (j + 1)) * N + k
            if code not in visited:
                visited.add(code)
                a = A[i]; b = B[j + 1]; c = C[k]
                push(heap, (-(a*b + b*c + c*a), i, j + 1, k))
        # neighbor (i, j, k+1)
        if k + 1 < N:
            code = (i * N + j) * N + (k + 1)
            if code not in visited:
                visited.add(code)
                a = A[i]; b = B[j]; c = C[k + 1]
                push(heap, (-(a*b + b*c + c*a), i, j, k + 1))

    sys.stdout.write(str(ans) + "\n")

solve()