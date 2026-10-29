""" Hangman game"""

import os
import random
import sys
import time

WORDS = ["python", "planet", "guitar", "castle", "rocket"]
MAX_MISTAKES = 6

# One drawing for each number of incorrect guesses (0 through 6).
HANGMAN = [
    ["  +---+", "  |   |", "      |", "      |", "      |", "========= "],
    ["  +---+", "  |   |", "  O   |", "      |", "      |", "========= "],
    ["  +---+", "  |   |", "  O   |", "  |   |", "      |", "========= "],
    ["  +---+", "  |   |", "  O   |", " /|   |", "      |", "========= "],
    ["  +---+", "  |   |", "  O   |", " /|\\  |", "      |", "========= "],
    ["  +---+", "  |   |", "  O   |", " /|\\  |", " /    |", "========= "],
    ["  +---+", "  |   |", "  O   |", " /|\\  |", " / \\  |", "========= "],
]

# ANSI colors work in the VS Code integrated terminal.
RESET = "\033[0m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
DIM = "\033[2m"


def clear_screen():
    """Clear the terminal between animation frames."""
    os.system("cls" if os.name == "nt" else "clear")


def type_text(message, delay=0.025):
    """Print a short typewriter-style animation."""
    for character in message:
        print(character, end="", flush=True)
        time.sleep(delay)
    print()


def draw_hangman(mistakes, animate=False):
    """Show the current drawing, optionally revealing new lines in sequence."""
    drawing = HANGMAN[mistakes]
    if animate:
        for line in drawing:
            print(CYAN + line + RESET)
            time.sleep(0.07)
    else:
        for line in drawing:
            print(CYAN + line + RESET)


def show_header():
    print(YELLOW + "╔══════════════════════════════════════╗" + RESET)
    print(YELLOW + "║       CODEALPHA • HANGMAN GAME       ║" + RESET)
    print(YELLOW + "╚══════════════════════════════════════╝" + RESET)


def play_round():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    mistakes = 0

    clear_screen()
    show_header()
    type_text("A word is hidden. Guess it one letter at a time!", 0.018)
    print(DIM + "Tip: type one letter, then press Enter." + RESET)
    time.sleep(0.45)

    while mistakes < MAX_MISTAKES:
        clear_screen()
        show_header()
        draw_hangman(mistakes)
        print()

        masked_word = " ".join(
            letter if letter in guessed_letters else "_" for letter in secret_word
        )
        print("Word:       " + GREEN + masked_word + RESET)
        print("Guessed:    " + (", ".join(sorted(guessed_letters)) or "—"))
        print(f"Mistakes:   {mistakes}/{MAX_MISTAKES}")

        if all(letter in guessed_letters for letter in secret_word):
            print("\n" + GREEN + "🎉 You saved the day! You guessed the word." + RESET)
            return

        guess = input("\nYour letter (or ? for a hint): ").strip().lower()
        if guess == "?":
            # A hint reveals one unguessed letter without counting as a mistake.
            hidden = [letter for letter in secret_word if letter not in guessed_letters]
            if hidden:
                revealed = random.choice(hidden)
                guessed_letters.add(revealed)
                print(YELLOW + f"Hint: revealed '{revealed}'." + RESET)
                time.sleep(0.8)
            continue
        if len(guess) != 1 or not guess.isalpha():
            print(YELLOW + "Please enter a single letter." + RESET)
            time.sleep(0.8)
            continue
        if guess in guessed_letters:
            print(YELLOW + "You already tried that letter." + RESET)
            time.sleep(0.8)
            continue

        guessed_letters.add(guess)
        if guess in secret_word:
            print(GREEN + "Nice guess!" + RESET)
        else:
            mistakes += 1
            print(RED + "Not in the word — the drawing changes..." + RESET)
            time.sleep(0.35)
            clear_screen()
            show_header()
            draw_hangman(mistakes, animate=True)
        time.sleep(0.55)

    clear_screen()
    show_header()
    draw_hangman(MAX_MISTAKES)
    print(RED + f"\nGame over! The word was: {secret_word}" + RESET)


def main():
    while True:
        clear_screen()
        show_header()
        print("\n  1. Play Hangman")
        print("  2. How to play")
        print("  3. Quit")
        choice = input("\nChoose 1, 2, or 3: ").strip()

        if choice == "1":
            play_round()
            input("\nPress Enter to return to the menu...")
        elif choice == "2":
            clear_screen()
            show_header()
            print("\nGuess the hidden word one letter at a time.")
            print(f"You can make up to {MAX_MISTAKES} incorrect guesses.")
            print("Enter ? during a round to reveal one hidden letter.")
            input("\nPress Enter to return to the menu...")
        elif choice == "3":
            clear_screen()
            type_text("Thanks for playing. Keep coding! 👋", 0.04)
            break
        else:
            print(YELLOW + "Please choose 1, 2, or 3." + RESET)
            time.sleep(0.9)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame closed. See you next time!")
        sys.exit(0)
