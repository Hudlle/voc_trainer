import random
import json
import sys
import os

class VocTraining:
    def __init__(self):
        self.exist_voc_path = False
        self.training_cmds = {"1" : self.learn_vocab, "2" : self.create_deck, "3" : self.edit_deck}

    def check_paths(self):
        cwd = os.getcwd()
        voc_decks_path = cwd + "\\voc_decks"

        print("[SYSTEM] Checking base path ...")
        if os.path.exists(voc_decks_path) == False:
            print(f"[ERROR] Failed to initalize vocab decks path.\n'{voc_decks_path}' does not exist. Would you like to create it? [y/n]")
            answer = input("[SYSTEM] > ")
            if answer == "y":
                os.mkdir(voc_decks_path)
                print(f"[SUCCESS] Successfully created vocab decks path at: '{voc_decks_path}'")
                self.exist_voc_path = True
                self.start_training()
            else:
                print(f"[ERROR] Creation of directory at '{voc_decks_path}' aborted. Returning to main menu.")
                self.exist_voc_path = False
                menu()
                return
        
        self.exist_voc_path = True
        print("[SYSTEM] Completed.")
        self.start_training()

    def start_training(self):
        if self.exist_voc_path == True:
            print("\n# Vocab Training\n[1] Learn vocab\n[2] Create new deck\n[3] Edit a deck\n[B] Back")
            answer = input("> ")
            if answer == "b" or answer == "B":
                menu()
                return
            keys = list(self.training_cmds.keys())
            for i in keys:
                if i == answer:
                    self.training_cmds[answer]()
                    self.start_training()
                    return
            print(f"[ERROR] '{answer}' is not a valid input. Try again.")
            self.start_training()
        else:
            self.check_paths()
            return

    def learn_vocab(self):
        pass

    def create_deck(self):
        deck_name = "deck 1"
        voc_originals = ["hello", "heißen"]
        voc_translations = ["hola", "llamarse"]
        voc_dict = dict(zip(voc_originals, voc_translations))

        deck1 = {deck_name : { "vocab" : voc_dict}}
        deck2 = {"deck 2" : {"vocab" : voc_dict}}

        decks = [deck1, deck2]

        data = {"decks" : decks}

        with open("voc_decks.json", "w") as f:
            json.dump(data, f, indent=4)

        with open("voc_decks.json", "r") as f:
            data = json.load(f)
            decks = data["decks"]
            print(decks[0]["deck 2"])
            
            decks_names = []
            for i in decks:
                decks_names.append(i.keys())

            for i in decks_names:
                print(decks[i])

    def edit_deck(self):
        pass

def menu():
    print("\n--> Main Menu\n[1] Vocab training\n[2] Tens training\n[Q] Quit\n")
    answer = input("> ")

    if answer == "q" or answer == "Q":
        print("Bye.")
        sys.exit()
    elif answer == "1":
        voc_training = VocTraining().start_training()
        return

    print(f"E: {answer} Is Not A Valid Input. Try Again.")
    menu()
        
menu()
