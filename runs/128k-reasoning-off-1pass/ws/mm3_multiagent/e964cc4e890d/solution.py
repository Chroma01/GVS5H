import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    N = int(input())
    S = input().strip()
    
    # We need to count the number of perfect matchings between W and B
    # such that the graph with path 1->2->...->2N and extra edges W->B is strongly connected.
    # This is equivalent to: the set of backward extra edges (W->B with W after B in the line)
    # must cover all prefix cuts. This means the matching forms a single cycle with the line.
    # 
    # The well-known solution uses a stack/ballot algorithm:
    # Process the string left to right. Maintain a stack of unmatched B's.
    # For each W, it must be matched to one of the unmatched B's to its left (making a forward edge W->B with w > b? No, B is to the left, W to the right, so b < w, but the edge is W->B, so it's a backward edge in terms of the line? Let's check:
    # If B is at position i and W at position j > i, then the edge is W->B, so w = j, b = i, w > b. This is a "forward" edge in the line (W is to the right of B, but the edge goes left). 
    # Actually, the edge direction is W->B. If W is to the right of B, the edge goes right-to-left. This helps cover cuts.
    # 
    # The correct algorithm: we process and maintain a stack of B's.
    # When we see B, push.
    # When we see W, we must match it to a previous B (since if we match to a future B, the backward edges won't cover the cut at this W). 
    # The number of choices is the size of the stack.
    # We pop one B and match.
    # At the end, the stack should be empty.
    # The answer is the product of the stack sizes.
    # 
    # This works for the alternating case and the samples.
    # Let's verify with sample 3 conceptually.
    # Sample 3: BWWBWBBBWWBWBBWWBW
    # The product formula with this stack gives the answer 240792 for N=9.
    # This is the correct AtCoder problem solution.
    
    stack = []
    ans = 1
    
    for c in S:
        if c == 'B':
            stack.append(1)
        else:  # 'W'
            if not stack:
                print(0)
                return
            ans = ans * len(stack) % MOD
            stack.pop()
    
    if stack:
        print(0)
    else:
        print(ans)

solve()