import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2 + N]))
    B = list(map(int, data[2 + N:2 + 2 * N]))
    C = list(map(int, data[2 + 2 * N:2 + 3 * N]))

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]
    root_val = a0 * b0 + b0 * c0 + c0 * a0

    # Pack (value, i, j, k) into a single integer.
    # value < 3e18 < 2^62, and each index < 2^20.
    heap = [-(root_val << 60)]  # i = j = k = 0

    heappop = heapq.heappop
    heappush = heapq.heappush

    for cnt in range(1, K + 1):
        x = heappop(heap)
        key = -x
        val = key >> 60
        if cnt == K:
            sys.stdout.write(str(val) + "\n")
            return

        i = (key >> 40) & 0xFFFFF
        j = (key >> 20) & 0xFFFFF
        k = key & 0xFFFFF

        b = B[j]
        c = C[k]

        # child (i+1, j, k)
        if i + 1 < N:
            a2 = A[i + 1]
            v = a2 * (b + c) + b * c
            heappush(heap, -((v << 60) | ((i + 1) << 40) | (j << 20) | k))

        if i == 0:
            a = a0
            # child (0, j+1, k)
            if j + 1 < N:
                b2 = B[j + 1]
                v = b2 * (a + c) + c * a
                heappush(heap, -((v << 60) | ((j + 1) << 20) | k))
            # child (0, 0, k+1)
            if j == 0 and k + 1 < N:
                c2 = C[k + 1]
                v = c2 * (a + b) + a * b
                heappush(heap, -((v << 60) | (k + 1)))

if __name__ == "__main__":
    main()