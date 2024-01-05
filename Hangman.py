import csv
import random
import time
import os

alphabet = [*"abcdefghijklmnopqrstuvwxyz"]

# Opens the external word list file and saves the words to a list
def load_wordlist(filename):
    global word_list
    with open(filename) as f:
        word_list = [word.strip() for word in f]

# Opens the external hangman animation file and saves all stages of the animation to a list
with open("hangmananimation.csv") as f:
    reader = csv.reader(f)
    hangman_animation_list = list(reader)
    hangman_animation_list = hangman_animation_list[0]

# Function to clear the terminal screen between rounds (found on Stack Overflow)
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to select a random word from the list
def select_word():
    selected_word = word_list[random.randint(0, len(word_list) - 1)]
    return selected_word

# Function to print the specific hangman image based on the number of incorrect guesses
def hangman_animation(incorrect_guesses):
    print(hangman_animation_list[incorrect_guesses])

# Function that converts a selected word into underscores, but leaves in place guessed letters and non-obscured letters
def replace_word_with_underscores(selected_word, guessed_letters):
    # Splits the word into a list of its characters
    selected_word_split = list(selected_word)
    non_obscured_letters = ["(", ")", "-", ",", "'"]
    for i, letter in enumerate(selected_word_split):
        # If letter has been guessed, leave it in place
        if letter.lower() in guessed_letters:
            pass
        # If character is a space, replace it with a forward slash
        elif letter == " ":
            selected_word_split[i] = "/"
        # If letter is in the non-obscured letters list, leave it in place (for example brackets)
        elif letter in non_obscured_letters:
            pass
        # If none of the above conditions are true, replace the letter with an underscore
        else:
            selected_word_split[i] = "_"
    # Returns the updated list of characters joined as a string, as well as the list of updated characters
    return " ".join(selected_word_split), selected_word_split

# Function to check if the word guess matches the selected word
def check_word(word_guess, selected_word):
    if word_guess == selected_word.lower():
        return True
    else:
        return False
    
# Function to check if the guessed letter is in the word
def check_guess(guess, selected_word):
    # Splits the selected word into a list of characters and checks if the guessed letter is in the list
    if guess in [*selected_word.lower()]:
        # gamemode_string has a value of 'station' in the default mode, or has a value of 'word' in the custom word list mode
        print(f"\n{guess.upper()} is in the {gamemode_string}!")
        return True
    else:
        print(f"\n{guess.upper()} is not in the {gamemode_string}")
        return False

# Function to check if the guessed character is a letter in the alphabet, otherwise it returns False
# Also checks if the letter has already been guessed, if so it returns False
def validate_guess(guess, guessed_letters):
    if guess not in alphabet:
        print("\nInvalid input")
        return False
    elif guess in guessed_letters:
        print(f"\n{guess.upper()} has already been guessed")
        return False
    else:
        return True

# Function to check if the displayed word has any underscores still in it
# If not, the word has been completely revealed and the player has won
def check_if_word_is_revealed(underscore_list):
    if "_" in underscore_list:
        return False
    else:
        return True

def game():
    selected_word = select_word()
    endloop = False
    win = False
    guessed_letters = []
    incorrect_letters = []
    guessed_words = []
    incorrect_guesses = 0
    # Runs the loop until the game is ended by setting endloop to True
    while endloop == False:
        clear_terminal()
        # If there are no incorrect letters guessed yet, print a blank line
        # Otherwise print the guessed letters that are not correct
        if len(incorrect_letters) != 0:
            print("Incorrect:", ", ".join(incorrect_letters).upper())
        else:
            print("")
        hangman_animation(incorrect_guesses)
        underscore_word, underscore_list = replace_word_with_underscores(selected_word, guessed_letters)
        print(underscore_word)
        # Runs the following code only if the number of incorrect guesses is less than 10
        if incorrect_guesses < 10:
            guess = input(f"Please enter a letter, or type 9 to guess the {gamemode_string}: ").lower()
            if guess == "9":
                # If 9 is entered, the game allows you to guess the full word (station name)
                word_guess = input("Please enter your guess in full: ").lower()
                # If the word guess is empty, you will be taken back to the letter guessing mode
                if word_guess == "":
                    print("Nothing entered")
                # If the word has already been guessed, return to the letter guessing mode,
                # without incrementing the incorrect_guesses counter
                elif word_guess in guessed_words:
                    print(f"That {gamemode_string} has already been guessed")
                # If the check_word function returns true, i.e. the guessed word matches the word (station name),
                # stop repeating the game loop and set the win variable to true, indicating that the player has won
                elif check_word(word_guess, selected_word):
                    print("Correct!")
                    guessed_words.append(word_guess)
                    win = True
                    endloop = True
                # If none of the above conditions are true, the guessed word is not correct
                # Therefore add the word to the list of guessed words and increment the incorrect_guesses counter
                else:
                    print("Incorrect")
                    guessed_words.append(word_guess)
                    incorrect_guesses += 1
            # If 9 is not entered, check if the guessed character is in the alphabet
            elif validate_guess(guess, guessed_letters):
                # If the letter is not in the word, increment the incorrect_guesses counter and add the letter
                # to the incorrect_letters list, which will be displayed to the player
                if not check_guess(guess, selected_word):
                    incorrect_guesses += 1
                    incorrect_letters.append(guess)
                guessed_letters.append(guess)
            time.sleep(0.5)
            # Runs the code to update the concealed word string and list, in case the remaining letter has just been guessed
            underscore_word, underscore_list = replace_word_with_underscores(selected_word, guessed_letters)
            if check_if_word_is_revealed(underscore_list):
                win = True
                clear_terminal()
                # Prints the elements of the game again to make the display consistent
                if len(incorrect_letters) != 0:
                    print("Incorrect:", ", ".join(incorrect_letters).upper())
                else:
                    print("")
                hangman_animation(incorrect_guesses)
                print(underscore_word)
                endloop = True
        # If the number of incorrect guesses is 10, the game ends and the player loses
        else:
            win = False
            endloop = True
    
    # If the game loop has ended and the win variable is True
    if win:
        # Calculates the total number of guesses by adding the lengths of the guessed_letters and guessed_words lists
        # Subtracts 1 from this to allow the first guess to be without penalty
        total_guesses = len(guessed_letters) + len(guessed_words) - 1
        score = 26 - total_guesses
        print(f"\nYou win! The answer is {selected_word}")
        time.sleep(0.75)
        print(f"You lost {total_guesses} points based on the number of guesses")
        print(f"Score for this game: {score}")
    else:
        print(f"\nYou lose. The correct answer is {selected_word}")

clear_terminal()
loaded = False
# Repeats the following code while a word list has not been loaded
while loaded == False:
    custom_wordlist = input("Enter the file name of a custom word list, or leave blank for the default: ")
    # If no custom word list has not been specified it will load the default word list
    if custom_wordlist == "":
        load_wordlist("wordlist.txt")
        time.sleep(0.5)
        # gamemode_string relates to the types of words in the word list
        # It will be used in messages throughout the game
        gamemode_string = "station"
        loaded = True
        print("\nWelcome to Guess the Station Hangman!\nYou must guess the name of one of the UK's 2580 train stations.")
    # If a custom word list has been specified, attempt to load it
    else:
        try:
            load_wordlist(custom_wordlist)
            print("Custom word list loaded successfully")
            gamemode_string = "word"
            loaded = True
            time.sleep(0.5)
            print("\nWelcome to Hangman")
        # If an error occurs while trying to load the custom word list, repeat the loop and ask the user to try again
        except Exception:
            print("Unable to load custom word list\n")
            time.sleep(1)

time.sleep(3)
# Repeat the following code until the player does not want to continue playing
while True:
    game()
    if input("\nPlay again? (y/n): ").lower() == "n":
        break