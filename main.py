import random
import json
import sys
import os

class VocTraining:
    def __init__(self):
        self.exist_data_path = False
        self.data_path = os.path.join(os.getcwd(), "data")
        self.exist_vocab_path = False
        self.vocab_path = os.path.join(self.data_path, "vocab_decks.json")
        self.training_cmds = {"1" : self.learn_vocab, "2" : self.create_deck, "3" : self.edit_deck}

    def check_paths(self):
        print("[SYSTEM] Checking data ...")
        if os.path.exists(self.data_path) == False:
            print(f"[ERROR] Failed to initalize data path.\n'{self.data_path}' does not exist. Would you like to create it? [y/n]")
            answer = input("[SYSTEM] > ")
            if answer == "y":
                os.mkdir(self.data_path)
                print(f"[SUCCESS] Successfully created data path at: '{self.data_path}'")
                self.exist_data_path = True
            else:
                print(f"[ERROR] Creation of needed directory at '{self.data_path}' aborted. Returning to main menu.")
                self.exist_data_path = False
                menu()
                return
        else:
            self.exist_data_path = True

        if self.exist_data_path == True:
            if os.path.exists(self.vocab_path) == False:
                print(f"[ERROR] Failed to initalize vocab decks storage.\nFile 'voc_decks.json' at '{self.data_path}' does not exist. Would you like to create it? [y/n]")
                print(f"[WARNING] By creating a new file, all decks created or not will be overwritten. It's a new start, be aware of that.")
                answer = input("[SYSTEM] > ")
                if answer == "y":
                    with open(self.vocab_path, "w") as f:
                        data = {"decks" : []}
                        json.dump(data, f, indent=4)
                    print(f"[SUCCESS] Successfully created vocab decks storage at: '{self.vocab_path}'")
                    self.exist_vocab_path = True
                else:
                    print(f"[ERROR] Creation of needed storage capacity at '{self.data_path}' aborted. Returning to main menu.")
                    menu()
                    return
            else:
                self.exist_vocab_path = True
        
        print("[SYSTEM] Data check completed.")
        self.start_training()

    def start_training(self):
        if self.exist_vocab_path == True:
            print("\n# Vocab Training\n[1] Learn vocab\n[2] Create new deck\n[3] Edit a deck\n[B] Back\n")
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
        with open(self.vocab_path, "r") as f:
            data = json.load(f)
            decks = data["decks"]
            
            deck_names = []
            for i in decks:
                deck_names.append(list(i)[0])
        
        deck_name = input("#Create new deck\nWhich name should the deck have?\n> ") 
        for i in deck_names:
            if deck_name == i:
                print(f"[ERROR] '{deck_name}' is already in use. Try again.")
                self.create_deck()
                return
        print(f"Deck name will be: {deck_name}\n")

        print("Now add vocab.")
        vocab_originals, vocab_translations, vocab_dict = [], [], []
        while True:
            print(f"Card #{len(vocab_originals) + 1}")
            output = self.create_voc()
            vocab_originals.append(output[0]), vocab_translations.append(output[1])
            answer = input("Do you want to create another card? [y/n]\n> ")
            if answer == "n":
                vocab_dict = dict(zip(vocab_originals, vocab_translations))
                break
        
        with open(self.vocab_path, "w") as f:
            new_deck = {deck_name: {"vocab" : vocab_dict}}
            decks.append(new_deck)
            data = {"decks" : decks}
            json.dump(data, f, indent=4)
            print(f"[SUCCESS] Successfully created '{deck_name}'")

    def create_voc(self):
        original = input("Original    > ")
        translation = input("Translation > ")
        
        answer = input("Do you want to make any changes? [y/n]\n> ")
        if answer == "y":
            return self.create_voc()
        return [original, translation]
    
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
