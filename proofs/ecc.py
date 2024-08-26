import hashlib
from random import randint

# Elliptic curve parameters for secp256k1 (used in Bitcoin and Ethereum)
a = 0
b = 7
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (Gx, Gy)

# Define the point addition function
def point_add(P, Q, p):
    if P is None:
        return Q
    if Q is None:
        return P
    
    if P == Q:
        lam = (3 * P[0]**2 + a) * pow(2 * P[1], p - 2, p) % p
    else:
        if P[0] == Q[0] and P[1] != Q[1]:
            return None
        lam = (Q[1] - P[1]) * pow(Q[0] - P[0], p - 2, p) % p

    x_r = (lam**2 - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p

    return (x_r, y_r)

# Define the point multiplication function
def point_multiply(k, P, p):
    R = None
    Q = P

    while k:
        if k & 1:
            R = point_add(R, Q, p)
        Q = point_add(Q, Q, p)
        k >>= 1

    return R

# Generate a key pair
def gen_key_pair(G, n, p):
    d = randint(1, n - 1)
    Q = point_multiply(d, G, p)
    return d, Q

# Hashing function using Keccak-256
def keccak256(data):
    return hashlib.sha3_256(data).digest()

# Sign a message
def sign(message, private_key, G, n, p):
    z_hex = keccak256(message).hex()
    z = int(z_hex, 16) % n
    while True:
        k = randint(1, n - 1)
        R = point_multiply(k, G, p)
        r = R[0] % n
        if r == 0:
            continue
        s = (pow(k, n - 2, n) * (z + r * private_key)) % n
        if s == 0:
            continue
        break
    return (r, s), z_hex

# Verify a signature
def verify_sign(message, signature, public_key, G, n, p):
    r, s = signature
    z_hex = keccak256(message).hex()
    z = int(z_hex, 16) % n
    w = pow(s, n - 2, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    X = point_add(point_multiply(u1, G, p), point_multiply(u2, public_key, p), p)
    return r == X[0] % n, z_hex

# Derive the Ethereum address from the public key
def derive_ethereum_address(public_key):
    # Concatenate the x and y coordinates of the public key
    public_key_hex = '04' + format(public_key[0], '064x') + format(public_key[1], '064x')
    public_key_bytes = bytes.fromhex(public_key_hex)
    keccak_hash = keccak256(public_key_bytes)
    eth_address = '0x' + keccak_hash[-20:].hex()
    return eth_address


def format_signature_ethereum(r, s):
    r_hex = format(r, '064x')  # 32 bytes, padded with zeros
    s_hex = format(s, '064x')  # 32 bytes, padded with zeros
    return r_hex + s_hex


# Generate a key pair
private_key, public_key = gen_key_pair(G, n, p)
public_key_eth_format = derive_ethereum_address(public_key)

# Convert the private key and public key to hexadecimal
private_key_hex = hex(private_key)
public_key_hex = (hex(public_key[0]), hex(public_key[1]))

# Sign a message
message = "Hello, ECC!"
signature, z_hex = sign(message.encode(), private_key, G, n, p)
r, s = signature
signature_eth_format = format_signature_ethereum(r, s)
# message = "Bye, ECC!"
# Verify the signature
valid, z_hex_verify = verify_sign(message.encode(), signature, public_key, G, n, p)

# Print the results
print(f"Private Key (Hex):\n\t{private_key_hex}")
print(f"Public Key (Hex):\n\tx: {public_key_hex[0]}\n\ty: {public_key_hex[1]}")
print(f"Public Key (Ethereum Format):\n\t{public_key_eth_format}")
print("Signature (r, s):\n\tr: {}\n\ts: {}".format(r, s))
print(f"Signature (Ethereum Format):\n\t{signature_eth_format}")
print(f"Message Hash (Hex):\n\t{z_hex}")
print(f"Signature valid:\n\t{'True' if valid else 'False'}")