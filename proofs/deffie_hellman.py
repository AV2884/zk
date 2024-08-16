import random

# Constants
n = 2**255 - 19
g = 26959946667150639794667015087019630673557916260026308143510066298881

# ALICE: Chooses a secret number a
input_string = "Client Password"
a = int("".join(str(ord(char)) for char in input_string)) 
A = pow(g, a, n)  # Alice computes A = g^a mod n

# BOB: Chooses a secret number b
input_string = "Server verification password"
b = int("".join(str(ord(char)) for char in input_string)) 
B = pow(g, b, n)  # Bob computes B = g^b mod n

# ALICE and BOB exchange A and B publicly
print("ALICE sends to BOB:")
print(f"A = {A}")
print("")

print("BOB sends to ALICE:")
print(f"B = {B}")
print("")

# ALICE: Computes the shared secret using Bob's public value B
input_string = "wrong client Password"
# a = int("".join(str(ord(char)) for char in input_string)) 
shared_secret_Alice = pow(B, a, n)  # Alice computes S = B^a mod n

# BOB: Computes the shared secret using Alice's public value A
shared_secret_Bob = pow(A, b, n)  # Bob computes S = A^b mod n

# Both ALICE and BOB should have the same shared secret
print("ALICE and BOB both compute the shared secret:")
print(f"Shared Secret (Alice): {shared_secret_Alice}")
print(f"Shared Secret (Bob): {shared_secret_Bob}")
print("")

if shared_secret_Alice == shared_secret_Bob:
    print("Diffie-Hellman key exchange successful: ALICE and BOB have the same shared secret.")
else:
    print("Diffie-Hellman key exchange failed: ALICE and BOB do not have the same shared secret.")
