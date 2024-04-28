from abc import ABC, abstractmethod

class PlayGame(ABC):
    def __init__(self, filename):
        self._filename = filename
        self._level_score = 0
        self._questions = self._read_from_file(filename)

    @abstractmethod
    def _read_from_file(self, filename):
        pass

    def _play_multiple_choice(self):

        for question, options, answer in self._questions:
            print(f"Question: {question}")
            for idx, option in enumerate(options, 1):
                print(f"{idx}. {option}")
            while True:     
                guess = input("Your answer (enter the number): ")
                try:
                    guess= int(guess)
                    break
                except ValueError:
                    print("Please enter a nunmber between 1-3")
            if int(guess) - 1 == int(answer) - 1:
                print("Correct!\n")
                self._level_score += 1
            else:
                print(f"Incorrect. The correct answer is: {options[int(answer)-1]}\n")

        print(f"You scored {self._level_score} points!")
        return self._level_score

    def _play_text_input(self):
        for question, answer in self._questions:
            print(f"Question: {question}")
            guess = input("Your answer: ")

            if guess.lower() == answer.lower():
                print("Correct!\n")
                self._level_score += 1
            else:
                print(f"Incorrect. The correct answer is: {answer}\n")

        print(f"You scored {self._level_score} points!")
        return self._level_score

class MultipleChoice(PlayGame):
    def _read_from_file(self, filename):
        questions = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) % 5 != 0:
                raise ValueError("Invalid file format: Each question should have 5 lines.")
            for i in range(0, len(lines), 5):
                question = lines[i].strip()
                options = [lines[i+j].strip() for j in range(1, 4)]
                answer = lines[i+4].strip()
                questions.append((question, options, answer))
        return questions

    def play_level(self):
        print("Multiple Choice\n")
        return self._play_multiple_choice()

class TextInput(PlayGame):
    def _read_from_file(self, filename):
        questions = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                question = lines[i].strip()  
                answer = lines[i+1].strip() 
                questions.append((question, answer))
        return questions

    def play_level(self):
        print("Text Input\n")
        return self._play_text_input()

class CountryGuessGame:
    def __init__(self):
        self._levels = []
        self._total_score = 0

    def add_level(self, filename, level_type):
        if level_type == "multiple_choice":
            level = MultipleChoice(filename)
        elif level_type == "text_input":
            level = TextInput(filename)
        else:
            raise ValueError("Invalid level type")
        self._levels.append(level)

    def play_game(self):
        player_name = input("\nEnter your name: ")
        print(f"\n{player_name}, welcome to the Country Guesser!")
        print("You will have to guess the country from given clues.")
        print("For each correct answer, you will receive points.\n")

        for i, level in enumerate(self._levels, 1):
            print(f"Level {i}")
            level_score = level.play_level()
            self._total_score += level_score
        print(f"Congratulations, your total score is {self._total_score} points!\n")

        with open("scores.txt", "a") as f:
            f.write(f"{player_name} scored {self._total_score} points!\n")

def main():
    game = CountryGuessGame()

    game.add_level("level_1.txt", "multiple_choice")
    game.add_level("level_2.txt", "text_input")
    #game.add_level("level_3.txt", "text_input")

    game.play_game()

if __name__ == "__main__":
    main()