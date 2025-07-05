# Fizzbuzz Project
for i in range(1, 101):
    if i % 15 == 0:
        print("fizzbuzz")
    elif i % 3 == 0:
        print("fizz")
    elif i % 5 == 0:
        print("buzz")
    else:
        print(i)


# Scrabble Project
import itertools

# Load a Scrabble word list
def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)

dictionary_path = "/Users/yvonnehan/Downloads/scrabble_words.txt"
scrabble_dict = load_dictionary(dictionary_path)


# Generate all permutations of the letters "tabind"
def generate_words(letters):
    results = set()
    for i in range(2, len(letters) + 1):  # create 2-letter to 6-letter words
        for p in itertools.permutations(letters, i):
            results.add(''.join(p))
    return results

# Filter only valid words in the Scrabble dictionary
def find_valid_words(letters, dictionary):
    possible_words = generate_words(letters)
    return sorted([word for word in possible_words if word in dictionary])

# Main function
def main():
    dictionary_path = "/Users/yvonnehan/Downloads/scrabble_words.txt"

    letters = "tabind"
    scrabble_dict = load_dictionary(dictionary_path)
    valid_words = find_valid_words(letters, scrabble_dict)

    print("Valid words from 'tabind':")
    print(f"Total number of valid words: {len(valid_words)}")
    for word in valid_words:
        print(word)

if __name__ == "__main__":
    main()

