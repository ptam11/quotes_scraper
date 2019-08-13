from csv import DictReader
from random import choice

file_name = "quotes.csv"

with open(file_name, "r") as file:
    csv_reader = DictReader(file)
    quotes = list(csv_reader)
print(quotes[0]["text"])


class GuessingGame:
    def __init__(self, text, author, link, birth, location):
        self.text = text
        self.author = author.lower()
        self.link = link
        self.birth = birth
        self.location = location
        self.playing = True
        self.guesses_remaining = 4

    def check_guess(self, guess):
        """
            Check if guess is correct.
            Keep track of remaining guesses and game state
        """
        if guess == self.author:
            self.playing = False
            return True
        else:
            self.guesses_remaining -= 1
            # gameover if guesses is 0
            if self.guesses_remaining == 0:
                self.playing = False
            # generate clue based on num guesses left
            else:
                self.generate_clue()
            return False

    def generate_clue(self):
        """
            Provide different clues based on different names
        """
        author_split = self.author.split(" ")
        if self.guesses_remaining == 3:
            print(f"Clue! Author was born in {self.location} on {self.birth}.")
        elif self.guesses_remaining == 2:
            print(f"Clue! First name has {len(author_split[0])} letters.")
        elif self.guesses_remaining == 1:
            print(f"Clue! Last name is {author_split[1]}.")


game = GuessingGame(**choice(quotes))

while game.playing:
    print(f"{game.text} \n")
    guess = input("Who is the author? \n").lower()
    if game.check_guess(guess):
        print("You Win!")
    else:
        print(f"Incorrect, you have {game.guesses_remaining} guesses remaining.")
    if not game.playing:
        retry = input("Play again? y/n").lower()
        while retry not in ["y", "n", "yes", "no"]:
            retry = input("Play again? y/n").lower()
        if retry in ["y", "yes"]:
            game = GuessingGame(**choice(quotes))
        else:
            print("Thank you for playing! Goodbye!")
