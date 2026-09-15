import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    total = 0
    for x in A:
        total ^= x

    if K == 0:
        print(0)
        return
    if K == N:
        print(total)
        return

    if K <= N - K:
        r = K
        base = 0
    else:
        r = N - K
        base = total

    if r == 0:
        print(base)
        return

    if r == 1:
        if base == 0:
            print(max(A))
        else:
            m = 0
            b = base
            for x in A:
                v = b ^ x
                if v > m:
                    m = v
            print(m)
        return

    if r == 2:
        m = 0
        arr = A
        n = N
        if base == 0:
            for i in range(n - 1):
                ai = arr[i]
                for j in range(i + 1, n):
                    v = ai ^ arr[j]
                    if v > m:
                        m = v
        else:
            b = base
            for i in range(n - 1):
                bai = b ^ arr[i]
                for j in range(i + 1, n):
                    v = bai ^ arr[j]
                    if v > m:
                        m = v
        print(m)
        return

    arr = A
    n = N
    b = base
    sys.setrecursionlimit(1000000)

    def dfs(start, left, x, arr=arr, n=n):
        if left == 3:
            best = 0
            for i in range(start, n - 2):
                xi = x ^ arr[i]
                for j in range(i + 1, n - 1):
                    xij = xi ^ arr[j]
                    for k in range(j + 1, n):
                        v = xij ^ arr[k]
                        if v > best:
                            best = v
            return best

        if left == 4:
            best = 0
            for i in range(start, n - 3):
                xi = x ^ arr[i]
                for j in range(i + 1, n - 2):
                    xij = xi ^ arr[j]
                    for k in range(j + 1, n - 1):
                        xijk = xij ^ arr[k]
                        for l in range(k + 1, n):
                            v = xijk ^ arr[l]
                            if v > best:
                                best = v
            return best

        best = 0
        end = n - left + 1
        for i in range(start, end):
            v = dfs(i + 1, left - 1, x ^ arr[i])
            if v > best:
                best = v
        return best

    print(dfs(0, r, b))

if __name__ == "__main__":
    solve()