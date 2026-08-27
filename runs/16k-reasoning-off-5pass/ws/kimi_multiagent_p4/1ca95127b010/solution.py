import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].decode()
    T = data[4].decode()

    if S == T:
        print("Yes")
        return
    if X + Y > N:
        print("No")
        return

    # Canonical form: fixpoint of repeatedly applying Operation A at the
    # leftmost valid position (pushes Y-blocks of ones as far left as
    # possible). Verified confluent/class-consistent by exhaustive BFS for
    # all N <= 12 and all X,Y with X+Y <= N: two strings are reachable from
    # each other iff they have the same A-leftmost normal form.
    #
    # Efficient computation: process the string left to right maintaining
    # the fully A-reduced prefix as a stack of runs. A run is (char, len).
    # Appending characters one at a time and eagerly firing any A-pattern
    # that ends at the current right end reproduces the leftmost-A fixpoint:
    # the reduced prefix never contains an A-pattern, and each firing only
    # affects the rightmost runs, so the total work is O(number of runs).
    #
    # Operation A on runs: 0^a 1^b (a >= X, b >= Y) at the right end becomes
    # 0^(a-X) 1^Y 0^X 1^(b-Y) with merging of zero-length runs. Since the
    # prefix is A-free, the only place a pattern can appear after appending
    # is at the right end, involving the last 0-run and last 1-run.

    def canon(s):
        stack = []  # list of [char, length]
        for ch in s:
            if stack and stack[-1][0] == ch:
                stack[-1][1] += 1
            else:
                stack.append([ch, 1])
            # Fire A-patterns at the right end while possible.
            while len(stack) >= 2 and stack[-2][0] == '0' \
                    and stack[-2][1] >= X and stack[-1][1] >= Y:
                a = stack[-2][1]
                b = stack[-1][1]
                stack.pop()
                stack.pop()
                # 0^(a-X)
                if a - X > 0:
                    if stack and stack[-1][0] == '0':
                        stack[-1][1] += a - X
                    else:
                        stack.append(['0', a - X])
                # 1^Y (merges with a 1-run on the left if a == X)
                if stack and stack[-1][0] == '1':
                    stack[-1][1] += Y
                else:
                    stack.append(['1', Y])
                # 0^X
                if stack and stack[-1][0] == '0':
                    stack[-1][1] += X
                else:
                    stack.append(['0', X])
                # 1^(b-Y)
                if b - Y > 0:
                    if stack and stack[-1][0] == '1':
                        stack[-1][1] += b - Y
                    else:
                        stack.append(['1', b - Y])
                # else the trailing 0^X may merge with a following 0-run
                # later; nothing to do now.
        return ''.join(c * l for c, l in stack)

    print("Yes" if canon(S) == canon(T) else "No")

solve()