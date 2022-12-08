class AddNi:

    def __init__(self, vocab):
        self.vocab = vocab
        self.ni = self.vocab('ni')
        self.li = self.vocab('li')

    def __call__(self, xs):
        if xs[0] == self.li:
            xs = [self.ni] + xs
        return xs

