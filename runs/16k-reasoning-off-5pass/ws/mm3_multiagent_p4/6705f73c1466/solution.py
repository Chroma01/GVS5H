import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    total = 0
    K = 0
    for i, ch in enumerate(S):
        if ch == '1':
            total += i
            K += 1
    # total is sum of positions of 1s (0-indexed)
    # answer = total - K*(N-K) - K*(K-1)//2
    ans = total - K * (N - K) - K * (K - 1) // 2
    print(ans)

if __name__ == "__main__":
    main()