"""
COMP.CS.100 Programming 1
Creator: Marko K*******, marko.k*******tuni.fi, student id number: 15*******
Solution of task 13.10 Project: Graphical User Interface

My own GUI version of the popular word guessing game Wordle
(https://www.nytimes.com/games/wordle/index.html)

The game's idea is to guess a 5-letter long word, with hints being given
based on what word the player has guessed. If the answer is not in the list
of words, it will not count towards the amount of guesses and will instead
reset the text on the labels, this feature actually makes the challenge
slightly more interesting.

This is to be submitted as an Advanced GUI program. According to the
guidelines of the assignment, this program would be comparable to the
hangman example, as a virtual keyboard is being used for user input,
and a loop is being used in the constructor for building and placing down
majority of the UI components.
"""

from tkinter import *
from random import choice
from string import ascii_uppercase

KEYBOARD_LAYOUT = ["QWERTYUIOP", "ASDFGHJKL", "ENTER", "ZXCVBNM", "BACKSPACE"]

# The constant KEYBOARD_LAYOUT is used in the loop when constructing buttons
# to mimic a QWERTY keyboard.


def choose_word():
    """
    Loops through a text file containing words, separated by individual
    rows. If they contain non-ascii characters as defined by the string
    (ascii_uppercase) from string module, in this case any special characters
    or umlauts, they will not be included in the output list. The textfile
    is changeable, however the test sample is already large enough so I saw
    no need to implement choosing a custom text file through the GUI
    application. In hindsight I also never approached writing the program
    with this in mind, so it would require retracing the steps back quite a
    bit and doing some design over from scratch.

    For testing purposes, there is a smaller pool of words to play with in
    the included simple_words.txt file. An empty .txt file may also be used
    to try out the fancy ERROR message presented by the GUI.

    :return: chooses a random word from a list of 5-letter words, also returns
    the list of words to compare with player's guesses.
    """

    if True:
        wordlist = "words.txt"
    else:
        wordlist = "simple_words.txt"

    try:
        with open(wordlist) as text_file:
            words = text_file.read()
            words = words.split("\n")

            answers = []

            for word in words:
                if len(word) != 5:
                    continue

                for letter in word:
                    if letter.upper() not in ascii_uppercase:
                        continue

                answers.append(word.upper())

            if len(answers) == 0:  # Prints out fancy ERROR in main GUI
                return None, None

            return choice(answers), answers

    except FileNotFoundError:
        return None, None


class WordleGame:
    """
    I chose to implement the game as a class, keeping in line with the last
    chapters. As the game handles a few attributes, it felt like a good
    approach to take, and I need to learn more about OOP anyway as it is
    something I haven't really learned on my own in the past.
    """

    def __init__(self):
        """
        The answer and list of answers are gotten from the function, which
        randomises a word for the game. Ratings are based on guess count.
        """

        self.__answer, self.__answers = choose_word()
        self.__guesses = 0
        self.__rating = {1: "Perfect", 2: "Excellent", 3: "Very good",
                         4: "Good", 5: "Okay", 6: "Clutch"}

    def confirm_answer(self):
        """
        This is only used when the GUI is started to check if there is any
        answer on the game, if Nonetype is returned, the GUI will display an
        error and will not accept user input (outside of Quit button).
        """
        return self.__answer

    def guess(self, word: str):
        """
        A method used by the main GUI program to input guesses into the game
        object. The logic is yet incomplete, as it doesn't account for words
        with multiple same characters as input or correct answer and may
        display partially incorrect results. This could be implemented with
        count() method or something else, but I feel like it may be
        excessive for an assignment of beginner level (or I'm just too lazy
        to think of a way). It looks clean for now and it will end up being
        spaghetti if I tamper any further with it, so I will omit this change.

        :param word: Word issued by the player's input from GUI element.
        :return: A list of tuples containing the guessed words letters with
        a color assigned to them representing if the letter is in the word
        (yellow), if it's in a correct position (green) or not in the word at
        all (dark gray).

        The other return value is either amount of guesses,
        or in case of a correct word, it will give the text-form grading from
        the self.__rating dict.

        In the first case, two Nonetype are returned instead, as the answer
        was not in the list of acceptable words. As with the real Wordle,
        a word that is not listed does not use up any guesses.
        """

        if word not in self.__answers:
            return None, None

        self.__guesses += 1

        answer = []

        for i in range(0, 5):
            letter = word[i]

            if letter == self.__answer[i]:
                answer.append((letter, "#6ca965"))  # Correct color

            elif letter in self.__answer:
                answer.append((letter, "#c8b653"))  # Correct, wrong position

            else:
                answer.append((letter, "#3e3e42"))  # Wrong letter

        if word == self.__answer:
            return answer, self.__rating[self.__guesses]

        return answer, self.__guesses


class GUI:
    def __init__(self):
        """
        The program is using only button input, I didn't feel like adding
        optional keyboard input reading as it seemed to require a lot more
        effort to get it working without using entry fields to read user input.
        """

        self.__main_window = Tk()
        self.__main_window.configure(bg="#252526")
        self.__main_window.title("Scuffdle by M.K.")

        """
        Game object related attributes
        """

        self.__game = WordleGame()
        self.__guess = ""
        self.__guess_count = 0
        self.__score = ""

        """
        Constructing the main labels, 6 rows, 5 columns each. These are used
        for displaying the player's guessed words.
        """

        self.__rows = {}  # A dict representing a matrix of labels

        for rows in range(0, 6):
            for columns in range(0, 5):
                label_position = (rows, columns)
                self.__rows[label_position] = Label(self.__main_window,
                                                    text="",
                                                    borderwidth=2,
                                                    relief=GROOVE,
                                                    width=10, height=5,
                                                    bg="#787c7f",
                                                    fg="white",
                                                    font=("Tahoma", 14))

                self.__rows[label_position].grid(row=rows, column=columns,
                                                 columnspan=6)

        """
        I am using lambdas in the next section after some googling to 
        figure out how to pass a command any arguments with vars from loops 
        without calling the methods upon running the program. I don't have a 
        full grasp yet on how to write lambdas, but the one I used here is 
        simple enough to that I somewhat understand what is going on with the 
        statement, so it felt reasonable to use it. This is mainly an issue 
        with Tkinter itself, it doesn't seem to allow passing parameters to 
        commands by default. 
        
        The lambda function simply passes the incremental loop variable into 
        another temporary variable which is then being used as the parameter 
        for the method call, a rather sketchy workaround, but it does not 
        require importing another library, which was another way of getting 
        around the Tkinter issues.
        
        This was necessary to reduce the lines, as I wanted to avoid writing 
        each keyboard button individually, keeping in line with the looping
        button and label principle, while still having a unique identifier for 
        the issued command (e.g. what key is being pressed, which is
        passed on to the other methods as a parameter)
        """

        self.__keyboard = {}  # A dict representing a virtual keyboard

        for alphabet in ascii_uppercase:  # Constructing buttons for keyboard.
            alphabet_button = Button(self.__main_window, text=alphabet,
                                     command=lambda key=alphabet:
                                     self.button_press(key),
                                     width=10, height=5,
                                     bg="#787c7f", fg="white",
                                     font=("Tahoma", 14))

            self.__keyboard[alphabet] = alphabet_button

        row_keyboard = 6  # The labels end on the 6th grid row.
        column_keyboard = 0

        for keys in KEYBOARD_LAYOUT:  # Placing the buttons for keyboard.
            if keys == "BACKSPACE" or keys == "ENTER":  # Special cases
                button = Button(self.__main_window, text=keys,
                                command=lambda key=keys:
                                self.button_press(key),
                                height=5, width=10,
                                bg="#787c7f", fg="white",
                                font=("Tahoma", 14))

                button.grid(row=row_keyboard, column=column_keyboard,
                            columnspan=2)

                if keys == "ENTER":  # As ENTER is the first key on the row,
                    column_keyboard += 1  # increasing column count is needed.

                continue

            for key in keys:
                if keys == "QWERTYUIOP":  # Shorter columnspan for top row.
                    columnspan = 1  # This is purely for aesthetic reasons.
                else:
                    columnspan = 2

                self.__keyboard[key].grid(row=row_keyboard,
                                          column=column_keyboard,
                                          columnspan=columnspan)
                column_keyboard += 1

            if key != "M":  # Skips creating another row to align backspace.
                column_keyboard = 0
                row_keyboard += 1

        """
        The main GUI components are now built and displayed.
        """

        self.__quit = Button(self.__main_window, text="Quit",
                             width=10, height=4,
                             bg="#787c7f", fg="white",
                             font=("Tahoma", 14),
                             command=self.quit)

        self.__quit.grid(row=0, column=9)

        """
        Below is a visual representation of an error in the program, 
        further explained under the called method's own definition.
        """

        if self.__game.confirm_answer() is None:
            self.error_message()

        self.__main_window.mainloop()

    def quit(self):
        """
        Quit command for the application.
        """
        self.__main_window.destroy()

    def button_press(self, key: str):
        """
        The main method behind the GUI, taking user input in form of button
        presses. If the game is finished, will not do anything as decided by
        the first condition check.

        Makes sure the guess is 5 letters long before allowing ENTER to be
        pressed, and will not accept any further key inputs beyond 5 letters.

        :param key: Key input from the GUI, used to dictate what course of
        action to take.
        """

        if self.__score != "" or self.__guess_count == 6:
            return

        row = self.__guess_count
        column = len(self.__guess)

        if key in ascii_uppercase and len(self.__guess) < 5:
            self.__guess += key
            self.__rows[(row, column)].configure(text=key)

        elif key == "BACKSPACE" and len(self.__guess) >= 1:
            self.__rows[(row, column - 1)].configure(text="")
            self.__guess = self.__guess[:-1]

        elif key == "ENTER" and len(self.__guess) == 5:
            answer, score = self.__game.guess(self.__guess)
            self.__guess = ""

            if answer is None:
                self.reset_row()

            else:
                self.print_row(answer, score)
                self.__guess_count += 1

    def reset_row(self):
        """
        If the given word is not within the list of acceptable words, this
        method will be called in order to clear the row of labels.
        """

        row = self.__guess_count
        for column in range(0, 5):
            self.__rows[(row, column)].configure(text="")

    def print_row(self, answer: tuple, score):
        """
        This method changes the color of a single row depending on the given
        answer. As self.__guess_count is increased after this method runs,
        it uses the value of 5 for the game over condition rather than 6.
        This is simply because I am using the guess_count var to also keep
        track of which row of labels to adjust.

        :param answer: A list of tuples from WordleGame class, has the
        guessed word's letters individually, with assigned color as the
        other item. The color is used to change backgrounds of labels and
        buttons accordingly, giving the player hints on their progress.

        :param score: Score as given by the WordleGame class. Doesn't matter
        unless its type is string, in which case this dictates the game
        being won.
        """

        row = self.__guess_count
        column = 0

        try:
            score = int(score)

            if self.__guess_count == 5:
                self.__score = "You lost :-("

        except ValueError:
            self.__score = score

        for character in answer:
            letter = character[0]
            color = character[1]

            self.__keyboard[letter].configure(bg=color)
            self.__rows[(row, column)].configure(text=letter, bg=color)

            column += 1

        if self.__score != "":  # Displays a text box when game is finished.
            result = Label(self.__main_window, text=self.__score,
                           borderwidth=2, relief=GROOVE, width=10,
                           height=4, bg="#787c7f", fg="white",
                           font=("Tahoma", 14))

            result.grid(row=1, column=9)

    def error_message(self):
        """
        Prints out a fancy ERROR message on the top row labels with a red
        background, this is only applicable if the user tries using their
        own list of words and it doesn't have any acceptable words for playing
        the game.
        """
        self.__rows[(0, 0)].configure(text="E", bg="red")
        self.__rows[(0, 1)].configure(text="R", bg="red")
        self.__rows[(0, 2)].configure(text="R", bg="red")
        self.__rows[(0, 3)].configure(text="O", bg="red")
        self.__rows[(0, 4)].configure(text="R", bg="red")

        self.__guess_count = 6  # Disable user's virtual keyboard input.


def main():
    gui = GUI()


if __name__ == "__main__":
    main()
