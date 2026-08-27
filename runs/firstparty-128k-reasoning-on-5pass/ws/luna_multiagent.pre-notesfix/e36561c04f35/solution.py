import sys


def solve_case(a):
    # Build runs of equal values.
    runs = []
    for x in a:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])

    reductions = 0
    stack = []

    def push(value, length):
        if stack and stack[-1][0] == value:
            stack[-1][1] += length
        else:
            stack.append([value, length])

    for value, length in runs:
        push(value, length)

        # Pattern x^p y x y^q can be transformed by one swap into
        # x^(p+1) y^(q+1), reducing the total number of runs by 2.
        while len(stack) >= 4:
            x0, l0 = stack[-4]
            x1, l1 = stack[-3]
            x2, l2 = stack[-2]
            x3, l3 = stack[-1]

            if x0 == x2 and x1 == x3 and l1 == 1 and l2 == 1:
                del stack[-4:]
                push(x0, l0 + 1)
                push(x1, l3 + 1)
                reductions += 1
            else:
                break

    return len(runs) - reductions


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    ans = []

    for _ in range(t):
        n = data[pos]
        pos += 1
        a = data[pos:pos + n]
        pos += n
        ans.append(str(solve_case(a)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()