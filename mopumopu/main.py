from argparse import ArgumentParser
import sys
import time
import torch
from ponalm.vocab import load_vocab
from ponalm.model.lm import PonaLM
from .soweli import Soweli
from .twiman import Twiman
from .scheduler import Scheduler

import logging
from logging import getLogger
logging.basicConfig(
        format = '[%(asctime)s] (%(levelname)s) %(message)s',
        datefmt = '%Y/%m/%d %H:%M:%S',
        level = logging.INFO,
        stream = sys.stdout)
logger = getLogger(__name__)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--checkpoint', default = 'lm.pt')
    parser.add_argument('--vocab', default = 'vocab.txt')
    parser.add_argument('--hidden-dim', type = int, default = 256)
    parser.add_argument('--rnn-dim', type = int, default = 256)
    parser.add_argument('--num-layers', type = int, default = 64)
    parser.add_argument('--soweli-th', type = float, default = 0.5)
    parser.add_argument('--tweet-p', type = float, default = 0.8)
    parser.add_argument('--tweet-t', type = float, default = 1.0)
    parser.add_argument('--tweet-interval-minutes', type = int, default = 30)
    parser.add_argument('--test', action = 'store_true')
    parser.add_argument('--consumer-key')
    parser.add_argument('--consumer-secret')
    parser.add_argument('--access-token')
    parser.add_argument('--access-token-secret')
    return parser.parse_args()


def get_soweli(args):
    vocab = load_vocab(args.vocab)
    model = PonaLM(
            len(vocab),
            args.hidden_dim,
            args.rnn_dim,
            0, 0,
            args.num_layers,
            padding_idx = vocab.pad)
    model.load_state_dict(torch.load(args.checkpoint, map_location = 'cpu'))
    if torch.cuda.is_available():
        model = model.cuda()
    model.eval()

    soweli = Soweli(
            model,
            vocab,
            soweli_th = args.soweli_th,
            tweet_p = args.tweet_p,
            tweet_t = args.tweet_t)
    return soweli


def get_twiman(args):
    soweli = get_soweli(args)
    twiman = Twiman(
            soweli,
            args.consumer_key,
            args.consumer_secret,
            args.access_token,
            args.access_token_secret)
    return twiman


def bot_main(args):
    twiman = get_twiman(args)
    scheduler = Scheduler(
            twiman,
            tweet_interval_minutes = args.tweet_interval_minutes)

    while True:
        scheduler.run()
        time.sleep(1)


def bot_test(args):
    twiman = get_twiman(args)
    twiman.tweet()


def main():
    args = parse_args()
    if args.test:
        bot_test(args)
    else:
        bot_main(args)

