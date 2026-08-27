import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))
    x.sort()
    gaps = [x[i + 1] - x[i] for i in range(n - 1)]
    # gaps[j] for j in 0..n-2 corresponds to position j+1 (1-indexed), weight = n - (j+1)
    # parity classes based on 1-indexed position: j+1 parity == j parity flipped; just split by j % 2
    odd = sorted((gaps[j] for j in range(n - 1) if j % 2 == 0), reverse=True)  # 1-indexed odd positions
    even = sorted((gaps[j] for j in range(n - 1) if j % 2 == 1), reverse=True)  # 1-indexed even positions
    # weights n-(j+1) decrease as j increases; assign largest gap to largest j (smallest weight)
    # within each parity class, positions j increase; weights decrease; so place sorted-descending gaps
    # at positions in increasing j order? No: largest gap should get smallest weight => largest j.
    # So iterate positions in decreasing j and assign largest gaps first.
    ans = n * x[0]
    io = ie = 0
    # collect positions per parity, sorted by weight ascending (i.e., j descending)
    pos_odd = [j for j in range(n - 1) if j % 2 == 0]
    pos_even = [j for j in range(n - 1) if j % 2 == 1]
    pos_odd.sort(reverse=True)   # largest j first = smallest weight first
    pos_even.sort(reverse=True)
    assigned = [0] * (n - 1)
    for k, j in enumerate(pos_odd):
        assigned[j] = odd[k]
    for k, j in enumerate(pos_even):
        assigned[j] = even[k]
    total = ans
    for j in range(n - 1):
        total += (n - 1 - j) * assigned[j]
    print(total)

solve()