import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = ''.join(data[1:])

    # cost1: min 0->1 flips to make a node output 1
    # cost0: min 1->0 flips to make a node output 0
    cost1 = [1 if c == '0' else 0 for c in A]
    cost0 = [1 if c == '1' else 0 for c in A]
    # original values of the leaves
    orig = [1 if c == '1' else 0 for c in A]

    for _ in range(n):
        # majority of 3 children, monotone -> pick two cheapest to force 1 (resp 0)
        it1 = iter(cost1)
        cost1 = [a + b + c - max(a, b, c) for a, b, c in zip(it1, it1, it1)]
        it0 = iter(cost0)
        cost0 = [a + b + c - max(a, b, c) for a, b, c in zip(it0, it0, it0)]
        ito = iter(orig)
        orig = [1 if a + b + c >= 2 else 0 for a, b, c in zip(ito, ito, ito)]

    # flip the root: if root originally 1, we must force 0 (cost0); else force 1 (cost1)
    print(cost0[0] if orig[0] == 1 else cost1[0])

main()