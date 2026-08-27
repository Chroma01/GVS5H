import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # XOR of all elements, useful when we enumerate the complement side
    total_xor = 0
    for a in A:
        total_xor ^= a

    # Enumerate the smaller side of the subsets:
    # size k = min(K, N-K) guarantees that C(N, k) ≤ 1e6
    k = K if K <= N - K else N - K

    # Special case: when k == 0 we either have K == N (full set) or K == 0
    # Both give a unique answer: XOR of all elements.
    if k == 0:
        print(total_xor)
        return

    sys.setrecursionlimit(1 << 20)  # depth is small, just a safety measure

    ans = 0
    N_local = N
    A_local = A
    total_xor_local = total_xor
    k_local = k
    K_local = K

    # Depth‑first search building subsets of size k
    def dfs(start: int, depth: int, cur_xor: int) -> None:
        nonlocal ans
        if depth == k_local:
            # If we enumerated the exact K side, the XOR is cur_xor;
            # otherwise we enumerated the complement, so XOR of the chosen K is
            # total_xor ^ cur_xor.
            cand = cur_xor if k_local == K_local else total_xor_local ^ cur_xor
            if cand > ans:
                ans = cand
            return
        # Number of positions still to choose
        remaining = k_local - depth
        # The last possible start index is N - remaining
        for i in range(start, N_local - remaining + 1):
            dfs(i + 1, depth + 1, cur_xor ^ A_local[i])

    dfs(0, 0, 0)
    print(ans)


if __name__ == "__main__":
    solve()