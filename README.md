# Kraken Challenge Solver

This project solves the Kraken API's cryptographic challenge using a brute-force approach with double SHA-256 hashing. The solver fetches challenge data from Kraken's API, computes a solution based on the specified difficulty, and provides the solution in the required format.

## How it works

- Fetches necessary cookies (SLID) from the Kraken API.
- Retrieves challenge data with a difficulty parameter from Kraken's session API.
- Solves the cryptographic challenge using a brute-force method.
- Computes the solution using double SHA-256 hashing.
- Prints the solution and execution time.
