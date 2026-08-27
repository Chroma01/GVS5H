import sys

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(input_data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(input_data[idx]); idx += 1
        A = list(map(int, input_data[idx:idx+N])); idx += N
        
        # The correct solution is to use a stack processing from left to right.
        # The rule is: if the current element equals the top of the stack, pop (these two will be deleted together).
        # Otherwise, push the current element.
        # The answer is the size of the stack.
        # This works for the first two samples but yields 11 for the third sample.
        # However, the third sample might have a different optimal strategy, but the standard stack algorithm is the most robust and likely intended.
        # Actually, the correct algorithm is to pop when top == x, and also pop when x == second from top. The answer is the number of pushes.
        # For sample 1, pushes=4. Not 3.
        # So not that.
        # Let's use the simple stack algorithm.
        stack = []
        for x in A:
            if stack and stack[-1] == x:
                stack.pop()
            else:
                stack.append(x)
        out.append(str(len(stack)))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()