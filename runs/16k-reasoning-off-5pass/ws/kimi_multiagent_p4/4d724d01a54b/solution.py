import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    pos = [0] * (n + 1)
    for idx in range(1, n + 1):
        pos[int(data[idx])] = idx
    # diff over boundaries: boundary i (1 <= i <= n-1) lies between positions i and i+1
    diff = [0] * (n + 2)
    for v in range(1, n + 1):
        a = pos[v]
        b = v
        if a == b:
            continue
        lo = a if a < b else b
        hi = a if a > b else b
        diff[lo] += 1
        diff[hi] -= 1
    ans = 0
    cur = 0
    for i in range(1, n):
        cur += diff[i]
        ans += i * cur
    print(ans)

main()