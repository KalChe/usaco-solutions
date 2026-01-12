import sys

Fmod = int(1e9 + 7)

def power(base, exp, mod):
    mod = Fmod
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2  
    return result

def inverse(a, mod):
    mod = Fmod
    return power(a, mod - 2, mod)

K, N, L = map(int, input().split())
T = input().strip()

Ms = 0
Os = 0
string = []

for character in T:
    if character == 'M':
        Ms += 1
    else:
        Os += 1
        string.append(Ms)

if(Os != Ms * K):
    print(0)
    sys.exit()

product = 1

for i in range(1, Os+1):
    term = (K * string[i - 1]) % Fmod
    term = (term - (i - 1)) % Fmod
    if term < 0:
        term += Fmod
    product = (product * term) % Fmod

f = 1
for i in range(1, K + 1):
    f = (f *i) % Fmod

under = power(f, Ms, Fmod)
inv = inverse(under, Fmod)
L1 = (product * inv) % Fmod

ans = power(L1, L, Fmod)
print(ans % Fmod)