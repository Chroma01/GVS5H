import sys

def solve():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].decode(); T = data[4].decode()

    # Operations preserve the number of 1s.
    if S.count('1') != T.count('1'):
        sys.stdout.write("No\n")
        return

    # No operation fits in the string, so nothing can change.
    if N < X + Y:
        sys.stdout.write("Yes\n" if S == T else "No\n")
        return

    # Operation A is the rewrite 0^X 1^Y -> 1^Y 0^X and B is its inverse.
    # The rule terminates (each application moves Y ones left past X zeros,
    # decreasing the sum of 1-positions by X*Y) and two redexes can never
    # overlap (the pattern has a single 0->1 transition), so disjoint redexes
    # commute; by Newman's lemma the normal form is unique. Hence S and T are
    # inter-reachable iff their normal forms coincide.
    #
    # Run-stack reduction, left to right; the stack always holds the normal
    # form of the processed prefix. Appending one character can only create a
    # redex involving the trailing runs:
    #   Phase 1: ... [0,a][1,b] with a >= X, b >= Y.
    #   Phase 2: ... [0,a][1,b][0,t] with a >= X, b >= Y (a 1-run moving left,
    #            dragging accumulated zeros t behind it).
    # Each step swaps the 0-run past the 1-run in q = a // X elementary swaps:
    # if r = a mod X > 0 the leftover boundary 0^r 1^b is inert and we stop;
    # if r == 0 the 1-run merges with the 1-run further left and may cascade.
    def canonical(s):
        stack = []  # list of [char, length], alternating chars
        for ch in s:
            if stack and stack[-1][0] == ch:
                stack[-1][1] += 1
            else:
                stack.append([ch, 1])
            while True:
                n = len(stack)
                if (n >= 2 and stack[-1][0] == '1' and stack[-2][0] == '0'
                        and stack[-2][1] >= X and stack[-1][1] >= Y):
                    a = stack[-2][1]; b = stack[-1][1]
                    q, r = divmod(a, X)
                    stack.pop(); stack.pop()
                    if r:
                        stack.append(['0', r])
                        stack.append(['1', b])
                        stack.append(['0', q * X])
                        break
                    if stack and stack[-1][0] == '1':
                        stack[-1][1] += b
                    else:
                        stack.append(['1', b])
                    stack.append(['0', q * X])
                    continue
                if (n >= 3 and stack[-1][0] == '0' and stack[-2][0] == '1'
                        and stack[-3][0] == '0' and stack[-3][1] >= X
                        and stack[-2][1] >= Y):
                    a = stack[-3][1]; b = stack[-2][1]; t = stack[-1][1]
                    q, r = divmod(a, X)
                    stack.pop(); stack.pop(); stack.pop()
                    if r:
                        stack.append(['0', r])
                        stack.append(['1', b])
                        stack.append(['0', t + q * X])
                        break
                    if stack and stack[-1][0] == '1':
                        stack[-1][1] += b
                    else:
                        stack.append(['1', b])
                    stack.append(['0', t + q * X])
                    continue
                break
        return stack

    sys.stdout.write("Yes\n" if canonical(S) == canonical(T) else "No\n")

solve()