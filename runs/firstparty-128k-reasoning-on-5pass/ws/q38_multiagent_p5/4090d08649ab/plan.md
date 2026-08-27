Observe that for a fixed subarray, f(L,R) equals the number of connected components of the set of distinct values in that subarray on the integer line, because one operation can erase exactly one consecutive block of present values and each component can be erased in one operation.  
Therefore f(L,R) is the number of values x present in A[L..R] whose predecessor x-1 is absent.  
The required sum is the sum over x of the number of subarrays that contain x but do not contain x-1.  
For each x, count these subarrays by splitting the index range at occurrences of x-1 and, in each gap, counting subarrays that contain at least one occurrence of x.  
Store positions of each value and process all x in total O(N) time, using 64-bit integers.