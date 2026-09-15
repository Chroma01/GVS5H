import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])

    A = [0] * N
    total_xor = 0
    for i in range(N):
        v = int(data[2 + i])
        A[i] = v
        total_xor ^= v

    # Complement symmetry:
    # XOR(chosen K) = total_xor XOR XOR(excluded N-K).
    # Enumerate the smaller side.
    if K <= N - K:
        M = K
        mask = 0
    else:
        M = N - K
        mask = total_xor

    if M == 0:
        sys.stdout.write(str(mask))
        return

    n = N
    arr = A

    # Fast paths for the cases where N can be very large.
    if M == 1:
        if mask == 0:
            ans = max(arr)
        else:
            ans = 0
            m = mask
            for v in arr:
                y = m ^ v
                if y > ans:
                    ans = y
        sys.stdout.write(str(ans))
        return

    if M == 2:
        ans = 0
        a = arr
        if mask == 0:
            for i in range(n - 1):
                ai = a[i]
                for j in range(i + 1, n):
                    y = ai ^ a[j]
                    if y > ans:
                        ans = y
        else:
            m = mask
            for i in range(n - 1):
                ai = a[i]
                for j in range(i + 1, n):
                    y = m ^ ai ^ a[j]
                    if y > ans:
                        ans = y
        sys.stdout.write(str(ans))
        return

    sys.setrecursionlimit(1000000)
    ans = 0

    # Enumerate combinations by index, carrying the current XOR.
    # Base cases rem == 1, 2, 3 avoid many leaf function calls.
    def dfs(start, rem, x, arr=arr, n=n, mask=mask):
        nonlocal ans

        if rem == 1:
            cur = ans
            m = mask
            a = arr
            for i in range(start, n):
                y = m ^ x ^ a[i]
                if y > cur:
                    cur = y
            ans = cur
            return

        if rem == 2:
            cur = ans
            m = mask
            a = arr
            for i in range(start, n - 1):
                xi = x ^ a[i]
                for j in range(i + 1, n):
                    y = m ^ xi ^ a[j]
                    if y > cur:
                        cur = y
            ans = cur
            return

        if rem == 3:
            cur = ans
            m = mask
            a = arr
            for i in range(start, n - 2):
                xi = x ^ a[i]
                for j in range(i + 1, n - 1):
                    xij = xi ^ a[j]
                    for k in range(j + 1, n):
                        y = m ^ xij ^ a[k]
                        if y > cur:
                            cur = y
            ans = cur
            return

        end = n - rem + 1
        a = arr
        for i in range(start, end):
            dfs(i + 1, rem - 1, x ^ a[i])

    dfs(0, M, 0)
    sys.stdout.write(str(ans))


if __name__ == "__main__":
    solve()