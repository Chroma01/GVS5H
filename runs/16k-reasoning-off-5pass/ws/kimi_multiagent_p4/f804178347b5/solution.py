import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    # A may be given as one token or space-separated characters
    a = ''.join(data[1:])
    size = 3 ** n
    cost0 = [0] * size
    cost1 = [0] * size
    for i, ch in enumerate(a):
        if ch == '0':
            cost1[i] = 1
        else:
            cost0[i] = 1
    # Bottom-up: combine groups of 3; majority needs >=2 children equal to v
    while size > 1:
        new_size = size // 3
        nc0 = [0] * new_size
        nc1 = [0] * new_size
        for i in range(new_size):
            j = 3 * i
            x0, x1, x2 = cost0[j], cost0[j + 1], cost0[j + 2]
            # sum of two smallest
            nc0[i] = x0 + x1 + x2 - max(x0, x1, x2)
            y0, y1, y2 = cost1[j], cost1[j + 1], cost1[j + 2]
            nc1[i] = y0 + y1 + y2 - max(y0, y1, y2)
        cost0, cost1 = nc0, nc1
        size = new_size
    # The cost of the current output value is 0; the answer is the other one.
    print(max(cost0[0], cost1[0]))

main()