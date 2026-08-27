Maintain a global offset `O` that records the cumulative displacement caused by the wind.  
All smoke pieces are stored as **relative coordinates** with respect to this offset, i.e. the absolute position of a piece at time `t` is `O(t) + s` for a stored `s`.  
Initially `O=(0,0)` and the set `rel = {(0,0)}`.  
For each step `t = 1..N`  

1. update `O` by the direction of `S[t]`,  
2. check whether the cell `(R,C)` is occupied: it is present iff `(R−O.r , C−O.c)` is in `rel`.  
3. after translation, a new piece is generated at the origin only if the origin is empty, i.e. iff `(-O.r , -O.c)` is **not** already in `rel`. In that case insert it.

All operations are O(1) average using a Python `set`, so the whole algorithm runs in O(N) time and O(N) memory.