import re

# Define card dictionary with prefixes and valid lengths
cards = {
    "AMEX": {"prefixes": [34, 37], "lengths": [15]},
    "MASTERCARD": {"prefixes": [51, 52, 53, 54, 55], "lengths": [16]},
    "VISA": {"prefixes": [4], "lengths": [13, 16]},
}


def main():
    card_number = get_input()
    print(find_card_type(card_number))


# Determine the card type based on its number
def find_card_type(card_number):
    if not is_valid(card_number):
        return "INVALID"

    for card_type, details in cards.items():
        if matches_card_type(card_number, details):
            return card_type

    return "INVALID"


def matches_card_type(card_number, details):
   # Check if the card number matches the given card type's prefixes and length
    prefixes = details["prefixes"]
    lengths = details["lengths"]
    first_two_digits = int(card_number[:2])
    first_digit = int(card_number[0])
    card_length = len(card_number)

    # Check for prefix and length conditions
    return (first_two_digits in prefixes or first_digit in prefixes) and card_length in lengths


# Function to validate card_number
def is_valid(card_number):

    # Ensure the input is numeric
    if not re.match(r"^\d+$", card_number):
        return False

    total = 0
    reversed = card_number[::-1]

    # Apply Luhn algorithm
    for i, digit in enumerate(reversed):
        digit = int(digit)
        # Double every second digit and sum the new digits
        if i % 2 != 0:
            doubled = digit * 2
            total += sum(int(x) for x in str(doubled))
        else:
            # Add digits at even indices directly
            total += digit

    # Check if the total sum is divisible by 10
    return total % 10 == 0


# Function to prompt the user for card number input and trim whitespace
def get_input():
    return input("Number: ").strip()


main()
