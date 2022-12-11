import random as rd
from .jansoweli import JanSoweliConverter
from ponalm.generation.sampler import SentenceSampler
from ponalm.preproc.preproc import LMPreproc
from ponalm.preproc.postproc import LMPostproc

class Soweli:

    def __init__(
            self,
            model,
            vocab,
            soweli_th = 0.5,
            tweet_p = 0.8,
            reply_p = 0.5,
            tweet_t = 1.0,
            reply_t = 1.0):

        self.model = model
        self.vocab = vocab
        self.tweet_p = tweet_p
        self.reply_p = reply_p
        self.tweet_t = tweet_t
        self.reply_t = reply_t

        self.soweli_th = soweli_th
        self.jansoweli = JanSoweliConverter(self.vocab)

        self.sampler = SentenceSampler(self.vocab, self.model)
        self.preproc = LMPreproc()
        self.postproc = LMPostproc()

    def join_sent(self, sent):
        return ' '.join([self.vocab[x] for x in sent])

    def jansoweli_cond(self, sent):
        sent = self.join_sent(sent)
        name_list = ['Nima', 'Mopumopu', 'Mopu', 'Nasa', 'Lunin']
        return all(name not in sent for name in name_list)

    def tweet(self):
        sent = self.sampler(
                temperature = self.tweet_t,
                top_p = self.tweet_p)

        if (rd.random() < self.soweli_th) and self.jansoweli_cond(sent):
            sent = self.jansoweli(sent)

        sent = self.join_sent(sent)
        sent = self.postproc(sent)
        return sent

    def reply(self, utt):
        utt = self.preproc(utt)
        sent = '" {} " "'.format(utt)
        sent = self.preproc(sent)
        sent = [self.vocab(token) for token in sent.split()]
        len_utt = len(sent)
        if self.jansoweli_cond(sent):
            sent = self.jansoweli(sent)
        sent = self.sampler(
                sent = sent,
                temperature = self.reply_t,
                top_p = self.reply_p,
                terminal = {self.vocab('"')},
                min_len = len_utt + 1)
        sent = sent[len_utt - 1 :]
        if self.jansoweli_cond(sent):
            sent = self.jansoweli(sent)
        sent = self.join_sent(sent)
        sent = self.postproc(sent)
        sent = sent.strip('"').strip()

        if sent.startswith('li '):
            sent = 'ni ' + sent
        if sent.startswith('. '):
            sent = sent[2:]

        return sent

