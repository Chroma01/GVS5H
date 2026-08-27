1. Sort the three arrays in non‑increasing order.  
2. Observe that for fixed `j,k` the value  
   `S(i,j,k) = A[i]*B[j] + B[j]*C[k] + C[k]*A[i]`  
   is non‑increasing when `i` increases, and similarly for the other two indices.  
   Hence the largest values are obtained by small indices, and every triple can be reached from `(0,0,0)` by repeatedly increasing one index.  
3. Use a max‑heap (implemented with `heapq` and negative values) that stores triples `(i,j,k)`.  
   Start with `(0,0,0)`.  
   Each time we pop a triple we push its three “neighbors” `(i+1,j,k)`, `(i,j+1,k)`, `(i,j,k+1)` if they are inside the arrays and not visited before.  
   Because the function is monotone, the heap always contains the next largest unvisited triple, so extracting the heap `K` times yields the values in descending order.  
4. The K‑th popped value is the required answer.