import random
import sympy
import numpy as np

# Polynomial class
class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def evaluate(self, x, p):
        result = 0
        for i, coeff in enumerate(self.coefficients):
            result += coeff * pow(x, i, p)
            result %= p  # Apply modulus p to keep the result within range
        return result

# Prover class
class Prover:
    def __init__(self, polynomial):
        self.polynomial = polynomial

    def commit(self, generator, p):
        return [pow(generator, coeff, p) for coeff in self.polynomial.coefficients]

    def evaluate_polynomial(self, x, p):
        return self.polynomial.evaluate(x, p)

# Verifier class
class Verifier:
    @staticmethod
    def verify(commitment, x, y, generator, p):
        lhs = pow(generator, y, p)
        rhs = 1
        for i, c in enumerate(commitment):
            rhs *= pow(c, pow(x, i, p), p)
            rhs %= p  # Apply modulus p to keep rhs within range
        return lhs == rhs

def string_to_ascii(string):
    return [ord(char) for char in string]

# Plot the ASCII values
# def plot_data(indices, ascii_values):
#     plt.figure(figsize=(10, 5))
#     plt.scatter(indices, ascii_values, color='blue')
#     plt.plot(indices, ascii_values, color='orange')
#     plt.title("Plot of ASCII values of the input string")
#     plt.xlabel("Index in String")
#     plt.ylabel("ASCII Value")
#     plt.grid(True)
#     plt.show()

# Fit a polynomial to the data
def fit_polynomial(indices, ascii_values):
    degree = len(ascii_values) - 1  # Degree of the polynomial
    coefficients = np.polyfit(indices, ascii_values, degree)
    polynomial = np.poly1d(coefficients)
    return polynomial


if __name__ == "__main__":
    input_string = "AV is 16 years old"

    # Convert the string to ASCII values
    ascii_values = string_to_ascii(input_string)
    indices = list(range(len(ascii_values)))

    # Fit a polynomial to the data
    fitted_polynomial = fit_polynomial(indices, ascii_values)
    
    # Print the polynomial equation
    print("Fitted Polynomial Equation:")
    print(fitted_polynomial)

    # Convert polynomial coefficients to integers
    coefficients = [int(round(coeff)) for coeff in fitted_polynomial.coefficients]
    polynomial = Polynomial(coefficients)
    
    prover = Prover(polynomial)

    p = 2**255 - 19
    generator = 26959946667150639794667015087019630673557916260026308143510066298881

    # Prover creates a commitment to the polynomial
    commitment = prover.commit(generator, p)

    # Prover chooses a random point x to evaluate the polynomial
    x = random.randint(1, 100)
    y = prover.evaluate_polynomial(x, p)

    # Verifier checks the validity of the commitment
    verifier = Verifier()
    is_valid = verifier.verify(commitment, x, y, generator, p)

    print(f"Polynomial coefficients: {coefficients}")
    print(f"Prime Modulus (p): {p}")
    print(f"Generator: {generator}")
    print(f"Commitment: {commitment}")
    print(f"Evaluation point (x): {x}")
    print(f"Evaluation result (y): {y}")
    print(f"Commitment valid: {is_valid}")