import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out_lines = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        A = data[idx].decode(); idx += 1
        B = data[idx].decode(); idx += 1
        sumA = A.count('1')
        sumB = B.count('1')
        if sumA != sumB:
            out_lines.append("-1")
            continue
        q = deque()
        for i, ch in enumerate(A):
            if ch == '1':
                q.append(i)  # 0-indexed position
        right_max = 0
        left_max = 0
        possible = True
        for i, ch in enumerate(B):
            if ch == '1':
                if not q:
                    possible = False
                    break
                p = q.popleft()
                if i > p:
                    d = i - p
                    if d > right_max:
                        right_max = d
                elif i < p:
                    d = p - i
                    if d > left_max:
                        left_max = d
        if q or not possible:
            out_lines.append("-1")
        else:
            out_lines.append(str(max(right_max, left_max)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()