# Problem Set 2, hangman.py
# Name: Prince Debrah
# Collaborators: Xavier Sanchez
# Time spent: 3:00

import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(" ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------
# END OF HELPER CODE
# -----------------------------------


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"            
    for i in secret_word:    #tests each letter in the secret word, returns False if even one of them isn't in the letters_guessed
        if i not in letters_guessed:
            return False
    
    return True
        


def get_word_progress(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and asterisks (*) that represents
        which letters in secret_word have not been guessed so far
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    your_progress = ''   #creates a new string that records the ones we've gotten right and blocks the ones we don't know yet
    for i in secret_word:
        if i in letters_guessed:
            your_progress += i
        else:
            your_progress += '*'
            
    return your_progress


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    alphabet = list(string.ascii_lowercase)  #lowercase letters list, used as a dummy copy
    
    for letter in letters_guessed:
        if letter in alphabet:
            alphabet.remove(letter)
            
    letters_left = ''
    for letter in alphabet:
        letters_left += letter
        
    return letters_left

def number_of_unique_letters(secret_word):
    """
    Parameters
    ----------
    secret_word : string, the secret word to guess

    Returns
    -------
    int, number of unique letters in the secret word

    """
    unique_count_list = []
    for i in secret_word:
        if i not in unique_count_list:
            unique_count_list.append(i)
            
    return len(unique_count_list)

def choose_from(secret_word, get_available_letters):
    '''
    

    Parameters
    ----------
    secret_word : string, the secret word to be guessed
        
    get_available_letters : function, returns string of available letters

    Returns
    -------
    possible_letters : string, returns list of possible letters to be revealed

    '''
    possible_letters = ""
    for letter in secret_word:
        if letter in get_available_letters:
            possible_letters += letter
    
    return possible_letters
        
        
def hangman(secret_word, with_help):
    """
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)

    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    #welcome message
    print('Welcome to hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print('You are supposed to guess the letters in this word. You have 1 letter per guess.')
    print('You begin with 10 guesses.')
    
    #variables we want to have
    guesses = 10   
    letters_guessed = []
    lower_alphabet = string.ascii_lowercase
    
    #interface during iteratrions of the game
    while guesses > 0:
        print('---------')
        print(f'You have {guesses} guesses left.')
        print("Available letters:", get_available_letters(letters_guessed))
        trial = input('Please guess a letter:')
        trial = trial.lower()     #changes all letters in guess to lowercase
            
        
        #tests to see if input is eligible
        if len(trial) > 1:   #ineligible if more than 1 character
            print('Oops! That is not a letter:', get_word_progress(secret_word, letters_guessed))
            continue
        elif with_help  == False and trial not in lower_alphabet:   #allows only letters in the alphabet if with_help isn't allowed
            print('Oops! That is not a valid letter:', get_word_progress(secret_word, letters_guessed))
            continue
        elif with_help == True and trial not in lower_alphabet and trial != '!':   #allows letters in the alphabet and ! since with_help is allowed
            print('Oops! That is not a valid letter:', get_word_progress(secret_word, letters_guessed))
            continue
        elif trial in letters_guessed and trial != '!':     #doesn't allow user to repeat guesses, but allows useer to get help more than once
            print('That letter has already been guessed:', get_word_progress(secret_word, letters_guessed))
            continue
        
        
        #adds letter to list of guessed letters
        letters_guessed.append(trial)
            
        #tests to check if it's in the word
        if trial in secret_word:  #tells you if you got the guess right
            print('Good guess:', get_word_progress(secret_word, letters_guessed))
            
        elif trial not in secret_word and trial != '!':   #tells you if you got the guess wrong
            print("Sorry, your guess isn't in the word:", get_word_progress(secret_word, letters_guessed))
            
            
         #point subtraction system     
        if trial in 'aeiou' and trial not in secret_word:    
            guesses -= 2
         
        if trial in lower_alphabet and trial not in 'aeiou' and trial not in secret_word:
            guesses -= 1
          
        if trial == '!' and guesses >= 3:
            reveal_string = choose_from(secret_word, get_available_letters(letters_guessed))
            new = random.randint(0, len(reveal_string)-1)
    
            revealed_letter = reveal_string[new]
            print('Letter revealed:', revealed_letter)
            
            letters_guessed.append(revealed_letter)
            print(get_word_progress(secret_word, letters_guessed))
            
            guesses -= 3
            
            
        elif trial == '!' and guesses < 3:
            print('Sorry, you do not have enough guesses for this:', get_word_progress(secret_word, letters_guessed))
            continue
        
         
        if has_player_won(secret_word, letters_guessed):
            print('--------')
            print('Congratulations, you won!')
            print('Your total score for this game is:', (guesses + 4*number_of_unique_letters(secret_word) + 3*len(secret_word)))
            break
            
            
    #if you run out of guesses, the game ends. 
    if guesses <= 0:
        print('--------')
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.')            
        
        
        
            
                
            
        
        



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test

if __name__ == "__main__":
    # To test your game, uncomment the following three lines.

    secret_word = choose_word(wordlist)
    with_help = False
    hangman(secret_word, with_help)

    # After you complete with_help functionality, change with_help to True
    # and try entering "!" as a guess!

    ###############

    # SUBMISSION INSTRUCTIONS
    # -----------------------
    # It doesn't matter if the lines above are commented in or not
    # when you submit your pset. However, please run ps2_student_tester.py
    # one more time before submitting to make sure all the tests pass.
    
    

