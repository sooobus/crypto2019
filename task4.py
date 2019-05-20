from random import randint
import math
from tqdm import tqdm

import hashlib
from sympy import mod_inverse


def naive_mod_pow(n, m, p):
    if m == 0:
        return 1
    else:
        half = m // 2
        half_pow = naive_mod_pow(n, half, p) % p
        if m % 2 == 0:
            return (half_pow * half_pow) % p
        else:
            return (half_pow * half_pow * n) % p


def is_prime(n):
    for i in range(2, math.ceil(math.sqrt(n))):
        if n % i == 0:
            return False
    return True


def get_large_prime(seed):
    for i in range(seed, seed + 1000):
        if is_prime(i):
            return i


def get_prime_divisor(n):
    for i in tqdm(range(math.ceil(math.sqrt(n)), 1, -1)):
        if n % i == 0 and is_prime(i):
            return i


def get_g(q, p):  #g ** q == 1 (p)
    while True:
        g = randint(1, p - 1)
        if naive_mod_pow(g, q, p) == 1:
            return g

def schnorr(m):
    p = get_large_prime(82194)  # truly random generated using my keyboard and fingers
    q = get_prime_divisor(p - 1)
    r = randint(2, q - 1)
    w = randint(2, q - 1)
    g = get_g(q, p)
    x = naive_mod_pow(g, r, p)
    y = mod_inverse(naive_mod_pow(g, w, p), p)

    hash = hashlib.sha256()
    hash.update(m + str(x).encode())
    s1 = int.from_bytes(hash.digest(), byteorder='big')
    s2 = r + (w * int(s1)) % q

    open = (p, q, g, y)
    return s1, s2, open

def check_schnorr(m, s1, s2, open):
    p, q, g, y = open
    X = (naive_mod_pow(g, s2, p) * naive_mod_pow(y, s1, p)) % p
    hash = hashlib.sha256()
    hash.update(m + str(X).encode())
    s1_ = int.from_bytes(hash.digest(), byteorder='big')
    if s1_ == s1:
        return True
    else:
        return False


def crack_schnorr(s1, s2, w_, open):
    p, q, g, y = open
    t1 = s2 * mod_inverse(s2 - w_ * s1, q)
    t2 = s1 * mod_inverse(s2 - w_ * s1, q)
    print(g, t1, y, t2)
    g_ = (naive_mod_pow(g, t1, p) * naive_mod_pow(y, t2, p)) % p
    y_ = mod_inverse(naive_mod_pow(g_, w_, p), p)
    return p, q, g_, y_


m = b"lalala"
s1, s2, open = schnorr(m)
print(check_schnorr(m, s1, s2, open))

new_open = crack_schnorr(s1, s2, randint(2, open[1] - 1), open)
print(open)
print(new_open)
print(check_schnorr(m, s1, s2, new_open))