from argparse import ArgumentParser
import sys
import time
import torch
from ponapt.vocab import load_vocab
from ponapt.lm import LM
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
    parser.add_argument('--checkpoint', default = 'bert.pt')
    parser.add_argument('--vocab', default = 'vocab.txt')
    parser.add_argument('--hidden-dim', type = int, default = 512)
    parser.add_argument('--nhead', type = int, default = 8)
    parser.add_argument('--feedforward-dim', type = int, default = 2048)
    parser.add_argument('--dropout', type = float, default = 0.3)
    parser.add_argument('--attention-dropout', type = float, default = 0.2)
    parser.add_argument('--activation-dropout', type = float, default = 0.2)
    parser.add_argument('--num-layers', type = int, default = 24)
    parser.add_argument('--max-len', type = int, default = 256)
    parser.add_argument('--soweli-th', type = float, default = 0.5)
    parser.add_argument('--tweet-p', type = float, default = 0.8)
    parser.add_argument('--reply-p', type = float, default = 0.3)
    parser.add_argument('--test', action = 'store_true')
    parser.add_argument('--consumer-key')
    parser.add_argument('--consumer-secret')
    parser.add_argument('--access-token')
    parser.add_argument('--access-token-secret')
    return parser.parse_args()


def get_soweli(args):
    vocab = load_vocab(args.vocab)
    model = LM(
            len(vocab),
            args.hidden_dim,
            args.nhead,
            args.feedforward_dim,
            args.dropout,
            args.attention_dropout,
            args.activation_dropout,
            args.num_layers,
            padding_idx = vocab.pad,
            max_len = args.max_len)
    model.load_state_dict(torch.load(args.checkpoint, map_location = 'cpu'))
    if torch.cuda.is_available():
        model = model.cuda()
    model.eval()

    soweli = Soweli(
            model,
            vocab,
            soweli_th = args.soweli_th,
            tweet_p = args.tweet_p,
            reply_p = args.reply_p)
    return soweli


def bot_main(args):
    soweli = get_soweli(args)
    twiman = Twiman(
            soweli,
            args.consumer_key,
            args.consumer_secret,
            args.access_token,
            args.access_token_secret)
    scheduler = Scheduler(twiman)

    while True:
        scheduler.run()
        time.sleep(1)


def test(args):
    soweli = get_soweli(args)
    for _ in range(10):
        x = soweli.tweet()
        print(x)
        y = soweli.reply(x)
        print(y)
        print('---')


def main():
    args = parse_args()
    if args.test:
        test(args)
    else:
        bot_main(args)

