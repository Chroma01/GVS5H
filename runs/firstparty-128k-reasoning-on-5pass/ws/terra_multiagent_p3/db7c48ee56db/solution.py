import sys

def main():
    input = sys.stdin.buffer.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    total_xor = 0
    for x in A:
        total_xor ^= x

    R = min(K, N - K)
    enumerate_excluded = (R != K)
    ans = 0

    def dfs(start, chosen, current_xor):
        nonlocal ans

        if chosen == R:
            value = total_xor ^ current_xor if enumerate_excluded else current_xor
            if value > ans:
                ans = value
            return

        need = R - chosen
        last = N - need
        for i in range(start, last + 1):
            dfs(i + 1, chosen + 1, current_xor ^ A[i])

    dfs(0, 0, 0)
    print(ans)

if __name__ == "__main__":
    main()