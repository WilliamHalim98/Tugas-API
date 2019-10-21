import tweepy
import csv
import json
import datetime

# me-load Twitter API credentials yang sudah dituliskan di file twitter_credentials.json

with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']
    
#menampilkan seluruh tweets pada timeline user
def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    all_tweets = []
    # maksimal 100 tweets
    new_tweets = api.user_timeline(screen_name=screen_name, count=100)
    # Melihat recent tweets
    all_tweets.extend(new_tweets)

    # save id of 1 less than the oldest tweet
    oldest_tweet = all_tweets[-1].id - 1

    while len(new_tweets) :
        new_tweets = api.user_timeline(screen_name=screen_name,
        count=100, max_id=oldest_tweet)

        # menyimpan tweet terbaru
        all_tweets.extend(new_tweets)

        oldest_tweet = all_tweets[-1].id - 1
        print ('...%s tweets yang sudah didownload' % len(all_the_tweets))

        outtweets = [[tweet.id_str, tweet.created_at,
        tweet.text.encode('utf-8')] for tweet in all_tweets]

    with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(outtweets)

    if __name__ == '__main__':
        get_all_tweets(input("Menginput twitter handle dari user yang tweetnya hendak ditampilkan :"))
        
#menampilkan informasi akun user
class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)
api = tweepy.API(auth)
twitterStream = Stream(auth,TweetListener())
test = api.lookup_users(user_ids=['17006157','59145948','157009365'])
for user in test:
    print (user.screen_name)
    print (user.name)
    print (user.description)
    print (user.followers_count)
    print (user.statuses_count)
    print (user.url)
#menampilkan informasi berdasarkan mentions
def save_mentions(self, tweet):
    for mention in tweet['entities']['user_mentions']:
        screen_name = USERS.find_one({'twitter': mention['screen_name']})
        if AUTO_REPLY and not DEVELOPER_MODE:
            # Send message to user if not in DEVELOPER_MODE
            send_message = 'Sending message to @%s. %s' % (tweet['user']['screen_name'], datetime.datetime.now())
            logging.info(send_message)
            if VERBOSE:
                print (send_message)
                message_thread = TweetMaker(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                                            tweet['user']['screen_name'])
                message_thread.start()
            # If no user (mention) was found in our database let's save it
            if not screen_name:
                USERS.insert({
                    'twitter': mention['screen_name'],
                    'created': datetime.datetime.utcnow(),
                    'mentioned_by': tweet['user']['screen_name']
                })
                added_message = 'Added @%s! %s' % (mention['screen_name'], datetime.datetime.now())
                logging.info(added_message)
                if VERBOSE:
                    print (added_message)
