import random

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def evaluate(self, x):
        result = 0
        for i, coeff in enumerate(self.coefficients):
            result += coeff * (x ** i)
        return result

class Prover:
    def __init__(self, polynomial):
        self.polynomial = polynomial

    def commit(self, generator):
        # Commit to a polynomial by computing the generator raised to the power of the polynomial evaluation
        return [generator ** coeff for coeff in self.polynomial.coefficients]

    def evaluate_polynomial(self, x):
        return self.polynomial.evaluate(x)

class Verifier:
    @staticmethod
    def verify(commitment, x, y, generator):
        print("VERIFifying")
        lhs = generator ** y  # generator raised to the value y
        print(f"LHS --> {lhs}")
        rhs = 1
        for i, c in enumerate(commitment):
            rhs *= c ** (x ** i)  # product of c_i raised to the power of x^i
            print(f"RHS ---> {rhs}")

        return lhs == rhs

def generate_random_scalar():
    return random.randint(1, 100)

if __name__ == "__main__":
    # Define a simple polynomial, for example: f(x) = 3 + 2x + x^2
    coefficients = [3, 2, 1]  # Represents the polynomial 3 + 2x + x^2
    polynomial = Polynomial(coefficients)

    # Initialize the Prover with the polynomial
    prover = Prover(polynomial)

    # Choose a random generator for the commitment (in practice, this would be a fixed value)
    # generator = generate_random_scalar()
    generator = 2

    # Prover creates a commitment to the polynomial
    commitment = prover.commit(generator)

    # Prover chooses a random point x to evaluate the polynomial
    # x = generate_random_scalar()
    x = 1
    y = prover.evaluate_polynomial(x)

    # Verifier checks the validity of the commitment
    verifier = Verifier()
    is_valid = verifier.verify(commitment, x, y, generator)

    print(f"Polynomial coefficients: {coefficients}")
    print(f"Random generator: {generator}")
    print(f"Commitment: {commitment}")
    print(f"Evaluation point (x): {x}")
    print(f"Evaluation result (y): {y}")
    print(f"Commitment valid: {is_valid}")
