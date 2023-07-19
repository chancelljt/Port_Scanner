import random
import time
import threading
from messages import Win_message, Lose_message, Play_again_message, yes_again_message, not_again_message, Win_Guess, Lose_Guess

def guessing_game():
    min_num = 1
    max_num = 100
    
    computer_number = random.randint(min_num, max_num)
    print("Guess a number between 1 and 100: ")
    user_guess = input("Your Guess: ")

    try:
        user_guess = int(user_guess)
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        play_game()

    print("Computer's number: ", computer_number)

    if user_guess == computer_number:
        print(Win_Guess)
    else:
        print(Lose_Guess)

    play_again = input(Play_again_message).lower()
    if play_again == "yes":
        print(yes_again_message)
        time.sleep(2)  # Wait for 2 seconds
        guessing_game()  # Start a new game
    else:
        print(not_again_message)

def timeout():
    print("Time Out! Please Try Again.")
    play_game()

def play_game():
    timer_thread = threading.Timer(7, timeout)  # Set a timeout of 7 seconds
    timer_thread.start()

    player_answer = input()
    timer_thread.cancel()  # Cancel the timer since the player has answered

    if not timer_thread.is_alive():
        timeout()
    else:
        guessing_game()
        
# Start the game
play_game()