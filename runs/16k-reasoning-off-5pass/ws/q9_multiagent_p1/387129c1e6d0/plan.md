1. Simulate Santa's movement step-by-step, updating his current coordinates $(x, y)$ for each command $(D_i, C_i)$.
2. For each horizontal or vertical move, determine the range of coordinates covered on that axis while the other axis remains fixed.
3. Use a hash set to store all house coordinates $(X_j, Y_j)$ that fall within the swept ranges of any move.
4. Finally, output the final coordinates and the count of unique houses found in the set.