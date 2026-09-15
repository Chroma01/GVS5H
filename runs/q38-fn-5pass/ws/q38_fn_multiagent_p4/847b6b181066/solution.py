import sys

N, R, C = map(int, sys.stdin.buffer.readline().split())
S = sys.stdin.buffer.readline().strip()

off = 2 * N + 1
sh = (4 * N + 2).bit_length()

seen = {((off) << sh) | off}
r = c = 0
ans = []

for ch in S:
    if ch == 78:
        r -= 1
    elif ch == 83:
        r += 1
    elif ch == 87:
        c -= 1
    else:
        c += 1

    ans.append('1' if (((r - R + off) << sh) | (c - C + off)) in seen else '0')
    seen.add(((r + off) << sh) | (c + off))

sys.stdout.write(''.join(ans) + '\n')