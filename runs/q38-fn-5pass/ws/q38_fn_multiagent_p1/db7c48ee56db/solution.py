import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:]
    del data

    total = 0
    for x in A:
        total ^= x

    if K <= N - K:
        M = K
        direct = True
    else:
        M = N - K
        direct = False

    if M == 0:
        print(total)
        return

    if M == 1:
        if direct:
            print(max(A))
        else:
            ans = 0
            t = total
            for x in A:
                v = t ^ x
                if v > ans:
                    ans = v
            print(ans)
        return

    if M == 2:
        ans = 0
        if direct:
            for i in range(N - 1):
                ai = A[i]
                for j in range(i + 1, N):
                    v = ai ^ A[j]
                    if v > ans:
                        ans = v
        else:
            t = total
            for i in range(N - 1):
                ai = t ^ A[i]
                for j in range(i + 1, N):
                    v = ai ^ A[j]
                    if v > ans:
                        ans = v
        print(ans)
        return

    if M == 3:
        ans = 0
        if direct:
            for i in range(N - 2):
                ai = A[i]
                for j in range(i + 1, N - 1):
                    aij = ai ^ A[j]
                    for k in range(j + 1, N):
                        v = aij ^ A[k]
                        if v > ans:
                            ans = v
        else:
            t = total
            for i in range(N - 2):
                ai = t ^ A[i]
                for j in range(i + 1, N - 1):
                    aij = ai ^ A[j]
                    for k in range(j + 1, N):
                        v = aij ^ A[k]
                        if v > ans:
                            ans = v
        print(ans)
        return

    # M >= 4
    ans = 0
    sys.setrecursionlimit(1_000_000)

    if direct:
        def dfs(start, rem, cur, A=A, n=N, range=range):
            nonlocal ans
            if rem == 4:
                best = ans
                for i in range(start, n - 3):
                    ai = cur ^ A[i]
                    for j in range(i + 1, n - 2):
                        aij = ai ^ A[j]
                        for k in range(j + 1, n - 1):
                            aijk = aij ^ A[k]
                            for l in range(k + 1, n):
                                v = aijk ^ A[l]
                                if v > best:
                                    best = v
                ans = best
                return

            end = n - rem + 1
            for i in range(start, end):
                dfs(i + 1, rem - 1, cur ^ A[i])
    else:
        t = total

        def dfs(start, rem, cur, A=A, n=N, t=t, range=range):
            nonlocal ans
            if rem == 4:
                best = ans
                base = t ^ cur
                for i in range(start, n - 3):
                    ai = base ^ A[i]
                    for j in range(i + 1, n - 2):
                        aij = ai ^ A[j]
                        for k in range(j + 1, n - 1):
                            aijk = aij ^ A[k]
                            for l in range(k + 1, n):
                                v = aijk ^ A[l]
                                if v > best:
                                    best = v
                ans = best
                return

            end = n - rem + 1
            for i in range(start, end):
                dfs(i + 1, rem - 1, cur ^ A[i])

    dfs(0, M, 0)
    print(ans)


if __name__ == "__main__":
    solve()