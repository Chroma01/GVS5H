import sys
from array import array

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = b''.join(data[1:])

    # Leaf costs: cost of making the leaf evaluate to 0 / to 1.
    # Byte value of '0' is 48, '1' is 49.
    cost0 = array('i', (b - 48 for b in s))      # 0 if bit is 0 else 1
    cost1 = array('i', (49 - b for b in s))      # 1 if bit is 0 else 0

    length = len(s)
    while length > 1:
        new_len = length // 3
        ncost0 = array('i', bytes(4 * new_len))
        ncost1 = array('i', bytes(4 * new_len))
        c0 = cost0
        c1 = cost1
        w0 = ncost0
        w1 = ncost1
        for i in range(new_len):
            j = 3 * i
            a = c0[j]; b = c0[j + 1]; c = c0[j + 2]
            # sum of the two smallest = total - max
            w0[i] = a + b + c - (a if a >= b and a >= c else (b if b >= c else c))
            a = c1[j]; b = c1[j + 1]; c = c1[j + 2]
            w1[i] = a + b + c - (a if a >= b and a >= c else (b if b >= c else c))
        cost0 = ncost0
        cost1 = ncost1
        length = new_len

    # The root's actual value costs 0 flips; the answer is the other (nonzero) cost.
    ans = cost0[0] if cost0[0] != 0 else cost1[0]
    sys.stdout.write(str(ans) + '\n')

main()