import re
import tweepy

from logging import getLogger
logger = getLogger(__name__)

def get_api(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret):

    auth = tweepy.OAuthHandler(
            consumer_key,
            consumer_secret)
    auth.set_access_token(
            access_token,
            access_token_secret)
    api = tweepy.API(auth)
    return api


class Twiman:

    def __init__(
            self,
            soweli,
            moses,
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret):

        self.soweli = soweli
        self.moses = moses
        self.api = get_api(
                consumer_key,
                consumer_secret,
                access_token,
                access_token_secret)

        timeline = self.api.mentions_timeline()
        self.last = timeline[0].id

    def tweet(self):
        try:
            text = self.soweli.tweet()
            self.api.update_status(status = text)
            logger.info('tweet: {}'.format(text))
        except Exception as e:
            logger.info('fail: ', e)

    def update_last(self):
        try:
            timeline = self.api.mentions_timeline(since_id = self.last)
        except:
            timeline = []

        if timeline != []:
            self.last = timeline[0].id
        return timeline

    def reply_for_mention(self, mention):
        utt = re.sub(r'@[^ ]+ ', '', mention.text)
        name = mention.user.screen_name
        stid = mention.id

        logger.info(utt)
        if utt.strip().startswith('><'):
            text = re.sub(r'><', '', utt.strip())
            text = self.moses.reply(text)
            if len(text) <= 0 or len(text) >= 120:
                text = 'mu??? mi ken ala ante e toki sina.'
        else:
            text = self.soweli.reply(utt)
            if len(text) <= 1 or len(text) >= 200:
                text = 'mu.'

        status = '@{} {}'.format(name, text)
        self.api.update_status(status = status, in_reply_to_status_id = stid)
        logger.info('reply: {} ({})'.format(status, stid))

    def reply(self):
        timeline = self.update_last()

        for mention in timeline:
            try:
                self.reply_for_mention(mention)
            except Exception as e:
                logger.info('fail: ', e)

