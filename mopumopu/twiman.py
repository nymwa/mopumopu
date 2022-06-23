import re
import tweepy
from xml.sax.saxutils import unescape

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
            kana,
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret):

        self.soweli = soweli
        self.moses = moses
        self.kana = kana
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

    def trial_for_mention(self, utt):
        for _ in range(3):
            text = self.soweli.reply(utt)
            if 1 < len(text) < 200:
                return text
        return 'mu.'

    def reply_for_mention(self, mention):
        utt = re.sub(r'@[^ ]+ ', '', mention.text)
        utt = unescape(utt)
        name = mention.user.screen_name
        stid = mention.id

        if name == 'soweli_mopumopu':
            logger.info('self replying')
            return

        if utt.strip().startswith('><'):
            text = re.sub(r'><', '', utt.strip())
            text = self.moses.reply(text)
            if len(text) <= 0 or len(text) >= 120:
                text = 'mu??? mi ken ala ante e toki sina.'
        elif utt.strip().startswith('もぷ'):
            text = re.sub(r'^もぷ', '', utt.strip())
            text = self.kana.pona_to_kana(text)
        else:
            text = self.trial_for_mention(utt)

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

