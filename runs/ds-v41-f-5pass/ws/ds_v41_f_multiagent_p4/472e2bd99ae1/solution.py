import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2+N]))
    B = list(map(int, data[2+N:2+2*N]))
    C = list(map(int, data[2+2*N:2+3*N]))
    
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    
    A2 = [a*a for a in A]
    N2 = N * N
    SHIFT = 54
    BASE = 1 << SHIFT
    
    val0 = (A[0] + B[0]) * (A[0] + C[0]) - A2[0]
    heap = [(-val0) * BASE]
    visited = {0}
    push = heapq.heappush
    pop = heapq.heappop
    
    for pop_cnt in range(K):
        key = pop(heap)
        if pop_cnt == K - 1:
            sys.stdout.write(str(- (key // BASE)) + '\n')
            return
        code = key % BASE
        i, rem = divmod(code, N2)
        j, k = divmod(rem, N)
        
        ni = i + 1
        if ni < N:
            ncode = ni * N2 + j * N + k
            if ncode not in visited:
                visited.add(ncode)
                val = (A[ni] + B[j]) * (A[ni] + C[k]) - A2[ni]
                push(heap, (-val) * BASE + ncode)
        nj = j + 1
        if nj < N:
            ncode = i * N2 + nj * N + k
            if ncode not in visited:
                visited.add(ncode)
                val = (A[i] + B[nj]) * (A[i] + C[k]) - A2[i]
                push(heap, (-val) * BASE + ncode)
        nk = k + 1
        if nk < N:
            ncode = i * N2 + j * N + nk
            if ncode not in visited:
                visited.add(ncode)
                val = (A[i] + B[j]) * (A[i] + C[nk]) - A2[i]
                push(heap, (-val) * BASE + ncode)

if __name__ == "__main__":
    solve()