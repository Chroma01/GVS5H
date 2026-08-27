import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # prefix sums, P[0] = 0, sum(i..j) = P[j] - P[i-1]
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + A[i]

    # R_bound[i]: farthest r reachable starting at i expanding only right.
    # First index k > i with sum(A[i..k-1]) <= A[k] stops the expansion.
    R_bound = [0] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        while stack and P[i - 1] - P[stack[-1] - 1] <= A[i]:
            R_bound[stack.pop()] = i - 1
        stack.append(i)
    while stack:
        R_bound[stack.pop()] = n

    # L_bound[i]: farthest l reachable starting at i expanding only left.
    # First index k < i with sum(A[k+1..i]) <= A[k] stops the expansion.
    L_bound = [0] * (n + 2)
    stack = []
    for i in range(n, 0, -1):
        while stack and P[stack[-1]] - P[i] <= A[i]:
            L_bound[stack.pop()] = i + 1
        stack.append(i)
    while stack:
        L_bound[stack.pop()] = 1

    ans = [0] * (n + 1)
    for k in range(1, n + 1):
        L = k
        R = k
        cur = A[k]
        while True:
            changed = False
            # expand right using precomputed block jumps
            while R < n and cur > A[R + 1]:
                j = R + 1
                rb = R_bound[j]
                cur += P[rb] - P[j - 1]
                R = rb
                changed = True
            # expand left using precomputed block jumps
            while L > 1 and cur > A[L - 1]:
                j = L - 1
                lb = L_bound[j]
                cur += P[j] - P[lb - 1]
                L = lb
                changed = True
            if not changed:
                break
        ans[k] = cur

    sys.stdout.write(' '.join(str(ans[k]) for k in range(1, n + 1)))

solve()