import csv
import sys


def main():

    # Check for command-line usage
    check_arguments()

    # Read database file into a variable
    database = read_database(sys.argv[1])

    # Read DNA sequence file into a variable
    sequence = read_sequence(sys.argv[2])

    # Find longest match of each STR in DNA sequence
    str_counts = find_str_counts(sequence, database[0].keys())

    # Check database for matching profiles
    find_matching_profile(database, str_counts)


def check_arguments():
    if len(sys.argv) != 3:
        print("3 command line arguments required: dny.py data.csv sequence.txt")
        sys.exit(1)


def read_database(file_path):
    # Create dictionary from database csv file
    with open(file_path, "r") as database_file:
        reader = csv.DictReader(database_file)
        return [row for row in reader] # [{"name":"Alice", "AGATC":"15", "TTTTTTCT":"20", ...}, {"name":"Tom", ...}]


def read_sequence(file_path):
    # Read DNA sequence file as string
    with open(file_path, "r") as sequence_file:
        return sequence_file.read()


def find_str_counts(sequence, strs):
    strs = list(strs)  # Copy strs (fieldnames) from database
    strs.remove("name")  # Remove "name" from STR list
    str_counts = {}
    for str in strs:
        str_counts[str] = longest_match(sequence, str)
    return str_counts


def find_matching_profile(database, str_counts):
    for row in database:
        match = True
        for str in database[0].keys():
            if str == "name":
                continue
            if int(row[str]) != str_counts[str]:
                match = False
                break
        if match:
            print(row["name"])
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
