import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    K = int(data[pos]); pos += 1
    A = sorted((int(x) for x in data[pos:pos+N]), reverse=True); pos += N
    B = sorted((int(x) for x in data[pos:pos+N]), reverse=True); pos += N
    C = sorted((int(x) for x in data[pos:pos+N]), reverse=True); pos += N

    N2 = N * N
    visited = set()
    visited.add(0)
    h = [(-(A[0]*B[0] + B[0]*C[0] + C[0]*A[0]), 0, 0, 0)]
    ans = 0
    for _ in range(K):
        negv, i, j, k = heapq.heappop(h)
        ans = -negv
        ai = A[i]; bj = B[j]; ck = C[k]
        if i + 1 < N:
            code = (i + 1) * N2 + j * N + k
            if code not in visited:
                visited.add(code)
                a1 = A[i + 1]
                heapq.heappush(h, (-(a1*bj + bj*ck + ck*a1), i + 1, j, k))
        if j + 1 < N:
            code = i * N2 + (j + 1) * N + k
            if code not in visited:
                visited.add(code)
                b1 = B[j + 1]
                heapq.heappush(h, (-(ai*b1 + b1*ck + ck*ai), i, j + 1, k))
        if k + 1 < N:
            code = i * N2 + j * N + (k + 1)
            if code not in visited:
                visited.add(code)
                c1 = C[k + 1]
                heapq.heappush(h, (-(ai*bj + bj*c1 + c1*ai), i, j, k + 1))
    sys.stdout.write(str(ans) + "\n")

main()