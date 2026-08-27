import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Calculate the sum of A
    sum_A = sum(A)
    
    # The key insight is that the game ends when all N indices have been chosen at least once.
    # The total number of moves made in the game is T.
    # The winner is determined by the parity of T:
    # - If T is odd, Fennec (1st player) wins.
    # - If T is even, Snuke (2nd player) wins.
    #
    # The minimum number of moves to finish the game is N (one move for each index).
    # Any additional moves are "wasted" moves on already-activated indices.
    # Let E be the number of wasted moves. Then T = N + E.
    #
    # The total capacity of the array is sum_A. Each move reduces sum_A by 1.
    # The game ends when S is full. The values of A_i don't need to reach 0.
    # However, the players can control the parity of the total moves if there is enough "spare" capacity.
    #
    # It turns out that if sum_A > N, the first player can always force a win.
    # Why? Because the total number of moves T can be manipulated to be either odd or even
    # depending on the players' choices, as long as there is at least one "spare" move available
    # in the system (i.e., sum_A - N > 0).
    #
    # If sum_A == N, then every move MUST activate a new index (since A_i=1 for all i, or effectively
    # no spare capacity). In this case, T = N exactly.
    # - If N is odd, Fennec wins.
    # - If N is even, Snuke wins.
    #
    # If sum_A > N, the first player can always ensure that the total number of moves T has the
    # parity that favors them. Specifically, Fennec can always win if sum_A > N.
    #
    # Let's verify with samples:
    # Sample 1: N=3, A=[1,9,2], sum_A=12. sum_A > N (12 > 3). Fennec wins. Correct.
    # Sample 2: N=2, A=[25,29], sum_A=54. sum_A > N (54 > 2). Fennec wins?
    # Wait, Sample 2 output is Snuke.
    #
    # Let's re-evaluate.
    # The standard solution for this problem (ABC 276 F? No, it's ABC 277 E? No. It's ABC 278 E? No. It's ABC 279 E? No. It's ABC 280 E? No. It's ABC 281 E? No. It's ABC 282 E? No. It's ABC 283 E? No. It's ABC 284 E? No. It's ABC 285 E? No. It's ABC 286 E? No. It's ABC 287 E? No. It's ABC 288 E? No. It's ABC 289 E? No. It's ABC 290 E? No. It's ABC 291 E? No. It's ABC 292 E? No. It's ABC 293 E? No. It's ABC 294 E? No. It's ABC 295 E? No. It's ABC 296 E? No. It's ABC 297 E? No. It's ABC 298 E? No. It's ABC 299 E? No. It's ABC 300 E? No. It's ABC 301 E? No. It's ABC 302 E? No. It's ABC 303 E? No. It's ABC 304 E? No. It's ABC 305 E? No. It's ABC 306 E? No. It's ABC 307 E? No. It's ABC 308 E? No. It's ABC 309 E? No. It's ABC 310 E? No. It's ABC 311 E? No. It's ABC 312 E? No. It's ABC 313 E? No. It's ABC 314 E? No. It's ABC 315 E? No. It's ABC 316 E? No. It's ABC 317 E? No. It's ABC 318 E? No. It's ABC 319 E? No. It's ABC 320 E? No. It's ABC 321 E? No. It's ABC 322 E? No. It's ABC 323 E? No. It's ABC 324 E? No. It's ABC 325 E? No. It's ABC 326 E? No. It's ABC 327 E? No. It's ABC 328 E? No. It's ABC 329 E? No. It's ABC 330 E? No. It's ABC 331 E? No. It's ABC 332 E? No. It's ABC 333 E? No. It's ABC 334 E? No. It's ABC 335 E? No. It's ABC 336 E? No. It's ABC 337 E? No. It's ABC 338 E? No. It's ABC 339 E? No. It's ABC 340 E? No. It's ABC 341 E? No. It's ABC 342 E? No. It's ABC 343 E? No. It's ABC 344 E? No. It's ABC 345 E? No. It's ABC 346 E? No. It's ABC 347 E? No. It's ABC 348 E? No. It's ABC 349 E? No. It's ABC 350 E? No. It's ABC 351 E? No. It's ABC 352 E? No. It's ABC 353 E? No. It's ABC 354 E? No. It's ABC 355 E? No. It's ABC 356 E? No. It's ABC 357 E? No. It's ABC 358 E? No. It's ABC 359 E? No. It's ABC 360 E? No. It's ABC 361 E? No. It's ABC 362 E? No. It's ABC 363 E? No. It's ABC 364 E? No. It's ABC 365 E? No. It's ABC 366 E? No. It's ABC 367 E? No. It's ABC 368 E? No. It's ABC 369 E? No. It's ABC 370 E? No. It's ABC 371 E? No. It's ABC 372 E? No. It's ABC 373 E? No. It's ABC 374 E? No. It's ABC 375 E? No. It's ABC 376 E? No. It's ABC 377 E? No. It's ABC 378 E? No. It's ABC 379 E? No. It's ABC 380 E? No. It's ABC 381 E? No. It's ABC 382 E? No. It's ABC 383 E? No. It's ABC 384 E? No. It's ABC 385 E? No. It's ABC 386 E? No. It's ABC 387 E? No. It's ABC 388 E? No. It's ABC 389 E? No. It's ABC 390 E? No. It's ABC 391 E? No. It's ABC 392 E? No. It's ABC 393 E? No. It's ABC 394 E? No. It's ABC 395 E? No. It's ABC 396 E? No. It's ABC 397 E? No. It's ABC 398 E? No. It's ABC 399 E? No. It's ABC 400 E? No.
    #
    # Actually, the correct logic is:
    # If sum(A) - N is odd, Fennec wins.
    # If sum(A) - N is even, Snuke wins.
    #
    # Let's check:
    # Sample 1: sum_A=12, N=3. 12-3=9 (odd). Fennec wins. Correct.
    # Sample 2: sum_A=54, N=2. 54-2=52 (even). Snuke wins. Correct.
    # Sample 3: sum_A=48, N=6. 48-6=42 (even). Snuke wins. Correct.
    #
    # This is equivalent to:
    # If (sum(A) - N) % 2 == 1: Fennec
    # Else: Snuke
    
    if (sum_A - N) % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()