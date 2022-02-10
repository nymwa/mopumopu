from datetime import datetime, timedelta

from logging import getLogger
logger = getLogger(__name__)

class Scheduler:

    def __init__(self, twiman):
        self.twiman = twiman

        now = datetime.now()
        self.next_tweet_time = datetime(now.year, now.month, now.day, now.hour)
        self.next_reply_time = datetime(now.year, now.month, now.day, now.hour, now.minute)
        self.make_next_tweet_time()
        self.make_next_reply_time()

    def make_next_tweet_time(self):
        while self.next_tweet_time < datetime.now():
            self.next_tweet_time += timedelta(minutes = 15)
        logger.debug('next tweet: {}'.format(self.next_tweet_time))

    def make_next_reply_time(self):
        while self.next_reply_time < datetime.now():
            self.next_reply_time += timedelta(seconds = 20)
        logger.debug('next reply: {}'.format(self.next_reply_time))

    def run(self):

        if self.next_tweet_time < datetime.now():
            self.make_next_tweet_time()
            self.twiman.tweet()

        if self.next_reply_time < datetime.now():
            self.make_next_reply_time()
            self.twiman.reply()

