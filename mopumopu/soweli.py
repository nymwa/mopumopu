import random as rd
from .jansoweli import JanSoweliConverter
from ponapt.generation.sampler import SentenceSampler
from ponapt.preproc import LMPreproc
from ponapt.postproc import LMPostproc

class Soweli:

    def __init__(
            self,
            model,
            vocab,
            soweli_th = 0.5,
            tweet_p = 0.8,
            reply_p = 0.5):

        self.model = model
        self.vocab = vocab
        self.tweet_p = tweet_p
        self.reply_p = reply_p

        self.soweli_th = soweli_th
        self.jansoweli = JanSoweliConverter(self.vocab)

        self.sampler = SentenceSampler(self.vocab, self.model)
        self.preproc = LMPreproc()
        self.postproc = LMPostproc()


    def tweet(self):
        sent = self.sampler(top_p = self.tweet_p)

        if rd.random() < self.soweli_th:
            sent = self.jansoweli(sent)

        sent = ' '.join([self.vocab[x] for x in sent])
        sent = self.postproc(sent)
        return sent

    def reply(self, utt):
        utt = self.preproc(utt)
        sent = '"{}" "'.format(utt)
        sent = self.preproc(sent)
        sent = [self.vocab(token) for token in sent.split()]
        len_utt = len(sent)
        sent = self.jansoweli(sent)
        sent = self.sampler(
                sent = sent,
                top_p = self.reply_p,
                terminal = {self.vocab('"')},
                min_len = len_utt + 1)
        sent = sent[len_utt - 1 :]
        sent = self.jansoweli(sent)
        sent = ' '.join([self.vocab[x] for x in sent])
        sent = self.postproc(sent)
        sent = sent.strip('"').strip()
        return sent

