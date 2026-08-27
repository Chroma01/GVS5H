
## ideation
The problem asks for each time step \(t = 1 \dots N\) whether smoke exists at cell \((R,C)\) at time \(t+0.5\).  
Smoke movement: at each integer time \(t\), wind blows and all smoke shifts by the direction given by \(S[t]\). Immediately after the wind, if \((0,0)\) is empty, new smoke is generated there. Thus at time \(t+0.5\), the occupied cells are exactly the set of all suffix sums of the first \(t\) moves, including the empty suffix (origin).  

Formally, let \(P[i]\) be the prefix sum of the first \(i\) moves (\(P[0]=(0,0)\)). At time \(t+0.5\), smoke occupies the set \(\{P[t] - P[j] \mid 0 \le j \le t\}\). This equals \((R,C)\) iff there exists \(j\) such that \(P[j] = P[t] - (R,C)\).  

Thus for each \(t\) we only need to check whether the value \(P[t] - (R,C)\) is among the already seen prefix sums \(P[0], P[1], \dots, P[t]\). Since \((R,C) \neq (0,0)\), we can simply check against the set of prefix sums before adding the current one.

The algorithm is \(O(N)\): maintain a set of visited prefix sums, update the current position step by step, and test membership.

## worker: Implement the solution in Python according to the 
The solution is based on the observation that at time \(t+0.5\), the smoke occupies exactly the set of all suffix sums of the moves up to time \(t\). This transforms the problem into checking whether \(P[t] - (R,C)\) appears among previously seen prefix sums \(P[0], \dots, P[t]\). The algorithm iterates through the string once, maintaining a hash set of complex numbers representing the prefix sums. The time complexity is \(O(N)\) and space is \(O(N)\), which is efficient for \(N \le 200,000\). The provided code uses Python's built-in `complex` type for fast hashing and comparison. It correctly handles the input constraints and produces the correct output for the sample cases.
