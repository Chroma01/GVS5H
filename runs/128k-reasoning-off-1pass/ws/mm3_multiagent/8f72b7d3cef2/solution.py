import sys
from collections import deque

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # Left pass: compute L[i] = total size slime i can achieve by absorbing only leftwards
    # Using a monotonic stack storing (index, current_size)
    stack = []
    L = [0] * N
    for i in range(N):
        cur_size = A[i]
        # Merge from stack while current slime can absorb the left neighbor
        while stack and cur_size > stack[-1][1]:
            idx, sz = stack.pop()
            cur_size += sz
        # If stack becomes empty or top size is larger, we cannot absorb it now,
        # but the top might be able to absorb us if it were larger - however we are processing left-to-right.
        # Actually, we need to maintain the stack of "dominant" slimes.
        # The standard trick: after merging all smaller left neighbors, push current slime with its accumulated size.
        # But we also need to know L[i] = cur_size (total size including leftward absorbed).
        # However, if stack is not empty, the top has size >= cur_size (since we stopped because cur_size <= top).
        # The top slime cannot be absorbed by us (since it's >= us), so we cannot expand further left.
        # So L[i] is just cur_size.
        L[i] = cur_size
        stack.append((i, cur_size))

    # Right pass: compute R[i] = total size slime i can achieve by absorbing only rightwards
    R = [0] * N
    stack = []
    for i in range(N - 1, -1, -1):
        cur_size = A[i]
        while stack and cur_size > stack[-1][1]:
            idx, sz = stack.pop()
            cur_size += sz
        R[i] = cur_size
        stack.append((i, cur_size))

    # For each K, answer = L[K] + R[K] - A[K]
    ans = [str(L[i] + R[i] - A[i]) for i in range(N)]
    sys.stdout.write(" ".join(ans))

if __name__ == "__main__":
    solve()