from ilonimi import (
        Normalizer,
        Tokenizer,
        Kanaizer)

class Kana:

    def __init__(self):
        self.normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        self.kanaizer = Kanaizer()

    def pona_to_kana(self, x):
        x = self.normalizer(x)
        x = self.tokenizer(x)
        x = self.kanaizer(x)
        return x

