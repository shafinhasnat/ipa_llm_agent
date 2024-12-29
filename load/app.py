from flask import Flask
import math

app = Flask(__name__)

@app.route('/<int:n>')
def cpu_intensive_task(n):
    # Simulate CPU usage by calculating prime numbers
    primes = []
    for num in range(2, n):
        if all(num % prime != 0 for prime in primes):
            primes.append(num)
    return f"Calculated {len(primes)} prime numbers!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
