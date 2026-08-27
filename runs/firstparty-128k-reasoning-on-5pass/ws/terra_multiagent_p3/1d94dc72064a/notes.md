- **State compression:** After some indices have entered `S`, all visited piles are interchangeable. Let `R` be the total remaining value among visited piles, and let `U` be the multiset of values at unvisited indices. A move either spends one token from `R`, or claims an unvisited pile of value `a`, producing `(U \\ {a}, R + a - 1)`.
- **Why values only matter by parity:** Spending from `R` alternates turns. When a pile is claimed, it contributes `a - 1` future spendable moves, so only the parity of `a` affects the winner.
- **Exhaustive small-state recurrence:** Let `W(U,R)` mean the current player wins. For one unvisited pile, every state is winning because it can be claimed immediately. For two unvisited piles, `W` holds exactly when `R` is odd.
- **Three unvisited piles:** Exhaustive recurrence gives:
  - if the three pile parities are mixed, every `R` is winning;
  - if all are odd, winning exactly for even `R`;
  - if all are even, winning exactly for odd `R`.
  Therefore, initially (`R=0`), Fennec wins iff at least one pile is odd.
- **Four or more unvisited piles:** The stable recurrence is:
  `W(U,R)` holds iff `R mod 2 = 1 - (#odd(U) mod 2)`.
  Claiming any pile transfers to a state with one fewer unvisited pile; substituting the changed resource parity and odd count proves the condition by induction from four piles onward.
- **Initial winner criterion:** Initially `R=0`.
  - `N=1`: Fennec.
  - `N=2`: Snuke.
  - `N=3`: Fennec iff at least one `A_i` is odd.
  - `N>=4`: Fennec iff the number of odd `A_i` is odd.
- **Complexity:** Count odd values in `O(N)` time and use `O(1)` extra space besides input storage.
- **Sorting:** Sorting and exact pile magnitudes are unnecessary for this game; exhaustive state analysis shows only `N` and the parities of pile values affect the outcome.
