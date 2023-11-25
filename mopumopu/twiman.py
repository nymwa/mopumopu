import tweepy

from logging import getLogger
logger = getLogger(__name__)


def get_client(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret):

    client = tweepy.Client(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            access_token = access_token,
            access_token_secret = access_token_secret)
    return client


class Twiman:

    def __init__(
            self,
            soweli,
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret):

        self.soweli = soweli
        self.client = get_client(
                consumer_key,
                consumer_secret,
                access_token,
                access_token_secret)

    def tweet(self):
        try:
            text = self.soweli.tweet()
            self.client.create_tweet(text = text)
            logger.info('tweet: {}'.format(text))
        except Exception as e:
            logger.info('fail: ', e)

