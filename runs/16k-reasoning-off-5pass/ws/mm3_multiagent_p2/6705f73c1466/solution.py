import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    
    # Collect 0-based indices of '1's
    p = [i for i, ch in enumerate(S) if ch == '1']
    k = len(p)
    
    # Transform to q[i] = p[i] - i
    q = [p[i] - i for i in range(k)]
    
    # Find median of q
    q_sorted = sorted(q)
    median = q_sorted[k // 2]
    
    # Compute sum of absolute differences
    total = sum(abs(x - median) for x in q)
    
    print(total)

if __name__ == "__main__":
    main()