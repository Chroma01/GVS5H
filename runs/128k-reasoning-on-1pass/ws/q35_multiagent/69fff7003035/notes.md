
## ideation


## worker: (none)
The problem asks for the sum of $f(P)$ over all permutations $P$ of $(1, \ldots, N)$, where $f(P)$ is the concatenation of elements.
We derived that the total sum can be computed by considering the contribution of each element $v$ at each position $i$.
The contribution depends on the number of digits of $v$ and the sum of lengths of elements to its right.
We used generating functions to compute the sum of $10^{\text{sum of lengths}}$ over all subsets of a given size.
The generating function $P(x) = \prod_{d=1}^6 (1 + 10^d x)^{cnt_d}$ encodes the lengths.
We computed coefficients of $P(x)$ using NTT.
Then for each digit length $d$, we computed $B^{(d)}_k$ which represents the sum for subsets excluding an element of length $d$.
Finally, we summed up the contributions using factorials to account for permutations.
The complexity is dominated by NTT, which is $O(N \log N)$.
