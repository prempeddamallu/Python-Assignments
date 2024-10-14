# 4. Write a program that can map() to make a list whose elements are squares of numbers
# between 1 and 20 (both included).
# Hints:
# Use map() to generate a list.
# Use Lambda to define anonymous functions.


# Define the range of numbers from 1 to 20
numbers = range(1, 21)

# Use map() with a lambda function to compute squares
squares = list(map(lambda x: x ** 2, numbers))

# Print the result
print(squares)
