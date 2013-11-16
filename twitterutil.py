import twitter
import ConfigParser 

class TwitterUtil(object):
    def __init__(self, config='webapp.conf'):
        _config = ConfigParser.ConfigParser()
        _config.read(config)
        self._api = twitter.Api(
                consumer_key = _config.get('twitter', 'consumer_key'),
                consumer_secret = _config.get('twitter', 'consumer_secret'),
                access_token_key = _config.get('twitter', 'access_token_key'),
                access_token_secret = _config.get('twitter', 'access_token_secret'))


    def tweet(self, status):
        self._api.PostUpdate(status)

    def tweet_img(self, status, image_path):
        self._api.PostMedia(status, image_path)

def _test():
    import datetime as dt
    tu = TwitterUtil()
    tu.tweet('Test message [%s]' % (dt.datetime.now(),))

if __name__ == '__main__':
    _test()
