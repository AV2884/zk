import numpy as np
import matplotlib.pyplot as plt
import random
import sympy

# Convert the string to a list of ASCII values
def string_to_ascii(string):
    return [ord(char) for char in string]

# Plot the ASCII values
def plot_data(indices, ascii_values):
    plt.figure(figsize=(10, 5))
    plt.scatter(indices, ascii_values, color='blue')
    plt.plot(indices, ascii_values, color='orange')
    plt.title("Plot of ASCII values of the input string")
    plt.xlabel("Index in String")
    plt.ylabel("ASCII Value")
    plt.grid(True)
    plt.show()

# Fit a polynomial to the data
def fit_polynomial(indices, ascii_values, degree=3):
    coefficients = np.polyfit(indices, ascii_values, degree)
    polynomial = np.poly1d(coefficients)
    return polynomial

# Find the largest prime number within practical limits
def largest_prime():
    return sympy.prevprime(2**63)

# Polynomial class
class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def evaluate(self, x):
        result = 0
        for i, coeff in enumerate(self.coefficients):
            result += coeff * (x ** i)
        return result

# Prover class
class Prover:
    def __init__(self, polynomial):
        self.polynomial = polynomial

    def commit(self, generator):
        return [generator ** coeff for coeff in self.polynomial.coefficients]

    def evaluate_polynomial(self, x):
        return self.polynomial.evaluate(x)

# Verifier class
class Verifier:
    @staticmethod
    def verify(commitment, x, y, generator):
        lhs = generator ** y
        rhs = 1
        for i, c in enumerate(commitment):
            rhs *= c ** (x ** i)
        return lhs == rhs

if __name__ == "__main__":
    # Input string
    input_string = "Abhiveer is 16 years old"
    ascii_values = string_to_ascii(input_string)
    indices = list(range(len(ascii_values)))

    # Plot the data
    plot_data(indices, ascii_values)

    # Fit a polynomial to the data
    degree = 3  # You can adjust the degree based on the complexity you need
    fitted_polynomial = fit_polynomial(indices, ascii_values, degree)
    coefficients = list(fitted_polynomial.coefficients[::-1])  # Reverse for correct order

    # Print the fitted polynomial equation
    print(f"Fitted Polynomial: {fitted_polynomial}")

    # Initialize the Prover with the polynomial
    polynomial = Polynomial(coefficients)
    prover = Prover(polynomial)

    # Use the largest prime number as the generator
    generator = largest_prime()

    # Prover creates a commitment to the polynomial
    commitment = prover.commit(generator)

    # Prover chooses a random point x to evaluate the polynomial
    x = random.randint(1, 100)
    y = prover.evaluate_polynomial(x)

    # Verifier checks the validity of the commitment
    verifier = Verifier()
    is_valid = verifier.verify(commitment, x, y, generator)

    print(f"Input String: {input_string}")
    print(f"ASCII Values: {ascii_values}")
    print(f"Polynomial coefficients: {coefficients}")
    print(f"Largest Prime Generator: {generator}")
    print(f"Commitment: {commitment}")
    print(f"Evaluation point (x): {x}")
    print(f"Evaluation result (y): {y}")
    print(f"Commitment valid: {is_valid}")
