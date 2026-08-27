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

    # f(i,j,k) = A_i*B_j + B_j*C_k + C_k*A_i is strictly increasing in each of
    # A_i, B_j, C_k (partial derivatives B_j+C_k, A_i+C_k, A_i+B_j are all > 0).
    # After sorting descending, f is monotone nonincreasing in each index, so
    # best-first search over the grid from (0,0,0) enumerates values in
    # nonincreasing order.
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # Within K pops, any index reached is at most K-1 (indices grow by 1 per
    # expansion from the origin), so capping at top-K elements is safe.
    if N > K:
        A = A[:K]
        B = B[:K]
        C = C[:K]
        n = K
    else:
        n = N

    nn = n * n
    visited = set()
    visited.add(0)
    h = [(-(A[0]*B[0] + B[0]*C[0] + C[0]*A[0]), 0, 0, 0)]
    ans = 0
    for _ in range(K):
        negv, i, j, k = heapq.heappop(h)
        ans = -negv
        ni = i + 1
        if ni < n:
            code = ni * nn + j * n + k
            if code not in visited:
                visited.add(code)
                heapq.heappush(h, (-(A[ni]*B[j] + B[j]*C[k] + C[k]*A[ni]), ni, j, k))
        nj = j + 1
        if nj < n:
            code = i * nn + nj * n + k
            if code not in visited:
                visited.add(code)
                heapq.heappush(h, (-(A[i]*B[nj] + B[nj]*C[k] + C[k]*A[i]), i, nj, k))
        nk = k + 1
        if nk < n:
            code = i * nn + j * n + nk
            if code not in visited:
                visited.add(code)
                heapq.heappush(h, (-(A[i]*B[j] + B[j]*C[nk] + C[nk]*A[i]), i, j, nk))
    sys.stdout.write(str(ans) + "\n")

main()