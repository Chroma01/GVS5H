Treat the small target array as a bitmask universe.  
For each possible subset of targets, compute its lcm and the cost to increment a given nums element to the next multiple of that lcm.  
Process nums elements with a DP where dp[mask] is the minimum cost to have covered the targets in mask.  
For each element, transition by either not using it or assigning it to cover any subset, adding the subset's cost and OR-ing the mask.  
This naturally allows one incremented element to satisfy multiple targets while preventing the same element from being used twice.  
The answer is dp[full_mask], with complexity easily within limits because target length is at most 4.