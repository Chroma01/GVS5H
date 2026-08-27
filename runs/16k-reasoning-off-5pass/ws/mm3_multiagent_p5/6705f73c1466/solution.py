import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    # Zero-based positions of '1's
    pos = [i for i, ch in enumerate(S) if ch == '1']
    K = len(pos)
    if K <= 1:
        print(0)
        return
    # Compute q_i = pos[i] - i
    q = [pos[i] - i for i in range(K)]
    q.sort()
    median = q[K // 2]
    # Total cost: sum |pos[i] - (median + i)|
    total = 0
    for i in range(K):
        total += abs(pos[i] - (median + i))
    print(total)

if __name__ == "__main__":
    solve()