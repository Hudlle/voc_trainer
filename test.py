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
                
                vocab_originals, vocab_translations = [], []
                for i in list(deck.values())[0].values():
                    for j in i.items():
                        vocab_originals.append(j[0])
                        vocab_translations.append(j[1])

                print(vocab_originals, vocab_translations, sep="\n")

if __name__ == "__main__":
    obj = TestObject()
    obj.debug()
