import random as rd
from .jansoweli import JanSoweliConverter
from ponalm.generation.sampler import SentenceSampler
from ponalm.preproc.preproc import LMPreproc
from ponalm.preproc.postproc import LMPostproc

from logging import getLogger
logger = getLogger(__name__)


class Soweli:

    def __init__(
            self,
            model,
            vocab,
            soweli_th = 0.5,
            tweet_p = 0.8,
            tweet_t = 1.0):

        self.model = model
        self.vocab = vocab
        self.tweet_p = tweet_p
        self.tweet_t = tweet_t

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
        sent = self.generate()

        if (rd.random() < self.soweli_th) and self.jansoweli_cond(sent):
            sent = self.jansoweli(sent)

        sent = self.join_sent(sent)
        sent = self.postproc(sent)
        return sent

    def generate(self):
        while True:
            sent, probs = self.sampler(
                temperature = self.tweet_t,
                top_p = self.tweet_p)
            text = self.join_sent(sent)
            logger.info('generate: {}'.format(text))
            if len(text) <= 120:
                break
        return sent

