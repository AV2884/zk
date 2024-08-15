import hashlib

def keccak256(data):
    return hashlib.sha3_256(data).digest()

# Prover
def generate_proof_and_encrypted_age(seed, age_actual, age_to_prove):
    proof = keccak256(seed)
    encrypted_age = keccak256(seed)
    
    for i in range(1, 1 + age_actual - age_to_prove):
        proof = keccak256(proof)

    for i in range(1, age_actual + 1):
        encrypted_age = keccak256(encrypted_age)

    return proof, encrypted_age

# Trusted Party
def generate_verified_proof(proof, age_to_prove):
    verfied_age = proof

    for i in range(age_to_prove):
        verfied_age = keccak256(verfied_age)

    return verfied_age

# Verifier
def verify_age(encrypted_age, verfied_age):
    return encrypted_age == verfied_age

# Parameters
age_actual = 14
age_to_prove = 18
seed = b"88899988899998898989898"

# Prover generates proof and encrypted age
proof, encrypted_age = generate_proof_and_encrypted_age(seed, age_actual, age_to_prove)

# Trusted Party generates verified proof
verified_proof = generate_verified_proof(proof, age_to_prove)

# Verifier checks the proof against the encrypted age
is_verified = verify_age(encrypted_age, verified_proof)

print("My Age:\t\t", age_actual)
print("Age to Prove:\t", age_to_prove)

print("Proof:\t\t", proof.hex())
print("Encrypted Age:\t", encrypted_age.hex())
print("Verified Proof:\t", verified_proof.hex())

if is_verified:
    print("You have proven your age ... please come in")
else:
    print("You have not proven your age!")
