class JanSoweliConverter:

    def __init__(self, vocab):
        self.vocab = vocab
        self.jan = self.vocab('jan')
        self.soweli = self.vocab('soweli')

    def get_target_token(self, token):
        if token == self.jan:
            return self.soweli
        elif token == self.soweli:
            return self.jan
        else:
            return token

    def __call__(self, source):
        target = [
            self.get_target_token(token)
            for token
            in source]
        return target

