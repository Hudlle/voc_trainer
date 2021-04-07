import random
import json
import sys
import os
import matplotlib

def voc_learn():
    voc_decks_path = init()
    print(voc_decks_path)
def create_deck():
    pass
def edit_deck():
    pass

voc_training_commands = {
    "1" : voc_learn,
    "2" : create_deck,
    "3" : edit_deck,
}
def voc_training():
    print("\n# Voc Training\n[1] Learn Vocab\n[2] Create New Deck\n[3] Edit A Deck\n[B] Back")
    answer = input("> ")
    if answer == "B" or answer == "b":
        menu()
        return
    keys = list(voc_training_commands.keys())
    for i in keys:
        if i  == answer:
            voc_training_commands[answer]()
            voc_training()
            return
    print(f"E: {answer} Is Not A Valid Input. Try Again.")
    voc_training()
    

def tens_training():
    pass

def quitApp():
    print("Bye.")
    sys.exit()

def init():
    cwd = os.getcwd()
    
    voc_decks_path = cwd + "/voc_decks"
    voc_decks_path_bool = False
    if os.path.exists(voc_decks_path) == False:
        os.makedirs(voc_decks_path)
        voc_decks_path_bool = True
    else:
        print()

    return voc_decks_path

commands = {
    "1" : voc_training,
    "2" : tens_training,
}
def menu():
    init()

    print("\n--> Main Menu\n[1] Voc. Training\n[2] Tens Training\n[Q] Quit\n")
    answer = input("> ")

    if answer == "q" or answer == "Q":
        quitApp()
    keys = list(commands.keys())
    for i in keys:
        if i == answer:
            commands[answer]()
            menu()
            return
    print(f"E: {answer} Is Not A Valid Input. Try Again.")
    menu()
        
menu()
