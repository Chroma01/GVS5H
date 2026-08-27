from typing import List


def cost(x: int) -> int:
    # Smallest k such that x < 4**k.
    # For positive x, this is ceil(bit_length(x) / 2).
    return (x.bit_length() + 1) // 2


def prefix_cost(n: int) -> int:
    # Sum of cost(x) for 1 <= x <= n.
    # cost is constant k on each block [4**(k-1), 4**k - 1].
    if n <= 0:
        return 0

    total = 0
    start = 1
    k = 1

    while start <= n:
        end = start * 4 - 1
        if n >= end:
            total += k * (end - start + 1)
            start *= 4
            k += 1
        else:
            total += k * (n - start + 1)
            break

    return total


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        ans = 0

        for l, r in queries:
            total_cost = prefix_cost(r) - prefix_cost(l - 1)
            ans += max(cost(r), (total_cost + 1) // 2)

        return ans


if __name__ == "__main__":
    sol = Solution()
    print(sol.minOperations([[1, 2], [2, 4]]))
    print(sol.minOperations([[2, 6]]))