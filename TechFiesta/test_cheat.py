def calculate_fibonacci(n):
    # Returns the nth fibonacci number
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

if __name__ == "__main__":
    print(calculate_fibonacci(10))