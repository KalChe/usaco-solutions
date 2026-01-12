## tc8 wrong, tc11 tle

from collections import deque
import sys

MOD=10**9+7
INV=pow(2, MOD-2, MOD)

full = sys.stdin.read().split()
n, d = int(full[0]), int(full[1])



#n,d = map(int, input().split())
position, type = [0]*n, [0]*n

i2 = 2
for i in range(n):
    position[i] = int(full[i2])
    type[i] = int(full[i2+1])
    i2+=2

#for i in range(n):
#    p,t = map(int, input().split())
#    position[i] = p
#    type[i] = t

bad, good, leftm, leftinv=1, 0, 1, 1
deck=deque()
l, i=0, 0

while(i<n):    
    p=position[i]
    t=type[i]
    diffs= p-d
    while(l<i and position[l]<diffs):
        l+=1
    while(deck and deck[0][1]<l):
        v,temp=deck.popleft()
        r=(v*leftm)%MOD
        good=(good-r)%MOD
        bad=(bad+r)%MOD
    if(t==0):
        if(good):
            good=(good*2)%MOD
            leftm=(leftm*2)%MOD
            leftinv=(leftinv*INV)%MOD
            #eftinv*=INV
            #leftinv = leftinv%MOD

    else:
        sum=(good+bad)%MOD
        good=(good+sum)%MOD
        deck.append(((sum*leftinv)%MOD,i))
    i=i+1

sum=(good+bad)%MOD-1
print(sum)