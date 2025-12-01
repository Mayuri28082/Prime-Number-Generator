

def check_prime(num, primes):
    if num in primes:
        return True 
        
    if num < 2:
        return False 
        
    for each in primes:
        if num % each == 0 :
            return False 
    return True

def get_primes(n):
    num = 2 
    count = 0 
    
    primes = []
    
    while len(primes) < n:
        if check_prime(num, primes):
            primes.append(num)
            
        num += 1 
    return primes
