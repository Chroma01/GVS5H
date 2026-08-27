import sys


def solve() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())

    for _ in range(m):
        input()

    maximum_bipartite_edges = (n * n) // 4
    print("Aoki" if (maximum_bipartite_edges - m) % 2 else "Takahashi")


if __name__ == "__main__":
    solve()