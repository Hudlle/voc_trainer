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
        self.training_cmds = {"1" : self.learn_vocab, "2" : self.create_deck, "3" : self.edit_deck, "4" : self.delete_deck}

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
            if os.path.exists(self.vocab_path) == False or os.path.getsize(self.vocab_path) == 0:
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
            print("\n# Vocab Training\n[1] Learn vocab\n[2] Create new deck\n[3] Edit a deck\n[4] Delete a deck\n[B] Back\n")
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
        with open(self.vocab_path, "r") as f:
            data = json.load(f)
            decks = data["decks"]

            deck_names = []
            for i in decks:
                print(f"#{decks.index(i) + 1} '{list(i)[0]}'")
                deck_names.append(list(i)[0])
            
            answer = input("Which deck would you like to learn? [index/b]\n> ")
            if answer == "b" or answer == "B":
                self.start_training()
                return
            
            vocab_originals, vocab_translations, vocab_list = self.get_vocab(data, int(answer) - 1)

        random_indexes = random.sample(range(0, len(vocab_originals)), len(vocab_originals))
        for i in vocab_list:
            answer = input(f"Card #{vocab_list.index(i) + 1}\nOriginal : {i[0]}\nTranslation > ")
            if answer == "b" or answer == "B":
                break
            
            error_list = []
            for j in list(answer):
                if j != i[1][list(answer).index(j)]:
                    error_list.append("X")
                else:
                    error_list.append(" ")
            
            print(f"\nCorrect answer : {i[1]}\nError chart :    {''.join(error_list)}\nYour input :     {answer}")

            #commit damit ich meine streak halte 2
            

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
        print(f"Deck name will be: {deck_name}. Don't worry if you've typed something wrong, you can change it later.\n")

        print("Now add vocab.")
        vocab_originals, vocab_translations, vocab_list = [], [], []
        while True:
            print(f"Card #{len(vocab_originals) + 1}")
            output = self.create_voc()
            vocab_originals.append(output[0]), vocab_translations.append(output[1])
            answer = input("Do you want to create another card? [y/n]\n> ")
            if answer == "n":
                vocab_list = dict(zip(vocab_originals, vocab_translations))
                break
        
        with open(self.vocab_path, "w") as f:
            new_deck = {deck_name: {"vocab" : vocab_list}}
            decks.append(new_deck)
            data = {"decks" : decks}
            json.dump(data, f, indent=4)
            print(f"[SUCCESS] Successfully created '{deck_name}'")

    def edit_deck(self):
        with open(self.vocab_path, "r") as f:
            data = json.load(f)
            decks = data["decks"]

            deck_names = []
            for i in decks:
                print(f"#{decks.index(i) + 1} '{list(i)[0]}'")
                deck_names.append(list(i)[0])

            deck_index = input("Which deck would you like to edit? [<index>/b]\n> ")
            if deck_index == "b" or deck_index == "B":
                self.start_training()
                return
            if int(deck_index) > len(deck_names) or int(deck_index) < len(deck_names):
                print(f"[ERROR] Index number is higher than decks count. Try again.")
                self.edit_deck()
                return

            vocab_originals, vocab_translations, vocab_list = self.get_vocab(data, int(deck_index) - 1)
        
        with open(self.vocab_path, "w") as f:
            answer = input("What would you like to change?\n[1] Deck name\n[2] Vocab\n[B] Back\n> ")
            if answer == "b" or answer == "B":
                self.edit_deck()
                return
            if answer == "1":
                new_name = input("New name > ")
                
                vocab_dict = dict(zip(vocab_originals, vocab_translations))
                new_deck = {new_name: {"vocab" : vocab_dict}}
                decks.pop(int(deck_index) - 1)
                decks.insert(int(deck_index) - 1, new_deck)
                json.dump(data, f, indent=4)
                print(f"[SUCCESS] Successfully changed deck name to '{new_name}'")
            
            elif answer == "2":
                answer = input(f"What would you like to do?\n[1] Create a new vocabulary\n[2] Edit an existing vocabulary\n[3] Delete a vocabulary\n[B] Back\n> ")
                if answer == "b" or answer == "B":
                    self.edit_deck()
                    return

                if answer == "1":
                    while True:
                        print(f"Card #{len(vocab_originals)} in deck '{list(i)[0]}'")
                        output = self.create_voc()
                        vocab_originals.append(output[0]), vocab_translations.append(output[1])
                        answer = input("Do you want to create another card? [y/n]\n> ")
                        if answer == "n":
                            vocab_dict = dict(zip(vocab_originals, vocab_translations))
                            break
                    
                    new_deck = {deck_names[int(deck_index) - 1] : {"vocab" : vocab_dict}} 
                    decks.pop(int(deck_index) - 1)
                    decks.insert(int(deck_index) - 1, new_deck)

                    json.dump(data, f, indent=4)
                    print(f"[SUCCESS] Successfully created new vocabulary.")

                elif answer == "2":
                    # print it out enumerated
                    for i in vocab_list:
                        print(f"#{vocab_list.index(i) + 1} {i[0]} | {i[1]}")

                    # index single vocab input
                    voc_index = input("Which vocabulary would you like to edit? [index]\n> ")

                    # print out single vocab and ask what should be changed [original or translation]
                    print(f"[1] Original : {vocab_list[int(voc_index) - 1][0]}\n[2] Translation : {vocab_list[int(voc_index) - 1][1]}")
                    answer = input("What would you like to change? [index]\n> ")

                    # get new entry
                    if answer == "1":
                        new_original = input("New original > ")
                        vocab_originals.pop(int(voc_index) - 1)
                        vocab_originals.insert(int(voc_index) - 1, new_original)
                    elif answer == "2":
                        new_translation = input("New translation > ")
                        vocab_translations.pop(int(voc_index) - 1)
                        vocab_translations.insert(int(voc_index) - 1, new_translation)
                    else:
                        print(f"[ERROR] '{answer}' is not a valid input. Try again.")
                        self.edit_deck()
                        return

                    # insert it into vocab and data
                    vocab_dict = dict(zip(vocab_originals, vocab_translations))
                    new_deck = {deck_names[int(deck_index) - 1] : {"vocab" : vocab_dict}} 
                    decks.pop(int(deck_index) - 1)
                    decks.insert(int(deck_index) - 1, new_deck)
                    # write it to file and print out success message
                    json.dump(data, f, indent=4)
                    print(f"[SUCCESS] Successfully changed vocabulary.")
                        
                elif answer == "3":
                    for i in vocab_list:
                        print(f"#{vocab_list.index(i) + 1} {i[0]} | {i[1]}")
                    voc_index = input("Which vocabulary would you like to delete? [index]\n> ")
                    vocab_originals.pop(int(voc_index) - 1)
                    vocab_translations.pop(int(voc_index) - 1)
                    
                    vocab_dict = dict(zip(vocab_originals, vocab_translations))
                    new_deck = {deck_names[int(deck_index) - 1] : {"vocab" : vocab_dict}}
                    decks.pop(int(deck_index) - 1)
                    decks.insert(int(deck_index) - 1, new_deck)
                    
                    json.dump(data, f, indent=4)
                    print(f"[SUCCESS] Successfully deleted vocabulary.")
            else:
                print(f"[ERROR] '{answer}' is not a valid input. Try again.")
                self.edit_deck()
                return
    
    def delete_deck(self):
        with open(self.vocab_path, "r") as f:
            data = json.load(f)
            decks = data["decks"]
            
            deck_names = []
            for i in decks:
                print(f"#{decks.index(i) + 1} '{list(i)[0]}'")
                deck_names.append(list(i)[0])

            answer = input("Which deck would you like to delete? [<index>/b]\n> ")
            if answer == "b" or answer == "B":
                self.start_training()
                return
            elif int(answer) > len(deck_names) or int(answer) < len(deck_names):
                print(f"[ERROR] Index number is higher than decks count. Try again.")
                self.delete_deck()
                return

        with open(self.vocab_path, "w") as f:
            del data["decks"][int(answer) - 1]
            json.dump(data, f, indent=4)
            print(f"[SUCCESS] Successfully deleted deck.")
    
    def create_voc(self):
        original = input("Original > ")
        translation = input("Translation > ")
        
        answer = input("Do you want to make any changes? [y/n]\n> ")
        if answer == "y":
            return self.create_voc()
        return [original, translation]
    
    def get_vocab(self, data, deck_index):
        decks = data["decks"]
        
        for i in decks:
            if int(deck_index) == decks.index(i):            
                vocab_originals, vocab_translations, vocab_list = [], [], []
                for j in list(i.values())[0].values():
                    for k in j.items():
                        vocab_originals.append(k[0])
                        vocab_translations.append(k[1])
                vocab_list = list(zip(vocab_originals, vocab_translations))
        
        return [vocab_originals, vocab_translations, vocab_list]
            
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