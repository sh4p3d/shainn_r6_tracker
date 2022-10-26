import tweepy
class twitterApi:
    def __init__(self):
        self.api_key = "s20mg1xirnsiz3kH7pkwIGc5l"
        self.api_key_secret = "2jePRD0Tr7Sh8u3GrWHkEVTiqGUrpVhJMogEJpTyLVYCOFMRf2"
        self.access_token = "1418629982998482949-MDLcU0PUaXWPcIVsBinIeAVaw0sKif"
        self.access_token_secret = "bXQYlgtOp0ddeDWHDj4lseSHnM5OFgJ1no0Sg38hATqRJ"
        authenticator = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        authenticator.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(authenticator, wait_on_rate_limit=True)
        user = user = api.get_user(screen_name="Rainbow6Game")
        self.tweets_user = api.user_timeline(user_id=user.id)
    def getLatestTweetText(self):
        return self.tweets_user[0].text
    def getLatestTweetURL(self):
        return f"https://fxtwitter.com/Rainbow6Game/status/{self.tweets_user[0].id}"
    def getLatestTweetId(self):
        return self.tweets_user[0].id
            