import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    # A may be given as one token or space-separated characters
    a = ''.join(data[1:])
    # Leaf costs: cost0[i] = flips to make leaf i equal 0, cost1[i] = flips to make it 1
    cost0 = [0 if ch == '0' else 1 for ch in a]
    cost1 = [0 if ch == '1' else 1 for ch in a]
    # Bottom-up DP: for each internal node, cost_v = sum of two smallest child cost_v
    size = len(cost0)
    while size > 1:
        new_size = size // 3
        new0 = [0] * new_size
        new1 = [0] * new_size
        for i in range(new_size):
            j = 3 * i
            x0, y0, z0 = cost0[j], cost0[j + 1], cost0[j + 2]
            # sum of two smallest = total - max
            new0[i] = x0 + y0 + z0 - max(x0, y0, z0)
            x1, y1, z1 = cost1[j], cost1[j + 1], cost1[j + 2]
            new1[i] = x1 + y1 + z1 - max(x1, y1, z1)
        cost0, cost1 = new0, new1
        size = new_size
    # Exactly one of the root costs is 0 (the current value); the other is the answer
    print(max(cost0[0], cost1[0]))

main()