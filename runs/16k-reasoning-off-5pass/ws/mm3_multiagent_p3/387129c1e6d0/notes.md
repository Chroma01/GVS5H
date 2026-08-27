
## ideation
The core difficulty is efficiently determining which houses lie on each axis-aligned move, while avoiding double counting when a house could be found via both its x-group and y-group. We must also handle large coordinates (up to 1e9) and large counts (up to 2e5).  
Candidate approaches:  
1. **Brute force per move**: iterate all houses → O(NM) too slow.  
2. **Grid/hash set of visited houses**: for each move, check all houses in a rectangle → still too slow.  
3. **Bucket by y for horizontal moves, bucket by x for vertical moves**: keep sorted lists for fast range queries. Remove houses from both buckets upon first visit to guarantee O(N) total extractions.  
Pitfalls:  
- Using a visited flag without removal could cause O(NM) in worst case if a house is in the range of many moves.  
- Integer overflow in final coordinates (use Python int).  
- Correct inclusive boundaries for the move (both endpoints).  
- Removing from the opposite bucket must be done immediately to keep the invariant that buckets contain only unvisited houses.  
- Using `defaultdict` can accidentally create empty lists if a key is missing; we only access keys that must exist.

## worker: Implement the solution in Python: read input, buil
We use two dictionaries keyed by x and y respectively. Each key maps to a sorted list of `(other_coordinate, house_id)` pairs.  
For each move, we binary search the relevant list to find the range of houses lying on the segment. We then iterate over that slice, increment the count, and immediately remove the house from the opposite bucket to keep the invariant that buckets contain only unvisited houses.  
Because each house is removed from both buckets exactly once, the total number of house processing steps is O(N), giving an overall time complexity of O((N+M) log N) and O(N) memory.
