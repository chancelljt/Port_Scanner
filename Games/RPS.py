import random
import time
import threading
from messages import Win_message, Lose_message, Play_again_message, yes_again_message, not_again_message

def print_message(has_won):
    if has_won:
        print(Win_message)
    else:
        print(Lose_message)

def play_game():
    print("Rock, Paper, or Scissors: Enter your option ")

    player_answer = None
    timeout_expired = False

    def timeout():
        nonlocal timeout_expired
        nonlocal player_answer
        if player_answer is None:
            timeout_expired = True

    timer_thread = threading.Timer(7, timeout)  # Set a timeout of 7 seconds
    timer_thread.start()

    player_answer = input()
    timer_thread.cancel()  # Cancel the timer since the player has answered

    if timeout_expired:
        print("Time Out! Please Try Again.")
        play_game()  # Ask the player to try again
        return  # Exit the function

    computer_answer = random.choice(["Rock", "Paper", "Scissors"])
    print("Computer's answer:", computer_answer)

    if player_answer == computer_answer:
        print("There is a Tie. Try again")
        has_won = None  # It's a tie
    elif (player_answer == "rock" and computer_answer == "Scissors") or \
         (player_answer == "paper" and computer_answer == "Rock") or \
         (player_answer == "scissors" and computer_answer == "Paper"):
        has_won = True  # Player wins
    else:
        has_won = False  # Computer wins

    print_message(has_won)

    play_again = input(Play_again_message).lower()
    if play_again == "yes":
        print(yes_again_message)
        time.sleep(2)  # Wait for 2 seconds
        play_game()  # Start a new game
    else:
        print(not_again_message)

play_game()  # Start the game