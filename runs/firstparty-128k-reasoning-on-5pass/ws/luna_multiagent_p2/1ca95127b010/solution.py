import sys
from array import array

def solve():
    input = sys.stdin.readline

    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    # For the k-th 1, its position modulo X is invariant.
    # For the k-th 0, its position modulo Y is invariant.
    ones_s = array('I')
    zeros_s = array('I')

    for i, ch in enumerate(s):
        if ch == '1':
            ones_s.append(i % x)
        else:
            zeros_s.append(i % y)

    one_index = 0
    zero_index = 0
    ok = True

    for i, ch in enumerate(t):
        if ch == '1':
            if one_index >= len(ones_s) or ones_s[one_index] != i % x:
                ok = False
            one_index += 1
        else:
            if zero_index >= len(zeros_s) or zeros_s[zero_index] != i % y:
                ok = False
            zero_index += 1

    if one_index != len(ones_s) or zero_index != len(zeros_s):
        ok = False

    print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()