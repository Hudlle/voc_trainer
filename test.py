import json
import os

class TestObject():
    def __init__(self):
        self.data_path = os.path.join(os.getcwd(), "data")
        self.vocab_path = os.path.join(self.data_path, "vocab_decks.json")

    def debug(self):
        with open(self.vocab_path, "r") as f:
            data = json.load(f)
            decks = data["decks"]

            for deck in decks:
                print(f"[DEBUG] Deck : {deck}")
                
                trying = list(deck.values())
                print(f"[TRY] {trying}")

                #need some nested for loops so i can assign vocab_originals and vocab_translations again

if __name__ == "__main__":
    obj = TestObject()
    obj.debug()
