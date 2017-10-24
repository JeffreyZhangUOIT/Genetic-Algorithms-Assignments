import random as r
import matplotlib.pyplot as plt

u = []
v = []
frontx = []
fronty = []

print "Generating 50 random numbers in the form (u, v)"

for i in range(100):
    u.append(r.randint(0, 100))
    v.append(r. randint(0, 100))

# Assuming max-max
for i in range(0, len(u)):
    NotDominated = True
    for j in range(0, len(u)):
        if (u[i] < u[j]) and (v[i] < v[j]):
            NotDominated = False
    if NotDominated:
        frontx.append(u[i])
        fronty.append(v[i])

plt.plot(u, v, 'ro')
plt.plot(frontx, fronty, 'bo')
print u, v
print frontx, fronty
plt.show()



