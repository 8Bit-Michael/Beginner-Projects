values = {chr(i): i - 96 for i in range(97, 123)}
reverse_values = {v: k for k, v in values.items()}

print("""Welcome to my number to word translator!
Enter numbers separated by spaces.
For example, if you enter 1 2 3, you will get back abc.""")

numbers = input("Enter numbers separated by spaces: ")
number_list = numbers.split()

valid = True
converted_numbers = []

for num_str in number_list:
    try:
        num = int(num_str)
        if num not in reverse_values:
            print(f"The number {num} does not correspond to a letter (1-26).")
            valid = False
        else:
            converted_numbers.append(reverse_values[num])
    except ValueError:
        print(f"'{num_str}' is not a valid number.")
        valid = False

if valid:
    print("The translated word is:", ''.join(converted_numbers))
