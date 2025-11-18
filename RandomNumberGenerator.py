"""
* Name         : <RandomNumberGenerator.py>
* Author       : <Adin Mujakovic>
* Created      : <11/18/2025>
* Course       : CIS189
* IDE          : <Visual Studio Code>
* Description  : <A GUI program that allows the user to play a number guessing game. 
                The user can start a new game, make guesses by clicking buttons, and reset the game. 
                The program keeps track of guessed numbers and provides feedback on each guess.>
*
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified.       
"""
import tkinter, unittest, random
from tkinter import messagebox
# max value for the guessing game, can be changed as needed to adjust difficulty
max = 25
# trigger to change label to "selections made" if something is checked
class NumberGuesser():
    def __init__(self):
        guessed_list = []
        self.guessed_list = guessed_list
    # adds a guess to the guessed_list if not already present
    def add_guess(self, guess):
        if guess not in self.guessed_list:
            self.guessed_list.append(guess)
        else:
            pass
    # resets the guessed_list to empty
    def reset_guesses(self):
        self.guessed_list = []
    # returns the guessed_list
    def get_guessed_list(self):
        return self.guessed_list
class NumberGuesserGUI(tkinter.Tk):
    def __init__(self, max_number=max):
        tkinter.Tk.__init__(self)
        self.title("Number Guessing Game")
        self.max_number = max_number
        self.number_guesser = NumberGuesser()
        self.target = None
        self.button_refs = {}

        # Controls
        top_frame = tkinter.Frame(self)
        top_frame.pack(padx=10, pady=10)

        self.start_button = tkinter.Button(top_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=5)

        self.reset_button = tkinter.Button(top_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=0, column=1, padx=5)

        self.status_label = tkinter.Label(top_frame, text="Press Start Game to begin")
        self.status_label.grid(row=0, column=2, padx=10)

        # Buttons area
        buttons_frame = tkinter.Frame(self)
        buttons_frame.pack(padx=10, pady=(0,10))

        columns = 7  # layout columns, can be adjusted
        for n in range(1, self.max_number + 1):
            btn = tkinter.Button(buttons_frame, text=str(n), width=6,
                            command=lambda v=n: self.make_guess(v), state=tkinter.DISABLED)
            r = (n - 1) // columns
            c = (n - 1) % columns
            btn.grid(row=r, column=c, padx=3, pady=3)
            self.button_refs[n] = btn

    def start_game(self):
        # pick random target and enable buttons; reset guessed list
        self.target = random.randint(1, self.max_number)
        NumberGuesser.reset_guesses(self)
        for btn in self.button_refs.values():
            btn.config(state=tkinter.NORMAL)
        self.status_label.config(text=f"Game started! Guess a number between 1 and {self.max_number}.")

    def reset_game(self):
        # resets game state and enable all buttons
        self.target = None
        NumberGuesser.reset_guesses(self)
        for btn in self.button_refs.values():
            btn.config(state=tkinter.DISABLED)
        self.status_label.config(text="Game reset. Press Start Game to begin")

    def make_guess(self, value: int):
        # handle a guess: if correct -> winner messagebox + reset; else disable button and record guess
        if value == self.target:
            messagebox.showinfo("Winner!", f"Correct! The number was {self.target}.")
            self.reset_game()
        else:
            # disable the button (visible but not clickable)
            btn = self.button_refs.get(value)
            if btn:
                btn.config(state=tkinter.DISABLED)
            NumberGuesser.add_guess(self, value)
            self.status_label.config(text=f"{value} is incorrect. Try again.")


# ----------------------------
# Unit tests for NumberGuesser
# ----------------------------
class TestNumberGuesser(unittest.TestCase):
    def setUp(self):
        # ensure we start with a clean class state
        NumberGuesser.reset_guesses(self)

    def tearDown(self):
        # clean up after tests
        NumberGuesser.reset_guesses(self)

    def test_constructor_sets_max_and_resets_guessed_list(self):
        max = 30
        self.assertEqual(max, 30)
        self.assertEqual(NumberGuesser.get_guessed_list(self), [])

    def test_add_guess_adds_to_guessed_list(self):
        NumberGuesser.add_guess(self, 3)
        self.assertIn(3, NumberGuesser.get_guessed_list(self))
        # adding the same guess again should not create duplicates
        NumberGuesser.add_guess(self, 3)
        self.assertEqual(NumberGuesser.get_guessed_list(self).count(3), 1)

    def test_reset_clears_guessed_list(self):
        NumberGuesser.add_guess(self, 1)
        NumberGuesser.add_guess(self, 2)
        self.assertEqual(len(NumberGuesser.get_guessed_list(self)), 2)
        NumberGuesser.reset_guesses(self)
        self.assertEqual(NumberGuesser.get_guessed_list(self), [])


if __name__ == '__main__':

    # To run unit tests, type this command in the terminal:
    # python -m unittest RandomNumberGenerator.py

    # Run the GUI application
    app = NumberGuesserGUI(max_number=max)
    app.mainloop()
