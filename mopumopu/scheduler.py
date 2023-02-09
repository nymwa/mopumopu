from datetime import datetime, timedelta

from logging import getLogger
logger = getLogger(__name__)

class Scheduler:

    def __init__(self, twiman, tweet_interval_minutes = 30, reply_interval_seconds = 30):
        self.twiman = twiman
        self.tweet_interval_minutes = tweet_interval_minutes
        self.reply_interval_seconds = reply_interval_seconds

        now = datetime.now()
        self.next_tweet_time = datetime(now.year, now.month, now.day, now.hour)
        self.next_reply_time = datetime(now.year, now.month, now.day, now.hour, now.minute)
        self.make_next_tweet_time()
        self.make_next_reply_time()

    def make_next_tweet_time(self):
        while self.next_tweet_time < datetime.now():
            self.next_tweet_time += timedelta(minutes = self.tweet_interval_minutes)
        logger.debug('next tweet: {}'.format(self.next_tweet_time))

    def make_next_reply_time(self):
        while self.next_reply_time < datetime.now():
            self.next_reply_time += timedelta(seconds = self.reply_interval_seconds)
        logger.debug('next reply: {}'.format(self.next_reply_time))

    def run(self):

        if self.next_tweet_time < datetime.now():
            self.make_next_tweet_time()
            self.twiman.tweet()

        if self.next_reply_time < datetime.now():
            self.make_next_reply_time()
            self.twiman.reply()

