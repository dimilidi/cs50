from cs50 import get_string
import re


def main():
    # Prompt the user for some text
    text = get_string("Text: ")

    # Print the grade level
    print(find_grade_level(text))


def calculate_index(letters, words, scentences):
    # Calculate the Coleman-Liau index
    return round(0.0588 * (letters * 100 / words) - 0.296 * (scentences * 100 / words) - 15.8)


def find_grade_level(text):
    # Compute the Coleman-Liau index
    index = calculate_index(count_letters(text), count_words(text), count_sentences(text))

    # Return the appropriate grade level based on the index
    if index < 1:
        return "Before Grade 1"
    elif index >= 16:
        return "Grade 16+"
    else:
        return f"Grade {index}"


# Count the number of letters, words, and sentences in the text
def count_letters(text):
    letter_count = 0
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            letter_count += 1
    return letter_count


def count_words(text):
    return len(text.split())


def count_sentences(text):
    # Split the text into scentences and clean the array of empty strings and each scentence of whitespaces
    sentences = [s.strip() for s in re.split(r'[.!?](?=\s+[A-Z])', text) if s.strip()]
    return len(sentences)


main()
