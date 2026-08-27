import sys

def solve():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()
    
    MOD = 998244353
    # Reverse the string and process
    S_rev = S[::-1]
    
    stack = []
    ans = 1
    for c in S_rev:
        if c == 'W':
            stack.append(1)
        else:  # 'B'
            if not stack:
                print(0)
                return
            # Pop one W from the stack
            # The number of choices is the current stack size
            s = len(stack)
            ans = ans * s % MOD
            stack.pop()
    
    if stack:
        print(0)
    else:
        print(ans)

solve()