import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    K = data[1]
    A = data[2:2 + N]

    total = 0
    for v in A:
        total ^= v

    choose = K <= N - K
    m = K if choose else N - K

    if m == 0:
        print(total if K == N else 0)
        return

    if m == 1:
        if choose:
            print(max(A))
        else:
            ans = 0
            t = total
            for v in A:
                val = t ^ v
                if val > ans:
                    ans = val
            print(ans)
        return

    base = N - m + 1
    ans = 0

    if choose:
        def dfs(start, x, stop, A=A, N=N):
            nonlocal ans
            if stop == N:
                for i in range(start, N):
                    val = x ^ A[i]
                    if val > ans:
                        ans = val
                return
            for i in range(start, stop):
                dfs(i + 1, x ^ A[i], stop + 1)

        dfs(0, 0, base)
    else:
        def dfs(start, x, stop, A=A, N=N, t=total):
            nonlocal ans
            if stop == N:
                y = t ^ x
                for i in range(start, N):
                    val = y ^ A[i]
                    if val > ans:
                        ans = val
                return
            for i in range(start, stop):
                dfs(i + 1, x ^ A[i], stop + 1)

        dfs(0, 0, base)

    print(ans)

if __name__ == "__main__":
    solve()