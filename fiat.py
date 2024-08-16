
import random

# Constants
n = 2**255 - 19
g = 26959946667150639794667015087019630673557916260026308143510066298881

# Alice's secrets
input_string = "client password"
x = int("".join(str(ord(char)) for char in input_string)) 
print(f"Alice's data {x}")
v = random.randint(1, 2**80)  # Alice's random value

# Bob's challenge
c = random.randint(1, 2**80)

# ALICE: Compute y and t, and send them to Bob
y = pow(g, x, n)
t = pow(g, v, n)

print(f"Both agree on g = {g}")

print("ALICE sends:")
print(f"y = {y}")
print(f"t = {t}")
print("")

# BOB: Sends challenge c to Alice
print("BOB sends:")
print(f"c = {c}")
print("")

# ALICE: Computes r and Result
z = 2347865 #If Alice wants to cheat
r = v - c * x
print("ALICE sends:")
print(f"r = {r}")
print("")

Result = (pow(g, r, n) * pow(y, c, n)) % n

# BOB: Verifies if Alice knows x by checking if t == Result
print("BOB verifies:")
print(f"t = {t}")
print(f"Result = {Result}")

if t == Result:
    print("Alice has proven she knows x")
else:
    print("Alice has not proven she knows x")
