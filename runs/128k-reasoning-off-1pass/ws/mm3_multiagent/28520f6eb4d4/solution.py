import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    X = [0] * N
    H = [0] * N
    for i in range(N):
        x, h = map(int, input().split())
        X[i] = x
        H[i] = h

    stack = []
    max_b = -1e30  # very small number

    for i in range(N):
        Xi = X[i]
        Hi = H[i]
        if stack:
            # Binary search on the stack to find the index that maximizes b(j, i)
            l, r = 0, len(stack) - 1
            while l < r:
                m = (l + r) // 2
                j1 = stack[m]
                j2 = stack[m + 1]
                # Compare b(j1, i) and b(j2, i)
                # b(j, i) = (H[j]*Xi - Hi*X[j]) / (Xi - X[j])
                # Cross-multiply to avoid float:
                # We want to know if b(j1, i) < b(j2, i)
                # (H[j1]*Xi - Hi*X[j1]) / (Xi - X[j1]) < (H[j2]*Xi - Hi*X[j2]) / (Xi - X[j2])
                # Since denominators are positive, cross-multiply:
                left = (H[j1] * Xi - Hi * X[j1]) * (Xi - X[j2])
                right = (H[j2] * Xi - Hi * X[j2]) * (Xi - X[j1])
                if left < right:
                    l = m + 1
                else:
                    r = m
            best_j = stack[l]
            b_val = (H[best_j] * Xi - Hi * X[best_j]) / (Xi - X[best_j])
            if b_val > max_b:
                max_b = b_val

        # Pop while the last point is useless
        while len(stack) >= 2:
            j = stack[-2]
            k = stack[-1]
            # Pop if b(j, k) >= b(k, i)
            left = (H[j] * X[k] - H[k] * X[j]) * (Xi - X[k])
            right = (H[k] * Xi - Hi * X[k]) * (X[k] - X[j])
            if left >= right:
                stack.pop()
            else:
                break
        stack.append(i)

    if max_b < 0:
        print(-1)
    else:
        print("{:.15f}".format(max_b))

if __name__ == "__main__":
    solve()