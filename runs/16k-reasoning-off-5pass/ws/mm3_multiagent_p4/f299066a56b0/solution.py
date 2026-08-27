import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    i = 0
    ans = 0
    for j in range(n):
        # advance i until either i == j or the condition 2*A[i] <= A[j] holds
        while i < j and A[i] * 2 <= A[j]:
            ans += 1
            i += 1
            break  # pair formed, move to next j
        # if i == j, the current j cannot be paired with itself; continue
        if i == j:
            # i must be less than j to pair, so skip this j by incrementing i
            i += 1
    print(ans)

if __name__ == "__main__":
    main()