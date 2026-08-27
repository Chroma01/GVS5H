import sys
from collections import deque
from itertools import combinations_with_replacement

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    T = int(input_data[idx]); idx += 1
    out_lines = []
    for _ in range(T):
        N = int(input_data[idx]); idx += 1
        A = input_data[idx]; idx += 1
        B = input_data[idx]; idx += 1
        a_pos = [i for i, c in enumerate(A) if c == '1']
        b_set = set(i for i, c in enumerate(B) if c == '1')
        b_pos = sorted(b_set)
        k = len(a_pos)
        m = len(b_pos)
        if m == 0 or k == 0:
            out_lines.append("-1")
            continue
        if m > k:
            out_lines.append("-1")
            continue
        if N <= 12 and k <= 4:
            start = tuple(sorted(a_pos))
            targets = set()
            for b_mult in combinations_with_replacement(b_pos, k):
                if list(b_mult) == sorted(b_mult):
                    targets.add(tuple(b_mult))
            visited = {start: 0}
            q = deque([start])
            found = -1
            while q:
                state = q.popleft()
                d = visited[state]
                if state in targets:
                    found = d
                    break
                seen_i = set()
                for i in range(N):
                    if i in seen_i:
                        continue
                    seen_i.add(i)
                    new_state = []
                    for x in state:
                        if x < i:
                            new_state.append(x+1)
                        elif x > i:
                            new_state.append(x-1)
                        else:
                            new_state.append(x)
                    new_state = tuple(sorted(new_state))
                    if new_state not in visited:
                        visited[new_state] = d+1
                        q.append(new_state)
            out_lines.append(str(found) if found != -1 else "-1")
        else:
            a = a_pos
            b = b_pos
            lo = 0
            hi = N
            ans = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                possible = True
                ptr = 0
                prev = -10**9
                for j in range(k):
                    min_val = max(a[j] - mid, prev)
                    max_val = a[j] + mid
                    while ptr < m and b[ptr] < min_val:
                        ptr += 1
                    if ptr == m:
                        possible = False
                        break
                    if b[ptr] > max_val:
                        possible = False
                        break
                    prev = b[ptr]
                if possible:
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

solve()