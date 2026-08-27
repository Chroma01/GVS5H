import sys
import heapq

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        N, K = map(int, input().split())
        cakes = []
        for _ in range(N):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        best = 0
        # Try sorting by each coordinate (descending)
        for dim in range(3):
            # Sort by the chosen coordinate in descending order
            sorted_cakes = sorted(cakes, key=lambda c: -c[dim])
            
            # Compute price for each adjacent pair in the sorted order
            prices = [0] * (N - 1)
            for i in range(N - 1):
                a = sorted_cakes[i]
                b = sorted_cakes[i+1]
                p = max(a[0] + b[0], a[1] + b[1], a[2] + b[2])
                prices[i] = p
            
            # Greedy selection of K non-overlapping edges from a path graph
            heap = [(-prices[i], i) for i in range(N - 1)]
            heapq.heapify(heap)
            
            vertex_used = [False] * N
            total = 0
            count = 0
            
            while heap and count < K:
                neg_p, i = heapq.heappop(heap)
                p = -neg_p
                if vertex_used[i] or vertex_used[i + 1]:
                    continue
                total += p
                count += 1
                vertex_used[i] = True
                vertex_used[i + 1] = True
            
            if total > best:
                best = total
        
        print(best)

if __name__ == "__main__":
    solve()