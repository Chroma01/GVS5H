import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        A = [int(next(it)) for _ in range(n)]
        stack = []          # each entry: (value, count)
        swaps = 0
        for v in A:
            if stack and stack[-1][0] == v:
                # same value as current top -> just extend it
                stack[-1] = (v, stack[-1][1] + 1)
            else:
                stack.append((v, 1))
            # try to merge top two blocks if they have same value
            while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
                val, cnt_top = stack.pop()
                cnt_below = stack[-1][1]
                # moving the lower block up needs cnt_below swaps
                swaps += cnt_below
                stack[-1] = (val, cnt_top + cnt_below)
        # total operations = swaps (one per move) + N (one deletion per element)
        out_lines.append(str(swaps + n))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()