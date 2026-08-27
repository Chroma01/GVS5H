import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].decode()          # string of '0' and '1'
    
    # positions of '1's (0‑based)
    pos = [i for i, ch in enumerate(S) if ch == '1']
    K = len(pos)                  # number of 1s
    
    # d_i = original position of i‑th '1' minus its index among the ones
    d = [pos[i] - i for i in range(K)]
    d.sort()
    
    # optimal start of the final block is a median of d
    median = d[K // 2]
    start = median
    if start < 0:
        start = 0
    elif start > N - K:
        start = N - K
    
    # minimal number of adjacent swaps
    ans = sum(abs(x - start) for x in d)
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()