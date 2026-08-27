
## ideation
The core difficulty is recognizing that each number requires a fixed number of selections before becoming zero: repeated floor division by 4 takes one step for values in [1, 3], two steps for [4, 15], three for [16, 63], and so on. An operation supplies two selections, so the query answer depends on the ceiling of half the total required selections, not simply on the number of elements.

The main implementation concerns are handling interval boundaries correctly, avoiding iteration over every value in a query, and using sufficiently wide integer arithmetic for the summed answer.

## worker: Implement the piecewise power-of-4 prefix-sum solu
Each value in `[4^(k-1), 4^k - 1]` requires exactly `k` selections to become zero. A single operation provides two selections, so a query with total selection requirement `S` needs `ceil(S / 2)` operations.

The prefix sum processes complete power-of-four intervals in `O(log_4 n)` time. Thus the total complexity is `O(q log_4 M)`, where `q` is the number of queries and `M` is the maximum endpoint.
