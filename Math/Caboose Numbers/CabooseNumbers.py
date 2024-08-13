from time import perf_counter
from functools import lru_cache

from sympy import isprime

UPPER_BOUND = 1_000_000_000
'''Limit to which to check for caboose numbers'''

MAX_CACHE_SIZE = 100_000_000
'''Limit that decides whether to set up an unbounded cache or not'''

if UPPER_BOUND < MAX_CACHE_SIZE:
    is_prime = lru_cache(maxsize = None)(isprime)
else:
    is_prime = isprime

def find_caboose(upper_bound: int):
    '''Checks for caboose numbers up to a specified limit'''

    caboose_eq = lambda m, n: (m * m) - m + n
    caboose_nums = [2] #2 is the only even caboose number

    n = 3 #Starting point of search
    start_time = perf_counter()

    while n <= upper_bound:
        #Can start from 2 since for m = 0 or m = 1, eq will always result in n which has been restricted here to always be a prime
        for m in range(2, n): 
            if not is_prime(caboose_eq(m, n)):
                break
        else: #Only executed if the for loop above completed without hitting a break
            print(f"Found caboose: {n:>6} | {perf_counter() - start_time:.4f}s")
            caboose_nums.append(n)
        
        n += 2 #Since even caboose numbers other than 2 are not possible
        while not is_prime(n): #Look for the next prime since composite caboose numbers are not possible
            n += 2

    return caboose_nums

if __name__ == "__main__":
    start_time = perf_counter()
    find_caboose(UPPER_BOUND)
    print(f"\nTime taken: {perf_counter() - start_time:.2f}s")

    if hasattr(is_prime, "cache_info"):
        cache_info = is_prime.cache_info()
        print(f"Cache hit ratio: {cache_info.hits / (cache_info.hits + cache_info.misses):.2%}")