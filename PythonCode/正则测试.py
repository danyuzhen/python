import time
import random

a=[11,3,7,5,3,11,5,7,101]

b=0

for i in a:
    print(b,i,b^i)
    b=b^i
print()
print(b)