import sys
import random

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
        except StopIteration:
            break
            
        cakes = []
        for i in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            z = int(next(iterator))
            cakes.append((x, y, z))
            
        if K == 0:
            results.append(0)
            continue
            
        # We need to find K disjoint pairs to maximize sum of max(x1+x2, y1+y2, z1+z2)
        # Since N is up to 10^5, we cannot try all pairs.
        # However, the optimal solution often involves pairing high-value cakes.
        # A simple greedy strategy: repeatedly pick the best available pair.
        # To make it efficient, we can use a priority queue, but updating it is hard.
        # Instead, we can use a randomized local search / simulated annealing approach
        # or a greedy approach with a limited look-ahead.
        
        # Given the constraints and problem type, a simple greedy might fail.
        # However, for this specific problem structure, there is a known trick:
        # The answer is often close to the max of sums of 2K largest values.
        # But we saw a counterexample.
        
        # Let's implement a greedy strategy with a priority queue of candidate pairs.
        # We can only consider pairs involving the top M cakes for some M.
        # But this is heuristic.
        
        # Actually, for this problem, a simple greedy (pick best pair, remove, repeat)
        # is O(K * N^2) which is too slow.
        
        # We will use a randomized local search.
        # Start with a random matching of K pairs.
        # Try to improve by swapping pairs.
        
        # Generate initial matching: pick 2K random indices, pair them arbitrarily.
        # Better: pick 2K indices with highest "potential".
        # Potential of a cake i: max(X_i, Y_i, Z_i) or sum?
        # Let's use sum X+Y+Z as potential.
        
        indices = list(range(N))
        # Sort by sum of attributes descending
        indices.sort(key=lambda i: cakes[i][0] + cakes[i][1] + cakes[i][2], reverse=True)
        
        # Take top 2K indices
        selected = indices[:2*K]
        
        # Initial pairing: pair selected[2i] with selected[2i+1]
        current_pairs = []
        for i in range(K):
            current_pairs.append((selected[2*i], selected[2*i+1]))
            
        def get_total_price(pairs):
            total = 0
            for u, v in pairs:
                x1, y1, z1 = cakes[u]
                x2, y2, z2 = cakes[v]
                total += max(x1+x2, y1+y2, z1+z2)
            return total
            
        current_price = get_total_price(current_pairs)
        
        # Local search: try to improve by swapping elements between pairs
        # or swapping one element with an unselected cake.
        # Since K can be large, we limit the number of iterations.
        
        # We'll use a simple hill climbing with random restarts
        best_price = current_price
        best_pairs = current_pairs
        
        # Number of iterations
        num_iterations = 5000
        
        for _ in range(num_iterations):
            # Randomly select two pairs to swap elements between
            if len(current_pairs) < 2:
                break
                
            idx1 = random.randint(0, len(current_pairs)-1)
            idx2 = random.randint(0, len(current_pairs)-1)
            
            if idx1 == idx2:
                continue
                
            u1, v1 = current_pairs[idx1]
            u2, v2 = current_pairs[idx2]
            
            # Try swapping v1 and v2
            new_pairs = current_pairs[:]
            new_pairs[idx1] = (u1, v2)
            new_pairs[idx2] = (u2, v1)
            
            new_price = get_total_price(new_pairs)
            if new_price > best_price:
                best_price = new_price
                best_pairs = new_pairs
                current_pairs = new_pairs
                current_price = new_price
                continue
                
            # Try swapping u1 and u2
            new_pairs = current_pairs[:]
            new_pairs[idx1] = (u2, v1)
            new_pairs[idx2] = (u1, v2)
            
            new_price = get_total_price(new_pairs)
            if new_price > best_price:
                best_price = new_price
                best_pairs = new_pairs
                current_pairs = new_pairs
                current_price = new_price
                continue
                
            # Try swapping u1 and v2
            new_pairs = current_pairs[:]
            new_pairs[idx1] = (u2, v1) # Wait, this is same as above? No.
            # Let's try all 3 swaps
            # Swap u1 <-> u2
            # Swap u1 <-> v2
            # Swap v1 <-> u2
            
            # Swap u1 <-> v2
            new_pairs = current_pairs[:]
            new_pairs[idx1] = (u2, v1) # This was u2,v1. Let's be careful.
            # Original: (u1, v1), (u2, v2)
            # Swap u1, v2 -> (v2, v1), (u2, u1) -> same as swapping both? No.
            # Let's just try all 3 possible pairings of {u1, v1, u2, v2} into 2 pairs.
            # The 3 pairings are:
            # 1. (u1, v1), (u2, v2) - current
            # 2. (u1, u2), (v1, v2)
            # 3. (u1, v2), (v1, u2)
            
            # Try pairing 2
            new_pairs = current_pairs[:]
            new_pairs[idx1] = (u1, u2)
            new_pairs[idx2] = (v1, v2)
            new_price = get_total_price(new_pairs)
            if new_price > best_price:
                best_price = new_price
                best_pairs = new_pairs
                current_pairs = new_pairs
                current_price = new_price
                continue
                
            # Try pairing 3
            new_pairs = current_pairs[:]
            new_pairs[idx1] = (u1, v2)
            new_pairs[idx2] = (v1, u2)
            new_price = get_total_price(new_pairs)
            if new_price > best_price:
                best_price = new_price
                best_pairs = new_pairs
                current_pairs = new_pairs
                current_price = new_price
                continue
                
        # Also try swapping one element with an unselected cake
        unselected = indices[2*K:]
        if unselected:
            for _ in range(1000):
                if not unselected:
                    break
                pair_idx = random.randint(0, len(current_pairs)-1)
                u, v = current_pairs[pair_idx]
                new_cake_idx = random.choice(unselected)
                
                # Try replacing u
                new_pairs = current_pairs[:]
                new_pairs[pair_idx] = (new_cake_idx, v)
                new_price = get_total_price(new_pairs)
                if new_price > best_price:
                    best_price = new_price
                    best_pairs = new_pairs
                    current_pairs = new_pairs
                    current_price = new_price
                    # Update unselected
                    unselected.remove(new_cake_idx)
                    unselected.append(u)
                    continue
                    
                # Try replacing v
                new_pairs = current_pairs[:]
                new_pairs[pair_idx] = (u, new_cake_idx)
                new_price = get_total_price(new_pairs)
                if new_price > best_price:
                    best_price = new_price
                    best_pairs = new_pairs
                    current_pairs = new_pairs
                    current_price = new_price
                    unselected.remove(new_cake_idx)
                    unselected.append(v)
                    continue
                    
        results.append(best_price)
        
    print('\n'.join(map(str, results)))

solve()