import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # Collect positions of all '1's (0-indexed)
    ones = [i for i, c in enumerate(s) if c == '1']
    k = len(ones)
    
    if k <= 1:
        print(0)
        return
    
    # Compute q[j] = ones[j] - j
    q = [ones[j] - j for j in range(k)]
    
    # Sort q to find the median
    q.sort()
    
    # The median is q[k//2] (works for both odd and even k)
    median = q[k // 2]
    
    # Calculate the sum of absolute differences from the median
    ans = sum(abs(qj - median) for qj in q)
    
    print(ans)

if __name__ == '__main__':
    solve()