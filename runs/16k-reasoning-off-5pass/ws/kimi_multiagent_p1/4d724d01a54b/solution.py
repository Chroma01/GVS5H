import sys

def solve(p):
    n = len(p)
    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i + 1  # 1-based original position of value v
    bit = [0] * (n + 2)

    def bit_add(i):
        while i <= n:
            bit[i] += 1
            i += i & -i

    def bit_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    total = 0
    # Process values from largest to smallest. All larger values are already
    # fixed in their final slots to the right, so v bubbles right through
    # exactly the smaller values, swapping at consecutive current indices
    # cur, cur+1, ..., v-1.
    for v in range(n, 0, -1):
        pv = pos[v]
        cur = pv - bit_sum(pv)  # current 1-based index of v
        m = v - cur             # number of rightward swaps needed
        if m > 0:
            total += (cur + v - 1) * m // 2  # arithmetic series sum
        bit_add(pv)
    return total

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    p = list(map(int, data[1:1 + n]))
    print(solve(p))

main()