import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); pos += 1
        arr = data[pos:pos + N]; pos += N

        # compress into runs [value, length]
        runs = []
        for x in arr:
            if runs and runs[-1][0] == x:
                runs[-1][1] += 1
            else:
                runs.append([x, 1])
        m = len(runs)

        stack = []
        type2 = 0
        for i in range(m):
            v = runs[i][0]
            l = runs[i][1]
            if stack and stack[-1][0] == v:
                stack[-1][1] += l
            else:
                stack.append([v, l])

            while True:
                changed = False

                # gain-1 move: X Y X Y with middle runs length 1
                if len(stack) >= 4:
                    v1, l1 = stack[-4]
                    v2, l2 = stack[-3]
                    v3, l3 = stack[-2]
                    v4, l4 = stack[-1]
                    if v1 == v3 and v2 == v4 and l2 == 1 and l3 == 1:
                        del stack[-4:]
                        stack.append([v1, l1 + 1])
                        stack.append([v4, l4 + 1])
                        type2 += 1
                        changed = True

                # neutral move: X Y X with last two runs length 1
                if not changed and len(stack) >= 3:
                    v1, l1 = stack[-3]
                    v2, l2 = stack[-2]
                    v3, l3 = stack[-1]
                    if v1 == v3 and l2 == 1 and l3 == 1:
                        do = True
                        if i + 1 < m:
                            n1 = runs[i + 1][0]
                            if n1 == v2:
                                # next run closes X Y X Y -> a Type2 appears
                                do = False
                            elif (n1 != v3 and i + 3 < m
                                  and runs[i + 1][1] == 1 and runs[i + 2][1] == 1
                                  and runs[i + 2][0] == v3 and runs[i + 3][0] == n1):
                                # top run becomes w1 of the upcoming Type2
                                # [v3, n1, v3, n1]
                                do = False
                        if do:
                            del stack[-3:]
                            stack.append([v1, l1 + 1])
                            stack.append([v2, 1])
                            changed = True

                if not changed:
                    break

        out.append(str(m - type2))

    sys.stdout.write("\n".join(out) + "\n")

main()