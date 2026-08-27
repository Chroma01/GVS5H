1. Read input and store people.
2. Create events for people: $(S_i, T_i, i)$.
3. Sort queries by $T_{min}$ (which depends on the min $S$ in $[L, R]$).
4. Use a sweep-line algorithm with a BIT to count/max query.
5. For each query, find min $S$ in $[L, R]$ using a segment tree.
6. Check the condition using the BIT.