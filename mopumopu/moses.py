import re
import xmlrpc.client as xmlrpc_client
from ilonimi import (
        Normalizer,
        Tokenizer)
from sacremoses import MosesDetokenizer

class Moses:

    def __init__(
            self,
            port):

        self.client = xmlrpc_client.ServerProxy(
                'http://127.0.0.1:{}'.format(port))
        self.normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        self.detokenizer = MosesDetokenizer()

    def translate(self, text):
        param = {'text': text}
        try:
            text = self.client.translate(param)['text']
        except:
            text = None
        return text

    def reply(self, source):
        text = self.normalizer(source)
        text = self.tokenizer(text)
        text = self.translate(text)
        text = self.detokenizer.detokenize(text.split())
        return text

