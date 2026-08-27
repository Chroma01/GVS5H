1. Simulate Santa's path step-by-step, tracking his current position.
2. For each move (U/D/L/R), determine the segment of movement.
3. For each segment, check which houses lie on that segment. Since moves are axis-aligned, a house (X_i, Y_i) is on a horizontal move if Y_i equals the current Y and X_i is between the start and end X coordinates. Similarly for vertical moves.
4. To efficiently find houses on each segment, we can preprocess the houses into two dictionaries: one mapping Y-coordinate to a sorted list of X-coordinates, and another mapping X-coordinate to a sorted list of Y-coordinates.
5. For each segment, use binary search (bisect) to find houses in the relevant range. Mark visited houses in a set to count distinct ones.
6. After processing all moves, output the final position and the count of distinct visited houses.