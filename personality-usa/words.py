from collections import Counter
import csv
import re
import os

import city


def parse_text_to_list(text):
    text = text.lower()

    text = re.sub(r"http\S+", "", text)  # Removes links
    text = re.sub(r"@\S+", "", text)  # Removes @user

    pattern = re.compile('([^\s\w]|_)+', re.UNICODE)  # Removes everything but spaces and alphanumeric chars
    text = pattern.sub('', text)

    words = text.split()

    return words


def dictionary_to_csv(dictionary, path):
    csv_path = path

    file_exists = os.path.isfile(csv_path)  # Checks if CSV file already exists

    if file_exists:  # If the file already exists, just update the CSV
        current_dictionary = Counter(convert_csv_to_dictionary(csv_path))
        new_dictionary = Counter(dictionary)

        combined_dictionary = current_dictionary + new_dictionary
        convert_dictionary_to_csv(combined_dictionary, path)
    else:  # If the file doesn't exist yet, create a new CSV
        convert_dictionary_to_csv(dictionary, csv_path)


def convert_dictionary_to_csv(dictionary, csv_path):
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "frequency"])  # Create header

        for word, frequency in dictionary.items():
            writer.writerow([word, frequency])


def convert_csv_to_dictionary(csv_path):
    my_dict = {}

    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skips header

        for word, str_frequency in reader:
            my_dict[word] = int(str_frequency)  # Casts string frequencies to integer values

    return my_dict
