# Define the range for valid height values
BEGIN = 0  # Minimum height (exclusive)
END = 9    # Maximum height (exclusive)


def main():
    # Get the pyramid height from the user and print the pyramid
    print_pyramid(get_height())


# Function to print a pyramid of a given height
def print_pyramid(height):
    # Iterate through each level of the pyramid
    for i in range(1, height + 1):
        # Print spaces for alignment and '#' for the pyramid blocks
        print(" " * (height - i) + "#" * i)


# Function to check if the user input is valid
def is_valid_input(h):
    return h.isdigit() and int(h) > BEGIN and int(h) < END


def get_height():
    while True:
        height = input("Height: ")

        if is_valid_input(height):
            return int(height)


main()
