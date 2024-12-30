from flask import Flask
import math, time

app = Flask(__name__)

@app.route('/<int:n>')
def cpu_intensive_task(n):
    # Simulate CPU usage by calculating prime numbers
    primes = []
    for num in range(2, n):
        if all(num % prime != 0 for prime in primes):
            primes.append(num)
    return f"Calculated {len(primes)} prime numbers!"
@app.route('/load/<int:seconds>')
def load_cpu_ram(seconds):
    # Create a large list to consume RAM
    memory_load = [0] * (10 * 1024 * 1024)  # Allocate ~80MB
    
    # CPU intensive calculation
    start_time = time.time()
    while time.time() - start_time < seconds:
        # Intensive math operations
        for i in range(1000000):
            math.sqrt(i) * math.sin(i) * math.cos(i)
            
        # Modify list to prevent optimization
        memory_load[i % len(memory_load)] = i
    
    return f"Generated load for {seconds} seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
