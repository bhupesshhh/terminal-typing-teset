# Imports
import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    # Start Screen Section
    stdscr.clear()  # Clear the terminal
    # Welcome Note
    stdscr.addstr("Welcome to Speed Typing Test!", curses.color_pair(1))
    stdscr.addstr("\nPress any key to begin!", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    # For the displayed and input text
    stdscr.addstr(target, curses.color_pair(3))
    stdscr.addstr(2, 0, f"WPM: {wpm}", curses.color_pair(3))

    for i, char in enumerate(current):
        # Check for correct character and change color
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        # Display the output
        stdscr.addstr(0, i, char, color)


def load_text():
    # Loading different texts
    with open("sample.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    # WPM Check Function
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)  # To keep the time running

    while True:
        # Check for Time & WPM
        time_passed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_passed/60)) / 5)

        # Show The Content First
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # Check for Win
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # Ask for response (Error handling)
        try:
            key = stdscr.getkey()
        except:
            continue  # Cause we turned on No Delay

        # Check for Esacape to Quit
        if ord(key) == 27:  # 27 represents ASCII for Escape Key
            break

        # Check for Backspace to clear
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        # To add the inputs
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    # Initiate Colour Palatte
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Initiate Welcome Screen
    start_screen(stdscr)

    # Gameplay
    while True:
        wpm_test(stdscr)
        # Game End Note
        stdscr.addstr(5, 0, "You finished the game. Press any key to continue ?")
        if ord(stdscr.getkey()) == 27:
            break


# Bringuing everything to Terminal
wrapper(main)
